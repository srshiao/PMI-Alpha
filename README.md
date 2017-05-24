<<<<<<< HEAD
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
=======
# PMI-Intern-Sign-In

## Synopsis

Internship signin web app developed using Django for Paradyme Management's 2017 summer internship program. 


## Interns Quickstart

Sign in.

Create New Session.

Select "Clock in"

When complete with work for the day, select current active session and click "End Session"

Select "Clock out"

Sign out.

Repeat. 

Past history of hours worked and work sessions can be found by navigating to "Past Logs" located at the top right of the webpage. 

Password can be changed by navigating to /admin

## Admin Quickstart

Create Users (the interns) as staff NOT as superusers. 

NOTE: MAKE SURE TO CREATE AN INTERN ENTRY FOR EVERY USER WITH CORRESPONDING USERNAME! SPELLING COUNTS!



>>>>>>> 9f3c05aa2127b15ff4b578434370a586518944f7

