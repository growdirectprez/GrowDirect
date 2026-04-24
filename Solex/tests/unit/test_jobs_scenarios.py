from datetime import datetime, timezone
from unittest.mock import patch
from solex.models import ScenarioRun


def test_execute_scenario_run_happy(app, db_session, mocker):
    """Register a one-off toy scenario and run it through the RQ entry."""
    from solex.services.scenarios import registry, base

    class Toy(base.Scenario):
        name = "toy-for-test"
        def run(self, ctx, params):
            return {"attempted": 1, "created": ["fake"], "failed": []}

    # Isolate registry
    mocker.patch.object(registry, "_registry", {})
    registry.register(Toy)

    run = ScenarioRun(
        scenario_name="toy-for-test",
        params_json={},
        started_at=datetime.now(timezone.utc),
        status="pending",
        summary_json={},
    )
    db_session.add(run); db_session.commit()
    run_id = str(run.id)

    # Patch registry._import_all to be a no-op (we registered Toy manually)
    mocker.patch("solex.services.scenarios.registry._import_all", lambda: None)
    # Patch create_app at the source so the lazy import inside the job picks it up
    mocker.patch("solex.create_app", return_value=app)

    from solex.jobs.scenarios import execute_scenario_run
    summary = execute_scenario_run(run_id)

    # The job ran in a separate app_context — re-fetch from our test session
    db_session.expire_all()
    from solex.models import ScenarioRun as SR
    import uuid
    refreshed = db_session.get(SR, uuid.UUID(run_id))
    assert refreshed.status == "succeeded"
    assert refreshed.summary_json["attempted"] == 1


def test_execute_scenario_run_unknown_scenario(app, db_session, mocker):
    run = ScenarioRun(
        scenario_name="nonexistent-xyz",
        params_json={},
        started_at=datetime.now(timezone.utc),
        status="pending", summary_json={},
    )
    db_session.add(run); db_session.commit()
    run_id = str(run.id)
    mocker.patch("solex.create_app", return_value=app)
    from solex.jobs.scenarios import execute_scenario_run
    execute_scenario_run(run_id)
    db_session.expire_all()
    from solex.models import ScenarioRun as SR
    import uuid
    refreshed = db_session.get(SR, uuid.UUID(run_id))
    assert refreshed.status == "failed"
    assert "unknown scenario" in refreshed.summary_json["error"]
