from datetime import datetime, timezone
from solex.services.scenarios import registry
from solex.models import ScenarioRun, AdminUser
from solex.services.auth import AuthService


def _login_admin(client, db_session):
    u = AdminUser(email="lab-admin@solex.local", active=True)
    db_session.add(u); db_session.flush()
    AuthService(db_session).set_admin_password(u, "pw")
    db_session.commit()
    client.post("/admin/login", data={"email": u.email, "password": "pw"})
    return u


def test_lab_list_requires_admin(client):
    resp = client.get("/admin/lab/", follow_redirects=False)
    assert resp.status_code in (302, 401)


def test_lab_list_renders_with_scenarios(client, db_session):
    _login_admin(client, db_session)
    resp = client.get("/admin/lab/")
    assert resp.status_code == 200
    registry._import_all()
    # All 9 scenarios should appear
    for name in registry.all_scenarios():
        assert name.encode() in resp.data, f"{name} not in lab listing"


def test_run_form_unknown_scenario_404(client, db_session):
    _login_admin(client, db_session)
    assert client.get("/admin/lab/scenarios/bogus").status_code == 404


def test_run_form_get_renders(client, db_session):
    _login_admin(client, db_session)
    registry._import_all()
    resp = client.get("/admin/lab/scenarios/shrink_event")
    assert resp.status_code == 200
    assert b"shrink_event" in resp.data


def test_run_detail_404_for_missing(client, db_session):
    _login_admin(client, db_session)
    import uuid
    assert client.get(f"/admin/lab/runs/{uuid.uuid4()}").status_code == 404
