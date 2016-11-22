Report : Nanna Radio
====================

### Abstract

### Introduction

### Related work and survey

### System Analysis

### System Design

### System Implementation

In the implementation stage the sculptor brings his ideas into existence. After the crucial stage of system analysis and design, the implementation phase gains a lot of importance.

Another challenge in this stage is gaining descent performance and efficiency. The code has to be developed in such a way that the system produces expected results in the shortest possible time.

The stages in implementation are as below:

Stage 1:	Connecting to the database

Python program is used to connect to the sqlite3 database.

Py Code:
	import sqlite3
	connection = sqlite3.connect("nanna_radio.db")
	cursor = connection.cursor()

The cursor object is used to execute any given query.

Stage 2:	User Authentication

Note: The relations are created in sqlite3 using the relational model given in system design.

With the help of HTML5 frontend , GET and POST requests are carried out to the flask server in python program.

Javascript Code to send a request.

<script type="text/javascript">
	/* Code to get the parameters from input fields */
	var params = {
		first: "Chaitanya"
		last: "Lakkundi"
		...
	}
	var xhr = new XMLHTTpRequest();
	xhr.open('POST','/login',true);
    xhr.send(JSON.stringify(params));
    /* Send as a JSON object */
</script>

Python Code to catch the request and verify login

@app.route("/login",methods=['GET','POST'])
def login():
	data = loads(request.data) #convert from JSON to dictionary
	if checkLogin(data['username'],data['password']):
		login_user(data['username'])

The login_user function creates session cookies to store the information about user login.

Stage 3:	Home Page

The homepage is displayed with a greeting. Mind enriching quotes are displayed. 

The Quotes relation maintains a count of the number of times a quote is displayed. This ensures that the quotes are recycled every time and the same quote is displayed after a very long interval.

Stage 4:	Profile page

The user can goto the profile page to change his preferences.
An option to change user's name is also provided so that any spelling mistakes can be rectified.
The user can choose FavouriteGenres so that preferred songs can be listed in the discover view.
Checkboxes are provided to choose Favourite Genres.

Code :

{% for fav in favourites %}

  <p>
  <input type="checkbox" id="{{ fav }}" checked="True" />
  <label for="{{ fav }}" style="font-size: 24px;
                                color: inherit;" >
                                {{ fav }}</label>
  </p>
{% endfor %}

Python Code to execute query:

for each_genre in allGenres:
            if each_genre in userGenres:
                cur.execute("insert or replace into FavouriteGenres values(?,?)",(user_id,each_genre))
                print "Insert ",each_genre
            else:
                cur.execute("delete from FavouriteGenres where user_id=? and genre=?",(user_id,each_genre))
                print "Delete ",each_genre
        conn.commit()

Stage 5:	Discover View

The discover page contains songs based on the users' favourite genres.
The users can provide their preference in profile page.

Jinja code is used to display the songs.

{% for song in songs_data %}
	<p> {{song[0]}} </p>
	<!-- code to display songs in required format -->
{% endfor %}

Stage 6:	Browse Page

Search feature is provied in the browse page. Two searching mode have been adopted in the backend.
1. Quick search 	2. Deep search

The quick search feature works as follows:
Search in playlists of other users having same fingerprint.
The word fingerprint denotes the users who have the similar features in profile as that of the current user. eg. Same Location, similar age etc.

step 1: select all user_id having same fingerprint.
step 2: select playlists of those whose user_id in step 1.
step 3: search for songs in that playlist by joining with songs.

Query used to implement quick search:

cur.execute("""select name,url,song_id from
           (select name,url,song_id from Songs where song_id in
           (select song_id from Playlists where user_id in
           (select user_id from UserProfile
              where city in
           (select city from UserProfile
              where user_id=?)))) where name like '%"""+phrase+"%'",(user_id,))        

Nested query is used here.

### Sample Test Cases

### Screen Shots

###References

