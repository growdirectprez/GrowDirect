"""Tests for /account/ dashboard."""
import pytest
from solex.models import Customer
from solex.services.auth import AuthService


def _login_customer(client, db_session, email="cust@ex.com"):
    c = Customer(email=email)
    db_session.add(c)
    db_session.flush()
    token = AuthService(db_session).issue_magic_link("customer", c.id)
    db_session.commit()
    client.get(f"/account/login/magic/{token}")
    return c


def test_dashboard_redirects_anonymous(client):
    resp = client.get("/account/", follow_redirects=False)
    assert resp.status_code in (302, 401)


def test_dashboard_redirect_target_is_login(client):
    resp = client.get("/account/", follow_redirects=False)
    assert resp.status_code == 302
    assert "/account/login" in resp.headers["Location"]


def test_dashboard_authenticated(client, db_session):
    c = _login_customer(client, db_session)
    resp = client.get("/account/")
    assert resp.status_code == 200
    assert b"Hi" in resp.data


def test_dashboard_shows_email_when_no_first_name(client, db_session):
    c = _login_customer(client, db_session, email="nofirstname@ex.com")
    resp = client.get("/account/")
    assert resp.status_code == 200
    assert b"nofirstname@ex.com" in resp.data


def test_dashboard_shows_empty_state(client, db_session):
    _login_customer(client, db_session)
    resp = client.get("/account/")
    assert b"No orders yet" in resp.data
    assert b"None" in resp.data
