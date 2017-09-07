import logger
import globalstats as gs
import time

# This script will run daily for data collection.

# Starting 09-06-2017

locations = ['global','us','eu','kr','cn']
modes = ['qp','comp']

# Keep track of how much time each part takes.
start = time.time()
def time_elapsed():
	global start
	print(str(time.time() - start) + ' seconds')

# For global stats stores for all locations with each mode as a table
for l in locations:
	for m in modes:
		logger.store_global_stats(l, m, 'Season6/globalstats_' + l, m)

time_elapsed()

# For leaderboards only keeps track for global and us (including each hero)
heros = gs._get_hero_dict()
for l in locations[:2]:
	logger.store_leaderboard(l, None, 'Season6/lb_' + l)
	for h in heros:
		logger.store_leaderboard(l, h, 'Season6/lb_' + l + '_' + h)

time_elapsed()