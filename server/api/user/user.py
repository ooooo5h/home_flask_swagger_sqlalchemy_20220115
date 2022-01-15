from flask_restful import Resource
from flask_restful_swagger_2 import swagger

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
        return {
            '임시' : '사용자 정보 조회'
        }
  
  
    @swagger.doc({
        'tags' : ['user'],
        'description' : '로그인 조회',
        'parameters' : [
            
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
        return{
            '임시' : '회원가입'
        }