#!/usr/bin/python

import sqlite3

conn = sqlite3.connect('test.db')

print('Opened database successfully')

conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (1, 'Paul', 32, 'California', 20000.00 )")

conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (2, 'Allen', 25, 'Texas', 15000.00 )")

conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )")

conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )")

conn.commit()
print("Records created successfully")
conn.close()

'''
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
'''