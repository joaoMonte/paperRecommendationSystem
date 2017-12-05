from flask import *
import urllib3
import json
from datetime import datetime, timedelta
import storage
from Recommender import Recommender

app = Flask(__name__)

example = [('Formal methods', 3.217777777777778), ('Programming language theory', 3.1928571428571435), ('Concurrency', 3.145), ('Software engineering', 2.5421428571428573), ('Databases', 2.488)]
userId = '1234567'
user_login='anyone'

def normalizeRecommendations(recommendations):
    for i in range(0,len(recommendations)):
        #print(recommendations[i])
        minimum=min(recommendations[i][1],5.0)
        recommendations[i]=(recommendations[i][0],minimum)
    return recommendations

def getRecomendation(all_ratings):
    global user_login
    r = Recommender(all_ratings,2)
    r.computeDeviations() # calc similarity matrix
    user_ratings = all_ratings[user_login]# aqui vai ser o vetor de avaliacoes que vem do BD
    result = r.slopeOneRecommendations(user_ratings)
    recommendations=normalizeRecommendations(result)
    #print(r.data)
    users_recom=r.computeNearestNeighbor(str(user_login))
    #print(user_login)
    #print(all_ratings)
    #print(result)
    print("Recommendations")
    print(recommendations)
    return recommendations,users_recom

def madeHtmlRecomendation():
    #papers = getRecomendation(user)
    global userId
    allPapers = storage.getAllpapers()
    #get results
    all_ratings=storage.getAllEvaluations()
    #print(userRatings)
    recom=getRecomendation(all_ratings)
    papers = recom
    #print(recom)
    fileHtml = open('templates/recommendation.html', 'w')
    html = '''<html><body>
        <p> <a href="/uploadPaper"> Upload a paper! </a> </p>
        <p> Recommended papers for you: </p> '''

    for paper in papers:
        partial = '''<p> - <a href="/paper/1">''' + paper[0] + ''' (''' + str(paper[1]) + ''')</a> </p>'''
        html += partial

    partial = ""
    for paper in allPapers:
        partial += '''<p> - <a href="/paper/''' + str(paper['_id']) + '''">''' + paper['title'] + ''' </a> </p>'''
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
        if field != '_id':
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

def addNameRecommendations(recommendations):
    recommendationsNames=[]
    #print(recommendations)
    allPapers=storage.getAllpapers()
    for paper in allPapers:
        for i in range (0, len(recommendations)):
            recommendationEntry={}
            #print(recommendations[i][0],paper['_id'])
            if str(recommendations[i][0])==str(paper['_id']):
                recommendationEntry['id']=recommendations[i][0]
                recommendationEntry['rating']=recommendations[i][1]
                recommendationEntry['title']=paper['title']

                recommendationsNames.append(recommendationEntry)
        if len(recommendationsNames)==len(recommendations):
            break
    return recommendationsNames


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
    global userId, user_login
    if user_login=="anyone":
        return redirect('/login')
    else:
        all_ratings=storage.getAllEvaluations()
        allPapers = storage.getAllpapers()
        recommendations,users_recom=getRecomendation(all_ratings)
        recommendationTitles=addNameRecommendations(recommendations)
        correlated_users=[]
        for user in users_recom:
            if user[1]>0:
                correlated_users.append(user)
        return render_template('recommendation.html',recom=recommendationTitles,papers=allPapers,users=correlated_users,login=user_login)

@app.route('/evaluations')
def getEVal():
    global userId
    output = []
    cursor = storage.getUserEvaluation(userId)
    for evaluation in cursor:
        output.append(evaluation)
    return str(output)

@app.route('/paper/<paperId>', methods=['GET', 'POST'])
def paperPage(paperId):
    global userId
    if request.method == 'GET':
        #generatePaperPage(paperId)
        paperJson = storage.getPaper(paperId)
        return render_template('paper.html',paper=paperJson)
    else:
        paperGrade = request.form['score']
        storage.addEvaluation(userId, paperId, paperGrade)

        return render_template('paperEvaluated.html')

@app.route('/login', methods=['GET', 'POST'])
def loginPage():
    global userId,user_login
    if request.method == 'GET':
        return render_template('login.html')
    else:
        login = request.form['login']
        password = request.form['password']
        userId = storage.getUser(login, password)
        if userId:
            user_login=login
            return redirect('/mainPage')
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

