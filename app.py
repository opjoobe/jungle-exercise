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
        players = list(db.user.find({"time" : {'$exists':True}}))
        if players:
            for player in players:
                user_name = player['username']
                # 현재는 더 많은 데이터를 뽑아 테스트하기 위해 시-분-초까지 나오게 했고, 최종 버전에서는 "%Y%m%d"로 수정하여야 함.
                # 데이터 뽑히게 하려면, 하단의 line 89 sched.add_job의 시간대를 변경해가며 py를 다시 실행하면 될거 같습니다!
                # 5시로 설정해 실행한 다음, 5시가 지나면 5시 10분으로 설정해 재실행, 이후 5시 10분이 지나면.....  

                player['log'][datetime.datetime.today().strftime("%Y%m%d%H%M%S")] = player['type'] # 운동날짜를 key로, 운동종류를 value로 log사전에 저장
                db.user.update_one({'username':user_name}, {'$set':{'log':player['log']}}) # 위를 반영해 log 사전을 update 해줌

                # count 증가시키는 코드 추가 ##############################
                db.user_rank.update_one({'username':user_name}, {'$inc':{'total_count':1}})
                if player['type'] == '헬스':
                     db.user_rank.update_one({'username':user_name}, {'$inc':{'health_count':1}})
                elif player['type'] == '산책':
                    db.user_rank.update_one({'username':user_name}, {'$inc':{'walking_count':1}})            
                else:
                    db.user_rank.update_one({'username':user_name}, {'$inc':{'running_count':1}})
                ###########################################################


                # 파이썬 상에서 원하는 데이터 뽑는 예시입니다. jinja2 짤 때 참고하시라고 같이 첨부해드립니다!
                '''
                h_list = [] #헬스 리스트
                s_list = [] #산책 리스트
                r_list = [] #러닝 리스트
                # log를 보고, 헬스, 산책, 러닝을 한 각각의 날짜를 각 리스트로 추출
                for k, v in player['log'].items():
                    if v == '헬스':
                        h_list.append(k)
                    elif v == '산책':
                        s_list.append(k)
                    else:
                        r_list.append(k)
                print("player {} 헬스 횟수: {}회 - 운동한 날: {}".format(user_name, len(h_list), h_list))
                print("player {} 산책 횟수: {}회 - 운동한 날: {}".format(user_name, len(s_list), s_list))
                print("player {} 러닝 횟수: {}회 - 운동한 날: {}".format(user_name, len(r_list), r_list))
                print("player {} 총 운동 횟수: {}회 - 운동한 날: {}".format(user_name, len(player['log']), list(player['log'].keys())))
                '''
            # 이렇게 for문을 다 돌려서 log를 업데이트 해줬으면, time과 type 필드를 제거해줌. 초기화 완료!
            db.user.update_many({},{'$unset':{'time':True, 'type':True}})
            return jsonify({"result":"초기화 완료"})
        else:
            return jsonify({"result":"등록한 사람이 없습니다."})

#apscheduler 선언
sched = BackgroundScheduler(daemon=True, timezone="Asia/Seoul")



#apscheduler 실행설정, Cron 방식으로, 1~53주간 실행, 월~일 실행, 8시 59분 55초 실행, hour='8', minute='59', second ='55'
sched.add_job(show_reset, 'cron', week='1-53', day_of_week='0-6', hour='08', minute='59', second ='55')


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
# 전달해줄 count_data 생성 #########################
    count_data = list(db.user_rank.find({},{"_id":False, "username":1, "total_count" : 1, "health_count" : 1, "walking_count" : 1, "running_count" : 1}))
####################################################
    players = []
    for player in list(db.user.find({"time":registeredTime,"type":registeredType})):
        players.append(player['username'])
    result = {"type" : registeredType, "time" : registeredTime, "players" : players}
    print(result)

# count_data 추가로 전달 ############################
    return render_template('mypage.html', loginChecked = loginChecked, username = user, result = result, userlog=loginUser['log'], count_data = count_data)
####################################################

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

    ### db에 'log' 추가
    if (junglerFound is not None and userFound is None) :

        # db에 rank 추가 ##################################
        rank = {"userid" : userId, "username" : userName,  "total_count" : 0, "health_count" : 0, "walking_count" : 0, "running_count" : 0}
        db.user_rank.insert_one(rank)
        ###################################################
        doc = {"userid" : userId, "password" : hashedPw, "username" : userName, "log" : dict()}       
        db.user.insert_one(doc)

        return jsonify({"result" : "success"})
    else :
        return jsonify({"result" : "fail"})


#로그인기능
@app.route('/login', methods=['POST'])
def user_login() :
    inputData = request.form
    userId = inputData['userid']
    userPw = inputData['password']
    user = db.user.find_one({'userid': userId}, {'_id': False})

    access_token = create_access_token(identity=userId, expires_delta= datetime.timedelta(hours=1))
    print(access_token)
    #ID/PW유효성확인 후 토큰 return
    if (userId == user['userid'] and
            bcrypt.checkpw(userPw.encode('utf-8'), user['password'])):
        return jsonify(
            {"result": "success",
            "token": access_token
            }
        )
    else:
        return jsonify({
            "result": "fail", 
            "msg": "유효하지 않은 id, pw 입니다."
        }
        )

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
    print("register 작업 시작")
    user = get_jwt_identity()
    
    if user is None :
        return jsonify({"result": "forbidden", "msg": "로그인 해주세요!"})
    else :
        time_receive = request.form['time_give'] # 1. 클라이언트가 전달한 time_give 변수를 time_receive 변수에 넣음
        type_receive = request.form['type_give'] # 2. 클라이언트가 전달한 type_give 변수를 type_receive 변수에 넣음
        db.user.update_one({'userid':user},{'$set':{"time":time_receive,"type":type_receive}})
        # 2. 성공하면 success 메시지와 함께 counts 라는 운동 인원 수를 클라이언트에 전달합니다.
        return jsonify({'result': 'success', 'msg':'참가 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)