#!/bin/python3

import csv
import sqlite3

places_file = open('places_list.csv')

conn = sqlite3.connect("nanna_radio.db")
cur = conn.cursor()

places_raw = csv.reader(places_file)

data = []
listOfPlaces = []

for row in places_raw:
    r = row[0].split('\t')
    if(r[0] not in listOfPlaces and r not in data):
        data.append(tuple(r))        
        listOfPlaces.append(r[0])
    else:
        print(r[0] + " is repeated")


for row in data:
    a=[]
    tmp = tuple(row)
    a.append(tmp)
    print(a)    
    
cur.executemany("insert into Places values(?,?)",a)
#cur.executemany("insert into Places values(?,?)",data)
    

"""for row in data:
    print(row)
"""
conn.commit()
#this commit is to insert into Places

