####Inspiration from geeksforgeeks.org

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'admin'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'project1'

mysql = MySQL(app)

###############################################
#Tables#

def doInsertAccount(username, password,email):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO accounts (username, password, email) VALUES (%s, %s, %s)',
                   [username, password, email])
    mysql.connection.commit()

def doUpdateAccount(username,password,email):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE accounts SET username = %s, password = %s WHERE email = %s ',
                   [username, password, email])
    mysql.connection.commit()

def doDeleteAccount(email):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM accounts WHERE email = %s", [email])
    mysql.connection.commit()

def doSelectAccountAll():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM accounts")
    columns = [col[0] for col in cursor.description]
    data = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return(data)

def doSelectAccountUsername(username):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE username = %s', [username])
    account = cursor.fetchone()
    return account

def doLogin(username,password):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE username = %s and password = %s', [username, password])
    account = cursor.fetchone()
    return account


##############
#Flask#

@app.route('/')
@app.route('/login', methods = ['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        account = doLogin(username,password)
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'You have successfully logged in!'
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect username/password'
    return render_template('login.html', msg = msg)
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        account = doSelectAccountUsername(username)
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username can only contain characters and numbers'
        elif not username or not password or not email:
            msg = 'Please fill out the form'
        else:
            doInsertAccount(username, password, email)
            msg = 'You have registered succesfully!'
    elif request.method == 'POST':
        msg = 'Please fill out the form'
    return render_template('register.html', msg = msg)

if __name__ == '__main__':
    app.run(debug=True)