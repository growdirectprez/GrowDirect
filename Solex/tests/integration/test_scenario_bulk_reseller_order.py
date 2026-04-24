from datetime import datetime, timezone
from solex.services.scenarios import prepare_context, registry
from solex.models import ScenarioRun, Order


def test_bulk_reseller_order_creates_multi_line_orders(
    app, db_session, scenario_catalog, mock_square_for_scenarios, scenario_config,
):
    registry._import_all()
    run = ScenarioRun(
        scenario_name="bulk_reseller_order",
        params_json={"count": 2, "seed": 99},
        started_at=datetime.now(timezone.utc), status="running", summary_json={},
    )
    db_session.add(run); db_session.flush()
    ctx = prepare_context(db_session, run, config=scenario_config)
    cls = registry.get("bulk_reseller_order")
    summary = cls().run(ctx, cls.params_schema(count=2, seed=99))
    assert not summary["failed"], summary["failed"]
    assert summary["attempted"] == 2
    # With 25 seed products, each order has 10–25 lines (lines_per_order_min=10)
    orders = db_session.query(Order).filter_by(scenario_tag=ctx.tag).all()
    assert len(orders) == 2
    for o in orders:
        assert 10 <= len(o.items) <= 25, f"expected 10–25 lines, got {len(o.items)}"
