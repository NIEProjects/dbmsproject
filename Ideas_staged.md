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

#Criteria For Project

1. A mini project
2. Change defalt formats..
3. Use as many query types as possible (eg. case, union, intersect etc)

#Relations (subject to modification)

STD: Relation names begin with capital letter

1. Profile(user_id(PK), username, first_name, last_name, date_of_birth, language, city(FK), state(FK), _favourites_(TODO))
2. Credentials (username, MD5hash of password )
3. Songs(id, name, singer, film, genre, language, duration, popularity, url)
4. Playlist(song_id, song_name, duration) --> View
5. Favourites(user_id(FK), genre(FK), language)
6. Quotes(quote, personality)

#Query types

##Group By
`Favourites`--> language or user_id
`Profile`	--> state

##Order By
`Songs`		--> name, singer, genre, language, duraition, popularity

##Union (Left, Full)

##Join

##Intersect

#Features

1. Developer Mode and User mode
