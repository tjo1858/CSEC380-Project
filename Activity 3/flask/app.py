from flask import Flask, render_template, request
from flaskext.mysql import MySQL
import pymysql
from werkzeug import generate_password_hash, check_password_hash
from datetime import date

app = Flask(__name__, template_folder='templates')

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
    cursor.execute("SELECT EncryptedPass FROM users WHERE Username={}".format(username))
    userpass = cursor.fetchone()
    if userpass == 0:
        cursor.execute("INSERT INTO users(Username, EncryptedPass, DateCreated) VALUES \
                ({}, {}, {})".format(username, hashedpass, datetime.date()))
        cursor.close()
        conn.close()
        return render_template('login.html')
    if check_password_hash(hashedpass, userpass):
        cursor.close()
        conn.close()
        return 'success!'

    cursor.close()
    conn.close()
    return "unsuccessful!"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
