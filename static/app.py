import os
import sqlite3

from flask import Flask, session, redirect, render_template, url_for, request, flash
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from helpers import login_required

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
@login_required
def index():
    return redirect('/search')

@app.route('/login', methods=['GET', 'POST'])
def login():
	session.clear()
	if request.method == 'POST':
		user = request.form.get('username')
		passwd = request.form.get('passwd')

		if not user:
			return render_template('error.html', message='Must provide username', hyperlink='login')
		elif not passwd:
			return render_template('error.html', message='Must provide Password field', hyperlink='login')

		USER = db.execute(
			'''
				SELECT *FROM info WHERE usr=:user;
			'''
			, {"user":user}).fetchall()

		if not USER or not check_password_hash(USER[0]["hash"], passwd):
			flash('INVALID username or password')
			return render_template('login.html')

		session["user_id"] = USER[0]["id"]
		return redirect(url_for('index'))

	else:
		return render_template('login.html')

@app.route('/search', methods=['POST', 'GET'])
@login_required
def search():
	if request.method == 'POST':

		if not request.form.get('search'):
			return render_template('error.html', message='Must provide a Keyword', hyperlink='search')

		return redirect(url_for('result', DATA=request.form.get('search')))

	else:
		return render_template('search.html')

@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():

	session.clear()
	if request.method == 'POST':
		usr = request.form.get('username')
		passwd = request.form.get('password')
		confirm = request.form.get('confirm')

		if not usr:
			return render_template('error.html', message='Must provide username field', hyperlink='register')
		elif not passwd or not confirm:
			return render_template('error.html', message='Must provide password fields', hyperlink='register')

		if not passwd == confirm:
			return render_template('error.html', message='Password Does not Match', hyperlink='register')

		hashed = generate_password_hash(passwd)

		user = db.execute(
			'''
				SELECT id FROM info WHERE usr = :usr;
			'''
			, {"usr":usr}).fetchone()

		if user:
			flash('Username is already taken')
			return render_template('register.html')
		else:
			new_user = db.execute(
				'''
					INSERT INTO info (usr, hash) VALUES (:usr, :hash);
				'''
				, {"usr":usr, "hash":hashed})
			flash('registerd Successfully')
			db.commit()
		return redirect(url_for('login'))

	else:
		return render_template('register.html')


@app.route('/result/<DATA>', methods=['GET'])
@login_required
def result(DATA):

	listed = []
	info = {"title", "auther", "isbn"}

	with sqlite3.connect('book.db') as localdb:
		cur = localdb.cursor()
		data = cur.execute(
			'''
				SELECT title, auther, isbn FROM info WHERE auther LIKE '%{}%' OR title LIKE '%{}%' OR isbn = '{}'
			'''
			.format(DATA, DATA, DATA))

		for book in data:
			info = {
				"title": book[0],
				"auther": book[1],
				"isbn": book[2]
			}
			listed.append(info)

	return render_template('result.html', INFO=map(dict, set(tuple(sorted(lists.items())) for lists in listed)))

@app.route('/book/<string:isbn>', methods=['GET'])
@login_required
def book(isbn):

	review = {"auther", "title", "isbn", "year"}
	lists = []
	with sqlite3.connect('book.db') as localdb:
		cur = localdb.cursor()
		DATA = cur.execute(
			'''
				SELECT auther, title, isbn, year FROM info WHERE isbn='{}'
			'''
			.format(isbn))

		for data in DATA:
			review = {
				"auther": data[0],
				 "title": data[1], 
				 "isbn": data[2], 
				 "year": data[3]	
			}
			lists.append(review)
	return render_template('book.html', INFO=map(dict, set(tuple(sorted(l.items())) for l in lists)))


if __name__ == '__main__':
	app.run()