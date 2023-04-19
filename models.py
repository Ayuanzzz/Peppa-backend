import datetime

from exts import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'role': self.role, 'timestamp': self.timestamp}



class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    num = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'num': self.num, 'timestamp': self.timestamp}


class UserProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    num = db.Column(db.Integer, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    # user = relationship(User, backref='projects')
    # project = relationship(Project, backref='users')
    def to_dict(self):
        return {'id': self.id, 'user_id': self.user_id, 'project_id': self.project_id, 'num': self.num, 'level': self.level}