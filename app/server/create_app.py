import os

from flask import Flask, render_template
try:
    from flask_debugtoolbar import DebugToolbarExtension
    toolbar = DebugToolbarExtension()
except ImportError:
    pass
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager

import app.server.constants as const

# instantiate the extensions
bootstrap = Bootstrap()
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    """Return a configured instance of Flask."""

    app = Flask(
            __name__,
            template_folder='../client/templates',
            static_folder='../client/static'
    )

    app_settings = os.getenv('APP_SETTINGS', 'app.server.config.ProdConfig')
    app.config.from_object(app_settings)

    try:
        toolbar.init_app(app)
    except NameError:
        pass
    bootstrap.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.server.main.views import main_blueprint
    from app.server.user.views import user_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint)

    from app.server.models import User

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

    return app
