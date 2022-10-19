# Routine-API
⭐ _단비교육 기업과제_ <br>
매 주마다 정해진 일정에 자신이 해야할 일을 등록하고, <br>
해당 수행 여부에 대한 내용을 기록하여 관리할 수 있도록 도와주는 Routine-API

## 목차
1. [프로젝트 개요](#프로젝트-개요)
2. [개발 기간](#개발-기간)
3. [프로젝트 기술 스택](#프로젝트-기술-스택)
4. [요구사항 분석](#요구사항-분석)
5. [ERD](#erd)
6. [API 명세](#api-명세)
7. [프로젝트 구조](#프로젝트-구조)
8. [프로젝트 시작 방법](#프로젝트-시작-방법)


<br>

## 프로젝트 개요


Django Rest Framework 를 이용한 REST API 서버로

- 유저 회원가입, 로그인(토큰 인증 방식) 기능
- Routine 생성, 수정, 삭제, 조회 기능
- Routine 수행 여부 기록, 수행 여부 조회 기능

위 기능을 제공합니다.

<br>

## 개발 기간
- 2022.10.14 - 2022.10.20  (5일)


<br>

## 프로젝트 기술 스택

### Backend
<section>
<img src="https://img.shields.io/badge/Django-092E20?logo=Django&logoColor=white"/>
<img src="https://img.shields.io/badge/Django%20REST%20Framework-092E20?logo=Django&logoColor=white"/>
</section>

### DB
<section>
<img src="https://img.shields.io/badge/MySQL-4479A1?logo=MySQL&logoColor=white"/>
</section>

### Tools
<section>
<img src="https://img.shields.io/badge/GitHub-181717?logo=GitHub&logoColor=white"/>
<img src="https://img.shields.io/badge/Postman-FF6C37?logo=Postman&logoColor=white">
</section>

<br>

## 요구사항 분석
✅ Routine 기능: 로그인한 유저만 접근 가능하며 유저 식별은 토큰을 사용합니다. <br>
✅ Routine 기능: Routine 식별은 uri를 사용합니다.

### 1. 유저 관련

- 모델링 : django의 `AbstractBaseUser`를 상속 받아 이메일을 id로 하는 User 모델 구현

#### 1-1) 유저 회원가입
- 이메일을 id로 사용 
- 비밀번호는 문자, 숫자, 특수문자 최소 1개 이상 포함, 최소 8자 이상
  1) 비밀번호 유효성 검증을 위한 custom validator 작성

#### 1-2) 유저 로그인
- `simplejwt`를 이용하여 토큰 인증 방식 로그인 구현


### 2. Routine 관련
#### 2-1) Routine 생성
- Routine 생성시 
  1) 제목(title), 목표(goal), 분류(category), 요일(days), 알림 여부(is_alarm) 필요
  2) 요일(days)의 경우 ["MON", "TUE"] 형태로 입력받게 됨(type: list)
  3) routine의 요일 중 생성 일자의 요일과 일치하는 요일이 있는 경우 RoutineResult를 생성

<br>


#### 2-2) Routine 수정
- Routine 수정시 
  1) 제목(title), 목표(goal), 분류(category), 요일(days), 알림 여부(is_alarm) 필요
  2) `routine_id`의 경우 정합성을 고려해 수정 불가능 
  3) 요일(days)의 경우 ["MON", "TUE"] 형태로 입력받게 됨(type: list)
  4) routine의 요일 중 수정 일자의 요일과 일치하는 요일이 있고 관련 result가 없는 경우 RoutineResult를 생성
  5) 수정 일자의 요일과 일치하는 요일이 없는 경우 해당 요일의 해당 routine result 삭제

#### 2-3) Routine 조회

- Routine 전체 조회시
  1) `url/?date=2022-10-20` 형태의 경우 해당 날짜에 해야 할 Routine 목록과 그 결과를 조회
  2) `url/` 형태의 경우 현재 날짜에 해야 할 Routine 목록과 그 결과를 조회
  
- Routine 상세 조회시
  1) Routine의 상세 정보(제목, 분류, 목표, 알림 여부, 요일) 조회 가능
  2) Routine 수행 결과를 보기 위해서는 Routine result 조회 참조


#### 2-4) Routine 삭제

- `is_deleted` 필드를 이용하여 soft delete 방식으로 구현
- Routine 삭제시 관련 result는 삭제하지 않음

#### 2-5) Routine Result 관련
- Routine result 조회시
  1) 현재 요일에 해야 하는 Routine의 결과만 조회 가능
  2) Routine의 상세 정보 및 수행 결과 반환

- Routine result 기록시
  1) 현재 요일에 해야 하는 Routine의 결과만 기록 가능

- 매일 오전 0시에 해당 요일에 해야 하는 Routine의 결과 생성 (default: "NOT")

### 3. 테스트
- `rest_framework`의 `APITestCase` 이용
- Account(유저 관련) 테스트
- Routine(기능 관련) 테스트

<br>

### 기능 목록

| 버전  | 기능       | API                            | 세부 기능       | 설명                         | 상태  |
|-----|----------|--------------------------------|----------------------------|----------------------------|---|
| v1  | 유저       | POST <br> /account/signup/     |  회원가입    | 회원가입                       | ✅   |
| -   | -        | POST <br> /account/login/      | 로그인       | jwt를 이용한 로그인               | ✅   |
| -   | Routine  | POST <br> /routines/           | 생성        | Routine 생성                 | ✅   |
| -   | -        | GET <br> /routines/?date=      |조회        | Routine 전체 조회(날짜별)         | ✅   |
| -   | -        | GET <br> /routines/:id/        |조회        | Routine 상세 조회        | ✅   |
| -   | -        | PUT <br> /routines/:id/        |수정        | Routine 수정                 | ✅   | 
| -   | -        | DELETE <br> /routines/:id/     |삭제        | Routine 삭제(soft-delete)    | ✅   |
| -   | -        | GET <br> /routines/:id/result/ |결과 조회     | (현재 요일에 해야할)Routine의 결과 조회 | ✅   |
| -   | -        | PUT <br> /routines/:id/check   |결과 기록     | (현재 요일에 해야할)Routine의 결과 기록 | ✅   |
| -   | -        | -                              | 결과 생성(배치) | (현재 요일에 해야할)Routine의 결과 생성 | ✅   |
| -   | 테스트      | -                              |테스트       | 기능, 전체 테스트                 | ✅   |

🔥 추가 기능 구현시 업데이트 예정

<br>

## ERD

- USER ↔ Routine (1:N)
- User model
  - User 모델은 Django의 `AbstractBaseUser`를 overriding 
- Routine model
  - Routine ↔ RoutineDay (1:N)
  - Routine ↔ RoutineResult (1:N)

<br>


## API 명세

[POSTMAN API DOCS](https://documenter.getpostman.com/view/19274775/2s847LMBGN)

### Account 관련
### 1. 유저 회원가입
- URL: `POST /account/signup/`
- Request
```json
{
    "email": "test@test.com",
    "nickname": "test_user",
    "password": "4321test!",
    "password2": "4321test!"
}
```
- Response
  - status: `201 Created`
```json
{
    "nickname": "test_user",
    "email": "test@test.com"
}
```

<br>

### 2. 유저 로그인
- URL: `POST /account/login/`
- Request
```json
{
    "email": "test@test.com",
    "password": "4321test!"
}
```
- Response
  - status: `200 OK`
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2Njc5NTEyOSwiaWF0IjoxNjY2MTkwMzI5LCJqdGkiOiJkZWE4MGE2NzRkODg0ZmM2YjQ0ZTM3NzZhZWRkN2RiZCIsInVzZXJfaWQiOjJ9.-A7-o6B27O6aXnFyB7sx3W9PKhnriVbFi22zbsthrGc",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY2MTkzOTI5LCJpYXQiOjE2NjYxOTAzMjksImp0aSI6Ijc3ZmM2ODVjNjllZTQ3MTRiN2EwZjYyYTY2NDkwYzQwIiwidXNlcl9pZCI6Mn0.8YHbm5eGisEkURNGAPu1ICijTugQnr_DdstHpL8a41E"
}
```

<br>

### Routine 관련
### 1. Routine 생성
- URL: `POST /routines/`
- Request
```json
{
   "title" : "problem solving",
   "category" : "HOMEWORK",
   "goal": "Increase your problem-solving skills",
   "is_alarm": true,
   "days": ["MON", "WED", "FRI"]
}
```
- Response
  - status: `201 Created`
```json
{
    "data": {
        "routine_id": 7
    },
    "message": {
        "msg": "You have successfully created the routine.",
        "status": "ROUTINE_CREATE_OK"
    }
}
```

<br>

### 2. Routine 조회
#### 2-1. 전체 조회
- URL: `GET /routines/?date=`

- Response
  - status: `200 OK`
```json
{
    "data": [
        {
            "id": 7,
            "title": "테스트",
            "goal": "테스트 성공",
            "result": "NOT"
        }
    ],
    "message": {
        "msg": "Routine lookup was successful.",
        "status": "ROUTINE_LIST_OK"
    }
}
```

<br>

#### 2-2. 상세 조회
- URL: `GET /routines/:id/`

- Response
  - status: `200 OK`
```json
{
    "data": {
        "id": 7,
        "title": "테스트",
        "goal": "테스트 성공",
        "days": [
            "MON",
            "TUE",
            "WED"
        ]
    },
    "message": {
        "msg": "Routine lookup was successful.",
        "status": "ROUTINE_DETAIL_OK"
    }
}
```

<br>


### 3. Routine 수정
- URL: `PUT /routines/:id/`
- Request
```json
{
    "title": "테스트(수정)",
    "goal": "테스트 성공",
    "category": "HOMEWORK",
    "is_alarm": true,
    "days": ["THU"]
}
```
- Response
  - status: `200 OK`
```json
{
    "data": {
        "routine_id": 7
    },
    "message": {
        "msg": "The routine has been modified.",
        "status": "ROUTINE_UPDATE_OK"
    }
}
```

<br>


### 4. Routine 삭제
- URL: `DELETE /routines/:id/`

- Response
  - status: `200 OK`
```json
{
    "data": {
        "routine_id": 7
    },
    "message": {
        "msg": "The routine has been deleted.",
        "status": "ROUTINE_DELETE_OK"
    }
}
```

<br>

### Routine Result 관련
### 1. Routine 결과 조회
- URL: `GET /routines/:id/result/`

- Response
  - status: `200 OK`
```json
{
    "data": {
        "id": 8,
        "title": "테스트(수정)",
        "goal": "테스트 성공",
        "days": [
            "THU"
        ],
        "result": "NOT"
    },
    "message": {
        "msg": "The routine result lookup was successful.",
        "status": "ROUTINE_RESULT_LOOKUP_OK"
    }
}
```

<br>

### 2. Routine 결과 기록
- URL: `PUT /routines/:id/check/`

- Request
```json
{
    "result": "TRY"
}
```
- Response
  - status: `200 OK`
```json
{
    "data": {
        "routine_id": 7
    },
    "message": {
        "msg": "The routine result has been modified.",
        "status": "ROUTINE_RESULT_UPDATE_OK"
    }
}
```

<br>

## 프로젝트 구조
```bash         
├── apps                  
│   ├── routine           
│   │   ├── admin.py      
│   │   ├── apps.py       
│   │   ├── migrations    
│   │   ├── models.py     
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── tests.py      
│   │   ├── urls.py       
│   │   └── views.py      
│   └── urls.py
├── common
│   └── account
│       ├── admin.py
│       ├── apps.py
│       ├── forms.py
│       ├── migrations
│       ├── models.py
│       ├── serializers.py
│       ├── tests.py
│       ├── urls.py
│       ├── validator.py
│       └── views.py
├── config
│   ├── asgi.py
│   ├── settings
│   │   ├── base.py
│   │   ├── dev.py
│   │   ├── prod.py
│   │   └── test.py
│   ├── urls.py
│   └── wsgi.py
├── jobs
│   ├── apps.py
│   ├── jobs.py
│   └── updater.py
├── manage.py
└── requirements.txt

```

<br>

## 프로젝트 시작 방법
1. 로컬에서 실행할 경우
```bash
# 프로젝트 clone(로컬로 내려받기)
git clone -b develop --single-branch ${github 주소}
cd ${디렉터리 명}

# 가상환경 설정
python -m venv ${가상환경명}
source ${가상환경명}/bin/activate
# window (2 ways) 
# 1> ${가상환경명}/Scripts/activate
# 2> activate

# 라이브러리 설치
pip install -r requirements.txt
# 실행
python manage.py runserver
```

<br>