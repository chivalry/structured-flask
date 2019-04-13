import subprocess

from flask.cli import FlaskGroup

from project.server import create_app

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def flake():
    """Runs flake8 on the project."""
    subprocess.run(['flake8'])

if __name__ == '__main__':
    cli()
