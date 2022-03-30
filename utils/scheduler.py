#APSCHEDULER 1
import time
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify
from utils.init_db import *
import datetime

app = Flask(__name__)

app.app_context().push()

#apscheduler를 활용한 reset 기능. 새로운 운동 신청이 시작되는 아침 9시 직전에 운동 참여자(player)의 운동 내역을 log에 저장해준 후 reset 해줌. 
@app.route('/reset', methods=["POST"])
def show_reset():
    with app.app_context():
        players = list(db.user.find({"time" : {'$exists':True}}))
        if players:
            for player in players:
                user_name = player['username']
                player['log'][datetime.datetime.today().strftime("%Y%m%d")] = player['type'] # 운동날짜를 key로, 운동종류를 value로 log사전에 저장
                db.user.update_one({'username':user_name}, {'$set':{'log':player['log']}}) # 위를 반영해 log 사전을 update 해줌          
            
            # 이렇게 for문을 다 돌려서 log를 업데이트 해줬으면, time과 type 필드를 제거해줌. 초기화 완료!
            db.user.update_many({},{'$unset':{'time':True, 'type':True}})
            return jsonify({"result":"초기화 완료"})
        else:
            return jsonify({"result":"등록한 사람이 없습니다."})

#apscheduler 선언, 시간대는 Seoul
sched = BackgroundScheduler(daemon=True, timezone="Asia/Seoul")

#apscheduler 실행설정, Cron 방식으로, 1~53주간 실행, 월~일 실행, 8시 59분 55초 실행, hour='8', minute='59', second ='55'
sched.add_job(show_reset, 'cron', week='1-53', day_of_week='0-6', hour='8', minute='59', second ='55')

#apscheduler 실행
sched.start()



print("abc")