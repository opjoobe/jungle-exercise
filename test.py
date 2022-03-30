from utils.init_db import *

print(list(db.user.find({},{'_id':False, 'username': 1, 'log': 1})))