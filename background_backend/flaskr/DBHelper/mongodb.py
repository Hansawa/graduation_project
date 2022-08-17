import pymongo

from flask import current_app, g


def get_cli():
    if 'mongodb' not in g:
        g.mongoCli = pymongo.MongoClient(host=current_app.config['MONGODB_URI'])

    return g.mongoCli


def close_cli(e=None):
    cli = g.pop('mongoCli', None)

    if cli is not None:
        cli.close()


def init_app(app):
    app.teardown_appcontext(close_cli)
