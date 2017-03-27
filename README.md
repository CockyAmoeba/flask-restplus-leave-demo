Flask-RestPlus Leave Demo
=========================
RESTful API Server Example
--------------------------

This project showcases my my scratchpad for building a demo RESTful server
with python and flask-restplus

The goals set for this example:

* RESTful API server should be self-documented using OpenAPI (fka Swagger)
  specifications, so interactive documentation UI is in place;
* Authentication is handled with Basic Auth and rudimentary roles queries.
  This can later be swapped out for OAuth2
* Request Args validation
* Testing with pytest
* Usage of SQLite
* Code migrations and code first models
* Dockerization

### View API

Once running browse the API via the browser @

#### http:<ip-address>:8888/api/v1



Dependencies
------------

### Project Dependencies

* [**Python**](https://www.python.org/) 3.5+
* [**flask-restplus**](https://github.com/noirbizarre/flask-restplus) (+
  [*flask*](http://flask.pocoo.org/))
* [**sqlalchemy**](http://www.sqlalchemy.org/) (+
  [*flask-sqlalchemy*](http://flask-sqlalchemy.pocoo.org/)) - Database ORM.
* [**alembic**](https://alembic.rtdf.org/) (+ [*flask-migrate*](https://flask-migrate.readthedocs.io/en/latest/))- for DB migrations.
* [**Swagger-UI**](https://github.com/swagger-api/swagger-ui) - for interactive
  RESTful API documentation.

Installation
------------

### Initialize Database

We need to create a blank sqlite db

#### Set environment variables - Windows:

```bash
$ set FLASK_APP=run.py
$ set FLASK_CONFIG=development
```

#### Set environment variables - linux:

```bash
$ export FLASK_APP=run.py
$ export FLASK_CONFIG=development
```

#### Run db migrations to create db and tables definitions from models

```bash
$ python migrate.py db upgrade
```

after which we need to copy it to the app folder for the service to access it

#### Initialize db with test data - Not required

We need to run the web app server command shell and execute a script to create teh entities

```bash
$ flask shell
$ >>> from initial_data_setup import setup
$ >>> setup()
$ >>> exit()
```

### Using Docker

It is very easy to start exploring the example using Docker!

Create teh IMage:

```bash
$  docker build -t restplus-service .
```

Run the dockerized server:

```bash
$ docker run -it --rm --publish 8888:8888 restplus-service
```

TODO
_____
* Authentication and Authorization
* More Tests
* Custom web test client to invoke Auth and perform authenticated tests


