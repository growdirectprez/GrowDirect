"""ARC structural components — posts and beams for post-and-beam construction.

Maps directly to the Post and Beam dataclasses in arc.model.spatial_model:
    Post  → post(size_in, height_in)
    Beam  → beam(width_in, depth_in, span_in)

Post origin:  base center (matches spatial_model Post.position [x,y])
Beam origin:  left end, bottom face center (matches spatial_model Beam.from_pt)

Seacove (mid-century modern post-and-beam) uses:
    Posts: 4×4 actual (3.5"×3.5") Douglas fir
    Ridge beam: 4×12 (3.5"×11.25") or glulam
    Main beams: 4×8 (3.5"×7.25"), 4×10 (3.5"×9.25")
    Exposed rafters: 2×6 or 2×8 at 24" o.c.
"""
from __future__ import annotations

import math as _math

from arc.components.base import ComponentRegistry, ComponentSpec, SnapPoint

# Material colors
_POST_COLOR   = (160, 120,  80, 255)   # darker Douglas fir
_BEAM_COLOR   = (150, 110,  70, 255)   # slightly reddish Douglas fir
_RAFTER_COLOR = (175, 140, 100, 255)   # lighter — exposed rafter

# Softwood framing standard: 1.5" off nominal for 2" dimension, 0.5" off for 4"+
ACTUAL_POST_SIZES = {
    "4x4":  3.5,
    "4x6":  5.5,
    "6x6":  5.5,
    "6x8":  7.5,
}

ACTUAL_BEAM_WIDTHS = {
    "4x":   3.5,   # 4-inch nominal
    "6x":   5.5,   # 6-inch nominal
}

ACTUAL_BEAM_DEPTHS = {
    6:   5.5,
    8:   7.25,
    10:  9.25,
    12: 11.25,
    14: 13.25,
    16: 15.25,
}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _box_code_structural(name: str, w: float, d: float, h: float,
                          ox: float, oy: float, oz: float,
                          mat_name: str, color: tuple) -> str:
    r, g, b, a = color
    return f"""\
comp_def = ComponentDefinition()
comp_def.set_name("{name}")
model.add_component_definitions([comp_def])
_existing_mats = {{m.get_name(): m for m in model.get_materials()}}
if "{mat_name}" not in _existing_mats:
    _mat = Material()
    _mat.set_name("{mat_name}")
    _mat.set_color(SUColor({r},{g},{b},{a}))
    model.add_materials([_mat])
    _existing_mats["{mat_name}"] = _mat
_mat = _existing_mats["{mat_name}"]
_w, _d, _h = {w}, {d}, {h}
_ox, _oy, _oz = {ox}, {oy}, {oz}
_geom = GeometryInput()
_geom.set_vertices([
    SUPoint3D(_ox,      _oy,      _oz),
    SUPoint3D(_ox+_w,   _oy,      _oz),
    SUPoint3D(_ox+_w,   _oy+_d,   _oz),
    SUPoint3D(_ox,      _oy+_d,   _oz),
    SUPoint3D(_ox,      _oy,      _oz+_h),
    SUPoint3D(_ox+_w,   _oy,      _oz+_h),
    SUPoint3D(_ox+_w,   _oy+_d,   _oz+_h),
    SUPoint3D(_ox,      _oy+_d,   _oz+_h),
])
for _tri in [[0,1,5],[0,5,4],[1,2,6],[1,6,5],[2,3,7],[2,7,6],
              [3,0,4],[3,4,7],[4,5,6],[4,6,7],[0,3,2],[0,2,1]]:
    _lp = LoopInput()
    for _i in _tri: _lp.add_vertex_index(_i)
    _, _geom = _geom.add_face(_lp)
comp_def.get_entities().fill(_geom, weld_vertices=True)
for _e in comp_def.get_entities().get_edges():
    _ef = _e.get_faces()
    if len(_ef) == 2:
        _n0, _n1 = _ef[0].get_normal(), _ef[1].get_normal()
        if _n0.x*_n1.x + _n0.y*_n1.y + _n0.z*_n1.z > 0.999:
            _e.set_soft(True); _e.set_smooth(True)
for _f in comp_def.get_entities().get_faces():
    _f.set_front_material(_mat)
    _f.set_back_material(_mat)\
"""


# ---------------------------------------------------------------------------
# Post
# ---------------------------------------------------------------------------

def post(
    size_in: float,
    height_in: float,
    registry: ComponentRegistry,
    nominal: str = "4x4",
) -> ComponentSpec:
    """Vertical square post.

    Origin at base center — place at spatial_model Post.position × 12.
    Height runs from Z=0 to Z=height_in.

    Args:
        size_in:   actual side dimension in inches (e.g. 3.5 for 4×4)
        height_in: post height in inches
        registry:  ComponentRegistry
        nominal:   label for the component name (e.g. "4x4", "6x6")

    Snap points:
        base       — bottom center (origin), faces down
        top        — top center, faces up (where beam lands)
        beam_seat  — alias for top (same point, semantic clarity)
        face_n/s/e/w — four vertical face centers
    """
    name = f"post_{nominal}_{height_in:.1f}in"
    if registry.has(name):
        return registry.get(name)

    s = size_in
    ox, oy = -s / 2, -s / 2
    mat_name = f"Structural_Post_{nominal}"

    code = _box_code_structural(name, s, s, height_in, ox, oy, 0.0,
                                 mat_name, _POST_COLOR)

    spec = ComponentSpec(
        name=name,
        category="structural",
        description=f"{nominal} post ({size_in}\"×{size_in}\"), {height_in:.1f}\" tall",
        params={"nominal": nominal, "size_in": size_in, "height_in": height_in},
        snap_points=[
            SnapPoint("base",      0,  0,  0,          0,  0, -1),
            SnapPoint("top",       0,  0,  height_in,  0,  0,  1),
            SnapPoint("beam_seat", 0,  0,  height_in,  0,  0,  1),
            SnapPoint("face_s",    0,  oy, height_in/2, 0, -1,  0),
            SnapPoint("face_n",    0,  oy+s, height_in/2, 0, 1, 0),
            SnapPoint("face_w",    ox, 0,  height_in/2, -1, 0,  0),
            SnapPoint("face_e",    ox+s, 0, height_in/2, 1, 0,  0),
        ],
        definition_code=code,
    )
    return registry.register(spec)


def post_from_model(model_post, plate_height_ft: float,
                    registry: ComponentRegistry) -> ComponentSpec:
    """Convenience: create a post ComponentSpec from a spatial_model Post object.

    Args:
        model_post:     arc.model.spatial_model.Post instance
        plate_height_ft: floor plate height in feet (used if post.height is None)
        registry:       ComponentRegistry
    """
    height_ft = model_post.height if model_post.height is not None else plate_height_ft
    height_in = height_ft * 12.0
    size_in = model_post.size_in

    # Determine nominal label from size
    nominal = "4x4"
    for nom, actual in ACTUAL_POST_SIZES.items():
        if abs(actual - size_in) < 0.1:
            nominal = nom
            break

    return post(size_in=size_in, height_in=height_in, registry=registry, nominal=nominal)


# ---------------------------------------------------------------------------
# Beam
# ---------------------------------------------------------------------------

def beam(
    width_in: float,
    depth_in: float,
    span_in: float,
    registry: ComponentRegistry,
    label: str = "beam",
) -> ComponentSpec:
    """Horizontal structural beam.

    Origin at left end, bottom face center.
    Beam runs from X=0 to X=span_in.
    Width (Y) is centered on origin. Depth (Z) runs up.

    Place by translating to the world position of Beam.from_pt at the
    correct elevation (Beam.z in spatial model = bottom of beam in feet).

    Args:
        width_in:  actual beam width in inches (e.g. 3.5 for 4-inch nominal)
        depth_in:  actual beam depth in inches (e.g. 9.25 for 2×10)
        span_in:   beam length in inches (from_pt to to_pt × 12)
        registry:  ComponentRegistry
        label:     "beam", "ridge_beam", "rafter" — affects name and color
    """
    name = f"{label}_{width_in:.2f}w_{depth_in:.2f}d_{span_in:.1f}in"
    if registry.has(name):
        return registry.get(name)

    oy = -width_in / 2
    color = _BEAM_COLOR if label != "rafter" else _RAFTER_COLOR
    mat_name = f"Structural_{label.title()}_{width_in:.1f}x{depth_in:.1f}"

    code = _box_code_structural(name, span_in, width_in, depth_in,
                                 0.0, oy, 0.0, mat_name, color)

    spec = ComponentSpec(
        name=name,
        category="structural",
        description=f"{label} {width_in:.2f}\"×{depth_in:.2f}\", {span_in:.1f}\" span",
        params={
            "label": label,
            "width_in": width_in,
            "depth_in": depth_in,
            "span_in": span_in,
        },
        snap_points=[
            SnapPoint("left_end",    0,          0, depth_in/2, -1, 0, 0),
            SnapPoint("right_end",   span_in,    0, depth_in/2,  1, 0, 0),
            SnapPoint("top_left",    0,          0, depth_in,    0, 0, 1),
            SnapPoint("top_right",   span_in,    0, depth_in,    0, 0, 1),
            SnapPoint("top_center",  span_in/2,  0, depth_in,    0, 0, 1),
            SnapPoint("base_left",   0,          0, 0,           0, 0, -1),
            SnapPoint("base_right",  span_in,    0, 0,           0, 0, -1),
            SnapPoint("base_center", span_in/2,  0, 0,           0, 0, -1),
        ],
        definition_code=code,
    )
    return registry.register(spec)


def beam_from_model(model_beam, registry: ComponentRegistry) -> ComponentSpec:
    """Convenience: create a beam ComponentSpec from a spatial_model Beam object.

    The span is computed from from_pt and to_pt (in feet → converted to inches).
    """
    import math
    from_pt = model_beam.from_pt
    to_pt = model_beam.to_pt
    dx = (to_pt[0] - from_pt[0]) * 12.0
    dy = (to_pt[1] - from_pt[1]) * 12.0
    span_in = math.hypot(dx, dy)

    label = model_beam.label.lower().replace(" ", "_") if model_beam.label else "beam"

    return beam(
        width_in=model_beam.width_in,
        depth_in=model_beam.depth_in,
        span_in=span_in,
        registry=registry,
        label=label,
    )


# ---------------------------------------------------------------------------
# Rafter (exposed rafter for post-and-beam roofs)
# ---------------------------------------------------------------------------

def rafter(
    nominal: str,
    length_in: float,
    registry: ComponentRegistry,
) -> ComponentSpec:
    """Exposed rafter for post-and-beam ceiling/roof.

    Standard Seacove rafters: 2×6 or 2×8 at 24" o.c.
    Origin at left (wall) end, bottom face center.

    Args:
        nominal:   "2x6" or "2x8"
        length_in: rafter length (span from bearing wall to ridge) in inches
        registry:  ComponentRegistry
    """
    depth_map = {"2x6": 5.5, "2x8": 7.25, "2x10": 9.25}
    if nominal not in depth_map:
        raise ValueError(f"Unknown rafter nominal: {nominal!r}")
    width_in = 1.5
    depth_in = depth_map[nominal]
    return beam(width_in, depth_in, length_in, registry, label=f"rafter_{nominal}")
