from faker import Faker

from app import User


def test_cli_help(runner):
    commands = ['create-user']
    for arg in commands:
        result = runner.invoke(args=[arg])
        assert 'Usage' in result.output


def test_create_user(runner, database):
    faker = Faker()
    user_count = User.count()
    runner.invoke(args=['create_user --email=fake.email(), --password=fake.password()'])
    assert user_count == User.count() - 1
