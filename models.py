from datetime import datetime

from exts import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)
    employed = db.Column(db.Integer, default=1)
    timestamp = db.Column(db.DateTime, default=datetime.now().strftime('%Y-%m-%d'))

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'role': self.role, 'timestamp': self.timestamp}


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    num = db.Column(db.Integer,default=0)
    timestamp = db.Column(db.DateTime, default=datetime.now().strftime('%Y-%m-%d'))
    userprojects =db.relationship('UserProject',backref='project')

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'num': self.num, 'timestamp': self.timestamp}


class UserProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete='CASCADE'))
    num = db.Column(db.Integer, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    status =db.Column(db.Boolean, default=True)
    remark=db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.now())

    def to_dict(self):
        return {'id': self.id, 'user_id': self.user_id, 'project_id': self.project_id, 'num': self.num,
                'level': self.level,'status':self.status,'remark':self.remark}
