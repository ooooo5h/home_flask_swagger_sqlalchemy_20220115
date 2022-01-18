from flask_restful import Resource

class LectureDetail(Resource):
    
    def get(self, lecture_id):
        return {
            'code' : f"{lecture_id}번 강의 상세조회"
        }