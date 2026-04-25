# GrowDirect LLC — Confidential & Proprietary
# Copyright (c) 2026 GrowDirect LLC. All rights reserved.
"""Tests for the `method` CLI command group — queries over role/stage metadata."""
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "content-engine"))
import engine  # noqa: E402


# ── helpers ──────────────────────────────────────────────────────────

def _write_skill(path: Path, name: str, primary=None, assist=None, stage=None):
    """Write a minimal skill file with the given role/stage frontmatter."""
    lines = ["---", f"name: {name}"]
    if primary:
        lines.append(f"roles-primary: [{', '.join(primary)}]")
    if assist:
        lines.append(f"roles-assist: [{', '.join(assist)}]")
    if stage:
        lines.append(f"stage: {stage}")
    lines.extend(["description: test skill", "---", "", "# body"])
    path.write_text("\n".join(lines))


def _write_template(path: Path, role=None, stage=None, type_="wiki"):
    lines = ["---", f"type: {type_}"]
    if role:
        lines.append(f"method-role: {role}")
    if stage:
        lines.append(f"method-stage: {stage}")
    lines.extend(["---", "", "# body"])
    path.write_text("\n".join(lines))


# ── method skills-for ────────────────────────────────────────────────

def test_skills_for_role_returns_primary(tmp_path, monkeypatch):
    """skills-for --role X returns skills where X is in roles-primary."""
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    _write_skill(skills_dir / "foo.md", "foo", primary=["ALX"], stage="preflight")
    _write_skill(skills_dir / "bar.md", "bar", primary=["Tom"], stage="blueprint")
    _write_skill(skills_dir / "baz.md", "baz", primary=["ALX"], assist=["Eva"], stage="close")

    monkeypatch.setattr(engine, "METHOD_SKILLS_DIR", skills_dir)
    runner = CliRunner()
    result = runner.invoke(engine.cli, ["method", "skills-for", "--role", "ALX"])
    assert result.exit_code == 0, result.output
    assert "foo" in result.output
    assert "baz" in result.output
    assert "bar" not in result.output


def test_skills_for_role_returns_assist(tmp_path, monkeypatch):
    """skills-for --role X includes X in roles-assist when --include-assist is on (default)."""
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    _write_skill(skills_dir / "foo.md", "foo", primary=["Tom"], assist=["ALX"])

    monkeypatch.setattr(engine, "METHOD_SKILLS_DIR", skills_dir)
    runner = CliRunner()
    result = runner.invoke(engine.cli, ["method", "skills-for", "--role", "ALX"])
    assert result.exit_code == 0, result.output
    assert "foo" in result.output  # as assist


def test_skills_for_role_primary_only_flag(tmp_path, monkeypatch):
    """--primary-only omits assist matches."""
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    _write_skill(skills_dir / "foo.md", "foo", primary=["Tom"], assist=["ALX"])
    _write_skill(skills_dir / "bar.md", "bar", primary=["ALX"])

    monkeypatch.setattr(engine, "METHOD_SKILLS_DIR", skills_dir)
    runner = CliRunner()
    result = runner.invoke(engine.cli, ["method", "skills-for", "--role", "ALX", "--primary-only"])
    assert result.exit_code == 0, result.output
    assert "bar" in result.output
    assert "foo" not in result.output


def test_skills_for_stage(tmp_path, monkeypatch):
    """skills-for --stage X returns skills with stage: X."""
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    _write_skill(skills_dir / "factory-ship.md", "factory-ship", primary=["Jeremy"], stage="ship")
    _write_skill(skills_dir / "canary-ship.md", "canary-ship", primary=["Jeremy"], stage="ship")
    _write_skill(skills_dir / "factory-qa.md", "factory-qa", primary=["Compliance"], stage="qa")

    monkeypatch.setattr(engine, "METHOD_SKILLS_DIR", skills_dir)
    runner = CliRunner()
    result = runner.invoke(engine.cli, ["method", "skills-for", "--stage", "ship"])
    assert result.exit_code == 0, result.output
    assert "factory-ship" in result.output
    assert "canary-ship" in result.output
    assert "factory-qa" not in result.output


def test_skills_for_role_and_stage(tmp_path, monkeypatch):
    """Combined filter — must match both."""
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    _write_skill(skills_dir / "a.md", "a", primary=["Jeremy"], stage="ship")
    _write_skill(skills_dir / "b.md", "b", primary=["Tom"], stage="ship")
    _write_skill(skills_dir / "c.md", "c", primary=["Jeremy"], stage="tdd")

    monkeypatch.setattr(engine, "METHOD_SKILLS_DIR", skills_dir)
    runner = CliRunner()
    result = runner.invoke(engine.cli, ["method", "skills-for", "--role", "Jeremy", "--stage", "ship"])
    assert result.exit_code == 0, result.output
    # Check per-line: skill listings are indented with "  <name>"
    listed = {line.strip().split()[0] for line in result.output.splitlines() if line.startswith("  ") and line.strip()}
    assert "a" in listed
    assert "b" not in listed  # wrong role
    assert "c" not in listed  # wrong stage


def test_skills_for_no_filter_errors():
    """--role or --stage is required."""
    runner = CliRunner()
    result = runner.invoke(engine.cli, ["method", "skills-for"])
    assert result.exit_code != 0


# ── method templates-for ─────────────────────────────────────────────

def test_templates_for_role(tmp_path, monkeypatch):
    """templates-for --role returns templates with method-role matching."""
    tpl_dir = tmp_path / "tpl"
    tpl_dir.mkdir()
    _write_template(tpl_dir / "wiki-article.md", role="Jess", stage="close")
    _write_template(tpl_dir / "raw-intake.md", role="Research", stage="research")
    _write_template(tpl_dir / "decision.md", role="Tom", stage="blueprint")

    monkeypatch.setattr(engine, "METHOD_TEMPLATES_DIR", tpl_dir)
    runner = CliRunner()
    result = runner.invoke(engine.cli, ["method", "templates-for", "--role", "Research"])
    assert result.exit_code == 0, result.output
    assert "raw-intake" in result.output
    assert "wiki-article" not in result.output


# ── method stats ─────────────────────────────────────────────────────

def test_stats_returns_counts(tmp_path, monkeypatch):
    """stats returns skill + template + stage coverage counts."""
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    _write_skill(skills_dir / "a.md", "a", primary=["ALX"], stage="preflight")
    _write_skill(skills_dir / "b.md", "b", primary=["Tom"], stage="blueprint")
    _write_skill(skills_dir / "c.md", "c")  # untagged

    tpl_dir = tmp_path / "tpl"
    tpl_dir.mkdir()
    _write_template(tpl_dir / "w.md", role="Jess")
    _write_template(tpl_dir / "x.md")  # untagged

    monkeypatch.setattr(engine, "METHOD_SKILLS_DIR", skills_dir)
    monkeypatch.setattr(engine, "METHOD_TEMPLATES_DIR", tpl_dir)
    runner = CliRunner()
    result = runner.invoke(engine.cli, ["method", "stats"])
    assert result.exit_code == 0, result.output
    assert "Skills" in result.output
    assert "2 tagged" in result.output or "Tagged: 2" in result.output
    # 1 untagged skill + 1 untagged template
    assert "1 untagged" in result.output or "Untagged: 1" in result.output
