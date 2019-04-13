import os

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension


# instantiate the extensions
toolbar = DebugToolbarExtension()

def create_app(script_info=None):

    # instantiate the app
    app = Flask(
            __name__,
            template_folder='../client/templates',
            static_folder='../client/static'
    )

    # set config
    app_settings = os.getenv('APP_SETTINGS', 'project.server.config.ProductionConfig')
    app.config.from_object(app_settings)

    toolbar.init_app(app)

    # register blueprints
    from project.server.main.views import main_blueprint
    app.register_blueprint(main_blueprint)

    return app
