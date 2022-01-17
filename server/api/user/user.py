from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

# users 테이블에 연결할 클래스 가져오기
from server.model import Users

# DB에 INSERT/UPDATE 등의 반영을 하기 위한 변수
from server import db

# post메쏘드에서 사용할 파라미터
post_parser = reqparse.RequestParser()
post_parser.add_argument('email', type=str, required=True, location='form')  # 파라미터 이름/데이터타입/필수여부/첨부된 곳 명시
post_parser.add_argument('password', type=str, required=True, location='form')

# put메쏘드에서 사용할 파라미터
put_parser = reqparse.RequestParser()
put_parser.add_argument('email', type=str, required=True, location='form')
put_parser.add_argument('password', type=str, required=True, location='form')
put_parser.add_argument('name', type=str, required=True, location='form')
put_parser.add_argument('phone', type=str, required=True, location='form')

class User(Resource):
    
    @swagger.doc({
        'tags' : ['user'],
        'description' : '사용자 정보 조회',
        'parameters' : [
                        
        ],
        'responses' : {
            '200' : {
                'description' : '사용자 정보 조회 성공',
            },
            '400' : {
                'description' : '사용자 정보 조회 실패',
            }
        }
    })   
    def get(self):
        """사용자 정보 조회"""
        return {
            '임시' : '사용자 정보 조회'
        }
  
  
    @swagger.doc({
        'tags' : ['user'],
        'description' : '로그인',
        'parameters' : [
            {
                'name' : 'email',
                'description' : '로그인에 사용할 이메일',
                'in' : 'formData',  # query or formData  ( 향후 header도 사용)
                'type' : 'string',  # string or integer or number(float) or boolean ( 향후 file도 이용 예정) 
                'required' : True,
            },     
            {
                'name' : 'password',
                'description' : '로그인에 사용할 비밀번호',
                'in' : 'formData',  
                'type' : 'string',  
                'required' : True,
            },     
        ],
        'responses' : {
            '200' : {
                'description' : '로그인 성공',
            },
            '400' : {
                'description' : '로그인 실패',
            }
        }
    })     
    def post(self):
        """로그인"""
        
        # 받아낸 파라미터들을 dict변수에 담기
        args = post_parser.parse_args()
        
        # 1단계 검사 : 이메일 있는가?        
        login_user = Users.query\
            .filter(Users.email == args['email'])\
            .first()
            
        if login_user is None:
            return{
                'code' : 400,
                'message' : '잘못된 이메일입니다.',
            }, 400
        
        # 1단계 통과 후 2단계 검사 : 비밀번호도 맞는가?
        # DB에 추가 쿼리를 조회할 필요가 없음 왜냐 => 여기 코드는 login_user가 실제 있는 상황이니까       
        if login_user.password == args['password']:
            # 이메일/비밀번호 둘다 일치
            return{
                'code' : 200,
                'message' : '로그인 성공',
                'data' : {
                    'user' : login_user.get_data_object()
                }
            }
        else:
            # 이메일은 맞는데, 비밀번호가 틀림
            return{
                'code' : 400,
                'message' : '비밀번호가 틀립니다.'
            }, 400
        
        
    @swagger.doc({
        'tags' : ['user'],
        'description' : '회원가입',
        'parameters' : [
            {
                'name' : 'email',
                'description' : '회원가입할 이메일 주소',
                'in' : 'formData',
                'type' : 'string',
                'required' : True              
            },
            {
                'name' : 'password',
                'description' : '회원가입 비밀번호',
                'in' : 'formData',
                'type' : 'string',
                'required' : True              
            },
            {
                'name' : 'name',
                'description' : '사용자 본명',
                'in' : 'formData',
                'type' : 'string',
                'required' : True              
            },
            {
                'name' : 'phone',
                'description' : '아이디 찾기에 사용할 연락처',
                'in' : 'formData',
                'type' : 'string',
                'required' : True              
            },
        ],
        'responses' : {
            '200' : {
                'description' : '회원가입 성공',
            },
            '400' : {
                'description' : '회원가입 실패',
            }
        }
    })   
    def put(self):
        """회원가입"""
        
        args = put_parser.parse_args()
        
        # 이미 사용중인 이메일이면 400으로 리턴
        already_email_used = Users.query\
            .filter(Users.email == args['email'])\
            .first()
            
        if already_email_used:
            return{
                'code' : 400,
                'message' : '이미 사용중인 이메일입니다.'
            }, 400
        
        # 파라미터들을 users테이블의 row에 추가해보기
        # 객체 지향 : 새로운 데이터를 추가한다 = 새 인스턴스를 만든다
        new_user = Users()
        new_user.email = args['email']
        new_user.password = args['password']
        new_user.name = args['name']
        new_user.phone = args['phone']
        
        # new_user의 객체를 DB에 등록시킬 준비를 하고 확정짓기
        db.session.add(new_user)
        db.session.commit()
        
        return{
            'code' : 200,
            'message' : '회원가입 성공',
            'data' : {
                'user' : new_user.get_data_object()
            }
        }
        
