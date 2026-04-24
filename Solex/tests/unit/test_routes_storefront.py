import pytest
from pathlib import Path
from solex.services.catalog_import import CatalogImporter


@pytest.fixture()
def seed_catalog(app, db_session, tmp_path):
    (tmp_path / "catalog").mkdir(exist_ok=True)
    importer = CatalogImporter(
        session=db_session,
        catalog_root=Path("catalog"),
        static_root=tmp_path,
    )
    importer.import_from_yaml(Path("catalog/products.yaml"))
    # reload session to see committed rows
    db_session.expire_all()
    from solex.models import Product
    return type("Seed", (), {"products": db_session.query(Product).all()})


def test_shop_lists_products(client, seed_catalog):
    resp = client.get("/shop")
    assert resp.status_code == 200
    assert b"AO Youth" in resp.data


def test_product_detail_by_slug(client, seed_catalog):
    resp = client.get("/products/ao-youth-30")
    assert resp.status_code == 200
    assert b"AO Youth" in resp.data


def test_product_detail_404_for_missing(client, seed_catalog):
    assert client.get("/products/nope").status_code == 404


def test_home_renders(client, seed_catalog):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Solex" in resp.data
