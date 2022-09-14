from email.quoprimime import quote
import os
from constant import query_path, output_path, delimiter_hpo, quotechar_hpo, rows_allowed
import pandas as pd
import numpy as np
import csv
import math
from change_data_type import change_col_type
from tqdm import tqdm


def read_write_person_file(db_properties, conn, omop_files, parse_dates):
    person_query = open(os.path.join(query_path, 'person.sql'), 'r')
    person_query_script = person_query.read().format(db_properties['database'], db_properties['schema'])
    person_table = pd.read_sql_query(person_query_script, conn, dtype=omop_files['person'], parse_dates=parse_dates['person'])
    person_list = person_table['person_id'].to_list()
    person_list = str(person_list).replace('[', '').replace(']', '')
    ###Export person table

    chunks = np.array_split(person_table.index, math.ceil(person_table.shape[0]/rows_allowed))
    for chunk, subset in enumerate(tqdm(chunks)):
        person_table = person_table.replace('None', '')
        if chunk == 0:
            person_table.iloc[subset].to_csv(os.path.join(output_path,'person.csv'), index=False, mode='w', sep=',', quoting=csv.QUOTE_NONNUMERIC, quotechar=quotechar_hpo, doublequote=True)
        else:
            person_table.iloc[subset].to_csv(os.path.join(output_path,'person.csv'), index=False, mode='a', header=False, sep=',', quoting=csv.QUOTE_NONNUMERIC, quotechar=quotechar_hpo, doublequote=True)

    print("Person table is written into database")
    return person_list
