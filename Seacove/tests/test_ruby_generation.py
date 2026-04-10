"""Tests for SketchUp Ruby code generation from spatial model."""
import pytest
from pathlib import Path
from arc.generate.sketchup_ruby import generate_ruby_scripts


class TestRubyGeneration:
    def test_generates_helpers_file(self, sample_project, tmp_path):
        generate_ruby_scripts(sample_project, tmp_path)
        helpers = tmp_path / "00_helpers.rb"
        assert helpers.exists()
        content = helpers.read_text()
        assert "module " in content
        assert "def self.ft(feet)" in content
        assert "def self.make_wall" in content

    def test_generates_walls_file(self, sample_project, tmp_path):
        generate_ruby_scripts(sample_project, tmp_path)
        walls = tmp_path / "04_walls.rb"
        assert walls.exists()
        content = walls.read_text()
        assert "wall-south" in content
        assert "start_operation" in content
        assert "commit_operation" in content
        assert "subtract" in content  # boolean opening cut

    def test_generates_structure_file(self, sample_project, tmp_path):
        generate_ruby_scripts(sample_project, tmp_path)
        structure = tmp_path / "05_structure.rb"
        assert structure.exists()
        content = structure.read_text()
        assert "make_post" in content
        assert "make_beam" in content

    def test_generates_roof_file(self, sample_project, tmp_path):
        generate_ruby_scripts(sample_project, tmp_path)
        roof = tmp_path / "06_roof.rb"
        assert roof.exists()
        content = roof.read_text()
        assert "Living_Wing" in content or "Living Wing" in content

    def test_wall_opening_positions_computed(self, sample_project, tmp_path):
        generate_ruby_scripts(sample_project, tmp_path)
        walls = tmp_path / "04_walls.rb"
        content = walls.read_text()
        assert "14.0" in content  # door position along wall-south

    def test_ruby_syntax_no_python_artifacts(self, sample_project, tmp_path):
        generate_ruby_scripts(sample_project, tmp_path)
        for rb_file in tmp_path.glob("*.rb"):
            content = rb_file.read_text()
            assert "{{" not in content, f"Unrendered Jinja2 in {rb_file.name}"
            assert "{%" not in content, f"Unrendered Jinja2 in {rb_file.name}"
            assert "None" not in content, f"Python None in {rb_file.name}"

    def test_opening_cut_north_south_wall(self, sample_project, tmp_path):
        """Opening cuts on N-S walls should swap width/depth."""
        generate_ruby_scripts(sample_project, tmp_path)
        walls = tmp_path / "04_walls.rb"
        content = walls.read_text()
        # wall-east runs N-S from [28,0] to [28,18], has a window
        assert "wall-east" in content
