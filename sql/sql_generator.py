from config.config import SqlGeneratorConfig
from schema import schema
import pandas as pd
import random
import os
from utils.utils import is_convertible_to_int


def gen():
    config = SqlGeneratorConfig().get_config()
    dataset = config['dataset']
    input_file = config['input_file']
    sql_num = config['sql_num']
    aggregate = config['aggregate']
    output_dir = config['output_dir']
    predicate_num = config['predicate_num']

    if dataset == 'flights':
        attrs = schema.flights
    else:
        print(f"[ERROR] dataset {dataset} is unknown.")
        return

    cate_cols, num_cols = [], []
    for k, v in attrs.items():
        if v == 'c':
            cate_cols.append(k)
        elif v == 'n':
            num_cols.append(k)
        else:
            print(f"[ERROR] {k}'s type is illegal.")
            return

    df = pd.read_csv(input_file)
    cate_unique_values = {}
    for cate_col in cate_cols:
        cate_unique_values[cate_col] = df[cate_col].unique()

    sqls = []
    if predicate_num == 1:
        for i in range(sql_num):
            num_col = num_cols[random.randint(0, len(num_cols) - 1)]

            cate_col = cate_cols[random.randint(0, len(cate_cols) - 1)]
            cate_col_value = cate_unique_values[cate_col][random.randint(0, len(cate_unique_values[cate_col]) - 1)]

            if is_convertible_to_int(cate_col_value):
                sql = f"SELECT {aggregate}({num_col}) from {dataset} where {cate_col} = {cate_col_value};"
            else:
                sql = f"SELECT {aggregate}({num_col}) from {dataset} where {cate_col} = '{cate_col_value}';"
            sqls.append(sql)

    file_name = os.path.join(output_dir, f"{dataset}_{aggregate}_{sql_num}.sql")
    with open(file_name, 'w') as f:
        for sql in sqls:
            f.write(sql + '\n')

    print(f"[INFO] generated sql has been saved in {file_name}.")
