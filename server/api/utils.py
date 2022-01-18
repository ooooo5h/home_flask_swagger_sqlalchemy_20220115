# 토큰을 발급하고, 발급된 토큰이 들어오면 사용자가 누구인지 분석하는 등의 기능 담당
# JWT 관련 기능 모아두는 모듈
from functools import wraps
import jwt
from flask import current_app, g
from flask_restful import reqparse

from server.model import Users

token_parser = reqparse.RequestParser()
token_parser.add_argument('X-Http-Token', type=str, required=True, location='headers')


# 토큰을 만드는 함수 => 사용자를 인증하는 용도 => 어떤 사용자에 대한 토큰?/ => 사용자 필요
def encode_token(user):
    
    # 발급된 토큰 곧바로 리턴
    # 1 : 사용자의 어떤 항목들로 토큰을 만들거야? => 나중에 복호화해서 꺼낼것도 고려해서 dict를 넣어서 암호화하자
    # 2 : 어떤 비밀키를 섞어서 암호화할거야?
    # 3 : 어떤 알고리즘으로 암호화할거야?
    return jwt.encode(
        {'id' : user.id, 'email' : user.email, 'password' : user.password}, 
        current_app.config['JWT_SECRET'],
        algorithm=current_app.config['JWT_ALGORITHM']
        )  # 이 실행결과가 곧바로 토큰 str로 나옴
    

# 토큰값을 가지고, 복호화해서 Users 객체로 변환하는 함수
def decode_token(token):
        
    try:
        # 이미 암호화된 str => 복호화 => 이전에 넣었던 dict 추출
        # 1 : 어떤 토큰 해체할꺼야?
        # 2 : 어떤 비밀키로 복호화?
        # 3 : 어떤 알고리즘?
        decoded_dict = jwt.decode(
            token,
            current_app.config['JWT_SECRET'],      
            algorithms=current_app.config['JWT_ALGORITHM']
        )
        
        user = Users.query\
            .filter(Users.id == decoded_dict['id'])\
            .filter(Users.email == decoded_dict['email'])\
            .filter(Users.password == decoded_dict['password'])\
            .first()
            
        # 제대로 토큰이 들어왔다면 복호화시 제대로된 정보로 사용자 정보 리턴
            
        return user
    
    except jwt.exceptions.DecodeError:
        # 잘못된 토큰이 들어오면, 복호화 실패 => 예외처리에 의해 이 코드로 빠짐
        # 사용자 못찾음으로 리턴
        return None
    

# 데코레이터 사용 => 추가함수에 적힌 코드를 먼저 실행하고, 실제 함수 이어서 진행
# @ 추가함수
# def 함수이름 : 

def token_required(func):
    
    @wraps(func)
    def decorator(*args, **kwargs):  # *args = 몇개의 인자를 입력할지 모를때 !! **kwargs => name='전은형'처럼 쓸 때.
    # 파라미터로 어떤 값을 받는 함수들간에 모든 함수에게 해당되게 하기 위해서 이렇게 코드 작성
    
        # 실제 함수 내용이 시작되기전에 먼저 실행해야하는 함수내용들
        
        # 1 : 토큰 파라미터를 받고
        args = token_parser.parse_args()
        
        # 2 : 그 토큰으로 실제 사용자를 받아내고
        user = decode_token(args['X-Http-Token'])
        
        # 3-1 : 사용자가 있다면 올바른 토큰이니까 원래 함수의 내용을 실행
        if user :
            
            # 토큰으로 사용자를 찾아냈다면, 원본 함수에서도 그 사용자를 가져다가 쓰면 편하겠다.
            g.user = user            
            
            return func(*args, **kwargs)
            
        # 3-2 : 사용자가 Null이라면 이유막론하고 잘못된 토큰이니까 403으로 에러 리턴
        else : 
            return {
                'code' : 403,
                'message' : '올바르지않은 토큰입니다.'
            }, 403
            
    # token_required이름표가 붙은 함수들에게 => decorator함수 전달
    return decorator