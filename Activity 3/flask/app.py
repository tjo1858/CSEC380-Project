from flask import Flask, render_template, request
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/")
def home():
	return render_template('login.html')

@app.route("/login", methods=['POST'])
def login():
	username = request.form['username']
	password = request.form['password']
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.callproc('adduser', (username, password))	
	return '{}\n{}'.format(username, password)

if __name__ == "__main__":
        app.run(app, host='0.0.0.0', port=5000)
