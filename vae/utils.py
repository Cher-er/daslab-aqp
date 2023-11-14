import pandas as pd
from config.config import VAEConfig


def execute_avg(data_path):
    config = VAEConfig().get_config()
    data = pd.read_csv(data_path, delimiter=",")
    with open(config["sql_file"]) as f:
        sqls = f.readlines()

    results = []
    for sql in sqls:
        data_c = data.copy()
        # print("[SQL]: {}".format(sql))
        sql = sql.split(";")[0]
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
            # print("col: {}, pre: {}".format(col, pre))
            data_c = data_c[data_c[col] == pre]

        results.append(data_c[agg].mean())

    return results
