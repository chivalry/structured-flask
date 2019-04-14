import datetime
import unittest

from flask_login import current_user

from project.tests.base import BaseTestCase
from project.server import bcrypt
from project.server.models import User
from project.server.user.forms import LoginForm
import project.server.constants as const


class TestUserBlueprint(BaseTestCase):
    def log_in(self, email=None, password=None):
        email = email or self.admin_email
        password = password or self.admin_password
        return self.client.post(
                '/login',
                data=dict(email=email, password=password),
                follow_redirects=True
        )

    def test_correct_login(self):
        with self.client:
            response = self.log_in()
            self.assertIn(b'Logout', response.data)
            self.assertTrue(current_user.email == self.admin_email)
            self.assertTrue(current_user.is_active)
            self.assertEqual(response.status_code, 200)

    def test_logout_behaves_correctly(self):
        with self.client:
            self.log_in()
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn(const.LOGOUT_SUCCESS_MSG, str(response.data))
            self.assertFalse(current_user.is_active)

    def test_logout_route_requires_login(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(self.create_app().login_manager.login_message, str(response.data))

    def test_validate_success_login_form(self):
        form = LoginForm(email=self.admin_email, password=self.admin_password)
        self.assertTrue(form.validate())

    def test_validate_invalid_email_format(self):
        form = LoginForm(email='unknown', password='example')
        self.assertFalse(form.validate())

    def test_get_by_id(self):
        with self.client:
            self.log_in()
            self.assertTrue(current_user.id == 1)

    def test_registered_on_defaults_to_datetime(self):
        with self.client:
            self.log_in()
            user = User.query.get(1)
            self.assertIsInstance(user.timestamp, datetime.datetime)

    def test_check_password(self):
        user = User.query.get(1)
        self.assertTrue(bcrypt.check_password_hash(user.password, self.admin_password))
        self.assertFalse(bcrypt.check_password_hash(user.password, 'foobar'))

    def test_validate_invalid_password(self):
        with self.client:
            response = self.log_in(password='foobar')
            self.assertIn(const.LOGIN_FAILURE_MSG, str(response.data))


if __name__ == '__main__':
    unittest.main()
