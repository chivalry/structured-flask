import pytest
from sqlalchemy.exc import IntegrityError

from app.server.models import User
import tests.test_constants as tconst

def test_incorrect_parameters(database):
    with pytest.raises(TypeError):
        user = User()


def test_duplicate_emails_prohibited(database):
    user = User(email=tconst.admin_email, password=tconst.admin_password)
    database.session.add(user)
    with pytest.raises(IntegrityError):
        database.session.commit()
