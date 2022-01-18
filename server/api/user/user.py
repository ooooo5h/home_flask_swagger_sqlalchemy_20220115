from ast import arg
from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

import datetime

# users 테이블에 연결할 클래스 가져오기
from server.model import Users
from server.api.utils import encode_token

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

# get메쏘드에서 사용할 파라미터
get_parser = reqparse.RequestParser()
get_parser.add_argument('email', type=str, required=False, location='args')
get_parser.add_argument('name', type=str, required=False, location='args')

# delete메쏘드에서 사용할 파라미터
delete_parser = reqparse.RequestParser()
delete_parser.add_argument('user_id', type=int, required=True, location='args')

# patch메쏘드에서 사용할 파라미터
patch_parser = reqparse.RequestParser()
patch_parser.add_argument('user_id', type=int, required=True, location='form')
patch_parser.add_argument('field', type=str, required=True, location='form')
patch_parser.add_argument('value', type=str, required=True, location='form')


class User(Resource):
    
    @swagger.doc({
        'tags' : ['user'],
        'description' : '사용자 정보 조회',
        'parameters' : [
            {
                'name' : 'email',
                'description' : '검색해볼 이메일 - 완전히 맞는 이메일만 찾아줌',
                'in' : 'query',
                'type' : 'string',
                'required' : False,
            },
            {
                'name' : 'name',
                'description' : '검색해볼 이름 - 일부분만 일치해도 찾아줌',
                'in' : 'query',
                'type' : 'string',
                'required' : False,
            },
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
        
        args = get_parser.parse_args()
        
        # 1 : 이메일을 파라미터로 받아서 일치하는 회원을 리턴
        # 이메일 파라미터는 없을 수도 있음 ==> 실제로 첨부되었는지 확인하는 작업이 필요
        if args['email']:
            # args : 일종의 dict => 'email'조회를 했는데 첨부가 안되었다면 None으로 리턴
            # email 파라미터가 첨부된 상황
            user_by_email = Users.query.filter(Users.email == args['email']).first()
            
            if user_by_email:
                return {
                    'code' : 200,
                    'message' : '이메일로 사용자 검색 성공',
                    'user' : user_by_email.get_data_object()
                }
            else:
                return{
                    'code' : 400,
                    'message' : '이메일로 사용자 검색 결과 없음'
                }, 400
        
        # 2 : 이름이 파라미터로 왔다면, 경진 => 조경진도 리턴
        if args['name']:
            # 이메일은 첨부가 안되어있음!!
            
            # ex. '은' ==> 전은형/ 전은영 등 여러 경우가 나올 수 있다 => all()
            # 쿼리의 조건에서 LIKE 활용 예시
            users_by_name = Users.query.filter(Users.name.like(f"%{args['name']}%")).all()
            
            # JSON 으로 내려갈 수 있는 dict형태로 목록을 변환
            searched_users_list = [ user.get_data_object()  for user in users_by_name]
        
            return{
                'code' : 200,
                'message' : '이름으로 사용자 검색 성공',
                'data' : {
                    'users' : searched_users_list
                }
            }
        
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
                    'user' : login_user.get_data_object(),
                    'token' : encode_token(login_user)
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
            
        # 이미 사용중인 연락처라면 가입 불허
        already_phone_used = Users.query\
            .filter(Users.phone == args['phone'])\
            .first()
            
        if already_phone_used:
            return{
                'code' : 400,
                'message' : '이미 사용중인 연락처입니다.'
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
                'user' : new_user.get_data_object(),
                'token' : encode_token(new_user)
            }
        }
        
    @swagger.doc({
        'tags' : ['user'],
        'description' : '회원탈퇴',
        'parameters' : [
            {
                'name' : 'user_id',
                'description' : '몇번 사용자를 지울건가요?',
                'in' : 'query',
                'type' : 'integer',
                'required' : True
            }
        ],
        'responses' : {
            '200' : {
                'description' : '삭제 성공'
            },
            '400' : {
                'description' : '삭제 실패'
            }
        }
    })   
    def delete(self):
        """회원 탈퇴하기"""
        
        args = delete_parser.parse_args()
        
        # args['user_id']를 이용해서 삭제할 사용자가 실존하는지 확인
        
        delete_user = Users.query.filter(Users.id == args['user_id']).first()
        
        if delete_user == None:
            return{
                'code' : 400,
                'message' : '해당 사용자는 존재하지 않습니다.'
            }, 400
       
        # delete_user에 실제 객체가 들어있다 => 활용하자
                    
        # db.session.delete(delete_user) # 누구를 삭제할지
        # db.session.commit()            # 실제 삭제 수행 => 이 사용자의 활동 내역도 다 같이 지워야 정상 동작
        
        # 실무 : 기존 데이터를 모두 임시 데이터로 변경
        delete_user.name = '탈퇴회원'
        delete_user.email = 'retired'
        delete_user.password = 'retired'
        delete_user.retired_at = datetime.datetime.utcnow()
        
        db.session.add(delete_user)
        db.session.commit()
        
        return{
            'code' : 200,
            'message' : '회원 삭제 수행 완료'
        }

    @swagger.doc({
        'tags' : ['user'],
        'description' : '회원정보 수정',
        'parameters' : [
            {
                'name' : 'user_id',
                'description' : '몇번 사용자를 수정할건지?',
                'in' : 'formData',
                'type' : 'integer',
                'required' : True
            },
            {
                'name' : 'field',
                'description' : '어느 항목을 변경할지? - name / phone 중 하나만 입력',
                'in' : 'formData',
                'type' : 'string',  # name / phone 둘 중 하나를 입력받자 => 입력자체를 제한걸자
                'enum' : ['name', 'phone'],
                'required' : True
            },
            {
                'name' : 'value',
                'description' : '어떤 값으로 변경할지?',
                'in' : 'formData',
                'type' : 'string',  
                'required' : True
            },
        ],
        'responses' : {
            '200' : {
                'description' : '회원 정보 변경 성공'
            },
            '400' : {
                'description' : '회원 정보 변경 실패'
            }
        }
    })           
    def patch(self):
        """회원 정보 수정"""
        
        args = patch_parser.parse_args()
        
        edit_user = Users.query.filter(Users.id == args['user_id']).first()
        
        if not edit_user:
            return{
                'code' : 400,
                'message' : '해당 사용자는 존재하지 않습니다.'
            }, 400
        
        # edit_user에 사용자가 존재함
        
        if args['field'] == 'name':
            edit_user.name = args['value']
            db.session.add(edit_user)
            db.session.commit()
            
            return {
                'code' : 200,
                'message' : '이름 변경 성공'
            }
        elif args['field'] == 'phone':
            edit_user.phone = args['value']
            db.session.add(edit_user)
            db.session.commit()
            
            return {
                'code' : 200,
                'message' : '연락처 변경 성공'
            }
            
        
        return{
            'code' : 400,
            'message' : 'field항목은 name/phone 중 하나여야 합니다.'
        }, 400
