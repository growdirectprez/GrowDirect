"""Tests for the ARC CLI."""
import pytest
from click.testing import CliRunner
from arc.cli import main


@pytest.fixture
def runner():
    return CliRunner()


class TestCLI:
    def test_version(self, runner):
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_validate_missing_project(self, runner, tmp_path):
        result = runner.invoke(main, ["validate", "nonexistent"])
        assert result.exit_code != 0

    def test_generate_missing_model(self, runner):
        result = runner.invoke(main, ["generate", "nonexistent"])
        assert result.exit_code != 0

    def test_commands_exist(self, runner):
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        for cmd in ["ingest", "extract", "model", "validate", "generate"]:
            assert cmd in result.output
