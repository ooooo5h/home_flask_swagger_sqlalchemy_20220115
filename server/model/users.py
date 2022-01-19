# DB의 users 테이블에 연결되는 클래스
from server import db
import hashlib

class Users(db.Model):
    # SQLAlchemy 라이브러리의 Model클래스를 활용
    
    # 1 : 어느 테이블을 연결할건지
    __tablename__ ='users'  # DB테이블 이름
    
    # 2 : 어떤 변수 / 어떤 컬럼 연결 명시 => 변수이름 = 컬럼 이름
    id = db.Column(db.Integer, primary_key=True)  # id라는 컬럼은 Int형이고, 기본키라고 명시
    email = db.Column(db.String(50), nullable=False, default='이메일 미입력')   # email컬럼은 50자 문구에 null불가하고, 기본값이 있다고 명시
    password_hashed = db.Column(db.String(32), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(15))  # nullable의 기본값은 null허용
    birth_year = db.Column(db.Integer, nullable=False, default=1995)
    
    profile_img_url = db.Column(db.String(200))  
    
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    retired_at = db.Column(db.DateTime)
    
    # cf)Feeds테이블에서 Users로 외래키를 들고 연결을 설정한 상태
    # Users의 입장에서는 Feeds테이블에서 본인을 참조하는 row들이 여러개가 있는 상태
    my_feeds = db.relationship('Feeds', backref='writer')
    
    
    # 3 : 객체 -> dict로 변환하는 메쏘드(응답을 내려주는 용도)
    # 사용자 입장에서 게시글 정보가 항상 필요한건 아님
    def get_data_object(self, need_feeds=False):
        data = {
            'id' : self.id,
            'email' : self.email,
            'name' : self.name,
            'phone' : self.phone,
            'birth_year' : self.birth_year,
            'profile_img_url' : f"https://s3.ap-northeast-2.amazonaws.com/neppplus.python.20220118.jeh/{self.profile_img_url}" if self.profile_img_url else None,   # 프사가 있따면 s3주소로 가공해서 내려주고 없다면 None을 리턴
            'created_at' : str(self.created_at), # SQLAlchemy의 DateTime은 JSON응답 처리 불가 => str로 변환해서 리턴
            'retired_at' : str(self.retired_at) if self.retired_at else None
        }
        
        if need_feeds:
            data['my_feeds'] = [feed.get_data_object(need_writer=False) for feed in self.my_feeds]
        
        # print(f"내 게시글들 : {self.my_feeds}")
                
        return data
    
    
    # 비밀번호 암호화 관련 기능들
    # 코드에서는 사용자.password=비번값 형태로 사용을 지원하고 싶음
    # 대입은 가능, 읽기는 불가 => 원문 파악 x
    @property
    def password(self):
        raise AttributeError('password변수는 쓰기 전용이라서, 조회는 불가합니다.')
        
    # password변수에 대입은 허용
    @password.setter
    def password(self, input_password):
        # password = 대입값 상황에서, 대입값을 input_password에 담아주자
        # 비밀번호 원문을 암호화를 해서 대입하자
        self.password_hashed = self.generate_password_hash(input_password)
        
        
    # 함수 추가 - 비밀번호 원문을 받아서 암호화를 해주는 함수
    def generate_password_hash(self, input_password):
        return hashlib.md5(input_password.encode('utf8')).hexdigest()
    
    # 비밀번호 원문을 받아서 비밀번호가 맞는 비밀번호인지 암호화된 값끼리 비교해보는 함수
    def verify_password(self, input_password):
        hashed_input_pw = self.generate_password_hash(input_password)  # 입력한 비밀번호를 암호화 하고
        return self.password_hashed == hashed_input_pw  # 내 암호화된 비밀번호와 들어온 암호화비밀번호가 같은지 비교