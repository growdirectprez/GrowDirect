from graphs.state import PipelineState


def test_pipeline_state_has_required_keys():
    state: PipelineState = {
        "task": "add hawk service",
        "service": "canary-gateway",
        "artifacts": {},
        "review_result": "",
        "revision_count": 0,
        "deploy_status": "",
        "error": "",
        "output_dir": "out/canary-gateway",
    }
    assert state["task"] == "add hawk service"
    assert state["revision_count"] == 0


def test_pipeline_state_artifacts_is_dict():
    state: PipelineState = {
        "task": "", "service": "", "artifacts": {"cmd/hawk/main.go": "package main"},
        "review_result": "", "revision_count": 0,
        "deploy_status": "", "error": "", "output_dir": "",
    }
    assert "cmd/hawk/main.go" in state["artifacts"]
