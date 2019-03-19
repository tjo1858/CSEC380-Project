from flask import Flask, render_template, request, session, redirect, url_for
import pymysql
from werkzeug import generate_password_hash, check_password_hash
import datetime
import sys
import os

app = Flask(__name__, template_folder='templates')
secretKey = os.urandom(24)
app.secret_key = secretKey

@app.route("/")
def home():
    return render_template('login.html')

@app.route("/login", methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    hashedpass = generate_password_hash(password)
    conn = pymysql.connect('mysql', 'root', 'root', 'db')
    cursor = conn.cursor()
    cursor.execute("SELECT EncryptedPass FROM users WHERE Username='{}'".format(str(username)))
    userpass = cursor.fetchone()
    print(userpass, file=sys.stderr)
    print(password, file=sys.stderr)
    print(hashedpass, file=sys.stderr)
    
    if userpass == None:
        #cursor.execute("INSERT INTO users(Username, EncryptedPass, DateCreated) VALUES \
                #('{}', '{}', '{}')".format(username, hashedpass, datetime.datetime.now().strftime('%Y-%m-%d')))
        return('wrong username')
        cursor.close()
        conn.commit()
        conn.close()
        return render_template('login.html')
    elif check_password_hash(userpass[0], password):
        cursor.close()
        conn.close()
        session['username'] = username
        #return 'success!'
        return redirect(url_for('mainpage'))

    cursor.close()
    conn.commit()
    conn.close()
    return "wrong password!"

@app.route("/homepage", methods=['GET','POST'])
def mainpage():
    if 'username' in session:
        return render_template('homepage.html')
    else:
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0')