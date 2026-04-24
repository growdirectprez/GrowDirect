import pytest
from pathlib import Path
from solex.services.catalog_import import CatalogImporter
from solex.models import Product, Category


@pytest.fixture()
def tmp_static(tmp_path):
    (tmp_path / "catalog").mkdir()
    return tmp_path


def test_imports_seed_yaml(app, db_session, tmp_static):
    importer = CatalogImporter(
        session=db_session,
        catalog_root=Path("catalog"),
        static_root=tmp_static,
    )
    counts = importer.import_from_yaml(Path("catalog/products.yaml"))
    assert counts["products"]["inserted"] == 25
    assert db_session.query(Product).count() == 25
    assert db_session.query(Category).count() == 4


def test_reimport_is_idempotent(app, db_session, tmp_static):
    importer = CatalogImporter(db_session, Path("catalog"), tmp_static)
    importer.import_from_yaml(Path("catalog/products.yaml"))
    importer.import_from_yaml(Path("catalog/products.yaml"))
    assert db_session.query(Product).count() == 25
