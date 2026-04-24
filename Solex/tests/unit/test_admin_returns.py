import pytest
from unittest.mock import patch
from datetime import datetime, timezone
from secrets import token_urlsafe
from solex.models import AdminUser, Customer, Product, Order, OrderItem, Inventory, ReturnRequest
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
def seed_return(db_session):
    cust = Customer(email="ret_cust@example.com")
    product = Product(
        sku="RET-P1", slug="ret-product", name="Return Product",
        price_cents=1500, description="", short_description="",
    )
    db_session.add_all([cust, product])
    db_session.flush()
    db_session.add(Inventory(product_id=product.id, on_hand=10))
    now = datetime.now(timezone.utc)
    order = Order(
        public_token=token_urlsafe(8),
        customer_id=cust.id,
        customer_email=cust.email,
        customer_name="Return Customer",
        shipping_address_json={"line1": "1 Test St"},
        billing_address_json={"line1": "1 Test St"},
        subtotal_cents=1500,
        tax_cents=0,
        shipping_cents=0,
        total_cents=1500,
        status="paid",
        square_order_id="sq_ret_order",
        square_payment_id="sq_ret_pay",
        placed_at=now,
    )
    db_session.add(order)
    db_session.flush()
    db_session.add(OrderItem(
        order_id=order.id,
        product_id=product.id,
        sku_snapshot="RET-P1",
        name_snapshot="Return Product",
        image_path_snapshot="",
        price_snapshot_cents=1500,
        qty=1,
        line_total_cents=1500,
    ))
    ret_req = ReturnRequest(
        order_id=order.id,
        customer_id=cust.id,
        reason="product was damaged",
        status="pending",
    )
    db_session.add(ret_req)
    db_session.commit()
    return ret_req.id


def test_returns_list_renders(admin_client):
    resp = admin_client.get("/admin/returns/")
    assert resp.status_code == 200
    assert b"Returns" in resp.data


def test_return_detail_renders(admin_client, seed_return):
    rid = seed_return
    resp = admin_client.get(f"/admin/returns/{rid}")
    assert resp.status_code == 200
    assert b"pending" in resp.data
    assert b"damaged" in resp.data


def test_approve_return(db_session, admin_client, seed_return):
    rid = seed_return
    with patch("solex.services.square_client.SquareClient.create_refund") as mock_refund:
        mock_refund.return_value = {"id": "sqr_test"}
        resp = admin_client.post(f"/admin/returns/{rid}/approve", follow_redirects=True)
    assert resp.status_code == 200
    assert b"Approved" in resp.data
    req = db_session.get(ReturnRequest, rid)
    assert req.status == "completed"
    assert req.refund_id is not None


def test_deny_return(db_session, admin_client, seed_return):
    rid = seed_return
    resp = admin_client.post(f"/admin/returns/{rid}/deny", data={
        "reason": "outside return window",
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert b"Denied" in resp.data
    req = db_session.get(ReturnRequest, rid)
    assert req.status == "denied"


def test_returns_redirects_unauthenticated(client):
    resp = client.get("/admin/returns/")
    assert resp.status_code in (302, 401)
