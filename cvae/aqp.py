from config.config import CVAEConfig
import os
from cvae.utils import execute_avg


def aqp_avg():
    config = CVAEConfig().get_config()
    results = execute_avg(os.path.join(config["output_dir"], "{}_imputed.tsv".format(config["model_name"])), '\t')
    with open(os.path.join(config["output_dir"], 'samples_{}x_aqp.csv'.format(config['num_imputations'])), 'w') as f:
        for result in results:
            f.write(str(result) + "\n")
    print("AQP results has been saved in {}".format(os.path.join(config["output_dir"], 'samples_{}x_aqp.csv'.format(config['num_imputations']))))
