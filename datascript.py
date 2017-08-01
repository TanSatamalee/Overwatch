import globalstats as gs
import playerstats as ps
import logstats as ls
# This script is run daily to collect the appropriate data.

locations = ['global', 'us', 'eu', 'kr', 'cn']

# Stores the global stats for all heroes.
#ls.store_global_stats()

# Stores all of my stats for all heroes.
#ls.store_player_stats('tannooby-11963', 'my_stats')

# Stores and updates the leaderboard list for top players.
heros = gs._get_hero_dict()
for l in locations:
	ls.store_leaderboard(l)
	for h in heros.keys():
		ls.store_leaderboard(l, h)
