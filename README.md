# MovieBase
A website which makes use of the **OMDB API** to fetch movie details and provides users with content-based recommendations based on the movies that the user has liked.

A website which makes use of the **OMDB API** to fetch details and displays them on the page. Users can search for movies and read details about these movies. Users can also like movies. The website has a **MovieBoard** where one can view the most liked movies by all users. The website also comprises of a **Machine Learning Recommendation Engine** which provides the user with content-based recommendations based on the movies that the user has liked.  

## Getting Started
These instructions will get you a copy of the project up and running on your local machine. 
### Installing
#### Flask
How to setup Flask: https://www.youtube.com/watch?v=QjtW-wnXlUY
#### Postgres
How to install postgreSQL: https://www.youtube.com/watch?v=e1MwsT5FJRQ
#### Numpy
```pip install numpy```
#### Pandas
```pip install pandas```
#### sklearn
```pip install sklearn```


### DB Creation
To create database:
```
1)  After installing postgreSQl, open SQL Shell (psql).

2)  Enter your Server(localhost), Database(postgres), Port(5432), Username(postgres) and Password(which you gave earlier while installing).

3)  After this, run all the commands/queries given in the movie.sql file
```
Make changes: In database.ini file, change password = the one which you gave earlier while installing postgreSQL

As a head start, run the queries in the **head_start.sql** file on PSQL shell 

After doing all these, run **python app.py**
