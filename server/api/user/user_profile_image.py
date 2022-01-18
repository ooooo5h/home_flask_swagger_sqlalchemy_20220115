import boto3

from flask import current_app
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage  # 파라미터로 파일을 받을 때 필요한 클래스
from flask_restful_swagger_2 import swagger


put_parser = reqparse.RequestParser()
put_parser.add_argument('profile_image', type=FileStorage, required=True, location='files', action='append')
put_parser.add_argument('user_id', type=int, required=True, location='form')


class UserProfileImage(Resource):
    
    @swagger.doc({
        'tags' : ['user'],
        'description' : '사용자 프로필사진 등록',
        'parameters' : [
            {
                'name' : 'user_id',
                'description' : '누구의 프사를 등록하나?',
                'in' : 'formData',
                'type' : 'integer',
                'required' : True
            },
            {
                'name' : 'profile_image',
                'description' : '실제로 첨부할 사진',
                'in' : 'formData',
                'type' : 'file',  
                'required' : True
            },
        ],
        'responses' : {
            '200' : {
                'description' : '사용자 프로필사진 등록 성공'
            },
            '400' : {
                'description' : '사용자 프로필사진 등록 실패'
            }
        }
    })     
    def put(self):
        """사용자 프로필사진 등록"""
        
        args = put_parser.parse_args()
        
        # aws - s3에 어떤 키/비밀키를 들고갈지 세팅
        # 키값들은 환경설정에 저장해둔 값들을 불러와서 사용
        aws_s3 = boto3.resource('s3',\
            aws_access_key_id= current_app.config['AWS_ACCESS_KEY_ID'],\
            aws_secret_access_key= current_app.config['AWS_SECRET_ACCESS_KEY'])
        
        
        # 파일의 경우 보통 여러장 첨부가 가능하다
        # args['profile_image']는 리스트로 구성된 경우가 많다
        
        for file in args['profile_image']:
            print(file)
        
        return{
            '임시' : '사용자가 프사 등록하는 기능'
        }