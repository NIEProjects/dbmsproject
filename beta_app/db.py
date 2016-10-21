import sqlite3

conn = sqlite3.connect('test.db')

print "connected to database securely"

conn.close()