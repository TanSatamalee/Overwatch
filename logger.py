import sqlite3
import datetime
import globalstats as gs
import playerstats as ps
import pandas as pd
import utils
from pathlib import Path

locations = ['global','us','eu','kr','cn']
modes = ['qp','comp']

# Stores the global stats for a specific location and mode into a db file.
def store_global_stats(location, mode, filename, table):
    now = datetime.datetime.now()
    date = str(now.month) + str(now.day) + str(now.year)
    data = gs.get_global_stats(location, mode)
    data['date'] = date
    utils.write_db(data, filename, table)


# Stores each hero stats for an individual player
def store_player_stats(player, mode, filename):
	now = datetime.datetime.now()
    date = str(now.month) + str(now.day) + str(now.year)
    data = ps.get_hero_stats(player, mode)
    for d in data:
    	hero = d['hero']
    	d['date'] = date
    	utils.write_db(d, filename, hero)


# Stores the leaderboard for a given location and hero (if specified)
def store_leaderboard(location, hero=None, filename):
    now = datetime.datetime.now()
    date = str(now.month) + str(now.day) + str(now.year)
    lb = gs.get_top500(location, hero)

    utils.drop_table(filename, 'current_lb')
    utils.write_db(lb, filename, 'current_lb')

    utils.write_db_count(lb, filename, 'total_lb')
