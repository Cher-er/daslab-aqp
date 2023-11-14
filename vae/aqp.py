import pandas as pd
from config.config import VAEConfig
import os


def execute_avg():
    config = VAEConfig().get_config()
    data = pd.read_csv(os.path.join(config["output_dir"], 'samples_{}.csv'.format(config['num_samples'])), delimiter=",")
    with open(config["sql_file"]) as f:
        sqls = f.readlines()
    print(data)
    print(sqls)
