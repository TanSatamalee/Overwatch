import sqlite3
import datetime
import globalstats as gs
import playerstats as ps
import pandas as pd
from pathlib import Path


# Checks filename to make sure correct type.
def _check_db_name(db):
    if not db[-3:] == '.db':
        db += '.db'
    return db

# Connects to a database.
def _sql_conn(db, table, con):
    if con == None:
        db = _check_db_name(db)
        conn = sqlite3.connect(db)
    else:
        conn = con
    return conn

# Checks database if table exists.
def _check_table_exist(db, table, con=None):
    conn = _sql_conn(db, table, con)
    if not conn.execute("SELECT name FROM sqlite_master WHERE type='table' and name=\'" + table + "\'").fetchone():
        return False
    return True


# Returns the column names for a specified filename and table.
def get_table_column_keys(db, table, con=None):
    conn = _sql_conn(db, table, con)
    cursor = conn.execute('SELECT * FROM ' + table)
    names = list(map(lambda x: x[0], cursor.description))
    return names


# Prints tables for specific filename.
def print_database(db, table):
    db = _check_db_name(db)
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    print(get_table_column_keys(db, table, conn))
    cur.execute('SELECT * FROM ' + table)
    for a in cur.fetchall():
        print(a)
    conn.close()


# Writes/updates a pandas array into a specified filename and table.
def write_db(data, db, table):
    db = _check_db_name(db)
    conn = sqlite3.connect(db)
    if _check_table_exist(db, table, conn):
        temp = pd.read_sql_query('SELECT * FROM ' + table, conn)
        arr = pd.concat([temp, data], axis=0, ignore_index=True)
        if 'level_0' in arr:
            arr = arr.drop('level_0', axis=1)
    else:
        arr = data
    conn.execute('DROP TABLE IF EXISTS ' + table)
    arr.to_sql(table, conn)
    conn.commit()
    conn.close()


# Writes/updates a pandas array into a specified filename and table.
# This also updates the 'count' column for any duplicates.
def write_db_count(data, db, table):
    db = _check_db_name(db)
    conn = sqlite3.connect(db)
    if _check_table_exist(db, table, conn):
        temp = pd.read_sql_query('SELECT * FROM ' + table, conn)
        arr = pd.concat([temp, data], axis=0, ignore_index=True)
        if 'level_0' in arr:
            arr = arr.drop('level_0', axis=1)
        temp['count'] = arr.groupby(list(data)[:2])['count'].transform('sum')
        conn.execute('DROP TABLE IF EXISTS ' + table)
        temp.to_sql(table, conn)
    else:
        conn.execute('DROP TABLE IF EXISTS ' + table)
        data['count'] = 1
        data.to_sql(table, conn)
    conn.commit()
    conn.close()


# Reads a pandas array from a specified filename and table.
def read_db(db, table):
    db = _check_db_name(db)
    conn = sqlite3.connect(db)
    if _check_table_exist(db, table, conn):
        arr = pd.read_sql_query('SELECT * FROM ' + table, conn)
    else:
        print('Table does not exist.')
    conn.close()
    return arr


# Drops given table from a specified filename.
def drop_table(db, table):
    db = _check_db_name(db)
    conn = sqlite3.connect(db)
    conn.execute('DROP TABLE IF EXISTS ' + table)
    conn.commit()
    conn.close()
