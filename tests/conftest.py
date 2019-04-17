import pytest

from app import create_app, db, User
from . import test_constants as tconst


@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config.from_object('app.TestConfig')
    context = app.app_context()
    context.push()
    yield app
    context.pop()


@pytest.fixture(scope='module')
def blank_app():
    app = create_app()
    context = app.app_context()
    context.push()
    yield app
    context.pop()


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture(scope='module')
def database(app):
    db.create_all()
    user = User(email=tconst.admin_email, password=tconst.admin_password)
    db.session.add(user)
    db.session.commit()
    yield db
    db.drop_all()
