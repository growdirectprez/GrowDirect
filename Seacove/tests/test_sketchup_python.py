"""Tests for arc.generate.sketchup_python — Python code generation for Trimble MCP."""
from __future__ import annotations

import ast
import math

import pytest

from arc.generate.sketchup_python import (
    FT_TO_IN,
    generate_stage_code,
    generate_all_stages,
    STAGES,
    _default_camera_for_project,
)


# ---------------------------------------------------------------------------
# Minimal project fixture (inline — no file I/O)
# ---------------------------------------------------------------------------

def _make_minimal_project():
    """Build a minimal Project in memory: one floor, two walls, one post, one beam."""
    from arc.model.spatial_model import (
        Project, CoordinateSystem, LotInfo, Floor, Room, Wall, Opening,
        Structural, Post, Beam, Roof, Source,
    )

    coord = CoordinateSystem("east", "north", "up", "SW corner")
    lot = LotInfo(boundaries=[], setbacks={"front": 20, "side": 5, "rear": 15})

    # A simple 24×18 ft box — south wall with one window
    walls = [
        Wall(
            id="wall_s",
            wall_type="exterior",
            from_pt=[0.0, 0.0],
            to_pt=[24.0, 0.0],
            thickness_in=5.5,
            rooms={"interior": "room_a", "exterior": None},
            openings=[
                Opening(
                    opening_type="window",
                    position_along_wall=6.0,
                    width=4.0,
                    height=4.0,
                    sill_height=2.5,
                )
            ],
        ),
        Wall(
            id="wall_n",
            wall_type="exterior",
            from_pt=[0.0, 18.0],
            to_pt=[24.0, 18.0],
            thickness_in=5.5,
            rooms={"interior": "room_a", "exterior": None},
        ),
        Wall(
            id="wall_w",
            wall_type="exterior",
            from_pt=[0.0, 0.0],
            to_pt=[0.0, 18.0],
            thickness_in=5.5,
            rooms={"interior": "room_a", "exterior": None},
            openings=[
                Opening(
                    opening_type="door",
                    position_along_wall=4.0,
                    width=3.0,
                    height=6.833,
                    sill_height=0.0,
                )
            ],
        ),
        Wall(
            id="wall_e",
            wall_type="exterior",
            from_pt=[24.0, 0.0],
            to_pt=[24.0, 18.0],
            thickness_in=5.5,
            rooms={"interior": "room_a", "exterior": None},
        ),
    ]

    rooms = [
        Room(
            id="room_a",
            label="Living Room",
            polygon=[[0,0],[24,0],[24,18],[0,18]],
            wall_refs=["wall_s","wall_n","wall_w","wall_e"],
        )
    ]

    structural = Structural(
        posts=[
            Post(position=[6.0, 6.0], size_in=3.5, z_base=0.0, height=8.0),
            Post(position=[18.0, 6.0], size_in=3.5, z_base=0.0, height=8.0),
        ],
        beams=[
            Beam(
                from_pt=[6.0, 6.0],
                to_pt=[18.0, 6.0],
                width_in=3.5,
                depth_in=9.25,
                z=8.0,
                label="Main Beam",
            )
        ],
    )

    floor = Floor(
        level=0,
        label="Ground Floor",
        plate_height=8.0,
        z_origin=0.0,
        rooms=rooms,
        walls=walls,
        structural=structural,
    )

    return Project(
        schema_version=1,
        project_name="test_house",
        address="1 Test St",
        coordinate_system=coord,
        lot=lot,
        floors=[floor],
        sources=[Source(id="test", source_type="blueprint", file="test.pdf")],
    )


@pytest.fixture
def project():
    return _make_minimal_project()


# ---------------------------------------------------------------------------
# generate_stage_code — general
# ---------------------------------------------------------------------------

def test_unknown_stage_raises(project):
    with pytest.raises(ValueError, match="Unknown stage"):
        generate_stage_code(project, "nonexistent")


def test_all_stages_returns_dict(project):
    result = generate_all_stages(project)
    assert set(result.keys()) == set(STAGES)
    for stage, code in result.items():
        assert isinstance(code, str)
        assert len(code) > 100


# ---------------------------------------------------------------------------
# Stage: structural
# ---------------------------------------------------------------------------

class TestStructuralStage:
    def test_structural_code_is_string(self, project):
        code = generate_stage_code(project, "structural")
        assert isinstance(code, str)

    def test_structural_code_no_import_statements(self, project):
        code = generate_stage_code(project, "structural")
        # No bare 'import' lines (SDK rule)
        for line in code.splitlines():
            stripped = line.strip()
            if stripped.startswith("import ") or stripped.startswith("from "):
                pytest.fail(f"Found import statement in generated code: {line!r}")

    def test_structural_code_contains_post_positions(self, project):
        code = generate_stage_code(project, "structural")
        # Post at [6,6] ft → [72,72] in
        assert "72.0" in code

    def test_structural_code_contains_beam_position(self, project):
        code = generate_stage_code(project, "structural")
        # Beam from_pt [6,6] ft → [72,72] in
        assert "72.0" in code

    def test_structural_code_has_result(self, project):
        code = generate_stage_code(project, "structural")
        assert "result" in code
        assert "structural" in code

    def test_structural_code_has_camera(self, project):
        code = generate_stage_code(project, "structural")
        assert "Camera()" in code
        assert "set_orientation" in code

    def test_structural_code_has_component_defs_lookup(self, project):
        code = generate_stage_code(project, "structural")
        assert "_arc_defs" in code

    def test_structural_no_structural_members_graceful(self):
        """Project with no structural members should not crash."""
        from arc.model.spatial_model import (
            Project, CoordinateSystem, LotInfo, Floor, Room, Wall, Source
        )
        proj = Project(
            schema_version=1,
            project_name="empty",
            address="",
            coordinate_system=CoordinateSystem("east","north","up","sw"),
            lot=LotInfo([], {}),
            floors=[Floor(0, "GF", 8.0, 0.0, [], [],)],
            sources=[],
        )
        code = generate_stage_code(proj, "structural")
        assert "placed': 0" in code or "placed': 0" in code.replace(" ", "")

    def test_feet_to_inches_conversion(self, project):
        code = generate_stage_code(project, "structural")
        # Post at 6 ft = 72 in, beam from 6 ft = 72 in
        assert "72.0" in code

    def test_beam_rotation_present_for_angled_beam(self):
        """Diagonal beam should have a non-zero rotation in placement code."""
        from arc.model.spatial_model import (
            Project, CoordinateSystem, LotInfo, Floor, Structural, Beam, Source
        )
        diagonal_beam = Beam(
            from_pt=[0.0, 0.0], to_pt=[10.0, 10.0],
            width_in=3.5, depth_in=9.25, z=8.0,
        )
        proj = Project(
            schema_version=1, project_name="diag", address="",
            coordinate_system=CoordinateSystem("east","north","up","sw"),
            lot=LotInfo([], {}),
            floors=[Floor(
                level=0, label="GF", plate_height=8.0, z_origin=0.0,
                rooms=[], walls=[],
                structural=Structural(posts=[], beams=[diagonal_beam]),
            )],
            sources=[],
        )
        code = generate_stage_code(proj, "structural")
        # 45° diagonal beam
        assert "45.0" in code


# ---------------------------------------------------------------------------
# Stage: framing
# ---------------------------------------------------------------------------

class TestFramingStage:
    def test_framing_code_is_string(self, project):
        code = generate_stage_code(project, "framing")
        assert isinstance(code, str)

    def test_framing_code_no_import_statements(self, project):
        code = generate_stage_code(project, "framing")
        for line in code.splitlines():
            stripped = line.strip()
            if stripped.startswith("import ") or stripped.startswith("from "):
                pytest.fail(f"Found import statement: {line!r}")

    def test_framing_code_contains_stud(self, project):
        code = generate_stage_code(project, "framing")
        assert "stud" in code.lower()

    def test_framing_code_contains_plate(self, project):
        code = generate_stage_code(project, "framing")
        assert "plate" in code.lower()

    def test_framing_code_has_result(self, project):
        code = generate_stage_code(project, "framing")
        assert "result" in code
        assert "framing" in code

    def test_framing_code_exterior_walls_use_2x6(self, project):
        code = generate_stage_code(project, "framing")
        assert "2x6" in code

    def test_framing_code_has_component_defs_lookup(self, project):
        code = generate_stage_code(project, "framing")
        assert "_arc_defs" in code

    def test_framing_contains_header_for_window(self, project):
        code = generate_stage_code(project, "framing")
        # Window on south wall should generate a header component
        assert "header" in code.lower()

    def test_framing_contains_header_for_door(self, project):
        code = generate_stage_code(project, "framing")
        # Door on west wall should also generate a header
        assert "header" in code.lower()

    def test_framing_feet_to_inches(self, project):
        code = generate_stage_code(project, "framing")
        # 8 ft plate height × 12 = 96.0 in
        assert "96.0" in code


# ---------------------------------------------------------------------------
# Camera
# ---------------------------------------------------------------------------

def test_camera_code_in_structural(project):
    code = generate_stage_code(project, "structural")
    assert "enable_perspective" in code
    assert "set_perspective_frustum_fov" in code

def test_default_camera_contains_camera_call(project):
    cam_code = _default_camera_for_project(project)
    assert "Camera()" in cam_code
    assert "set_orientation" in cam_code
