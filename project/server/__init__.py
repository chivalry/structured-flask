import os

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

# instantiate the extensions
toolbar = DebugToolbarExtension()
bootstrap = Bootstrap()
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()


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
    migrate.init_app(app)

    # register blueprints
    from project.server.main.views import main_blueprint
    app.register_blueprint(main_blueprint)

    from .models import User

    @app.shell_context_processor
    def shell_context_processor():
        return {
                'app': app,
                'db': db,
                'User': User,
        }

    return app
