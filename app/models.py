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

    def add_and_commit(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def count(cls):
        return db.session.query(cls.id).count()


class User(UserMixin, AbstractModel):
    """A simple user model that will support logging into the app."""
    __tablename__ = 'users'

    email = db.Column(db.String(255), unique=True, nullable=False)
    _hash = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, admin=False, commit=True):
        self.email = email
        self.password = password
        self.admin = admin
        if commit:
            self.add_and_commit()

    def check_password(self, password):
        return bcrypt.check_password_hash(self._hash, password)

    @property
    def password(self):
        """Password is not stored, return the hash."""
        return self._hash

    @password.setter
    def password(self, password, commit=True):
        self._hash = bcrypt.generate_password_hash(
                password, current_app.config['BCRYPT_LOG_ROUNDS']
        ).decode('utf-8')
        if commit:
            self.add_and_commit()

    def __repr__(self):
        return '<User {}>'.format(self.email)

    @classmethod
    def select_by_email(cls, email):
        """Return the unique user identified by the email address."""
        return cls.query.filter_by(email=email)
