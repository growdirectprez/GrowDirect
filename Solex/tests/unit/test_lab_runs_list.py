from datetime import datetime, timedelta, timezone

from solex.models import AdminUser, ScenarioRun, ScenarioRunFavorite
from solex.services.auth import AuthService


def _login_admin(client, db_session, email="runs-admin@solex.local"):
    u = AdminUser(email=email, active=True)
    db_session.add(u); db_session.flush()
    AuthService(db_session).set_admin_password(u, "pw")
    db_session.commit()
    client.post("/admin/login", data={"email": email, "password": "pw"})
    return u


def _seed_runs(db_session):
    """Three runs across two scenarios + two statuses + two days."""
    now = datetime.now(timezone.utc)
    yesterday = now - timedelta(days=1)
    rows = [
        ScenarioRun(scenario_name="high_value_sale", params_json={},
                    started_at=now, status="succeeded", summary_json={}),
        ScenarioRun(scenario_name="shrink_event", params_json={},
                    started_at=now, status="failed", summary_json={"error": "x"}),
        ScenarioRun(scenario_name="high_value_sale", params_json={},
                    started_at=yesterday, status="succeeded", summary_json={}),
    ]
    for r in rows:
        db_session.add(r)
    db_session.commit()
    return rows


def test_runs_list_requires_admin(client):
    resp = client.get("/admin/lab/runs/", follow_redirects=False)
    assert resp.status_code in (302, 401)


def test_runs_list_renders_all_recent(client, db_session):
    _login_admin(client, db_session)
    runs = _seed_runs(db_session)
    resp = client.get("/admin/lab/runs/")
    assert resp.status_code == 200
    body = resp.data.decode()
    for r in runs:
        assert str(r.id) in body, f"{r.scenario_name} run {r.id} missing"


def test_runs_list_filter_by_scenario(client, db_session):
    _login_admin(client, db_session)
    runs = _seed_runs(db_session)
    resp = client.get("/admin/lab/runs/?scenario=shrink_event")
    body = resp.data.decode()
    shrink = [r for r in runs if r.scenario_name == "shrink_event"][0]
    hvs = [r for r in runs if r.scenario_name == "high_value_sale"]
    assert str(shrink.id) in body
    for r in hvs:
        assert str(r.id) not in body


def test_runs_list_filter_by_status(client, db_session):
    _login_admin(client, db_session)
    runs = _seed_runs(db_session)
    resp = client.get("/admin/lab/runs/?status=failed")
    body = resp.data.decode()
    failed = [r for r in runs if r.status == "failed"][0]
    succeeded = [r for r in runs if r.status == "succeeded"]
    assert str(failed.id) in body
    for r in succeeded:
        assert str(r.id) not in body


def test_runs_list_favorites_only(client, db_session):
    admin = _login_admin(client, db_session)
    runs = _seed_runs(db_session)
    # Favorite one run
    target = runs[0]
    db_session.add(ScenarioRunFavorite(admin_user_id=admin.id, scenario_run_id=target.id))
    db_session.commit()

    resp = client.get("/admin/lab/runs/?favorites=1")
    body = resp.data.decode()
    assert str(target.id) in body
    for r in runs[1:]:
        assert str(r.id) not in body


def test_runs_list_filter_by_date_range(client, db_session):
    _login_admin(client, db_session)
    runs = _seed_runs(db_session)
    today_iso = datetime.now(timezone.utc).date().isoformat()
    # Only today's runs (excludes yesterday's high_value_sale)
    resp = client.get(f"/admin/lab/runs/?from={today_iso}")
    body = resp.data.decode()
    today_runs = [r for r in runs if r.started_at.date() == datetime.now(timezone.utc).date()]
    yesterday_runs = [r for r in runs if r.started_at.date() != datetime.now(timezone.utc).date()]
    for r in today_runs:
        assert str(r.id) in body
    for r in yesterday_runs:
        assert str(r.id) not in body
