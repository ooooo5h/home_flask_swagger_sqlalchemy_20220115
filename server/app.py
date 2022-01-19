from flask import Flask
from flask_restful_swagger_2 import Api
from flask_swagger_ui import get_swaggerui_blueprint
# DB담당하는 라이브러리를 import
from flask_sqlalchemy import SQLAlchemy

# DB연결을 전담하는 변수를 만들고, import로 찾아다 쓸 수 있게 세팅
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    
    app.config.from_object(f'server.config.{config_name}')
       
    #SQL Alchemy 세팅 진행 => 플라스크에 해둔 환경설정값을 불러다가 활용
    db.init_app(app)
    
    api = Api(app, api_spec_url='/api/spec', title='은형이의 SNS Server 기능 명세', api_version='0.1', catch_all_404s=True)
    

    from server.api.user import User, UserProfileImage, UserEmailFind
    from server.api.lecture import Lecture, LectureDetail
    from server.api.feed import Feed, FeedReply
    
    api.add_resource(User, '/user')
    api.add_resource(UserProfileImage, '/user/profile')
    api.add_resource(UserEmailFind, '/user/find')
    api.add_resource(Lecture, '/lecture') 
    api.add_resource(LectureDetail, '/lecture/<int:lecture_id>')  # 자료형 기재해야함
    api.add_resource(Feed, '/feed')
    api.add_resource(FeedReply, '/feed/<int:feed_id>/reply')

    
    swagger_ui = get_swaggerui_blueprint('/api/docs', '/api/spec.json', config={'app_name' : 'my sns service'})
    app.register_blueprint(swagger_ui, url_prefix='/api/docs')
    
    
    return app