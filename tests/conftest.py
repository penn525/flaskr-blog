import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql')) as f:
    _data_sql = f.read()


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)
    print('before yielf')
    yield app
    print('after yielf')
    os.close(db_fd)
    os.unlink(db_path)
    print('tests all end')


@pytest.fixture
def client(app):
    print('client')
    return app.test_client()


@pytest.fixture
def runner(app):
    print('runner')
    return app.test_cli_runner()
