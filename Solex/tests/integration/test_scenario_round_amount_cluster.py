from datetime import datetime, timezone
from solex.services.scenarios import prepare_context, registry
from solex.models import ScenarioRun, Order


def test_round_amount_cluster_totals_are_round(
    app, db_session, scenario_catalog, mock_square_for_scenarios, scenario_config,
):
    registry._import_all()
    run = ScenarioRun(
        scenario_name="round_amount_cluster",
        params_json={"count": 5, "seed": 13},
        started_at=datetime.now(timezone.utc),
        status="running", summary_json={},
    )
    db_session.add(run); db_session.flush()
    ctx = prepare_context(db_session, run, config=scenario_config)
    cls = registry.get("round_amount_cluster")
    summary = cls().run(ctx, cls.params_schema(count=5, seed=13))
    assert not summary["failed"], summary["failed"]
    assert summary["attempted"] == 5
    for oid in summary["created"]:
        order = db_session.get(Order, oid)
        assert order.total_cents % 100 == 0, (
            f"order {oid} total {order.total_cents} is not round"
        )
