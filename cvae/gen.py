from os.path import join

import numpy as np
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm

from cvae.datasets import compute_normalization
from cvae.imputation_networks import get_imputation_networks
from cvae.train_utils import extend_batch
from config.config import CVAEConfig
import json
from cvae.VAEAC import VAEAC
from cvae.utils import gen_masked_samples

import pandas as pd


def gen():
    gen_masked_samples()

    config = CVAEConfig().get_config()
    output_dir = config["output_dir"]
    dataset = config["dataset"]
    iter_bar = config["iter_bar"]
    batch_size = config["batch_size"]
    num_imputations = config["num_imputations"]

    with open(join(output_dir, "{}_info.json".format(dataset))) as f:
        dataset_info = json.load(f)
    columns = dataset_info["columns"]
    cat_cols = dataset_info["cat_cols"]
    one_hot_map = dataset_info["one_hot_map"]
    one_hot_max_sizes = dataset_info["one_hot_max_sizes"]

    networks = get_imputation_networks(one_hot_max_sizes)

    use_cuda = torch.cuda.is_available()

    model = VAEAC(
        networks['reconstruction_log_prob'],
        networks['proposal_network'],
        networks['prior_network'],
        networks['generative_network']
    )
    model.load_state_dict(torch.load(join(output_dir, "model.pth")))
    if use_cuda:
        model = model.cuda()

    num_workers = 0

    raw_data = np.loadtxt(join(output_dir, "{}_masked.tsv".format(dataset)), delimiter='\t', skiprows=1)
    raw_data = torch.from_numpy(raw_data).float()
    norm_mean, norm_std = compute_normalization(raw_data, one_hot_max_sizes)
    norm_std = torch.max(norm_std, torch.tensor(1e-9))

    sample_data = np.loadtxt(join(output_dir, "{}_masked_for_sql.tsv".format(dataset)), delimiter='\t', skiprows=1)
    sample_data = torch.from_numpy(sample_data).float()
    data = (sample_data - norm_mean[None]) / norm_std[None]


    # build dataloader for the whole input data
    dataloader = DataLoader(data, batch_size=batch_size,
                            shuffle=False, num_workers=num_workers,
                            drop_last=False)

    # prepare the store for the imputations
    results = []
    for i in range(num_imputations):
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
                                                           num_imputations)
            samples_params = samples_params[:batch.shape[0]]

        # make a copy of batch with zeroed missing values
        mask = torch.isnan(batch)
        batch_zeroed_nans = batch.clone().detach()
        batch_zeroed_nans[mask] = 0

        # impute samples from the generative distributions into the data
        # and save it to the results
        for i in range(num_imputations):
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

    list_of_key = {}
    list_of_value = {}
    for col, col_map in one_hot_map.items():
        list_of_key[col] = list(col_map.keys())
        list_of_value[col] = list(col_map.values())

    result_df = pd.DataFrame(result.numpy())
    result_df.columns = columns
    for col in cat_cols:
        for j, one_hot in enumerate(result_df[col]):
            one_hot = int(one_hot)
            col_value = list_of_key[col][list_of_value[col].index(one_hot)]
            result_df.iloc[j, result_df.columns.get_loc(col)] = col_value

    imputed_file_path = join(output_dir, "{}_imputed.tsv".format(dataset))
    result_df.to_csv(imputed_file_path, header=columns, index=False, sep='\t')
    print("Out file has been saved in {}".format(imputed_file_path))
