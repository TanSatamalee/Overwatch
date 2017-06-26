import numpy as np
import globalstats as gs
import playerstats as ps
import datetime

locations = ['global']#,'us','eu','kr','cn']
modes = ['qp']#,'comp']

# Saves global hero stats for all locations and modes in files.
# File naming: location_mode_date.txt
def store_global_stats():
	now = datetime.datetime.now()
	date = str(now.month) + str(now.day) + str(now.year)
	global locations, modes
	for l in locations:
		for m in modes:
			data = gs.get_global_stats(l, m)
			f =  open(l + '_' +  m + '_' + date, 'wb')
			np.savetxt(f, data, fmt='%.5f')
			f.close()

store_global_stats()