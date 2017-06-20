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

	print(len(players))
	return players

get_leaderboard()