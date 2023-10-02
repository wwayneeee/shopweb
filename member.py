# 初始化連線資料庫
import pymongo
client = pymongo.MongoClient("mongodb+srv://wayne:wayne123@mycluster.p6yq4gq.mongodb.net/?retryWrites=true&w=majority")
db = client.member_system
print("資料庫連線成功")

# from app import get_db
# db = get_db()

collection=db.users

class membersystem():
    def __init__(self,username,email,password):
        self.username=username
        self.email=email
        self.password=password

    def signup(self):
        # 檢查信箱是否被註冊過
        result=collection.find_one({
            "email":self.email
        })
        if result:
            return result
        
        # 把資料存進資料庫
        collection.insert_one({
            "username":self.username,
            "password":self.password,
            "email":self.email
        })

    def signin(self):
        result=collection.find_one({
            "$and":[
                {"email":self.email},
                {"password":self.password}
            ]
        })
        return result

    def changepw(self,newpassword):
        result=collection.find_one({
            "$and":[
                {"email":self.email},
                {"password":self.password}
            ]
        })

        if not result:
            return "-1"
        
        collection.update_one({
            "email":self.email,
            "password":self.password
        },{
            "$set":{
                "password":newpassword
            }
        })