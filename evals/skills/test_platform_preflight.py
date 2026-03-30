"""Platform Preflight eval suite — 100% binary pass/fail.

Source material:
  - CLAUDE.md § Shared Infrastructure (4 containers: postgres, valkey, ollama, pgadmin)
  - CLAUDE.md § Database Layout (growdirect/growdirect_dev credentials)
  - CLAUDE.md § Port Allocation (5432, 6379, 11434, 5050)
  - factory-manifest.json § preflight stage (checks list)
  - factory-preflight.md (GREEN/YELLOW/RED gate criteria)

Eval target: 100% pass rate (all binary checks).
"""

import json
import os
import subprocess

import pytest


# ---------------------------------------------------------------------------
# 1. Docker stack checks
#    Source: CLAUDE.md § Shared Infrastructure
#    "growdirect_postgres, growdirect_valkey, growdirect_ollama, growdirect_pgadmin"
# ---------------------------------------------------------------------------

REQUIRED_CONTAINERS = [
    "growdirect_postgres",
    "growdirect_valkey",
    "growdirect_ollama",
    "growdirect_pgadmin",
]


class TestDockerStack:
    """Docker infrastructure must be running."""

    def test_docker_daemon_available(self):
        """Docker daemon responds to commands."""
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10,
        )
        assert result.returncode == 0, "Docker daemon not available"

    @pytest.mark.parametrize("container", REQUIRED_CONTAINERS)
    def test_container_running(self, container):
        """Each required growdirect container is running.

        Source: CLAUDE.md § Shared Infrastructure
        """
        result = subprocess.run(
            ["docker", "inspect", "-f", "{{.State.Running}}", container],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0, f"Container {container} not found"
        assert result.stdout.strip() == "true", f"Container {container} not running"


# ---------------------------------------------------------------------------
# 2. PostgreSQL checks
#    Source: CLAUDE.md § Database Layout
#    "Dev credentials: growdirect / growdirect_dev"
# ---------------------------------------------------------------------------

class TestPostgreSQL:
    """PostgreSQL accepts connections and has required databases."""

    def test_postgres_accepting_connections(self):
        """pg_isready confirms PostgreSQL is accepting connections.

        Source: factory-preflight.md § PostgreSQL check
        """
        result = subprocess.run(
            ["docker", "exec", "growdirect_postgres", "pg_isready", "-U", "growdirect"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0, "PostgreSQL not accepting connections"
        assert "accepting connections" in result.stdout

    @pytest.mark.parametrize("database", [
        "canary",
        "canary_test",
        "cove",
        "cove_test",
        "growdirect_memory",
        "growdirect_memory_test",
    ])
    def test_database_exists(self, database):
        """Each required database exists in the PostgreSQL instance.

        Source: CLAUDE.md § Database Layout table
        """
        result = subprocess.run(
            [
                "docker", "exec", "growdirect_postgres",
                "psql", "-U", "growdirect", "-d", database,
                "-c", "SELECT 1",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0, f"Database '{database}' not accessible"


# ---------------------------------------------------------------------------
# 3. Valkey checks
#    Source: CLAUDE.md § Shared Infrastructure
#    "growdirect_valkey :6379 — sessions and cache"
# ---------------------------------------------------------------------------

class TestValkey:
    """Valkey responds to commands."""

    def test_valkey_responds(self):
        """Valkey container is reachable and responds.

        Source: factory-preflight.md § Valkey check
        """
        result = subprocess.run(
            ["docker", "exec", "growdirect_valkey", "valkey-cli", "ping"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        # Accept PONG or NOAUTH — both prove Valkey is alive
        assert result.returncode == 0 or "NOAUTH" in result.stdout or "NOAUTH" in result.stderr, (
            "Valkey not responding"
        )


# ---------------------------------------------------------------------------
# 4. Ollama checks
#    Source: CLAUDE.md § Embeddings
#    "Model: qwen3-embedding:8b (1024 dimensions)"
# ---------------------------------------------------------------------------

class TestOllama:
    """Ollama serves the embedding model."""

    def test_ollama_reachable(self):
        """Ollama API responds on port 11434.

        Source: CLAUDE.md § Port Allocation
        """
        result = subprocess.run(
            ["curl", "-sf", "http://localhost:11434/api/tags"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0, "Ollama not reachable at localhost:11434"

    def test_embedding_model_loaded(self):
        """qwen3-embedding model is available.

        Source: CLAUDE.md § Embeddings — "Model: qwen3-embedding:8b"
        """
        result = subprocess.run(
            ["curl", "-sf", "http://localhost:11434/api/tags"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0, "Ollama not reachable"
        tags = json.loads(result.stdout)
        model_names = [m["name"] for m in tags.get("models", [])]
        assert any("qwen3" in name for name in model_names), (
            f"qwen3-embedding model not loaded. Available: {model_names}"
        )


# ---------------------------------------------------------------------------
# 5. Git checks
#    Source: factory-preflight.md § Git status
# ---------------------------------------------------------------------------

class TestGitStatus:
    """Git repository is valid and on expected branch."""

    def test_is_git_repo(self):
        """Working directory is a git repository."""
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            cwd=os.path.expanduser("~/GrowDirect"),
            timeout=5,
        )
        assert result.returncode == 0, "Not a git repository"

    def test_branch_not_detached(self):
        """HEAD is attached to a branch (not detached)."""
        result = subprocess.run(
            ["git", "symbolic-ref", "HEAD"],
            capture_output=True,
            text=True,
            cwd=os.path.expanduser("~/GrowDirect"),
            timeout=5,
        )
        assert result.returncode == 0, "HEAD is detached"


# ---------------------------------------------------------------------------
# 6. Manifest checks
#    Source: factory-manifest.json
# ---------------------------------------------------------------------------

MANIFEST_PATH = os.path.join(os.path.expanduser("~/GrowDirect"), "factory-manifest.json")

EXPECTED_STAGES = [
    "preflight", "research", "blueprint", "tdd",
    "assembly", "verify", "qa", "ship", "close",
]


class TestManifest:
    """Factory manifest is valid and complete."""

    def test_manifest_exists(self):
        """factory-manifest.json exists at repo root."""
        assert os.path.isfile(MANIFEST_PATH), "factory-manifest.json not found"

    def test_manifest_valid_json(self):
        """Manifest parses as valid JSON."""
        with open(MANIFEST_PATH) as f:
            data = json.load(f)
        assert "pipeline" in data, "Manifest missing 'pipeline' key"
        assert "stages" in data, "Manifest missing 'stages' key"

    def test_pipeline_order(self):
        """Pipeline declares all 9 stages in correct order.

        Source: CLAUDE.md § Factory Process
        """
        with open(MANIFEST_PATH) as f:
            data = json.load(f)
        assert data["pipeline"] == EXPECTED_STAGES, (
            f"Pipeline order mismatch. Expected: {EXPECTED_STAGES}, got: {data['pipeline']}"
        )

    def test_preflight_checks_declared(self):
        """Preflight stage declares required infrastructure checks.

        Source: factory-manifest.json § preflight.checks
        """
        with open(MANIFEST_PATH) as f:
            data = json.load(f)
        checks = data["stages"]["preflight"].get("checks", [])
        for required in ["docker", "postgres", "valkey", "ollama", "git_clean", "gro_exists"]:
            assert required in checks, f"Preflight missing check: {required}"


# ---------------------------------------------------------------------------
# 7. Skill file checks
#    Source: factory-manifest.json § stages + CLAUDE.md § Factory Process
# ---------------------------------------------------------------------------

SKILLS_DIR = os.path.join(os.path.expanduser("~/GrowDirect"), ".claude", "skills")

REQUIRED_FACTORY_SKILLS = [
    "factory-preflight.md",
    "factory-research.md",
    "factory-blueprint.md",
    "factory-tdd.md",
    "factory-assembly.md",
    "factory-verify.md",
    "factory-qa.md",
    "factory-ship.md",
    "factory-close.md",
]


class TestSkillFiles:
    """Required skill files exist and have valid frontmatter."""

    @pytest.mark.parametrize("skill_file", REQUIRED_FACTORY_SKILLS)
    def test_factory_skill_exists(self, skill_file):
        """Each factory stage has a corresponding skill file."""
        path = os.path.join(SKILLS_DIR, skill_file)
        assert os.path.isfile(path), f"Missing skill: {skill_file}"

    @pytest.mark.parametrize("skill_file", REQUIRED_FACTORY_SKILLS)
    def test_skill_has_frontmatter(self, skill_file):
        """Each skill file starts with YAML frontmatter (--- delimiters)."""
        path = os.path.join(SKILLS_DIR, skill_file)
        with open(path) as f:
            content = f.read()
        assert content.startswith("---"), f"{skill_file} missing frontmatter"
        # Must have closing --- delimiter
        parts = content.split("---", 2)
        assert len(parts) >= 3, f"{skill_file} frontmatter not closed"

    @pytest.mark.parametrize("skill_file", REQUIRED_FACTORY_SKILLS)
    def test_skill_has_name_field(self, skill_file):
        """Each skill frontmatter contains a 'name:' field."""
        path = os.path.join(SKILLS_DIR, skill_file)
        with open(path) as f:
            content = f.read()
        # Extract frontmatter
        parts = content.split("---", 2)
        frontmatter = parts[1] if len(parts) >= 3 else ""
        assert "name:" in frontmatter, f"{skill_file} missing 'name:' in frontmatter"


# ---------------------------------------------------------------------------
# 8. Context loading checks
#    Source: factory-preflight.md § Load context
# ---------------------------------------------------------------------------

class TestContextFiles:
    """Required context files exist for preflight loading."""

    def test_platform_claude_md_exists(self):
        """Platform CLAUDE.md exists at repo root.

        Source: factory-preflight.md step 4.1
        """
        path = os.path.join(os.path.expanduser("~/GrowDirect"), "CLAUDE.md")
        assert os.path.isfile(path), "Platform CLAUDE.md not found"

    def test_canary_claude_md_exists(self):
        """Canary app CLAUDE.md exists."""
        path = os.path.join(os.path.expanduser("~/GrowDirect"), "Canary", "CLAUDE.md")
        assert os.path.isfile(path), "Canary CLAUDE.md not found"

    def test_cove_claude_md_exists(self):
        """Cove app CLAUDE.md exists."""
        path = os.path.join(os.path.expanduser("~/GrowDirect"), "Cove", "CLAUDE.md")
        assert os.path.isfile(path), "Cove CLAUDE.md not found"
