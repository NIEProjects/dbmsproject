import sqlite3
import hashlib
from time import time

def connectDB():
    conn = sqlite3.connect("../nanna_radio.db")
    cur = conn.cursor()
    return (conn,cur)

def closeDB(conn):
    conn.commit()
    conn.close()

def insertProfile(username, first, last, dob, city, state, passwd):
    user_id = int(time())
    md5 = hashlib.md5()
    md5.update(passd)
    hash_pass = md5.hexdigest()
    cur.execute("insert into UserProfile \
                (user_id,username,first_name,last_name,date_of_birth,city,state) \
                values (?,?,?,?,?,?,?)" \
                ,(user_id,username,first,last,dob,city,state))
    cur.execute("insert into Credentials values \
                (?,?,?)",(user_id,username,hash_pass))

def checkLogin(username,password):
    (conn,cur) = connectDB()
    md5 = hashlib.md5()
    md5.update(password)
    hash_pass = md5.hexdigest()
    cur.execute("select md5_passwd from Credentials\
     where username=?",(username,))
    res = cur.fetchall()
    #print "Generated: ",res[0][0],"Required",hash_pass
    closeDB(conn)
    try:
        if res[0][0] == hash_pass:
            #md5 match
            print "Password Matched"
            return True
        else:
            return False
    except Exception as e:
        print # coding=utf-8
        return False
