import pytest
from contextlib import contextmanager

from flask import template_rendered

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
def database(app):
    db.create_all()
    user = User(email=tconst.ADMIN_EMAIL, password=tconst.ADMIN_PASSWORD)
    yield db
    db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture(scope='function')
def blank_app():
    app = create_app()
    context = app.app_context()
    context.push()
    yield app
    context.pop()


@pytest.fixture(scope='function')
def runner(app):
    yield app.test_cli_runner()


@contextmanager
def captured_templates(app):
    """Use signals to capture the templates rendered for a route."""
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


def template_used(app, client, route):
    """Return True if the named template was the only one rendered by the route."""
    with captured_templates(app) as templates:
        response = client.get(route, follow_redirects=True)
        return len(templates), templates[0][0].name
