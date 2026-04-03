#!/usr/bin/env python3
"""Build Seacove spatial model from known dimensions in 25-Seacove-As-Built.rb.

This script manually constructs the Project dataclass from the hand-written
Ruby model, then serializes it to JSON for the ARC pipeline.

Usage:
    python3 scripts/create_seacove_model.py

Output:
    projects/seacove/model/spatial_model.json
"""
from pathlib import Path
import sys

# Ensure arc package is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from arc.model.spatial_model import (
    Beam,
    Conflict,
    CoordinateSystem,
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
from arc.model.serialization import save_project

ARC_ROOT = Path(__file__).parent.parent
OUTPUT_PATH = ARC_ROOT / "projects" / "seacove" / "model" / "spatial_model.json"

# ---------------------------------------------------------------------------
# Constants from 25-Seacove-As-Built.rb
# ---------------------------------------------------------------------------
PLATE_HEIGHT = 8.0   # line 38
WT = 0.5             # wall thickness in feet (6 inches) — line 39
WT_IN = 6.0          # wall thickness in inches


def make_source_ref(confidence: float = 0.8) -> list[SourceRef]:
    return [SourceRef(ref="as-built-rb", confidence=confidence)]


# ---------------------------------------------------------------------------
# Walls
# ---------------------------------------------------------------------------
def build_walls() -> list[Wall]:
    walls = []

    # --- South walls ---
    walls.append(Wall(
        id="wall_s_living",
        from_pt=[0.0, 0.0], to_pt=[28.0, 0.0],
        wall_type="exterior", thickness_in=WT_IN,
        rooms={"interior": "living_room", "exterior": None},
        openings=[
            Opening(
                opening_type="door",
                position_along_wall=14.0,
                width=3.0,
                height=7.0,
                sill_height=0.0,
                label="Front Door",
                sources=make_source_ref(),
            ),
        ],
        sources=make_source_ref(),
    ))
    walls.append(Wall(
        id="wall_s_bedrooms",
        from_pt=[28.0, 0.0], to_pt=[42.0, 0.0],
        wall_type="exterior", thickness_in=WT_IN,
        rooms={"interior": "bathroom2", "exterior": None},
        sources=make_source_ref(),
    ))

    # --- North walls ---
    walls.append(Wall(
        id="wall_n_living",
        from_pt=[0.0, 18.0], to_pt=[28.0, 18.0],
        wall_type="exterior", thickness_in=WT_IN,
        rooms={"interior": "living_room", "exterior": None},
        sources=make_source_ref(),
    ))
    walls.append(Wall(
        id="wall_n_bedrooms",
        from_pt=[18.0, 28.0], to_pt=[42.0, 28.0],
        wall_type="exterior", thickness_in=WT_IN,
        rooms={"interior": "bedroom1", "exterior": None},
        sources=make_source_ref(),
    ))

    # --- West wall ---
    walls.append(Wall(
        id="wall_west",
        from_pt=[0.0, 0.0], to_pt=[0.0, 18.0],
        wall_type="exterior", thickness_in=WT_IN,
        rooms={"interior": "living_room", "exterior": None},
        sources=make_source_ref(),
    ))

    # --- East wall ---
    walls.append(Wall(
        id="wall_east",
        from_pt=[42.0, 0.0], to_pt=[42.0, 28.0],
        wall_type="exterior", thickness_in=WT_IN,
        rooms={"interior": "bedroom2", "exterior": None},
        sources=make_source_ref(),
    ))

    # --- Connection wall (living to bedroom wing at X=18) ---
    walls.append(Wall(
        id="wall_connect",
        from_pt=[18.0, 0.0], to_pt=[18.0, 18.0],
        wall_type="interior", thickness_in=WT_IN,
        rooms={"interior": "living_room", "exterior": "bathroom"},
        sources=make_source_ref(),
    ))

    # --- Hall wall (Y=14, from X=18 to X=42) ---
    walls.append(Wall(
        id="wall_hall",
        from_pt=[18.0, 14.0], to_pt=[42.0, 14.0],
        wall_type="interior", thickness_in=WT_IN,
        rooms={"interior": "hall", "exterior": "bedroom1"},
        sources=make_source_ref(),
    ))

    # --- Bedroom dividers ---
    walls.append(Wall(
        id="wall_br1_divider",
        from_pt=[26.0, 14.0], to_pt=[26.0, 28.0],
        wall_type="interior", thickness_in=WT_IN,
        rooms={"interior": "bedroom1", "exterior": "bedroom2"},
        sources=make_source_ref(),
    ))
    walls.append(Wall(
        id="wall_br2_divider",
        from_pt=[34.0, 14.0], to_pt=[34.0, 28.0],
        wall_type="interior", thickness_in=WT_IN,
        rooms={"interior": "bedroom2", "exterior": "bedroom1"},
        sources=make_source_ref(),
    ))

    # --- Kitchen partition (Y=10, X=12 to X=18) ---
    walls.append(Wall(
        id="wall_kitchen",
        from_pt=[12.0, 10.0], to_pt=[18.0, 10.0],
        wall_type="interior", thickness_in=WT_IN,
        rooms={"interior": "kitchen", "exterior": "living_room"},
        sources=make_source_ref(),
    ))

    # --- Bathroom walls ---
    walls.append(Wall(
        id="wall_bath_south",
        from_pt=[18.0, 6.0], to_pt=[24.0, 6.0],
        wall_type="interior", thickness_in=WT_IN,
        rooms={"interior": "bathroom", "exterior": "hall"},
        sources=make_source_ref(),
    ))
    walls.append(Wall(
        id="wall_bath_west",
        from_pt=[24.0, 0.0], to_pt=[24.0, 14.0],
        wall_type="interior", thickness_in=WT_IN,
        rooms={"interior": "bathroom", "exterior": "bathroom2"},
        sources=make_source_ref(),
    ))

    # --- 1960 Addition walls ---
    walls.append(Wall(
        id="wall_add_north",
        from_pt=[5.0, 42.0], to_pt=[30.0, 42.0],
        wall_type="exterior", thickness_in=WT_IN,
        rooms={"interior": "addition_br1", "exterior": None},
        sources=make_source_ref(),
    ))
    walls.append(Wall(
        id="wall_add_west",
        from_pt=[5.0, 28.0], to_pt=[5.0, 42.0],
        wall_type="exterior", thickness_in=WT_IN,
        rooms={"interior": "addition_br1", "exterior": None},
        sources=make_source_ref(),
    ))
    walls.append(Wall(
        id="wall_add_east",
        from_pt=[30.0, 28.0], to_pt=[30.0, 42.0],
        wall_type="exterior", thickness_in=WT_IN,
        rooms={"interior": "addition_br2", "exterior": None},
        sources=make_source_ref(),
    ))
    walls.append(Wall(
        id="wall_add_divider",
        from_pt=[17.0, 28.0], to_pt=[17.0, 42.0],
        wall_type="interior", thickness_in=WT_IN,
        rooms={"interior": "addition_br1", "exterior": "addition_br2"},
        sources=make_source_ref(),
    ))
    walls.append(Wall(
        id="wall_add_bath",
        from_pt=[12.0, 35.0], to_pt=[17.0, 35.0],
        wall_type="interior", thickness_in=WT_IN,
        rooms={"interior": "addition_br1", "exterior": "addition_br1"},
        sources=make_source_ref(),
    ))

    # --- Garage walls ---
    walls.append(Wall(
        id="wall_gar_south",
        from_pt=[42.0, -2.0], to_pt=[62.0, -2.0],
        wall_type="exterior", thickness_in=WT_IN,
        rooms={"interior": "garage", "exterior": None},
        sources=make_source_ref(),
    ))
    walls.append(Wall(
        id="wall_gar_north",
        from_pt=[42.0, 16.0], to_pt=[62.0, 16.0],
        wall_type="exterior", thickness_in=WT_IN,
        rooms={"interior": "garage", "exterior": None},
        sources=make_source_ref(),
    ))
    walls.append(Wall(
        id="wall_gar_east",
        from_pt=[62.0, -2.0], to_pt=[62.0, 16.0],
        wall_type="exterior", thickness_in=WT_IN,
        rooms={"interior": "garage", "exterior": None},
        sources=make_source_ref(),
    ))

    return walls


# ---------------------------------------------------------------------------
# Rooms
# ---------------------------------------------------------------------------
def build_rooms() -> list[Room]:
    return [
        Room(
            id="living_room", label="Living Room",
            polygon=[[0, 0], [18, 0], [18, 18], [0, 18]],
            wall_refs=["wall_s_living", "wall_west", "wall_n_living", "wall_connect"],
            sources=make_source_ref(),
        ),
        Room(
            id="kitchen", label="Kitchen",
            polygon=[[12, 10], [18, 10], [18, 18], [12, 18]],
            wall_refs=["wall_kitchen", "wall_connect", "wall_n_living"],
            sources=make_source_ref(),
        ),
        Room(
            id="hall", label="Hall",
            polygon=[[18, 0], [42, 0], [42, 14], [18, 14]],
            wall_refs=["wall_s_bedrooms", "wall_hall", "wall_connect"],
            sources=make_source_ref(),
        ),
        Room(
            id="bathroom", label="Bathroom",
            polygon=[[18, 0], [24, 0], [24, 6], [18, 6]],
            wall_refs=["wall_bath_south", "wall_bath_west", "wall_connect"],
            sources=make_source_ref(),
        ),
        Room(
            id="bathroom2", label="Bathroom 2",
            polygon=[[24, 0], [42, 0], [42, 14], [24, 14]],
            wall_refs=["wall_s_bedrooms", "wall_bath_west", "wall_hall", "wall_east"],
            sources=make_source_ref(),
        ),
        Room(
            id="bedroom1", label="Bedroom 1",
            polygon=[[18, 14], [26, 14], [26, 28], [18, 28]],
            wall_refs=["wall_hall", "wall_br1_divider", "wall_n_bedrooms"],
            sources=make_source_ref(),
        ),
        Room(
            id="bedroom2", label="Bedroom 2",
            polygon=[[26, 14], [34, 14], [34, 28], [26, 28]],
            wall_refs=["wall_br1_divider", "wall_br2_divider", "wall_n_bedrooms"],
            sources=make_source_ref(),
        ),
        Room(
            id="garage", label="Garage",
            polygon=[[42, -2], [62, -2], [62, 16], [42, 16]],
            wall_refs=["wall_gar_south", "wall_gar_north", "wall_gar_east", "wall_east"],
            sources=make_source_ref(),
        ),
        Room(
            id="addition_br1", label="Addition BR1",
            polygon=[[5, 28], [17, 28], [17, 42], [5, 42]],
            wall_refs=["wall_add_north", "wall_add_west", "wall_add_divider"],
            sources=make_source_ref(),
        ),
        Room(
            id="addition_br2", label="Addition BR2",
            polygon=[[17, 28], [30, 28], [30, 42], [17, 42]],
            wall_refs=["wall_add_north", "wall_add_east", "wall_add_divider"],
            sources=make_source_ref(),
        ),
    ]


# ---------------------------------------------------------------------------
# Structural members
# ---------------------------------------------------------------------------
def build_structural() -> Structural:
    posts = []

    # South face posts (living wing) at X = 2, 8, 14, 20, 26
    for i in range(5):
        x = 2.0 + i * 6.0
        posts.append(Post(position=[x, 0.0], size_in=4.0, material="douglas_fir"))

    # North face posts (living wing) at same X positions, Y=18
    for i in range(5):
        x = 2.0 + i * 6.0
        posts.append(Post(position=[x, 18.0], size_in=4.0, material="douglas_fir"))

    # Corner posts
    for pos in [[42, 0], [42, 14], [42, 28], [18, 28], [0, 0], [0, 18]]:
        posts.append(Post(
            position=[float(pos[0]), float(pos[1])],
            size_in=4.0,
            material="douglas_fir",
        ))

    beams = [
        # Ridge beam - living wing (E-W)
        Beam(
            from_pt=[-2.0, 9.0], to_pt=[30.0, 9.0],
            width_in=4.0, depth_in=10.0,
            z=PLATE_HEIGHT,
            material="douglas_fir",
            label="Ridge Beam - Living Wing",
        ),
        # Ridge beam - bedroom wing (E-W)
        Beam(
            from_pt=[18.0, 14.0], to_pt=[44.0, 14.0],
            width_in=4.0, depth_in=10.0,
            z=PLATE_HEIGHT,
            material="douglas_fir",
            label="Ridge Beam - Bedroom Wing",
        ),
    ]

    return Structural(posts=posts, beams=beams)


# ---------------------------------------------------------------------------
# Roof
# ---------------------------------------------------------------------------
def build_roof() -> Roof:
    return Roof(planes=[
        RoofPlane(
            label="Living Wing Roof",
            roof_type="flat",
            slope=0.02,
            overhang=3.5,
            boundary=[[0, 0], [28, 0], [28, 18], [0, 18]],
            z_base=PLATE_HEIGHT + 10.0 / 12.0,  # plate + beam depth
        ),
        RoofPlane(
            label="Bedroom Wing Roof",
            roof_type="flat",
            slope=0.02,
            overhang=3.5,
            boundary=[[18, 0], [42, 0], [42, 28], [18, 28]],
            z_base=PLATE_HEIGHT + 10.0 / 12.0 - 0.3,
        ),
        RoofPlane(
            label="Addition Roof",
            roof_type="flat",
            slope=0.02,
            overhang=3.5,
            boundary=[[5, 28], [30, 28], [30, 42], [5, 42]],
            z_base=PLATE_HEIGHT + 0.3,
        ),
        RoofPlane(
            label="Garage Roof",
            roof_type="flat",
            slope=0.02,
            overhang=3.5,
            boundary=[[42, -2], [62, -2], [62, 16], [42, 16]],
            z_base=PLATE_HEIGHT - 0.5,
        ),
    ])


# ---------------------------------------------------------------------------
# Build the full Project
# ---------------------------------------------------------------------------
def build_project() -> Project:
    walls = build_walls()
    rooms = build_rooms()
    structural = build_structural()
    roof = build_roof()

    floor = Floor(
        level=0,
        label="Ground Floor",
        plate_height=PLATE_HEIGHT,
        z_origin=0.0,
        rooms=rooms,
        walls=walls,
        structural=structural,
    )

    return Project(
        schema_version=1,
        project_name="seacove",
        address="25 Sea Cove Drive, Rancho Palos Verdes, CA 90275",
        coordinate_system=CoordinateSystem(
            x="east", y="north", z="up",
            origin="SW corner of original house",
        ),
        lot=LotInfo(
            boundaries=[],  # Not modeled yet
            setbacks={"front": 20.0, "side": 5.0, "rear": 15.0},
            apn="7585-021-069",
        ),
        floors=[floor],
        sources=[
            Source(
                id="as-built-rb",
                source_type="ruby_script",
                file="25-Seacove-As-Built.rb",
                notes="Hand-coded SketchUp Ruby model — reference for spatial model",
            ),
            Source(
                id="original-blueprints",
                source_type="blueprint",
                file="25 Seacove Blueprints/",
                notes="1958 original Douglas Rucker drawings",
            ),
            Source(
                id="dim-reference",
                source_type="document",
                file="blueprint-dimensions-reference.md",
                notes="Compiled dimension reference from blueprint analysis",
            ),
        ],
        roof=roof,
        notes=(
            "V0 model built from hand-coded Ruby script dimensions. "
            "Garage is east of main house at offset (42, -2). "
            "1960 addition is north at offset (5, 28)."
        ),
    )


def main():
    project = build_project()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    save_project(project, OUTPUT_PATH)
    print(f"Saved spatial model to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
