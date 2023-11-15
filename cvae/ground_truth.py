from config.config import CVAEConfig
import os
from cvae.utils import execute_avg


def exact_avg():
    config = CVAEConfig().get_config()
    input_file = config['input_file']
    output_dir = config['output_dir']
    num_imputations = config['num_imputations']

    results = execute_avg(input_file, ',')
    truth_file_path = os.path.join(output_dir, 'samples_{}x_truth.csv'.format(num_imputations))
    with open(truth_file_path, 'w') as f:
        for result in results:
            f.write(str(result) + "\n")
    print("Ground truth has been saved in {}".format(truth_file_path))
