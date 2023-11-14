from config.config import VAEConfig
import os
from vae.utils import execute_avg


def aqp_avg():
    config = VAEConfig().get_config()
    results = execute_avg(os.path.join(config["output_dir"], 'samples_{}.csv'.format(config['num_samples'])))
    with open(os.path.join(config["output_dir"], 'samples_{}_aqp.csv'.format(config['num_samples'])), 'w') as f:
        f.writelines(results)
    print("AQP results has been saved in {}".format(os.path.join(config["output_dir"], 'samples_{}_aqp.csv'.format(config['num_samples']))))
