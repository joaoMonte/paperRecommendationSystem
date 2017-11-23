from flask import *
import urllib3
import json
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/login')
def loginPage():
    return '''
            <p> Sistema de recomendação: </p>
            <p> Login: <input type="text" id="upper"> </p>
            <p> Senha: <input type="text" id="lower"> </p>
            <button type="button" onclick="foo('upper','lower')"> Entrar </button>
            <p> <a href="/cadastro">criar conta</a> </p>
            '''

@app.route('/cadastro')
def cadastroPage():
    return '''
            <p> Cadastro: </p>
            <p> Nome: <input type="text" id="upper"> </p>
            <p> Login: <input type="text" id="upper"> </p>
            <p> Senha: <input type="text" id="lower"> </p>
            <button type="button" onclick="foo('upper','lower')"> Cadastrar </button>
            '''



if __name__ == '__main__':
    app.run(debug=True)

