"""ARC spatial model JSON serialization — save/load with schema versioning.

JSON key mapping (Python → JSON):
  project_name  → "project"
  wall_type     → "type"
  from_pt       → "from"
  to_pt         → "to"
  opening_type  → "type"
  fixture_type  → "type"
  roof_type     → "type"
  source_type   → "type"

DO NOT use dataclasses.asdict for types with field name remapping.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from arc.model.spatial_model import (
    Beam,
    Conflict,
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

SUPPORTED_SCHEMA_VERSIONS = {1}


# ---------------------------------------------------------------------------
# Serialization helpers (_to_dict)
# ---------------------------------------------------------------------------

def _source_ref_to_dict(sr: SourceRef) -> dict:
    return {"ref": sr.ref, "confidence": sr.confidence}


def _conflict_to_dict(c: Conflict) -> dict:
    d: dict = {"description": c.description, "sources": c.sources}
    if c.resolution is not None:
        d["resolution"] = c.resolution
    return d


def _opening_to_dict(o: Opening) -> dict:
    d: dict = {
        "type": o.opening_type,
        "position_along_wall": o.position_along_wall,
        "width": o.width,
        "height": o.height,
        "sill_height": o.sill_height,
    }
    if o.label is not None:
        d["label"] = o.label
    if o.sources:
        d["sources"] = [_source_ref_to_dict(s) for s in o.sources]
    return d


def _fixture_to_dict(f: Fixture) -> dict:
    d: dict = {"type": f.fixture_type, "position": f.position}
    if f.label is not None:
        d["label"] = f.label
    if f.sources:
        d["sources"] = [_source_ref_to_dict(s) for s in f.sources]
    return d


def _wall_to_dict(w: Wall) -> dict:
    d: dict = {
        "id": w.id,
        "type": w.wall_type,
        "from": w.from_pt,
        "to": w.to_pt,
        "thickness_in": w.thickness_in,
        "rooms": w.rooms,
    }
    if w.height is not None:
        d["height"] = w.height
    if w.openings:
        d["openings"] = [_opening_to_dict(o) for o in w.openings]
    if w.sources:
        d["sources"] = [_source_ref_to_dict(s) for s in w.sources]
    if w.conflicts:
        d["conflicts"] = [_conflict_to_dict(c) for c in w.conflicts]
    return d


def _room_to_dict(r: Room) -> dict:
    d: dict = {
        "id": r.id,
        "label": r.label,
        "polygon": r.polygon,
        "wall_refs": r.wall_refs,
    }
    if r.fixtures:
        d["fixtures"] = [_fixture_to_dict(f) for f in r.fixtures]
    if r.sources:
        d["sources"] = [_source_ref_to_dict(s) for s in r.sources]
    if r.conflicts:
        d["conflicts"] = [_conflict_to_dict(c) for c in r.conflicts]
    return d


def _post_to_dict(p: Post) -> dict:
    d: dict = {
        "position": p.position,
        "size_in": p.size_in,
        "material": p.material,
        "z_base": p.z_base,
    }
    if p.height is not None:
        d["height"] = p.height
    return d


def _beam_to_dict(b: Beam) -> dict:
    d: dict = {
        "from": b.from_pt,
        "to": b.to_pt,
        "width_in": b.width_in,
        "depth_in": b.depth_in,
        "z": b.z,
        "material": b.material,
    }
    if b.label is not None:
        d["label"] = b.label
    return d


def _structural_to_dict(s: Structural) -> dict:
    return {
        "posts": [_post_to_dict(p) for p in s.posts],
        "beams": [_beam_to_dict(b) for b in s.beams],
    }


def _roof_plane_to_dict(rp: RoofPlane) -> dict:
    return {
        "label": rp.label,
        "type": rp.roof_type,
        "slope": rp.slope,
        "overhang": rp.overhang,
        "boundary": rp.boundary,
        "z_base": rp.z_base,
    }


def _roof_to_dict(r: Roof) -> dict:
    return {"planes": [_roof_plane_to_dict(rp) for rp in r.planes]}


def _floor_to_dict(f: Floor) -> dict:
    d: dict = {
        "level": f.level,
        "label": f.label,
        "plate_height": f.plate_height,
        "z_origin": f.z_origin,
        "rooms": [_room_to_dict(r) for r in f.rooms],
        "walls": [_wall_to_dict(w) for w in f.walls],
    }
    if f.structural is not None:
        d["structural"] = _structural_to_dict(f.structural)
    return d


def _coordinate_system_to_dict(cs: CoordinateSystem) -> dict:
    return {"x": cs.x, "y": cs.y, "z": cs.z, "origin": cs.origin}


def _lot_info_to_dict(lot: LotInfo) -> dict:
    d: dict = {"boundaries": lot.boundaries, "setbacks": lot.setbacks}
    if lot.area_sqft is not None:
        d["area_sqft"] = lot.area_sqft
    if lot.apn is not None:
        d["apn"] = lot.apn
    return d


def _source_to_dict(s: Source) -> dict:
    d: dict = {
        "id": s.id,
        "type": s.source_type,
        "file": s.file,
    }
    if s.page is not None:
        d["page"] = s.page
    if s.notes is not None:
        d["notes"] = s.notes
    return d


def project_to_dict(project: Project) -> dict:
    d: dict = {
        "schema_version": project.schema_version,
        "project": project.project_name,
        "address": project.address,
        "coordinate_system": _coordinate_system_to_dict(project.coordinate_system),
        "lot": _lot_info_to_dict(project.lot),
        "structure": {
            "floors": [_floor_to_dict(f) for f in project.floors],
        },
        "sources": [_source_to_dict(s) for s in project.sources],
    }
    if project.structural is not None:
        d["structural"] = _structural_to_dict(project.structural)
    if project.roof is not None:
        d["roof"] = _roof_to_dict(project.roof)
    if project.conflicts:
        d["conflicts"] = [_conflict_to_dict(c) for c in project.conflicts]
    if project.notes is not None:
        d["notes"] = project.notes
    return d


# ---------------------------------------------------------------------------
# Deserialization helpers (_dict_to_*)
# ---------------------------------------------------------------------------

def _dict_to_source_ref(d: dict) -> SourceRef:
    return SourceRef(ref=d["ref"], confidence=d.get("confidence", 1.0))


def _dict_to_conflict(d: dict) -> Conflict:
    return Conflict(
        description=d["description"],
        sources=d.get("sources", []),
        resolution=d.get("resolution"),
    )


def _dict_to_opening(d: dict) -> Opening:
    return Opening(
        opening_type=d["type"],
        position_along_wall=d["position_along_wall"],
        width=d["width"],
        height=d["height"],
        sill_height=d.get("sill_height", 0.0),
        label=d.get("label"),
        sources=[_dict_to_source_ref(s) for s in d.get("sources", [])],
    )


def _dict_to_fixture(d: dict) -> Fixture:
    return Fixture(
        fixture_type=d["type"],
        position=d["position"],
        label=d.get("label"),
        sources=[_dict_to_source_ref(s) for s in d.get("sources", [])],
    )


def _dict_to_wall(d: dict) -> Wall:
    return Wall(
        id=d["id"],
        wall_type=d["type"],
        from_pt=d["from"],
        to_pt=d["to"],
        thickness_in=d["thickness_in"],
        rooms=d["rooms"],
        height=d.get("height"),
        openings=[_dict_to_opening(o) for o in d.get("openings", [])],
        sources=[_dict_to_source_ref(s) for s in d.get("sources", [])],
        conflicts=[_dict_to_conflict(c) for c in d.get("conflicts", [])],
    )


def _dict_to_room(d: dict) -> Room:
    return Room(
        id=d["id"],
        label=d["label"],
        polygon=d["polygon"],
        wall_refs=d.get("wall_refs", []),
        fixtures=[_dict_to_fixture(f) for f in d.get("fixtures", [])],
        sources=[_dict_to_source_ref(s) for s in d.get("sources", [])],
        conflicts=[_dict_to_conflict(c) for c in d.get("conflicts", [])],
    )


def _dict_to_post(d: dict) -> Post:
    return Post(
        position=d["position"],
        size_in=d["size_in"],
        material=d.get("material", "douglas_fir"),
        z_base=d.get("z_base", 0.0),
        height=d.get("height"),
    )


def _dict_to_beam(d: dict) -> Beam:
    return Beam(
        from_pt=d["from"],
        to_pt=d["to"],
        width_in=d["width_in"],
        depth_in=d["depth_in"],
        z=d["z"],
        material=d.get("material", "douglas_fir"),
        label=d.get("label"),
    )


def _dict_to_structural(d: dict) -> Structural:
    return Structural(
        posts=[_dict_to_post(p) for p in d.get("posts", [])],
        beams=[_dict_to_beam(b) for b in d.get("beams", [])],
    )


def _dict_to_roof_plane(d: dict) -> RoofPlane:
    return RoofPlane(
        label=d["label"],
        roof_type=d["type"],
        slope=d["slope"],
        overhang=d["overhang"],
        boundary=d["boundary"],
        z_base=d["z_base"],
    )


def _dict_to_roof(d: dict) -> Roof:
    return Roof(planes=[_dict_to_roof_plane(rp) for rp in d.get("planes", [])])


def _dict_to_floor(d: dict) -> Floor:
    structural = None
    if "structural" in d:
        structural = _dict_to_structural(d["structural"])
    return Floor(
        level=d["level"],
        label=d["label"],
        plate_height=d["plate_height"],
        z_origin=d["z_origin"],
        rooms=[_dict_to_room(r) for r in d.get("rooms", [])],
        walls=[_dict_to_wall(w) for w in d.get("walls", [])],
        structural=structural,
    )


def _dict_to_coordinate_system(d: dict) -> CoordinateSystem:
    return CoordinateSystem(x=d["x"], y=d["y"], z=d["z"], origin=d["origin"])


def _dict_to_lot_info(d: dict) -> LotInfo:
    return LotInfo(
        boundaries=d["boundaries"],
        setbacks=d["setbacks"],
        area_sqft=d.get("area_sqft"),
        apn=d.get("apn"),
    )


def _dict_to_source(d: dict) -> Source:
    return Source(
        id=d["id"],
        source_type=d["type"],
        file=d["file"],
        page=d.get("page"),
        notes=d.get("notes"),
    )


def dict_to_project(d: dict) -> Project:
    version = d.get("schema_version")
    if version not in SUPPORTED_SCHEMA_VERSIONS:
        raise ValueError(
            f"Unsupported schema_version: {version!r}. "
            f"Supported: {sorted(SUPPORTED_SCHEMA_VERSIONS)}"
        )

    structural = None
    if "structural" in d:
        structural = _dict_to_structural(d["structural"])

    roof = None
    if "roof" in d:
        roof = _dict_to_roof(d["roof"])

    structure = d.get("structure", {})
    floors = [_dict_to_floor(f) for f in structure.get("floors", [])]

    return Project(
        schema_version=version,
        project_name=d["project"],
        address=d.get("address", ""),
        coordinate_system=_dict_to_coordinate_system(d["coordinate_system"]),
        lot=_dict_to_lot_info(d["lot"]),
        floors=floors,
        sources=[_dict_to_source(s) for s in d.get("sources", [])],
        structural=structural,
        roof=roof,
        conflicts=[_dict_to_conflict(c) for c in d.get("conflicts", [])],
        notes=d.get("notes"),
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def save_project(project: Project, path: Path) -> None:
    """Serialize project to JSON file."""
    data = project_to_dict(project)
    path.write_text(json.dumps(data, indent=2))


def load_project(path: Path) -> Project:
    """Deserialize project from JSON file. Raises ValueError for unknown schema versions."""
    data = json.loads(path.read_text())
    return dict_to_project(data)
