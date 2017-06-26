import playerstats as ps
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

# Returns a list of the top 500 players with their id.
def get_leaderboard():
	url = 'https://masteroverwatch.com/leaderboards/pc/global'
	browser = webdriver.Chrome("C:/Games/chromedriver.exe")
	browser.get(url)
	time.sleep(1)

	elem = browser.find_element_by_tag_name("body")

	pagedowns = 60
	while pagedowns:
		elem.send_keys(Keys.PAGE_DOWN)
		time.sleep(1)
		pagedowns = pagedowns - 1

	soup = BeautifulSoup(browser.page_source, 'html.parser')
	links = soup.find_all('a', {'class':'table-row-link'}, href=True)

	players = []
	for p in links:
		players.append(p['href'])

	return players


# Returns the overview stats of all heroes for a specified mode.
# Stats: Popularity, Winrate, KDA, Medals
# Locations: global, us, eu, kr, cn
# Mode: qp, comp
def get_hero_overview(location, mode):
	url = 'https://masteroverwatch.com/heroes/pc/' + location + '/mode/'
	if mode == 'qp':
		url = url + 'quick'
	elif mode == 'comp':
		url = url + 'ranked'
	else:
		return None

	page = ps._request_page(url)
	soup = BeautifulSoup(page.content, 'html.parser')

	table = soup.find_all('div', class_='tab-pane')
	heroes = table[0].find('div', class_='table-body').find_all(class_='table-row row')
	
	hero_name = []
	popularity = []
	winrate = []
	kda = []
	medals = []
	for h in heroes:
		hero_name.append(h.find('strong').getText())
		t = h.find_all(class_='bar-outer')
		popularity.append(t[0].getText())
		winrate.append(t[1].getText())
		kda.append(t[2].getText())
		medals.append(t[3].getText())

	result = [hero_name, popularity, winrate, kda, medals]

	return result

# Returns the combat stats of all heroes for a specified mode.
# Stats: elims, deaths, damage, block, heals, accuracy
# Locations: global, us, eu, kr, cn
# Mode: qp, comp
def get_hero_combat(location, mode):
	url = 'https://masteroverwatch.com/heroes/pc/' + location + '/mode/'
	if mode == 'qp':
		url = url + 'quick'
	elif mode == 'comp':
		url = url + 'ranked'
	else:
		return None

	page = ps._request_page(url)
	soup = BeautifulSoup(page.content, 'html.parser')

	table = soup.find_all('div', class_='tab-pane')
	heroes = table[1].find('div', class_='table-body').find_all(class_='table-row row')
	
	hero_name = []
	elim = []
	death = []
	damage = []
	block = []
	heal = []
	acc = []
	for h in heroes:
		hero_name.append(h.find('strong').getText())
		t = h.find_all(class_='bar-outer')
		elim.append(t[0].getText())
		death.append(t[1].getText())
		damage.append(t[2].getText())
		block.append(t[3].getText())
		heal.append(t[4].getText())
		acc.append(t[5].getText())

	result = [hero_name, elim, death, damage, block, heal, acc]

	return result


# Returns the misc stats of all heroes for a specified mode.
# Stats: obj time, obj kills, medals, cards
# Locations: global, us, eu, kr, cn
# Mode: qp, comp
def get_hero_misc(location, mode):
	url = 'https://masteroverwatch.com/heroes/pc/' + location + '/mode/'
	if mode == 'qp':
		url = url + 'quick'
	elif mode == 'comp':
		url = url + 'ranked'
	else:
		return None

	page = ps._request_page(url)
	soup = BeautifulSoup(page.content, 'html.parser')

	table = soup.find_all('div', class_='tab-pane')
	heroes = table[1].find('div', class_='table-body').find_all(class_='table-row row')
	
	hero_name = []
	obj_time = []
	obj_kill = []
	medals = []
	cards = []
	for h in heroes:
		hero_name.append(h.find('strong').getText())
		t = h.find_all(class_='bar-outer')
		obj_time.append(t[0].getText())
		obj_kill.append(t[1].getText())
		medals.append(t[2].getText())
		cards.append(t[3].getText())

	result = [hero_name, obj_time, obj_kill, medals, cards]

	return result


# Converts data string scraped from website to anfloat stat.
def _convert(data):
	data = data.replace(',','')
	if data[-1] == '%':
		return float(data[:-1])
	elif len(data) > 1 and data[-2] == ':':
		return float(data[:-2])
	else:
		return float(data)


# Returns all global stats for all heroes for a specified mode and location.
# Locations: global, us, eu, kr, cn
# Mode: qp, comp
def get_global_stats(location, mode):
	overview = get_hero_overview(location, mode)
	combat = get_hero_combat(location, mode)
	misc = get_hero_misc(location, mode)

	total = []
	label = ['hero','popularity','winrate','kda','medals',\
		'elims','deaths','damage','block','heal','accuracy'\
		'obj time','obj kills','medals','cards']
	total.append(label)
	for i in range(len(overview[0])):
		temp = []
		for a in overview:
			if temp:
				temp.append(_convert(a[i]))
			else:
				temp.append(a[i])
		for b in combat[1:]:
			temp.append(_convert(b[i]))
		for c in misc[1:]:
			temp.append(_convert(c[i]))
		total.append(temp)

	return total
