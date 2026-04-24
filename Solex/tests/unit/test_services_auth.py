from solex.models import AdminUser
from solex.services.auth import AuthService


def test_password_roundtrip(db_session):
    svc = AuthService(db_session)
    u = AdminUser(email="a@b.c", active=True)
    db_session.add(u)
    db_session.flush()
    svc.set_admin_password(u, "hunter2")
    assert svc.verify_admin_password("a@b.c", "hunter2") is not None
    assert svc.verify_admin_password("a@b.c", "wrong") is None
    assert svc.verify_admin_password("nobody@x.y", "anything") is None


def test_magic_link_single_use(db_session):
    svc = AuthService(db_session)
    u = AdminUser(email="m@b.c", active=True)
    db_session.add(u)
    db_session.flush()
    token = svc.issue_magic_link("admin", u.id)
    db_session.commit()
    assert svc.consume_magic_link("admin", token) is not None
    assert svc.consume_magic_link("admin", token) is None
    assert svc.consume_magic_link("admin", "bogus") is None


def test_admin_login_bad_creds(client, db_session, app):
    with app.app_context():
        u = AdminUser(email="x@y.z", active=True)
        db_session.add(u)
        db_session.flush()
        AuthService(db_session).set_admin_password(u, "secret")
        db_session.commit()
    resp = client.post("/admin/login", data={"email": "x@y.z", "password": "wrong"})
    assert resp.status_code == 401


def test_admin_login_good_creds(client, db_session, app):
    with app.app_context():
        u = AdminUser(email="x2@y.z", active=True)
        db_session.add(u)
        db_session.flush()
        AuthService(db_session).set_admin_password(u, "secret")
        db_session.commit()
    resp = client.post(
        "/admin/login",
        data={"email": "x2@y.z", "password": "secret"},
        follow_redirects=False,
    )
    assert resp.status_code == 302
