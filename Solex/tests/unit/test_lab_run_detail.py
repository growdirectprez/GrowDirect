import json
import uuid
from datetime import datetime, timezone

from solex.models import AdminUser, ScenarioRun
from solex.services.auth import AuthService


def _login_admin(client, db_session, email="detail-admin@solex.local"):
    u = AdminUser(email=email, active=True)
    db_session.add(u); db_session.flush()
    AuthService(db_session).set_admin_password(u, "pw")
    db_session.commit()
    client.post("/admin/login", data={"email": email, "password": "pw"})
    return u


def _seed_run(db_session, name="high_value_sale", status="succeeded", params=None):
    run = ScenarioRun(
        scenario_name=name,
        params_json=params or {"count": 2, "min_total_cents": 50000, "seed": 7},
        started_at=datetime.now(timezone.utc),
        completed_at=datetime.now(timezone.utc) if status in ("succeeded", "failed", "partial") else None,
        status=status,
        summary_json={"attempted": 2, "created": ["abc", "def"], "failed": []},
    )
    db_session.add(run); db_session.commit()
    return run


def test_run_status_endpoint_returns_json(client, db_session):
    _login_admin(client, db_session)
    run = _seed_run(db_session, status="running")
    resp = client.get(f"/admin/lab/runs/{run.id}/status.json")
    assert resp.status_code == 200
    body = json.loads(resp.data)
    assert body["status"] == "running"
    assert body["id"] == str(run.id)
    assert "completed_at" in body
    assert "summary_keys" in body and isinstance(body["summary_keys"], list)


def test_run_status_endpoint_unknown_returns_404(client, db_session):
    _login_admin(client, db_session)
    resp = client.get(f"/admin/lab/runs/{uuid.uuid4()}/status.json")
    assert resp.status_code == 404


def test_run_status_endpoint_requires_admin(client, db_session):
    run = _seed_run(db_session)
    resp = client.get(f"/admin/lab/runs/{run.id}/status.json", follow_redirects=False)
    assert resp.status_code in (302, 401)


def test_run_detail_renders_structured_summary(client, db_session):
    _login_admin(client, db_session)
    run = _seed_run(db_session)
    resp = client.get(f"/admin/lab/runs/{run.id}")
    assert resp.status_code == 200
    body = resp.data.decode()
    # Scenario metadata is surfaced (not just the name)
    assert "high_value_sale" in body
    # Description from registry
    assert "high-value transaction cluster" in body
    # Expected behaviors are listed (one of them)
    assert "min_total_cents" in body or "card-nonce-ok" in body
    # Params surfaced (count=2)
    assert "count" in body
    # Status label
    assert "succeeded" in body
    # No raw JSON dump of summary_json with the structural braces visible
    # (the rebuilt detail page renders structured panels — we don't expect to
    # see the literal '"created":' on the rendered page)
    assert '"created":' not in body, "raw summary_json dump should not appear"


def test_run_detail_no_brand_token_regressions(client, db_session):
    _login_admin(client, db_session)
    run = _seed_run(db_session)
    resp = client.get(f"/admin/lab/runs/{run.id}")
    body = resp.data.decode()
    for needle in ("text-stone-", "bg-stone-", "border-stone-"):
        assert needle not in body, f"pre-brand utility {needle!r} regressed in run_detail"
