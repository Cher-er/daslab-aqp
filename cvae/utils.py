import pandas as pd
from config.config import CVAEConfig
import os
import json


def gen_masked_samples():
    config = CVAEConfig().get_config()
    output_dir = config['output_dir']
    sql_file = config['sql_file']
    dataset = config['dataset']

    with open(sql_file) as f:
        sqls = f.readlines()

    with open(os.path.join(output_dir, "{}_info.json".format(dataset))) as f:
        dataset_info = json.load(f)

    columns = dataset_info["columns"]
    cat_cols = dataset_info["cat_cols"]
    num_cols = dataset_info["num_cols"]
    one_hot_map = dataset_info["one_hot_map"]

    masked_datas = []
    for sql in sqls:
        masked_data = ["nan"] * len(columns)

        sql = sql.split(";")[0]
        where = sql.split("WHERE")[1].strip()
        # if "(" in where:
        #     where = where.split("(")[1]
        #     where = where.split(")")[0].strip()
        if "AND" in where:
            predicates = where.split("AND")
            for n, predicate in enumerate(predicates):
                predicates[n] = predicate.strip()
        else:
            predicates = [where]

        for predicate in predicates:
            col = predicate.split("=")[0].strip()
            pre = predicate.split("=")[1].strip().strip("'").strip("\"")
            if col in num_cols:
                masked_data[columns.index(col)] = pre
            elif col in cat_cols:
                one_hot_code = one_hot_map[col][pre]
                masked_data[columns.index(col)] = one_hot_code
        masked_datas.append(masked_data)

    masked_datas = pd.DataFrame(masked_datas)
    masked_file_path = os.path.join(output_dir, "{}_masked_for_sql.tsv".format(dataset))
    masked_datas.to_csv(masked_file_path, sep='\t', na_rep="nan", header=columns, index=False)
    print("The masked samples according to SQL have been saved in {}".format(masked_file_path))


def execute_avg(data_path, sep):
    config = CVAEConfig().get_config()
    sql_file = config['sql_file']

    data = pd.read_csv(data_path, delimiter=sep)
    with open(sql_file) as f:
        sqls = f.readlines()

    results = []
    for sql in sqls:
        data_c = data.copy()
        # print("[SQL]: {}".format(sql))
        sql = sql.split(";")[0]
        agg = sql.split("SELECT")[1].split("FROM")[0].strip()
        agg = agg.split("(")[1].split(")")[0].strip()
        where = sql.split("WHERE")[1].strip()
        # if "(" in where:
        #     where = where.split("(")[1]
        #     where = where.split(")")[0].strip()
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
            # print("col: {}, pre: {}".format(col, pre))
            data_c = data_c[data_c[col] == pre]

        results.append(data_c[agg].mean())

    return results
