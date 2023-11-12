from os import makedirs
from os.path import join

import numpy as np
import pandas as pd
from config.config import CVAEConfig
import torch
import json


def stratified_masking(data, r, cat_cols, num_cols):
    b, k = data.shape
    mask = np.zeros((b, k))
    for i, col in enumerate(data.columns):
        if col in num_cols:
            mask[:, i] = 1
        elif col in cat_cols:
            values = data[col].values
            unique_values, counts = np.unique(values, return_counts=True)
            weights = {value: count/len(values) for value, count in zip(unique_values, counts)}
            weights = torch.tensor([weights[value] for value in values])
            batch_indices = torch.multinomial(weights, int(r * b))
            mask[batch_indices, i] = 1
    data_masked = data.copy()
    data_masked[mask.astype('bool')] = np.nan
    return data_masked


def loader():
    path = CVAEConfig().get_config()["input_file"]
    csv_separator = CVAEConfig().get_config()["csv_separator"]
    data = pd.read_csv(path, sep=csv_separator)
    cols = data.columns
    cat_cols = list(filter(lambda x: '_c' in x, cols))
    num_cols = list(filter(lambda x: '_n' in x, cols))
    unique_values = []
    one_hot_map = {}
    one_hot_max_sizes = []
    for i, cat_col in enumerate(cat_cols):
        unique_values.append(data[cat_col].unique())
        one_hot_map[cat_col] = {x: i for i, x in enumerate(unique_values[i])}
        data[cat_col] = data[cat_col].map(one_hot_map[cat_col])
        one_hot_max_sizes.append(len(one_hot_map[cat_col]) - 1)
    return data, cols, cat_cols, num_cols, one_hot_map, one_hot_max_sizes


def save_data(filename, data):
    np.savetxt(filename, data, delimiter='\t', fmt='%s')


def prepare_data():
    config = CVAEConfig().get_config()
    print("Reading data...")
    data, cols, cat_cols, num_cols, one_hot_map, one_hot_max_sizes = loader()
    random_seed = config["random_seed"]
    np.random.seed(random_seed)
    model_name = config["model_name"]
    r = config["mask_r"]
    output_dir = config["output_dir"]

    print("Masking data...")
    data_masked = stratified_masking(data, r, cat_cols, num_cols)

    makedirs(join(output_dir, 'train_test_split'), exist_ok=True)
    save_data(join(output_dir, 'train_test_split', '{}_masked.tsv'.format(model_name)), data_masked)
    save_data(join(output_dir, 'train_test_split', '{}_original_data.tsv'.format(model_name)), data)
    print("Masked data has been saved in {}.".format(output_dir))

    dataset_info = {
        "columns": cols,
        "one_hot_map": one_hot_map,
        "one_hot_max_sizes": one_hot_max_sizes
    }
    with open(join(output_dir, "info", "{}_info.json".format(model_name))) as f:
        json.dump(dataset_info, f)
