from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbjungle

class Init_db:
    @staticmethod
    def insert_all():
        db.junglers.drop()
        junglerList = ["계윤우", "송성곤", "이진호", "이재관", "이주형", "최제민", "김건엽", "김해인", "조현욱", "김영천", "이현주", "장혜원",
                "배동준", "이동희", "한승희", "강찬익", "김민우", "석혜린", "김민성", "김현진", "왕경업", "강세훈", "이기성", "박윤찬", "이승원"]
        for jungler in junglerList:
            db.junglers.insert_one({'username':jungler})