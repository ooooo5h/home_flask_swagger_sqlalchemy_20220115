from ast import arg
from flask import current_app, g
from flask_restful import Resource, reqparse
from flask_restful_swagger_2 import swagger

from server import db
from server.model import FeedReplies
from server.api.utils import token_required

post_parser = reqparse.RequestParser()
post_parser.add_argument('content', type=str, required=True, location='form')


put_parser = reqparse.RequestParser()
put_parser.add_argument('feed_reply_id', type=int, required=True, location='form')
put_parser.add_argument('content', type=str, required=True, location='form')

class FeedReply(Resource):
    
    @swagger.doc({
        'tags' : ['feed/reply'],
        'description' : '게시글에 댓글 작성하기',
        'parameters' : [
            {
                'name' : 'X-Http-Token',
                'description' : '어느 사용자가 쓴건지',
                'in' : 'header',
                'type' : 'string',  
                'required' : True
            },   
            {
                'name' : 'feed_id',
                'description' : '어느 피드에 남긴 댓글인지',
                'in' : 'path',
                'type' : 'integer',  
                'required' : True
            },        
            {
                'name' : 'content',
                'description' : '댓글 내용',
                'in' : 'formData',
                'type' : 'string',  
                'required' : True
            },
        ],
        'responses' : {
            '200' : {
                'description' : '등록 성공',
            },
            '400' : {
                'description' : '등록 실패',
            }
        }
    })    
    @token_required
    def post(self, feed_id):
        """댓글 등록하기"""            
        args = post_parser.parse_args()
        
        user = g.user
        
        # FeedReplies 객체 생성해서 데이터를 기입한 다음 db에 전달하자
        new_reply = FeedReplies()
        
        new_reply.feed_id = feed_id
        new_reply.user_id = user.id
        new_reply.content = args['content']
        
        db.session.add(new_reply)
        db.session.commit()
                        
        
        return {
            'code' : 200,
            'message' : '댓글 등록 성공',
            'data' : {
                'feed_reply' : new_reply.get_data_object()
            }
        }

    
    @swagger.doc({
        'tags' : ['feed/reply'],
        'description' : '달아둔 댓글 수정하기',
        'parameters' : [
            {
                'name' : 'X-Http-Token',
                'description' : '사용자 토큰',
                'in' : 'header',
                'type' : 'string',  
                'required' : True
            },   
            {
                'name' : 'feed_id',
                'description' : '몇번 게시글에 포함된 댓글을 수정할지',
                'in' : 'path',
                'type' : 'integer',  
                'required' : True
            },        
            {
                'name' : 'feed_reply_id',
                'description' : '몇번 댓글을 수정할지',
                'in' : 'formData',
                'type' : 'integer',  
                'required' : True
            },   
            {
                'name' : 'content',
                'description' : '수정해줄 내용',
                'in' : 'formData',
                'type' : 'string',  
                'required' : True
            },
        ],
        'responses' : {
            '200' : {
                'description' : '수정 성공',
            }
        }
    })    
    @token_required
    def put(self, feed_id):
        """댓글 수정하기"""       
        
        args = put_parser.parse_args()      
        user = g.user     
        
        # 내가 쓴 댓글이 맞는지 확인하기
        reply = FeedReplies.query.filter(FeedReplies.id == args['feed_reply_id']).first()
        
        if reply.user_id != user.id:
            return {
                'code' : 400,
                'message' : '본인이 쓴 댓글만 수정가능합니다.'
            }, 400
            
        reply.content = args['content']                
                        
        db.session.add(reply)
        db.session.commit()         

        return {
        'code' : 200,
        'message' : '임시 : 댓글 수정 성공'
    }