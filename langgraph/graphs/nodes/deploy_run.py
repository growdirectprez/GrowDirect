import os
import subprocess
from graphs.state import PipelineState


def deploy_run_node(state: PipelineState) -> dict:
    project = os.getenv("GCP_PROJECT", "")
    region  = os.getenv("GCP_REGION", "us-central1")
    service = state["service"]

    if not project:
        return {"deploy_status": "failed", "error": "GCP_PROJECT not set"}

    cmd = [
        "gcloud", "run", "deploy", service,
        "--source", f"out/{service}",
        "--region", region,
        "--project", project,
        "--quiet",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            return {"deploy_status": "failed", "error": result.stderr[:500]}
        return {"deploy_status": "ok", "error": ""}
    except subprocess.TimeoutExpired:
        return {"deploy_status": "failed", "error": "gcloud deploy timed out after 5 minutes"}
    except FileNotFoundError:
        return {"deploy_status": "failed", "error": "gcloud not found in PATH"}
