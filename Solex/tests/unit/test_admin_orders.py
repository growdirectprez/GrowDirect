import pytest
from unittest.mock import patch
from datetime import datetime, timezone
from solex.models import AdminUser, Product, Order, OrderItem, Inventory
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
def seed_order(db_session):
    from secrets import token_urlsafe
    product = Product(
        sku="ORD-P1", slug="ord-product", name="Order Product",
        price_cents=2000, description="", short_description="",
    )
    db_session.add(product)
    db_session.flush()
    db_session.add(Inventory(product_id=product.id, on_hand=10))
    now = datetime.now(timezone.utc)
    order = Order(
        public_token=token_urlsafe(8),
        customer_email="cust@example.com",
        customer_name="Test Customer",
        shipping_address_json={"line1": "123 Main St"},
        billing_address_json={"line1": "123 Main St"},
        subtotal_cents=2000,
        tax_cents=0,
        shipping_cents=0,
        total_cents=2000,
        status="paid",
        square_order_id="sq_order_test",
        square_payment_id="sq_pay_test",
        placed_at=now,
    )
    db_session.add(order)
    db_session.flush()
    db_session.add(OrderItem(
        order_id=order.id,
        product_id=product.id,
        sku_snapshot="ORD-P1",
        name_snapshot="Order Product",
        image_path_snapshot="",
        price_snapshot_cents=2000,
        qty=1,
        line_total_cents=2000,
    ))
    db_session.commit()
    return order.id


def test_orders_list_renders(admin_client):
    resp = admin_client.get("/admin/orders/")
    assert resp.status_code == 200
    assert b"Orders" in resp.data


def test_order_detail_renders(admin_client, seed_order):
    order_id = seed_order
    resp = admin_client.get(f"/admin/orders/{order_id}")
    assert resp.status_code == 200
    assert b"cust@example.com" in resp.data


def test_issue_refund(admin_client, seed_order):
    order_id = seed_order
    with patch("solex.services.square_client.SquareClient.create_refund") as mock_refund:
        mock_refund.return_value = {"id": "sqr_test"}
        resp = admin_client.post(f"/admin/orders/{order_id}/refund", data={
            "amount_cents": "2000",
            "reason": "customer request",
        }, follow_redirects=True)
    assert resp.status_code == 200
    assert b"Refund issued" in resp.data


def test_orders_list_redirects_unauthenticated(client):
    resp = client.get("/admin/orders/")
    assert resp.status_code in (302, 401)


def test_orders_list_scenario_tag_filter(admin_client, db_session):
    from secrets import token_urlsafe
    from datetime import datetime, timezone
    from solex.models import Product, Order, Inventory

    product = Product(
        sku="TAG-P1", slug="tag-product", name="Tag Product",
        price_cents=500, description="", short_description="",
    )
    db_session.add(product)
    db_session.flush()
    db_session.add(Inventory(product_id=product.id, on_hand=10))
    now = datetime.now(timezone.utc)

    def _make_order(tag):
        o = Order(
            public_token=token_urlsafe(8),
            customer_email="cust@example.com",
            customer_name="Test Customer",
            shipping_address_json={"line1": "1 Main"},
            billing_address_json={"line1": "1 Main"},
            subtotal_cents=500, tax_cents=0, shipping_cents=0, total_cents=500,
            status="paid",
            square_order_id=f"sq_{token_urlsafe(4)}",
            square_payment_id=f"sp_{token_urlsafe(4)}",
            placed_at=now,
            scenario_tag=tag,
        )
        db_session.add(o)
        return o

    o1 = _make_order("alpha-run-aabbccdd")
    o2 = _make_order("beta-run-11223344")
    db_session.commit()

    # Filter by alpha tag — only o1 should appear
    resp = admin_client.get("/admin/orders/?scenario_tag=alpha-run-aabbccdd")
    assert resp.status_code == 200
    assert o1.public_token.encode() in resp.data
    assert o2.public_token.encode() not in resp.data

    # No filter — both appear
    resp_all = admin_client.get("/admin/orders/")
    assert o1.public_token.encode() in resp_all.data
    assert o2.public_token.encode() in resp_all.data
