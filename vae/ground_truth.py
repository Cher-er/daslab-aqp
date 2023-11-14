from config.config import VAEConfig
import os
from vae.utils import execute_avg
import pickle


def exact_avg():
    config = VAEConfig().get_config()
    results = execute_avg(config["input_file"])
    with open(os.path.join(config["output_dir"], 'samples_{}_truth.pkl'.format(config['num_samples'])), 'wb') as f:
        pickle.dump(results, f)
    print("Ground truth has been saved in {}".format(os.path.join(config["output_dir"], 'samples_{}_truth.pkl'.format(config['num_samples']))))
