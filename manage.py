import subprocess

from flask.cli import FlaskGroup

from project.server import create_app

__author__ = 'Charles Ross'
__email__ = 'chivalry@mac.com'
__copyright__ = 'Copyright 2019, Charles Ross'
__version__ = '0.0.1'

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def flake():
    """Runs flake8 on the project."""
    subprocess.run(['flake8'])


if __name__ == '__main__':
    cli()
