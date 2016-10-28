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
    cur.execute("select md5_passwd,user_id from Credentials\
     where username=?",(username,))
    res = cur.fetchall()
    #print "Generated: ",res[0][0],"Required",hash_pass
    closeDB(conn)
    try:
        if res[0][0] == hash_pass:
            #md5 match
            print "Password Matched"
            return (res[0][1],username)
        else:
            return None
    except Exception as e:
        print # coding=utf-8
        return None

def createToken(user_id):
    print "createToken"
    (conn,cur) = connectDB()
    salt = unicode(int(time())) + "ssaalltt"
    md5 = hashlib.md5()
    md5.update(str(user_id) + salt)
    token = md5.hexdigest()
    try:
        cur.execute("INSERT INTO LoggedInUsers values(?,?)",(user_id,token))
        conn.commit()
    except Exception as e:
        print e
        closeDB(conn)
        return False

    closeDB(conn)
    return token

def getLoggedinUsers():
    (conn,cur) = connectDB()
    cur.execute("select user_id,token from LoggedInUsers")
    users = cur.fetchall()
    users = dict((x,y) for x,y in users)
    closeDB(conn)
    return users

def logoutUser(user_id,token):
    (conn,cur) = connectDB()
    cur.execute("delete from LoggedInUsers where user_id=? and token=?",(user_id,token))
    conn.commit()
    closeDB(conn)
    return True