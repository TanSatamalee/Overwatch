# Overwatch API

An attempt at creating an easy way for obtaining any kind of information on Overwatch from known sources.

## playerstats.py

Gets data for specific players from *playoverwatch.com*.

`get_overall_stats(player, mode)`

Gets the overall stats for a player in a specific mode.
Arguments: player (username-battlenetid) && mode (qp, comp)
Return: 2D array of value labels and values for a player

`get_hero_stats(player, mode)`

Gets the overall stats for each hero for a specific player.
Arguments: player (username-battlenetid) && mode (qp, comp)
Return: 2D array of value labels followed by all values for each hero


## globalstats.py

Gets global data for heroes, leaderboards, etc. from *masteroverwatch.com*

`get_leaderboard()`

Gets a list of all top 500 players with their battlenet ids.
Arguments: none
Return: array of 500 strings of username and battlenet ids of the current top 500 players

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
