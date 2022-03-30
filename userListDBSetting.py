from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbjungle

# junglerList = ["계윤우", "송성곤", "이진호", "이재관", "이주형", "최제민", "김건엽", "김해인", "조현욱", "김영천", "이현주", "장혜원",
#             "배동준", "이동희", "한승희", "강찬익", "김민우", "석혜린", "김민성", "김현진", "왕경업", "강세훈", "이기성", "박윤찬", "이승원"]

# for jungler in junglerList:
#     doc = {"username": jungler}
#     db.junglers.insert_one(doc)

# db.user.update_many({"time":{'$exists':True}},{'$set':{'log':{"헬스":1, "런닝":1}}})

a = db.user.find_one({"username":'이주형'})
b = a['log']

print(b['헬스'])
print(a)

# db.user.update_many({},{'$unset':{'time':True, 'type':True}})
# db.user.insert_one({"username":이주형},{})
