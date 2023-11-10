import numpy as np
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm

from cvae.datasets import compute_normalization
from cvae.imputation_networks import get_imputation_networks
from cvae.train_utils import extend_batch, get_validation_iwae
from cvae.VAEAC import VAEAC

from config.config import CVAEConfig
import os


def train():
    model_name = CVAEConfig().get_config()["model_name"]
    output_dir = CVAEConfig().get_config()["output_dir"]

    input_file = os.path.join(output_dir, 'train_test_split', '{}_mask.tsv'.format(model_name))
    # input_file = "./data/train_test_split/Flights_stratified_train.tsv"
    output_file = os.path.join(output_dir, 'imputations', '{}_imputed.tsv'.format(model_name))

    mask_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "mask_by_queries", "flights_test.tsv")

    # one_hot_max_sizes = [4, 12, 31, 7, 17, 372, 53, 373, 53, 1751, 194, 229, 1768, 673, 1603]
    one_hot_max_sizes = [21, 25, 371, 52, 371, 52, 1, 1, 1, 1, 1, 1]
    num_imputations = 10
    epochs = 5
    validation_ratio = 0.15
    batch_size = 64
    num_workers = 0
    verbose = True
    use_cuda = torch.cuda.is_available()

    # design all necessary networks and learning parameters for the dataset
    networks = get_imputation_networks(one_hot_max_sizes)

    # build VAEAC on top of returned network, optimizer on top of VAEAC,
    # extract optimization parameters and mask generator
    model = VAEAC(
        networks['reconstruction_log_prob'],
        networks['proposal_network'],
        networks['prior_network'],
        networks['generative_network']
    )
    if use_cuda:
        model = model.cuda()
    optimizer = networks['optimizer'](model.parameters())
    batch_size = networks['batch_size']  # 64
    mask_generator = networks['mask_generator']
    vlb_scale_factor = networks.get('vlb_scale_factor', 1)

    state_dict = torch.load('trained.pth')
    model.load_state_dict(state_dict)

    raw_data = np.loadtxt(input_file, delimiter='\t')  # train的数据被随机mask掉了一些
    raw_data = torch.from_numpy(raw_data).float()

    # 在这里修改为我们想要mask的东西
    test_data = np.loadtxt(mask_file, delimiter='\t')  # train的数据被随机mask掉了一些
    test_data = torch.from_numpy(test_data).float()
    norm_mean, norm_std = compute_normalization(raw_data, one_hot_max_sizes)
    norm_std = torch.max(norm_std, torch.tensor(1e-9))
    data = (test_data - norm_mean[None]) / norm_std[None]

    # build dataloader for the whole input data
    dataloader = DataLoader(data, batch_size=batch_size,
                            shuffle=False, num_workers=num_workers,
                            drop_last=False)

    # prepare the store for the imputations
    results = []
    for i in range(num_imputations):
        results.append([])

    iterator = dataloader
    if verbose:
        iterator = tqdm(iterator)

    # impute missing values for all input data
    for batch in iterator:

        # if batch size is less than batch_size, extend it with objects
        # from the beginning of the dataset
        batch_extended = torch.tensor(batch)
        batch_extended = extend_batch(batch_extended, dataloader, batch_size)

        if use_cuda:
            batch = batch.cuda()
            batch_extended = batch_extended.cuda()

        # compute the imputation mask
        mask_extended = torch.isnan(batch_extended).float()

        # compute imputation distributions parameters
        with torch.no_grad():
            samples_params = model.generate_samples_params(batch_extended,
                                                           mask_extended,
                                                           num_imputations)
            samples_params = samples_params[:batch.shape[0]]

        # make a copy of batch with zeroed missing values
        mask = torch.isnan(batch)
        batch_zeroed_nans = torch.tensor(batch)
        batch_zeroed_nans[mask] = 0

        # impute samples from the generative distributions into the data
        # and save it to the results
        for i in range(num_imputations):
            sample_params = samples_params[:, i]
            sample = networks['sampler'](sample_params)
            sample[(~ mask).byte()] = 0  # [1 - mask] change to [~ mask]
            sample += batch_zeroed_nans
            results[i].append(torch.tensor(sample, device='cpu'))

    # concatenate all batches into one [n x K x D] tensor,
    # where n in the number of objects, K is the number of imputations
    # and D is the dimensionality of one object
    for i in range(len(results)):
        results[i] = torch.cat(results[i]).unsqueeze(1)
    result = torch.cat(results, 1)

    # reshape result, undo normalization and save it
    result = result.view(result.shape[0] * result.shape[1], result.shape[2])
    result = result * norm_std[None] + norm_mean[None]
    np.savetxt(output_file, result.numpy(), delimiter='\t')