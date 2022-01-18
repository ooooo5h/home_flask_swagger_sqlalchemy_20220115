import hashlib
import boto3
import time
import os
import hashlib # str -> 암호화된 문구로 변경

from flask import current_app
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage  # 파라미터로 파일을 받을 때 필요한 클래스
from flask_restful_swagger_2 import swagger

from server import db
from server.model import Users

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
        
        upload_user = Users.query.filter(Users.id == args['user_id']).first()
        
        if upload_user is None:
            return{
                'code' : 400,
                'message' : '해당 사용자 없음'
            }, 400
        
        # aws - s3에 어떤 키/비밀키를 들고갈지 세팅
        # 키값들은 환경설정에 저장해둔 값들을 불러와서 사용
        aws_s3 = boto3.resource('s3',\
            aws_access_key_id= current_app.config['AWS_ACCESS_KEY_ID'],\
            aws_secret_access_key= current_app.config['AWS_SECRET_ACCESS_KEY'])
        
        
        # 파일의 경우 보통 여러장 첨부가 가능하다
        # args['profile_image']는 리스트로 구성된 경우가 많다
        
        for file in args['profile_image']:
            # print(file)   # file : 파일이름/실제 이미지 등 본문 분리
            
            # 파일 이름이 저장됨 filename => S3버킷에 저장될 경로 생성에 활용
            # print(file.filename)
            
            # 1 : 파일 이름 재가공
            
            user_email = upload_user.email      # 실제 업로드하는 사람의 이메일
            now = round(time.time() * 10000)  #   현재 시간을 대충 숫자값으로 표현.
            
            new_file_name = f"MySNS_{hashlib.md5(user_email.encode('utf-8')).hexdigest()}_{now}"
            
            # 2 : 확장자 추출
            
            _, file_extension = os.path.splitext(file.filename)  # 원래 올라온 파일명을 파일이름/확장자로 분리
            
            new_file_name = f"{new_file_name}{file_extension}"
            
            # 최종경로 => 1, 2의 합체 + S3의 폴더            
            
            s3_file_path = f'images/profile_imgs/{new_file_name}'   # 올라갈 경로
            
            
            # 파일 본문도  따로 저장 => 실제로 s3 경로에 업로드
            file_body = file.stream.read()   # 올려줄 파일
            
            # 어떤 버킷에 올려줄거야 + 파일업로드 한 큐에
            aws_s3.Bucket(current_app.config['AWS_S3_BUCKET_NAME']).put_object(Key=s3_file_path, Body=file_body)
            
            # 이 파일을 누구나 볼 수 있게 public허용
            aws_s3.ObjectAcl(current_app.config['AWS_S3_BUCKET_NAME'], s3_file_path).put(ACL='public-read')
            
            
            # 사용자의 프로필 사진 경로를, s3_file_path로 저장해보자
            upload_user.profile_img_url = s3_file_path  # DB에 사용자 프사 경로 저장
            
            db.session.add(upload_user)
            db.session.commit()
            
        
        return{
            'code' : 200,
            'message' : '사용자 프로필 사진 변경',
            'data' : {
                'user' : upload_user.get_data_object()
            }
        }