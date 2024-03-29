from dateutil import tz
from dateutil.parser import parse
import numpy as np
import pandas as pd

NYC = tz.gettz('America/New_York')

#TODO: Add the data format enforcement while loading data from sql
def change_col_type(omop_check_files, df, file_name):
    '''
    Enforce column types
    '''
    for col in df.columns:
        col_type = omop_check_files[file_name][col]
        if col_type == 'string':
            df[col] = df[col].fillna('')
            df[col] = df[col].astype(str)
            df[col] = df[col].apply(lambda x: x.replace('"', '""').replace('\n', ' '))
        elif col_type == 'integer':
            df[col] = df[col].astype('Int64')
        elif col_type == 'float':
            df[col] = pd.to_numeric(df[col], errors='coerce').astype(float)
        elif col_type == 'date':
            df[col] = df[col].apply(lambda x: parse(x).strftime('%Y-%m-%d') if pd.notnull(x) else x)
        elif col_type == 'timestamp':
            df[col] = df[col].astype(object).where(df[col].notnull(), None)
            df[col] = df[col].apply(lambda x: parse(x).replace(tzinfo=NYC).isoformat() if pd.notnull(x) else x)
        else:
            pass
    df = df.replace(np.nan, '', regex=True)
    return df
