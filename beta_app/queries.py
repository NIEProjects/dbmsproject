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
                 state from UserProfile where user_id=?",(user_id,))
    res = cur.fetchall()[0]
    data = OrderedDict()    
    #All the values are declared sequentially to store the order of values
    data['Email'] = res[0]
    data['First Name'] = res[1]
    data['Last Name'] = res[2]
    data['Date of Birth'] = res[3]
    data['City'] = res[4]
    data['State'] = res[5]
    # if user_id in getActiveUsers():
    #     data['Active Status'] = True
    # else:
    #     data['Active Status'] = False

    cur.execute("""select genre from FavouriteGenres as f JOIN UserProfile as u
                 where f.user_id = u.user_id""")

    tmp_fav = cur.fetchall()
    tmp_fav = [genre[0] for genre in tmp_fav]
    fav={}
    for each_genre in getGenres():
        if each_genre in tmp_fav:
            fav[each_genre] = True
        else:
            fav[each_genre] = False

    closeDB(conn)
    return (data,fav)

def getStates():
    (conn,cur) = connectDB()
    cur.execute("select state_name from States order by state_name")
    states = cur.fetchall()
    states = [ state[0] for state in states]
    closeDB(conn)
    return states
    
def getCities(state):
    (conn,cur) = connectDB()
    cur.execute("select city_name from Places where state_name=? order by city_name",(state,))
    cities = cur.fetchall()
    cities = [city[0] for city in cities]    
    closeDB(conn)
    return cities

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

def updateProfile(user_id,data):
    (conn,cur) = connectDB()
    first = data['first']
    last = data['last']
    city = data['city']
    state = data['state']
    genreCount = data['genreCount']

    try:
        cur.execute("update UserProfile set first_name=? where user_id=?",(first,user_id))
        cur.execute("update UserProfile set last_name=? where user_id=?",(last,user_id))        
        cur.execute("update UserProfile set city=? where user_id=?",(city,user_id))
        cur.execute("update UserProfile set state=? where user_id=?",(state,user_id))
        allGenres = getGenres()
        userGenres=[]
        for i in range(len(allGenres)):
            try:
                userGenres.append(data['genre'+str(i)])
            except Exception as e:
                print "Error in ",e
        print "userGenres = ",userGenres
        for each_genre in allGenres:
            if each_genre in userGenres:
                cur.execute("insert or replace into FavouriteGenres values(?,?)",(user_id,each_genre))
                print "Insert ",each_genre
            else:
                cur.execute("delete from FavouriteGenres where user_id=? and genre=?",(user_id,each_genre))
                print "Delete ",each_genre
        conn.commit()
    except Exception as e:
        print "Error in updateProfile query : ",e
        conn.rollback()
        raise e
    finally:
        closeDB(conn)

def updatePopularity(song_url):
    (conn,cur) = connectDB()
    try:
        cur.execute("update Songs set rating=rating+1 where url=?",(song_url,))
        conn.commit()
    except Exception as e:
        print "Error in updatePopularity: ",e
    closeDB(conn)

def checkLogin(username,password):
    print "Check Login"
    (conn,cur) = connectDB()
    md5 = hashlib.md5()
    md5.update(password)
    hash_pass = md5.hexdigest()
    try:
        cur.execute("select md5_passwd,user_id from Credentials\
     where username=?",(username,))
        res = cur.fetchall()
        cur.execute("select first_name from UserProfile where user_id=?",(res[0][1],))
        first = cur.fetchall()[0][0]
    except:
        print "Login Error"        
    finally:
        closeDB(conn)
        
    #print "Generated: ",res[0][0],"Required",hash_pass

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
        cur.execute("INSERT or REPLACE INTO LoggedInUsers values(?,?)",(user_id,token))
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

def getQuotes():
    (conn,cur) = connectDB()
    cur.execute("select quote_url from QUOTES order by count limit 4")
    quotes = cur.fetchall()
    quotes = [quote[0] for quote in quotes]
    try:
        for quote in quotes:
            cur.execute("update quotes set count=count+1 where quote_url=?",(quote,))
        conn.commit()
    except Exception as e:
        print "Error in getQuotes : ",e
    closeDB(conn)
    return quotes
    
# Queries related to songs
def getSongs(min,max,user_id):
    (conn,cur) = connectDB()
    cur.execute("select genre from FavouriteGenres where user_id=?",(user_id,))
    genres = cur.fetchall()
    genres = [genre[0] for genre in genres] 
    songslist = []    
    for genre in genres:   
        cur.execute("select name,url,img_url from Songs where genre=?",(genre,))
        songslist.extend(cur.fetchall())

    songsCount = len(songslist)
    # print songslist
    closeDB(conn)
    return (songslist[min:max],songsCount)

def getPlaylist(user_id):
    (conn,cur) = connectDB()
    cur.execute("select name,url,img_url from Songs where Songs.song_id in \
                 (select song_id from Playlists where user_id=?)",(user_id,))
    data = cur.fetchall()
    count = len(data)
    closeDB(conn)

    return (data,count)

def deletePlaylist(user_id):
    (conn,cur) = connectDB()
    cur.execute("delete from Playlists where user_id=?",(user_id,))
    conn.commit()
    closeDB(conn)

def search(name,user_id):
    (conn,cur) = connectDB()
    #this function will search tokens as a whole
    tokens = name.split(' ')
    results = []
    count = len(tokens)
    for i in range(0,count):
        phrase = ' '.join(tokens[0:count-i])
        print "phrase : ",phrase
        #search in playlists of others having same fingerprint
        #step 1: select all user_id having same fingerprint
        #step 2: select playlists of those whose user_id in step 1
        #step 3: search for songs in that playlist by joining with songs 

        cur.execute("""select name,url,song_id from
                    (select name,url,song_id from Songs where song_id in
                    (select song_id from Playlists where user_id in
                    (select user_id from UserProfile
                     where city in
                     (select city from UserProfile
                     where user_id=?)))) where name like '%"""+phrase+"%'",(user_id,))        
        data = cur.fetchall()
        if(data):
            print "Quick Search!"
            break
    if not data:
        print "Deep search"
        return deepSearch(name)
    else:
        final_results = {}
        for result in data:
            final_results[result[0]] = (result[1],result[2])
        return final_results

def deepSearch(name):
    (conn,cur) = connectDB()
    tokens = name.split(' ')
    results = []
    for token in tokens:
        if len(token)<3:
            continue
        cur.execute("select name,url,songs.song_id from songs where name like '%"+token+"%' or singer like '%"+token+"%'")            
        #uses index on table songs
        results.append(cur.fetchall())
        cur.execute("select name,url,songs.song_id from songs join SongTags where songs.song_id=SongTags.song_id and tag like '%"+token+"%'")        
        results.append(cur.fetchall())
    closeDB(conn)
    final_results={}
    for each_result in results:
        for val in each_result:
            final_results[val[0]] = (val[1],val[2])
    
    return final_results

def updatePlaylist(user_id,song_id,action):
    (conn,cur) = connectDB()
    if action == "add":
        cur.execute("insert or replace into Playlists values(?,?)",(user_id,song_id))
    elif action == "remove":
        cur.execute("delete from Playlists where user_id=? and song_id=?",(user_id,song_id))
    conn.commit()
    closeDB(conn)    

def getGenres():
    return ['Patriotic','Devotional','Bollywood Hits','Ghazal']

# Active users are defined as -> last_logged_in time within 1 week
def getActiveUsers():
    (conn,cur) = connectDB()
    cur.execute("select * from ActiveUsers")
    data = cur.fetchall()
    data = [val[0] for val in data]
    closeDB(conn)
    return data      
