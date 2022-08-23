from constant import delimiter_hpo, quotechar_hpo, pii_table_list, table_name_list
import export_data
import configparser
import db_connection
import pandas as pd
from time import perf_counter
import json

def main():
    # Create db connection
    config = configparser.ConfigParser()
    config.read('a_dm_aou.ini')
    db_settings = config.defaults()
    conn = db_connection.test_conn(db_settings)

    with open('for_json_notes.sql', 'r') as query:
        for_json_sql = query.read()

        # Test speed of sql query with FOR JSON PATH
        t0= perf_counter()
        df_output = pd.read_sql_query(for_json_sql, conn)
        t1 = perf_counter()
        print(df_output)
        print("FOR JSON: ", t1 - t0)


    # Test speed of json library/pandas to convert to json
    with open('notes.sql', 'r') as query2:
        original_sql = query2.read()

        # Test speed of sql query with FOR JSON PATH
        t0= perf_counter()
        test_df2 = pd.read_sql_query(original_sql, conn)
        json_output = test_df2.to_json(orient='records', lines=True)
        t1 = perf_counter()
        print(json_output)
        print("PANDAS: ", t1 - t0)


if __name__ == "__main__":
    main()