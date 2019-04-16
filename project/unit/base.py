from flask_testing import TestCase

from project.server import db, create_app
from project.server.models import User

app = create_app()


class BaseTestCase(TestCase):
    admin_email = 'ad@min.com'
    admin_password = 'admin_user'

    def create_app(self):
        app.config.from_object('project.server.config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        user = User(email=self.admin_email, password=self.admin_password)
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
