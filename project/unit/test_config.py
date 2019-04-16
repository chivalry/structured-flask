import unittest
import os

from flask import current_app
from flask_testing import TestCase

from project.server import create_app

app = create_app()


class TestDevConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.server.config.DevConfig')
        return app

    def test_app_is_dev(self):
        self.assertFalse(current_app.config['TESTING'])
        self.assertTrue(app.config['WTF_CSRF_ENABLED'] is False)
        self.assertTrue(app.config['DEBUG_TB_ENABLED'] is True)
        self.assertFalse(current_app is None)


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.server.config.TestConfig')
        return app

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
        self.assertTrue(app.config['BCRYPT_LOG_ROUNDS'] == 4)
        self.assertTrue(app.config['WTF_CSRF_ENABLED'] is False)


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.server.config.ProdConfig')
        return app

    def test_app_is_production(self):
        self.assertFalse(current_app.config['TESTING'])
        self.assertTrue(app.config['DEBUG_TB_ENABLED'] is False)
        self.assertTrue(app.config['WTF_CSRF_ENABLED'] is True)
        self.assertTrue(app.config['BCRYPT_LOG_ROUNDS'] == 13)

    def test_secret_key_has_been_set(self):
        self.assertTrue(
            app.secret_key == os.getenv('SECRET_KEY', default='not-secret')
        )


if __name__ == '__main__':
    unittest.main()
