Report : Nanna Radio
====================
### Cover Page including project title and NIE logo as given in template

### Acknowledgement

We would like to express our sincere gratitude to all those who helped us in completing the project successfully. We express our profound thanks to Dr.G.L.Shekar, Principal, NIE, Mysore for much moral support and encouragement.
We are grateful to Dr. H D Phaneendra, Prof and Head of the department of Computer Science and Engineering, NIE for support and encouragement in facilitating the progress of this work.

The satisfaction that accompanies the successful completion of any task would be incomplete without the mention of people whose ceaseless cooperation made it possible, whose constant guidance and encouragement crown all efforts with success.

We are grateful to our project guides, Shri. Ramesh Sir and Ms. Rani madam for the guidance, inspiration and constructive suggestions which were very helpful to us in the preparation of this project. 
We also thank our colleagues who have helped in successful completion of the project.

Finally we thank our families and friends for being a constant source of inspiration and advice.

Chaitanya S Lakkundi                         Mohd Sanad Zaki Rizvi
    4NI14CS027                                     4NI14CS048
(let this be in left right form)

### Abstract

The music industry of the 21st century is in disarray because of new demands from consumers. Gone are the days of cassettes and tape recorders , consumers now expect to access their favourite music on the fly. To solve this problem, Nanna Radio is developed.

Nanna Radio is a modern way of listening to music. It strives to provide an all inclusive platform to listen to your favourite songs and playlists, discover new songs based on smart recommendations. 

The users' requirements are analyzed to identify their needs. The user desires simplified aggregation of services such as storing favourite songs, listening to songs, discovering new songs etc. The requirements have been analyzed and divided into small modules for easy access.
	
Databases are designed with care to accommodate growth in future. User friendly forms have been designed for data entry.  The systems have been developed using procedural design. Number of validation checks are built in to ensure the integrity of the data.

### Introduction

The project titled Nanna Radio is an online music streaming platform. It is a web application for providing services such as music streaming, playlists, discover new songs, search songs and inspirational qoutes . The project is developed using HTML5, CSS3, JavaScript, Materalize CSS at the front end and Python , Python Flask , SQlite3 at the back end for server and database. AJAX is used for linking the front end and back end using REST API(GET,POST,PUT,DELETE) calls. 

Nanna Radio is a web application designed for all kinds of operating systems capable of running a web browser. This software is easy to use for all kinds of people with little or no knowledge of computer operations. It features a familiar and well thought-out, an attractive user interface, combined with strong searching, insertion and reporting capabilities. 

It also has strong security features.

The project has the following main modules : 

1) Insertion into and extraction from registered users using user friendly Sign Up and Log In screen.

2) The user's profile that contains user's general details along with his/her favourite genres and options to update them.

3) RADIO view where one can listen to his/her playlist and add/delete songs to the playlist.

4) DISCOVER view where the user can discover new songs based on smart recommendations.

5) BROWSE view where a user can search for his/her favourite songs.

6) A Home page that has daily inspirational qoutes generated at random every time.

### Related work and survey

There are many prominent music streaming platforms already available but many have various limitations. Some of them are : 

1. Spotify : Not available in India
2. Google Play Music : Requires to upload card details before access.
3. Itunes : Requires payment and limited to Apple devices.
4. Amazon Prime : $99/year.
5. Pandora : available only in USA, Australia and New Zealand.

The closest competition to our project is from Saavn.com and Gaana.com but their websites are filled with distracting advertisements that spoil the user experience. Infact Gaana.com has audio advertisements playing in between songs which can be an unpleasant experience to user. Unless the user goes for paid version , this issue persists.

### System Analysis
System requirements
Proposed system

### System Design

E-R diagram with some explanation

### System Implementation

In the implementation stage the sculptor brings his ideas into existence. After the crucial stage of system analysis and design, the implementation phase gains a lot of importance.

Another challenge in this stage is gaining descent performance and efficiency. The code has to be developed in such a way that the system produces expected results in the shortest possible time.

Ten stages [0-9] are illustrated below:

Stage 0:	Connecting to the database

Python program is used to connect to the sqlite3 database.

Py Code:
	import sqlite3
	connection = sqlite3.connect("nanna_radio.db")
	cursor = connection.cursor()

The cursor object is used to execute any given query.

Stage 1:	Registration

Registration is required to obtain the necessary details of the user.
The state and city details are used to provide the quick search feature as described later.

The input fields are enclosed within a <div> tag to separately handle user input.

Validity checks are made from point to point to ensure the legitimacy of the entered data.
An example validity check in javascript is shown below.

<script type="text/javascript">
if (!datepicker.validity.valid) {
            res.innerHTML = "Please Choose a Date";
            return;
        }
</script>

A POST request is made to insert the details into the database.
xhr.open('POST','/signupDB',true);

The queries used to insert data are:

cur.execute("insert into UserProfile values (?,?,?,?,?,?,?,?)"
            ,(user_id,username,first,last,dob,city,state,None))
cur.execute("insert into Credentials values \
            (?,?,?)",(user_id,username,hash_pass))

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

A trigger has been used to update the last_loggedin_time in the database.

CREATE TRIGGER updateLastLoggedIn
after insert on LoggedInUsers
for each row
begin
update UserProfile set last_logged_in=datetime("now","localtime")
where UserProfile.user_id=NEW.user_id;
end;

Stage 3:	Home Page

The homepage is displayed with a greeting. Mind enriching quotes are displayed. 

The `Quotes` relation maintains a count of the number of times a quote is displayed. This ensures that the quotes are recycled every time and the same quote is displayed after a very long interval.

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

The PLAY button is provided so that the user can listen to songs on the go.
The <audio> tag has been used to play songs. </audio>

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

The deep search feature is implemented by tokenizing the input and searching for tokens in all the tables including Song Name,Singer,Genre etc.
The LIKE operator is used generously.

The queries used are:

cur.execute("select name,url,songs.song_id from songs where name like '%"+token+"%' or singer like '%"+token+"%'")

cur.execute("select name,url,songs.song_id from songs join SongTags where songs.song_id=SongTags.song_id and tag like '%"+token+"%'")        

After the user searches for a song, an option has been provided to add the song to playlist. The user can populate his/her playlist for later use.

Stage 7:	Radio Page

The radio page is provided to view the saved playlist. The user can listen to songs here as well. Two buttons are provided specially.
1. Add songs to the playlist
2. Delete complete playlist

When the user clicks the first button he/she is directed to the Browse page.
The second button is used to flush the playlist when a new playlist needs to be created.

Stage 8:	Mobile optimization

The website is designed to work on mobile devices as well. The Materialize CSS is used to take care of the viewport (size of the screen)..

The <ul> tag has been used under the following tagline so that separate mobile view can be provided.

<a href="#" data-activates="mobile-demo" class="button-collapse"><i class="material-icons">menu</i></a>

The login and signup pages are opened in a new tab instead as an overlay in case of mobile devices.

Stage 9:	Logout

Finally, after the user is satisfied and sufficiently entertained, Logout option has been provided so that nobody else can use his/her identity.

The logout option, executes a query at the backend which deletes the secure token along with the user_id from the LoggedInUsers table.

Once the user has been logged out, further login can be done at a later time.

### Sample Test Cases

To be done in the form of a table.
Login, Search, Playlist test cases.

### Screen Shots

Screenshots of all views

###References

tutorialspoint.com
stackoverflow.com
w3schools.com
materializecss.com