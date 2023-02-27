from cgi import test
from constant import delimiter_hpo, quotechar_hpo, pii_table_list, table_name_list
import export_data as ed
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

    # with open('for_json_notes.sql', 'r') as query:
    #     for_json_sql = query.read()

    #     # Test speed of sql query with FOR JSON PATH
    #     t0= perf_counter()
    #     df_output = pd.read_sql_query(for_json_sql, conn)
    #     df_output_json = df_output.to_json(orient='records', lines=True)
    #     t1 = perf_counter()
    #     with open('for_json_output_test.txt', 'w', newline='') as for_json_file:
    #         for_json_file.write(df_output_json)
    #         for_json_file.close()
    #     #print(df_output)
    #     print("FOR JSON: ", t1 - t0)


    # Test speed of json library/pandas to convert to json
    with open('test_notes.sql', 'r') as query2:
        original_sql = query2.read()
        
        # Test speed of sql query with FOR JSON PATH
        t0= perf_counter()
        test_df2 = pd.read_sql_query(original_sql, conn)

        print(test_df2['note_source_value'])
        
        # Separate df into notes w/ note_source_value like ORDER_PROC_ID: and those without 
        # TODO: create function to format split dataframes
        json_output = ed.format_json(test_df2)

        with open('output_test.txt', 'w', newline='') as json_file:
            json_file.write(json_output)
            json_file.close()

        t1 = perf_counter()
        print('TIME:', t1-t0)



if __name__ == "__main__":
    main()