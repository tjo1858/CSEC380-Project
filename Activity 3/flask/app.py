from flask import Flask, render_template, request
import pymysql

app = Flask(__name__, template_folder='templates')
#mysql = MySQL()
#app.config['MYSQL_DATABASE_USER'] = 'admin'
#app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
#app.config['MYSQL_DATABASE_DB'] = 'db'
#app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
#mysql.init_app(app)

@app.route("/")
def home():
    return render_template('login.html')

@app.route("/login", methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    db=pymysql.connect(db='db', user='admin', password='root', host='127.0.0.1', cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    #cursor.callproc('adduser', (username, password))	
    #return '{}\n{}'.format(username, password)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
