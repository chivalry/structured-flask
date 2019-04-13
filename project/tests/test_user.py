import datetime
import unittest

from flask_login import current_user

from base import BaseTestCase
from project.server import bcrypt
from project.server.models import User
from project.server.user.forms import LoginForm


class TestUserBlueprint(BaseTestCase):
    def test_correct_login(self):
        # Ensure login behaves correctly with correct credentials.
        with self.client:
            response = self.client.post(
                    '/login',
                    data=dict(email='ad@min.com', password='admin_user'),
                    follow_redirects=True
            )
            self.assertIn(b'Welcome', response.data)
            self.assertIn(b'Logout', response.data)
            self.assertTrue(current_user.email == 'ad@min.com')
            self.assertTrue(current_user.is_active)
            self.assertEqual(response.status_code, 200)

    def test_logout_behaves_correctly(self):
        # Ensure logout behaves correctly - regarding the session.
        with self.client:
            self.client.post(
                    '/login',
                    data=dict(email='ad@min.com', password='admin_user'),
                    follow_redirects=True
            )
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn(b'You were logged out. Bye!', response.data)
            self.assertFalse(current_user.is_active)

    def test_logout_route_requires_login(self):
        # Ensure logout route requires logged in user.
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'Please log in to access this page', response.data)

    def test_validate_success_login_form(self):
        # Ensure correct data validates.
        form = LoginForm(email='ad@min.com', password='admin_user')
        self.assertTrue(form.validate())

    def test_validate_invalid_email_format(self):
        # Ensure invalid email format throws error.
        form = LoginForm(email='unknown', password='example')
        self.assertFalse(form.validate())

    def test_get_by_id(self):
        # Ensure id is correct for the currently logged in user.
        with self.client:
            self.client.post(
                    '/login',
                    data=dict(email='ad@min.com', password='admin_user'),
                    follow_redirects=True
            )
            self.assertTrue(current_user.id == 1)

    def test_registered_on_defaults_to_datetime(self):
        # Ensure registered_on is a datetime
        with self.client:
            self.client.post(
                    '/login',
                    data=dict(email='ad@min.com', password='admin_user'),
                    follow_redirects=True
            )
            user = User.query.get(1)
            self.assertIsInstance(user.timestamp, datetime.datetime)

    def test_check_password(self):
        # Ensure given password is correct after unhashing.
        user = User.query.get(1)
        self.assertTrue(bcrypt.check_password_hash(user.password, 'admin_user'))
        self.assertFalse(bcrypt.check_password_hash(user.password, 'foobar'))

    def test_validate_invalid_password(self):
        # Ensure user can't login when the password is incorrect.
        with self.client:
            response = self.client.post(
                    '/login',
                    data=dict(email='ad@min.com', password='foobar'),
                    follow_redirects=True
            )
            self.assertIn(b'Invalid email or password', response.data)

if __name__ == '__main__':
    unittest.main()
