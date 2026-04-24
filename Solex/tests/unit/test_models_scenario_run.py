from datetime import datetime, timezone
from solex.models.scenarios import ScenarioRun


def test_scenario_run_fields():
    r = ScenarioRun(
        scenario_name="normal_retail_day",
        params_json={"count": 10},
        started_at=datetime.now(timezone.utc),
        status="pending",
        summary_json={},
    )
    assert r.scenario_name == "normal_retail_day"
    assert r.status == "pending"
