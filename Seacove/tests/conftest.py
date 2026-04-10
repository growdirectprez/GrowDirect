"""Shared pytest fixtures for ARC tests."""
import pytest
from arc.model.spatial_model import (
    Beam,
    CoordinateSystem,
    Fixture,
    Floor,
    LotInfo,
    Opening,
    Post,
    Project,
    Roof,
    RoofPlane,
    Room,
    Source,
    SourceRef,
    Structural,
    Wall,
)


@pytest.fixture
def sample_project() -> Project:
    """Minimal but complete project for generation tests.

    Layout:
      wall-south: E-W from [0,0] to [28,0], has a door at 14.0ft
      wall-east:  N-S from [28,0] to [28,18], has a window at 6.0ft
    """
    wall_south = Wall(
        id="wall-south",
        from_pt=[0.0, 0.0],
        to_pt=[28.0, 0.0],
        wall_type="exterior",
        thickness_in=6.0,
        rooms={"interior": "living-01", "exterior": None},
        openings=[
            Opening(
                opening_type="door",
                position_along_wall=14.0,
                width=3.0,
                height=6.67,
                sill_height=0.0,
                label="Front Door",
            )
        ],
        sources=[SourceRef(ref="as-built", confidence=0.95)],
    )
    wall_east = Wall(
        id="wall-east",
        from_pt=[28.0, 0.0],
        to_pt=[28.0, 18.0],
        wall_type="exterior",
        thickness_in=6.0,
        rooms={"interior": "living-01", "exterior": None},
        openings=[
            Opening(
                opening_type="window",
                position_along_wall=6.0,
                width=4.0,
                height=4.0,
                sill_height=3.0,
                label="East Window",
            )
        ],
    )
    room = Room(
        id="living-01",
        label="Living Room",
        polygon=[[0, 0], [28, 0], [28, 18], [0, 18]],
        wall_refs=["wall-south", "wall-east"],
        fixtures=[Fixture(fixture_type="fireplace", position=[2, 9])],
    )
    floor = Floor(
        level=0,
        label="Ground Floor",
        plate_height=8.0,
        z_origin=0.0,
        rooms=[room],
        walls=[wall_south, wall_east],
    )
    return Project(
        schema_version=1,
        project_name="test-project",
        address="25 Seacove Dr, RPV",
        coordinate_system=CoordinateSystem(
            x="east", y="north", z="up", origin="SW corner of lot"
        ),
        lot=LotInfo(
            boundaries=[[0, 0], [80, 0], [80, 60], [0, 60]],
            setbacks={"front": 20, "rear": 15, "side_left": 5, "side_right": 5},
        ),
        floors=[floor],
        sources=[
            Source(
                id="as-built",
                source_type="blueprint",
                file="inputs/plan.pdf",
                page=1,
            )
        ],
        structural=Structural(
            posts=[Post(position=[2.0, 0.0], size_in=4.0, material="douglas_fir")],
            beams=[
                Beam(
                    from_pt=[-2.0, 9.0],
                    to_pt=[30.0, 9.0],
                    width_in=4.0,
                    depth_in=10.0,
                    z=8.0,
                    label="Ridge Beam",
                )
            ],
        ),
        roof=Roof(
            planes=[
                RoofPlane(
                    label="Living Wing",
                    roof_type="flat",
                    slope=0.25,
                    overhang=3.5,
                    boundary=[[0, 0], [28, 0], [28, 18], [0, 18]],
                    z_base=8.83,
                )
            ]
        ),
    )
