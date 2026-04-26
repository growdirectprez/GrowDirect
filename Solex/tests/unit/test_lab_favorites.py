from datetime import datetime, timezone

from sqlalchemy import select

from solex.models import AdminUser, ScenarioRun
from solex.services.auth import AuthService


def _login_admin(client, db_session, email="fav-admin@solex.local"):
    u = AdminUser(email=email, active=True)
    db_session.add(u); db_session.flush()
    AuthService(db_session).set_admin_password(u, "pw")
    db_session.commit()
    client.post("/admin/login", data={"email": email, "password": "pw"})
    return u


def _seed_run(db_session, name="high_value_sale"):
    run = ScenarioRun(
        scenario_name=name,
        params_json={},
        started_at=datetime.now(timezone.utc),
        status="succeeded",
        summary_json={},
    )
    db_session.add(run); db_session.commit()
    return run


def test_favorite_toggle_requires_admin(client, db_session):
    run = _seed_run(db_session)
    resp = client.post(f"/admin/lab/runs/{run.id}/favorite", follow_redirects=False)
    assert resp.status_code in (302, 401)


def test_favorite_toggle_inserts_favorite_row(client, db_session):
    from solex.models import ScenarioRunFavorite  # noqa: PLC0415 — exercises new model
    admin = _login_admin(client, db_session)
    run = _seed_run(db_session)
    resp = client.post(f"/admin/lab/runs/{run.id}/favorite")
    assert resp.status_code == 204
    db_session.expire_all()
    rows = db_session.execute(
        select(ScenarioRunFavorite).where(
            ScenarioRunFavorite.admin_user_id == admin.id,
            ScenarioRunFavorite.scenario_run_id == run.id,
        )
    ).scalars().all()
    assert len(rows) == 1


def test_favorite_toggle_removes_existing_favorite(client, db_session):
    from solex.models import ScenarioRunFavorite
    admin = _login_admin(client, db_session)
    run = _seed_run(db_session)
    # First toggle inserts
    client.post(f"/admin/lab/runs/{run.id}/favorite")
    # Second toggle removes
    resp = client.post(f"/admin/lab/runs/{run.id}/favorite")
    assert resp.status_code == 204
    db_session.expire_all()
    rows = db_session.execute(
        select(ScenarioRunFavorite).where(
            ScenarioRunFavorite.admin_user_id == admin.id,
            ScenarioRunFavorite.scenario_run_id == run.id,
        )
    ).scalars().all()
    assert rows == []


def test_favorite_is_per_admin_user(client, db_session):
    from solex.models import ScenarioRunFavorite
    # Admin A favorites the run
    admin_a = _login_admin(client, db_session, email="admin-a@solex.local")
    run = _seed_run(db_session)
    client.post(f"/admin/lab/runs/{run.id}/favorite")
    # Logout, login as Admin B
    client.get("/admin/logout")
    admin_b = _login_admin(client, db_session, email="admin-b@solex.local")
    # Admin B's favorite is independent — toggling adds B's row, doesn't touch A's
    client.post(f"/admin/lab/runs/{run.id}/favorite")
    db_session.expire_all()
    a_rows = db_session.execute(
        select(ScenarioRunFavorite).where(ScenarioRunFavorite.admin_user_id == admin_a.id)
    ).scalars().all()
    b_rows = db_session.execute(
        select(ScenarioRunFavorite).where(ScenarioRunFavorite.admin_user_id == admin_b.id)
    ).scalars().all()
    assert len(a_rows) == 1
    assert len(b_rows) == 1


def test_favorite_404_for_unknown_run(client, db_session):
    import uuid
    _login_admin(client, db_session)
    resp = client.post(f"/admin/lab/runs/{uuid.uuid4()}/favorite")
    assert resp.status_code == 404
