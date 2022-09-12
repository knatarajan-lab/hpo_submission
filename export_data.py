from distutils.command.clean import clean
import pandas as pd
import numpy as np
import csv
import os
import re
from constant import delimiter_hpo, quotechar_hpo, pii_table_list, table_name_list
from change_data_type import change_col_type
from tqdm import tqdm


def export_to_csv(file_path, query, conn, omop_check_files, parse_dates, file_name, empty_list):
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
        data = pd.read_sql_query(query, conn)
        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=delimiter_hpo, quotechar=quotechar_hpo, quoting=csv.QUOTE_ALL)
            csv_writer.writerow(data.columns)
    # if it contains PII do not check data types
    # TODO: combine with else condition (check data types)
    elif file_name in pii_table_list:
        data = pd.read_sql_query(query, conn)
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
        datatypes = omop_check_files[file_name]
        parse_dates_list = parse_dates[file_name]
        data = pd.read_sql_query(query, conn, dtype=datatypes, parse_dates=parse_dates_list, chunksize=50000)
        is_header_added = False
        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=delimiter_hpo, quotechar=quotechar_hpo, quoting=csv.QUOTE_ALL)
            for batch in data:
                # if file_name in table_name_list:
                #     batch = change_col_type(omop_check_files, batch, file_name)
                # else:
                #     pass
                if not is_header_added:
                    csv_writer.writerow(batch.columns)
                    is_header_added = True
                for row in tqdm(batch.itertuples(index=False), total=len(batch)):
                    csv_writer.writerow(row)


def clean_note_text(df):
    ''' 
    This function will take in a dataframe and replace extra carriage returns found in the note_text column of certain notes

    Args:
        df: dataframe to be cleaned
    
    Returns:
        df: dataframe with carriage returns removed

    Raises:
        N/A
    
    '''
    if 'note_text' in df:
        df['note_text'] = df['note_text'].str.replace('&#x0D;','\n')
        df['note_text'] = df['note_text'].str.replace('#x0D;','')

    return df


def format_json(df):
    ''' 
    This function takes in a list of dataframes and paritions rows that require removal of erroneous characters from the note_text column. The replaced/formatted text is then reinserted into the data frame row and then the entire data frame is converted to a json object string.

    Args:
        df: dataframe to be converted to json
    
    Returns:
        json_output: string output by pandas.to_json containing a json string of the following format {key1: value1, key2:value2, ...}

    Raises:
        N/A
    
    '''
    
    # Return tuple (x,y) -> (boolean, df_partition)
    dataframes= [(x,y) for x, y in df.groupby(df['note_source_value'].str.contains('ORDER_PROC_ID:'))]
    # Go through each tuple
    formatted_df = pd.DataFrame()
    for conditional, df_group in dataframes:
        # If the first tuple's boolean is True this means the df needs to be reformatted and concatenated to the final df
        if conditional:
            reformatted_df = clean_note_text(df_group)
            formatted_df = formatted_df.append(reformatted_df)
        # Otherwise the df is already formatted correctly and can be concatenated as is
        else:
            formatted_df = formatted_df.append(df_group)

    formatted_df['note_text'] = formatted_df['note_text'].apply(spaces_to_newline)
    print(formatted_df['note_text'])
    json = formatted_df.to_json(orient='records', date_format='iso', force_ascii=True, lines=True)
    return json


def spaces_to_newline(input_text):
    clean_text = input_text.replace('    ', '\n').replace('   ', '\n')
    collapsed_newline_text = re.sub(r'\n+', '\n', clean_text)
    return collapsed_newline_text

def export_to_jsonl(file_path, query, conn):
    df_notes = pd.read_sql_query(query, conn, dtype={'visit_occurrence_id':'Int64'})
    json_notes = format_json(df_notes)
    with open(file_path, 'w', newline='') as json_file:
        json_file.write(json_notes)
        json_file.close()


def export_omop_file(table_name, query_path, output_path, connection, omop_check_files, parse_dates, empty_list, db_properties, person_list):
    query = open(os.path.join(query_path, f'{table_name}.sql'), 'r')
    query_script = query.read()
    if 'person_id' in query_script:
        query_script = query_script.format(db_properties['database'], db_properties['schema'], person_list)
    else:
        query_script = query_script.format(db_properties['database'], db_properties['schema'])
    if table_name == 'note':
        output_file_path = f'{output_path}{table_name}.jsonl'
        export_to_jsonl(output_file_path, query_script, connection)
    else:
        output_file_path = f'{output_path}{table_name}.csv'
        export_to_csv(output_file_path, query_script, connection, omop_check_files, parse_dates, table_name, empty_list)
    query.close()
    return f'{table_name}.csv file exported'
