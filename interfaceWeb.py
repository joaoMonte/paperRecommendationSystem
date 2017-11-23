from flask import *
import urllib3
import json
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/login', methods=['GET'])
def loginPage():
    return render_template('login.html')

@app.route('/cadastro', methods = ['GET', 'POST'])
def cadastroPage():
    if request.method == 'GET':
        return render_template('cadastro.html')
    else:
        request.


if __name__ == '__main__':
    app.run(debug=True)

