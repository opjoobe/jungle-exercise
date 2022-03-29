# 서버부터 만들기

from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbjungle

app.config.update(
    DEBUG=True,
    JWT_SECRET_KEY="JUNGLERSSPORTS"
)


# HTML 화면 보여주기 
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result')
def show_result():
    return render_template('result.html')

@app.route('/login')
def show_login():
    return render_template('login.html')

@app.route('/signup')
def show_signup():
    return render_template('signup.html')

# API 역할을 하는 부분

@app.route('/api/list', methods=['GET'])
def show_member_counts():
    time_receive = request.form['time_give'] # 1. 클라이언트가 전달한 time_give 변수를 time_receive 변수에 넣음
    type_receive = request.form['type_give'] # 2. 클라이언트가 전달한 type_give 변수를 type_receive 변수에 넣음

    # 1. db에서 위의 조건을 바탕으로 DB 목록 전체를 검색해서, time과 type가 일치하는 인원 수를 가져옵니다.
    counts = len(list(db.service.find_one({"time":time_receive, "type":type_receive}, {"_id":False})))
    # 2. 성공하면 success 메시지와 함께 counts 라는 운동 인원 수를 클라이언트에 전달합니다.
    return jsonify({'result': 'success', 'counts': counts, 'msg':'운동인원 불러오기 완료!'})

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

@app.route('/signup', methods=['POST'])
def user_signup() :
    inputData = request.form
    userId = inputData['userid']
    userPw = inputData['password']
    userName = inputData['username']

    userFound = db.junglers.find_one(userName)
    if userFound is None :
        doc = {"userid" : userId, "password" : userPw, "username" : userName}
        db.junglers.insert_one(doc)
        return jsonify({"result" : "success", "data" : doc})
    else :
        return jsonify({"result" : "이미 가입된 회원입니다."})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)