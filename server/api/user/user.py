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
    
    def post(self):
        return{
            '임시' : '로그인'
        }
        
    def put(self):
        return{
            '임시' : '회원가입'
        }