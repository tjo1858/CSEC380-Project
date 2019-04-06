from flask import Flask, flash, jsonify, render_template, request, session, redirect, url_for
import pymysql
import requests
import shutil
import json
from werkzeug import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import datetime
import sys
import os
from flask_cors import CORS, cross_origin

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, static_url_path='/static', template_folder='templates')

# sql connect

conn = pymysql.connect('mysql', 'root', 'root', 'db')
cursor = conn.cursor()

# rate limit for password brute force

limiter = Limiter (
    app,
    key_func=get_remote_address,
    default_limits=["28000 per day", "1000 per hour", "20 per minute"]
)

# creating session key

secretKey = os.urandom(24)
app.secret_key = secretKey


# configure CORS

app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app)


@app.route("/")
def home():
    return render_template('login.html')


@app.route("/login", methods=['GET','POST'])
@limiter.limit("14400/day;600/hour;10/minute")
def login():

    if request.method == 'GET':
        return redirect('http://localhost:5000')
    testuser1 = 'admin'
    testuser1hashedpass = generate_password_hash('admin')
    username = request.form['username']
    password = request.form['password']
    hashedpass = generate_password_hash(password)
    cursor.execute("INSERT INTO users(Username, EncryptedPass, TotalVideoCount, \
                    DateCreated) VALUES ('{}', '{}', 0, '{}')".format(testuser1, \
                    testuser1hashedpass, datetime.datetime.now().strftime('%Y-%m-%d')))
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
            target = os.path.join(APP_ROOT, "static")

            link = request.form['linkupload']
            if link != '':
                localfile = link.split('/')[-1]
                r = requests.get(link, stream=True)
                with open(localfile, 'wb') as f:
                    #shutil.copyfileobj(r.raw, f)
                    if not localfile.endswith(".mp4"):
                        flash("Please upload a file with .mp4 extension.")
                        return render_template('homepage.html')
                    destination = "/".join([target, localfile])
                    print("Storing in database . . . " + destination, file=sys.stderr)
                    shutil.copyfileobj(r.raw, f)
                    #f.write(destination)
                    cursor.execute("SELECT UserID FROM users WHERE Username='{}'".format((session['username'])))
                    userid = cursor.fetchone()
                    print(userid, file=sys.stderr)
                    cursor.execute("INSERT INTO video(UserID, VideoTitle, DateUploaded) VALUES \
                        ('{}', '{}', '{}')".format(userid[0], localfile, \
                        datetime.datetime.now().strftime('%Y-%m-%d')))
                    cursor.execute("UPDATE users SET TotalVideoCount = TotalVideoCount + \
                        1 WHERE Username = '{}'".format(str(session['username'])))
                    conn.commit()
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
                cursor.execute("INSERT INTO video(UserID, VideoTitle, VideoURL, DateUploaded) VALUES \
                    ('{}', '{}', '{}', '{}')".format(userid[0], filename, \
                    str(destination), datetime.datetime.now().strftime('%Y-%m-%d')))
                cursor.execute("UPDATE users SET TotalVideoCount = TotalVideoCount + \
                    1 WHERE Username = '{}'".format(str(session['username'])))
                conn.commit()
        return render_template('homepage.html', username = session['username'])
    else:
        return redirect(url_for('login'))


@app.route('/getvideos', methods=['GET', 'POST'])
def getvideos():

    username = request.get_json()
    username = username['username']
    cursor.execute("SELECT UserID FROM users WHERE Username='{}'".format(username))
    userid = cursor.fetchone()
    cursor.execute("SELECT * FROM video WHERE UserID={}".format(userid[0]))
    rows = cursor.fetchall()
    row_headers=[x[0] for x in cursor.description]
    json_data=[]
    for result in rows:
        json_data.append(dict(zip(row_headers,result)))
    print(json_data, file=sys.stderr)
    return jsonify(json_data)


@app.route('/videos/<title>')
def videos(title):

    return app.send_static_file(title)


@app.route('/delete/<videoid>')
def delete(videoid):
    
    if 'username' in session:
        cursor.execute("DELETE FROM video WHERE VideoID={}".format(videoid))
        cursor.execute("SELECT UserID FROM users WHERE Username='{}'".format((session['username'])))
        userid = cursor.fetchone()
        cursor.execute("UPDATE users SET TotalVideoCount = TotalVideoCount - \
                    1 WHERE Username = '{}'".format(str(session['username'])))
        conn.commit()
        return redirect(url_for('homepage'))
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host='0.0.0.0')

