import pandas as pd
import numpy as np
import time
import sys

sys.path.insert(0, '../..')
import utils

# Declare parameters
time = ['1w', '1m', '3m', '6m']
mode = ['qp', 'comp']
con = ['pc', 'psn', 'xbl']
role = ['all', 'off', 'def', 'tank', 'supp']
sr = ['all', 'bronze', 'silver', 'gold', 'plat', 'diamond', 'master', 'gm']

''' ==========================================================
# Import data from separate excel files and combine to one pandas dataframe.
df = None
for t in time[:2]:
	for s in sr:
		xl = pd.ExcelFile('data/' + t + '_' + s + '.xlsx')
		temp = xl.parse('Sheet1')
		if df is None:
			df = temp
		else:
			df = pd.concat([df, temp])

utils.write_db(df, 'data/master.db', 'master')
========================================================== '''

# Loads data from master file.
data = utils.read_db('data/master.db', 'master')

# Renaming Columns for convenience (and correcting previous label bug).
new_clm = ['index', 'hero', 'role', 'pickrate', 'winrate', 'tierate', 'onfire',
       'elims', 'objkills', 'objtime', 'damage', 'healing',
       'edratio', 'solokills', 'finalblows', 'medals', 'gold',
       'silver', 'bronze', 'cards', 'period', 'mode', 'sr', 'console']
data.columns = new_clm

# Changing data to numerics
data['pickrate'] = data['pickrate'].str[:-1].astype(np.float64)
data['winrate'] = data['winrate'].str[:-1].astype(np.float64)
data['tierate'] = data['tierate'].str[:-1].astype(np.float64)
data['onfire'] = data['onfire'].str[:-1].astype(np.float64)
data['objtime'] = data['objtime'].str[:2].astype(np.float64) * 60 + data['objtime'].str[-2:].astype(np.float64)
data['damage'] = data['damage'].str.extract('(\d+)', expand=False).astype(np.float64)
data['healing'] = data['healing'].str.extract('(\d+)', expand=False).astype(np.float64)
data['solokills'] = data['solokills'].str[:-1].astype(np.float64)
data['finalblows'] = data['finalblows'].str[:-1].astype(np.float64)
print(data.dtypes)

