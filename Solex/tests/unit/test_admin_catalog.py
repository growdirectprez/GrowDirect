import pytest
from sqlalchemy import select
from solex.models import AdminUser, Product, Inventory
from solex.extensions import db as _db


@pytest.fixture()
def admin_client(app, db_session, client):
    admin = AdminUser(email="admin@test.com", active=True)
    db_session.add(admin)
    db_session.commit()
    with client.session_transaction() as sess:
        sess["_user_id"] = str(admin.id)
    return client


def test_catalog_list_renders(admin_client):
    resp = admin_client.get("/admin/catalog/")
    assert resp.status_code == 200
    assert b"Catalog" in resp.data


def test_new_product_form_renders(admin_client):
    resp = admin_client.get("/admin/catalog/new")
    assert resp.status_code == 200
    assert b"New Product" in resp.data
    assert b"starting_inventory" in resp.data


def test_create_product(app, db_session, admin_client):
    resp = admin_client.post("/admin/catalog/new", data={
        "sku": "TEST-001",
        "slug": "test-product-001",
        "name": "Test Product",
        "description": "A test product",
        "short_description": "Short desc",
        "price_cents": "1000",
        "compare_at_cents": "",
        "image_path": "",
        "weight_grams": "0",
        "category_id": "",
        "active": "on",
        "starting_inventory": "5",
    }, follow_redirects=True)
    assert resp.status_code == 200
    p = db_session.execute(
        select(Product).where(Product.slug == "test-product-001")
    ).scalar_one_or_none()
    assert p is not None
    assert p.price_cents == 1000
    inv = db_session.execute(
        select(Inventory).where(Inventory.product_id == p.id)
    ).scalar_one_or_none()
    assert inv is not None
    assert inv.on_hand == 5


def test_edit_product_form_no_starting_inventory_field(db_session, admin_client):
    p = Product(sku="TEST-002", slug="test-002", name="Test 2",
                price_cents=500, description="", short_description="")
    db_session.add(p)
    db_session.commit()

    resp = admin_client.get(f"/admin/catalog/{p.id}/edit")
    assert resp.status_code == 200
    assert b"Edit Product" in resp.data
    assert b"starting_inventory" not in resp.data


def test_catalog_list_redirects_unauthenticated(client):
    resp = client.get("/admin/catalog/")
    assert resp.status_code in (302, 401)
