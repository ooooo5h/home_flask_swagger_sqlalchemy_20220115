# DB의 users 테이블에 연결되는 클래스
from server import db

class Users(db.Model):
    # SQLAlchemy 라이브러리의 Model클래스를 활용
    
    # 1 : 어느 테이블을 연결할건지
    __tablename__ ='users'  # DB테이블 이름
    
    # 2 : 어떤 변수 / 어떤 컬럼 연결 명시 => 변수이름 = 컬럼 이름
    id = db.Column(db.Integer, primary_key=True)  # id라는 컬럼은 Int형이고, 기본키라고 명시
    email = db.Column(db.String(50), nullable=False, default='이메일 미입력')   # email컬럼은 50자 문구에 null불가하고, 기본값이 있다고 명시
    password = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(15))  # nullable의 기본값은 null허용
    birth_year = db.Column(db.Integer, nullable=False, default=1995)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    retired_at = db.Column(db.DateTime)
    
    # cf)Feeds테이블에서 Users로 외래키를 들고 연결을 설정한 상태
    # Users의 입장에서는 Feeds테이블에서 본인을 참조하는 row들이 여러개가 있는 상태
    my_feeds = db.relationship('Feeds')
    
    
    # 3 : 객체 -> dict로 변환하는 메쏘드(응답을 내려주는 용도)
    # 사용자 입장에서 게시글 정보가 항상 필요한건 아님
    def get_data_object(self, need_feeds=False):
        data = {
            'id' : self.id,
            'email' : self.email,
            'name' : self.name,
            'phone' : self.phone,
            'birth_year' : self.birth_year,
            'created_at' : str(self.created_at), # SQLAlchemy의 DateTime은 JSON응답 처리 불가 => str로 변환해서 리턴
            'retired_at' : str(self.retired_at) if self.retired_at else None
        }
        
        if need_feeds:
            data['my_feeds'] = [feed.get_data_object(need_writer=False) for feed in self.my_feeds]
        
        # print(f"내 게시글들 : {self.my_feeds}")
                
        return data