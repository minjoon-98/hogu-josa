from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, create_access_token
import datetime
from pymongo import MongoClient
import jwt

app = Flask(__name__)
# MongoDB 연결 설정
client = MongoClient('localhost', 27017)
db = client.hogu_user_db
users_collection = db.users

# 토큰 생성에 사용될 SECRET_KEY를 flask 환경변수로 등록.
app.config.update(
    DEBUG = True,
    JWT_SECRET_KEY = "HOGU_SECRET_KEY"
)

jwt = JWTManager(app) # JWTManager 객체 생성

admin_id = "admin"
admin_password = "password"

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

#회원가입 엔드포인트
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    id = data.get('id')
    password = data.get('password')

    #이미 등록된 사용자인지 확인
    existing_user = users_collection.find_one({'id': id})
    if existing_user:
        return jsonify({'message': '이미 등록된 사용자입니다.'}), 400
    
    #사용자 정보 mongoDB에 저장.
    user_data = {
        'id': id,
        'password': password
    }
    users_collection.insert_one(user_data)
    
    return jsonify({'message': '회원가입 완료'}), 200

# 로그인 엔드포인트
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    id = data.get('id')
    password = data.get('password')

    # 사용자 인증
    if id == admin_id and password == admin_password:
        # JWT 토큰 생성
        expires = datetime.timedelta(seconds=60)
        access_token = create_access_token(identity=id, expires_delta=expires)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': '인증 실패'}), 401

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
