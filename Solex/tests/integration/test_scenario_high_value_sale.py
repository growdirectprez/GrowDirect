from datetime import datetime, timezone
from solex.services.scenarios import prepare_context, registry
from solex.models import ScenarioRun, Order


def test_high_value_sale_totals_exceed_threshold(
    app, db_session, scenario_catalog, mock_square_for_scenarios, scenario_config,
):
    registry._import_all()
    run = ScenarioRun(
        scenario_name="high_value_sale",
        params_json={"count": 2, "seed": 55},
        started_at=datetime.now(timezone.utc),
        status="running", summary_json={},
    )
    db_session.add(run); db_session.flush()
    ctx = prepare_context(db_session, run, config=scenario_config)
    cls = registry.get("high_value_sale")
    summary = cls().run(ctx, cls.params_schema(count=2, seed=55))
    assert not summary["failed"], summary["failed"]
    assert summary["attempted"] == 2
    assert len(summary["created"]) == 2
    for oid in summary["created"]:
        order = db_session.get(Order, oid)
        assert order.total_cents >= 50000, (
            f"order {oid} total {order.total_cents} is below $500"
        )
