from flask_login import current_user

import project.server.constants as const
from project.server.user.forms import LoginForm
import tests.test_constants as tconst


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
