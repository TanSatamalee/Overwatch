import requests
from bs4 import BeautifulSoup

url = 'https://playoverwatch.com/en-us/career/pc/us/'

my_ign = 'tannooby-11963'

page = requests.get(url + my_ign)

soup = BeautifulSoup(page.content, 'html.parser')

temp = soup.find_all(class_='card-heading')

for a in temp:
	print(a.get_text())
