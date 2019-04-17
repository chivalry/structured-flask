import datetime

from flask_login import current_user

from app import bcrypt, User, LoginForm
from app import constants as const
from . import test_constants as tconst


def log_in(client, email=None, password=None):
    email = email or tconst.admin_email
    password = password or tconst.admin_password
    return client.post('/login', data=dict(email=email, password=password), follow_redirects=True)


def test_correct_login(client, database):
    with client:
        response = log_in(client)
        assert 'Logout' in str(response.data)
        assert current_user.email == tconst.admin_email
        assert current_user.is_active


def test_logout_behaves_correctly(client, database):
    with client:
        log_in(client)
        response = client.get('/logout', follow_redirects=True)
        assert const.LOGOUT_SUCCESS_MSG in str(response.data)
        assert not current_user.is_active


def test_logout_route_requires_login(app, client, database):
    response = client.get('/logout', follow_redirects=True)
    assert app.login_manager.login_message in str(response.data)


def test_validate_success_login_form(app):
    form = LoginForm(email=tconst.admin_email, password=tconst.admin_password)
    assert form.validate()


def test_invalid_email_invalidates_form(app):
    form = LoginForm(email='not and email', password='example')
    assert not form.validate()


def test_first_user_has_id(client, database):
    with client:
        log_in(client)
        assert current_user.id == 1


def test_registered_on_defaults_to_datetime(client, database):
    with client:
        log_in(client)
        user = User.query.get(1)
        assert isinstance(user.timestamp, datetime.datetime)


def test_check_password(database):
    user = User.query.get(1)
    assert bcrypt.check_password_hash(user.password, tconst.admin_password)
    assert not bcrypt.check_password_hash(user.password, 'foobar')


def test_failed_loging(client, database):
    with client:
        response = log_in(client, password='foobar')
        assert const.LOGIN_FAILURE_MSG in str(response.data)
