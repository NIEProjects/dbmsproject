#Topics Proposed.

1. Personalised Feed generator
2. Daily Radio (Based on Favourites)

#Etymology

1. My Radio
2. Nanna Radio ( In Kannada )

#Technologies Used

1. Git
2. Sqlite3
3. Python3 (Mostly Backend, may be with CGI)
4. Html5 with Javascript (Frontend)
5. Inkscape (Drawing E-R Diagrams)

#Criteria For Project

1. A mini project
2. Change defalt formats..
3. Use as many query types as possible (eg. case, union, intersect etc)

#Features

1. Developer Mode and User mode
2. Listen or Buy songs
3. Get enriched with daily quotes.
4. Free registration
5. Register with minimum details and then update profile

#Relations

STD: Relation names begin with capital letter
	 Column names begin with small letter and separated by underscore incase of composite name

1. `Profile`(user_id(PK), username, first_name, last_name, date_of_birth, language, city(FK), state(FK), _favourites_(TODO))
2. `Credentials` (username, MD5hash of password)
3. `Songs`(id(PK), name, singer, film, genre, language, duration, price, popularity, url, copies_sold)
4. `Playlist`(song_id, song_name, duration) --> View
5. `Favourites`(user_id(FK), genre(FK), language)
6. `Quotes`(quote, personality)
7. `OrderInfo`(order_id,user_id(FK),song_id(FK),date_of_order)
8. `ActiveUsers`(user_id(FK)) --> View using Union
9. `InactiveUsers`(user_id(FK)) --> View using difference
10. `Freebirds`(user_id(FK))  --> View using difference

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
