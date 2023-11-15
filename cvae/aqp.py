from config.config import CVAEConfig
import os
from cvae.utils import execute_avg


def aqp_avg():
    config = CVAEConfig().get_config()
    output_dir = config['output_dir']
    dataset = config['dataset']
    num_imputations = config['num_imputations']

    results = execute_avg(os.path.join(output_dir, "{}_imputed.tsv".format(dataset)), '\t')
    aqp_file_path = os.path.join(output_dir, 'samples_{}x_aqp.csv'.format(num_imputations))
    with open(aqp_file_path, 'w') as f:
        for result in results:
            f.write(str(result) + "\n")
    print("AQP results has been saved in {}".format(aqp_file_path))
