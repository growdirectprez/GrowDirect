"""Tests for spatial model validation."""
import pytest
from arc.model.spatial_model import Floor, Opening, Room, Wall
from arc.model.validator import validate_floor, ValidationError


def _make_floor(walls, rooms):
    return Floor(level=0, label="Ground", plate_height=8.0, z_origin=0.0,
                 rooms=rooms, walls=walls)


class TestWallValidation:
    def test_opening_exceeds_wall_length(self):
        wall = Wall(
            id="short-wall", from_pt=[0, 0], to_pt=[5, 0],
            wall_type="exterior", thickness_in=6,
            rooms={"interior": "r1", "exterior": None},
            openings=[Opening("door", position_along_wall=3.0, width=4.0,
                              height=6.67, sill_height=0.0)],
        )
        floor = _make_floor([wall], [])
        errors = validate_floor(floor)
        assert any("exceeds wall length" in e.message for e in errors)

    def test_opening_fits_wall(self):
        wall = Wall(
            id="long-wall", from_pt=[0, 0], to_pt=[20, 0],
            wall_type="exterior", thickness_in=6,
            rooms={"interior": "r1", "exterior": None},
            openings=[Opening("door", position_along_wall=3.0, width=3.0,
                              height=6.67, sill_height=0.0)],
        )
        floor = _make_floor([wall], [])
        errors = validate_floor(floor)
        assert len(errors) == 0

    def test_zero_length_wall(self):
        wall = Wall(
            id="zero-wall", from_pt=[5, 5], to_pt=[5, 5],
            wall_type="interior", thickness_in=4,
            rooms={"interior": "r1", "exterior": "r2"},
        )
        floor = _make_floor([wall], [])
        errors = validate_floor(floor)
        assert any("zero length" in e.message for e in errors)


class TestRoomValidation:
    def test_room_refs_missing_wall(self):
        room = Room(id="r1", label="Room", polygon=[[0,0],[10,0],[10,10],[0,10]],
                    wall_refs=["wall-missing"])
        floor = _make_floor([], [room])
        errors = validate_floor(floor)
        assert any("wall-missing" in e.message for e in errors)

    def test_room_refs_existing_wall(self):
        wall = Wall(id="w1", from_pt=[0,0], to_pt=[10,0],
                    wall_type="exterior", thickness_in=6,
                    rooms={"interior": "r1", "exterior": None})
        room = Room(id="r1", label="Room", polygon=[[0,0],[10,0],[10,10],[0,10]],
                    wall_refs=["w1"])
        floor = _make_floor([wall], [room])
        errors = validate_floor(floor)
        assert len(errors) == 0
