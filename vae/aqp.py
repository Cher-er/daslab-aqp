from config.config import VAEConfig
import os
from vae.utils import execute_avg


def aqp_avg():
    config = VAEConfig().get_config()
    output_dir = config['output_dir']
    num_samples = config['num_samples']
    epochs = config['epochs']

    results = execute_avg(os.path.join(output_dir, 'samples_{}_{}.csv'.format(num_samples, epochs)))
    aqp_file_path = os.path.join(output_dir, 'samples_{}_{}_aqp.csv'.format(num_samples, epochs))
    with open(aqp_file_path, 'w') as f:
        for result in results:
            f.write(str(result) + "\n")
    print("AQP results has been saved in {}".format(aqp_file_path))
