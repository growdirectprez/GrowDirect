import pytest
from solex.models import AdminUser
from solex.extensions import db as _db


@pytest.fixture()
def admin_client(app, db_session, client):
    """Test client with an active admin session."""
    admin = AdminUser(email="admin@test.com", active=True)
    db_session.add(admin)
    db_session.commit()
    with client.session_transaction() as sess:
        sess["_user_id"] = str(admin.id)
    return client


def test_dashboard_redirects_unauthenticated(client):
    resp = client.get("/admin/")
    assert resp.status_code in (302, 401)


def test_dashboard_renders_for_admin(admin_client):
    resp = admin_client.get("/admin/")
    assert resp.status_code == 200
    assert b"Dashboard" in resp.data
