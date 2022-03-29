from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbjungle

# 기존 mystar 콜렉션을 삭제하고, 출처 url들을 가져온 후, 크롤링하여 DB에 저장합니다.
def insert_all():
    db.service.drop()  # mystar 콜렉션을 모두 지워줍니다.
    # names = ['홍길동','김다미','이주형']
    # for name in names:
    #     db.service.insert_one({'name':name, 'time':'06:00', 'type':'러닝'})
    #     print('완료!',name)
    junglerList = ["계윤우", "송성곤", "이진호", "이재관", "이주형", "최제민", "김건엽", "김해인", "조현욱", "김영천", "이현주", "장혜원",
            "배동준", "이동희", "한승희", "강찬익", "김민우", "석혜린", "김민성", "김현진", "왕경업", "강세훈", "이기성", "박윤찬", "이승원"]
    for jungler in junglerList:
        doc = {"username": jungler}
        db.junglers.insert_one(doc)
### 실행하기
insert_all()