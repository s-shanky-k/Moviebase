# MovieBase
A website which makes use of the OMDB API to fetch details and displays them on the page. Users can Like movies and can also view most Liked movies by all users

## Getting Started
These instructions will get you a copy of the project up and running on your local machine. 
### Installing
#### Flask
How to setup Flask: https://www.youtube.com/watch?v=QjtW-wnXlUY
#### Postgres
How to install postgreSQL: https://www.youtube.com/watch?v=e1MwsT5FJRQ
#### Numpy
pip install numpy
### Pandas
pip install pandas
### sklearn
pip install sklearn


### DB Creation
To create database:
```
1)  After installing postgreSQl, open SQL Shell (psql).

2)  Enter your Server(localhost), Database(postgres), Port(5432), Username(postgres) and Password(which you gave earlier while installing).

3)  After this, run all the commands/queries given in the movie.sql file
```

Make changes: In database.ini file, change password = the one which you gave earlier while installing postgreSQL

After doing all these, run python app.py
