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


@pytest.fixture()
def seed_product(db_session):
    product = Product(
        sku="INV-001", slug="inv-product", name="Inventory Product",
        price_cents=1500, description="", short_description="",
    )
    db_session.add(product)
    db_session.flush()
    db_session.add(Inventory(product_id=product.id, on_hand=20))
    db_session.commit()
    return product.id


def test_inventory_list_renders(admin_client, seed_product):
    resp = admin_client.get("/admin/inventory/")
    assert resp.status_code == 200
    assert b"Inventory" in resp.data
    assert b"Inventory Product" in resp.data


def test_inventory_adjust(db_session, admin_client, seed_product):
    pid = seed_product
    resp = admin_client.post(f"/admin/inventory/{pid}/adjust", data={
        "delta": "5",
        "reason": "restock",
        "note": "extra stock",
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert b"Adjusted" in resp.data
    inv = db_session.execute(
        select(Inventory).where(Inventory.product_id == pid)
    ).scalar_one()
    assert inv.on_hand == 25


def test_inventory_redirects_unauthenticated(client):
    resp = client.get("/admin/inventory/")
    assert resp.status_code in (302, 401)
