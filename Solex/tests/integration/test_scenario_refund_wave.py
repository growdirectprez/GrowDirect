from datetime import datetime, timezone
from unittest.mock import MagicMock
from solex.services.scenarios import prepare_context, registry
from solex.models import ScenarioRun, Order, Refund


def test_refund_wave_refunds_prior_orders(
    app, db_session, scenario_catalog, mocker, scenario_config,
):
    # Seed paid orders via normal_retail_day first
    counter = {"n": 0}

    def _order(*a, **kw):
        counter["n"] += 1
        return {"id": f"sq_order_{counter['n']}"}

    def _payment(*a, **kw):
        return {"id": f"sq_pay_{counter['n']}"}

    def _refund(*a, **kw):
        counter["n"] += 1
        return {"id": f"sq_refund_{counter['n']}"}

    client = MagicMock(
        create_order=MagicMock(side_effect=_order),
        create_payment=MagicMock(side_effect=_payment),
        create_refund=MagicMock(side_effect=_refund),
    )
    mocker.patch("solex.services.scenarios.base._square", return_value=client)
    registry._import_all()

    # Seed 3 paid orders
    run1 = ScenarioRun(
        scenario_name="normal_retail_day",
        params_json={"count": 3, "seed": 1},
        started_at=datetime.now(timezone.utc), status="running", summary_json={},
    )
    db_session.add(run1)
    db_session.flush()
    ctx1 = prepare_context(db_session, run1, config=scenario_config)
    nrd = registry.get("normal_retail_day")()
    nrd.run(ctx1, nrd.params_schema(count=3, seed=1))

    # Run refund_wave
    run2 = ScenarioRun(
        scenario_name="refund_wave",
        params_json={"count": 2, "seed": 2, "full_refund": True},
        started_at=datetime.now(timezone.utc), status="running", summary_json={},
    )
    db_session.add(run2)
    db_session.flush()
    ctx2 = prepare_context(db_session, run2, config=scenario_config)
    rw = registry.get("refund_wave")()
    summary = rw.run(ctx2, rw.params_schema(count=2, seed=2, full_refund=True))

    assert summary["attempted"] == 2
    assert len(summary["refunded"]) == 2
    assert summary["failed"] == []

    refunds = db_session.query(Refund).filter_by(scenario_tag=ctx2.tag).all()
    assert len(refunds) == 2
    # Refunded orders transitioned to "refunded"
    refunded_order_ids = [r.order_id for r in refunds]
    for oid in refunded_order_ids:
        order = db_session.get(Order, oid)
        assert order.status == "refunded"


def test_refund_wave_empty_when_no_orders(
    app, db_session, scenario_catalog, mock_square_for_scenarios, scenario_config,
):
    registry._import_all()
    run = ScenarioRun(
        scenario_name="refund_wave",
        params_json={"count": 5, "seed": 3},
        started_at=datetime.now(timezone.utc), status="running", summary_json={},
    )
    db_session.add(run)
    db_session.flush()
    ctx = prepare_context(db_session, run, config=scenario_config)
    rw = registry.get("refund_wave")()
    summary = rw.run(ctx, rw.params_schema(count=5, seed=3))
    assert summary.get("error") == "no paid orders to refund"
