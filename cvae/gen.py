from os.path import join

import numpy as np
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm

from cvae.datasets import compute_normalization
from cvae.imputation_networks import get_imputation_networks
from cvae.train_utils import extend_batch, get_validation_iwae
from config.config import CVAEConfig
import json


def gen():
    config = CVAEConfig().get_config()
    output_dir = config["output_dir"]
    iter_bar = config["iter_bar"]

    with open(join(config["output_dir"], "info", "{}_info.json".format(config["model_name"]))) as f:
        dataset_info = json.load(f)
    one_hot_max_sizes = dataset_info["one_hot_max_sizes"]

    model = torch.load(join(output_dir, "model.pth"))

    networks = get_imputation_networks(one_hot_max_sizes)

    batch_size = networks['batch_size']
    num_workers = 0

    use_cuda = torch.cuda.is_available()

    raw_data = np.loadtxt(join(config["output_dir"], "train_test_split", "{}_masked.tsv".format(config["model_name"])), delimiter='\t', skiprows=1)
    raw_data = torch.from_numpy(raw_data).float()
    norm_mean, norm_std = compute_normalization(raw_data, one_hot_max_sizes)
    norm_std = torch.max(norm_std, torch.tensor(1e-9))
    data = (raw_data - norm_mean[None]) / norm_std[None]


    # build dataloader for the whole input data
    dataloader = DataLoader(data, batch_size=batch_size,
                            shuffle=False, num_workers=num_workers,
                            drop_last=False)

    # prepare the store for the imputations
    results = []
    for i in range(config["num_imputations"]):
        results.append([])

    iterator = dataloader
    if iter_bar:
        iterator = tqdm(iterator)

    # impute missing values for all input data
    for batch in iterator:

        # if batch size is less than batch_size, extend it with objects
        # from the beginning of the dataset
        batch_extended = batch.clone().detach()
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
                                                           config["num_imputations"])
            samples_params = samples_params[:batch.shape[0]]

        # make a copy of batch with zeroed missing values
        mask = torch.isnan(batch)
        batch_zeroed_nans = batch.clone().detach()
        batch_zeroed_nans[mask] = 0

        # impute samples from the generative distributions into the data
        # and save it to the results
        for i in range(config["num_imputations"]):
            sample_params = samples_params[:, i]
            sample = networks['sampler'](sample_params)
            sample[~mask] = 0
            sample += batch_zeroed_nans
            results[i].append(sample.clone().detach().cpu())

    # concatenate all batches into one [n x K x D] tensor,
    # where n in the number of objects, K is the number of imputations
    # and D is the dimensionality of one object
    for i in range(len(results)):
        results[i] = torch.cat(results[i]).unsqueeze(1)
    result = torch.cat(results, 1)

    # reshape result, undo normalization and save it
    result = result.view(result.shape[0] * result.shape[1], result.shape[2])
    result = result * norm_std[None] + norm_mean[None]
    np.savetxt(join(config["output_dir"], "{}_imputed.tsv".format(config["model_name"])), result.numpy(),
               delimiter='\t')
    print("out file has been saved in {}".format(
        join(config["output_dir"], "{}_imputed.tsv".format(config["model_name"]))))