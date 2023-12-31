from os import makedirs
from os.path import join

import numpy as np
import pandas as pd
from config.config import CVAEConfig
import torch
import json
import schema.flights


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
    config = CVAEConfig().get_config()
    input_file = config["input_file"]
    csv_separator = CVAEConfig().get_config()["csv_separator"]
    data = pd.read_csv(input_file, sep=csv_separator)
    cols = data.columns
    cat_cols, num_cols = [], []
    for k, v in schema.flights.schema.items():
        if v == "c":
            cat_cols.append(k)
        elif v == "n":
            num_cols.append(k)
    unique_values = []
    one_hot_map = {}
    for i, cat_col in enumerate(cat_cols):
        unique_values.append(data[cat_col].unique())
        # print(unique_values[i])
        one_hot_map[cat_col] = {}
        for j, x in enumerate(unique_values[i]):
            if type(x) == np.int64:
                one_hot_map[cat_col][int(x)] = j
            else:
                one_hot_map[cat_col][x] = j
        # one_hot_map[cat_col] = {x: i for i, x in enumerate(unique_values[i])}
        data[cat_col] = data[cat_col].map(one_hot_map[cat_col])
    return data, list(cols), cat_cols, num_cols, one_hot_map


def save_data(filename, data, cols):
    data_df = pd.DataFrame(data)
    data_df.to_csv(filename, header=cols, sep='\t', index=False, na_rep="nan")


def prepare_data():
    config = CVAEConfig().get_config()
    random_seed = config['random_seed']
    dataset = config["dataset"]
    output_dir = config["output_dir"]

    print("Reading data...")
    data, cols, cat_cols, num_cols, one_hot_map = loader()
    np.random.seed(random_seed)

    r = config["mask_r"]

    print("Masking data...")
    data_odd = data[data.index % 2 == 1]
    data_even = data[data.index % 2 == 0]
    data_even_masked = stratified_masking(data_even, r, cat_cols, num_cols)
    data_masked = pd.concat([data_odd, data_even_masked])

    makedirs(output_dir, exist_ok=True)
    save_data(join(output_dir, '{}_masked.tsv'.format(dataset)), data_masked, cols)
    save_data(join(output_dir, '{}_original_data.tsv'.format(dataset)), data, cols)
    print("Masked data has been saved in {}.".format(join(output_dir, '{}_masked.tsv'.format(dataset))))

    one_hot_max_sizes = []
    for col in cols:
        if col in num_cols:
            one_hot_max_sizes.append(1)
        else:
            one_hot_max_sizes.append(len(one_hot_map[col]))

    dataset_info = {
        "columns": cols,
        "cat_cols": cat_cols,
        "num_cols": num_cols,
        "one_hot_map": one_hot_map,
        "one_hot_max_sizes": one_hot_max_sizes
    }
    with open(join(output_dir, "{}_info.json".format(dataset)), 'w') as f:
        json.dump(dataset_info, f)
    print("Some information of dataset has been saved in {}.".format(join(output_dir, "{}_info.json".format(dataset))))
