from pymongo import MongoClient

# MongoDB 연결 설정
client = MongoClient('localhost', 27017)
db = client.hogu_user_db
users_collection = db.users  # 사용자 정보를 저장할 컬렉션 생성

# 모든 사용자 정보 출력
for user in users_collection.find():
    print(user)
