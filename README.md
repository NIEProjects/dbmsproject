#DBMS Project
##ನನ್ನ Radio
##Nanna Radio

#Topics Proposed.

An online music streaming platform with the following features : 

1. Music divided by genres, artists, albums etc.
2. Option to create your playlist
3. Option to search music based on various filters like genre,language etc.
4. Recently played songs

#Technologies Used

1. Git : Code management
2. Sqlite3 : DBMS
3. Python3 : Mostly Backend, may be with CGI
4. HTML5, CSS3 and Javascript : Frontend
5. Inkscape : Drawing E-R Diagrams

#Criteria For Project

A mini project with the following goals : 

1. Using multiple tables to store different kinds of data
2. Using different types of relations 
3. Using a variety of relational concepts like joins,indexes, intersect etc.
4. Maintaining efficient queries
5. Implementing advanced SQL concepts to better use and store the data

#Features (from developers point of view)

1. Login
2. Personal playlist
3. Recently played
4. Bookmarked/Favourites list
5. Listen or Buy songs
6. Developer and User mode

#Relations

STD: Relation names begin with capital letter
	 Column names begin with small letter and separated by underscore incase of composite name

1. `UserProfile`(user_id(PK), username, first_name, last_name, date_of_birth, language, city(FK), state(FK), _favourites_(multivalued attribue))
2. `Credentials` (username, MD5hash of password)
3. `Songs`(song_id(PK), name, composer/band, film/album, genre, language, duration, price, popularity/rating, url, copies_sold)
4. `Playlist`(user_id, song_id, song_name, duration) --> View
5. `Favourites`(user_id(FK), genre, language)
6. `Quotes`(quote, personality)
7. `OrderInfo`(order_id,user_id(FK),song_id(FK),date_of_order)
8. `ActiveUsers`(user_id(FK)) --> View using Union
9. `InactiveUsers`(user_id(FK)) --> View using difference
10. `Freebirds`(user_id(FK))  --> View using difference
11. `City`(city_name(PK))
12. `State`(state_name(PK))

PS: Popularity is an integer value for the number of times played.

#Query types

##Group By
`Favourites`--> language or user_id
`Profile`	--> state

##Order By
`Songs`		--> name, singer, genre, language, duraition, popularity

##Union (Left, Full)
Active users are those who have either listened to a song or bought a song.

##Intersect 
Users who have listened to a song as well as bought a song (need not be the same song)

##Join
Join `Profile` with `Favourites` and get the details of person 

##Difference
`InactiveUsers`  = All users - Active users
`Freebirds`      = Listen - Buy
