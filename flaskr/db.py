import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    """ 
    get a sqlite3 db connection 
    :return g.db: a sqlite3 connection
    """
    if 'db' not in g:
        # if connection is not in g, get a connection and store in g object
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    # return a connection
    return g.db


def close_db(e=None):
    """ remove it from g object and close connection if it extists"""
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """ create tables with the schema.sql file """
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """ 
    define 'flask init-db' as commandline to call init_db.
    clear the existing data and create new tables, show success message.
    """
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """ register close_db and init_db to a application """
    # teardown_appcontext(f) registers a function to be called when the application context ends.
    app.teardown_appcontext(close_db)
    # add_command(f) add a new command that can be called with flask command
    app.cli.add_command(init_db_command)
