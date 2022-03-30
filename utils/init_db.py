from pymongo import MongoClient

client = MongoClient('mongodb://test:test@52.79.117.11',27017)
db = client.dbjungle