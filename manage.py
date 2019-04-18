import click
from faker import Faker
from sqlalchemy.exc import IntegrityError

from flask.cli import FlaskGroup

from app import create_app, db, User

__author__ = 'Charles Ross'
__email__ = 'chivalry@mac.com'
__copyright__ = 'Copyright 2019, Charles Ross'
__version__ = '0.0.1'

app = create_app()
cli = FlaskGroup(create_app=create_app)


def __create_user(email, password):
    """Create the user record with the given information."""
    user = User(email=email, password=password)
    db.session.add(user)
    try:
        db.session.commit()
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
        user = User(email=email, password=password)
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
def create_fake_data():
    """Create dummy records in the database."""
    __create_fake_users()


@app.cli.command()
@click.option('-c', '--count', default=100, help='The number of fake users to create.')
@click.option('--no-echo', is_flag=True, default=False, help='If passed, suppressed record output')
def create_fake_users(count, no_echo):
    """Create the indicated number of fake users and output their emails and passwords."""
    users = __create_fake_users(count=count)
    if not no_echo:
        for user in users:
            print('{}: {}'.format(user[0], user[1]))


if __name__ == '__main__':
    cli()
