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

1. Git 				: Code management
2. Sqlite			: DBMS
3. Python3 			: Mostly Backend, may be with CGI
4. HTML5, CSS3 and Javascript 	: Frontend
5. Inkscape 			: Drawing E-R Diagrams

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
	 Column names begin with small letter and separated by underscore in case of composite name

1. `UserProfile`(user_id(PK), username, first_name, last_name, date_of_birth, city(FK), state(FK), _favourites_(multivalued attribue))
2. `Credentials` (user_id(FK), username(FK), MD5hash of password)
3. `Songs`(song_id(PK), name, singer, film/album, genre, duration, price, popularity/rating, url, copies_sold)
4. `Playlist`(user_id, song_id)
5. `FavouriteGenres`(user_id(FK), genre)
6. `Quotes`(quote_id, quote, personality)
7. `ActiveUsers`(user_id(FK)) --> View using Union
8. `InactiveUsers`(user_id(FK)) --> View using difference

9. `Places`(city_name(PK),state_name(FK))
10. `States`(state_name(PK))
11. `SongTags`(song_id int(20)(FK), tag TEXT)

PS: Popularity is an integer value for the number of times played.

#Query types

##Group By
`Favourites`--> language or user_id
`Profile`	--> state

##Order By
`Songs`		--> name, singer, genre, language, duraition, popularity

##Union (Left, Full)
Active users are those who have either listened to a song within last week.

##Intersect

##Join
Join `UserProfile` with `FavouriteGenres` and get the details of person

##Difference
`InactiveUsers`  = All users - Active users
