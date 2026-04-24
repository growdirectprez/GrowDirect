"""
Visual smoke tests — every branded route must return 200.
These tests use a seed_25 fixture that loads all 25 SKUs from the real
products.yaml so product-detail and category paths resolve correctly.
"""
import pytest
from pathlib import Path
from solex import create_app
from solex.config import TestConfig
from solex.extensions import db as _db
from sqlalchemy import text, inspect


@pytest.fixture(scope="module")
def smoke_app():
    app = create_app(TestConfig)
    with app.app_context():
        yield app


@pytest.fixture(scope="module")
def seed_25(smoke_app):
    """Import all 25 SKUs from catalog/products.yaml into the test DB."""
    from solex.services.catalog_import import CatalogImporter
    import tempfile, shutil

    with smoke_app.app_context():
        # Truncate catalog tables before seeding
        bind = _db.session.get_bind()
        tables = inspect(bind).get_table_names()
        for t in ["inventory", "product", "category"]:
            if t in tables:
                _db.session.execute(text(f'TRUNCATE "{t}" CASCADE'))
        _db.session.commit()

        with tempfile.TemporaryDirectory() as tmp:
            importer = CatalogImporter(
                session=_db.session,
                catalog_root=Path("catalog"),
                static_root=Path(tmp),
            )
            importer.import_from_yaml(Path("catalog/products.yaml"))
            _db.session.commit()

        yield

        # Teardown — leave clean for other suites
        for t in ["inventory", "product", "category"]:
            if t in tables:
                _db.session.execute(text(f'TRUNCATE "{t}" CASCADE'))
        _db.session.commit()


@pytest.fixture(scope="module")
def client(smoke_app, seed_25):
    return smoke_app.test_client()


# ── Storefront core paths ──────────────────────────────────────────────────

def test_home(client):
    resp = client.get("/")
    assert resp.status_code == 200


def test_shop(client):
    resp = client.get("/shop")
    assert resp.status_code == 200


def test_search(client):
    resp = client.get("/search?q=ao")
    assert resp.status_code == 200


def test_cart(client):
    resp = client.get("/cart")
    assert resp.status_code == 200


# ── Category paths ─────────────────────────────────────────────────────────

@pytest.mark.parametrize("slug", ["supplements", "devices", "therapy", "pet"])
def test_category_page(client, slug):
    resp = client.get(f"/shop/{slug}")
    assert resp.status_code == 200


# ── Product detail — 4 representative SKUs ────────────────────────────────

@pytest.mark.parametrize("slug", [
    "ao-youth-30",       # supplements
    "ao-scan-v1",        # devices
    "ao-infinity-mat",   # therapy
    "pet-gut-60",        # pet
])
def test_product_detail(client, slug):
    resp = client.get(f"/products/{slug}")
    assert resp.status_code == 200


# ── Static pages (all 9) ──────────────────────────────────────────────────

@pytest.mark.parametrize("slug", [
    "about", "events", "university", "blog", "resources",
    "privacy", "refunds", "shipping", "terms",
])
def test_static_page(client, slug):
    resp = client.get(f"/{slug}")
    assert resp.status_code == 200


# ── Content assertions ────────────────────────────────────────────────────

def test_home_hero_copy(client):
    resp = client.get("/")
    body = resp.data.decode()
    assert "Frequency" in body
    assert "Wellness" in body or "wellness" in body.lower()


def test_shop_shows_all_categories(client):
    resp = client.get("/shop")
    body = resp.data.decode()
    assert "Supplements" in body
    assert "Frequency Devices" in body
    assert "Light" in body          # "Light & PEMF Therapy"
    assert "Pet" in body
