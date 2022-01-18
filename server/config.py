"""
Flask Configuration
"""

class Config(object):
    DEBUG = False
    TESTING = False
    
    # SQLAlchemy가 접속할 DB 연결 정보(URI)
    # SQLAlchemy 라이브러리가, 어떤 변수를 끌어다 쓸 지도 미리 지정되어있어서 변수이름 바꾸면 안됨!!
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://아이디:비밀번호@DB호스트주소/논리DB이름"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:admin123"+\
                            "@my-first-db2.ckcb9pt3t4a9.ap-northeast-2.rds.amazonaws.com/my_sns"
                            
    # DB 변경을 추적하는 기능 꺼두자
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # S3에 접속하기 위한 접속 정보들을 변수에 저장
    AWS_ACCESS_KEY_ID = 'AKIA2M6T2DEZLNT6VYXT'
    AWS_SECRET_ACCESS_KEY = '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'
    AWS_S3_BUCKET_NAME = 'neppplus.python.20220118.jeh'
    
class ProductionConfig(Config):
    pass

class TestConfig(Config):
    TESTING = True
    
class DebugConfig(Config):
    DEBUG = True