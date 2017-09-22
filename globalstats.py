import playerstats as ps
import json
import urllib
import time
import sqlite3
import pandas as pd
import gzip
from io import BytesIO
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
    return pd.DataFrame(_get_leaderboard(url), columns=['name','region'])


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

    if total == []:
        return None
    return pd.concat(total)


# UNUSABLE UNTIL FIGURE OUT HOW TO DECODE STRING FROM GZIP FILE
# A more specific version of get_global_stats() taken from overbuff.com
# Allows for specification of time length[time] (1w, 1m, 3m, 6m),
# console[con] (pc, psn, xbl), role[role] (all, off, def, tank, supp),
# and skill rate[sr] (all, bronze, silver, gold, plat, diamond, master, gm).
def get_gloal_stats2(mode, time, con, role, sr):
    # Adds the time to request URL.
    if not (time == '1w' or time == '1m' or time == '3m' or time == '6m'):
        print('Time Error')
        return None
    url = 'https://www.overbuff.com/tank/heroes?v=2293d4f&time=' + time + '&platform='

    # Adds console to request URL.
    con_list = {'pc':'1', 'psn':'2', 'xbl':'3'}
    if con in con_list:
        url += con_list[con]
    else:
        print('Console Error')
        return None

    # Adds game mode to request URL
    url += '&game_mode='
    mode_list = {'qp':'1', 'comp':'2'}
    if mode in mode_list:
        url += mode_list[mode]
    else:
        print('Mode Error')
        return None

    # Adds hero role to request URL
    url += '&group_hero=true'
    role_list = {'all':'', 'off':'&role=1', 'def':'&role=2', 'tank':'&role3', 'supp':'&role4'}
    if role in role_list:
        url += role_list[role]
    else:
        print('Role Error')
        return None

    # Adds skill rating to request URL
    sr_list = {
        'all':'',
        'bronze':'1',
        'silver':'2',
        'gold':'3',
        'plat':'4',
        'diamond':'5',
        'master':'6',
        'gm':'7',
    }
    if sr in sr_list:
        url += '&skill_tier' + sr_list[sr]
    else:
        print('SR Error')
        return None

    # Request URL and reads string and decodes
    hdr = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0', 'Accept-Encoding': 'gzip'}
    req = urllib.request.Request(url, headers=hdr)
    response = urllib.request.urlopen(req)
    buf = BytesIO(response.read())
    gzipFile = gzip.GzipFile(fileobj=buf, mode='r')
    data = gzipFile.read().decode('utf-8')
    print(data)

#get_gloal_stats2('qp', '1w', 'pc', 'all', 'all')