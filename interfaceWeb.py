from flask import *
import urllib3
import json
from datetime import datetime, timedelta

app = Flask(__name__)

example = [('Formal methods', 3.217777777777778), ('Programming language theory', 3.1928571428571435), ('Concurrency', 3.145), ('Software engineering', 2.5421428571428573), ('Databases', 2.488)]
userId = '1234567'


def stubCreateUser(name, login, password):
    pass

def stubAuthUser(login, password):
    pass

def getRecomendation(user):
    pass

def getAllPapers():
    pass

def getPaperDataFromDb(paperId):
    pass

def stubEvaluatePaper(paperId, grade):
    pass

def madeHtmlRecomendation(user):
    papers = getRecomendation(user)
    allPapers = getAllPapers()
    allPapers = {'p1':'id', 'p2':'id', 'p3':'id', 'p4':'id', 'p5':'id', 'p6':'id', 'p7':'id', 'p8':'id', 'p9':'id', 'p10':'id'}
    papers = example
    fileHtml = open('templates/recommendation.html', 'w')
    html = '''<html><body>
        <p> Recommended papers for you: </p> '''

    for paper in papers:
        partial = '''<p> - <a href="/paper/1">''' + paper[0] + ''' (''' + str(paper[1]) + ''')</a> </p>'''
        html += partial

    partial = ""
    for paper in allPapers.keys():
        partial += '''<p> - <a href="/paper/''' + allPapers[paper] + '''">''' + paper + ''' </a> </p>'''
    html += '''<p> Select a paper to evalue: </p>'''
    html += partial
    html += '''</body></html>'''
    fileHtml.write(html)
    fileHtml.close()

def generatePaperPage(paperId):
    fileHtml = open('templates/paper.html', 'w')

    paperJson = getPaperDataFromDb(paperId)
    paperJson = {'name': 'Formal methods', 'authors': 'Cicrano, beltrano'}
    html = '''<html><body>
            <p> Paper </p> '''

    for field in paperJson.keys():
        partial = '''<p> - ''' + field + ''' : ''' + paperJson[field] + '''</p>'''
        html += partial

    form = '''<form method="POST">

    <br> Evaluate this paper <input type="text" name="score"></br>
    <input type="submit" value="Ok">
    </form>
    <p> <a href="/mainPage"> << Back </a></p>

    '''

    html += form
    html += '''</body></html>'''

    fileHtml.write(html)
    fileHtml.close()

@app.route('/mainPage', methods=['GET'])
def userMainPage():
    return render_template('recommendation.html')

@app.route('/paper/<paperId>', methods=['GET', 'POST'])
def paperPage(paperId):
    if request.method == 'GET':
        generatePaperPage(paperId)
        return render_template('paper.html')
    else:
        paperGrade = request.form['score']
        stubEvaluatePaper(paperId, paperGrade)
        return render_template('paperEvaluated.html')

@app.route('/login', methods=['GET', 'POST'])
def loginPage():
    global userId
    if request.method == 'GET':
        return render_template('login.html')
    else:
        login = request.form['login']
        password = request.form['password']
        userId = stubAuthUser(login, password)
        madeHtmlRecomendation(userId)
        return render_template('recommendation.html')

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

