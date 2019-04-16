import pytest

from project.server import create_app, db


@pytest.fixture
def app():
    app = create_app()
    app.config.from_object('project.server.config.TestConfig')
    yield app


@pytest.fixture
def client(app):
    with app.app_context():
        db.create_all()
    client = app.test_client()
    yield client
