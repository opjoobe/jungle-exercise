from pymongo import MongoClient
import bcrypt
import random
client = MongoClient('mongodb://test:test@52.79.117.11', 27017)
db = client.dbjungle

def setTest() :
    junglerList = ["계윤우", "송성곤", "이진호", "이재관", "이주형", "최제민", "김건엽", "김해인", "조현욱", "김영천", "이현주", "장혜원",
                "배동준", "이동희", "한승희", "강찬익", "김민우", "석혜린", "김민성", "김현진", "왕경업", "강세훈", "이기성", "박윤찬", "이승원"]

    db.junglers.drop()
    db.user.drop()
    db.user_rank.drop()

    for jungler in junglerList:
        doc = {"username": jungler}
        db.junglers.insert_one(doc)

    types = ["헬스","러닝","산책"]
    dates = [str(x) for x in range(20220320,20220330)]

    hashedPw = bcrypt.hashpw('1234'.encode('utf-8'), bcrypt.gensalt())

    

    for i in range(11):
        total_count = 0
        health_count = 0
        walking_count = 0
        running_count = 0
        log = {}
        for date in dates:
            type = types[random.randrange(3)]
            log[date] = type
            total_count +=1 
            if type == "헬스":
                health_count+=1
            elif type == "산책":
                walking_count+=1
            else:
                running_count+=1
        doc = {"userid":"jungle"+str(i), "password":hashedPw, "username":junglerList[i], "log":log}
        db.user.insert_one(doc)
        rank = {"userid":"jungle"+str(i), "username" : junglerList[i], "total_count" : total_count, "health_count" : health_count, "walking_count" : walking_count, "running_count" : running_count}
        db.user_rank.insert_one(rank)

if __name__ == "__main__" :
    setTest()

# hashedPw = bcrypt.hashpw('1234'.encode('utf-8'), bcrypt.gensalt())



##log 업데이트 코드 ###

# 여러개 업데이트 예시 - db.user.update_many({"time":{'$exists':True}},{'$set':{'log':{"헬스":1, "런닝":1}}})
# 여러개 특정필드 설정 예시 - db.user.update_many({},{'$set':{'log':dict()}})
# 여러개 특정필드 제거 예시 - db.user.update_many({},{'$unset':{'log':True}})
# 여러개 특정두필드 제거 예시 db.user.update_many({},{'$unset':{'time':True, 'type':True}})

# 특정필드 존재하는 db 찾기 예시 - players = list(db.user.find({"time" : {'$exists':True}}))

# 로그를 딕셔너리 형태로 만들어줌. {날짜:운동타입, 날짜:운동타입, ..}

## log에 날짜 상관 없이, 운동 종류에 따라 운동 횟수만 기록하는 경우

# players = list(db.user.find({"time" : {'$exists':True}}))

# for player in players:
#     user_name = player['username']
#     print("기존 player_log", player['log'])
#     player['log'][datetime.today().strftime("%Y%m%d%H%M%S")] = player['type']
#     db.user.update_one({'username':user_name}, {'$set':{'log':player['log']}})
#     print("새로운 player_log", player['log'])
#     h_datelist = []
#     s_datelist = []
#     for k, v in player['log'].items():
#         if v == '헬스':
#             h_datelist.append(k)
#         elif v == '산책':
#             s_datelist.append(k)
#     print("player {} 헬스 횟수: {}회 - [{}]".format(user_name, len(h_datelist), h_datelist))
#     print("player {} 산책 횟수: {}회 - [{}]".format(user_name, len(s_datelist), s_datelist))
#     print("player {} 총 운동 횟수: {}회 - [{}]".format(user_name, len(player['log']), list(player['log'].keys())))



###### db.user.update_many({},{'$unset':{'log':True}})

