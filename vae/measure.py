import pandas as pd
import os
from config.config import VAEConfig


def measure():
    config = VAEConfig().get_config()
    aqp = pd.read_csv(os.path.join(config["output_dir"], 'samples_{}_aqp.csv'.format(config['num_samples'])))
    truth = pd.read_csv(os.path.join(config["output_dir"], 'samples_{}_truth.csv'.format(config['num_samples'])))
    print(aqp)
    print(truth)
