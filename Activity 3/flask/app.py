from flask import Flask, render_template, request, session, redirect, url_for
import pymysql
from werkzeug import generate_password_hash, check_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import datetime
import sys
import os

app = Flask(__name__, template_folder='templates')
limiter = Limiter (
    app,
    key_func=get_remote_address,
    default_limits=["28000 per day", "1000 per hour", "20 per minute"]
)
secretKey = os.urandom(24)
app.secret_key = secretKey

@app.route("/")
def home():
    return render_template('login.html')

@app.route("/login", methods=['GET','POST'])
@limiter.limit("14400/day;600/hour;10/minute")
def login():
    if request.method == 'GET':
        return redirect("http://127.0.0.1:5000/")
    testuser1 = 'admin'
    testuser1hashedpass = generate_password_hash('admin')
    username = request.form['username']
    password = request.form['password']
    hashedpass = generate_password_hash(password)
    conn = pymysql.connect('mysql', 'root', 'root', 'db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users(Username, EncryptedPass, DateCreated) VALUES \
            ('{}', '{}', '{}')".format(testuser1, testuser1hashedpass, datetime.datetime.now().strftime('%Y-%m-%d')))
    cursor.execute("SELECT EncryptedPass FROM users WHERE Username='{}'".format(str(username)))
    userpass = cursor.fetchone()
    print(userpass, file=sys.stderr)
    print(password, file=sys.stderr)
    print(hashedpass, file=sys.stderr)
    
    if userpass == None:
        cursor.close()
        conn.commit()
        conn.close()
        return render_template('wronguser.html')
    elif check_password_hash(userpass[0], password):
        cursor.close()
        conn.close()
        session['username'] = username
        return redirect(url_for('mainpage'))
    cursor.close()
    conn.commit()
    conn.close()
    return redirect(url_for('wrongpass'))

@app.route("/wronguser", methods=['GET','POST'])
def wronguser():
    return render_template('wronguser.html')

@app.route("/wrongpass", methods=['GET','POST'])
def wrongpass():
    return render_template('wrongpass.html')

@app.route("/homepage", methods=['GET','POST'])
def mainpage():
    if 'username' in session:
        return render_template('homepage.html')
    else:
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
