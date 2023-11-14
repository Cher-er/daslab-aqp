from config.config import CVAEConfig
import os
from cvae.utils import execute_avg


def exact_avg():
    config = CVAEConfig().get_config()
    results = execute_avg(os.path.join(config["output_dir"], "{}_original_data.tsv".format(config["model_name"])))
    with open(os.path.join(config["output_dir"], 'samples_{}x_truth.csv'.format(config['num_imputations'])), 'w') as f:
        for result in results:
            f.write(str(result) + "\n")
    print("Ground truth has been saved in {}".format(os.path.join(config["output_dir"], 'samples_{}x_truth.csv'.format(config['num_imputations']))))
