"""Shared fixtures for skill eval suites.

Skill evals test the *output* of skills — not the skills themselves as code.
They validate that infrastructure checks, domain calculations, and structured
outputs meet pass/fail criteria derived from source material.
"""

import subprocess
import pytest


@pytest.fixture
def docker_running():
    """Check if Docker daemon is available."""
    result = subprocess.run(
        ["docker", "info"],
        capture_output=True,
        timeout=10,
    )
    if result.returncode != 0:
        pytest.skip("Docker not available")
    return True


@pytest.fixture
def growdirect_containers(docker_running):
    """Return list of running growdirect_* containers."""
    result = subprocess.run(
        ["docker", "ps", "--format", "{{.Names}}", "--filter", "name=growdirect"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    return [name.strip() for name in result.stdout.strip().split("\n") if name.strip()]
