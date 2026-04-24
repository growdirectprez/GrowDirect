import pytest
from solex.models import AdminUser, Customer
from solex.extensions import db as _db


@pytest.fixture()
def admin_client(app, db_session, client):
    admin = AdminUser(email="admin@test.com", active=True)
    db_session.add(admin)
    db_session.commit()
    with client.session_transaction() as sess:
        sess["_user_id"] = str(admin.id)
    return client


def test_customers_list_renders(admin_client):
    resp = admin_client.get("/admin/customers/")
    assert resp.status_code == 200
    assert b"Customers" in resp.data


def test_customers_list_shows_customer(db_session, admin_client):
    cust = Customer(email="alice@example.com", first_name="Alice", last_name="Jones")
    db_session.add(cust)
    db_session.commit()
    resp = admin_client.get("/admin/customers/")
    assert resp.status_code == 200
    assert b"alice@example.com" in resp.data


def test_customers_redirects_unauthenticated(client):
    resp = client.get("/admin/customers/")
    assert resp.status_code in (302, 401)
