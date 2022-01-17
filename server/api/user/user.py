from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

# post메쏘드에서 사용할 파라미터
post_parser = reqparse.RequestParser()
post_parser.add_argument('email', type=str, required=True, location='form')  # 파라미터 이름/데이터타입/필수여부/첨부된 곳 명시
post_parser.add_argument('password', type=str, required=True, location='form')


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
        
        # 이메일, 비밀번호를 받아왔으면 확인
        print(f"이메일 : {args['email']}")
        print(f"비번 : {args['password']}")
        
        return{
            '임시' : '로그인'
        }
        
        
    @swagger.doc({
        'tags' : ['user'],
        'description' : '회원가입',
        'parameters' : [
            
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
        return{
            '임시' : '회원가입'
        }