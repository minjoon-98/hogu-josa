# 호구조사 (Hogujosa)
 
## 프로젝트 개요
프로젝트 기간 : 2024.03.18 ~ 2024.03.21 (3일)
 
팀원 : [강용제](https://github.com/oasisgorilla)(Leader/FE), [김민준](https://github.com/minjoon-98)(FE), [김재학](https://github.com/rlawogkr)(BE)

## 기술 스택
| 분류 | 기술 | 
|-----|-----|
|**Frontend**|<img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=HTML5&logoColor=FFFFFF"/> <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=CSS3&logoColor=FFFFFF"/> <img src="https://img.shields.io/badge/Bulma-00D1B2?style=for-the-badge&logo=Bulma&logoColor=FFFFFF"/> <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=JavaScript&logoColor=FFFFFF"/>|
|**Backend**|<img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=Flask&logoColor=white"> <img src="https://img.shields.io/badge/Jinja-B41717?style=for-the-badge&logo=Jinja&logoColor=FFFFFF"/> <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=FFFFFF"/>|
|**Database**|<img src="https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=MongoDB&logoColor=FFFFFF"/>| 
|**Infra/Devops**|<img src="https://img.shields.io/badge/FileZilla-BF0000?style=for-the-badge&logo=FileZilla&logoColor=FFFFFF"/> <img src="https://img.shields.io/badge/Amazon EC2-FF9900?style=for-the-badge&logo=Amazon EC2&logoColor=FFFFFF"/>|
 
## 프로젝트 소개

**개인 정보 공유 서비스 '호구조사'**

크래프톤 정글 5기 2교육장 2팀 0주차 프로젝트

“**첫 만남에 선넘지 않도록**”

호구조사는 정보 공유가 부담스러울 수 있는 점을 고려하여, 사용자가 원하는 만큼만 자신을 공개할 수 있도록 설계되었습니다. 

이 서비스에서는 사용자가 공개한 정보에 한해 상대방의 정보를 열람할 수 있습니다. <br/> 즉, 상대방의 정보를 더 알고 싶다면, 자신도 해당 정보를 등록해야 합니다. <br/> 이를 통해 사용자는 부담 없이 필요한 만큼만 정보를 공유하고, 상대방과 더 빠르고 자연스럽게 서로를 알아갈 수 있습니다.

## 주요 기능

- **회원가입**: 사용자가 다양한 정보를 입력하여 회원가입할 수 있습니다.
- **로그인**: 가입한 사용자는 JWT를 발급받아 로그인할 수 있습니다.
- **사용자 정보 보기**: 사용자는 자신이 등록한 정보에 한해서만 다른 사용자들의 공개된 정보를 열람할 수 있습니다.
- **프로필 업데이트**: 사용자가 자신의 프로필 정보를 수정할 수 있습니다.
- **계정 삭제**: 사용자는 자신의 계정을 삭제할 수 있습니다.
- **JWT 인증 및 토큰 갱신**: JWT를 통해 인증하며, 토큰 만료 시 리프레시 토큰을 사용하여 갱신합니다.

## 디렉토리 구조

```
├── app.py                # Flask 애플리케이션의 메인 파일
├── templates
│   ├── login.html        # 로그인 페이지
│   ├── main.html         # 메인 페이지
│   ├── signup.html       # 회원가입 페이지
│   └── mypage.html       # 사용자 정보 페이지
├── find_users.py         # MongoDB 연결 및 사용자 정보 조회 스크립트
└── README.md             # 프로젝트 설명 파일
```

### 페이지 설명

- **login.html**: 로그인 페이지, 사용자가 로그인할 수 있습니다.
- **signup.html**: 회원가입 페이지, 새로운 사용자가 계정을 생성할 수 있습니다.
- **main.html**: 메인 페이지, 로그인 후 다른 사용자들의 정보를 카드 형태로 볼 수 있습니다.
- **mypage.html**: 사용자가 자신의 정보를 확인하고 수정할 수 있는 페이지입니다.

## 설치 및 실행 방법

1. **필수 구성 요소**:
   - Python 3.7 이상
   - MongoDB 설치 및 실행

2. **패키지 설치**:
   ```bash
   pip install Flask pymongo Flask-JWT-Extended
   ```

3. **MongoDB 설정**:
   - MongoDB를 실행하고, `hogu_user_db` 데이터베이스를 생성합니다.
   - `users`와 `refresh_tokens` 컬렉션이 자동으로 생성됩니다.

4. **애플리케이션 실행**:
   ```bash
   python app.py
   ```
   - 서버는 기본적으로 `http://localhost:5001`에서 실행됩니다.

## 엔드포인트 설명

- **회원가입** (`/signup`)
  - **메소드**: `POST`
  - **요청 데이터**: `id`, `password`, `name`, `location`, `birthday`, `motivation`, `interests`, `mbti`, `major`, `baekjoon_rank`, `relationship_status`, `pet_status`, `hobbies`

- **로그인** (`/login`)
  - **메소드**: `POST`
  - **요청 데이터**: `id`, `password`
  - **응답 데이터**: `access_token`, `refresh_token`

- **사용자 정보 조회** (`/users`)
  - **메소드**: `GET`
  - **요청 헤더**: `Authorization: Bearer {access_token}`

- **사용자 정보 수정** (`/update`)
  - **메소드**: `PUT`
  - **요청 헤더**: `Authorization: Bearer {access_token}`
  - **요청 데이터**: 수정할 필드와 해당 값

- **계정 삭제** (`/delete_account`)
  - **메소드**: `DELETE`
  - **요청 헤더**: `Authorization: Bearer {access_token}`

- **토큰 갱신** (`/refresh`)
  - **메소드**: `POST`
  - **요청 헤더**: `Authorization: Bearer {refresh_token}`

- **사용자 정보 찾기** (`/find`)
  - **메소드**: `POST`
  - **요청 헤더**: `Authorization: Bearer {access_token}`

## JWT 인증

이 애플리케이션은 JWT를 사용하여 사용자를 인증합니다. 로그인 후 발급된 액세스 토큰을 통해 보호된 리소스에 접근할 수 있으며, 토큰이 만료되면 리프레시 토큰을 사용하여 새로운 액세스 토큰을 발급받을 수 있습니다.

## 주의사항

- **MongoDB**: 이 애플리케이션은 MongoDB와 연결되어 있으므로, MongoDB가 로컬에서 실행 중이어야 합니다.
- **시크릿 키 관리**: `app.config['JWT_SECRET_KEY']`에 설정된 시크릿 키는 안전하게 관리해야 합니다.
- **토큰 만료 시간**: 기본 설정으로 액세스 토큰은 10분, 리프레시 토큰은 10일 동안 유효합니다. 필요에 따라 이 값을 조정할 수 있습니다.

<!--
### 기여 방법

이 프로젝트는 오픈 소스입니다. 기여를 환영하며, 버그 수정, 기능 추가 및 개선 사항에 대한 PR(Pull Request)을 제출해 주세요.

### 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 LICENSE 파일을 참조하세요.
-->
