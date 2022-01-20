from flask_restful import Resource
from server.model import Users, Lectures, LectureUser

class DashBoard(Resource):
    
    def get(self):
        
        # 탈퇴하지 않은 회원 수? => SELECT / users 테이블 활용 => Users 모델 import
        # first()는 한 줄 / all()은 목록 / count() 는 검색된 갯수
        users_count = Users.query.filter(Users.email != 'retired').count()
        
        
        # 연습 : 자바 강의를 듣는 사람들의 정보 => JOIN 어떻게 할꺼야..?
        
        java_user_list = Users.query\
            .filter(LectureUser.user_id == Users.id)\
            .filter(LectureUser.lecture_id == Lectures.id)\
            .filter(Lectures.title == '자바')\
            .all()
            
        print(java_user_list)
        
        return{
            'code' : 200,
            'message' : '관리자용 각종 통계 api',
            'data' : {
                'live_user_count' : users_count
            }
        }