#Queries 

PRAGMA foreign_keys = 1; 

##Create tables

CREATE TABLE UserProfile(
    user_id int(20) PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT,
    date_of_birth date NOT NULL,
    city TEXT,
    state TEXT,
    FOREIGN KEY(city) REFERENCES Places(city_name),
    FOREIGN KEY(state) REFERENCES States(state_name) 
    );

CREATE TABLE Credentials(
	user_id int(20),
    username TEXT,
    md5_passwd TEXT NOT NULL UNIQUE,
    FOREIGN KEY(username) REFERENCES UserProfile(username),
	FOREIGN KEY(user_id) REFERENCES UserProfile(user_id)
    );
    
CREATE TABLE Songs(
    song_id int(20) PRIMARY KEY,
    name TEXT NOT NULL,
	singer TEXT NOT NULL,
    film TEXT,
    genre TEXT NOT NULL,
    language TEXT,
    duration float NOT NULL,
    price float,
    rating int(3),
    url TEXT NOT NULL UNIQUE,
    copies_sold int(10)
    );

CREATE TABLE FavouriteGenres(
	user_id int(20),
	genre TEXT NOT NULL,
	FOREIGN KEY(user_id) REFERENCES UserProfile(user_id)
	);

CREATE TABLE Quotes(
	quote_id int(20) PRIMARY KEY,
	quote_text TEXT NOT NULL,
	personality TEXT
	);

CREATE TABLE OrderInfo(
	order_id int(20) PRIMARY KEY,
	user_id int(20),
	song_id int(20),
	date_of_order DATETIME,
	FOREIGN KEY(user_id) REFERENCES UserProfile(user_id),
	FOREIGN KEY(song_id) REFERENCES Songs(song_id)
	);

#data is populated by DBA
CREATE TABLE Places(
    city_name  TEXT PRIMARY KEY,
	state_name TEXT NOT NULL,
	FOREIGN KEY(state_name) REFERENCES States(state_name) 
	);
	
CREATE TABLE States(
    state_name  TEXT  PRIMARY KEY
    );
