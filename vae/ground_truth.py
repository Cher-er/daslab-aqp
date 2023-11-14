from config.config import VAEConfig
import os
from vae.utils import execute_avg


def exact_avg():
    config = VAEConfig().get_config()
    results = execute_avg(config["input_file"])
    with open(os.path.join(config["output_dir"], 'samples_{}_truth.csv'.format(config['num_samples']))) as f:
        f.writelines(results)
    print("Ground truth has been saved in {}".format(os.path.join(config["output_dir"], 'samples_{}_truth.csv'.format(config['num_samples']))))
