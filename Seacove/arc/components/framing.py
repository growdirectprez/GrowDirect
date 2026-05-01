"""ARC framing components — dimensional lumber for wall assemblies.

All components use standard nominal/actual sizes:
    2×4 → actual 1.5" × 3.5"
    2×6 → actual 1.5" × 5.5"
    2×8 → actual 1.5" × 7.25"
    2×10 → actual 1.5" × 9.25"
    2×12 → actual 1.5" × 11.25"

Component origin is always at the BASE CENTER of the member so that
placement transforms simply translate to the desired world position.

Snap points:
    Studs/posts:     base (bottom), top, face_front, face_back
    Plates:          left_end, right_end, face_front, face_back, top_center, base_center
    Headers:         left_end, right_end, base_center, top_center

The generated definition_code follows Trimble MCP SDK rules:
    - No import statements
    - Units: INCHES
    - Box pattern with 12 triangles
    - Coplanar edge softening (dot > 0.999)
    - Materials registered before add_materials()
"""
from __future__ import annotations

from arc.components.base import ComponentRegistry, ComponentSpec, SnapPoint

# ---------------------------------------------------------------------------
# Actual lumber dimensions (inches)
# ---------------------------------------------------------------------------

ACTUAL_SIZES = {
    "2x4":  (1.5,  3.5),
    "2x6":  (1.5,  5.5),
    "2x8":  (1.5,  7.25),
    "2x10": (1.5,  9.25),
    "2x12": (1.5, 11.25),
}

# Material colors
_FRAMING_COLOR = (210, 180, 140, 255)   # tan — raw douglas fir
_PLATE_COLOR   = (195, 165, 125, 255)   # slightly darker for plates
_HEADER_COLOR  = (180, 150, 110, 255)   # darker — doubled/LVL header


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _box_code(name: str, w: float, d: float, h: float,
              ox: float, oy: float, oz: float,
              mat_name: str, color: tuple[int,int,int,int]) -> str:
    """Generate Python code for a box ComponentDefinition.

    The box runs from (ox, oy, oz) to (ox+w, oy+d, oz+h) in local space.
    """
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
# Stud components
# ---------------------------------------------------------------------------

def stud(
    nominal: str,
    height_in: float,
    registry: ComponentRegistry,
) -> ComponentSpec:
    """Vertical stud of any nominal size at given height.

    Origin at base center. Stud runs from Z=0 to Z=height_in.
    Width (X) and depth (Y) are centered on origin.

    Args:
        nominal:   "2x4" or "2x6" (most common for walls)
        height_in: height in inches (e.g. 92.625 for pre-cut stud, 96 for 8ft)
        registry:  ComponentRegistry to register into
    """
    if nominal not in ACTUAL_SIZES:
        raise ValueError(f"Unknown nominal size: {nominal!r}. Use: {list(ACTUAL_SIZES)}")
    w, d = ACTUAL_SIZES[nominal]
    name = f"stud_{nominal.replace('x','x')}_{height_in:.3f}in"
    if registry.has(name):
        return registry.get(name)

    ox, oy = -w / 2, -d / 2   # center on origin
    mat_name = f"Framing_{nominal}"

    code = _box_code(name, w, d, height_in, ox, oy, 0.0,
                     mat_name, _FRAMING_COLOR)

    spec = ComponentSpec(
        name=name,
        category="framing",
        description=f"{nominal} stud, {height_in:.3f}\" tall",
        params={"nominal": nominal, "width_in": w, "depth_in": d, "height_in": height_in},
        snap_points=[
            SnapPoint("base",        0,    0,           0,    0,  0, -1),
            SnapPoint("top",         0,    0,           height_in, 0, 0, 1),
            SnapPoint("face_front",  0,    oy,          height_in / 2, 0, -1, 0),
            SnapPoint("face_back",   0,    oy + d,      height_in / 2, 0,  1, 0),
            SnapPoint("face_left",   ox,   0,           height_in / 2, -1, 0, 0),
            SnapPoint("face_right",  ox+w, 0,           height_in / 2,  1, 0, 0),
        ],
        definition_code=code,
    )
    return registry.register(spec)


def stud_2x4(height_in: float, registry: ComponentRegistry) -> ComponentSpec:
    """2×4 stud (1.5" × 3.5") — interior walls."""
    return stud("2x4", height_in, registry)


def stud_2x6(height_in: float, registry: ComponentRegistry) -> ComponentSpec:
    """2×6 stud (1.5" × 5.5") — exterior walls, load-bearing."""
    return stud("2x6", height_in, registry)


# ---------------------------------------------------------------------------
# Plate components (horizontal, runs along wall length)
# ---------------------------------------------------------------------------

def plate(
    nominal: str,
    length_in: float,
    registry: ComponentRegistry,
    label: str = "plate",
) -> ComponentSpec:
    """Horizontal wall plate (top or bottom) of given nominal size and length.

    Origin at left end, bottom face center (Z=0 at bottom of plate).
    Plate runs from X=0 to X=length_in.
    Width (Y) centered on origin.

    Args:
        nominal:   "2x4" or "2x6"
        length_in: plate length in inches
        label:     "plate", "top_plate", "bottom_plate" — appended to name
        registry:  ComponentRegistry
    """
    if nominal not in ACTUAL_SIZES:
        raise ValueError(f"Unknown nominal size: {nominal!r}")
    w, d = ACTUAL_SIZES[nominal]   # w = 1.5 (thickness), d = 3.5 or 5.5 (depth)
    # Plate runs along X; thickness is Z (1.5"), depth is Y
    name = f"{label}_{nominal}_{length_in:.3f}in"
    if registry.has(name):
        return registry.get(name)

    oy = -d / 2   # center Y on origin
    mat_name = f"Framing_{nominal}"

    # For a plate: runs X direction, thickness = w (1.5") in Z, depth = d in Y
    code = _box_code(name, length_in, d, w, 0.0, oy, 0.0,
                     mat_name, _PLATE_COLOR)

    spec = ComponentSpec(
        name=name,
        category="framing",
        description=f"{nominal} {label}, {length_in:.1f}\" long",
        params={"nominal": nominal, "length_in": length_in, "thickness_in": w, "depth_in": d},
        snap_points=[
            SnapPoint("left_end",     0,           0, w / 2,  -1, 0, 0),
            SnapPoint("right_end",    length_in,   0, w / 2,   1, 0, 0),
            SnapPoint("base_center",  length_in/2, 0, 0,       0, 0, -1),
            SnapPoint("top_center",   length_in/2, 0, w,       0, 0,  1),
            SnapPoint("face_front",   length_in/2, oy,    w/2, 0, -1, 0),
            SnapPoint("face_back",    length_in/2, oy+d,  w/2, 0,  1, 0),
        ],
        definition_code=code,
    )
    return registry.register(spec)


def plate_2x4(length_in: float, registry: ComponentRegistry,
              label: str = "plate") -> ComponentSpec:
    return plate("2x4", length_in, registry, label)


def plate_2x6(length_in: float, registry: ComponentRegistry,
              label: str = "plate") -> ComponentSpec:
    return plate("2x6", length_in, registry, label)


# ---------------------------------------------------------------------------
# Header (spans door/window rough opening)
# ---------------------------------------------------------------------------

def header(
    span_in: float,
    header_height_in: float,
    nominal: str = "2x10",
    registry: ComponentRegistry = None,
) -> ComponentSpec:
    """Doubled header spanning a rough opening.

    Modeled as a single box representing the doubled member + plywood spacer.
    Total depth = 3" (two 1.5" members). Height = header_height_in.
    Origin at left end, bottom face center.

    Standard header heights:
        2×6 wall:  5.5" (one member laid flat) or 9.25" (2×10)
        2×4 wall:  3.5" or 7.25" (2×8)

    Args:
        span_in:          clear span of rough opening in inches
        header_height_in: height of header assembly in inches
        nominal:          lumber size for each ply (default 2×10)
        registry:         ComponentRegistry
    """
    if registry is None:
        raise ValueError("registry is required")
    total_depth = 3.0   # doubled 1.5" + plywood spacer ~0.5" → round to 3"
    name = f"header_{nominal}_{span_in:.1f}in_span"
    if registry.has(name):
        return registry.get(name)

    oy = -total_depth / 2
    mat_name = "Framing_Header"
    code = _box_code(name, span_in, total_depth, header_height_in,
                     0.0, oy, 0.0, mat_name, _HEADER_COLOR)

    spec = ComponentSpec(
        name=name,
        category="framing",
        description=f"Doubled {nominal} header, {span_in:.1f}\" span × {header_height_in:.1f}\" tall",
        params={
            "span_in": span_in,
            "header_height_in": header_height_in,
            "nominal": nominal,
            "total_depth_in": total_depth,
        },
        snap_points=[
            SnapPoint("left_end",    0,        0, header_height_in / 2, -1, 0, 0),
            SnapPoint("right_end",   span_in,  0, header_height_in / 2,  1, 0, 0),
            SnapPoint("base_center", span_in/2, 0, 0,                    0, 0, -1),
            SnapPoint("top_center",  span_in/2, 0, header_height_in,     0, 0,  1),
        ],
        definition_code=code,
    )
    return registry.register(spec)


# ---------------------------------------------------------------------------
# Blocking (horizontal member between studs)
# ---------------------------------------------------------------------------

def blocking(
    nominal: str,
    length_in: float,
    registry: ComponentRegistry,
) -> ComponentSpec:
    """Horizontal blocking between studs at mid-height.

    Same profile as a stud but oriented horizontally (rotated 90° in Z).
    Origin at left end, bottom face center. Runs along X.

    Args:
        nominal:   "2x4" or "2x6"
        length_in: length between studs (center-to-center minus stud width)
        registry:  ComponentRegistry
    """
    if nominal not in ACTUAL_SIZES:
        raise ValueError(f"Unknown nominal size: {nominal!r}")
    w, d = ACTUAL_SIZES[nominal]
    name = f"blocking_{nominal}_{length_in:.1f}in"
    if registry.has(name):
        return registry.get(name)

    oy = -d / 2
    mat_name = f"Framing_{nominal}"
    # Block runs X direction; thickness Z = w (1.5"), depth Y = d
    code = _box_code(name, length_in, d, w, 0.0, oy, 0.0,
                     mat_name, _FRAMING_COLOR)

    spec = ComponentSpec(
        name=name,
        category="framing",
        description=f"{nominal} blocking, {length_in:.1f}\" long",
        params={"nominal": nominal, "length_in": length_in, "width_in": w, "depth_in": d},
        snap_points=[
            SnapPoint("left_end",    0,          0, w/2, -1, 0, 0),
            SnapPoint("right_end",   length_in,  0, w/2,  1, 0, 0),
            SnapPoint("base_center", length_in/2, 0, 0,   0, 0, -1),
            SnapPoint("top_center",  length_in/2, 0, w,   0, 0,  1),
        ],
        definition_code=code,
    )
    return registry.register(spec)


# ---------------------------------------------------------------------------
# Cripple stud (short stud above/below opening)
# ---------------------------------------------------------------------------

def cripple(
    nominal: str,
    height_in: float,
    registry: ComponentRegistry,
) -> ComponentSpec:
    """Short cripple stud above a header or below a sill.

    Same geometry as a regular stud — just a different name/label
    to distinguish in the model.
    """
    if nominal not in ACTUAL_SIZES:
        raise ValueError(f"Unknown nominal size: {nominal!r}")
    w, d = ACTUAL_SIZES[nominal]
    name = f"cripple_{nominal}_{height_in:.3f}in"
    if registry.has(name):
        return registry.get(name)

    ox, oy = -w / 2, -d / 2
    mat_name = f"Framing_{nominal}"
    code = _box_code(name, w, d, height_in, ox, oy, 0.0,
                     mat_name, _FRAMING_COLOR)

    spec = ComponentSpec(
        name=name,
        category="framing",
        description=f"{nominal} cripple, {height_in:.3f}\" tall",
        params={"nominal": nominal, "width_in": w, "depth_in": d, "height_in": height_in},
        snap_points=[
            SnapPoint("base", 0, 0, 0,          0, 0, -1),
            SnapPoint("top",  0, 0, height_in,  0, 0,  1),
        ],
        definition_code=code,
    )
    return registry.register(spec)
