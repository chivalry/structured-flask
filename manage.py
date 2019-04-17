import subprocess
import unittest
import sys

from flask.cli import FlaskGroup

from app.server import create_app

__author__ = 'Charles Ross'
__email__ = 'chivalry@mac.com'
__copyright__ = 'Copyright 2019, Charles Ross'
__version__ = '0.0.1'

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def create_data():
    """Create sample data."""
    pass


@cli.command()
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('app.tests', pattern='test_*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)


@cli.command()
def flake():
    """Runs flake8 on the app."""
    subprocess.run(['flake8'])


if __name__ == '__main__':
    cli()
