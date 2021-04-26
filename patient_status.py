import os
import pandas as pd
import numpy as np
from constant import rows_allowed, query_path, patient_status_folder


def extract_patient_status(db_properties, conn):
    ps_query = open(os.path.join(query_path, 'patient_status.sql'), 'r')
    ps_script = ps_query.read().format(db_properties['database'], db_properties['schema'])
    patient_status_df = pd.read_sql(ps_script, conn)
    for k, g in patient_status_df.groupby(np.arange(len(patient_status_df.index)) // rows_allowed, axis=0):
        g.to_csv(os.path.join(patient_status_folder, 'patient_status_{}.csv'.format(k + 1)), index=False)
    return print('files exported')
