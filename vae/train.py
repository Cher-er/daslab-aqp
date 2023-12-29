import matplotlib.pyplot as plt
from vae.VAE import *
import time
from torch import optim
import os
from config.config import VAEConfig
import schema.flights


def train_vae():

    config = VAEConfig().get_config()
    input_file = config['input_file']
    output_dir = config['output_dir']
    seed = config['seed']
    batch_size = config['batch_size']
    epochs = config['epochs']
    log_interval = config['log_interval']
    latent_dim = config['latent_dim']
    neuron_list = config['neuron_list']
    rejection = config['rejection']

    use_cuda = torch.cuda.is_available()
    print("[use_cuda]: ", use_cuda)

    ### Set the seeds. Default: 42
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

    # Specify which are categorical and which are numeric
    # We don't care about header, so delete the header from input if it has.
    # After reading the input, this cell converts the input to encoding.
    print("Reading INPUT File")
    orig_df = pd.read_csv(input_file)
    orig_df = orig_df.dropna().reset_index(drop=True)

    # if orig_df.shape[0] >= 1000000:
    #     df = orig_df.sample(1000000).reset_index(drop=True)
    # else:
    #     df = orig_df
    df = orig_df

    print("Original", orig_df.shape)
    print("Sampled", df.shape)
    cols = df.columns
    cat_cols, num_cols = [], []
    for k, v in schema.flights.schema.items():
        if v == "c":
            cat_cols.append(k)
        elif v == "n":
            num_cols.append(k)
    org_input_dim = len(cat_cols) + len(num_cols)

    # hot_hot, num_num and hot_num three supported encoding type for categorical_numerical data
    encoding_type = "hot_num"  # categorical hot and numeric column in numeric form

    print("Transforming Train/Test")
    if os.path.exists(os.path.join(output_dir, 'data.pkl')):
        x_train, x_test = pickle.load(open(os.path.join(output_dir, 'data.pkl'), 'rb'))
    else:
        x_train, x_test = transform_forward(config, df, num_cols, cat_cols, encoding_type)
        pickle.dump((x_train, x_test), open(os.path.join(output_dir, 'data.pkl'), 'wb'), protocol=4)
    print("Train Shape: ", x_train.shape, "Test Shape", x_test.shape)

    start = time.time()

    model = VAE(x_train.shape[1], latent_dim, neuron_list)

    if use_cuda:
        dev_gpu = "cuda"  ## Yes, it uses a GPU.
        device_gpu = torch.device(dev_gpu)
        model.to(device_gpu)
        # model = torch.nn.DataParallel(model)
        print("Model to GPU")
        x_train = torch.from_numpy(x_train)
        # x_train = torch.from_numpy(x_train).to(device_gpu)
        # x_test = torch.from_numpy(x_test).to(device_gpu)

    optimizer = optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)
    loss = []
    bestLoss = -1
    start_epoch = 0

    if os.path.exists(os.path.join(output_dir, 'model_state')):
        checkpoint = torch.load(os.path.join(output_dir, 'model_state'))
        model.load_state_dict(checkpoint['state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer'])
        start_epoch = checkpoint['epoch']
        bestLoss = checkpoint['bestLoss']
        loss = pickle.load(open(os.path.join(output_dir, 'loss.pkl'), 'rb'))

    for epoch in tqdm(range(start_epoch + 1, epochs + 1)):
        currentLoss = train(model, optimizer, epoch, x_train, log_interval, batch_size, org_input_dim, rejection)
        loss.append(currentLoss)
        if bestLoss < 0 or (currentLoss < bestLoss):
            torch.save(model, os.path.join(output_dir, 'model.pt'))
            bestLoss = currentLoss

        if epoch % 10 == 0:
            t_val = calculate_t(model, x_train,
                                batch_size)  ## The value of T computed here is used during sample generation.
            time_taken = time.time() - start

            pickle.dump(t_val, open(os.path.join(output_dir, 't-val.pkl'), 'wb'))
            pickle.dump(loss, open(os.path.join(output_dir, 'loss.pkl'), 'wb'))
            pickle.dump(time_taken, open(os.path.join(output_dir, 'time_taken.pkl'), 'wb'))
            plt.plot(loss)
            plt.savefig(os.path.join(output_dir, 'loss.png'))

            state = {'epoch': epoch, 'state_dict': model.state_dict(), 'optimizer': optimizer.state_dict(),
                     'bestLoss': bestLoss}
            torch.save(state, os.path.join(output_dir, 'model_state'))

    t_val = calculate_t(model, x_train, batch_size)  ## The value of T computed here is used during sample generation.
    print("90th Percentile value of T", t_val)
    print("Training Ends")
    time_taken = time.time() - start

    pickle.dump(t_val, open(os.path.join(output_dir, 't-val.pkl'), 'wb'))
    pickle.dump(loss, open(os.path.join(output_dir, 'loss.pkl'), 'wb'))
    pickle.dump(time_taken, open(os.path.join(output_dir, 'time_taken.pkl'), 'wb'))
    plt.plot(loss)
    plt.savefig(os.path.join(output_dir, 'loss.png'))

    state = {'epoch': epochs, 'state_dict': model.state_dict(), 'optimizer': optimizer.state_dict(),
             'bestLoss': bestLoss}
    torch.save(state, os.path.join(output_dir, 'model_state'))
