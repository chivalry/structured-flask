import click

from flask.cli import FlaskGroup

from app import create_app, db, User

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


@app.cli.command()
@click.option('-e', '--email', prompt='Email', help="The user's email address.")
@click.option('-p', '--password', prompt='Password', help="The user's password.")
def create_user(email, password):
    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    cli()
