import os

from flask import Flask, render_template, request, current_app
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_babel import Babel
import click
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException

from . import constants as const

bootstrap = Bootstrap()
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
babel = Babel()


def create_app(config=None):
    """Return a configured instance of Flask."""

    app = Flask(
            __name__,
            template_folder='./templates',
            static_folder='./static'
    )

    config = config or os.getenv('APP_SETTINGS', 'app.ProdConfig')
    app.config.from_object(config)

    register_extensions(app)
    register_blueprints(app)

    from .models import User

    login_manager.login_view = 'user.login'
    login_manager.login_message = const.LOGIN_DIRECTIVE_MSG
    login_manager.login_message_category = 'danger'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()

    @app.errorhandler(HTTPException)
    def error_handler(err):
        code = err.code
        return render_template('errors.html', err=err), code

    @app.shell_context_processor
    def shell_context_processor():
        return {
                'app': app,
                'db': db,
                'User': User,
        }

    @app.cli.command()
    @click.option('-e', '--email', prompt='Email', help="The user's email address.")
    @click.option('-p', '--password', prompt='Password', help="The user's password.")
    def create_user(email, password):
        """Offer a CLI interface into creating a user."""
        try:
            User(email=email, password=password)
        except IntegrityError:
            print('Error: Duplicate email address')

    @app.cli.command()
    @click.option('-c', '--count', default=100,
                  help='The number of fake users to create. Defaults to 100')
    @click.option('--no-echo', is_flag=True, default=False,
                  help='If passed, suppressed record output')
    def create_fake_users(count, no_echo):
        """Create the indicated number of fake users and output their emails and passwords."""
        users = User.create_fake_users(count=count)
        if not no_echo:
            for user in users:
                print(f'{user[0]}: {user[1]}')

    @app.cli.command()
    def create_fake_data():
        """Create dummy records in the database."""
        User.create_fake_users()

    return app


def register_extensions(app):
    """Conditionally register the extensions."""
    try:
        from flask_debugtoolbar import DebugToolbarExtension
        DebugToolbarExtension(app)
    except ModuleNotFoundError:
        pass
    bootstrap.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    babel.init_app(app)


def register_blueprints(app):
    """Register the blueprints."""
    from .main.views import main_blueprint
    from .user.views import user_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint)


@babel.localeselector
def get_locale():
    language = request.accept_languages.best_match(current_app.config['LANGUAGES'])
    if language:
        return language
    locales = [item[0] for item in list(request.accept_languages)]
    languages = [str[0:2] for str in locales]
    try:
        language = [lang for lang in languages if lang in current_app.config['LANGUAGES']][0]
    except IndexError:
        return 'en'
    return language
