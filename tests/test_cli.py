from faker import Faker

from app import User


def test_cli_help(runner):
    commands = ['create-user']
    for arg in commands:
        result = runner.invoke(args=[arg])
        assert 'Usage' in result.output
