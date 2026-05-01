"""ARC component base types — SnapPoint, ComponentSpec, ComponentRegistry.

All geometry lives in component LOCAL space, in INCHES.
The component origin is always the primary snap point (usually base-center).

Coordinate convention (matches Trimble MCP SDK):
    X = width (east)
    Y = depth (north)
    Z = height (up)
    Origin = base center of the component
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# SnapPoint
# ---------------------------------------------------------------------------

@dataclass
class SnapPoint:
    """A named connection point in component local space (inches).

    'normal' is the direction this face points — used to orient mating parts.
    E.g., a stud's 'face_exterior' snap has normal (0, -1, 0) pointing outward.
    """
    name: str
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    # Unit normal — which direction this snap face points
    nx: float = 0.0
    ny: float = 0.0
    nz: float = 1.0

    def offset_from(self, other: "SnapPoint") -> tuple[float, float, float]:
        """Return the (dx, dy, dz) to add to a world position so that
        'other' aligns with 'self' in world space."""
        return (self.x - other.x, self.y - other.y, self.z - other.z)


# ---------------------------------------------------------------------------
# ComponentSpec
# ---------------------------------------------------------------------------

@dataclass
class ComponentSpec:
    """A reusable building component for the SketchUp Python SDK.

    definition_code is the Python string that, when executed inside a
    build_model call, registers the ComponentDefinition with the model.
    The code must:
      - Create a ComponentDefinition named exactly self.name
      - Register it via model.add_component_definitions([comp_def])
      - Add geometry to comp_def.get_entities()
      - Apply materials face-by-face
      - Soften coplanar edges (boxes) or all edges (curved)

    snap_points are in component LOCAL space (inches).
    The component origin [0,0,0] is always the primary snap point.
    """
    name: str                           # unique key: "stud_2x6_96in"
    category: str                       # framing | structural | electrical | roof | site | finish
    description: str
    params: dict                        # {"height_in": 96.0, "width_in": 1.5, ...}
    snap_points: list[SnapPoint]
    definition_code: str                # Python code string for build_model
    symbol_2d: Optional[str] = None    # SVG string for 2D plan/elevation symbol (future)

    def snap(self, name: str) -> SnapPoint:
        """Look up a snap point by name. Raises KeyError if not found."""
        for sp in self.snap_points:
            if sp.name == name:
                return sp
        raise KeyError(f"Snap point {name!r} not on component {self.name!r}. "
                       f"Available: {[s.name for s in self.snap_points]}")

    def instance_code(
        self,
        tx: float,
        ty: float,
        tz: float,
        rotation_z_deg: float = 0.0,
        instance_name: str = "",
    ) -> str:
        """Generate Python code to place one instance of this component.

        tx, ty, tz are world coordinates IN INCHES (Trimble MCP units).
        rotation_z_deg rotates around the Z axis at the origin.

        The generated code assumes the ComponentDefinition is already registered
        and accessible via:
            _arc_defs = {cd.get_name(): cd for cd in model.get_component_definitions()}
        which should be set up once per build_model call.
        """
        lines = []
        if rotation_z_deg != 0.0:
            lines.append(f"_arc_cos = math.cos(math.radians({rotation_z_deg}))")
            lines.append(f"_arc_sin = math.sin(math.radians({rotation_z_deg}))")
            transform = (f"[_arc_cos,_arc_sin,0,0, "
                         f"-_arc_sin,_arc_cos,0,0, "
                         f"0,0,1,0, "
                         f"{tx:.4f},{ty:.4f},{tz:.4f},1]")
        else:
            transform = f"[1,0,0,0, 0,1,0,0, 0,0,1,0, {tx:.4f},{ty:.4f},{tz:.4f},1]"

        lines.append(f'_arc_inst = _arc_defs["{self.name}"].create_instance()')
        lines.append(f"_arc_inst.set_transform(SUTransformation({transform}))")
        if instance_name:
            lines.append(f'_arc_inst.set_name("{instance_name}")')
        lines.append("model.get_entities().add_instance(_arc_inst)")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# ComponentRegistry
# ---------------------------------------------------------------------------

class ComponentRegistry:
    """Central registry of ComponentSpecs for a build session.

    Tracks which components have been defined so the assembler can:
      1. Emit definition code once per unique component type
      2. Look up snap points for placement math
      3. List all components by category

    Example:
        reg = ComponentRegistry()
        stud_2x6(height_in=96.0, registry=reg)
        print(reg.all_definition_code())   # → Python for build_model
    """

    def __init__(self) -> None:
        self._specs: dict[str, ComponentSpec] = {}

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, spec: ComponentSpec) -> ComponentSpec:
        """Register a ComponentSpec. Raises ValueError on duplicate name."""
        if spec.name in self._specs:
            raise ValueError(
                f"Component already registered: {spec.name!r}. "
                "Use get() to retrieve an existing spec."
            )
        self._specs[spec.name] = spec
        return spec

    def register_or_get(self, spec: ComponentSpec) -> ComponentSpec:
        """Register spec, or return existing one if name already present."""
        if spec.name in self._specs:
            return self._specs[spec.name]
        return self.register(spec)

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get(self, name: str) -> ComponentSpec:
        """Return spec by name. Raises KeyError if not registered."""
        if name not in self._specs:
            raise KeyError(
                f"Component not registered: {name!r}. "
                f"Registered: {list(self._specs.keys())}"
            )
        return self._specs[name]

    def has(self, name: str) -> bool:
        return name in self._specs

    def snap(self, comp_name: str, snap_name: str) -> SnapPoint:
        """Shortcut: get a snap point from a registered component."""
        return self.get(comp_name).snap(snap_name)

    # ------------------------------------------------------------------
    # Code generation
    # ------------------------------------------------------------------

    def all_definition_code(self, categories: Optional[list[str]] = None) -> str:
        """Return Python code that registers all (or filtered) ComponentDefinitions.

        Pass this as the 'code' argument to build_model. It ends with a
        _arc_defs dict so subsequent instance_code() calls can look up defs.
        """
        specs = list(self._specs.values())
        if categories:
            specs = [s for s in specs if s.category in categories]

        lines = [
            "# ARC Component Library — auto-generated definition code",
            "# Do not import anything — all SDK names are pre-loaded.",
            "",
        ]
        for spec in specs:
            lines.append(f"# ── {spec.name} ({spec.category}) ──────────────────")
            lines.append(spec.definition_code)
            lines.append("")

        # Build lookup dict at the end — used by instance_code()
        lines += [
            "# Component lookup dict (required for instance placement)",
            "_arc_defs = {cd.get_name(): cd for cd in model.get_component_definitions()}",
            f"result = {{'registered': {[s.name for s in specs]!r}}}",
        ]
        return "\n".join(lines)

    def instance_placement_code(
        self,
        placements: list[dict],
    ) -> str:
        """Generate Python code that places a list of component instances.

        Each placement dict:
            {
                "component": "stud_2x6_96in",
                "tx": 12.0,   # world X in inches
                "ty": 0.0,
                "tz": 0.0,
                "rotation_z_deg": 0.0,    # optional
                "name": "stud_001",       # optional instance name
            }
        """
        lines = [
            "# ARC instance placement — auto-generated",
            "_arc_defs = {cd.get_name(): cd for cd in model.get_component_definitions()}",
            "",
        ]
        for i, p in enumerate(placements):
            comp_name = p["component"]
            spec = self.get(comp_name)
            lines.append(f"# instance {i}: {comp_name}")
            lines.append(spec.instance_code(
                tx=p["tx"],
                ty=p["ty"],
                tz=p["tz"],
                rotation_z_deg=p.get("rotation_z_deg", 0.0),
                instance_name=p.get("name", ""),
            ))
            lines.append("")
        lines.append(f"result = {{'placed': {len(placements)}}}")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def list_by_category(self, category: str) -> list[ComponentSpec]:
        return [s for s in self._specs.values() if s.category == category]

    @property
    def names(self) -> list[str]:
        return list(self._specs.keys())

    @property
    def categories(self) -> list[str]:
        return sorted({s.category for s in self._specs.values()})

    def summary(self) -> str:
        lines = [f"ComponentRegistry: {len(self._specs)} component(s)"]
        for cat in self.categories:
            specs = self.list_by_category(cat)
            lines.append(f"  [{cat}] {len(specs)} component(s):")
            for s in specs:
                lines.append(f"    {s.name} — {s.description}")
        return "\n".join(lines)
