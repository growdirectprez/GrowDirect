import pytest
from datetime import datetime, timezone, timedelta
from solex.models import AdminUser, Customer, Product, Subscription
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
def seed_sub(db_session):
    cust = Customer(email="sub_cust@example.com")
    product = Product(
        sku="SUB-P1", slug="sub-product", name="Sub Product",
        price_cents=1000, description="", short_description="",
    )
    db_session.add_all([cust, product])
    db_session.flush()
    sub = Subscription(
        customer_id=cust.id,
        product_id=product.id,
        qty=1,
        cadence_days=30,
        square_card_id="sqc_test",
        next_charge_at=datetime.now(timezone.utc) + timedelta(days=30),
        status="active",
    )
    db_session.add(sub)
    db_session.commit()
    return sub.id


def test_subscriptions_list_renders(admin_client):
    resp = admin_client.get("/admin/subscriptions/")
    assert resp.status_code == 200
    assert b"Subscriptions" in resp.data


def test_subscription_detail_renders(admin_client, seed_sub):
    sid = seed_sub
    resp = admin_client.get(f"/admin/subscriptions/{sid}")
    assert resp.status_code == 200
    assert b"active" in resp.data


def test_force_pause(db_session, admin_client, seed_sub):
    sid = seed_sub
    resp = admin_client.post(f"/admin/subscriptions/{sid}/pause", follow_redirects=True)
    assert resp.status_code == 200
    assert b"Paused" in resp.data
    sub = db_session.get(Subscription, sid)
    assert sub.status == "paused"


def test_force_cancel(db_session, admin_client, seed_sub):
    sid = seed_sub
    resp = admin_client.post(f"/admin/subscriptions/{sid}/cancel", follow_redirects=True)
    assert resp.status_code == 200
    assert b"Cancelled" in resp.data
    sub = db_session.get(Subscription, sid)
    assert sub.status == "cancelled"


def test_subscriptions_redirects_unauthenticated(client):
    resp = client.get("/admin/subscriptions/")
    assert resp.status_code in (302, 401)
