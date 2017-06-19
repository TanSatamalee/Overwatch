import requests
import locale
from bs4 import BeautifulSoup

url = 'https://playoverwatch.com/en-us/career/pc/us/'

my_ign = 'tannooby-11963'


# Returns BeautifulSoup object given a player's name.
def createSoup(player):
	page = requests.get(url + player)
	return BeautifulSoup(page.content, 'html.parser')


# Returns the overall player stats for a specific mode('qp' or 'comp').
def get_overall_stats(player, mode):
	# Checks for valid player argument
	if player is None:
		print('Not a valid player name.')
		return None

	soup = createSoup(player)
	featured_stats = soup.find_all(class_='card-heading')
	l = int(len(featured_stats) / 2)
	stats = []
	if mode == 'qp':
		for fs in featured_stats[:l]:
			stats.append(fs.get_text())
	elif mode == 'comp':
		for fs in featured_stats[l:]:
			stats.append(fs.get_text())
	else:
		print('Not a valid mode.')
		return None
	return stats


# Returns the label for the overall stats of a player.
def get_overall_stats_label():
	soup = createSoup(my_ign)
	featured_stats = soup.find_all(class_='card-copy')
	stats = []
	for fs in featured_stats:
		stats.append(fs.get_text())
	return stats[:int(len(stats) / 2)]


# Returns the player stats for specific heros in an array form.
def get_hero_stats(player, mode):
	soup = createSoup(player)

	# Find the page for the game mode.
	page = None
	if mode == 'qp':
		page = soup.find('div', {'id':'quickplay'})
	elif mode == 'comp':
		page = soup.find('div', {'id':'competitive'})
	else:
		print('Not a valid mode.')
		return None

	stats_array = []
	for c in page.find_all():
		if 'data-group-id' in c.attrs:
			stats = c.find_all('td')
			stats_dict = dict()
			n = 0
			while n < len(stats):
				stats_dict[stats[n].contents[0]] = stats[n + 1].contents[0]
				n = n + 2
			if stats_dict:
				stats_array.append(stats_dict)
	print(len(stats_array))

