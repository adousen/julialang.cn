This is a site like julialang.org, but it uses python and flask instead of ruby to generate the markdown pages.
This Project is in development.

##Installation

1. clone the repo
2. set up virtual environment: `virtualenv venv`. (if you donnot want use virtualenv, you can skip this step)
3. activate vitual environment: `source venv/bin/activate`. (if you donnot want use virtualenv, you can skip this step)
4. `pip install -r requirements.txt`

##Create database
1. open `config.py`, set `SQLALCHEMY_DATABASE_URI`, MySQL example:
```
SQLALCHEMY_DATABASE_URI = 'mysql://juliacn:somepass@localhost/juliacn?charset=utf8'
```

2. create a new database `juliacn`, MySQL example:
```
CREATE DATABASE IF NOT EXISTS juliacn DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
```

##Init database tables
1. `python manage.py db init`
2. `python manage.py db migrate`
3. `python manage.py db upgrade`

##Run
4. `python manage.py runserver`
5. visit `http://localhost:5000`
