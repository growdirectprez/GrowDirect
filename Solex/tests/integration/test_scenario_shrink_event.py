from datetime import datetime, timezone
from solex.services.scenarios import prepare_context, registry
from solex.models import ScenarioRun, InventoryAdjustment, Inventory


def test_shrink_event_adjusts_inventory_without_sales(
    app, db_session, scenario_catalog, scenario_config,
):
    registry._import_all()

    # Record pre-shrink inventory levels for the seed products
    pre = {
        inv.product_id: inv.on_hand
        for inv in db_session.query(Inventory).all()
    }
    assert all(v > 0 for v in pre.values())

    run = ScenarioRun(
        scenario_name="shrink_event",
        params_json={"count": 3, "seed": 5},
        started_at=datetime.now(timezone.utc), status="running", summary_json={},
    )
    db_session.add(run)
    db_session.flush()
    ctx = prepare_context(db_session, run, config=scenario_config)
    cls = registry.get("shrink_event")
    summary = cls().run(ctx, cls.params_schema(count=3, seed=5))

    assert summary["attempted"] == 3
    assert len(summary["shrunk"]) == 3
    assert summary["failed"] == []

    # 3 InventoryAdjustment rows with reason='shrink' + scenario_tag
    adjs = db_session.query(InventoryAdjustment).filter_by(
        reason="shrink", scenario_tag=ctx.tag,
    ).all()
    assert len(adjs) == 3
    # on_hand decreased for each affected product
    for adj in adjs:
        inv = db_session.query(Inventory).filter_by(product_id=adj.product_id).one()
        assert inv.on_hand == pre[adj.product_id] + adj.delta
        assert adj.delta < 0


def test_shrink_event_no_inventory_returns_error(
    app, db_session, scenario_config,
):
    # No seed catalog — no inventory
    registry._import_all()
    run = ScenarioRun(
        scenario_name="shrink_event",
        params_json={"count": 3, "seed": 5},
        started_at=datetime.now(timezone.utc), status="running", summary_json={},
    )
    db_session.add(run)
    db_session.flush()
    ctx = prepare_context(db_session, run, config=scenario_config)
    cls = registry.get("shrink_event")
    summary = cls().run(ctx, cls.params_schema(count=3, seed=5))
    assert summary.get("error") == "no inventory to shrink"
