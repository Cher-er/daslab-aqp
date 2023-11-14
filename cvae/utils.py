import pandas as pd
from config.config import CVAEConfig
import os
import json


def gen_masked_samples():
    config = CVAEConfig().get_config()
    with open(config["sql_file"]) as f:
        sqls = f.readlines()

    with open(os.path.join(config["output_dir"], "{}_info.json".format(config["model_name"]))) as f:
        dataset_info = json.load(f)

    columns = dataset_info["columns"]

    masked_datas = []
    for sql in sqls:
        masked_data = ["nan"] * len(columns)

        sql = sql.split(";")[0]
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
            if pre.isdigit():
                pre = int(pre)
            masked_data[masked_data.index(col)] = pre
        masked_datas.append(masked_data)

    masked_datas = pd.DataFrame(masked_datas)
    masked_datas.to_csv(os.path.join(config["output_dir"], "{}_masked_for_sql.tsv".format(config["model_name"])), sep='\t', na_rep="nan", header=columns, index=False)
