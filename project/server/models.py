from datetime import datetime

from flask import current_app

from project.server import db, bcrypt


class AbstractModel(db.Model):
    __abstract__= True
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<{}: "{}">'.format(self.__class__.__name__, self.id)

    @classmethod
    def select_by_id(cls, id):
        return cls.query.filter_by(id=id).first()


class User(AbstractModel):
    __tablename__ = 'users'

    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
                password, current_app.config['BCRYPT_LOG_ROUNDS']
        ).decode('utf-8')
        self.admin = admin

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def is_autneticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
