"""Tests for /account/orders/* routes."""
import pytest
from datetime import datetime, timezone
from solex.models import Customer, Order
from solex.services.auth import AuthService


def _login_customer(client, db_session, email="cust@ex.com"):
    c = Customer(email=email)
    db_session.add(c)
    db_session.flush()
    token = AuthService(db_session).issue_magic_link("customer", c.id)
    db_session.commit()
    client.get(f"/account/login/magic/{token}")
    return c


def _make_order(db_session, customer_id, token="tok123"):
    o = Order(
        customer_id=customer_id,
        public_token=token,
        customer_email="cust@ex.com",
        customer_name="Test Customer",
        shipping_address_json={
            "first_name": "Test", "last_name": "Customer",
            "line1": "123 Main St", "city": "Anytown",
            "region": "CA", "postal_code": "90210", "country": "US",
        },
        billing_address_json={
            "first_name": "Test", "last_name": "Customer",
            "line1": "123 Main St", "city": "Anytown",
            "region": "CA", "postal_code": "90210", "country": "US",
        },
        subtotal_cents=1000,
        tax_cents=100,
        shipping_cents=695,
        total_cents=1795,
        square_order_id=f"sq_order_{token}",
        square_payment_id=f"sq_pay_{token}",
        placed_at=datetime.now(timezone.utc),
        status="paid",
    )
    db_session.add(o)
    db_session.commit()
    return o


def test_orders_list_redirects_anonymous(client):
    resp = client.get("/account/orders/", follow_redirects=False)
    assert resp.status_code in (302, 308, 401)


def test_orders_list_authenticated(client, db_session):
    c = _login_customer(client, db_session)
    resp = client.get("/account/orders/")
    assert resp.status_code == 200


def test_orders_list_shows_own_order(client, db_session):
    c = _login_customer(client, db_session)
    o = _make_order(db_session, c.id, token="mytoken001")
    resp = client.get("/account/orders/")
    assert resp.status_code == 200
    assert b"mytoken001" in resp.data


def test_order_detail_authenticated(client, db_session):
    c = _login_customer(client, db_session)
    o = _make_order(db_session, c.id, token="dettoken1")
    resp = client.get(f"/account/orders/{o.id}")
    assert resp.status_code == 200
    assert b"dettoken1" in resp.data


def test_cannot_view_another_customers_order(client, db_session):
    a = _login_customer(client, db_session, email="a@ex.com")
    b = Customer(email="b@ex.com")
    db_session.add(b)
    db_session.flush()
    o = _make_order(db_session, b.id, token="btok001")
    resp = client.get(f"/account/orders/{o.id}")
    assert resp.status_code == 404


def test_return_form_own_order(client, db_session):
    c = _login_customer(client, db_session)
    o = _make_order(db_session, c.id, token="retformtok")
    resp = client.get(f"/account/orders/{o.id}/return")
    assert resp.status_code == 200
    assert b"return" in resp.data.lower()


def test_return_form_another_customers_order_404(client, db_session):
    a = _login_customer(client, db_session, email="aa@ex.com")
    b = Customer(email="bb@ex.com")
    db_session.add(b)
    db_session.flush()
    o = _make_order(db_session, b.id, token="abtok002")
    resp = client.get(f"/account/orders/{o.id}/return")
    assert resp.status_code == 404


def test_request_return_requires_reason(client, db_session):
    c = _login_customer(client, db_session)
    o = _make_order(db_session, c.id, token="reatoken1")
    resp = client.post(f"/account/orders/{o.id}/return",
                       data={"reason": ""},
                       follow_redirects=True)
    assert resp.status_code == 200
    assert b"describe the issue" in resp.data.lower() or b"Please describe" in resp.data


def test_cannot_post_return_for_another_customers_order(client, db_session):
    a = _login_customer(client, db_session, email="aaa@ex.com")
    b = Customer(email="bbb@ex.com")
    db_session.add(b)
    db_session.flush()
    o = _make_order(db_session, b.id, token="xreturntok")
    resp = client.post(f"/account/orders/{o.id}/return",
                       data={"reason": "damaged"})
    assert resp.status_code == 404
