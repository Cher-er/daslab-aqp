import pandas as pd
from config.config import VAEConfig
import os


def execute_avg():
    config = VAEConfig().get_config()
    data = pd.read_csv(os.path.join(config["output_dir"], 'samples_{}.csv'.format(config['num_samples'])), delimiter=",")
    with open(config["sql_file"]) as f:
        sqls = f.readlines()

    results = []
    for sql in sqls:
        print("[SQL]: {}".format(sql))
        agg = sql.split("SELECT")[1].split("FROM")[0].strip()
        agg = agg.split("(")[1].split(")")[0].strip()
        where = sql.split("WHERE")[1].strip()
        if "(" in where:
            where = where.split("(")[1]
            where = where.split(")")[0].strip()
        if "AND" in where:
            predicates = where.split("AND")
            for n, predicate in enumerate(predicates):
                predicates[n] = predicate.strip()
        else:
            predicates = [where]

        for predicate in predicates:
            col = predicate.split("=")[0].strip()
            pre = predicate.split("=")[1].strip().strip("'").strip("\"")
            print("col: {}, pre: {}".format(col, pre))
            data = data[data[col] == pre]

        results.append(data[agg].mean())

    print(results)
