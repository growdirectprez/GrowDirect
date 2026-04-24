"""Tests for checkout routes (Task 6.3)."""
import pytest
from solex.models import Order
from datetime import datetime, timezone


def test_checkout_empty_cart_renders_empty(client):
    """GET /checkout with no cart key returns the empty cart page."""
    resp = client.get("/checkout")
    assert resp.status_code == 200
    data = resp.data.lower()
    assert b"empty" in data or b"shop now" in data


def test_order_confirmation_404_for_missing(client):
    """GET /order/<bogus-token> returns 404."""
    assert client.get("/order/bogustoken").status_code == 404


def test_order_confirmation_renders_for_existing(client, db_session, app):
    """GET /order/<token> renders confirmation page for a real order."""
    order = Order(
        public_token="tok-test-abc",
        customer_email="a@b.c",
        customer_name="Test User",
        shipping_address_json={"region": "CA"},
        billing_address_json={"region": "CA"},
        subtotal_cents=1000,
        tax_cents=0,
        shipping_cents=500,
        total_cents=1500,
        status="paid",
        square_order_id="sq_order_test",
        square_payment_id="sq_pay_test",
        placed_at=datetime.now(timezone.utc),
    )
    with app.app_context():
        db_session.add(order)
        db_session.commit()

    resp = client.get("/order/tok-test-abc")
    assert resp.status_code == 200
    assert b"tok-test-abc" in resp.data


def test_submit_empty_cart_returns_400(client):
    """POST /checkout/submit with no cart returns 400."""
    resp = client.post(
        "/checkout/submit",
        json={
            "email": "a@b.c",
            "name": "A B",
            "payment_token": "cnon:test",
            "shipping_address": {"region": "CA"},
        },
    )
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "empty_cart"
