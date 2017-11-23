from flask import *
import urllib3
import json
from datetime import datetime, timedelta

app = Flask(__name__)

def stubCreateUser(name, login, password):
    pass

def stubAuthUser(login, password):
    pass

@app.route('/login', methods=['GET', 'POST'])
def loginPage():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        login = request.form['login']
        password = request.form['password']
        stubAuthUser(login, password)
        return login + ' ' + password

@app.route('/signup', methods = ['GET', 'POST'])
def signupPage():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        name = request.form['name']
        login = request.form['login']
        password = request.form['password']
        stubCreateUser(name, login, password)
        return render_template('sucessfullSignup.html')

if __name__ == '__main__':
    app.run(debug=True)

