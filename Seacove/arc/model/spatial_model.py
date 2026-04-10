"""ARC spatial model data classes.

Coordinate system: X=East, Y=North, Z=Up.
All dimensions in feet. Fields ending in _in are in inches.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Supporting types
# ---------------------------------------------------------------------------

@dataclass
class CoordinateSystem:
    x: str          # e.g. "east"
    y: str          # e.g. "north"
    z: str          # e.g. "up"
    origin: str     # e.g. "SW corner of lot"


@dataclass
class Source:
    id: str
    source_type: str        # JSON key: "type"
    file: str
    page: Optional[int] = None
    notes: Optional[str] = None


@dataclass
class SourceRef:
    ref: str
    confidence: float = 1.0


@dataclass
class Conflict:
    description: str
    sources: list[str] = field(default_factory=list)
    resolution: Optional[str] = None


# ---------------------------------------------------------------------------
# Openings (doors, windows, pass-throughs)
# ---------------------------------------------------------------------------

@dataclass
class Opening:
    opening_type: str           # JSON key: "type" — "door", "window", etc.
    position_along_wall: float  # distance from wall start (ft)
    width: float
    height: float
    sill_height: float = 0.0
    label: Optional[str] = None
    sources: list[SourceRef] = field(default_factory=list)

    @property
    def end_position(self) -> float:
        """Far edge of the opening along the wall (ft)."""
        return self.position_along_wall + self.width


# ---------------------------------------------------------------------------
# Walls — top-level per floor (not nested in rooms)
# ---------------------------------------------------------------------------

@dataclass
class Wall:
    id: str
    from_pt: list[float]        # JSON key: "from" — [x, y]
    to_pt: list[float]          # JSON key: "to"   — [x, y]
    wall_type: str              # JSON key: "type" — "exterior", "interior"
    thickness_in: float         # inches
    rooms: dict                 # {"interior": room_id | None, "exterior": room_id | None}
    height: Optional[float] = None      # ft; if None, inherits floor plate_height
    openings: list[Opening] = field(default_factory=list)
    sources: list[SourceRef] = field(default_factory=list)
    conflicts: list[Conflict] = field(default_factory=list)

    @property
    def length_ft(self) -> float:
        dx = self.to_pt[0] - self.from_pt[0]
        dy = self.to_pt[1] - self.from_pt[1]
        return math.hypot(dx, dy)

    @property
    def thickness_ft(self) -> float:
        return self.thickness_in / 12.0

    @property
    def direction(self) -> tuple[float, float]:
        """Unit vector from from_pt to to_pt."""
        length = self.length_ft
        if length == 0:
            return (0.0, 0.0)
        dx = (self.to_pt[0] - self.from_pt[0]) / length
        dy = (self.to_pt[1] - self.from_pt[1]) / length
        return (dx, dy)


# ---------------------------------------------------------------------------
# Fixtures (appliances, built-ins inside rooms)
# ---------------------------------------------------------------------------

@dataclass
class Fixture:
    fixture_type: str           # JSON key: "type"
    position: list[float]       # [x, y]
    label: Optional[str] = None
    sources: list[SourceRef] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Rooms
# ---------------------------------------------------------------------------

@dataclass
class Room:
    id: str
    label: str
    polygon: list[list[float]]  # list of [x, y] vertices (closed implied)
    wall_refs: list[str]        # ids of Wall objects bounding this room
    fixtures: list[Fixture] = field(default_factory=list)
    sources: list[SourceRef] = field(default_factory=list)
    conflicts: list[Conflict] = field(default_factory=list)

    @property
    def area_sqft(self) -> float:
        """Shoelace formula for polygon area."""
        pts = self.polygon
        n = len(pts)
        if n < 3:
            return 0.0
        total = 0.0
        for i in range(n):
            x0, y0 = pts[i]
            x1, y1 = pts[(i + 1) % n]
            total += x0 * y1 - x1 * y0
        return abs(total) / 2.0


# ---------------------------------------------------------------------------
# Structural members
# ---------------------------------------------------------------------------

@dataclass
class Post:
    position: list[float]   # [x, y]
    size_in: float          # square section size in inches
    material: str = "douglas_fir"
    z_base: float = 0.0
    height: Optional[float] = None


@dataclass
class Beam:
    from_pt: list[float]    # JSON key: "from"
    to_pt: list[float]      # JSON key: "to"
    width_in: float
    depth_in: float
    z: float                # elevation at bottom of beam
    material: str = "douglas_fir"
    label: Optional[str] = None


@dataclass
class Structural:
    posts: list[Post] = field(default_factory=list)
    beams: list[Beam] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Roof
# ---------------------------------------------------------------------------

@dataclass
class RoofPlane:
    label: str
    roof_type: str          # JSON key: "type" — "flat", "gable", "hip", etc.
    slope: float            # rise/run
    overhang: float         # ft
    boundary: list[list[float]]
    z_base: float           # elevation at eave


@dataclass
class Roof:
    planes: list[RoofPlane] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Lot
# ---------------------------------------------------------------------------

@dataclass
class LotInfo:
    boundaries: list[list[float]]
    setbacks: dict[str, float]
    area_sqft: Optional[float] = None
    apn: Optional[str] = None


@dataclass
class Site:
    lot: LotInfo
    address: Optional[str] = None


# ---------------------------------------------------------------------------
# Floor
# ---------------------------------------------------------------------------

@dataclass
class Floor:
    level: int              # 0 = ground, 1 = first floor above grade, etc.
    label: str
    plate_height: float     # ft — wall height for this floor
    z_origin: float         # elevation of floor slab
    rooms: list[Room]
    walls: list[Wall]
    structural: Optional[Structural] = None


# ---------------------------------------------------------------------------
# Project (top-level)
# ---------------------------------------------------------------------------

@dataclass
class Project:
    schema_version: int
    project_name: str           # JSON key: "project"
    address: str
    coordinate_system: CoordinateSystem
    lot: LotInfo
    floors: list[Floor]
    sources: list[Source]
    structural: Optional[Structural] = None
    roof: Optional[Roof] = None
    conflicts: list[Conflict] = field(default_factory=list)
    notes: Optional[str] = None
