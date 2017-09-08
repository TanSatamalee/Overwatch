import sqlite3
import datetime
import globalstats as gs
import playerstats as ps
import pandas as pd
import numpy as np
import utils
from pathlib import Path

locations = ['global','us','eu','kr','cn']
modes = ['qp','comp']

# Returns the date as an integer for easy sorting (year + month + day)
def _get_date():
    now = datetime.datetime.now()
    year = str(now.year)
    if len(str(now.month)) < 2:
        month = '0' + str(now.month)
    else:
        month = str(now.month)
    if len(str(now.day)) < 2:
        day = '0' + str(now.day)
    else:
        day = str(now.day)
    return int(year + month + day)


# Adds a date column to pandas array.
def _add_date(data):
    date = _get_date()
    if type(data) == 'list':
        for d in data:
            d['date'] = date
    else:
        data['date'] = date
    return data


# Stores the global stats for a specific location and mode into a db file.
def store_global_stats(location, mode, filename, table):
    date = _get_date()
    data = gs.get_global_stats(location, mode)
    if data is None:
        return
    data = _add_date(data)
    utils.write_db(data, filename, table)


# Stores each hero stats for an individual player
def store_player_stats(player, location, mode, filename):
    date = _get_date()
    data = ps.get_hero_stats(player, mode)
    if data is None:
        return
    for d in data:
        hero = d['hero'][0]
        d = _add_date(d)
        utils.write_db(d, filename, hero)


# Stores specific hero stats for an individual player
def store_player_hero_stats(player, location, hero, mode, filename, table):
    date = _get_date()
    data = ps.get_hero_stats(player, mode)
    if data is None:
        return
    for d in data:
        h = d['hero'][0]
        if h == hero:
            d = _add_date(d)
            utils.write_db(d, filename, table)
            break


# Stores the leaderboard for a given location and hero (if specified)
def store_leaderboard(location, hero, filename):
    date = _get_date()
    lb = gs.get_top500(location, hero)
    if lb is None:
        return

    utils.write_db(lb, filename, 'current_lb')
    
    utils.write_db_count(lb, filename, 'total_lb')


# Reads a pandas array from a given filename and table
def read_database(filename, table):
    return utils.read_db(filename, table)