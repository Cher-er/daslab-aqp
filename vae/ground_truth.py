from config.config import VAEConfig
import os
from vae.utils import execute_avg


def exact_avg():
    config = VAEConfig().get_config()
    input_file = config['input_file']
    output_dir = config['output_dir']

    results = execute_avg(input_file)
    truth_file_path = os.path.join(output_dir, 'samples_truth.csv')
    with open(truth_file_path, 'w') as f:
        for result in results:
            f.write(str(result) + "\n")
    print("Ground truth has been saved in {}".format(truth_file_path))
