from datetime import datetime, timezone
from solex.services.scenarios import prepare_context, registry
from solex.models import ScenarioRun, Cart, CartLine


def test_cart_abandonment_cohort_creates_stale_carts(
    app, db_session, scenario_catalog, scenario_config,
):
    registry._import_all()
    run = ScenarioRun(
        scenario_name="cart_abandonment_cohort",
        params_json={"count": 4, "seed": 13, "hours_idle": 5},
        started_at=datetime.now(timezone.utc), status="running", summary_json={},
    )
    db_session.add(run)
    db_session.flush()
    ctx = prepare_context(db_session, run, config=scenario_config)
    cls = registry.get("cart_abandonment_cohort")
    summary = cls().run(ctx, cls.params_schema(count=4, seed=13, hours_idle=5))

    assert summary["attempted"] == 4
    assert len(summary["created"]) == 4

    # Carts are old
    carts = db_session.query(Cart).filter(
        Cart.session_key.like(f"{ctx.tag}-%")
    ).all()
    assert len(carts) == 4
    for c in carts:
        age = datetime.now(timezone.utc) - c.last_activity_at
        assert age.total_seconds() / 3600 > 4.5

    # Each has a line
    for c in carts:
        lines = db_session.query(CartLine).filter_by(cart_id=c.id).all()
        assert len(lines) == 1

    # And a distinct customer
    customer_ids = {c.customer_id for c in carts}
    assert len(customer_ids) == 4
