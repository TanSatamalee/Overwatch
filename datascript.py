import globalstats as gs
import playerstats as ps
import logstats as ls

# This script is run daily to collect the appropriate data.

# Stores the global stats for all heroes.
#ls.store_global_stats()

# Stores all of my stats for all heroes.
ls.store_player_stats('tannooby-11963', 'my_stats')

# Stores and updates the leaderboard list for top players.
#ls.store_leaderboard()
