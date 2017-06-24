import webscrape as ws
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

	pagedowns = 100
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


# Returns the popularity and winrate of all heroes for a specified mode.
def get_hero_overview(mode):
	url = 'https://masteroverwatch.com/heroes/pc/us/mode/'
	if mode == 'qp':
		url = url + 'quick'
	elif mode == 'comp':
		url = url + 'ranked'
	else:
		return None

	page = ws.request_page(url)
	soup = BeautifulSoup(page.content, 'html.parser')

	table = soup.find_all('div', class_='tab-pane')
	heroes = table[0].find('div', class_='table-body').find_all(class_='table-row row')
	
	hero_name = []
	popularity = []
	winrate = []
	for h in heroes:
		hero_name.append(h.find('strong').getText())
		t = h.find_all(class_='bar-outer')
		popularity.append(t[0].getText())
		winrate.append(t[1].getText())

	result = [hero_name, popularity, winrate]

	return result

get_hero_overview('qp')
