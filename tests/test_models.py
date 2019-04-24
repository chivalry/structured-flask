import pytest
from sqlalchemy.exc import IntegrityError

from app import User
from . import test_constants as tconst


def test_incorrect_parameters(database):
    with pytest.raises(TypeError):
        user = User()  # noqa F841


def test_duplicate_emails_prohibited(database):
    with pytest.raises(IntegrityError):
        User(email=tconst.ADMIN_EMAIL, password=tconst.ADMIN_PASSWORD)
