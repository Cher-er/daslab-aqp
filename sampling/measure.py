import pandas as pd
import os
from config.config import SamplingConfig
from utils.utils import sMAPE


def measure():
    config = SamplingConfig().get_config()
    output_dir = config['output_dir']
    method = config['method']
    sample_size = config['sample_size']

    if method == 'random':
        aqp_file_path = os.path.join(output_dir, 'random_sampling_{}.csv'.format(sample_size))
        aqp = pd.read_csv(aqp_file_path, header=None)
    elif method == 'stratified':
        aqp_file_path = os.path.join(output_dir, 'stratified_sampling_{}.csv'.format(config['sample_size']))
        aqp = pd.read_csv(aqp_file_path, header=None)
    else:
        print('Unknown sampling method')
        return

    truth_file_path = os.path.join(output_dir, 'ground_truth.csv')
    truth = pd.read_csv(truth_file_path, header=None)

    smape = sMAPE(truth, aqp)

    measure_file_path = os.path.join(output_dir, 'measure_{}_{}.csv'.format(method, sample_size))
    smape.to_csv(measure_file_path, index=False, header=["sMAPE"])
    print("Measure result has been saved in {}".format(measure_file_path))
