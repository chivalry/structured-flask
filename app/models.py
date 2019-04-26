from datetime import datetime

from flask import current_app
from flask_login import UserMixin
from faker import Faker

from . import db, bcrypt


class AbstractModel(db.Model):
    """An abstract model with basic items required by all models."""
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __init__(self, commit=True):
        self.commit = commit

    def __repr__(self):
        """Return a default __repr__ for all subclasses."""
        return '<{}: "{}">'.format(self.__class__.__name__, self.id)

    def add_and_commit(self):
        """Add the record to the session and commit it to the database."""
        if self.commit:
            db.session.add(self)
            db.session.commit()

    @classmethod
    def count(cls):
        """Return the number of records of this class in the database."""
        return db.session.query(cls.id).count()

    @classmethod
    def select_by_id(cls, id):
        return cls.query.filter_by(id=id).first()


class User(UserMixin, AbstractModel):
    """A simple user model that will support logging into the app."""
    __tablename__ = 'users'

    email = db.Column(db.String(255), unique=True, nullable=False)
    _hash = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, admin=False, commit=True):
        """Initialize the user with data.

        :param commit: If True, commits the record to the database, defaults to True
        """
        super().__init__(commit=commit)
        self.email = email
        self.password = password
        self.admin = admin
        self.add_and_commit()

    def __repr__(self):
        """Override the super class's __repr__ to show the user's email address."""
        return '<User: "{}">'.format(self.email)

    def check_password(self, password):
        """Return True if the given password matches the stored hash."""
        return bcrypt.check_password_hash(self._hash, password)

    @property
    def password(self):
        """Password is not stored, return the hash."""
        return self._hash

    @password.setter
    def password(self, password, commit=True):
        """Hash the given password and store it in the database.

        :param commit: If True, commits the record to the database, defaults to True
        """
        self.commit = commit
        self._hash = bcrypt.generate_password_hash(
                password, current_app.config['BCRYPT_LOG_ROUNDS']
        ).decode('utf-8')
        self.add_and_commit()

    @classmethod
    def select_by_email(cls, email):
        """Return the unique user identified by the email address."""
        return cls.query.filter_by(email=email).first()

    @classmethod
    def create_fake_users(cls, count=100):
        """Create the number of fake users given by count.

        Returns a list of the created users for possible echoing to a cli function.
        """
        users = []
        fake = Faker()
        for _ in range(count):
            email = fake.email()
            password = fake.password()
            users.append((email, password))
            user = cls(email=email, password=password, commit=False)
            db.session.add(user)
        db.session.commit()
        return users
