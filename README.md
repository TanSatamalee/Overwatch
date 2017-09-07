# Overwatch Webscraper and Logger

Easy to use webscraper that gets info from *playoverwatch.com* and *masteroverwatch.com* and returns 'pandas' arrays of data. Also has a logger to store info using SQLite.

## `playerstats.py`

Gets data for specific players from *playoverwatch.com*.

`get_overall_stats(player, mode)`

Gets the overall stats for a player in a specific mode.

`get_hero_stats(player, mode)`

Gets the overall stats for each hero for a specific player.



## `globalstats.py`

Gets global data for heroes, leaderboards, etc. from *masteroverwatch.com*

`get_top500(location, hero)`

Gets a list of top 500 players with their battlenet ids (can also get top 500 for a specific hero). Hero is `None` if general top 500 is wanted.

`get_global_stats(location, mode)`

Gets the data for all heros in a particular region.



## `logger.py`

`store_global_stats(location, mode, filename, table)`

Logs the global stats for a particular location and mode at the given filename and table.

`store_player_stats(player, mode, filename)`

Logs the player stats for a given battlenet id at the given filename where the table name are the heros.

`store_leaderboard(location, hero, filename)`

Logs the leaderboard (top 500) for a locatin at a given filename. If a hero is given, then the top 500 players of that hero will be stored instead.


### Example

An example script is given in `scraper.py` and the SQLite files are in the Season(X) folders.