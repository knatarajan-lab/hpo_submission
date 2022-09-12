import os
from constant import query_path, output_path, delimiter_hpo, quotechar_hpo
import pandas as pd
import csv
from change_data_type import change_col_type
from tqdm import tqdm


def read_write_person_file(db_properties, conn, omop_files, parse_dates):
    print(omop_files)
    person_query = open(os.path.join(query_path, 'person.sql'), 'r')
    person_query_script = person_query.read().format(db_properties['database'], db_properties['schema'])
    person_table = pd.read_sql_query(person_query_script, conn, dtype=omop_files['person'], parse_dates=parse_dates['person'])
    print(person_table)
    person_list = person_table['person_id'].to_list()
    person_list = str(person_list).replace('[', '').replace(']', '')
    ###Export person table
    is_header_added = False
    
    with open(output_path + 'person.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=delimiter_hpo, quotechar=quotechar_hpo, quoting=csv.QUOTE_ALL)
        # person_table = change_col_type(omop_files, person_table, 'person')
        if not is_header_added:
            csv_writer.writerow(person_table.columns)
            is_header_added = True
        for row in tqdm(person_table.itertuples(index=False), total=person_table.shape[0]):
            csv_writer.writerow(row)
    print("Person table is written into database")
    return person_list
