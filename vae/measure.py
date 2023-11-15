import pandas as pd
import os
from config.config import VAEConfig
from utils.utils import sMAPE


def measure():
    config = VAEConfig().get_config()
    output_dir = config['output_dir']

    aqp_file_path = os.path.join(output_dir, 'samples_{}_aqp.csv'.format(config['num_samples']))
    aqp = pd.read_csv(aqp_file_path, header=None)

    truth_file_path = os.path.join(output_dir, 'samples_{}_truth.csv'.format(config['num_samples']))
    truth = pd.read_csv(truth_file_path, header=None)

    smape = sMAPE(truth, aqp)

    measure_file_path = os.path.join(output_dir, 'samples_{}_measure.csv'.format(config['num_samples']))
    smape.to_csv(measure_file_path, index=False, header=["sMAPE"])
    print("Measure result has been saved in {}".format(measure_file_path))
