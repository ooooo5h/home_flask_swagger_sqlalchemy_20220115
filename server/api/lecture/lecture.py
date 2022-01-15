from flask_restful import Resource
from flask_restful_swagger_2 import swagger

class Lecture(Resource):

    @swagger.doc({
        'tags' : ['lecture'],
        'description' : '수강 취소',
        'parameters' : [
            
        ],
        'responses' : {
            '200' : {
                'description' : '수강 취소 성공',
            },
            '400' : {
                'description' : '수강 취소 실패',
            }
        }
    })      
    def delete(self):
        """수강 취소 기능"""
        return{
            '임시' : '수강취소 기능'
        }