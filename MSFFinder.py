import re

import pyodbc
import pandas as pd


def db():
    server = 'hacker1'
    database = 'skodahacker1'
    username = 'hacker1'
    password = 'hacker1'
    driver = '{ODBC Driver 17 for SQL Server}'

    conn = pyodbc.connect(
        'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

    return conn


def main():
    conn = db()
    cursor = conn.cursor()
    tables = cursor.tables(tableType='TABLE')
    list_of_tables = tables.fetchall()

    list_of_tables = [x[2] for x in list_of_tables]
    list_of_tables = list_of_tables[:-2]  # last two tables are sys tables

    sysmon_tables = [table for table in list_of_tables if 'sysmon' in table]
    CMD_REGEX = re.compile(r"(ParentCommandLine:.*""powershell.exe"".*hidden)")

    sqls = ["SELECT * FROM PC1_sysmon", "SELECT * FROM PC2_sysmon", "SELECT * FROM PC3_sysmon",
            "SELECT * FROM PC4_sysmon"]

    # for sql in sqls:
    sql = "SELECT * FROM PC2_sysmon"
    df = pd.read_sql(sql, conn)
    result = pd.DataFrame()
    for _, row in df['Message'].iteritems():
        match = CMD_REGEX.search(row)
        if match:
            splitted_result = row.split('\r\n')
            result_dict = {}
            for pair in splitted_result:
                splitted_pair = pair.split(":")
                result_dict[splitted_pair[0]] = "".join(splitted_pair[1:])
            result = result.append(pd.Series(result_dict), ignore_index=True)
    result.to_csv(f'powershell.csv', index=False)


if __name__ == "__main__":
    main()
