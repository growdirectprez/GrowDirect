"""Tests for engine._extract_file and the `extract` CLI command."""
import json
import subprocess
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE = REPO_ROOT / "content-engine" / "engine.py"
FIXTURES = Path(__file__).parent / "fixtures"

sys.path.insert(0, str(REPO_ROOT / "content-engine"))
import engine  # noqa: E402


# ── _extract_file ────────────────────────────────────────────────────

def test_extract_file_docx_returns_markdown(tmp_path):
    src = FIXTURES / "sample.docx"
    target = tmp_path / "sample.docx.md"
    entry = engine._extract_file(src, target)
    assert entry["status"] == "ok"
    assert entry["method"] == "markitdown"
    assert target.exists()
    text = target.read_text()
    assert len(text) > 0
    assert entry["source_sha256"]
    assert entry["target_path"] == str(target)
    assert entry["extracted_at"].startswith("20")
    assert entry["error"] is None

def test_extract_file_pdf_returns_markdown(tmp_path):
    src = FIXTURES / "sample.pdf"
    if not src.exists():
        pytest.skip("sample.pdf fixture not present (gitignored via *.pdf rule)")
    target = tmp_path / "sample.pdf.md"
    entry = engine._extract_file(src, target)
    if entry["status"] != "ok":
        import shutil as sh
        if not sh.which("pdftotext"):
            pytest.skip(f"PDF extraction failed and pdftotext not installed: {entry['error']}")
    assert entry["status"] == "ok"
    assert entry["method"] in ("markitdown", "pdftotext")
    assert target.exists()
    assert len(target.read_text()) > 0

def test_extract_file_unsupported_ext_returns_skipped(tmp_path):
    src = tmp_path / "thing.vsd"
    src.write_bytes(b"FAKE VISIO")
    target = tmp_path / "thing.vsd.md"
    entry = engine._extract_file(src, target)
    assert entry["status"] == "skipped"
    assert entry["method"] == "skip"
    assert not target.exists()

def test_extract_file_nonexistent_source_raises(tmp_path):
    src = tmp_path / "does-not-exist.docx"
    target = tmp_path / "out.md"
    with pytest.raises((FileNotFoundError, OSError)):
        engine._extract_file(src, target)


# ── extract CLI command ──────────────────────────────────────────────

def test_extract_cli_dry_run_default(tmp_path):
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    (src_dir / "a.docx").write_bytes((FIXTURES / "sample.docx").read_bytes())
    target = tmp_path / "out"

    runner = CliRunner()
    result = runner.invoke(engine.cli, ["extract", str(src_dir), "--target", str(target)])
    assert result.exit_code == 0, result.output
    assert "DRY RUN" in result.output or "dry-run" in result.output.lower()
    assert not any(target.rglob("*.md")) if target.exists() else True

def test_extract_cli_execute_writes_manifest_and_markdown(tmp_path):
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    (src_dir / "a.docx").write_bytes((FIXTURES / "sample.docx").read_bytes())
    (src_dir / "~$a.docx").write_bytes(b"tempfile")
    target = tmp_path / "out"

    runner = CliRunner()
    result = runner.invoke(
        engine.cli,
        ["extract", str(src_dir), "--target", str(target), "--execute"],
    )
    assert result.exit_code == 0, result.output
    assert (target / "a.docx.md").exists()
    assert not (target / "~$a.docx.md").exists()
    manifest_path = target / ".extract-manifest.json"
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text())
    assert isinstance(manifest, list)
    ok = [m for m in manifest if m["status"] == "ok"]
    assert len(ok) == 1
    assert ok[0]["source_path"].endswith("a.docx")

def test_extract_cli_ext_filter(tmp_path):
    if not (FIXTURES / "sample.pdf").exists():
        pytest.skip("sample.pdf fixture not present (gitignored via *.pdf rule)")
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    (src_dir / "a.docx").write_bytes((FIXTURES / "sample.docx").read_bytes())
    (src_dir / "b.pdf").write_bytes((FIXTURES / "sample.pdf").read_bytes())
    target = tmp_path / "out"

    runner = CliRunner()
    result = runner.invoke(
        engine.cli,
        ["extract", str(src_dir), "--target", str(target), "--ext", "docx", "--execute"],
    )
    assert result.exit_code == 0, result.output
    assert (target / "a.docx.md").exists()
    assert not (target / "b.pdf.md").exists()

def test_extract_cli_maxdepth_top_level_only(tmp_path):
    src_dir = tmp_path / "src"
    (src_dir / "nested").mkdir(parents=True)
    (src_dir / "top.docx").write_bytes((FIXTURES / "sample.docx").read_bytes())
    (src_dir / "nested" / "deep.docx").write_bytes((FIXTURES / "sample.docx").read_bytes())
    target = tmp_path / "out"

    runner = CliRunner()
    result = runner.invoke(
        engine.cli,
        ["extract", str(src_dir), "--target", str(target), "--maxdepth", "1", "--execute"],
    )
    assert result.exit_code == 0, result.output
    assert (target / "top.docx.md").exists()
    assert not (target / "nested" / "deep.docx.md").exists()
