import pandas as pd
from config.config import VAEConfig
import re
import schema.flights


def execute_avg(data_path):
    config = VAEConfig().get_config()
    sql_file = config['sql_file']

    data = pd.read_csv(data_path, delimiter=",")
    columns = schema.flights.schema.keys()
    data.columns = columns

    with open(sql_file) as f:
        sqls = f.readlines()

    results = []
    for sql in sqls:
        data_c = data.copy()
        sql = sql.split(";")[0]
        agg = re.split(re.compile(r'\bSELECT\b', re.IGNORECASE), sql)[1]
        agg = re.split(re.compile(r'\bFROM\b', re.IGNORECASE), agg)[0].strip()
        agg = agg.split("(")[1].split(")")[0].strip()

        where = re.split(re.compile(r'\bWHERE\b', re.IGNORECASE), sql)[1].strip()
        if "AND" in where or "and" in where:
            predicates = re.split(re.compile(r'\bAND\b', re.IGNORECASE), where)
            for n, predicate in enumerate(predicates):
                predicates[n] = predicate.strip()
        else:
            predicates = [where]

        for predicate in predicates:
            col = predicate.split("=")[0].strip()
            pre = predicate.split("=")[1].strip().strip("'").strip("\"")
            if pre.isdigit():
                pre = int(pre)
            data_c = data_c[data_c[col] == pre]

        results.append(data_c[agg].mean())

    return results
