import sqlite3
import datetime
import globalstats as gs
import playerstats as ps
import pandas as pd
from pathlib import Path

locations = ['global','us','eu','kr','cn']
modes = ['qp','comp']


# Returns the column names for a table conn.
def _get_table_column_keys(conn, table):
    cursor = conn.execute('select * from ' + table)
    names = list(map(lambda x: x[0], cursor.description))
    return names

# Prints tables for specific database name.
def _print_database(name, table):
    conn = sqlite3.connect(name)
    cur = conn.cursor()
    print(_get_table_column_keys(conn, table))
    cur.execute('SELECT * FROM ' + table)
    for a in cur.fetchall():
        print(a)


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


# Saves player sats for all modes for a specific player.
# Player: username-battlenetid
# Folder: name of folder to put database file into.
def store_player_stats(player, folder):
    now = datetime.datetime.now()
    date = str(now.month) + str(now.day) + str(now.year)
    global modes
    for m in modes:
        data = ps.get_hero_stats(player, m)
        for d in data:
            hero = d['hero']
            conn = sqlite3.connect(folder + '/' + player + '_' + m + '_playerstats.db')

            create_table = 'CREATE TABLE IF NOT EXISTS ' + hero \
                + ' (date TEXT PRIMARY KEY'
            for label in d:
                if not label == 'hero':
                    create_table += ', ' + label + ' REAL'
            create_table += ');'
            conn.execute(create_table)

            d['date'] = date
            del d['hero']
            old_arr = pd.read_sql_query('SELECT * FROM ' + hero, conn)
            new_arr = pd.DataFrame([d], columns=d.keys())
            if any(old_arr.date == date):
                arr = old_arr
            else:
                arr = pd.concat([old_arr,new_arr], axis=0, ignore_index=True)
                if 'level_0' in arr:
                    arr = arr.drop('level_0', axis=1)
            conn.execute('DROP TABLE IF EXISTS ' + hero)
            arr.to_sql(hero, conn)

            conn.commit()
            conn.close()


# Updates current top 500 players into databases (for heroes if specified).
# Keeps track of all players who have made leaderboard and the current leaderboard.
# Locations: global, us, eu, kr, cn
def store_leaderboard(location, hero=None):
    now = datetime.datetime.now()
    date = '\'' + str(now.month) + str(now.day) + str(now.year) + '\''
    if hero is None:
        conn = sqlite3.connect('top500/' + location + '_leaderboard.db')
    else:
        conn = sqlite3.connect('top500/' + location + '_' + hero + '_leaderboard.db')

    create_table = '''CREATE TABLE IF NOT EXISTS total_lb 
                (player TEXT PRIMARY KEY, region TEXT, date TEXT, amt INT)'''
    conn.execute(create_table)

    conn.execute('DROP TABLE IF EXISTS current_lb')
    create_table2 = '''CREATE TABLE IF NOT EXISTS current_lb 
                (player TEXT, region TEXT)'''
    conn.execute(create_table2)

    cursor = conn.cursor()
    lb = gs.get_top500(location, hero)
    for p in lb:
        ign = '\'' + p[0]  + '\''
        cty = '\'' + p[1]  + '\''
        cursor.execute('SELECT player FROM total_lb WHERE player = ' + ign)
        n = cursor.fetchone()
        if n is None:
            conn.execute('INSERT INTO total_lb VALUES(' + ign + ', ' + cty + ', ' + date + ', 1)')
        else:
            cur = conn.execute('SELECT amt FROM total_lb WHERE player = ' + ign)
            for row in cur:
                x = row[0] + 1
            conn.execute('UPDATE total_lb SET amt = ' + str(x) + ' WHERE player = ' + ign)
        conn.execute('INSERT INTO current_lb VALUES(' + ign + ', ' + cty + ')')
    conn.commit()
    conn.close()
