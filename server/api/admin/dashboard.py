from xml.dom.minidom import ReadOnlySequentialNamedNodeMap
from flask_restful import Resource
from server.model import Users

class DashBoard(Resource):
    
    def get(self):
        
        # 탈퇴하지 않은 회원 수? => SELECT / users 테이블 활용 => Users 모델 import
        users = Users.query.filter(Users.email != 'retired').all()
        
        
        return{
            'code' : 200,
            'message' : '관리자용 각종 통계 api',
            'data' : {
                'live_user_count' : len(users)
            }
        }