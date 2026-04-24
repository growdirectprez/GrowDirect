import pytest
from datetime import datetime, timezone
from solex.services.scenarios.base import Scenario, ScenarioParams, prepare_context
from solex.services.scenarios import registry
from solex.models import ScenarioRun


def test_register_requires_name():
    class Bogus(Scenario):
        def run(self, ctx, params): return {}
    with pytest.raises(ValueError):
        registry.register(Bogus)


def test_register_rejects_duplicates(monkeypatch):
    monkeypatch.setattr(registry, "_registry", {})
    class A(Scenario):
        name = "same-test-name"
        def run(self, ctx, params): return {}
    class B(Scenario):
        name = "same-test-name"
        def run(self, ctx, params): return {}
    registry.register(A)
    with pytest.raises(ValueError):
        registry.register(B)


def test_prepare_context_records_seed(app, db_session):
    run = ScenarioRun(
        scenario_name="x", params_json={"count": 3},
        started_at=datetime.now(timezone.utc), status="pending", summary_json={},
    )
    db_session.add(run); db_session.flush()
    ctx = prepare_context(db_session, run, config={})
    assert ctx.run.params_json.get("seed") is not None
    assert ctx.rng is not None
    assert ctx.tag.startswith("x-")


def test_prepare_context_uses_provided_seed(app, db_session):
    run = ScenarioRun(
        scenario_name="y", params_json={"count": 5, "seed": 42},
        started_at=datetime.now(timezone.utc), status="pending", summary_json={},
    )
    db_session.add(run); db_session.flush()
    ctx = prepare_context(db_session, run, config={})
    assert ctx.run.params_json["seed"] == 42


def test_synth_customer_is_deterministic():
    import random
    from solex.services.scenarios.synth import synth_customer
    rng1 = random.Random(123)
    rng2 = random.Random(123)
    c1 = synth_customer(rng1, "run1", 0)
    c2 = synth_customer(rng2, "run1", 0)
    assert c1 == c2


def test_pick_time_in_window_wraps_midnight():
    import random
    from solex.services.scenarios.synth import pick_time_in_window
    rng = random.Random(0)
    # after_hours window 22..2; all 100 samples fall inside
    for _ in range(100):
        t = pick_time_in_window(rng, 22, 2)
        hour = t.hour
        # either 22 or 23 (first 2 hours) OR 0 or 1 (last 2 hours)
        assert hour in (22, 23, 0, 1), f"unexpected hour {hour}"
