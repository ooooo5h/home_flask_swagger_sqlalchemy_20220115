from flask_restful import Resource
from flask_restful_swagger_2 import swagger

from server.model import Lectures

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
        
    @swagger.doc({
        'tags' : ['lecture'],
        'description' : '강의 목록 조회 - 가나다순',
        'parameters' : [
            
        ],
        'responses' : {
            '200' : {
                'description' : '강의 목록 조회 성공',
            },
            '400' : {
                'description' : '강의 목록 조회 실패',
            }
        }
    })      
    def get(self):
        """강의 목록 조회"""
        
        lecture_rows = Lectures.query.order_by(Lectures.title).all()
        
        lectures = [row.get_data_object() for row in lecture_rows]
        
        return{
            'code' : 200,
            'message' : '모든 강의 목록',
            'data' : {
                'lectures' : lectures
            }
        }