from copy import deepcopy
from math import ceil
from os.path import join
from os import makedirs
from sys import stderr
import os

import numpy as np
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm

from cvae.datasets import compute_normalization
from cvae.imputation_networks import get_imputation_networks
from cvae.train_utils import extend_batch, get_validation_iwae
from cvae.VAEAC import VAEAC
from config.config import CVAEConfig
import json

from cvae.data.prepare_data import prepare_data


def train():
    prepare_data()
    config = CVAEConfig().get_config()
    output_dir = config["output_dir"]
    dataset = config["dataset"]
    epochs = config["epochs"]
    verbose = config["verbose"]
    iter_bar = config["iter_bar"]
    validation_ratio = config["validation_ratio"]
    validations_per_epoch = config["validations_per_epoch"]
    validation_iwae_num_samples = config["validation_iwae_num_samples"]

    with open(join(output_dir, "{}_info.json".format(dataset))) as f:
        dataset_info = json.load(f)

    one_hot_max_sizes = dataset_info["one_hot_max_sizes"]

    # Read and normalize input data
    raw_data = np.loadtxt(join(output_dir, "{}_masked.tsv".format(dataset)), delimiter='\t', skiprows=1)
    raw_data = torch.from_numpy(raw_data).float()
    norm_mean, norm_std = compute_normalization(raw_data, one_hot_max_sizes)
    norm_std = torch.max(norm_std, torch.tensor(1e-9))
    data = (raw_data - norm_mean[None]) / norm_std[None]

    # Default parameters which are not supposed to be changed from user interface
    use_cuda = torch.cuda.is_available()
    print("[use_cuda]:", use_cuda)

    # Non-zero number of workers cause nasty warnings because of some bug in
    # multiprocess library. It might be fixed now, but anyway there is no need
    # to have a lot of workers for dataloader over in-memory tabular data.
    num_workers = 0

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
        print("Model to GPU")
    optimizer = networks['optimizer'](model.parameters())
    batch_size = networks['batch_size']
    mask_generator = networks['mask_generator']
    vlb_scale_factor = networks.get('vlb_scale_factor', 1)

    # train-validation split
    val_size = ceil(len(data) * validation_ratio)
    val_indices = np.random.choice(len(data), val_size, False)
    val_indices_set = set(val_indices)
    train_indices = [i for i in range(len(data)) if i not in val_indices_set]
    train_data = data[train_indices]
    val_data = data[val_indices]

    # initialize dataloaders
    dataloader = DataLoader(train_data, batch_size=batch_size, shuffle=True,
                            num_workers=num_workers, drop_last=False)
    val_dataloader = DataLoader(val_data, batch_size=batch_size, shuffle=True,
                                num_workers=num_workers, drop_last=False)

    # number of batches after which it is time to do validation
    validation_batches = ceil(len(dataloader) / validations_per_epoch)

    # a list of validation IWAE estimates
    validation_iwae = []
    # a list of running variational lower bounds on the train set
    train_vlb = []
    # the length of two lists above is the same because the new
    # values are inserted into them at the validation checkpoints only

    # best model state according to the validation IWAE
    best_state = None

    # main train loop
    for epoch in range(epochs):

        iterator = dataloader
        avg_vlb = 0
        if verbose:
            print('Epoch %d...' % (epoch + 1), file=stderr, flush=True)
        if iter_bar:
            iterator = tqdm(iterator)

        # one epoch
        for i, batch in enumerate(iterator):

            # the time to do a checkpoint is at start and end of the training
            # and after processing validation_batches batches
            if any([
                i == 0 and epoch == 0,
                i % validation_batches == validation_batches - 1,
                i + 1 == len(dataloader)
            ]):
                val_iwae = get_validation_iwae(val_dataloader, mask_generator,
                                               batch_size, model,
                                               validation_iwae_num_samples,
                                               iter_bar)
                validation_iwae.append(val_iwae)
                train_vlb.append(avg_vlb)

                # if current model validation IWAE is the best validation IWAE
                # over the history of training, the current state
                # is saved to best_state variable
                if max(validation_iwae[::-1]) <= val_iwae:
                    best_state = deepcopy({
                        'epoch': epoch,
                        'model_state_dict': model.state_dict(),
                        'optimizer_state_dict': optimizer.state_dict(),
                        'validation_iwae': validation_iwae,
                        'train_vlb': train_vlb,
                    })

                if verbose:
                    print(file=stderr)
                    print(file=stderr)

            # if batch size is less than batch_size, extend it with objects
            # from the beginning of the dataset
            batch = extend_batch(batch, dataloader, batch_size)

            # generate mask and do an optimizer step over the mask and the batch
            mask = mask_generator(batch)
            optimizer.zero_grad()
            if use_cuda:
                batch = batch.cuda()
                mask = mask.cuda()
            vlb = model.batch_vlb(batch, mask).mean()
            (-vlb / vlb_scale_factor).backward()
            optimizer.step()

            # update running variational lower bound average
            avg_vlb += (float(vlb) - avg_vlb) / (i + 1)
            if iter_bar:
                iterator.set_description('Train VLB: %g' % avg_vlb)

    makedirs(output_dir, exist_ok=True)
    torch.save(best_state["model_state_dict"], join(output_dir, "model.pth"))
    print("CVAE model has been saved in {}".format(join(output_dir, "model.pth")))
