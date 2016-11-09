import sqlite3
import hashlib
from time import time
from collections import OrderedDict
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

def getProfile(user_id):
    (conn,cur) = connectDB()
    cur.execute("select username,first_name,last_name,strftime('%d-%m-%Y',date_of_birth),city, \
                 state,strftime('%d-%m-%Y %H:%M:%S',last_logged_in) from UserProfile where user_id=?",(user_id,))
    res = cur.fetchall()[0]
    data = OrderedDict()
    #All the values are declared sequentially to store the order of values
    data['Email'] = res[0]
    data['First Name'] = res[1]
    data['Last Name'] = res[2]
    data['Date of Birth'] = res[3]
    data['City'] = res[4]
    data['State'] = res[5]
    data['Last Logged in Time'] = res[6]
    closeDB(conn)
    return data

def insertProfile(username, first, last, dob, city, state, passwd):
    (conn,cur) = connectDB()
    user_id = int(time())
    md5 = hashlib.md5()
    md5.update(passwd)
    hash_pass = md5.hexdigest()

    try:
        cur.execute("insert into UserProfile values (?,?,?,?,?,?,?,?)"
                    ,(user_id,username,first,last,dob,city,state,None))
        cur.execute("insert into Credentials values \
                    (?,?,?)",(user_id,username,hash_pass))
        conn.commit()
    except Exception as e:
        print e
        conn.rollback()
        return False
    finally:        
        closeDB(conn)
    return True

def updateProfile(user_id,first,last):
    (conn,cur) = connectDB()
    try:
        cur.execute("update UserProfile set first_name=? where user_id=?",(first,user_id))
        cur.execute("update UserProfile set last_name=? where user_id=?",(last,user_id))
        conn.commit()
    except Exception as e:
        print "Error in updateProfile query : ",e
        conn.rollback()
    finally:
        closeDB(conn)

def checkLogin(username,password):
    (conn,cur) = connectDB()
    md5 = hashlib.md5()
    md5.update(password)
    hash_pass = md5.hexdigest()
    cur.execute("select md5_passwd,user_id from Credentials\
     where username=?",(username,))
    res = cur.fetchall()
    cur.execute("select first_name from UserProfile where user_id=?",(res[0][1],))
    first = cur.fetchall()[0][0]
    #print "Generated: ",res[0][0],"Required",hash_pass
    closeDB(conn)
    try:
        if res[0][0] == hash_pass:
            #md5 match
            print "Password Matched"
            return (res[0][1],username,first)
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
        print "Error in createToken",e
        conn.rollback()
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