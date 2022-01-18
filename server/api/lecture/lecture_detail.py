from flask_restful import Resource

class LectureDetail(Resource):
    
    def get(self):
        return {
            'code' : '특정 강의 상세조회'
        }