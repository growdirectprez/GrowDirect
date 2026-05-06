import pytest
from unittest.mock import patch, MagicMock
from graphs.nodes.deploy_run import deploy_run_node


def test_deploy_node_fails_without_gcp_project(base_state):
    with patch.dict("os.environ", {}, clear=False):
        import os
        os.environ.pop("GCP_PROJECT", None)
        result = deploy_run_node(base_state)
    assert result["deploy_status"] == "failed"
    assert "GCP_PROJECT" in result["error"]


def test_deploy_node_handles_gcloud_not_found(base_state):
    with patch.dict("os.environ", {"GCP_PROJECT": "test-project"}):
        with patch("subprocess.run", side_effect=FileNotFoundError):
            result = deploy_run_node(base_state)
    assert result["deploy_status"] == "failed"
    assert "gcloud not found" in result["error"]


def test_deploy_node_success(base_state):
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stderr = ""
    with patch.dict("os.environ", {"GCP_PROJECT": "test-project"}):
        with patch("subprocess.run", return_value=mock_result):
            result = deploy_run_node(base_state)
    assert result["deploy_status"] == "ok"
