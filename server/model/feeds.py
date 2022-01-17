from sqlite3 import dbapi2
from server import db

class Feeds(db.Model):
    __tablename__ = 'feeds'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    lecture_id = db.Column(db.Integer)  # null이면, 특정 강의에 대한 글이 아님
    content = db.Column(db.TEXT, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())