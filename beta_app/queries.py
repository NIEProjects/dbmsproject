import sqlite3
import hashlib
from time import time

def connectDB():
    conn = sqlite3.connect("../nanna_radio.db")
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys=True;")
    return (conn,cur)

def closeDB(conn):    
    conn.close()

def getUsers():
    (conn,cur) = connectDB()
    cur.execute("select user_id,username from UserProfile")
    data = cur.fetchall()
    closeDB(conn)
    return dict((y,x) for x,y in data)

def insertProfile(username, first, last, dob, city, state, passwd):
    (conn,cur) = connectDB()
    user_id = int(time())
    md5 = hashlib.md5()
    md5.update(passwd)
    hash_pass = md5.hexdigest()

    try:
        cur.execute("insert into UserProfile values (?,?,?,?,?,?,?)"
                    ,(user_id,username,first,last,dob,city,state))
        cur.execute("insert into Credentials values \
                    (?,?,?)",(user_id,username,hash_pass))
    except Exception as e:
        print e
        conn.rollback()
        return False
    finally:
        conn.commit()
        closeDB(conn)
    return True

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
