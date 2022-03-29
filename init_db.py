from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbjungle

# 기존 mystar 콜렉션을 삭제하고, 출처 url들을 가져온 후, 크롤링하여 DB에 저장합니다.
def insert_all():
    db.service.drop()  # mystar 콜렉션을 모두 지워줍니다.
    names = ['홍길동','김다미','이주형']
    for name in names:
        db.service.insert_one({'name':name, 'time':'06:00', 'type':'러닝'})
        print('완료!',name)

### 실행하기
insert_all()