from config.config import VAEConfig
import os
from vae.utils import execute_avg
import pickle


def aqp_avg():
    config = VAEConfig().get_config()
    results = execute_avg(os.path.join(config["output_dir"], 'samples_{}.csv'.format(config['num_samples'])))
    with open(os.path.join(config["output_dir"], 'samples_{}_aqp.pkl'.format(config['num_samples'])), 'w') as f:
        pickle.dump(results, f)
    print("AQP results has been saved in {}".format(os.path.join(config["output_dir"], 'samples_{}_aqp.pkl'.format(config['num_samples']))))
