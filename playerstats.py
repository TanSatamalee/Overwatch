import requests
import locale
from bs4 import BeautifulSoup

url = 'https://playoverwatch.com/en-us/career/pc/us/'

my_ign = 'tannooby-11963'


# Returns the page request from url.
def _request_page(site_url):
    return requests.get(site_url)


# Returns BeautifulSoup object given a player's name.
# Player: username-battlenetid
def _create_soup(player):
    page = _request_page(url + player)
    return BeautifulSoup(page.content, 'html.parser')


# Returns the overall player stats value for a specific mode.
# Player: username-battlenetid
# Mode: qp, comp
def get_overall_stats_value(player, mode):
    # Checks for valid player argument
    if player is None:
        print('Not a valid player name.')
        return None

    soup = _create_soup(player)
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
    soup = _create_soup(my_ign)
    featured_stats = soup.find_all(class_='card-copy')
    stats = []
    for fs in featured_stats:
        stats.append(fs.get_text())
    return stats[:int(len(stats) / 2)]


# Returns the overall player stats for a specific mode.
# Player: username-battlenetid
# Mode: qp, comp
def get_overall_stats(player, mode):
    all_label = get_overall_stats_label()
    all_stat = get_overall_stats_value(player, mode)
    return [all_label, all_stat]


# Returns the player stats for specific heros in an array form.
# Return format: array of dictionaries with keys being string name of stat
#    and value being string of the stat value.
def get_hero_stats(player, mode):
    soup = _create_soup(player)

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
    
    return stats_array


qp_hero = None
cp_hero = None
qp_over = None
cp_over = None

# Creates the dictionaries for the character stats.
def get_all_stats(player):
    global qp_hero, cp_hero, qp_over, cp_over
    qp_hero = get_hero_stats(player, 'qp')
    cp_hero = get_hero_stats(player, 'comp')
    qp_over = get_overall_stats(player, 'qp')
    cp_over = get_overall_stats(player, 'comp')
