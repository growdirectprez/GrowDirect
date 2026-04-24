import pytest
from pathlib import Path
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


@pytest.fixture()
def seed_catalog(app, db_session, tmp_path):
    from solex.services.catalog_import import CatalogImporter
    (tmp_path / "catalog").mkdir(exist_ok=True)
    importer = CatalogImporter(
        session=db_session,
        catalog_root=Path("catalog"),
        static_root=tmp_path,
    )
    importer.import_from_yaml(Path("catalog/products.yaml"))
    db_session.expire_all()
    from solex.models import Product
    return type("Seed", (), {"products": db_session.query(Product).all()})
