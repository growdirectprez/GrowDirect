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


def test_lab_list_renders_categorized_grid(client, db_session):
    """All 5 categories appear as section headers, each with the right scenarios."""
    _login_admin(client, db_session)
    resp = client.get("/admin/lab/")
    assert resp.status_code == 200
    body = resp.data.decode()
    # 5 category section headers (human-readable forms — see template)
    expected_headers = ["Operations", "Loss prevention", "Fraud", "Customer behavior", "Subscriptions"]
    for header in expected_headers:
        assert header in body, f"category header {header!r} missing from lab list"
    # Per-category scenario placement (canonical from registry.by_category)
    expected_pairs = [
        ("Operations", "normal_retail_day"),
        ("Operations", "after_hours_burst"),
        ("Loss prevention", "shrink_event"),
        ("Fraud", "high_value_sale"),
        ("Fraud", "round_amount_cluster"),
        ("Fraud", "refund_wave"),
        ("Customer behavior", "cart_abandonment_cohort"),
        ("Customer behavior", "bulk_reseller_order"),
        ("Subscriptions", "autoship_cohort"),
    ]
    for category, scenario in expected_pairs:
        # Each scenario appears AFTER its category header in the document order
        cat_pos = body.find(category)
        scen_pos = body.find(scenario, cat_pos)
        assert cat_pos != -1 and scen_pos != -1 and scen_pos > cat_pos, (
            f"{scenario} should appear after {category} header"
        )


def test_lab_list_uses_brand_tokens_only(client, db_session):
    """No leftover pre-brand stone-* utility classes in the lab list."""
    _login_admin(client, db_session)
    resp = client.get("/admin/lab/")
    body = resp.data.decode()
    # The PR #8 stone-* sweep should have eliminated these from the lab list
    forbidden_substrings = ["text-stone-", "bg-stone-", "border-stone-"]
    for needle in forbidden_substrings:
        assert needle not in body, f"pre-brand utility class {needle!r} still present"


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
