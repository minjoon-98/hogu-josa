from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import JWTManager, create_refresh_token, create_access_token, jwt_required, get_jwt_identity
import datetime
from pymongo import MongoClient
import jwt

app = Flask(__name__)

# MongoDB 연결 설정
client = MongoClient('localhost', 27017)
db = client.hogu_user_db
users_collection = db.users
refresh_tokens_collection = db.refresh_tokens #리프레시토큰 저장 컬렉션

app.config['JWT_SECRET_KEY'] = 'hogu' # JWT 시크릿 키 설정
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=10) # JWT 토큰 만료 시간 설정
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(days=10) # JWT 리프레시 토큰 만료 시간 설정

jwt = JWTManager(app) # JWTManager 객체 생성

def is_token_valid(token):
    try:
        jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return True
    except Exception as e:
        return False
    return False

@app.route('/test')
def test():
    return jsonify({"data": request.headers.get('Authorization')})

@app.route('/')
def index():
    if is_token_valid(request.headers.get('Authorization')):
        return render_template('/main.html')
    return render_template('login.html')

@app.route('/main')
@jwt_required()
def main_page():
    return render_template('main.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

#회원가입 엔드포인트
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json # 클라이언트로부터 전달받은 JSON 데이터
    id = data.get('id')
    password = data.get('password')
    name = data.get('name')
    location = data.get('location')
    birthday = data.get('birthday')
    motivation = data.get('motivation')
    interests = data.get('interests')
    mbti = data.get('mbti')
    major = data.get('major')
    baekjoon_rank = data.get('baekjoon_rank')
    relationship_status = data.get('relationship_status')
    pet_status = data.get('pet_status')
    hobbies = data.get('hobbies')
    


    #이미 등록된 사용자인지 확인
    existing_user = users_collection.find_one({'id': id})
    if existing_user:
        return jsonify({'message': '이미 등록된 사용자입니다.'}), 400
    
    #사용자 정보 mongoDB에 저장.
    user_data = {
        'id': id,
        'password': password,
        'name': name,
        'location': location,
        'birthday': birthday,
        'motivation': motivation,
        'interests': interests,
        'mbti': mbti,
        'major': major,
        'baekjoon_rank': baekjoon_rank,
        'relationship_status': relationship_status,
        'pet_status': pet_status,
        'hobbies': hobbies
    }
    users_collection.insert_one(user_data)
    
    return jsonify({'message': '회원가입 완료'}), 200

@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    expires = datetime.timedelta(seconds=600) 
    access_token = create_access_token(identity=current_user, expires_delta=expires)
    return jsonify({'access_token': access_token}), 200

# 로그인 엔드포인트
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    id = data.get('id')
    password = data.get('password')

    # 사용자 인증
    user = users_collection.find_one({'id': id, 'password': password})
    if user:
        # JWT 토큰 생성
        access_token = create_access_token(identity=id)
        refresh_token = create_refresh_token(identity=id)

        # 리프레시 토큰 저장
        refresh_tokens_collection.insert_one({'refresh_token': refresh_token})

        return jsonify({'access_token': access_token, 'refresh_token':refresh_token}), 200
    else:
        return jsonify({'message': '인증 실패'}), 401
    
# 사용자 정보를 가져오는 엔드포인트
@app.route('/users', methods=['GET'])
def get_users():
    users = list(users_collection.find({}, {'_id': 0}))  # 모든 사용자 정보를 가져옴
    return jsonify(users), 200

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
