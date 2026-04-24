import pytest
from sqlalchemy import text, inspect
from solex import create_app
from solex.config import TestConfig
from solex.extensions import db as _db


@pytest.fixture()
def app():
    return create_app(TestConfig)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def db_session(app):
    with app.app_context():
        yield _db.session
        _db.session.rollback()
        bind = _db.session.get_bind()
        tables = inspect(bind).get_table_names()
        for table in [t for t in tables if t != "alembic_version"]:
            _db.session.execute(text(f'TRUNCATE "{table}" CASCADE'))
        _db.session.commit()
