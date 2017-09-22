import logger
import globalstats as gs
import re
import time

# This script will run daily for data collection.

# Starting 09-06-2017

locations = ['global','us','eu','kr','cn']
modes = ['qp','comp']
season = 'Season6'
heros = gs._get_hero_dict().keys()

# Keep track of how much time each part takes.
start = time.time()
def time_elapsed():
	global start
	print(str(time.time() - start) + ' seconds')


# For global stats stores for all locations with each mode as a table
for l in locations:
	for m in modes:
		logger.store_global_stats(l, m, season + '/globalstats_' + l, m)

time_elapsed()

'''
# For leaderboards only keeps track for global and us (including each hero)
for l in locations[:2]:
	logger.store_leaderboard(l, None, season + '/lb_' + l)
	for h in heros:
		logger.store_leaderboard(l, h, season + '/lb_' + l + '_' + h)

time_elapsed()


# Keeps track of all top 500 stats for a specific hero.
for l in locations[:2]:
	for h in heros:
		# Gets all who have made top 500 this season
		lb = logger.read_database(season + '/lb_' + l + '_' + h, 'total_lb')
		for index, row in lb.iterrows():
			if row['name'].split('-')[0].isalnum():
				print(row['name'])
				print(row['region'])
				logger.store_player_hero_stats(row['name'], row['region'], h, 'comp', season + '/hero/' + h, season)
				break
		break
	break
'''