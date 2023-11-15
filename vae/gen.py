from vae.VAE import *
from config.config import VAEConfig
import os


def gen_sample():
    config = VAEConfig().get_config()
    output_dir = config['output_dir']
    num_samples = config['num_samples']
    seed = config['seed']
    gpus = config['gpus']
    latent_dim = config['latent_dim']

    os.environ['CUDA_VISIBLE_DEVICES'] = str(gpus)
    use_cuda = torch.cuda.is_available()

    ### Set the seeds. Default: 42
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

    model = torch.load(os.path.join(output_dir, 'model.pt'))

    device_gpu = None
    if use_cuda:
        dev_gpu = "cuda"
        device_gpu = torch.device(dev_gpu)
        model.to(device_gpu)

    if os.path.exists(os.path.join(output_dir, 'data.pkl')):
        x_train, x_test = pickle.load(open(os.path.join(output_dir, 'data.pkl'), 'rb'))
    else:
        print("Training Data Doesn't exist.")
        exit(0)
        return

    print(x_train.shape)
    x_train_sampled = x_train[np.random.randint(x_train.shape[0], size=num_samples), :]
    print(x_train_sampled.shape)
    x_train = torch.from_numpy(x_train_sampled)
    if use_cuda:
        x_train = x_train.to(device_gpu)
    xt = x_train.float()
    T = pickle.load(open(os.path.join(output_dir, 't-val.pkl'), 'rb'))
    print("T", T)
    model.eval()
    assert (num_samples == xt.shape[0])
    with torch.no_grad():
        # compute the mu and logarithmic variance of the original data's z.
        mu, logvar = model.encode(xt.view(-1, xt.shape[1]))
        std = torch.exp(0.5 * logvar)
        num_samples_in_one_go = xt.shape[0]

        ### For each generated sample, compute these values.
        tgt_count = num_samples
        all_tensor_out_taken = []
        while tgt_count > 0:
            m = torch.randn(num_samples_in_one_go, latent_dim)  ## Sample z?
            if use_cuda:
                m = m.to(device_gpu).float()
            rep_z = m * std + mu

            any_inf = torch.any(torch.isinf(rep_z), axis=1)
            mu = mu[~any_inf]
            std = std[~any_inf]
            rep_z = rep_z[~any_inf]
            xt = xt[~any_inf]
            num_samples_in_one_go = xt.shape[0]

            ## P(z)
            normal = torch.distributions.normal.Normal(0, 1)  ## Normal Prior on Z.
            p_z = normal.log_prob(rep_z)  ## Probabilitiy of z being sampled from normal prior.

            ## P(x|z)
            x_cap = model.decode(rep_z)  ## Output based on the obtained z.
            x_distr = torch.distributions.normal.Normal(torch.mean(x_cap, axis=0),
                                                        1)  ## Distribution with x_cap as mean
            p_x_z = x_distr.log_prob(xt)

            ## Q(z|x)
            q_normal = torch.distributions.normal.Normal(mu, std)
            q_z_x = q_normal.log_prob(rep_z)

            a = torch.exp(T + torch.mean(p_z, axis=-1) + torch.mean(p_x_z, axis=-1) - torch.mean(q_z_x, axis=-1))
            a_ones = torch.ones_like(a)
            if use_cuda:
                a_ones = a_ones.to(device_gpu)
            a = torch.min(a_ones, a)

            u = torch.rand(num_samples_in_one_go)  ### Randomly generate U values.
            if use_cuda:
                u = u.to(device_gpu)
            accept_mask = (u - a <= 0)
            tensor_out_taken = x_cap[accept_mask]
            tgt_count -= len(tensor_out_taken)
            all_tensor_out_taken.append(tensor_out_taken)
        tensor_out = torch.cat(all_tensor_out_taken)[:num_samples]
        out = tensor_out.cpu().detach().numpy()
        transformed_output = transform_reverse(out, output_dir)
        print("GENERATED NUM OF SAMPLES", transformed_output.shape[0])

        sample_file_path = os.path.join(output_dir, 'samples_{}.csv'.format(num_samples))
        transformed_output.to_csv(sample_file_path, index=False)
        print("Sample has been saved in {}".format(sample_file_path))
