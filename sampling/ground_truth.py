import psycopg2
import csv
from config.config import SamplingConfig
import os


def exact():
    config = SamplingConfig().get_config()
    pgsql_parameter = config['pgsql']
    sql_file = config['sql_file']
    output_dir = config['output_dir']

    conn = psycopg2.connect(host=pgsql_parameter["host"],
                            port=pgsql_parameter["port"],
                            database=pgsql_parameter["database"],
                            user=pgsql_parameter["user"],
                            password=pgsql_parameter["password"])
    cur = conn.cursor()

    with open(sql_file, 'r') as f:
        commands = f.readlines()

    results = []
    for command in commands:
        cur.execute(command)
        record = cur.fetchone()
        results.append(record)

    with open(os.path.join(output_dir, 'ground_truth.csv'), 'w') as f:
        writer = csv.writer(f)
        writer.writerows(results)

    cur.close()
    conn.close()
