import click

from flask.cli import with_appcontext

from server import db


@click.command(name='create-db')
@with_appcontext
def create_db():
    db.create_all()
    click.echo('Database tables created')
