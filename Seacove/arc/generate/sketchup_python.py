"""ARC Python assembler — generates Trimble MCP build_model code from spatial_model.

One build_model call per assembly stage. Each stage registers its ComponentDefinitions
and places instances. The snapshot after each call verifies geometry before the next
stage begins.

Assembly stages (in construction order):
    1. structural   — posts and beams from spatial_model structural data
    2. framing      — wall stud assemblies (king studs, plates, headers)
    3. openings     — door and window components (inner-loop cutouts)
    4. roof         — roof planes, rafters, ridge beam
    5. camera       — set camera position + save_model boilerplate

Usage:
    from arc.model.serialization import load_project
    from arc.generate.sketchup_python import generate_stage_code

    project = load_project(Path("projects/seacove/model/spatial_model.json"))
    code = generate_stage_code(project, stage="structural")
    # → pass code to mcp__...__build_model(code=code)
"""
from __future__ import annotations

import math
from pathlib import Path
from typing import Optional

from arc.model.spatial_model import Project, Post, Beam, Wall, Floor

FT_TO_IN = 12.0   # multiply feet by this to get inches


# ---------------------------------------------------------------------------
# Camera boilerplate (appended to every stage's code block)
# ---------------------------------------------------------------------------

def _camera_code(
    eye_x: float, eye_y: float, eye_z: float,
    target_x: float, target_y: float, target_z: float,
) -> str:
    """Generate camera-setting code (all coords in inches)."""
    return f"""\
# Camera
_cam = Camera()
_cam.enable_perspective(True)
_cam.set_perspective_frustum_fov(35.0)
_cam.set_orientation(
    SUPoint3D({eye_x:.1f}, {eye_y:.1f}, {eye_z:.1f}),
    SUPoint3D({target_x:.1f}, {target_y:.1f}, {target_z:.1f}),
    SUVector3D(0, 0, 1),
)
model.set_camera(_cam)
"""


def _default_camera_for_project(project: Project) -> str:
    """Compute a reasonable isometric camera from the project bounding box."""
    # Collect all wall endpoints to get rough extents
    all_x, all_y = [0.0], [0.0]
    for fl in project.floors:
        for wall in fl.walls:
            all_x += [wall.from_pt[0], wall.to_pt[0]]
            all_y += [wall.from_pt[1], wall.to_pt[1]]

    cx = (min(all_x) + max(all_x)) / 2.0 * FT_TO_IN
    cy = (min(all_y) + max(all_y)) / 2.0 * FT_TO_IN
    extent = max(max(all_x) - min(all_x), max(all_y) - min(all_y)) * FT_TO_IN
    eye_offset = extent * 1.5

    return _camera_code(
        eye_x=cx - eye_offset,
        eye_y=cy - eye_offset,
        eye_z=eye_offset * 0.8,
        target_x=cx,
        target_y=cy,
        target_z=0,
    )


# ---------------------------------------------------------------------------
# Stage: structural
# ---------------------------------------------------------------------------

def _structural_stage(project: Project) -> str:
    """Generate Python code to place all posts and beams from spatial_model."""
    from arc.components import ComponentRegistry
    from arc.components.structural import post_from_model, beam_from_model

    reg = ComponentRegistry()
    placements: list[dict] = []

    # Collect from project-level structural
    sources = []
    if project.structural:
        sources.append((project.structural, 0.0))  # project-level, z_base=0

    for fl in project.floors:
        if fl.structural:
            sources.append((fl.structural, fl.z_origin))

    post_idx = 0
    beam_idx = 0

    for structural, z_base_ft in sources:
        for model_post in structural.posts:
            # Determine plate height for this post
            plate_ht = 8.0
            for fl in project.floors:
                if fl.structural and model_post in fl.structural.posts:
                    plate_ht = fl.plate_height
                    break
            spec = post_from_model(model_post, plate_ht, reg)
            tx = model_post.position[0] * FT_TO_IN
            ty = model_post.position[1] * FT_TO_IN
            tz = (model_post.z_base + z_base_ft) * FT_TO_IN
            placements.append({
                "component": spec.name,
                "tx": tx, "ty": ty, "tz": tz,
                "name": f"post_{post_idx:03d}",
            })
            post_idx += 1

        for model_beam in structural.beams:
            spec = beam_from_model(model_beam, reg)
            # Beam origin = left end (from_pt), bottom face
            tx = model_beam.from_pt[0] * FT_TO_IN
            ty = model_beam.from_pt[1] * FT_TO_IN
            tz = (model_beam.z + z_base_ft) * FT_TO_IN

            # Compute rotation so beam points from from_pt to to_pt
            dx = model_beam.to_pt[0] - model_beam.from_pt[0]
            dy = model_beam.to_pt[1] - model_beam.from_pt[1]
            rot = math.degrees(math.atan2(dy, dx))

            placements.append({
                "component": spec.name,
                "tx": tx, "ty": ty, "tz": tz,
                "rotation_z_deg": rot,
                "name": f"beam_{beam_idx:03d}",
            })
            beam_idx += 1

    if not placements:
        return "# No structural members found in spatial model.\nresult = {'placed': 0}"

    lines = [
        "# ── ARC Stage: structural ────────────────────────────────",
        "# Component definitions",
        reg.all_definition_code(categories=["structural"]),
        "",
        "# Instance placement",
        reg.instance_placement_code(placements),
        "",
        _default_camera_for_project(project),
        f"result = {{'stage': 'structural', 'posts': {post_idx}, 'beams': {beam_idx}}}",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Stage: framing
# ---------------------------------------------------------------------------

def _framing_stage(project: Project) -> str:
    """Generate Python code to frame all walls from spatial_model.

    For each wall:
    - Bottom plate (single, full wall length)
    - Top plates (double — two layers)
    - King studs at each end
    - Studs at 16" or 24" o.c. between king studs
    - Headers + cripple studs over each opening
    - Jack studs flanking each opening
    """
    from arc.components import ComponentRegistry
    from arc.components.framing import (
        stud, plate, header, cripple, blocking
    )

    reg = ComponentRegistry()
    placements: list[dict] = []

    for fl in project.floors:
        plate_ht_in = fl.plate_height * FT_TO_IN
        z_in = fl.z_origin * FT_TO_IN

        for wall in fl.walls:
            _frame_wall(wall, fl.plate_height, fl.z_origin, reg, placements)

    if not placements:
        return "# No walls found in spatial model.\nresult = {'placed': 0}"

    lines = [
        "# ── ARC Stage: framing ───────────────────────────────────",
        "# Component definitions",
        reg.all_definition_code(categories=["framing"]),
        "",
        "# Instance placement",
        reg.instance_placement_code(placements),
        "",
        _default_camera_for_project(project),
        f"result = {{'stage': 'framing', 'placements': {len(placements)}}}",
    ]
    return "\n".join(lines)


def _frame_wall(
    wall: Wall,
    plate_height_ft: float,
    z_origin_ft: float,
    reg: ComponentRegistry,
    placements: list[dict],
    stud_spacing_in: float = 16.0,
) -> None:
    """Add framing placements for a single wall."""
    from arc.components.framing import stud as make_stud, plate as make_plate
    from arc.components.framing import header as make_header, cripple as make_cripple

    from_pt = wall.from_pt
    to_pt = wall.to_pt
    length_ft = wall.length_ft
    length_in = length_ft * FT_TO_IN

    # Nominal size based on wall type
    nominal = "2x6" if wall.wall_type == "exterior" else "2x4"
    plate_ht_in = plate_height_ft * FT_TO_IN
    z_base_in = z_origin_ft * FT_TO_IN

    # Wall direction vector (unit)
    dx = (to_pt[0] - from_pt[0]) / length_ft
    dy = (to_pt[1] - from_pt[1]) / length_ft
    rot_deg = math.degrees(math.atan2(dy, dx))

    def world_at(along_in: float, z_in: float = 0.0) -> tuple[float, float, float]:
        """World coords (inches) at distance along_in from wall start, height z_in."""
        fx = from_pt[0] * FT_TO_IN + dx * along_in
        fy = from_pt[1] * FT_TO_IN + dy * along_in
        return fx, fy, z_base_in + z_in

    # ── Plates ──────────────────────────────────────────────────────
    bot_plate = make_plate(nominal, length_in, reg, label="bottom_plate")
    top_plate1 = make_plate(nominal, length_in, reg, label="top_plate")
    top_plate2 = make_plate(nominal, length_in, reg, label="top_plate")

    from arc.components.framing import ACTUAL_SIZES
    plate_thickness_in = ACTUAL_SIZES[nominal][0]  # 1.5"

    wx, wy, wz = world_at(0, 0)
    placements.append({"component": bot_plate.name, "tx": wx, "ty": wy, "tz": wz,
                        "rotation_z_deg": rot_deg})
    wx, wy, wz = world_at(0, plate_ht_in - plate_thickness_in * 2)
    placements.append({"component": top_plate1.name, "tx": wx, "ty": wy, "tz": wz,
                        "rotation_z_deg": rot_deg})
    wx, wy, wz = world_at(0, plate_ht_in - plate_thickness_in)
    placements.append({"component": top_plate2.name, "tx": wx, "ty": wy, "tz": wz,
                        "rotation_z_deg": rot_deg})

    # Stud height = plate height minus top two plates and bottom plate
    stud_ht_in = plate_ht_in - plate_thickness_in * 3

    # ── Map openings along the wall ──────────────────────────────────
    # Sort openings by position
    openings_sorted = sorted(wall.openings, key=lambda o: o.position_along_wall)

    # Regions of full-height studs (between openings)
    full_stud_regions: list[tuple[float, float]] = []
    prev_end = 0.0
    for opening in openings_sorted:
        pos_in = opening.position_along_wall * FT_TO_IN
        end_in = opening.end_position * FT_TO_IN
        if pos_in > prev_end:
            full_stud_regions.append((prev_end, pos_in))
        prev_end = end_in
    if prev_end < length_in:
        full_stud_regions.append((prev_end, length_in))

    # ── Studs in full-height regions ────────────────────────────────
    s = make_stud(nominal, stud_ht_in, reg)
    for (region_start, region_end) in full_stud_regions:
        # King stud at region start
        wx, wy, wz = world_at(region_start, plate_thickness_in)
        placements.append({"component": s.name, "tx": wx, "ty": wy, "tz": wz,
                            "rotation_z_deg": rot_deg})
        # Studs at spacing
        pos = region_start + stud_spacing_in
        while pos < region_end - stud_spacing_in * 0.5:
            wx, wy, wz = world_at(pos, plate_thickness_in)
            placements.append({"component": s.name, "tx": wx, "ty": wy, "tz": wz,
                                "rotation_z_deg": rot_deg})
            pos += stud_spacing_in

    # ── Headers + jack/cripple studs for openings ──────────────────
    from arc.components.framing import ACTUAL_SIZES as _SIZES
    stud_actual_w = _SIZES[nominal][0]

    for opening in openings_sorted:
        pos_in = opening.position_along_wall * FT_TO_IN
        end_in = opening.end_position * FT_TO_IN
        op_width_in = opening.width * FT_TO_IN
        op_height_in = opening.height * FT_TO_IN
        sill_in = opening.sill_height * FT_TO_IN

        # Jack stud height = sill height (doors: full height to header)
        jack_ht_in = sill_in if opening.opening_type == "window" else op_height_in

        # Header
        header_ht_in = min(stud_ht_in - jack_ht_in, 9.25)  # up to 2×10 default
        hdr = make_header(op_width_in, header_ht_in, registry=reg)

        wx, wy, wz = world_at(pos_in, plate_thickness_in + jack_ht_in)
        placements.append({"component": hdr.name, "tx": wx, "ty": wy, "tz": wz,
                            "rotation_z_deg": rot_deg})

        # Jack studs (flanking opening)
        if jack_ht_in > 0:
            jack = make_stud(nominal, jack_ht_in, reg)
            for x_off in [pos_in, end_in]:
                wx, wy, wz = world_at(x_off, plate_thickness_in)
                placements.append({"component": jack.name, "tx": wx, "ty": wy, "tz": wz,
                                    "rotation_z_deg": rot_deg})

        # Cripple studs above header
        cripple_ht_in = stud_ht_in - jack_ht_in - header_ht_in
        if cripple_ht_in > 1.5:
            crip = make_cripple(nominal, cripple_ht_in, reg)
            cripple_z = plate_thickness_in + jack_ht_in + header_ht_in
            crip_pos = pos_in + stud_spacing_in
            while crip_pos < end_in - stud_spacing_in * 0.5:
                wx, wy, wz = world_at(crip_pos, cripple_z)
                placements.append({"component": crip.name, "tx": wx, "ty": wy, "tz": wz,
                                    "rotation_z_deg": rot_deg})
                crip_pos += stud_spacing_in


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

STAGES = ("structural", "framing")


def generate_stage_code(project: Project, stage: str) -> str:
    """Generate Python code for one assembly stage.

    Args:
        project: loaded Project from spatial_model.json
        stage:   one of STAGES ("structural", "framing")

    Returns:
        Python code string ready to pass to Trimble MCP build_model.
    """
    if stage not in STAGES:
        raise ValueError(f"Unknown stage: {stage!r}. Available: {STAGES}")

    if stage == "structural":
        return _structural_stage(project)
    if stage == "framing":
        return _framing_stage(project)

    raise NotImplementedError(f"Stage {stage!r} not yet implemented")


def generate_all_stages(project: Project) -> dict[str, str]:
    """Generate code for all stages. Returns {stage_name: code_string}."""
    return {stage: generate_stage_code(project, stage) for stage in STAGES}
