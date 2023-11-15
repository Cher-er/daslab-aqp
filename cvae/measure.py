import pandas as pd
import os
from config.config import CVAEConfig
from utils.utils import sMAPE


def measure():
    config = CVAEConfig().get_config()
    output_dir = config['output_dir']
    num_imputations = config['num_imputations']

    aqp = pd.read_csv(os.path.join(output_dir, 'samples_{}x_aqp.csv'.format(num_imputations)), header=None)
    truth = pd.read_csv(os.path.join(output_dir, 'samples_{}x_truth.csv'.format(num_imputations)), header=None)
    smape = sMAPE(truth, aqp)

    measure_file_path = os.path.join(output_dir, 'samples_{}x_measure.csv'.format(num_imputations))
    smape.to_csv(measure_file_path, index=False, header=["sMAPE"])
    print("Measure result has been saved in {}".format(measure_file_path))
