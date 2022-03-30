#APSCHEDULER 1
import time
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify
from utils.init_db import *
import datetime

app = Flask(__name__)

#APSCHEDULER 2
app.app_context().push()

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
sched.add_job(show_reset, 'cron', week='1-53', day_of_week='0-6', hour='8', minute='59', second ='55')


#apscheduler 실행
sched.start()

### APSCHEDULER END ###