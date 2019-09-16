# Project 1

Web Programming with Python and JavaScript


# CS50W Project 1

## Web Programming with Python and JavaScript
### https://courses.edx.org/courses/course-v1:HarvardX+CS50W+Web/course/

## Use the app on Heroku

## Usage

* Register
* Search books by name, author or ISBN
* Get info about a book and submit your own review!

## :gear: Setup your own

```bash
# Clone repo
$ git clone https://github.com/me50/xhaatemx.git

$ cd cs50-project1

# Create a virtualenv (Optional but reccomended)
$ python3 -m venv myvirtualenv

# Activate the virtualenv
$ source myvirtualenv/bin/activate (Linux)

# Install all dependencies
$ pip install -r requirements.txt

# ENV Variables
$ export FLASK_APP = application.py # flask run
$ export DATABASE_URL = Heroku Postgres DB URI
$ export GOODREADS_KEY = Goodreads API Key. # More info: https://www.goodreads.com/api
```
