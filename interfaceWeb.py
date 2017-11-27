from flask import *
import urllib3
import json
from datetime import datetime, timedelta
import storage

app = Flask(__name__)

example = [('Formal methods', 3.217777777777778), ('Programming language theory', 3.1928571428571435), ('Concurrency', 3.145), ('Software engineering', 2.5421428571428573), ('Databases', 2.488)]
userId = '1234567'


def getRecomendation(user):
    pass

def getAllPapers():
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
        <p> <a href="/uploadPaper"> Upload a paper! </a> </p>
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

    paperJson = storage.getPaper(paperId)
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

@app.route('/uploadPaper', methods=['GET', 'POST'])
def uploadPaper():
    global userId
    if request.method == 'GET':
        return render_template('uploadPaper.html')
    else:
        title = request.form['title']
        link = request.form['link']
        author = request.form['author']
        year = request.form['year']

        storage.addPaper(title, link, author, year)
        return render_template('sucessfullUpload.html')

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
        userId = storage.getUser(login, password)
        if userId:
            madeHtmlRecomendation(userId)
            return render_template('recommendation.html')
        else:
            return render_template('invalidLogin.html')


@app.route('/signup', methods = ['GET', 'POST'])
def signupPage():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        name = request.form['name']
        login = request.form['login']
        password = request.form['password']
        storage.createUser(login, password, name)
        return render_template('sucessfullSignup.html')

if __name__ == '__main__':
    app.run(debug=True)

