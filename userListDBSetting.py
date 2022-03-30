from pymongo import MongoClient
from datetime import datetime

client = MongoClient('localhost', 27017)
db = client.dbjungle

junglerList = ["계윤우", "송성곤", "이진호", "이재관", "이주형", "최제민", "김건엽", "김해인", "조현욱", "김영천", "이현주", "장혜원",
             "배동준", "이동희", "한승희", "강찬익", "김민우", "석혜린", "김민성", "김현진", "왕경업", "강세훈", "이기성", "박윤찬", "이승원"]

for jungler in junglerList:
    doc = {"username": jungler}
    db.junglers.insert_one(doc)

##log 업데이트 코드 ###

# 여러개 업데이트 예시 - db.user.update_many({"time":{'$exists':True}},{'$set':{'log':{"헬스":1, "런닝":1}}})
# 여러개 특정필드 설정 예시 - db.user.update_many({},{'$set':{'log':dict()}})
# 여러개 특정필드 제거 예시 - db.user.update_many({},{'$unset':{'log':True}})
# 여러개 특정두필드 제거 예시 db.user.update_many({},{'$unset':{'time':True, 'type':True}})

# 특정필드 존재하는 db 찾기 예시 - players = list(db.user.find({"time" : {'$exists':True}}))

# 로그를 딕셔너리 형태로 만들어줌. {날짜:운동타입, 날짜:운동타입, ..}


## log에 날짜 상관 없이, 운동 종류에 따라 운동 횟수만 기록하는 경우

players = list(db.user.find({"time" : {'$exists':True}}))

for player in players:
    user_name = player['username']
    print("기존 player_log", player['log'])
    player['log'][datetime.today().strftime("%Y%m%d%H%M%S")] = player['type']
    db.user.update_one({'username':user_name}, {'$set':{'log':player['log']}})
    print("새로운 player_log", player['log'])
    h_datelist = []
    s_datelist = []
    for k, v in player['log'].items():
        if v == '헬스':
            h_datelist.append(k)
        elif v == '산책':
            s_datelist.append(k)
    print("player {} 헬스 횟수: {}회 - [{}]".format(user_name, len(h_datelist), h_datelist))
    print("player {} 산책 횟수: {}회 - [{}]".format(user_name, len(s_datelist), s_datelist))
    print("player {} 총 운동 횟수: {}회 - [{}]".format(user_name, len(player['log']), list(player['log'].keys())))



###### db.user.update_many({},{'$unset':{'log':True}})
