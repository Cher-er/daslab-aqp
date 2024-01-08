import psycopg2
import csv
from config.config import SamplingConfig
import os
import re
from rich.progress import Progress


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
    selectivity = []
    cur.execute(f"select count(*) from {pgsql_parameter['database']};")
    total = cur.fetchone()[0]

    with Progress() as progress:
        progress.add_task("Processing...", total=len(commands), auto_refresh=True)
        for command in commands:
            cur.execute(command)
            record = cur.fetchone()[0]
            results.append(record)

            command = re.sub(r'\bAVG\b', 'COUNT', command, flags=re.IGNORECASE)
            command = re.sub(r'\bSUM\b', 'COUNT', command, flags=re.IGNORECASE)
            cur.execute(command)
            count = cur.fetchone()[0]
            selectivity.append(float(count) / total)

    output_file = os.path.join(output_dir, 'ground_truth.csv')
    with open(output_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(results)

    print(f"[INFO] ground truth has been saved in {output_file}")

    output_file = os.path.join(output_dir, 'selectivity.csv')
    with open(output_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(selectivity)

    print(f"[INFO] selectivity has been saved in {output_file}")

    cur.close()
    conn.close()
