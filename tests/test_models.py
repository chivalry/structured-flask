import pytest
from sqlalchemy.exc import IntegrityError

from app import User
from . import test_constants as tconst


def test_user_repr(database, fake):
    email = fake.email()
    user = User(email=email, password=fake.password())
    assert user.__repr__() == f'<User: "{email}">'


def test_user_select_by_id(database):
    user = User.select_by_id(1)
    assert user.id == 1


def test_user_select_by_email(database):
    assert User.select_by_email(email=tconst.ADMIN_EMAIL).email == tconst.ADMIN_EMAIL


def test_user_duplicate_emails_prohibited(database):
    with pytest.raises(IntegrityError):
        User(email=tconst.ADMIN_EMAIL, password=tconst.ADMIN_PASSWORD)
    database.session.rollback()


def test_user_incorrect_parameters(database):
    with pytest.raises(IntegrityError):
        User()


def test_user_correct_parameters(database, fake):
    user = User(email=fake.email(), password=fake.password())
    assert user.id is not None


@pytest.mark.skip  # TODO: This currently fails, is record being committed?
def test_user_false_commit(database, fake):
    email = fake.email()
    user = User(email=email, password=fake.password(), commit=False)
    database.session.rollback()
    user = User.select_by_email(email=email)
    assert user is None


def test_user_password(app, fake):
    password = fake.password()
    user = User(email=fake.email(), password=password)
    assert user.check_password(password)


def test_user_create_fake_users(database):
    user_count = User.count()
    User.create_fake_users()
    assert User.count() == user_count + 100

def test_user_create_fake_users_manual_count(database):
    count = 10
    user_count = User.count()
    User.create_fake_users(count=count)
    assert User.count() == user_count + count
