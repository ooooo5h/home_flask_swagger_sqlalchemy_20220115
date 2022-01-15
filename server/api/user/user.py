from flask_restful import Resource

class User(Resource):
    
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