from bson.objectid import ObjectId
from bson.json_util import dumps
from pymongo import MongoClient
import json


client = MongoClient()
db = client["paper-recommendation"]
users = "users"
papers = "papers"


def createUser(login, password, name):
    user = db[users].find_one({'login':login})
    if user == None:
        user = {'login':login, 'password':password, 'name': name}
        userId = db[users].insert_one(user)
        return userId
    else:
        return "user already exists"


def getUser(login, password):
    user = db[users].find_one({'login':login, 'password':password})
    return user


def addPaper(title,link):
    paper = db[papers].find_one({'title': title})
    if paper == None:
        paper = {'title':title, 'link':link}
        paperId = db[papers].insert_one(paper)
        return paperId
    else:
        return "paper already exists"


def getPaper(title):
    paper = db[papers].find_one({'title': title})
    return paper


def addEvaluation(userLogin, paperTitle, score):
    collection = "evaluation"+userLogin
    evaluation = db[collection].find_one({'paper':paperTitle})
    new_evaluation = {'paper': paperTitle, 'score': score}
    if evaluation == None:
        evaluationId = db[collection].insert_one(new_evaluation)
    else:
        evaluationId = db[collection].find_one_and_replace({'paper':paperTitle},
                                                             new_evaluation,
                                                             {'returnNewDocument':True})
    return evaluationId


def getUserEvaluation(userLogin):
    evaluations = db["evaluation" + userLogin].find()
    return evaluations


def getAllEvaluations():
    pass
    userList = db[users].find()
    result = {}
    for user in userList:
        userEvaluations = getUserEvaluation(user["login"])
        userResult = {}
        for evaluation in userEvaluations:
            userResult[evaluation["paper"]] = evaluation['score']
        result[user["login"]] = userResult
    return result


if __name__ == "__main__":
    print("add user:", createUser("vmsf","123","vinicius"),"\n")
    print("add user:", createUser("guto", "123", "guto"), "\n")
    print("add user:", createUser("demis", "123", "demis"), "\n")
    print("login with right password:", getUser("vmsf","123"),"\n")
    print("login with WRONG password:", getUser("vmsf","13"),"\n")
    print("add a paper:", addPaper("paper1", "http://meuspapers.com/paper1"))
    print(getPaper('paper1'),"\n")
    print("add a paper:", addPaper("paper2", "http://meuspapers.com/paper2"))
    print(getPaper('paper2'),"\n")
    print("add a paper:", addPaper("paper3", "http://meuspapers.com/paper3"))
    print(getPaper('paper3'), "\n")
    print("evaluate paper:", addEvaluation('vmsf','paper1',0.5))
    print("evaluate paper:", addEvaluation('guto', 'paper1', 5.5))
    print("evaluate paper:", addEvaluation('guto', 'paper3', 4.5))
    print("evaluate paper:", addEvaluation('demis', 'paper2', 6.5))
    print("evaluate paper:", addEvaluation('demis', 'paper3', 2.53))
    print(dumps(getUserEvaluation('vmsf')),"\n")
    print("evaluate same paper:", addEvaluation('vmsf', 'paper1', 2.5))
    print(dumps(getUserEvaluation('vmsf')),"\n")
    print("evaluate paper:", addEvaluation('vmsf', 'paper2', 4.5))
    print(getUserEvaluation('vmsf'),"\n")
    print("get all evaluations:", getAllEvaluations())




