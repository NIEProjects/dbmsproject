#Queries 

PRAGMA foreign_keys = 1; 

##Create tables

CREATE TABLE UserProfile(
    user_id int(20) PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    user_dp blob,
    first_name TEXT NOT NULL,
    last_name TEXT,
    date_of_birth date NOT NULL,
    language TEXT,
    city TEXT,
    state TEXT,
    FOREIGN KEY(city) REFERENCES City(city_name),
    FOREIGN KEY(state) REFERENCES State(state_name) 
    );

[ city and state are foreign keys. We could have used a dropdown but then ]
[ integrity of database depends on frontend. (wrt security) ]

CREATE TABLE Credentials(
    username TEXT,
    md5_passwd TEXT NOT NULL UNIQUE,
    FOREIGN KEY(username) REFERENCES UserProfile(username)
    );
    
CREATE TABLE Songs(
    song_id int(20) PRIMARY KEY,
    name TEXT NOT NULL,
    composer TEXT,
    film TEXT,
    genre TEXT NOT NULL,
    language TEXT,
    duration float NOT NULL,
    price float,
    rating int(3),
    url TEXT NOT NULL UNIQUE,
    copies_sold int(10)
    );
    
CREATE VIEW Playlist AS
    SELECT 
