import sqlite3
import datetime
import globalstats as gs
import playerstats as ps
import pandas as pd
from pathlib import Path

locations = ['global','us','eu','kr','cn']
modes = ['qp','comp']


# Checks filename to make sure correct type.
def __check_db_name(db):
    if not db[-3:] == '.db':
        db += '.db'
    return db

# Connects to a database.
def __sql_conn(db, table, con):
    if con == None:
        db = __check_db_name(db)
        conn = sqlite3.connect(db)
    else:
        conn = con
    return conn

# Checks database if table exists.
def __check_table_exist(db, table, con=None):
    conn = __sql_conn(db, table, con)
    if not conn.execute('SELECT * FROM ' + table):
        return False
    return True


# Returns the column names for a specified database file and table.
def _get_table_column_keys(db, table, con=None):
    conn = __sql_conn(db, table, con)
    cursor = conn.execute('SELECT * FROM ' + table)
    names = list(map(lambda x: x[0], cursor.description))
    return names


# Prints tables for specific database file.
def _print_database(db, table):
    db = __check_db_name(db)
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    print(_get_table_column_keys(db, table, conn))
    cur.execute('SELECT * FROM ' + table)
    for a in cur.fetchall():
        print(a)
    conn.close()


# Writes/updates a pandas array into a specified database file and table.
def _write_db(data, db, table):
    db = __check_db_name(db)
    conn = sqlite3.connect(db)
    if __check_table_exist(db, table, conn):
        temp = pd.read_sql_query('SELECT * FROM ' + table, conn)
        arr = pd.concat([temp, data], axis=0, ignore_index=True)
        if 'level_0' in arr:
            arr = arr.drop('level_0', axis=1)
    else:
        arr = data
    arr.to_sql(table, conn)
    conn.commit()
    conn.close()


# Reads a pandas array from a specified database file and table.
def _read_db(db, table):
    db = __check_db_name(db)
    conn = sqlite3.connect(db)
    arr = pd.read_sql_query('SELECT * FROM ' + table, conn)
    conn.close()
    return arr
