from flask import current_app, g
from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from server import db
from server.model import Users
from server.api.utils import token_required

get_parser = reqparse.RequestParser()
get_parser.add_argument('name', type=str, required=True, location='args')
get_parser.add_argument('phone', type=str, required=True, location='args')


class UserFindEmail(Resource):
    
    @swagger.doc({
        'tags' : ['user'],
        'description' : '아이디 찾기',
        'parameters' : [
            {
                'name' : 'name',
                'description' : '사용중인 이름',
                'in' : 'query',
                'type' : 'string',  
                'required' : True
            },
            {
                'name' : 'phone',
                'description' : '사용중인 핸드폰 번호',
                'in' : 'query',
                'type' : 'string',  
                'required' : True
            },
        ],
        'responses' : {
            '200' : {
                'description' : '이메일이 문자로 전송됨'
            },
            '400' : {
                'description' : '이름/폰번 중 하나가 틀렸음'
            }
        }
    })     
    def get(self):
        """사용자 이메일 찾기(문자로 전송)"""
        
        args = get_parser.parse_args()
        
        

        
        return{
            'code' : 200,
            'message' : '문자로 이메일찾기 - 문자 전송 완료',
        }