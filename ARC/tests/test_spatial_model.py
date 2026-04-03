"""Tests for the ARC spatial model data classes."""
import json
import pytest
import tempfile
from pathlib import Path

from arc.model.spatial_model import (
    Project, Floor, Wall, Room, Opening, Post, Beam,
    RoofPlane, LotInfo, Source, Conflict, CoordinateSystem,
)


class TestWall:
    def test_wall_creation(self):
        wall = Wall(
            id="wall-south",
            from_pt=[0, 0],
            to_pt=[28, 0],
            wall_type="exterior",
            thickness_in=6,
            rooms={"interior": "kitchen-01", "exterior": None},
        )
        assert wall.id == "wall-south"
        assert wall.length_ft == pytest.approx(28.0)
        assert wall.thickness_ft == pytest.approx(0.5)

    def test_wall_length_diagonal(self):
        wall = Wall(
            id="wall-diag",
            from_pt=[0, 0],
            to_pt=[3, 4],
            wall_type="interior",
            thickness_in=4,
            rooms={"interior": "room-a", "exterior": "room-b"},
        )
        assert wall.length_ft == pytest.approx(5.0)

    def test_wall_direction_vector(self):
        wall = Wall(
            id="wall-east",
            from_pt=[0, 0],
            to_pt=[10, 0],
            wall_type="exterior",
            thickness_in=6,
            rooms={"interior": "room-a", "exterior": None},
        )
        dx, dy = wall.direction
        assert dx == pytest.approx(1.0)
        assert dy == pytest.approx(0.0)


class TestOpening:
    def test_opening_creation(self):
        opening = Opening(
            opening_type="door",
            position_along_wall=14.0,
            width=3.0,
            height=6.67,
            sill_height=0.0,
        )
        assert opening.opening_type == "door"
        assert opening.width == 3.0

    def test_opening_end_position(self):
        opening = Opening(
            opening_type="window",
            position_along_wall=8.0,
            width=4.0,
            height=4.0,
            sill_height=3.0,
        )
        assert opening.end_position == pytest.approx(12.0)


class TestRoom:
    def test_room_creation(self):
        room = Room(
            id="kitchen-01",
            label="Kitchen",
            polygon=[[0, 0], [12, 0], [12, 14], [0, 14]],
            wall_refs=["wall-s", "wall-e", "wall-n", "wall-w"],
        )
        assert room.id == "kitchen-01"
        assert len(room.polygon) == 4

    def test_room_area(self):
        room = Room(
            id="room-rect",
            label="Rectangle",
            polygon=[[0, 0], [10, 0], [10, 12], [0, 12]],
            wall_refs=[],
        )
        assert room.area_sqft == pytest.approx(120.0)

    def test_room_area_l_shape(self):
        room = Room(
            id="room-l",
            label="L-Shape",
            polygon=[[0, 0], [10, 0], [10, 6], [5, 6], [5, 12], [0, 12]],
            wall_refs=[],
        )
        assert room.area_sqft == pytest.approx(90.0)


class TestFloor:
    def test_floor_creation(self):
        floor = Floor(
            level=0,
            label="Ground Floor",
            plate_height=8.0,
            z_origin=0.0,
            rooms=[],
            walls=[],
        )
        assert floor.level == 0
        assert floor.plate_height == 8.0


class TestProject:
    def test_project_creation(self):
        project = Project(
            schema_version=1,
            project_name="seacove",
            address="25 Seacove Dr, RPV",
            coordinate_system=CoordinateSystem(
                x="east", y="north", z="up", origin="SW corner of lot"
            ),
            lot=LotInfo(
                boundaries=[[0, 0], [80, 0], [80, 60], [0, 60]],
                setbacks={"front": 20, "rear": 15, "side_left": 5, "side_right": 5},
            ),
            floors=[],
            sources=[],
        )
        assert project.schema_version == 1
        assert project.project_name == "seacove"


# ---------------------------------------------------------------------------
# Task 3: Serialization tests
# ---------------------------------------------------------------------------

from arc.model.serialization import save_project, load_project
from arc.model.spatial_model import (
    Structural, Roof, RoofPlane, Fixture, SourceRef,
)


class TestSerialization:
    def _make_sample_project(self) -> Project:
        wall = Wall(
            id="wall-south",
            from_pt=[0, 0],
            to_pt=[28, 0],
            wall_type="exterior",
            thickness_in=6,
            rooms={"interior": "living-01", "exterior": None},
            openings=[
                Opening(
                    opening_type="door",
                    position_along_wall=14.0,
                    width=3.0,
                    height=6.67,
                    sill_height=0.0,
                )
            ],
            sources=[SourceRef(ref="as-built", confidence=0.95)],
        )
        room = Room(
            id="living-01",
            label="Living Room",
            polygon=[[0, 0], [28, 0], [28, 18], [0, 18]],
            wall_refs=["wall-south"],
            fixtures=[Fixture(fixture_type="fireplace", position=[2, 9])],
        )
        floor = Floor(
            level=0,
            label="Ground Floor",
            plate_height=8.0,
            z_origin=0.0,
            rooms=[room],
            walls=[wall],
        )
        return Project(
            schema_version=1,
            project_name="seacove",
            address="25 Seacove Dr, RPV",
            coordinate_system=CoordinateSystem(
                x="east", y="north", z="up", origin="SW corner of lot"
            ),
            lot=LotInfo(
                boundaries=[[0, 0], [80, 0], [80, 60], [0, 60]],
                setbacks={"front": 20, "rear": 15, "side_left": 5, "side_right": 5},
            ),
            floors=[floor],
            sources=[Source(id="as-built", source_type="blueprint", file="inputs/plan.pdf", page=1)],
            structural=Structural(
                posts=[Post(position=[2, 0], size_in=4, material="douglas_fir")],
                beams=[Beam(from_pt=[-2, 9], to_pt=[30, 9], width_in=4, depth_in=10, z=8.0)],
            ),
            roof=Roof(planes=[
                RoofPlane(label="Living Wing", roof_type="flat", slope=0.25,
                          overhang=3.5, boundary=[[0, 0], [28, 0], [28, 18], [0, 18]], z_base=8.83),
            ]),
        )

    def test_save_and_load_round_trip(self):
        project = self._make_sample_project()
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "model.json"
            save_project(project, path)
            loaded = load_project(path)
            assert loaded.project_name == "seacove"
            assert loaded.schema_version == 1
            assert len(loaded.floors) == 1
            assert len(loaded.floors[0].walls) == 1
            assert loaded.floors[0].walls[0].length_ft == pytest.approx(28.0)
            assert len(loaded.floors[0].walls[0].openings) == 1
            assert loaded.floors[0].rooms[0].area_sqft == pytest.approx(504.0)

    def test_save_produces_valid_json(self):
        project = self._make_sample_project()
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "model.json"
            save_project(project, path)
            data = json.loads(path.read_text())
            assert data["schema_version"] == 1
            assert data["project"] == "seacove"
            assert "floors" in data["structure"]

    def test_json_key_names_match_spec(self):
        """Verify JSON keys match the spec, not Python field names."""
        project = self._make_sample_project()
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "model.json"
            save_project(project, path)
            data = json.loads(path.read_text())
            # Wall uses "type" not "wall_type", "from"/"to" not "from_pt"/"to_pt"
            wall = data["structure"]["floors"][0]["walls"][0]
            assert "type" in wall  # not "wall_type"
            assert "from" in wall  # not "from_pt"
            assert "to" in wall   # not "to_pt"
            # Opening uses "type" not "opening_type"
            opening = wall["openings"][0]
            assert "type" in opening
            # Fixture uses "type" not "fixture_type"
            fixture = data["structure"]["floors"][0]["rooms"][0]["fixtures"][0]
            assert "type" in fixture  # not "fixture_type"
            # RoofPlane uses "type" not "roof_type"
            roof = data["roof"]["planes"][0]
            assert "type" in roof  # not "roof_type"
            # Source uses "type" not "source_type"
            source = data["sources"][0]
            assert "type" in source  # not "source_type"

    def test_load_rejects_wrong_schema_version(self):
        bad_json = '{"schema_version": 999, "project": "test"}'
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "bad.json"
            path.write_text(bad_json)
            with pytest.raises(ValueError, match="schema_version"):
                load_project(path)
