from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
engine = create_engine('sqlite:///tutorial.db', echo=True) #this will be our SQL server
 
app = Flask(__name__)
 
@app.route('/')
def home():
  if not session.get('logged_in'):
		return render_template('login.html') #this page is ugly
	else:
		return "Hello Boss!  <a href="/logout">Logout</a>" #this should instead redirect to existing server
 
@app.route('/login', methods=['POST'])
def do_login():
 
	POST_USERNAME = str(request.form['username'])
	POST_PASSWORD = str(request.form['password'])
 
	Session = sessionmaker(bind=engine)
	s = Session()
	query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
	result = query.first()
	if result:
		session['logged_in'] = True
	else:
		flash('wrong password!')
	return home()
 
@app.route("/logout") # a logout page may not be necessary
def logout():
	session['logged_in'] = False
	return home()
 
if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(debug=True,host='0.0.0.0', port=8081)