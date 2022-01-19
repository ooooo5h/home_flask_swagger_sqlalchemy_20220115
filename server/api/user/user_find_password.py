import requests

from flask import current_app, g
from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from server import db
from server.model import Users
from server.api.utils import token_required

get_parser = reqparse.RequestParser()
get_parser.add_argument('name', type=str, required=True, location='args')
get_parser.add_argument('email', type=str, required=True, location='args')
get_parser.add_argument('phone', type=str, required=True, location='args')


class UserPasswordFind(Resource):
    
    @swagger.doc({
        'tags' : ['user'],
        'description' : '비밀번호 찾기',
        'parameters' : [
            {
                'name' : 'email',
                'description' : '비밀번호 찾을 이메일',
                'in' : 'query',
                'type' : 'string',  
                'required' : True
            },
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
                'description' : '비밀번호가 이메일로 전송됨'
            },
            '400' : {
                'description' : '이름/폰번 중 하나가 틀렸음'
            }
        }
    })     
    def get(self):
        """비밀번호 찾기(이메일로 전송)"""
        
        args = get_parser.parse_args()
        
        user = Users.query.filter(Users.email == args['email']).first()
        
        if user is None:
            return{
                'code' : 400,
                'message' : '해당 이메일의 사용자는 없습니다.'
            }, 400
            
        # 이메일로 사용자 검색 성공했다. 핸드폰도 비교, - 를 삭제하고 나서 비교하자 + 이름도 비교
        input_phone = args['phone'].replace('-', '')
        user_phone = user.phone.replace('-', '')
        
        if input_phone != user_phone or args['name'] != user.name:
            return{
                'code' : 400,
                'message' : '이메일은 맞는데, 연락처나 이름이 맞지 않습니다.'
            }, 400
        
        # 메일 전송의 api는 mailgun.com 사이트를 활용해보자
        
        # 어느 주소
        mailgun_url = 'https://api.mailgun.net/v3/mg.gudoc.in/messages'
              
        # 어느 파라미터
        email_data = {
            'from' : 'system@gudoc.in',
            'to' : user.email,
            'subject' : '[MySNS 비밀번호 안내] 비밀번호 찾기 알림 메일입니다.',
            'text' : '실제 발송 내용'
        }
        
        # 어느 메쏘드
        requests.post(url=mailgun_url, data=email_data, auth=('api', current_app.config['MAILGUN_API_KEY']))
        
        
        return {
            'code' : 200,
            'message' : '비밀번호를 이메일로 전송했습니다.(임시)'
        }