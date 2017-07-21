import sqlite3
import datetime
import globalstats as gs
from pathlib import Path


locations = ['global','us','eu','kr','cn']
modes = ['qp','comp']

# Saves global hero stats for all locations and modes in files.
# File naming: mode_location_globalstats.db
def store_global_stats():
    now = datetime.datetime.now()
    date = str(now.month) + str(now.day) + str(now.year)
    global locations, modes
    for l in locations:
        for m in modes:
            data = gs.get_global_stats(l, m)
            prefix = m + '_' + l + '_'
            conn = sqlite3.connect(m + '/' + prefix + 'globalstats.db')

            create_table = '''CREATE TABLE IF NOT EXISTS globalstats 
                (key TEXT PRIMARY KEY, date TEXT, hero TEXT'''
            for label in data[0][1:]:
                create_table += ', ' + label + ' REAL'
            create_table += ');'
            conn.execute(create_table)

            insert_table = 'INSERT INTO globalstats VALUES(\'' + date
            for d in data[1:]:
                temp = insert_table + d[0] + '\', ' + date
                d[0] = '\'' + d[0] + '\''
                for v in d:
                    temp +=  ', ' + str(v)
                conn.execute(temp + ' )')

            conn.commit()
            conn.close()


# Prints the column names for a table conn.
def _get_table_column_keys(conn):
    cursor = conn.execute('select * from globalstats')
    names = list(map(lambda x: x[0], cursor.description))
    print(names)

# Prints tables for specific database name.
def _print_database(name):
    conn = sqlite3.connect(name)
    cur = conn.cursor()
    cur.execute('SELECT * FROM globalstats')
    for a in cur.fetchall():
        print(a)
