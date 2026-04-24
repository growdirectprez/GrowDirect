"""Tests for /account/subscriptions/* routes."""
import os
import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import patch, MagicMock
from solex.models import Customer, Subscription, Product, Category
from solex.services.auth import AuthService


def _login_customer(client, db_session, email="sub@ex.com"):
    c = Customer(email=email)
    db_session.add(c)
    db_session.flush()
    token = AuthService(db_session).issue_magic_link("customer", c.id)
    db_session.commit()
    client.get(f"/account/login/magic/{token}")
    return c


def _make_product(db_session, suffix="") -> Product:
    slug_suffix = suffix or "001"
    cat = Category(name=f"Test{slug_suffix}", slug=f"test-cat-{slug_suffix}")
    db_session.add(cat)
    db_session.flush()
    p = Product(
        category_id=cat.id,
        name=f"Test Product {slug_suffix}",
        slug=f"test-product-{slug_suffix}",
        sku=f"SKU-{slug_suffix}",
        price_cents=2000,
        description="desc",
        active=True,
    )
    db_session.add(p)
    db_session.flush()
    return p


def _make_sub(db_session, customer_id, product_id, status="active") -> Subscription:
    s = Subscription(
        customer_id=customer_id,
        product_id=product_id,
        qty=1,
        cadence_days=30,
        square_card_id="card_test_001",
        next_charge_at=datetime.now(timezone.utc) + timedelta(days=30),
        status=status,
    )
    db_session.add(s)
    db_session.commit()
    return s


def test_subs_list_redirects_anonymous(client):
    resp = client.get("/account/subscriptions/", follow_redirects=False)
    assert resp.status_code in (302, 308, 401)


def test_subs_list_empty(client, db_session):
    _login_customer(client, db_session)
    resp = client.get("/account/subscriptions/")
    assert resp.status_code == 200
    assert b"No subscriptions" in resp.data


def test_cannot_view_another_customers_subscription(client, db_session):
    a = _login_customer(client, db_session, email="asub@ex.com")
    b = Customer(email="bsub@ex.com")
    db_session.add(b)
    db_session.flush()
    db_session.commit()
    p = _make_product(db_session, "view")
    s = _make_sub(db_session, b.id, p.id)
    resp = client.get(f"/account/subscriptions/{s.id}")
    assert resp.status_code == 404


def test_cancel_own_subscription(client, db_session):
    c = _login_customer(client, db_session, email="cancel_sub@ex.com")
    p = _make_product(db_session, "cancel")
    s = _make_sub(db_session, c.id, p.id)
    with patch("solex.routes.account_subscriptions.SquareClient") as MockSq:
        MockSq.return_value = MagicMock()
        resp = client.post(f"/account/subscriptions/{s.id}/cancel",
                           follow_redirects=True)
    assert resp.status_code == 200
    assert b"cancelled" in resp.data.lower()
    db_session.refresh(s)
    assert s.status == "cancelled"


def test_pause_blocked_when_flag_off(client, db_session):
    c = _login_customer(client, db_session, email="pause_off@ex.com")
    p = _make_product(db_session, "poff")
    s = _make_sub(db_session, c.id, p.id)
    env = {k: v for k, v in os.environ.items()}
    env.pop("SOLEX_FLAG_SUB_SELFSERVE", None)
    with patch.dict(os.environ, env, clear=True):
        resp = client.post(f"/account/subscriptions/{s.id}/pause")
    assert resp.status_code == 403


def test_pause_allowed_when_flag_on(client, db_session):
    c = _login_customer(client, db_session, email="pause_on@ex.com")
    p = _make_product(db_session, "pon")
    s = _make_sub(db_session, c.id, p.id)
    with patch.dict(os.environ, {"SOLEX_FLAG_SUB_SELFSERVE": "true"}):
        with patch("solex.routes.account_subscriptions.SquareClient") as MockSq:
            MockSq.return_value = MagicMock()
            resp = client.post(f"/account/subscriptions/{s.id}/pause",
                               follow_redirects=True)
    assert resp.status_code == 200
    db_session.refresh(s)
    assert s.status == "paused"


def test_resume_blocked_when_flag_off(client, db_session):
    c = _login_customer(client, db_session, email="resume_off@ex.com")
    p = _make_product(db_session, "roff")
    s = _make_sub(db_session, c.id, p.id, status="paused")
    env = {k: v for k, v in os.environ.items()}
    env.pop("SOLEX_FLAG_SUB_SELFSERVE", None)
    with patch.dict(os.environ, env, clear=True):
        resp = client.post(f"/account/subscriptions/{s.id}/resume")
    assert resp.status_code == 403


def test_resume_allowed_when_flag_on(client, db_session):
    c = _login_customer(client, db_session, email="resume_on@ex.com")
    p = _make_product(db_session, "ron")
    s = _make_sub(db_session, c.id, p.id, status="paused")
    with patch.dict(os.environ, {"SOLEX_FLAG_SUB_SELFSERVE": "true"}):
        with patch("solex.routes.account_subscriptions.SquareClient") as MockSq:
            MockSq.return_value = MagicMock()
            resp = client.post(f"/account/subscriptions/{s.id}/resume",
                               follow_redirects=True)
    assert resp.status_code == 200
    db_session.refresh(s)
    assert s.status == "active"
