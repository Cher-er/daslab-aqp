import psycopg2
import csv
import pandas as pd
import re
import os
from config.config import SamplingConfig


def aqp():
    config = SamplingConfig().get_config()
    method = config['method']
    if method == 'random':
        random_sampling()
    elif method == 'stratified':
        stratified_sampling()
    else:
        print("Unknown sampling method")


def random_sampling():
    config = SamplingConfig().get_config()
    pgsql_parameter = config['pgsql']
    sql_file = config['sql_file']
    output_dir = config['output_dir']
    sample_size = config['random_sampling_size']

    conn = psycopg2.connect(host=pgsql_parameter["host"],
                            port=pgsql_parameter["port"],
                            database=pgsql_parameter["database"],
                            user=pgsql_parameter["user"],
                            password=pgsql_parameter["password"])
    cur = conn.cursor()

    with open(sql_file, 'r') as f:
        commands = f.readlines()

    cur.execute(f"select * from {pgsql_parameter['database']} tablesample bernoulli({sample_size});")
    sample = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    def is_convertible_to_int(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    results = []
    for command in commands:
        pattern_count = re.compile(r'^select\s+count', re.IGNORECASE)
        pattern_avg = re.compile(r'^select\s+avg', re.IGNORECASE)
        pattern_sum = re.compile(r'^select\s+sum', re.IGNORECASE)
        if pattern_count.match(command):
            agg = "count"
        elif pattern_avg.match(command):
            agg = "avg"
        elif pattern_sum.match(command):
            agg = "sum"
        else:
            agg = "unknown"
        sample_df = pd.DataFrame(sample, columns=columns)
        command = command.split(';')[0]
        pattern_1 = re.compile(r'\bWHERE\b', flags=re.IGNORECASE)
        pattern_2 = re.compile(r'\bAND\b', flags=re.IGNORECASE)
        predicates = re.split(pattern_2, re.split(pattern_1, command)[1])
        for predicate in predicates:
            if ">=" in predicate:
                attr = predicate.split(">=")[0].strip()
                val = predicate.split(">=")[1].strip()
                sample_df = sample_df[sample_df[attr] >= int(val)]
            elif "<=" in predicate:
                attr = predicate.split("<=")[0].strip()
                val = predicate.split("<=")[1].strip()
                sample_df = sample_df[sample_df[attr] <= int(val)]
            elif ">" in predicate:
                attr = predicate.split(">")[0].strip()
                val = predicate.split(">")[1].strip()
                sample_df = sample_df[sample_df[attr] > int(val)]
            elif "<" in predicate:
                attr = predicate.split("<")[0].strip()
                val = predicate.split("<")[1].strip()
                sample_df = sample_df[sample_df[attr] < int(val)]
            elif "=" in predicate:
                attr = predicate.split("=")[0].strip()
                val = predicate.split("=")[1].strip()
                if is_convertible_to_int(val):
                    val = int(val)
                else:
                    val = val.replace("'", "")
                    val = val.replace('"', "")
                sample_df = sample_df[sample_df[attr] == val]
        if agg == "count":
            results.append(sample_df.shape[0] * (100 / sample_size))
        elif agg == 'avg':
            match = re.search(r'AVG\(([^)]+)\)', command, re.IGNORECASE)
            if match:
                target = match.group(1)
                results.append(float(sample_df[target].mean()))
        elif agg == 'sum':
            match = re.search(r'SUM\(([^)]+)\)', command, re.IGNORECASE)
            if match:
                target = match.group(1)
                results.append(float(sample_df[target].sum()) * (100 / sample_size))

    output_file = os.path.join(output_dir, f'random_sampling_{sample_size}.csv')
    with open(output_file, 'w') as f:
        writer = csv.writer(f)
        for result in results:
            writer.writerow([result])

    print(f"Random sampling of {sample_size} results has been saved in {output_file}")

    cur.close()
    conn.close()


def stratified_sampling():
    pass