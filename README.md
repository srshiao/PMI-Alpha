<h1>Alpha Build of PMI Database. </h1>

Constructed during the spring term of 2017, from Januaray to May.

Database currently consists of a relational database running on MySQL, and Django to create the webapplication to interact with the database.

The GUI is not polished, but included core functions are:
User Authentication.
Priveldges,
Basic Search of entire database and all tables,
Search specific table,
Filter each table by any field in table,
Sort table by any field.




Install django-watson using pip: pip3 install django-watson.


Update your Database:

python3 manage.py migrate.

python3 manage.py installwatson.

python3 manage.py buildwatson

