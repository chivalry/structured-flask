import os

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
import click
from faker import Faker
from sqlalchemy.exc import IntegrityError

from . import constants as const

bootstrap = Bootstrap()
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()


def create_app():
    """Return a configured instance of Flask."""

    app = Flask(
            __name__,
            template_folder='./templates',
            static_folder='./static'
    )

    app_settings = os.getenv('APP_SETTINGS', 'app.ProdConfig')
    app.config.from_object(app_settings)

    register_extensions(app)
    register_blueprints(app)

    from .models import User

    login_manager.login_view = 'user.login'
    login_manager.login_message = const.LOGIN_DIRECTIVE_MSG
    login_manager.login_message_category = 'danger'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()

    @app.errorhandler(401)
    def unauthorized_page(error):
        return render_template('errors/401.html'), 401

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template('errors/500.html'), 500

    @app.shell_context_processor
    def shell_context_processor():
        return {
                'app': app,
                'db': db,
                'User': User,
        }

    def __create_user(email, password):
        """Create the user record with the given information."""
        try:
            user = User(email=email, password=password)
        except IntegrityError:
            print('Error: Duplicate email address')

    def __create_fake_users(count=100):
        """Create the number of dummy users given by count.

        Returns a list of the created users for possible echoing to the user.
        """
        users = []
        fake = Faker()
        for _ in range(count):
            email = fake.email()
            password = fake.password()
            users.append((email, password))
            user = User(email=email, password=password, commit=False)
            db.session.add(user)
        db.session.commit()
        return users

    @app.cli.command()
    @click.option('-e', '--email', prompt='Email', help="The user's email address.")
    @click.option('-p', '--password', prompt='Password', help="The user's password.")
    def create_user(email, password):
        """Offer a CLI interface into creating a user."""
        __create_user(email=email, password=password)

    @app.cli.command()
    @click.option('-c', '--count', default=100,
                  help='The number of fake users to create. Defaults to 100')
    @click.option('--no-echo', is_flag=True, default=False,
                  help='If passed, suppressed record output')
    def create_fake_users(count, no_echo):
        """Create the indicated number of fake users and output their emails and passwords."""
        users = __create_fake_users(count=count)
        if not no_echo:
            for user in users:
                print('{}: {}'.format(user[0], user[1]))

    @app.cli.command()
    def create_fake_data():
        """Create dummy records in the database."""
        __create_fake_users()

    return app


def register_extensions(app):
    """Conditionally register the extensions."""
    try:
        from flask_debugtoolbar import DebugToolbarExtension
        DebugToolbarExtension(app)
    except NameError:
        pass
    bootstrap.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)


def register_blueprints(app):
    """Register the blueprints."""
    from .main.views import main_blueprint
    from .user.views import user_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint)
