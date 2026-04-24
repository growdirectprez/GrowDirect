"""Tests for /account/addresses/* routes."""
import pytest
from solex.models import Customer, Address
from solex.services.auth import AuthService


def _login_customer(client, db_session, email="addr@ex.com"):
    c = Customer(email=email)
    db_session.add(c)
    db_session.flush()
    token = AuthService(db_session).issue_magic_link("customer", c.id)
    db_session.commit()
    client.get(f"/account/login/magic/{token}")
    return c


_VALID_ADDR = dict(
    first_name="Jane", last_name="Doe",
    line1="100 Main St", city="Anytown",
    region="CA", postal_code="90210", country="US",
)


def test_addresses_redirects_anonymous(client):
    resp = client.get("/account/addresses/", follow_redirects=False)
    assert resp.status_code in (302, 308, 401)


def test_addresses_list_empty(client, db_session):
    _login_customer(client, db_session)
    resp = client.get("/account/addresses/")
    assert resp.status_code == 200
    assert b"No addresses" in resp.data


def test_create_address(client, db_session):
    c = _login_customer(client, db_session)
    resp = client.post("/account/addresses/", data=_VALID_ADDR, follow_redirects=True)
    assert resp.status_code == 200
    assert b"Address added" in resp.data
    from sqlalchemy import select
    from solex.extensions import db
    addrs = db.session.execute(
        select(Address).where(Address.customer_id == c.id)
    ).scalars().all()
    assert len(addrs) == 1
    assert addrs[0].city == "Anytown"


def test_create_address_missing_required_field(client, db_session):
    _login_customer(client, db_session)
    data = dict(_VALID_ADDR)
    del data["city"]
    resp = client.post("/account/addresses/", data=data, follow_redirects=True)
    assert resp.status_code == 200
    assert b"required fields" in resp.data.lower()


def test_delete_own_address(client, db_session):
    c = _login_customer(client, db_session)
    addr = Address(customer_id=c.id, **_VALID_ADDR)
    db_session.add(addr)
    db_session.commit()
    resp = client.post(f"/account/addresses/{addr.id}/delete", follow_redirects=True)
    assert resp.status_code == 200
    assert b"Address deleted" in resp.data


def test_cannot_delete_another_customers_address(client, db_session):
    a = _login_customer(client, db_session, email="a_addr@ex.com")
    b = Customer(email="b_addr@ex.com")
    db_session.add(b)
    db_session.flush()
    addr = Address(customer_id=b.id, **_VALID_ADDR)
    db_session.add(addr)
    db_session.commit()
    resp = client.post(f"/account/addresses/{addr.id}/delete")
    assert resp.status_code == 404
