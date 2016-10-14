#!/usr/bin/env python3

import sqlite3

conn = sqlite3.connect("nanna_radio.db")

cur = conn.cursor()

states_file = open("states_list")

states_list = states_file.read().split('\n')
data = []

for state in states_list:
	prin
#list of tuples 
cur.execute("insert into States values(?)",)
conn.commit()
