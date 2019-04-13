import os

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_login import LoginManager

# instantiate the extensions
toolbar = DebugToolbarExtension()
bootstrap = Bootstrap()
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()


def create_app():

    # instantiate the app
    app = Flask(
            __name__,
            template_folder='../client/templates',
            static_folder='../client/static'
    )

    # set config
    app_settings = os.getenv('APP_SETTINGS', 'project.server.config.ProdConfig')
    app.config.from_object(app_settings)

    toolbar.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # register blueprints
    from project.server.main.views import main_blueprint
    from project.server.user.views import user_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_blueprint)

    # flask login
    from project.server.models import User

    login_manager.login_view = 'user.login'
    login_manager.login_message_category = 'danger'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()

    @app.shell_context_processor
    def shell_context_processor():
        return {
                'app': app,
                'db': db,
                'User': User,
        }

    return app
