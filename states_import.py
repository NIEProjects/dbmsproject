#!/usr/bin/env python3

import sqlite3

conn = sqlite3.connect("nanna_radio.db")

cur = conn.cursor()

states_file = open("states_list")

states_list = states_file.read().split('\n')

#Note that this program works only if there are two columns in States table
#After populating the data, the column has been deleed
for state in states_list:
    l=[]
    a=(state,'')
    l.append(a)
    print(l)
    cur.executemany("insert into States values(?,?)",l)

conn.commit()
