from os import makedirs
from os.path import join

import numpy as np
import pandas as pd
from random import sample

random_seed = 239


def stratified_masking(data, r, cat_cols, num_cols):
    b, k = data.shape
    m = np.zeros((b, k))
    for i, col in enumerate(data.columns):
        if col in num_cols:
            m[:, i] = 1
        elif col in cat_cols:
            values = data[col].values
            unique_values, counts = np.unique(values, return_counts=True)
            weights = {value: count/len(values) for value, count in zip(unique_values, counts)}
            weights_data = np.array([weights[value] for value in values])
            print(weights_data)
            # batch_indices = sample(range(b), int(r * b), weights=weights_data)
            batch_indices = sample(range(b), int(r * b))
            m[batch_indices, i] = 1
    return m


def Flights_loader(path):
    #Reporting_Airline	Origin	OriginStateName	Dest	DestStateName
    data = pd.read_csv(join(path, 'flights.csv'),sep=',')
    unique_values1 = data["unique_carrier_c"].unique()
    target_id1 = {x: i for i, x in enumerate(unique_values1)}   #对于字符串类型修改为对应的one hot编码
    unique_values2 = data["origin_c"].unique()
    target_id2 = {x: i for i, x in enumerate(unique_values2)}   #对于字符串类型修改为对应的one hot编码
    unique_values3 = data["origin_state_abr_c"].unique()
    target_id3 = {x: i for i, x in enumerate(unique_values3)}   #对于字符串类型修改为对应的one hot编码
    unique_values4 = data["dest_c"].unique()
    target_id4 = {x: i for i, x in enumerate(unique_values4)}   #对于字符串类型修改为对应的one hot编码
    unique_values5 = data["dest_state_abr_c"].unique()
    target_id5 = {x: i for i, x in enumerate(unique_values5)}   #对于字符串类型修改为对应的one hot编码
    unique_values6 = data["year_data_c"].unique()
    target_id6 = {x: i for i, x in enumerate(unique_values6)}  # 对于字符串类型修改为对应的one hot编码
    print("unique_carrier_c = ",target_id1)
    print("origin_c = ", target_id2)
    print("origin_state_abr_c = ", target_id3)
    print("dest_c = ", target_id4)
    print("dest_state_abr_c = ", target_id5)
    print("year_data_c = ", target_id6)


    data["unique_carrier_c"] = data["unique_carrier_c"].map(target_id1)
    data["origin_c"] = data["origin_c"].map(target_id2)
    data["origin_state_abr_c"] = data["origin_state_abr_c"].map(target_id3)
    data["dest_c"] = data["dest_c"].map(target_id4)
    data["dest_state_abr_c"] = data["dest_state_abr_c"].map(target_id5)
    data["year_data_c"] = data["year_data_c"].map(target_id6)

    return data


def save_data(filename, data):
    np.savetxt(filename, data, delimiter='\t',fmt = '%s')


if __name__ == "__main__":
    for loader, name in [
        # (yeast_loader, 'yeast'),
        # (white_loader, 'white'),
        # (mushroom_loader, 'mushroom'),
        # (PM25_loader,'PM25'),
        (Flights_loader, 'Flights')
    ]:
        data = loader(join('..', 'original_data'))
        np.random.seed(random_seed)
        # train_data = corrupt_data_mcar(data)

        r = 0.5  # 每行掩码的概率
        cat_cols = ["year_data_c", "unique_carrier_c", "origin_c", "origin_state_abr_c", "dest_c", "dest_state_abr_c"]
        num_cols = ["dep_delay_n", "taxi_out_n", "taxi_in_n", "arr_delay_n", "air_time_n", "distance_n"]

        train_data = stratified_masking(data, r, cat_cols, num_cols)

        makedirs(join('..', 'train_test_split'), exist_ok=True)
        save_data(join('..', 'train_test_split', '{}_train.tsv'.format(name)),
                  train_data)
        save_data(join('..', 'train_test_split', '{}_groundtruth.tsv'.format(name)),
                  data)
