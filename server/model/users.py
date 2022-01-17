# DB의 users 테이블에 연결되는 클래스
from server import db

class Users(db.Model):
    # SQLAlchemy 라이브러리의 Model클래스를 활용
    
    # 1 : 어느 테이블을 연결할건지
    # 2 : 어떤 변수 / 어떤 컬럼 연결 명시
    # 3 : 객체 -> dict로 변환하는 메쏘드(응답을 내려주는 용도)
    pass