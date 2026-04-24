from datetime import datetime, timezone
from solex.services.scenarios import prepare_context, registry
from solex.models import ScenarioRun, Order


def test_after_hours_burst_placed_at_in_window(
    app, db_session, scenario_catalog, mock_square_for_scenarios, scenario_config,
):
    registry._import_all()
    run = ScenarioRun(
        scenario_name="after_hours_burst",
        params_json={"count": 5, "seed": 7},
        started_at=datetime.now(timezone.utc),
        status="running", summary_json={},
    )
    db_session.add(run); db_session.flush()
    ctx = prepare_context(db_session, run, config=scenario_config)
    cls = registry.get("after_hours_burst")
    summary = cls().run(ctx, cls.params_schema(count=5, seed=7))
    assert not summary["failed"]
    for oid in summary["created"]:
        order = db_session.get(Order, oid)
        assert order.placed_at.hour in (22, 23, 0, 1), order.placed_at
