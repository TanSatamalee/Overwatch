import webscrape as ws
from bs4 import BeautifulSoup

# Returns a list of the top 500 players with their id.
def get_leaderboard():
	url = 'https://masteroverwatch.com/leaderboards/pc/global'
	page = ws.request_page(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	links = soup.find_all('a', {'class':'table-row-link'}, href=True)

	players = []
	for p in links:
		players.append(p['href'])

	print(len(players))
	return players

get_leaderboard()