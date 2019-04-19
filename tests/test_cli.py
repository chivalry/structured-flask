from faker import Faker

from app import User


def test_cli_help(app, runner):
    commands = {command: app.cli.commands[command].__doc__ for command in app.cli.commands.keys()}
    for command, help_text in commands.items():
        result = runner.invoke(args=[command, '--help'])
        assert help_text[:50] in result.output  # Help text gets truncated for some reason


def test_create_user(database, runner):
    fake = Faker()
    email = fake.email()
    password = fake.password()
    user_count = User.count()
    runner.invoke(args=['create-user', '-e', email, '-p', password])
    user = User.query.filter_by(email=email)
    assert user is not None
    assert User.count() == user_count + 1


def test_create_fake_users(database, runner):
    user_count = User.count()
    count = 100
    result = runner.invoke(args=['create-fake-users', '-c', count])
    assert len(result.output.split('\n')) == count + 1  # An extra newline?
    assert User.count() == user_count + count
