import time
from selenium import webdriver
import pandas as pd
import re

# Allows for specification of time length[t] (1w, 1m, 3m, 6m),
# console[con] (pc, psn, xbl), role[role] (all, off, def, tank, supp),
# and skill rate[sr] (all, bronze, silver, gold, plat, diamond, master, gm).
def get_global_stats(mode, t, con, role, sr):
    url = "https://www.overbuff.com/heroes"

    browser = webdriver.Chrome("C:/Games/chromedriver.exe")
    browser.get(url)
    time.sleep(1)
    
    # Adds the time to request URL.
    t_list = {'1w':0, '1m':1, '3m':2, '6m':3}
    con_list = {'pc':0, 'psn':1, 'xbl':2}
    mode_list = {'qp':0, 'comp':1}
    role_list = {'all':0, 'off':1, 'def':2, 'tank':3, 'supp':4}
    sr_list = {
        'all':0,
        'bronze':1,
        'silver':2,
        'gold':3,
        'plat':4,
        'diamond':5,
        'master':6,
        'gm':7,
    }

    # Make an array of given parameters to be used for scraping
    params = [t_list[t], con_list[con], mode_list[mode], role_list[role], sr_list[sr]]
    if None in params:
        print("Error in params")
        return None

    # Use selenium to click webpage for the correct stats
    param_buttons = browser.find_elements_by_class_name('filter-group')
    param_num = 0
    for pb in param_buttons:
        pb_group = pb.find_elements_by_class_name('filter-option')
        pb_group[params[param_num]].click()
        param_num += 1

    time.sleep(1)

    # Scrape page and produce a pandas array.
    param_tabs = browser.find_elements_by_class_name('filter-tabs')[0].find_elements_by_class_name('filter-option')
    stats_label = ['Hero', 'Role']
    stats_table = []
    for pt in param_tabs:
        n = 0
        pt.click()

        # Adds the stats label into array
        labels = browser.find_elements_by_class_name('sortable')
        for l in labels:
            stats_label.append(l.text)
        
        heros = browser.find_elements_by_tag_name('tbody')[0].find_elements_by_tag_name('tr')
        for h in heros:
            stat_box = h.find_elements_by_tag_name('td')
            hero_name = stat_box[1].find_element_by_tag_name('a').text
            hero_name = re.sub(r'[^a-zA-Z ]', '', hero_name)
            hero_role = stat_box[1].find_element_by_tag_name('small').text
            if len(stats_table) < (n + 1):
                temp = []
                temp.append(hero_name)
                temp.append(hero_role)
                stats_table.append(temp)
            for stats in stat_box[2:]:
                stats_table[n].append(stats.find_element_by_tag_name('span').text)
                
            n += 1
    
    # Exits the selenium webdriver
    browser.quit()

    # Converts to readable pandas dataframe
    del stats_label[2]
    del stats_label[6]
    del stats_label[11]
    del stats_label[12]
    del stats_label[14]
    for i in stats_table:
        del i[11]
    df = pd.DataFrame.from_records(stats_table, columns=stats_label)
    df['Period'] = t
    df['Mode'] = mode
    df['SR'] = sr
    df['Console'] = con
    
    return df

    

def store_global_stats():

    time = ['1w', '1m', '3m', '6m']
    mode = ['qp', 'comp']
    con = ['pc', 'psn', 'xbl']
    role = ['all', 'off', 'def', 'tank', 'supp']
    sr = ['all', 'bronze', 'silver', 'gold', 'plat', 'diamond', 'master', 'gm']

    for t in time[:2]:
        for s in sr:
            df = get_global_stats('comp', t, 'pc', 'all', s)
            writer = pd.ExcelWriter('Season6/' + t + '_' + s + '.xlsx', engine='openpyxl')
            df.to_excel(writer, sheet_name= 'Sheet1', index=False)
            writer.save()

store_global_stats()