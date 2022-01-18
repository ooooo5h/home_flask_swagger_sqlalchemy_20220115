import hashlib
import boto3
import time
import os

from flask import current_app
from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from server import db
from server.model import Feeds, Users

from werkzeug.datastructures import FileStorage

post_parser = reqparse.RequestParser()
post_parser.add_argument('user_id', type=int, required=True, location='form')
post_parser.add_argument('lecture_id', type=int, required=True, location='form')
post_parser.add_argument('content', type=str, required=True, location='form')
post_parser.add_argument('feed_images', type=FileStorage, required=False, location='files', action='append')

class Feed(Resource):
    
    @swagger.doc({
        'tags' : ['feed'],
        'description' : '게시글 등록하기',
        'parameters' : [
            {
                'name' : 'user_id',
                'description' : '어느 사용자가 쓴건지',
                'in' : 'formData',
                'type' : 'integer',  
                'required' : True
            },   
            {
                'name' : 'lecture_id',
                'description' : '어느 강의에 대해 쓴건지',
                'in' : 'formData',
                'type' : 'integer',  
                'required' : True
            },        
            {
                'name' : 'content',
                'description' : '게시글 내용',
                'in' : 'formData',
                'type' : 'string',  
                'required' : True
            }
        ],
        'responses' : {
            '200' : {
                'description' : '게시글 등록 성공',
            },
            '400' : {
                'description' : '게시글 등록 실패',
            }
        }
    })    
    def post(self):
        """게시글 등록하기"""
        
        args = post_parser.parse_args()
        
        new_feed = Feeds()
        new_feed.user_id = args['user_id']
        new_feed.lecture_id = args['lecture_id']
        new_feed.content = args['content']
        
        db.session.add(new_feed)
        db.session.commit()

        # commit시점 이후에는 DB에 등록이 완료되었기때문에, id/created_at 등의 자동 등록 데이터도 모두 설정이 완료됨
        
        # 사진 목록을 등록하는 행위는 commit()으로 id값이 확인 가능하게 된 후에 작업하자
        
        # 사진이 첨부되지 않았을 수도 있다 => 확인해보고 올리자
        if args['feed_images'] : #사진이 파라미터에 첨부되었나?
            
            upload_user = Users.query.filter(Users.id == args['user_id']).first()
            
            aws_s3 = boto3.resource('s3',\
                aws_access_key_id= current_app.config['AWS_ACCESS_KEY_ID'],\
                aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'])
            
            for image in args['feed_images']:  
                
                _, file_extensions = os.path.splitext(image.filename)
                
                s3_file_name = f"images/feed_images/MySNS_{hashlib.md5(upload_user.email.encode('utf-8')).hexdigest()}}_{round(time.time() * 10000)}{file_extensions}"
                
                image_body = image.stream.read()
                
                aws_s3\
                    .Bucket(current_app.config['AWS_S3_BUCKET_NAME'])\
                    .put_object(Key=s3_file_name, Body=image_body)
                
                aws_s3\
                    .ObjectAcl().put(current_app.config['AWS_S3_BUCKET_NAME'], s3_file_name)\
                    .put(ACL='public-read')
            
        
        return {
            'code' : 200,
            'message' : '게시글 등록 성공',
            'data' : {
                'feed' : new_feed.get_data_object()
            }
        }

    @swagger.doc({
        'tags' : ['feed'],
        'description' : '모든 게시글 목록 조회',
        'parameters' : [
            
        ],
        'responses' : {
            '200' : {
                'description' : '모든 게시글 목록 조회 성공',
            },
            '400' : {
                'description' : '모든 게시글 목록 조회 실패',
            }
        }
    })            
    def get(self):
        """모든 게시글 최신순으로 조회"""
        
        # 모든 게시글을 생성일시의 역순으로 가져와라(최신순)
        feed_data_arr = Feeds.query.order_by(Feeds.created_at.desc()).all()
        
        feeds = [row.get_data_object() for row in feed_data_arr] 
        
        return {
            'code' : 200,
            'message' : '모든 게시글 조회',
            'data' : {
                'feeds' : feeds,
            }
        }