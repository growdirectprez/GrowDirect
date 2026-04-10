"""SketchUp Ruby script generator — renders Jinja2 templates from a spatial model.

Key design principle: all geometry (opening cut positions, roof overhang expansion)
is computed HERE before passing flat pre-computed values to Jinja2. Templates do
NOT compute geometry.
"""
from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader

from arc.model.spatial_model import (
    Beam,
    Floor,
    Opening,
    Post,
    Project,
    RoofPlane,
    Structural,
    Wall,
)

_TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates" / "ruby"


# ---------------------------------------------------------------------------
# Name helpers
# ---------------------------------------------------------------------------

def _module_name(project_name: str) -> str:
    """Convert project slug to Ruby module name.

    Examples:
        "seacove"       → "SeacoveHelpers"
        "test-project"  → "TestProjectHelpers"
        "25_seacove"    → "SeacoveHelpers"  (leading digits stripped)
    """
    # Split on non-alphanumeric chars
    parts = re.split(r"[^a-zA-Z0-9]+", project_name)
    # Drop empty parts and leading all-digit parts
    parts = [p for p in parts if p and not p.isdigit()]
    return "".join(p.capitalize() for p in parts) + "Helpers"


# ---------------------------------------------------------------------------
# Opening cut geometry
# ---------------------------------------------------------------------------

def _compute_opening_cut(wall: Wall, opening: Opening) -> dict[str, Any]:
    """Compute the axis-aligned bounding box for a boolean subtraction cutter.

    For E-W walls (abs(dx) >= abs(dy)):
        cut_w = opening width along X axis
        cut_d = wall thickness along Y axis

    For N-S walls (abs(dy) > abs(dx)):
        cut_w = wall thickness along X axis
        cut_d = opening width along Y axis

    The cutter origin (cut_x, cut_y) is positioned at the sill corner so that
    make_box(group, cut_x, cut_y, z_sill, cut_w, cut_d, height) subtracts correctly.
    """
    dx = wall.to_pt[0] - wall.from_pt[0]
    dy = wall.to_pt[1] - wall.from_pt[1]
    thickness_ft = wall.thickness_ft

    # Unit direction vector
    length = math.hypot(dx, dy)
    ux = dx / length if length > 0 else 1.0
    uy = dy / length if length > 0 else 0.0

    # Position along wall to the opening start
    pos = opening.position_along_wall
    start_x = wall.from_pt[0] + ux * pos
    start_y = wall.from_pt[1] + uy * pos

    if abs(dx) >= abs(dy):
        # Primarily E-W wall
        cut_w = opening.width       # along X
        cut_d = thickness_ft        # along Y
        cut_x = start_x
        cut_y = start_y - thickness_ft / 2.0
    else:
        # Primarily N-S wall
        cut_w = thickness_ft        # along X
        cut_d = opening.width       # along Y
        cut_x = start_x - thickness_ft / 2.0
        cut_y = start_y

    return {
        "type": opening.opening_type,
        "cut_x": round(cut_x, 6),
        "cut_y": round(cut_y, 6),
        "cut_w": round(cut_w, 6),
        "cut_d": round(cut_d, 6),
        "sill_height": opening.sill_height,
        "height": opening.height,
        "width": opening.width,
    }


# ---------------------------------------------------------------------------
# Boundary expansion
# ---------------------------------------------------------------------------

def _centroid(boundary: list[list[float]]) -> tuple[float, float]:
    """Compute centroid of a polygon."""
    xs = [p[0] for p in boundary]
    ys = [p[1] for p in boundary]
    return sum(xs) / len(xs), sum(ys) / len(ys)


def _expand_boundary(boundary: list[list[float]], overhang: float) -> list[list[float]]:
    """Expand each vertex of a polygon outward from the centroid by overhang distance.

    This is a simple centroid-offset expansion — appropriate for convex roof
    boundary polygons representing rectangular or near-rectangular footprints.
    """
    cx, cy = _centroid(boundary)
    expanded = []
    for px, py in boundary:
        vx = px - cx
        vy = py - cy
        dist = math.hypot(vx, vy)
        if dist < 1e-9:
            expanded.append([px, py])
            continue
        scale = (dist + overhang) / dist
        expanded.append([
            round(cx + vx * scale, 6),
            round(cy + vy * scale, 6),
        ])
    return expanded


# ---------------------------------------------------------------------------
# Context builders
# ---------------------------------------------------------------------------

def _prepare_floors_context(project: Project) -> tuple[list[dict], int]:
    """Flatten Floor/Wall/Opening dataclasses into template-ready dicts.

    Returns (floors_list, total_wall_count).
    """
    floors_out = []
    total_walls = 0

    for floor in project.floors:
        walls_out = []
        for wall in floor.walls:
            plate_height = wall.height if wall.height is not None else floor.plate_height
            openings_out = [_compute_opening_cut(wall, op) for op in wall.openings]

            walls_out.append({
                "id": wall.id,
                "wall_type": wall.wall_type,
                "from_x": wall.from_pt[0],
                "from_y": wall.from_pt[1],
                "to_x": wall.to_pt[0],
                "to_y": wall.to_pt[1],
                "thickness_ft": round(wall.thickness_ft, 6),
                "length_ft": round(wall.length_ft, 6),
                "plate_height": plate_height,
                "openings": openings_out,
            })
            total_walls += 1

        floors_out.append({
            "label": floor.label,
            "z_origin": floor.z_origin,
            "plate_height": floor.plate_height,
            "walls": walls_out,
        })

    return floors_out, total_walls


def _prepare_structure_context(project: Project) -> tuple[list[dict], list[dict], float]:
    """Flatten Structural dataclass into template-ready dicts.

    Returns (posts_list, beams_list, default_plate_height).
    """
    # Collect from top-level structural and from each floor
    all_posts: list[Post] = []
    all_beams: list[Beam] = []

    if project.structural:
        all_posts.extend(project.structural.posts)
        all_beams.extend(project.structural.beams)

    for floor in project.floors:
        if floor.structural:
            all_posts.extend(floor.structural.posts)
            all_beams.extend(floor.structural.beams)

    posts_out = []
    for post in all_posts:
        posts_out.append({
            "x": post.position[0],
            "y": post.position[1],
            "size_in": post.size_in,
            "z_base": post.z_base,
        })

    beams_out = []
    for beam in all_beams:
        beams_out.append({
            "from_x": beam.from_pt[0],
            "from_y": beam.from_pt[1],
            "to_x": beam.to_pt[0],
            "to_y": beam.to_pt[1],
            "width_in": beam.width_in,
            "depth_in": beam.depth_in,
            "z": beam.z,
            "label": beam.label,
        })

    default_plate = project.floors[0].plate_height if project.floors else 8.0

    return posts_out, beams_out, default_plate


def _prepare_roof_context(project: Project) -> list[dict]:
    """Expand roof plane boundaries by overhang distance.

    Returns roof_planes list ready for the template.
    """
    if not project.roof:
        return []

    planes_out = []
    for plane in project.roof.planes:
        expanded = _expand_boundary(plane.boundary, plane.overhang)
        planes_out.append({
            "label": plane.label,
            "type": plane.roof_type,
            "slope": plane.slope,
            "overhang": plane.overhang,
            "expanded_boundary": expanded,
            "z_base": plane.z_base,
        })

    return planes_out


# ---------------------------------------------------------------------------
# Jinja2 environment
# ---------------------------------------------------------------------------

def _make_env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(_TEMPLATES_DIR)),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_ruby_scripts(project: Project, output_dir: Path) -> list[Path]:
    """Render all Ruby scripts for project into output_dir.

    Returns list of written file paths.

    Renders:
        00_helpers.rb
        04_walls.rb
        05_structure.rb
        06_roof.rb

    Deferred for v0 (not rendered):
        scenes.rb — camera scene generation requires interactive SketchUp session info
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    env = _make_env()

    module = _module_name(project.project_name)
    floors_ctx, wall_count = _prepare_floors_context(project)
    posts_ctx, beams_ctx, plate_height = _prepare_structure_context(project)
    roof_ctx = _prepare_roof_context(project)

    rendered: list[Path] = []

    # --- 00_helpers.rb ---
    tmpl = env.get_template("helpers.rb.j2")
    content = tmpl.render(
        module_name=module,
        project_name=project.project_name,
    )
    out = output_dir / "00_helpers.rb"
    out.write_text(content)
    rendered.append(out)

    # --- 04_walls.rb ---
    tmpl = env.get_template("walls.rb.j2")
    content = tmpl.render(
        project_name=project.project_name,
        module_name=module,
        floors=floors_ctx,
        wall_count=wall_count,
    )
    out = output_dir / "04_walls.rb"
    out.write_text(content)
    rendered.append(out)

    # --- 05_structure.rb ---
    tmpl = env.get_template("structure.rb.j2")
    content = tmpl.render(
        project_name=project.project_name,
        module_name=module,
        posts=posts_ctx,
        beams=beams_ctx,
        plate_height=plate_height,
    )
    out = output_dir / "05_structure.rb"
    out.write_text(content)
    rendered.append(out)

    # --- 06_roof.rb ---
    tmpl = env.get_template("roof.rb.j2")
    content = tmpl.render(
        project_name=project.project_name,
        module_name=module,
        roof_planes=roof_ctx,
    )
    out = output_dir / "06_roof.rb"
    out.write_text(content)
    rendered.append(out)

    # scenes.rb — deferred for v0
    # Scene generation requires knowing active view state from an open SketchUp session.
    # Will be implemented in v1 with a scenes data model.

    return rendered
