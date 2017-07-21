import sqlite3
import datetime
import globalstats as gs
from pathlib import Path


locations = ['global','us','eu','kr','cn']
modes = ['qp','comp']

# Saves global hero stats for all locations and modes in files.
# File naming: location_mode_date.txt
def store_global_stats():
    now = datetime.datetime.now()
    date = str(now.month) + str(now.day) + str(now.year)
    global locations, modes
    for l in locations:
        for m in modes:
            data = gs.get_global_stats(l, m)
            prefix = m + '_' + l + '_'
            conn = sqlite3.connect(prefix + 'globalstats.db')

            create_table = '''CREATE TABLE IF NOT EXISTS globalstats 
                (date TEXT, hero TEXT'''
            for l in data[0][1:]:
                create_table += ', ' + l + ' REAL'
            create_table += ');'
            conn.execute(create_table)

            insert_table = 'INSERT INTO globalstats VALUES(' + date
            for d in data[1:]:
                temp = insert_table
                d[0] = '\'' + d[0] + '\''
                for v in d:
                    temp +=  ', ' + str(v)
                conn.execute(temp + ' )')

            conn.commit()
            conn.close()

store_global_stats()

# For debugging. Prints the column names for a table conn.
def _get_table_column_keys(conn):
    cursor = conn.execute('select * from globalstats')
    names = list(map(lambda x: x[0], cursor.description))
    print(names)