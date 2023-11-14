import pandas as pd
import os
from config.config import VAEConfig
import numpy as np


def sMAPE(truth, aqp):
    result = 2 * (truth - aqp).abs() / (truth.abs() + aqp.abs())
    print(result)
    result[np.isinf(result)] = 0
    return result.mean()


def measure():
    config = VAEConfig().get_config()
    aqp = pd.read_csv(os.path.join(config["output_dir"], 'samples_{}_aqp.csv'.format(config['num_samples'])))
    truth = pd.read_csv(os.path.join(config["output_dir"], 'samples_{}_truth.csv'.format(config['num_samples'])))
    print(sMAPE(truth, aqp))
