# 서버부터 만들기

import json
from wsgiref.util import request_uri
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request
from flask_jwt_extended import *
import bcrypt, datetime
from flask_jwt_extended.config import config

from jwt.exceptions import (
    ExpiredSignatureError
)

# 부가기능
from init_db import Init_db
 
#APSCHEDULER 1
import time
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

app.config.update(
    DEBUG=True,
    JWT_SECRET_KEY="JUNGLERSSPORTS",
    JWT_TOKEN_LOCATION=["headers", "cookies"]
)

#APSCHEDULER 2
app.app_context().push()

client = MongoClient('localhost', 27017)
db = client.dbjungle

times = ["06:00","07:00","08:00"]
types = ["헬스", "러닝", "산책"]

#JWT 매니저 활성화
jwt = JWTManager(app)
jwt_blocklist = set()

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload) :
	jti = jwt_payload['jti']
	return jti in jwt_blocklist

### APSCHEDULER 3 ###

@app.route('/kill', methods=["POST"])
def show_reset():
    with app.app_context():
        time_L = list(db.user.find({"time" : {'$exists':True}}))
        if time_L:
            db.user.update_many({},{'$unset':{'time':True, 'type':True}})
            return jsonify({"result":"초기화 완료"})
        else:
            return jsonify({"result":"등록한 사람이 없습니다."})

#apscheduler 선언
sched = BackgroundScheduler(daemon=True, timezone="Asia/Seoul")

#apscheduler 실행설정, Cron 방식으로, 1~53주간 실행, 월~일 실행, 8시 59분 55초 실행, hour='8', minute='59', second ='55'
sched.add_job(show_reset, 'cron', week='1-53', day_of_week='0-6', hour='8', minute='59', second ='55')

#apscheduler 실행
sched.start()

### APSCHEDULER END ###

# HTML 화면 보여주기 
@app.route('/')
def home():
    homeDict = dict()
    for time in times:
        homeDict[time] = list()
        for type in types:
            players = []
            for player in list(db.user.find({"time":time,"type":type})):
                players.append(player['username'])
            homeDict[time].append({"type":type, "players":players})

    jwtToken = request.cookies.get('jwt-token')
    if jwtToken is None : return render_template('index.html', loginChecked = "true", homeDict = homeDict)

    try: 
        jti = decode_token(jwtToken)['jti']
        user = decode_token(jwtToken).get(config.identity_claim_key, None)
    except ExpiredSignatureError:
        return render_template('index.html', loginChecked = "true", homeDict = homeDict)
    
    loginChecked = jti in jwt_blocklist
    return render_template('index.html', homeDict = homeDict, loginChecked = loginChecked, username = user)

    


@app.route('/mypage')
def show_mypage():
    jwtToken = request.cookies.get('jwt-token')
    if jwtToken is None :
        return render_template('mypage.html', loginChecked = True)

    try:
        jti = decode_token(jwtToken)['jti']
        user = decode_token(jwtToken).get(config.identity_claim_key, None)
    except ExpiredSignatureError:
        return render_template('mypage.html', loginChecked = "true")
    
    loginChecked = jti in jwt_blocklist
    
    loginUser = db.user.find_one({"userid": user})
    registeredType = loginUser['type']
    registeredTime = loginUser['time']
    
    players = []
    for player in list(db.user.find({"time":registeredTime,"type":registeredType})):
        players.append(player['username'])
    result = {"type" : registeredType, "time" : registeredTime, "players" : players}
    print(result)
    
    return render_template('mypage.html', loginChecked = loginChecked, username = user, result = result)


@app.route('/login')
def show_login():
    return render_template('login.html')

@app.route('/signup', methods=['GET'])
def show_signup():
    return render_template('signup.html')

# API 역할을 하는 부분

# 운동하기 클릭했을 경우 DB 업데이트
    
#회원가입기능
@app.route('/signup', methods=["POST"])
def signup():
    inputData = request.form
    
    userId = inputData['userid']
    userPw = inputData['password']
    userName = inputData['username']

    #비밀번호암호화
    hashedPw = bcrypt.hashpw(userPw.encode('utf-8'), bcrypt.gensalt())

    #정글 a반 인원인지 and 이미가입된 회원은 아닌지 확인 후 등록
    junglerFound = db.junglers.find_one({"username" : userName}, {'_id': False})
    userFound = db.user.find_one({"username" : userName}, {'_id': False})

    if (junglerFound is None) :
        return jsonify({
                "result" : "fail",
                "msg": "정글 4기 A반만 가입하실 수 있습니다."
                })
    elif (userFound is not None) :
        return jsonify({
            "result" : "fail",
            "msg": "이미 가입된 회원입니다."
            })
    else :
        doc = {"userid" : userId, "password" : hashedPw, "username" : userName}
        db.user.insert_one(doc)
        return jsonify({"result" : "success"})
        


#로그인기능
@app.route('/login', methods=['POST'])
def user_login() :
    inputData = request.form
    userId = inputData['userid']
    userPw = inputData['password']
    user = db.user.find_one({'userid': userId}, {'_id': False})

    if user is not None :
        #ID/PW유효성확인 후 토큰 return
        if (userId == user['userid'] and
                bcrypt.checkpw(userPw.encode('utf-8'), user['password'])):
            return jsonify(
                {"result": "success",
                "token": create_access_token(identity=userId, expires_delta= datetime.timedelta(hours=1))
                }
            )
        else:
            return jsonify({
                "result": "fail", 
                "msg": "틀린 아이디이거나 비밀번호입니다. 다시 확인해주세요."
            }
            )
    else :
        return jsonify({
            "result": "fail",
            "msg": "가입되지 않은 회원입니다. 가입 후 이용해주세요."
        })

#로그아웃기능
@app.route('/logout', methods=['GET'])
@jwt_required()
def user_logout() :
    jti = get_jwt()['jti']
    jwt_blocklist.add(jti)
    return jsonify({"result": "success", "msg": "로그아웃 완료"}) #index로 redirect해줘야하나?

#운동등록기능
@app.route('/register', methods=['POST'])
@jwt_required()
def register() :
    user = get_jwt_identity()
    
    if user is None :
        return jsonify({"result": "forbidden", "msg": "로그인 해주세요!"})
    else :
        time_receive = request.form['time_give'] # 1. 클라이언트가 전달한 time_give 변수를 time_receive 변수에 넣음
        type_receive = request.form['type_give'] # 2. 클라이언트가 전달한 type_give 변수를 type_receive 변수에 넣음
        print("case1")
        db.user.update_one({'userid':user},{'$set':{"time":time_receive,"type":type_receive}})
        print("case2")
        # 2. 성공하면 success 메시지와 함께 counts 라는 운동 인원 수를 클라이언트에 전달합니다.
        return jsonify({'result': 'success', 'msg':'참가 완료!'})

if __name__ == '__main__':
    Init_db.insert_all()
    app.run('0.0.0.0', port=5000, debug=True)