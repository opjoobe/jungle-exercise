# 서버부터 만들기

from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request
import itertools
from flask_jwt_extended import *
import bcrypt, datetime

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbjungle

times = ["06:00","07:00","08:00"]
types = ["헬스", "러닝", "산책"]

# HTML 화면 보여주기 
@app.route('/')
def home():
    # for time, type in itertools.product(times, types):
    #     players = list(db.service.find({"time":time, "type":type}))
    #     homeList.append({"time":time, "type":type, "players":players})
    homeDict = dict()
    for time in times:
        homeDict[time] = list()
        for type in types:
            players = []
            for player in list(db.service.find({"time":time,"type":type})):
                players.append(player['name'])
            homeDict[time].append({"type":type, "players":players})
        print(homeDict)
    return render_template('index.html', homeDict = homeDict)

@app.route('/mypage')
def show_result():
    # results = list()
    # res = dict()
    # for time in times:
    #     res[time] = list()
    #     for type in types:
    #         players = list(db.service.find({"time":time,"type":type}))
    #         res[time].append({"type":type, "players":players})
    # print(res)
            
    # for time, type in itertools.product(times, types):
    #     players = list(db.service.find({"time":time, "type":type}))
    #     results.append({"time":time, "type":type, "players":players})
    # print(results, "왜안나와")
    return render_template('mypage.html')

@app.route('/login')
def show_login():
    return render_template('login.html')

@app.route('/signup')
def show_signup():
    return render_template('signup.html')

# API 역할을 하는 부분

@app.route('/register', methods=['POST'])
def register():
    time_receive = request.form['time_give'] # 1. 클라이언트가 전달한 time_give 변수를 time_receive 변수에 넣음
    type_receive = request.form['type_give'] # 2. 클라이언트가 전달한 type_give 변수를 type_receive 변수에 넣음
    # userid = 
    # 해당 로그인 사용자의 db를 업데이트 시켜줌. 
    # db.service.update_one({'userid':userid},{'$set':{"time":time_receive,"type":type_receive}})
    #db.service.insert_one({'name':'김소정', 'time':time_receive, 'type':type_receive})
    # 2. 성공하면 success 메시지와 함께 counts 라는 운동 인원 수를 클라이언트에 전달합니다.
    return jsonify({'result': 'success', 'msg':'참가 완료!'})

# 운동하기 클릭했을 경우 DB 업데이트
@app.route('/api/add', methods=['POST'])
def add():
    name_receive = request.form['name_give']# 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    new_time_receive = request.form['new_time_give']
    new_type_receive = request.form['new_type_give']
    target_user = db.service.find_one({"name":name_receive})# 2. service 목록에서 find_one으로 name이 name_receive와 일치하는 user를 찾습니다.
    db.service.update_one({"name":name_receive}, {'$set':{"type":new_type_receive}})
    db.service.update_one({"name":name_receive}, {'$set':{"time":new_time_receive}})

    return jsonify({'result': 'success', 'msg':'운동하기 신청되었습니다!'})


@app.route('/api/cancel', methods=['POST'])
def delete_count():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    name_receive = request.form['name_give']
    # 2. mystar 목록에서 delete_one으로 name이 name_receive와 일치하는 star를 제거합니다.
    db.mystar.delete_one({"name":name_receive})
    # 3. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success', 'msg': '삭제 완료! 안녕!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)