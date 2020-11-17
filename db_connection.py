import pymssql
import pandas as pd


def db_conn(properties):

    db_user, db_pass, database, server, schema = properties['user'], properties['password'], \
                                 properties['database'], properties['server'], properties['schema']
    conn = pymssql.connect(server, db_user, db_pass, database)
    return conn


def test_conn(db_settings):
    try:
        query = "select 1 as test"
        conn = db_conn(db_settings)
        test_df = pd.read_sql(query, conn)
        if test_df.shape[0] >= 1:
            print('Sql Server connected')
        else:
            print('Sql Server not connected')
        return conn
    except Exception as e:
        print(str(e))
