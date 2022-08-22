import pandas as pd
import csv
import os
from constant import delimiter_hpo, quotechar_hpo, pii_table_list, table_name_list
from change_data_type import change_col_type
from tqdm import tqdm


def export_to_csv(file_path, query, conn, omop_check_files, file_name, empty_list):
    ''' 
    This function creates csv output for the given file input. The resulting output is determined by the kind of table the file name is associated with.

    Args:
        empty_list: list of empty tables
        file_path: output folder + file_name
        conn: db connection
        omop_check_files: json file to check datatype
    
    Returns:
        N/A

    Raises:
        N/A
    
    '''
    print('Start exporting {}...'.format(file_name))
    # if it is an empty table just write column headers
    if file_name in empty_list:
        data = pd.read_sql(query, conn)
        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=delimiter_hpo, quotechar=quotechar_hpo, quoting=csv.QUOTE_ALL)
            csv_writer.writerow(data.columns)
    # if it contains PII do not check data types
    # TODO: combine with else condition (check data types)
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
    # otherwise validate data types for all columns and output csv
    else:
        data = pd.read_sql(query, conn, chunksize=50000)
        is_header_added = False
        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=delimiter_hpo, quotechar=quotechar_hpo, quoting=csv.QUOTE_ALL)
            for batch in data:
                if file_name in table_name_list:
                    batch = change_col_type(omop_check_files, batch, file_name)
                else:
                    pass
                if not is_header_added:
                    csv_writer.writerow(batch.columns)
                    is_header_added = True
                for row in tqdm(batch.itertuples(index=False), total=len(batch)):
                    csv_writer.writerow(row)


#TODO: Create a function to export note table into jsonl
def export_to_jsonl(file_path, query, conn, omop_check_files, file_name, empty_list):
    data = pd.read_sql(query, conn)
    


def export_omop_file(table_name, query_path, output_path, connection, omop_check_files, empty_list, db_properties, person_list):
    query = open(os.path.join(query_path, f'{table_name}.sql'), 'r')
    query_script = query.read()
    if 'person_id' in query_script:
        query_script = query_script.format(db_properties['database'], db_properties['schema'], person_list)
    else:
        query_script = query_script.format(db_properties['database'], db_properties['schema'])
    if table_name == 'note':
        output_file_path = f'{output_path}{table_name}.jsonl'
        export_to_jsonl(output_file_path)
    else:
        output_file_path = f'{output_path}{table_name}.csv'
        export_to_csv(output_file_path, query_script, connection, omop_check_files, table_name, empty_list)
    query.close()
    return f'{table_name}.csv file exported'
