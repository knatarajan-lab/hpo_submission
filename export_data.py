import pandas as pd
import csv
import os
from constant import delimiter_hpo, quotechar_hpo, pii_table_list, file_name_list
from change_data_type import change_col_type
from tqdm import tqdm


def export_to_csv(file_path, query, conn, omop_check_files, file_name, empty_list):
    print('Start exporting {}...'.format(file_name))
    if file_name in empty_list:
        data = pd.read_sql(query, conn)
        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=delimiter_hpo, quotechar=quotechar_hpo, quoting=csv.QUOTE_ALL)
            csv_writer.writerow(data.columns)
    elif file_name in pii_table_list:
        data = pd.read_sql(query, conn)
        is_header_added = False
        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=delimiter_hpo, quotechar=quotechar_hpo, quoting=csv.QUOTE_ALL)
            if not is_header_added:
                csv_writer.writerow(data.columns)
                is_header_added = True
            for row in tqdm(data.itertuples(index=False), total=data.shape[0]):
                csv_writer.writerow(row)
    else:
        data = pd.read_sql(query, conn, chunksize=50000)
        is_header_added = False
        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=delimiter_hpo, quotechar=quotechar_hpo, quoting=csv.QUOTE_ALL)
            for batch in data:
                if file_name in file_name_list:
                    batch = change_col_type(omop_check_files, batch, file_name)
                else:
                    pass
                if not is_header_added:
                    csv_writer.writerow(batch.columns)
                    is_header_added = True
                for row in tqdm(batch.itertuples(index=False), total=len(batch)):
                    csv_writer.writerow(row)


def export_omop_file(file_name, query_path, output_path, connection, omop_check_files, empty_list, db_properties, person_list):
    query = open(os.path.join(query_path, file_name + '.sql'), 'r')
    query_script = query.read()
    if 'person_id' in query_script:
        query_script = query_script.format(db_properties['database'], db_properties['schema'], person_list)
    else:
        query_script = query_script.format(db_properties['database'], db_properties['schema'])
    output_file_path = output_path + file_name + '.csv'
    export_to_csv(output_file_path, query_script, connection, omop_check_files, file_name, empty_list)
    query.close()
    return file_name + '.csv file exported'
