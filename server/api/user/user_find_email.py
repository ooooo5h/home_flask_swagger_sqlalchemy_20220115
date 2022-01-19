import requests

from flask import current_app, g
from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from server import db
from server.model import Users
from server.api.utils import token_required

get_parser = reqparse.RequestParser()
get_parser.add_argument('name', type=str, required=True, location='args')
get_parser.add_argument('phone', type=str, required=True, location='args')


class UserEmailFind(Resource):
    
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
        
        user = Users.query.filter(Users.name == args['name']).first()
        
        if user is None:
            return{
                'code' : 400,
                'message' : '해당 이름의 사용자는 없습니다.'
            }, 400
            
        # 이름으로 사용자 검색 성공했다. 핸드폰도 비교해야하는데, - 를 삭제하고 나서 비교하자
        input_phone = args['phone'].replace('-', '')
        user_phone = user.phone.replace('-', '')
        
        if input_phone != user_phone:
            return{
                'code' : 400,
                'message' : '이름은 맞지만 연락처가 틀립니다.'
            }, 400
            
        # 이름/핸드폰 다 맞는 유저를 찾았으면 알리고로 가자
        # 1 : 주소 => apis.aligo.in/send
        sms_url = 'https://apis.aligo.in/send/'

        # 2 : 파라미터 => 명세서 참조
        sms_send_data = {
            'key' : current_app.config['ALIGO_API_KEY'],
            'user_id' : 'cho881020',
            'sender' : '010-5112-3237',
            'receiver' : user.phone,
            'msg' : f"-MySNS 계정 안내-\n 가입하신 계정은 [{user.email}]입니다.",
        }      
                
        # 3 : 어떤 메쏘드 => POST       
        # requests의 요청에 대한 결과를 변수에 담자
        response = requests.post(url=sms_url, data=sms_send_data)
        
        respJson = response.json()
        
        # 결과코드가 1이면 성공, 그 외의 값은 500으로 알리고 문제라고 리턴
        if int(respJson['result_code']) != 1:
            return {
                'code' : 500,
                'message' : respJson['message']
            }, 500
        else :
            return{
                'code' : 200,
                'message' : '문자로 이메일찾기 - 문자 전송 완료',
            }