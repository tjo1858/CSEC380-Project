from flask import Flask, flash, render_template, request, session, redirect, url_for
import pymysql
from werkzeug import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import datetime
import sys
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
os.makedirs("videos")
app = Flask(__name__, template_folder='templates')
conn = pymysql.connect('mysql', 'root', 'root', 'db')
cursor = conn.cursor()
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
    cursor.execute("INSERT INTO users(Username, EncryptedPass, TotalVideoCount, DateCreated) VALUES \
            ('{}', '{}', 0, '{}')".format(testuser1, testuser1hashedpass, datetime.datetime.now().strftime('%Y-%m-%d')))
    cursor.execute("SELECT EncryptedPass FROM users WHERE Username='{}'".format(str(username)))
    userpass = cursor.fetchone()
    
    if userpass == None:
        conn.commit()
        return render_template('wronguser.html')
    elif check_password_hash(userpass[0], password):
        session['username'] = username
        conn.commit()
        return redirect(url_for('homepage'))
    conn.commit()
    return redirect(url_for('wrongpass'))

@app.route("/wronguser", methods=['GET','POST'])
def wronguser():
    return render_template('wronguser.html')

@app.route("/wrongpass", methods=['GET','POST'])
def wrongpass():
    return render_template('wrongpass.html')

@app.route("/homepage", methods=['GET','POST'])
def homepage():
	if 'username' in session:
		if request.method == 'POST':
                    target = os.path.join(APP_ROOT, "videos")

                    link = request.form['linkupload']
                    #if link != '':
                    #    with request.get(link) as response:
                    #        response_text = response.read()
                    #        data = json.loads(response_text.decode())
                    #        title = data['title']
                    #        destination = "/".join([target, title])
                    #        response.write(destination)
                    #        cursor.execute("SELECT UserID FROM users WHERE Username='{}'".format((session['username'])))
                    #        userid = cursor.fetchone()
                    #        print(userid, file=sys.stderr)
                    #        cursor.execute("INSERT INTO video(UserID, VideoTitle, DateUploaded) VALUES \
                    #        ('{}', '{}', '{}')".format(userid[0], title, \
                    #        datetime.datetime.now().strftime('%Y-%m-%d')))
                    for f in request.files.getlist("file"):
                        filename = f.filename
                        if not filename.endswith(".mp4"):
                            flash("Please upload a file with .mp4 extension.")
                            return render_template('homepage.html')
                        destination = "/".join([target, filename])
                        print("Storing in database . . . " + destination, file=sys.stderr)
                        f.save(destination)
                        cursor.execute("SELECT UserID FROM users WHERE Username='{}'".format((session['username'])))
                        userid = cursor.fetchone()
                        print(userid, file=sys.stderr)
                        cursor.execute("INSERT INTO video(UserID, VideoTitle, DateUploaded) VALUES \
                        ('{}', '{}', '{}')".format(userid[0], filename, \
                        datetime.datetime.now().strftime('%Y-%m-%d')))
                        cursor.execute("UPDATE users SET TotalVideoCount = TotalVideoCount + \
                        1 WHERE Username = '{}'".format(str(session['username'])))
                        conn.commit()
		return render_template('homepage.html')
	else:
		return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
