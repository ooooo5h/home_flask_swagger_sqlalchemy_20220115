from server import db

class Lectures(db.Model):
    __tablename__ = 'lectures'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    campus = db.Column(db.String(10), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    fee = db.Column(db.Integer, nullable=False, default=0)
    teacher = db.relationship('Users')
    
    feeds = db.relationship('Feeds', backref='lecture')
    
    def get_data_object(self, need_teacher_info=False):
        data = {
            'id' : self.id,
            'title' : self.title,
            'campus' : self.campus,
            'fee' : self.fee,
            'teacher_id' : self.teacher_id,
        }
        
        if need_teacher_info:
            data['teacher'] = self.teacher.get_data_object()
        
        return data