from dateutil import tz
import numpy as np
import pandas as pd

NYC = tz.gettz('America/New_York')


def change_col_type(omop_check_files, df, file_name):
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
            df[col] = df[col].apply(lambda x: x.isoformat() if pd.notnull(x) else x)
        elif col_type == 'timestamp':
            df[col] = df[col].astype(object).where(df[col].notnull(), None)
            df[col] = df[col].apply(lambda x: x.replace(tzinfo=NYC).isoformat() if pd.notnull(x) else x)
        else:
            pass
    df = df.replace(np.nan, '', regex=True)
    return df