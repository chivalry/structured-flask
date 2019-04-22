import datetime
import re
from urllib.parse import urlparse

from flask import g
from flask_login import current_user
import pytest

from app import bcrypt, User, LoginForm, mail
from app import constants as const
from . import test_constants as tconst


def log_in(client, email=None, password=None):
    email = email or tconst.ADMIN_EMAIL
    password = password or tconst.ADMIN_PASSWORD
    return client.post('/login', data=dict(email=email, password=password), follow_redirects=True)


@pytest.mark.usefixtures('database')
def test_correct_login(client):
    with client:
        response = log_in(client)
        assert 'Logout' in str(response.data)
        assert current_user.email == tconst.ADMIN_EMAIL
        assert current_user.is_active


def test_logout_behaves_correctly(client):
    with client:
        log_in(client)
        response = client.get('/logout', follow_redirects=True)
        assert const.LOGOUT_SUCCESS_MSG in str(response.data)
        assert not current_user.is_active


def test_logout_route_requires_login(app, client):
    response = client.get('/logout', follow_redirects=True)
    assert app.login_manager.login_message in str(response.data)


def test_validate_success_login_form():
    form = LoginForm(email=tconst.ADMIN_EMAIL, password=tconst.ADMIN_PASSWORD)
    assert form.validate()


def test_invalid_email_invalidates_form():
    form = LoginForm(email='not an email', password='example')
    assert not form.validate()


def test_first_user_has_id(client):
    with client:
        log_in(client)
        assert current_user.id == 1


def test_registered_on_defaults_to_datetime(client):
    with client:
        log_in(client)
        user = User.query.get(1)
        assert isinstance(user.timestamp, datetime.datetime)


def test_check_password(database):
    user = User.query.get(1)
    assert bcrypt.check_password_hash(user.password, tconst.ADMIN_PASSWORD)
    assert not bcrypt.check_password_hash(user.password, 'foobar')


def test_failed_login(client):
    with client:
        response = log_in(client, password='foobar')
        assert const.LOGIN_FAILURE_MSG in str(response.data)


def test_login_page_has_success_code(client):
    response = client.get('/login')
    assert response.status_code == 200


def test_form_submission_has_success_code(client):
    response = client.post('/login')
    assert response.status_code == 200


def test_reset_route(client):
    response = client.get('/login')
    assert response.status_code == 200

@pytest.mark.usefixtures('database')
def test_reset_email(client):
    with mail.record_messages() as outbox:
        response = client.post('/reset', data=dict(email=tconst.ADMIN_EMAIL),
                               follow_redirects=True)
        msg = outbox[-1]
        assert const.RESET_PASSWORD_REQUEST_FLASH in str(response.data)
        assert msg.subject == const.RESET_EMAIL_SUBJECT
        assert 'Reset Password' in msg.html
        assert 'Reset Password' in msg.body
        pattern = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        url = re.findall(pattern, msg.body)[0]
        path = urlparse(url).path
        response = client.post(path, data=dict(password='newpass'), follow_redirects=True)
        log_in(client, tconst.ADMIN_EMAIL, 'newpass')
        assert 'Logout' in str(response.data)
