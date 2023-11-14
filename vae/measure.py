import pandas as pd
import os
from config.config import VAEConfig
from utils.utils import sMAPE


def measure():
    config = VAEConfig().get_config()
    aqp = pd.read_csv(os.path.join(config["output_dir"], 'samples_{}_aqp.csv'.format(config['num_samples'])), header=None)
    truth = pd.read_csv(os.path.join(config["output_dir"], 'samples_{}_truth.csv'.format(config['num_samples'])), header=None)
    smape = sMAPE(truth, aqp)
    smape.to_csv(os.path.join(config["output_dir"], 'samples_{}_measure.csv'.format(config['num_samples'])), index=False, header=["sMAPE"])
    print("Measure result has been saved in {}".format(os.path.join(config["output_dir"], 'samples_{}_measure.csv'.format(config['num_samples']))))
