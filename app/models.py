from datetime import datetime

from flask import current_app
from flask_login import UserMixin

from . import db, bcrypt


class AbstractModel(db.Model):
    """An abstract model with basic items required by all models."""
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<{}: "{}">'.format(self.__class__.__name__, self.id)

    @classmethod
    def count(cls):
        return db.session.query(cls.id).count()


class User(UserMixin, AbstractModel):
    """A simple user model that will support logging into the app."""
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

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(
                password, current_app.config['BCRYPT_LOG_ROUNDS']
        ).decode('utf-8')

    def __repr__(self):
        return '<User {}>'.format(self.email)

    @classmethod
    def select_by_email(cls, email):
        """Return the unique user identified by the email address."""
        return cls.query.filter_by(email=email)
