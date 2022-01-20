from flask_restful import Resource
from server.model import Users, Lectures, LectureUser
from server import db

class DashBoard(Resource):
    
    def get(self):
        
        # 탈퇴하지 않은 회원 수? => SELECT / users 테이블 활용 => Users 모델 import
        # first()는 한 줄 / all()은 목록 / count() 는 검색된 갯수
        users_count = Users.query.filter(Users.email != 'retired').count()
        
        
        # 연습 : 자바 강의의 매출 총액이 궁금해=> JOIN 어떻게 할꺼야..?
        # query(SELECT문의 컬럼 선택처럼 여러 항목 가능)
        # db.func.집계함수(컬럼) => 집계함수 동작
        
        # filter 나열 => JOIN과 ON을 한번에 명시
        # filter 나열 2 => 마지막 filter는 JOIN이 끝난 후, WHERE절처럼 실제 필터 조건을 적으면 됨
        
        # group_by => 어떤 값을 기준으로 그룹지을지
        lecture_fee_amount = db.session.query(Lectures.title, db.func.sum(Lectures.fee))\
            .filter(Lectures.id == LectureUser.lecture_id)\
            .filter(LectureUser.user_id == Users.id)\
            .group_by(Lectures.id)\
            .all()
        
        # print(lecture_fee_amount) => JSON 응답으로 내려갈 수 없어서 추가 가공이 필요함
        
        amount_list = [{ 'lecture_title' : row[0], 'amount' : int(row[1]) } for row in lecture_fee_amount]         
        
        # 남성 회원수와 여성 회원수를 보여줘
        users_count_by_gender_list = db.session.query(Users.is_male, db.func.count(Users.id))\
            .group_by(Users.is_male)\
            .all()
            
        gender_user_counts = [{'is_male' : row[0], 'user_count' : int(row[1])} for row in users_count_by_gender_list]
                
        return{
            'code' : 200,
            'message' : '관리자용 각종 통계 api',
            'data' : {
                'live_user_count' : users_count,
                'lecture_fee_amount' : amount_list, # 각 강의별 총 합
                'gender_user_counts' : gender_user_counts, # 성별에 따른 사용자 수
            }
        }