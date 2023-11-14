import pandas as pd
import os
from config.config import CVAEConfig
from utils.utils import sMAPE


def measure():
    config = CVAEConfig().get_config()
    aqp = pd.read_csv(os.path.join(config["output_dir"], 'samples_{}x_aqp.csv'.format(config['num_imputations'])), header=None)
    truth = pd.read_csv(os.path.join(config["output_dir"], 'samples_{}x_truth.csv'.format(config['num_imputations'])), header=None)
    smape = sMAPE(truth, aqp)
    smape.to_csv(os.path.join(config["output_dir"], 'samples_{}x_measure.csv'.format(config['num_imputations'])), index=False, header=["sMAPE"])
    print("Measure result has been saved in {}".format(os.path.join(config["output_dir"], 'samples_{}x_measure.csv'.format(config['num_imputations']))))
