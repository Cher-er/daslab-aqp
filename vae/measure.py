import pandas as pd
import os
from config.config import VAEConfig
import numpy as np


def sMAPE(truth, aqp):
    result = 2 * (truth - aqp).abs() / (truth.abs() + aqp.abs())
    result[np.isinf(result)] = 0
    return result.mean()


def measure():
    config = VAEConfig().get_config()
    aqp = pd.read_csv(os.path.join(config["output_dir"], 'samples_{}_aqp.csv'.format(config['num_samples'])), header=None)
    truth = pd.read_csv(os.path.join(config["output_dir"], 'samples_{}_truth.csv'.format(config['num_samples'])), header=None)
    smape = sMAPE(truth, aqp)
    with open(os.path.join(config["output_dir"], 'samples_{}_sMAPE.csv'.format(config['num_samples'])), 'w') as f:
        print(smape)
        f.write(str(smape))
    print("Measure result has been saved in {}".format(os.path.join(config["output_dir"], 'samples_{}_measure.csv'.format(config['num_samples']))))
