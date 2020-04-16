from flask import Flask,jsonify,request,abort
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
import requests
import datetime
import random
from datetime import date
import pandas as pd
import numpy as np
import threading
import json
from sklearn.preprocessing import StandardScaler
from sklearn import svm
import warnings
import time 
warnings.filterwarnings('ignore')

check_var = 1
app = Flask(__name__)
CORS(app,support_credentials = True)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Origin','127.0.0.1')
  return response

@app.route("/check",methods=['GET'])
def trial_connection():
    trial_dict = dict()
    trial_dict["trial"] = "ok"
    global check_var
    check_var = check_var + 1
    #print(check_var)
    return jsonify(trial_dict),200

@app.route("/donate",methods=["POST"])
def donate_blood():
    user_id = request.json["user_id"]
    time = datetime.datetime.now()
    day = str(time.day)
    month = str(time.month)
    year = str(time.year)
    date = day + "/" + month + "/" + year
    info = request.json["info"]
    bg = request.json["blood_group"]
    #print("before",bg)
    bgg=bg
    rh=bg[-1]
    bg=bg[:-1]
    #print("rh",rh)
    if(rh=="+"):
        bg+="%2B"
    else:
        bg+="%2D"
    #print("after",bg)
    client = MongoClient()
    db = client["blood_bank_db"]
    donar = db.donate_table
    donar_data = list(donar.find())
    max_id = -1
    for i in donar_data:
        bi = i["blood_id"]
        b_id = int(bi.split("SAMPLE")[1])
        if(b_id > max_id):
            max_id = b_id
    blood_id = "SAMPLE" + str(max_id+1)
    data = {"blood_id":blood_id,"user_id":user_id,"blood_group":bgg,"date":date,"time":time,"info":info}
    donar.insert_one(data)
    link="http://127.0.0.1:5000/writeblood?bg="+bg+"&qt="+str(350)
    res=requests.get(link)
    seek=db.seek_table
    link="http://127.0.0.1:5000/readblood?bg="+bg
    res=requests.get(link)
    y=json.loads(res.text)
    av=int(y["avail"])
    seeks=list(seek.find({"blood_group":bgg,"status":"pending"}))
    for i in seeks:
        if(int(i["quantity"])<=av):
            link="http://127.0.0.1:5000/writeblood?bg="+bg+"&qt=%2D"+str(i["quantity"])
            res=requests.get(link)
            seek.update({"randid":i["randid"]},{"$set":{"status":"available"}})
    return jsonify({}),200

@app.route("/seek",methods=["POST"])
def seek_blood():
    #print(request.json)
    user_id = request.json["user_id"]
    quantity = int(request.json["quantity"])
    info = request.json["info"]
    blood_group = request.json["blood_group"]
    bg=blood_group[:-1]
    rh=blood_group[-1]
    if(rh=="+"):
        bg+="%2B"
    else:
        bg+="%2D"
    link="http://127.0.0.1:5000/readblood?bg="+bg
    ##print(link)
    res=requests.get(link)
    y=json.loads(res.text)
    av=int(y["avail"])
    # d={}
    # for i in range(len(res)):
    #     d["group"]=bg
    #     d["avail"]=res[i]["avail"]
    # #print(d)
    client = MongoClient()
    db = client["blood_bank_db"]
    seek = db.seek_table
    now = datetime.datetime.now()
    day = str(now.day)
    month = str(now.month)
    year = str(now.year)
    date = day + "/" + month + "/" + year
    randi=str(random.random())
    if(av>quantity):
        data = {"user_id":user_id,"quantity":quantity,"info":info,"blood_group":blood_group,"status":"available","date":date,"randid":randi}
        link="http://127.0.0.1:5000/writeblood?bg="+bg+"&qt=%2D"+str(quantity)
        res=requests.get(link)
    else:
        data = {"user_id":user_id,"quantity":quantity,"info":info,"blood_group":blood_group,"status":"pending","date":date,"randid":randi}
    seek.insert_one(data)
    #print("done")
    client.close()
    return jsonify({}),200

@app.route("/register",methods=["POST"])
def register_user():
    sex = request.json["sex"]
    user_name = request.json["user_name"]
    DOB = request.json["DOB"]
    address = request.json["address"]
    email = request.json["email"]
    blood_group = request.json["blood_group"]
    password = request.json["password"]
    client = MongoClient()
    db = client["blood_bank_db"]
    user_info = db.person_details_table
    res = list(user_info.find())
    for i in res:
        if(i["email"] == email):
            client.close()
            return jsonify({}),401
    max_id = -1
    for i in res:
        user_id = int(i["user_id"].split("BLOOD")[1])
        if(user_id > max_id):
            max_id = user_id
    max_id = max_id + 1
    user_id = "BLOOD" + str(max_id)
    data = {"user_id":user_id,"name":user_name,"sex":sex,"DOB":DOB,"address":address,"email":email,"blood_group":blood_group,"password":password}
    user_info.insert_one(data)
    client.close()
    return jsonify({}),200

@app.route("/login",methods=["POST"])
def user_login():
    email = request.json["email"]
    password = request.json["password"]
    client = MongoClient()
    db = client["blood_bank_db"]
    user_info = db.person_details_table
    res = list(user_info.find({"email":email}))
    if(len(res) == 0):
        client.close()
        return jsonify({}),400
    if(res[0]["password"] != password):
        client.close()
        return jsonify({}),400
    user_id = res[0]["user_id"]
    return jsonify({"user_id":user_id}),200

@app.route("/get_status",methods=["POST"])
def get_status():
    client = MongoClient()
    db = client["blood_bank_db"]
    seek = db.seek_table
    #print("request json",request.json)
    user_id = request.json["user_id"]
    res = list(seek.find({"user_id":user_id}))
    d = dict()
    if(len(res) != 0):
        d["status"] = res[0]["status"]
        d["blood_group"] = res[0]["blood_group"]
        d["info"] = res[0]["info"]
        d["quantity"] = res[0]["quantity"]
    else:
        d["status"] = "NA"
        d["blood_group"] = "NA"
        d["info"] = "NA"
        d["quantity"] = "NA"
    client.close()
    return jsonify(d),200

@app.route("/predict",methods=["POST"])
def predict_donor():
    #code to input
    msld = int(request.json["msld"])
    td = int(request.json["td"])
    tv = int(request.json["tv"])
    msfd = int(request.json["msfd"])
    df = pd.read_csv('train.csv', index_col=False)
    df.columns = ['id','months_since_last_donation','num_donations','vol_donations','months_since_first_donation', 'class']
    df = df.drop(['id'], axis=1)

    #Enter test values in the below line here
    test = pd.DataFrame(columns=['months_since_last_donation','num_donations','vol_donations','months_since_first_donation'], data=[[msld,td,tv,msfd]])

    df["class"] = df["class"].astype(int)

    Y_train = df["class"]

    X_train = df.drop(labels = ["class"],axis = 1)

    sc = StandardScaler()
    X_train_scaled = sc.fit_transform(X_train)
    test_scaled = sc.transform(test)

    clf = svm.SVC(kernel='linear', C = 1.0, probability=True)
    clf.fit(X_train_scaled,Y_train)

    predictions = clf.predict_proba(test_scaled)
    predictions = predictions[:,1]
    d = dict()
    if(predictions[0]>0.24):
        output = "Yes, Will donate"
    else:
        output = "No, Will not donate"
    d["output"] = output
    return jsonify(d),200

# @app.route("/testit",methods=["POST"])
# def testit():
#     user_id = request.json["user_id"]
#     client = MongoClient()
#     db = client["blood_bank_db"]
#     seek = db.seek_table
#     res = list(seek.find())
#     client.close()
#     return jsonify(res),200
@app.route("/testit",methods=["POST"])
def testit():
    client = MongoClient()
    db = client["blood_bank_db"]
    seek = db.seek_table
    #print("request json",request.json)
    user_id = request.json["user_id"]
    res = list(seek.find({"user_id":user_id}))
    ##print(res)
    
    li=[]
    for i in range(len(res)):
        #print("i",res[i])
        d = {}

        d["status"] = res[i]["status"]
        d["blood_group"] = res[i]["blood_group"]
        d["info"] = res[i]["info"]
        d["quantity"] = res[i]["quantity"]
        d["randid"] =res[i]["randid"]
        li.append(d)
    #print("li",li)
    client.close()
    return jsonify(li),200

@app.route("/readblood",methods=["GET"])
def readblood():
    client=MongoClient()
    bg = request.args.get('bg')
    #print(bg)
    db = client["blood_bank_db"]
    res=list(db.blood_data.find({"group":bg}))
    d={}
    for i in range(len(res)):
        d["group"]=bg
        d["avail"]=res[i]["avail"]
    client.close()
    #print("read:",d)
    return jsonify(d)

@app.route("/writeblood",methods=["GET"])
def writeblood():
    #print("came here")
    client=MongoClient()
    bg = request.args.get('bg')
    qt = int(request.args.get('qt'))
    #print(bg)
    #print(qt)
    db = client["blood_bank_db"]
    res=list(db.blood_data.find({"group":bg}))
    d={}
    for i in range(len(res)):
        d["group"]=bg
        d["avail"]=res[i]["avail"]
    il=int(d["avail"])
    #print(il)
    il+=qt
    db.blood_data.update({"group":bg},{"$set":{"avail":il}})
    client.close()
    return jsonify({}),200
if __name__ == '__main__':
    app.run("0.0.0.0",port=5000,debug=True)
