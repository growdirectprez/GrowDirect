"""Integration tests for Subscribe & Save at checkout.

All Square API calls are mocked. These tests verify the end-to-end flow
through the /cart/add and /checkout/submit routes.
"""
import uuid
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock

import pytest
from sqlalchemy import select

from solex.models import Customer, Product, Category, Order, Subscription
from solex.services.auth import AuthService


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def customer(db_session):
    c = Customer(email="sub_checkout@ex.com", first_name="Jo", last_name="Smith")
    db_session.add(c)
    db_session.commit()
    return c


@pytest.fixture()
def product(db_session):
    cat = Category(name="SubCat", slug="sub-cat")
    db_session.add(cat)
    db_session.flush()
    p = Product(
        category_id=cat.id,
        name="Autoship Product", slug="autoship-product", sku="AUTO-001",
        price_cents=3000, description="d", active=True,
    )
    db_session.add(p)
    db_session.commit()
    return p


def _login(client, db_session, customer):
    token = AuthService(db_session).issue_magic_link("customer", customer.id)
    db_session.commit()
    client.get(f"/account/login/magic/{token}")


_SUBMIT_BASE = {
    "email": "sub_checkout@ex.com",
    "name": "Jo Smith",
    "payment_token": "cnon:card-nonce-ok",
    "shipping_address": {
        "first_name": "Jo", "last_name": "Smith",
        "line1": "1 Main St", "city": "LA",
        "region": "CA", "postal_code": "90001", "country": "US",
    },
}

_SQUARE_ORDER = {"id": "sq_order_abc"}
_SQUARE_PAYMENT = {"id": "sq_pay_abc"}
_SQUARE_CUSTOMER = {"id": "sq_cust_xyz"}
_SQUARE_CARD = {"id": "sq_card_xyz"}


def _mock_square():
    """Return a mock SquareClient with plausible return values."""
    sq = MagicMock()
    sq.create_order.return_value = _SQUARE_ORDER
    sq.create_payment.return_value = _SQUARE_PAYMENT
    sq.create_customer.return_value = _SQUARE_CUSTOMER
    sq.save_card_on_file.return_value = _SQUARE_CARD
    return sq


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_subscribe_at_checkout_creates_subscription(app, client, db_session, customer, product):
    """Full happy path: login, add with cadence, checkout → Subscription created."""
    _login(client, db_session, customer)

    sq = _mock_square()
    with patch("solex.routes.checkout._square", return_value=sq):
        # Add to cart with subscription cadence
        resp = client.post("/cart/add", data={
            "product_id": str(product.id),
            "qty": "1",
            "subscription_cadence_days": "30",
        })
        assert resp.status_code == 200
        cart_data = resp.get_json()
        line = cart_data["lines"][0]
        assert line.get("cadence_days") == 30

        # Submit checkout with both tokens
        body = dict(_SUBMIT_BASE)
        body["store_payment_token"] = "cnon:store-nonce-ok"
        resp = client.post("/checkout/submit",
                           json=body,
                           content_type="application/json")

    assert resp.status_code == 200
    data = resp.get_json()
    assert "order_token" in data
    assert "subscription_next_charge" in data

    # Order committed
    order = db_session.execute(
        select(Order).where(Order.public_token == data["order_token"])
    ).scalar_one_or_none()
    assert order is not None

    # Subscription committed
    db_session.expire_all()
    subs = db_session.execute(
        select(Subscription).where(Subscription.customer_id == customer.id)
    ).scalars().all()
    assert len(subs) == 1
    assert subs[0].cadence_days == 30
    assert subs[0].square_card_id == "sq_card_xyz"
    assert subs[0].status == "active"

    # Customer square_customer_id set
    db_session.refresh(customer)
    assert customer.square_customer_id == "sq_cust_xyz"

    # Square calls made
    sq.create_customer.assert_called_once()
    sq.save_card_on_file.assert_called_once_with("sq_cust_xyz", "cnon:store-nonce-ok")


def test_subscribe_without_store_token_400(app, client, db_session, customer, product):
    """Omitting store_payment_token when cart has sub lines → 400."""
    _login(client, db_session, customer)

    sq = _mock_square()
    with patch("solex.routes.checkout._square", return_value=sq):
        client.post("/cart/add", data={
            "product_id": str(product.id),
            "qty": "1",
            "subscription_cadence_days": "30",
        })
        # No store_payment_token
        resp = client.post("/checkout/submit",
                           json=_SUBMIT_BASE,
                           content_type="application/json")

    assert resp.status_code == 400
    assert resp.get_json()["error"] == "store_payment_token_required_for_subscription"


def test_subscribe_as_guest_returns_login_required(app, client, db_session, product):
    """Guest (not logged in) with sub cart line → 400 login_required_for_subscription."""
    sq = _mock_square()
    with patch("solex.routes.checkout._square", return_value=sq):
        client.post("/cart/add", data={
            "product_id": str(product.id),
            "qty": "1",
            "subscription_cadence_days": "30",
        })
        body = dict(_SUBMIT_BASE)
        body["store_payment_token"] = "cnon:store-nonce-ok"
        resp = client.post("/checkout/submit",
                           json=body,
                           content_type="application/json")

    assert resp.status_code == 400
    assert resp.get_json()["error"] == "login_required_for_subscription"


def test_onetime_checkout_no_subscription(app, client, db_session, customer, product):
    """One-time cart line (no cadence) → no Subscription row created."""
    _login(client, db_session, customer)

    sq = _mock_square()
    with patch("solex.routes.checkout._square", return_value=sq):
        client.post("/cart/add", data={
            "product_id": str(product.id),
            "qty": "1",
            # No subscription_cadence_days
        })
        resp = client.post("/checkout/submit",
                           json=_SUBMIT_BASE,
                           content_type="application/json")

    assert resp.status_code == 200
    data = resp.get_json()
    assert "subscription_next_charge" not in data

    subs = db_session.execute(
        select(Subscription).where(Subscription.customer_id == customer.id)
    ).scalars().all()
    assert len(subs) == 0
    sq.save_card_on_file.assert_not_called()


def test_existing_square_customer_skips_create(app, client, db_session, product):
    """If customer already has square_customer_id, create_customer is not called again."""
    c = Customer(email="existing_sq@ex.com", square_customer_id="already_sq_999")
    db_session.add(c)
    db_session.commit()
    _login(client, db_session, c)

    sq = _mock_square()
    with patch("solex.routes.checkout._square", return_value=sq):
        client.post("/cart/add", data={
            "product_id": str(product.id),
            "qty": "1",
            "subscription_cadence_days": "30",
        })
        body = dict(_SUBMIT_BASE)
        body["email"] = "existing_sq@ex.com"
        body["store_payment_token"] = "cnon:store-nonce-ok"
        resp = client.post("/checkout/submit",
                           json=body,
                           content_type="application/json")

    assert resp.status_code == 200
    sq.create_customer.assert_not_called()
    sq.save_card_on_file.assert_called_once_with("already_sq_999", "cnon:store-nonce-ok")
