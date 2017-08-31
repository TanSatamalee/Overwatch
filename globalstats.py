import playerstats as ps
import json
import urllib
import time
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup

heros = {
    'roadhog':'1',
    'junkrat':'2',
    'lucio':'3',
    'soldier':'4',
    'zarya':'5',
    'mcree':'6',
    'tracer':'7',
    'reaper':'8',
    'widowmaker':'9',
    'winston':'10',
    'pharah':'11',
    'reinhardt':'12',
    'symmetra':'13',
    'torbjrn':'14',
    'bastion':'15',
    'hanzo':'16',
    'mercy':'17',
    'zenyatta':'18',
    #'':'19', NUMBER 19 DOENST EXIST ON MASTEROVERWATCH.COM
    'mei':'20',
    'genji':'21',
    'dva':'22',
    'ana':'23',
    'sombra':'24',
    'orisa':'25',
    'doomfist':'26'
}

# Returns the top 500 players for a certain region (certain hero if provided).
# Locations: global, us, eu, kr, cn
def get_top500(location, hero=None):
    if hero is None:
        url = 'https://masteroverwatch.com/leaderboards/pc/' + location
    else:
        n = _get_hero_dict()[hero.lower()]
        if n is None:
            print('Hero does not exist')
            return None
        url = 'https://masteroverwatch.com/leaderboards/pc/' + location + \
         '/hero/' + n + '/mode/ranked/category/averagescore'
    return _get_leaderboard(url)

# Returns a list of the leaderboard with their id according to the url.
def _get_leaderboard(url):
    # Getting the top 50 players
    page = ps._request_page(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    links = soup.find_all('a', {'class':'table-row-link'}, href=True)

    players = []
    for p in links:
        players.append((p['href'].split('/')[-1], p['href'].split('/')[-2]))

    # Getting the other 450 players by JSON.
    json_url = 'https://masteroverwatch.com/leaderboards/pc/global/mode/'
    json_url += 'ranked/category/skillrating/hero/overall/role/overall/data?offset='
    hdr = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}
    for i in range(1, 10):
        req = urllib.request.Request(json_url + str(i * 50), headers=hdr)
        response = urllib.request.urlopen(req)
        str_response = response.read().decode('utf-8')
        data = json.loads(str_response)
        for item in data.get('entries',[]):
            players.append((item.split('href')[1].split('\"')[1].split('/')[-1], item.split('href')[1].split('\"')[1].split('/')[-2]))

    return players

# Returns the hero dictionary for corresponding number on masteroverwatch.com
def _get_hero_dict():
    global heros
    return heros

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
        if t:
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
        if t:
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
        if t:
            obj_time.append(t[0].getText())
            obj_kill.append(t[1].getText())
            medals.append(t[2].getText())
            cards.append(t[3].getText())

    result = [hero_name, obj_time, obj_kill, medals, cards]

    return result


# Converts data string scraped from website to a float stat.
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
        'elims','deaths','damage','block','heal','accuracy',\
        'obj_time','obj_kills','cards']
    for i in range(min(len(overview[0]),len(overview[1]))):
        temp = []
        for a in overview:
            if temp:
                temp.append(_convert(a[i]))
            else:
                temp.append(a[i])
        for b in combat[1:]:
            temp.append(_convert(b[i]))
        for c in misc[1:]:
            if not c == misc[3]:
                temp.append(_convert(c[i]))
        total.append(pd.DataFrame([temp], columns=label))

    return total
print(get_global_stats('global', 'qp'))

# Reads one of the top500 player databases and extracts all heros stats in a dictionary.
def get_top500_heros(location, table, hero=None):
    if not (table == 'current_lb' or table == 'total_lb'):
        print('Table name non existant or not entered correctly.')
        return None
    db = 'top500/' + location + '_'
    if not hero is None:
        db += hero + '_'
    db += 'leaderboard.db'
    conn = sqlite3.connect(db)

    old_arr = pd.read_sql_query('SELECT * FROM ' + table, conn)
    stat_dict = dict()
    for i, row in old_arr.iterrows():
        p = row['player']
        s = ps.get_hero_stats(p, 'comp', row['region'])
        if s is None:
            continue
        stat_dict[ps._convert_string(p)] = s

    return stat_dict
#ans = get_top500_heros('global','current_lb','mercy')
#print(len(ans))