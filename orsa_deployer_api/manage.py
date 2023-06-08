import click
from flask.cli import with_appcontext


@click.command("init")
@with_appcontext
def init():
    """Create a new admin user"""
    from orsa_deployer_api.extensions import db
    from orsa_deployer_api.models import User

    click.echo("create user")
    user = User(username="admin", email="orsa.cloud@gmail.com", password="my_password", active=True)
    db.session.add(user)
    db.session.commit()
    click.echo("created user admin")
