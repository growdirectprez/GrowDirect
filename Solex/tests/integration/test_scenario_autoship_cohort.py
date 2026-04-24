from datetime import datetime, timezone
from unittest.mock import MagicMock
from solex.services.scenarios import prepare_context, registry
from solex.models import ScenarioRun, Subscription, Order


def _mock_square_for_subs(mocker):
    counter = {"n": 0}

    def _cust(*a, **kw):
        counter["n"] += 1
        return {"id": f"sq_cust_{counter['n']}"}

    def _card(*a, **kw):
        return {"id": f"ccof:test_{counter['n']}"}

    def _payment(*a, **kw):
        counter["n"] += 1
        return {"id": f"sq_pay_{counter['n']}", "order_id": f"sq_order_{counter['n']}"}

    client = MagicMock(
        create_customer=MagicMock(side_effect=_cust),
        save_card_on_file=MagicMock(side_effect=_card),
        charge_saved_card=MagicMock(side_effect=_payment),
    )
    mocker.patch("solex.services.scenarios.base._square", return_value=client)
    mocker.patch(
        "solex.services.scenarios.autoship_cohort._square",
        return_value=client,
        create=True,
    )
    return client


def test_autoship_cohort_creates_subs_and_charges(
    app, db_session, scenario_catalog, mocker, scenario_config,
):
    _mock_square_for_subs(mocker)
    registry._import_all()

    run = ScenarioRun(
        scenario_name="autoship_cohort",
        params_json={"count": 3, "seed": 11, "cadence_days": 30},
        started_at=datetime.now(timezone.utc),
        status="running", summary_json={},
    )
    db_session.add(run)
    db_session.flush()
    ctx = prepare_context(db_session, run, config=scenario_config)
    cls = registry.get("autoship_cohort")
    summary = cls().run(ctx, cls.params_schema(count=3, seed=11, cadence_days=30))

    assert summary["subs_created"] == 3
    assert summary["subs_failed"] == []
    assert summary["charge_cycle"]["attempted"] == 3
    assert summary["charge_cycle"]["succeeded"] == 3

    assert db_session.query(Subscription).count() == 3
    autoship_orders = db_session.query(Order).filter_by(
        autoship=True, scenario_tag=ctx.tag,
    ).all()
    assert len(autoship_orders) == 3
