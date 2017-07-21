# Overwatch API

An attempt at creating an easy way for obtaining any kind of information on Overwatch from known sources.

## playerstats.py

Gets data for specific players from *playoverwatch.com*.

`get_overall_stats(player, mode)`

Gets the overall stats for a player in a specific mode.
Arguments: player (username-battlenetid) && mode (qp, comp)
Return: 2D array of value labels and values for a player. First row is the labels and second row is values. ** ALL VALUES ARE IN STRING **

`get_hero_stats(player, mode)`

Gets the overall stats for each hero for a specific player.
Arguments: player (username-battlenetid) && mode (qp, comp)
Return: 2D array of dictonaries of stats for each hero. ** ALL VALUES ARE IN STRING **


## globalstats.py

Gets global data for heroes, leaderboards, etc. from *masteroverwatch.com*

`get_leaderboard()`

Gets a list of all top 500 players with their battlenet ids. (NOTE THAT THIS OPENS A CHROME BROWSER AND GOING TO MASTEROVERWATCH)
Arguments: none
Return: array of 500 strings of username and battlenet ids of the current top 500 players ** STILL NEED TO DEBUG UNCONVENTIONAL NAMES **

`get_hero_overview(location, mode)`

Gets the overall stats for heroes.
Arguments: location (global, us, eu, kr, cn) && mode (qp, comp)
Return: 2D array of hero name, popularity, winrate, KDA, and medals for all heroes

`get_hero_combat(location, mode)`

Gets the combat stats for heroes.
Arguments: location (global, us, eu, kr, cn) && mode (qp, comp)
Return: 2D array of hero name, elims, deaths, damage, block, heals, and accuracy for all heroes

`get_hero_misc(location, mode)`

Gets the combat stats for heroes.
Arguments: location (global, us, eu, kr, cn) && mode (qp, comp)
Return: 2D array of hero name, obj time, obj kills, medals, and cards for all heroes

'get_global_stats(location, mode)'
Gets the all stats for heroes.
Arguments: location (global, us, eu, kr, cn) && mode (qp, comp)
Return: 2D array of all hero stats. First row is all the labels for the column values. The following rows start with the hero name and then the values for the corrsponding stats.


## logstats.py

'store_global_stats()'
Stores the global stats in a sqlite file for each region and game mode.
Return: Creates a database for each region and game mode.