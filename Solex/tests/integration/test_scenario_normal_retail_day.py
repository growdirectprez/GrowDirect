from datetime import datetime, timezone
from solex.services.scenarios import prepare_context, registry
from solex.models import ScenarioRun, Order


def test_normal_retail_day_runs_and_tags(
    app, db_session, scenario_catalog, mock_square_for_scenarios, scenario_config,
):
    registry._import_all()
    run = ScenarioRun(
        scenario_name="normal_retail_day",
        params_json={"count": 5, "seed": 42},
        started_at=datetime.now(timezone.utc), status="running", summary_json={},
    )
    db_session.add(run); db_session.flush()

    ctx = prepare_context(db_session, run, config=scenario_config)
    cls = registry.get("normal_retail_day")
    summary = cls().run(ctx, cls.params_schema(count=5, seed=42))
    assert summary["attempted"] == 5
    assert len(summary["created"]) == 5
    assert not summary["failed"]
    orders = db_session.query(Order).filter_by(scenario_tag=ctx.tag).all()
    assert len(orders) == 5
