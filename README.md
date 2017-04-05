yo do this or your code wont run

To install django-watson, follow these steps:

Install django-watson using pip: pip install django-watson.
Add 'watson' to your INSTALLED_APPS setting.
Update your Database:
Django >=1.7: Run the command manage.py migrate.
Django <1.7: Run the command manage.py syncdb.
Run the command manage.py installwatson.
Existing website data: If you're integrating django-watson with an existing site, then you'll also want to run ./manage.py buildwatson to index your existing data.

