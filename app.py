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


@app.route('/delete_account', methods=['DELETE'])
@jwt_required()
def delete_account():
    current_user = get_jwt_identity() # 현재 로그인 사용자 id
    res = users_collection.delete_one({'id': current_user})

    if res.deleted_count == 1:
        return jsonify({'message': '계정 삭제 완료'}), 200
    else:
        return jsonify({'message': '사용자 정보를 찾을 수 없습니다.'}), 400


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/main')
def main_page():
    return render_template('main.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/mypage')
def mypage():
    return render_template('mypage.html')

#회원가입 엔드포인트
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json # 클라이언트로부터 전달받은 폼 데이터

    # 'id' 필드가 전송되었는지 확인
    if 'id' not in data:
        return jsonify({'message': '아이디를 입력해주세요.'}), 400

    id = data['id']
    password = data['password']
    name = data['name']
    location = data['location']
    birthday = data['birthday']
    motivation = data['motivation']
    interests = data['interests']
    mbti = data['mbti']
    major = data['major']
    baekjoon_rank = data['baekjoon_rank']
    relationship_status = data['relationship_status']
    pet_status = data['pet_status']
    hobbies = data['hobbies']

    # 이미 등록된 사용자인지 확인
    existing_user = users_collection.find_one({'id': id})
    if existing_user:
        return jsonify({'message': '이미 등록된 사용자입니다.'}), 400
    
    # 사용자 정보 MongoDB에 저장
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

# 사용자 정보를 업데이트
@app.route('/update', methods=['PUT'])
@jwt_required() # JWT 토큰이 필요한 엔드포인트
def update_user():
    current_user = get_jwt_identity()   # 현재 로그인한 사용자의 ID
    data = request.json # 클라이언트로부터 전달받은 JSON 데이터

    existing_user = users_collection.find_one({'id': current_user})
    
    if existing_user:
        for key, value in data.items():
            existing_user[key] = value

        users_collection.update_one({'id': current_user}, {'$set': existing_user})
        return jsonify({'message': '사용자 정보 업데이트 완료'}), 200
    else:
        return jsonify({'message': '사용자 정보를 찾을 수 없습니다.'}), 404

# 사용자 정보를 찾는 엔드포인트
@app.route('/find', methods=['POST'])
@jwt_required() # JWT 토큰이 필요한 엔드포인트
def find_user():
    current_user = get_jwt_identity()
    currUser = users_collection.find_one({'id': current_user}, {'_id': 0})
    if currUser:
        for _ in currUser.items():
            # print(currUser.items())
            currUser_name = currUser['name']
            currUser_id = currUser['id']
            currUser_location = currUser['location']
            currUser_birthday = currUser['birthday']
            currUser_motivation = currUser['motivation']
            currUser_interests = currUser['interests']
            currUser_mbti = currUser['mbti']
            currUser_major = currUser['major']
            currUser_baekjoon_rank = currUser['baekjoon_rank']
            currUser_relationship_status = currUser['relationship_status']
            currUser_pet_status = currUser['pet_status']
            currUser_hobbies = currUser['hobbies']


            return jsonify({'name': currUser_name, 
                            'id': currUser_id, 
                            'location': currUser_location, 
                            'birthday': currUser_birthday, 
                            'motivation': currUser_motivation, 
                            'interests': currUser_interests, 
                            'mbti': currUser_mbti, 
                            'major': currUser_major, 
                            'baekjoon_rank': currUser_baekjoon_rank, 
                            'relationship_status': currUser_relationship_status, 
                            'pet_status': currUser_pet_status, 
                            'hobbies': currUser_hobbies}), 200
    else:
        return jsonify({'message': '사용자 정보를 찾을 수 없습니다.'}), 404

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
