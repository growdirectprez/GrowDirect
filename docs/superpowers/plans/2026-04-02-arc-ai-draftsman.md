# ARC AI Draftsman Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the ARC AI draftsman pipeline — a CLI tool that reads architectural blueprints, builds a spatial model, and generates SketchUp Ruby scripts for accurate 3D architectural models.

**Architecture:** Python 3.12 CLI tool with 5 pipeline stages (Ingest → Extract → Model → Validate → Generate). File-based I/O between stages — no database, no web server. Jinja2 templates for Ruby code generation. Ollama vision for blueprint reading.

**Tech Stack:** Python 3.12, Click (CLI), Jinja2 (templates), Ollama (vision AI), pytest, JSON (spatial model storage)

**Spec:** `docs/superpowers/specs/2026-04-02-arc-ai-draftsman-design.md`

---

## File Map

### New Files to Create

| File | Responsibility |
|------|---------------|
| `ARC/CLAUDE.md` | ARC-specific rules: not a web app, no MCP, no factory pipeline |
| `ARC/pyproject.toml` | Package config, dependencies, CLI entry point |
| `ARC/requirements.txt` | Pinned dependencies |
| `ARC/arc/__init__.py` | Package init with version |
| `ARC/arc/cli.py` | Click CLI: `arc ingest`, `arc extract`, `arc model`, `arc validate`, `arc generate` |
| `ARC/arc/ingest/__init__.py` | Ingest package |
| `ARC/arc/ingest/blueprint_reader.py` | PDF/image → normalized page images |
| `ARC/arc/ingest/photo_reader.py` | Site photos → tagged, normalized images |
| `ARC/arc/ingest/description.py` | Natural language → structured intent JSON |
| `ARC/arc/extract/__init__.py` | Extract package |
| `ARC/arc/extract/dimension_extractor.py` | Vision AI → wall lengths, room sizes, scale factors |
| `ARC/arc/extract/element_detector.py` | Vision AI → doors, windows, fixtures |
| `ARC/arc/extract/sheet_classifier.py` | Vision AI → sheet type classification |
| `ARC/arc/model/__init__.py` | Model package |
| `ARC/arc/model/spatial_model.py` | Core data classes: Project, Floor, Wall, Room, Opening |
| `ARC/arc/model/validator.py` | Model consistency checks |
| `ARC/arc/model/constraints.py` | Lot boundaries, setbacks |
| `ARC/arc/model/serialization.py` | JSON load/save with schema versioning |
| `ARC/arc/generate/__init__.py` | Generate package |
| `ARC/arc/generate/sketchup_ruby.py` | Spatial model → Jinja2 context → rendered .rb files |
| `ARC/arc/generate/layout_template.py` | Spatial model → LayOut .rb script (v1, stub for now) |
| `ARC/arc/llm/__init__.py` | LLM package |
| `ARC/arc/llm/vision.py` | Ollama vision API client |
| `ARC/arc/llm/embeddings.py` | Ollama embeddings client (stub for now) |
| `ARC/templates/ruby/helpers.rb.j2` | SeacoveHelpers module template |
| `ARC/templates/ruby/components.rb.j2` | Component definitions (doors, windows, posts) |
| `ARC/templates/ruby/walls.rb.j2` | Wall generation with boolean opening cuts |
| `ARC/templates/ruby/structure.rb.j2` | Posts and beams |
| `ARC/templates/ruby/roof.rb.j2` | Roof planes with overhangs |
| `ARC/templates/ruby/site.rb.j2` | Lot boundary, roads, building footprint |
| `ARC/templates/ruby/scenes.rb.j2` | Camera positions, tag visibility, section planes |
| `ARC/projects/seacove/ground_truth/dimensions.json` | Ground truth from blueprint-dimensions-reference.md as structured JSON |
| `ARC/tests/conftest.py` | Shared fixtures: sample spatial model, temp directories |
| `ARC/tests/test_spatial_model.py` | Spatial model creation, validation, serialization |
| `ARC/tests/test_validator.py` | Model consistency checks |
| `ARC/tests/test_ruby_generation.py` | Generated Ruby syntax/structure validation |
| `ARC/tests/test_ingest.py` | Blueprint reader, description parser |
| `ARC/tests/test_extract_accuracy.py` | Extracted vs ground truth dimensions |

### Existing Files Referenced (read-only)

| File | Used For |
|------|----------|
| `ARC/25-Seacove-As-Built.rb` | Reference: hand-written Ruby patterns to match |
| `ARC/sketchup-ruby/00_helpers.rb` | Reference: helper module patterns |
| `ARC/sketchup-ruby/02_site_plan.rb` | Reference: site plan Ruby patterns |
| `ARC/blueprint-dimensions-reference.md` | Ground truth dimensions for validation |
| `ARC/25 Seacove Blueprints/*.pdf` | Input blueprints for Seacove project |

---

## Chunk 1: Project Scaffold + Spatial Model + Serialization

This chunk creates the project structure, the core spatial model data classes,
validation, serialization, and the CLI skeleton. After this chunk, you can
create spatial models in Python, validate them, and save/load them as JSON.

### Task 1: Project Scaffold

**Files:**
- Create: `ARC/CLAUDE.md`
- Create: `ARC/pyproject.toml`
- Create: `ARC/requirements.txt`
- Create: `ARC/arc/__init__.py`

- [ ] **Step 1: Create ARC/CLAUDE.md**

```markdown
> **Platform parent:** Read ~/GrowDirect/CLAUDE.md first.

# ARC — AI Draftsman

ARC is a CLI pipeline tool, NOT a web app. It does not follow the Flask/PostgreSQL
pattern used by Canary and Cove.

## What ARC Is

- Python CLI tool that reads blueprints and generates SketchUp Ruby scripts
- File-based I/O between pipeline stages (JSON spatial models, .rb output)
- Single-user tool for Jeffe's projects — no multi-tenancy

## Hard Rules

1. **No MCP** — ARC never registers as an MCP server. Invisible to platform.
2. **No memory bus** — ARC does not participate in the platform memory bus.
3. **No Linear/GRO dispatch** — ARC is not managed by ALX or factory pipeline.
4. **No Flask** — No web server, no routes, no templates (except Jinja2 for Ruby codegen).
5. **No shared database** — File-based storage only (JSON). May use Postgres later.
6. **Directory boundary** — Everything stays inside `GrowDirect/ARC/`.

## What ARC CAN Use

- Ollama (vision + embeddings) via localhost:11434
- Local filesystem
- pytest for testing

## Pipeline

```
arc ingest <project>    — normalize inputs (PDFs, photos, descriptions)
arc extract <project>   — vision AI reads dimensions from blueprints
arc model <project>     — build spatial model from extractions
arc validate <project>  — check model consistency
arc generate <project>  — produce SketchUp Ruby scripts
```

## Protected Files

- `arc/model/spatial_model.py` — core data structure
- `templates/ruby/*.rb.j2` — Ruby code templates
```

- [ ] **Step 2: Create ARC/pyproject.toml**

```toml
[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"

[project]
name = "arc"
version = "0.1.0"
description = "ARC AI Draftsman — blueprint to SketchUp pipeline"
requires-python = ">=3.12"
dependencies = [
    "click>=8.1",
    "jinja2>=3.1",
    "httpx>=0.27",
    "Pillow>=10.0",
    "pymupdf>=1.24",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=5.0",
]

[project.scripts]
arc = "arc.cli:main"

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
```

- [ ] **Step 3: Create ARC/requirements.txt**

```
click>=8.1
jinja2>=3.1
httpx>=0.27
Pillow>=10.0
pymupdf>=1.24
pytest>=8.0
pytest-cov>=5.0
```

- [ ] **Step 4: Create ARC/arc/__init__.py**

```python
"""ARC — AI Draftsman. Blueprint to SketchUp pipeline."""

__version__ = "0.1.0"
```

- [ ] **Step 5: Create package __init__.py files**

Create empty `__init__.py` in: `arc/ingest/`, `arc/extract/`, `arc/model/`,
`arc/generate/`, `arc/llm/`

- [ ] **Step 6: Create project directories**

```bash
mkdir -p ARC/projects/seacove/{inputs,model,output,ground_truth}
mkdir -p ARC/templates/{ruby,layout}
mkdir -p ARC/reference
mkdir -p ARC/tests
```

- [ ] **Step 7: Install in dev mode and verify**

```bash
cd /Users/gclyle/GrowDirect/ARC
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python3 -c "import arc; print(arc.__version__)"
```

Expected: `0.1.0`

- [ ] **Step 8: Commit**

```bash
git add ARC/CLAUDE.md ARC/pyproject.toml ARC/requirements.txt ARC/arc/
git add ARC/projects/ ARC/templates/ ARC/reference/ ARC/tests/
git commit -m "feat(arc): project scaffold — package, CLI entry, directory structure"
```

---

### Task 2: Spatial Model Data Classes

**Files:**
- Create: `ARC/arc/model/spatial_model.py`
- Test: `ARC/tests/test_spatial_model.py`

- [ ] **Step 1: Write failing tests for spatial model**

```python
# tests/test_spatial_model.py
"""Tests for the ARC spatial model data classes."""
import pytest
from arc.model.spatial_model import (
    Project, Floor, Wall, Room, Opening, Post, Beam,
    RoofPlane, LotInfo, Source, Conflict, CoordinateSystem,
)


class TestWall:
    def test_wall_creation(self):
        wall = Wall(
            id="wall-south",
            from_pt=[0, 0],
            to_pt=[28, 0],
            wall_type="exterior",
            thickness_in=6,
            rooms={"interior": "kitchen-01", "exterior": None},
        )
        assert wall.id == "wall-south"
        assert wall.length_ft == pytest.approx(28.0)
        assert wall.thickness_ft == pytest.approx(0.5)

    def test_wall_length_diagonal(self):
        wall = Wall(
            id="wall-diag",
            from_pt=[0, 0],
            to_pt=[3, 4],
            wall_type="interior",
            thickness_in=4,
            rooms={"interior": "room-a", "exterior": "room-b"},
        )
        assert wall.length_ft == pytest.approx(5.0)

    def test_wall_direction_vector(self):
        wall = Wall(
            id="wall-east",
            from_pt=[0, 0],
            to_pt=[10, 0],
            wall_type="exterior",
            thickness_in=6,
            rooms={"interior": "room-a", "exterior": None},
        )
        dx, dy = wall.direction
        assert dx == pytest.approx(1.0)
        assert dy == pytest.approx(0.0)


class TestOpening:
    def test_opening_creation(self):
        opening = Opening(
            opening_type="door",
            position_along_wall=14.0,
            width=3.0,
            height=6.67,
            sill_height=0.0,
        )
        assert opening.opening_type == "door"
        assert opening.width == 3.0

    def test_opening_fits_wall(self):
        """Opening position + width must not exceed wall length."""
        opening = Opening(
            opening_type="window",
            position_along_wall=8.0,
            width=4.0,
            height=4.0,
            sill_height=3.0,
        )
        # 8 + 4 = 12, fits in a 15-foot wall
        assert opening.end_position == pytest.approx(12.0)


class TestRoom:
    def test_room_creation(self):
        room = Room(
            id="kitchen-01",
            label="Kitchen",
            polygon=[[0, 0], [12, 0], [12, 14], [0, 14]],
            wall_refs=["wall-s", "wall-e", "wall-n", "wall-w"],
        )
        assert room.id == "kitchen-01"
        assert len(room.polygon) == 4

    def test_room_area(self):
        room = Room(
            id="room-rect",
            label="Rectangle",
            polygon=[[0, 0], [10, 0], [10, 12], [0, 12]],
            wall_refs=[],
        )
        assert room.area_sqft == pytest.approx(120.0)

    def test_room_area_l_shape(self):
        """L-shaped room using shoelace formula."""
        room = Room(
            id="room-l",
            label="L-Shape",
            polygon=[[0, 0], [10, 0], [10, 6], [5, 6], [5, 12], [0, 12]],
            wall_refs=[],
        )
        # 10*6 + 5*6 = 60 + 30 = 90
        assert room.area_sqft == pytest.approx(90.0)


class TestFloor:
    def test_floor_creation(self):
        floor = Floor(
            level=0,
            label="Ground Floor",
            plate_height=8.0,
            z_origin=0.0,
            rooms=[],
            walls=[],
        )
        assert floor.level == 0
        assert floor.plate_height == 8.0


class TestProject:
    def test_project_creation(self):
        project = Project(
            schema_version=1,
            project_name="seacove",
            address="25 Seacove Dr, RPV",
            coordinate_system=CoordinateSystem(
                x="east", y="north", z="up", origin="SW corner of lot"
            ),
            lot=LotInfo(
                boundaries=[[0, 0], [80, 0], [80, 60], [0, 60]],
                setbacks={"front": 20, "rear": 15, "side_left": 5, "side_right": 5},
            ),
            floors=[],
            sources=[],
        )
        assert project.schema_version == 1
        assert project.project_name == "seacove"
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd /Users/gclyle/GrowDirect/ARC
source .venv/bin/activate
pytest tests/test_spatial_model.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'arc.model.spatial_model'`

- [ ] **Step 3: Implement spatial model data classes**

```python
# arc/model/spatial_model.py
"""Core spatial model data classes for ARC.

All dimensions in feet unless field name ends with _in (inches).
Coordinate system: X=East, Y=North, Z=Up.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field


@dataclass
class CoordinateSystem:
    x: str  # e.g., "east"
    y: str  # e.g., "north"
    z: str  # e.g., "up"
    origin: str  # e.g., "SW corner of lot"


@dataclass
class Source:
    id: str
    source_type: str  # "blueprint", "photo", "description"
    file: str
    page: int | None = None


@dataclass
class SourceRef:
    """Reference to a source with extraction confidence."""
    ref: str  # Source.id
    confidence: float  # 0.0 to 1.0


@dataclass
class Conflict:
    """When two sources disagree on a dimension."""
    field: str  # e.g., "wall-south.length"
    values: list[dict]  # [{"source": "plan", "value": 12.0}, {"source": "elev", "value": 12.5}]
    resolved: bool = False
    resolution: float | None = None


@dataclass
class Opening:
    opening_type: str  # "door", "window"
    position_along_wall: float  # feet from wall start
    width: float  # feet
    height: float  # feet
    sill_height: float  # feet from floor (0 for doors)

    @property
    def end_position(self) -> float:
        return self.position_along_wall + self.width


@dataclass
class Wall:
    id: str
    from_pt: list[float]  # [x, y] in feet
    to_pt: list[float]  # [x, y] in feet
    wall_type: str  # "exterior", "interior"
    thickness_in: int  # inches
    rooms: dict[str, str | None]  # {"interior": "room-id", "exterior": "room-id" | None}
    openings: list[Opening] = field(default_factory=list)
    sources: list[SourceRef] = field(default_factory=list)

    @property
    def length_ft(self) -> float:
        dx = self.to_pt[0] - self.from_pt[0]
        dy = self.to_pt[1] - self.from_pt[1]
        return math.sqrt(dx * dx + dy * dy)

    @property
    def thickness_ft(self) -> float:
        return self.thickness_in / 12.0

    @property
    def direction(self) -> tuple[float, float]:
        """Unit direction vector from start to end."""
        length = self.length_ft
        if length < 0.001:
            return (0.0, 0.0)
        dx = self.to_pt[0] - self.from_pt[0]
        dy = self.to_pt[1] - self.from_pt[1]
        return (dx / length, dy / length)


@dataclass
class Fixture:
    fixture_type: str  # "sink", "range", "toilet", etc.
    position: list[float]  # [x, y] in feet


@dataclass
class Room:
    id: str
    label: str
    polygon: list[list[float]]  # [[x, y], ...] in feet
    wall_refs: list[str]  # Wall.id references
    fixtures: list[Fixture] = field(default_factory=list)

    @property
    def area_sqft(self) -> float:
        """Polygon area via shoelace formula."""
        n = len(self.polygon)
        if n < 3:
            return 0.0
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += self.polygon[i][0] * self.polygon[j][1]
            area -= self.polygon[j][0] * self.polygon[i][1]
        return abs(area) / 2.0


@dataclass
class Post:
    position: list[float]  # [x, y] in feet
    size_in: int  # cross-section in inches (e.g., 4 for 4x4)
    material: str  # e.g., "douglas_fir"


@dataclass
class Beam:
    from_pt: list[float]  # [x, y] in feet
    to_pt: list[float]  # [x, y] in feet
    width_in: int  # inches
    depth_in: int  # inches
    z: float  # bottom of beam, in feet


@dataclass
class RoofPlane:
    label: str
    roof_type: str  # "flat", "gable", "hip"
    slope: float  # rise per foot of run
    overhang: float  # feet
    boundary: list[list[float]]  # [[x, y], ...]
    z_base: float  # feet


@dataclass
class LotInfo:
    boundaries: list[list[float]]  # [[x, y], ...]
    setbacks: dict[str, float]  # {"front": 20, "rear": 15, ...}
    slope: float | None = None


@dataclass
class Structural:
    posts: list[Post] = field(default_factory=list)
    beams: list[Beam] = field(default_factory=list)


@dataclass
class Roof:
    planes: list[RoofPlane] = field(default_factory=list)


@dataclass
class Site:
    roads: list = field(default_factory=list)
    driveway: list = field(default_factory=list)
    trees: list = field(default_factory=list)
    pool: dict = field(default_factory=dict)


@dataclass
class Floor:
    level: int
    label: str
    plate_height: float  # feet
    z_origin: float  # feet
    rooms: list[Room]
    walls: list[Wall]


@dataclass
class Project:
    schema_version: int
    project_name: str
    address: str
    coordinate_system: CoordinateSystem
    lot: LotInfo
    floors: list[Floor]
    sources: list[Source]
    structural: Structural = field(default_factory=Structural)
    roof: Roof = field(default_factory=Roof)
    site: Site = field(default_factory=Site)
    conflicts: list[Conflict] = field(default_factory=list)
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_spatial_model.py -v
```

Expected: all tests PASS

- [ ] **Step 5: Commit**

```bash
git add ARC/arc/model/spatial_model.py ARC/tests/test_spatial_model.py
git commit -m "feat(arc): spatial model data classes — Wall, Room, Floor, Project with computed properties"
```

---

### Task 3: Spatial Model Serialization (JSON round-trip)

**Files:**
- Create: `ARC/arc/model/serialization.py`
- Test: `ARC/tests/test_spatial_model.py` (append)

- [ ] **Step 1: Write failing tests for serialization**

```python
# Append to tests/test_spatial_model.py
import json
import tempfile
from pathlib import Path
from arc.model.serialization import save_project, load_project


class TestSerialization:
    def _make_sample_project(self) -> Project:
        wall = Wall(
            id="wall-south",
            from_pt=[0, 0],
            to_pt=[28, 0],
            wall_type="exterior",
            thickness_in=6,
            rooms={"interior": "living-01", "exterior": None},
            openings=[
                Opening(
                    opening_type="door",
                    position_along_wall=14.0,
                    width=3.0,
                    height=6.67,
                    sill_height=0.0,
                )
            ],
            sources=[SourceRef(ref="as-built", confidence=0.95)],
        )
        room = Room(
            id="living-01",
            label="Living Room",
            polygon=[[0, 0], [28, 0], [28, 18], [0, 18]],
            wall_refs=["wall-south"],
            fixtures=[Fixture(fixture_type="fireplace", position=[2, 9])],
        )
        floor = Floor(
            level=0,
            label="Ground Floor",
            plate_height=8.0,
            z_origin=0.0,
            rooms=[room],
            walls=[wall],
        )
        return Project(
            schema_version=1,
            project_name="seacove",
            address="25 Seacove Dr, RPV",
            coordinate_system=CoordinateSystem(
                x="east", y="north", z="up", origin="SW corner of lot"
            ),
            lot=LotInfo(
                boundaries=[[0, 0], [80, 0], [80, 60], [0, 60]],
                setbacks={"front": 20, "rear": 15, "side_left": 5, "side_right": 5},
            ),
            floors=[floor],
            sources=[Source(id="as-built", source_type="blueprint", file="inputs/plan.pdf", page=1)],
            structural=Structural(
                posts=[Post(position=[2, 0], size_in=4, material="douglas_fir")],
                beams=[Beam(from_pt=[-2, 9], to_pt=[30, 9], width_in=4, depth_in=10, z=8.0)],
            ),
        )

    def test_save_and_load_round_trip(self):
        project = self._make_sample_project()
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "model.json"
            save_project(project, path)
            loaded = load_project(path)
            assert loaded.project_name == "seacove"
            assert loaded.schema_version == 1
            assert len(loaded.floors) == 1
            assert len(loaded.floors[0].walls) == 1
            assert loaded.floors[0].walls[0].length_ft == pytest.approx(28.0)
            assert len(loaded.floors[0].walls[0].openings) == 1
            assert loaded.floors[0].rooms[0].area_sqft == pytest.approx(504.0)

    def test_save_produces_valid_json(self):
        project = self._make_sample_project()
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "model.json"
            save_project(project, path)
            data = json.loads(path.read_text())
            assert data["schema_version"] == 1
            assert data["project"] == "seacove"
            assert "floors" in data["structure"]

    def test_load_rejects_wrong_schema_version(self):
        bad_json = '{"schema_version": 999, "project": "test"}'
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "bad.json"
            path.write_text(bad_json)
            with pytest.raises(ValueError, match="schema_version"):
                load_project(path)
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_spatial_model.py::TestSerialization -v
```

Expected: FAIL — `ImportError`

- [ ] **Step 3: Implement serialization**

```python
# arc/model/serialization.py
"""JSON serialization for the ARC spatial model.

Handles conversion between Project dataclasses and the JSON schema
defined in the design spec (schema_version: 1).
"""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from arc.model.spatial_model import (
    Beam, Conflict, CoordinateSystem, Fixture, Floor, LotInfo,
    Opening, Post, Project, Roof, RoofPlane, Room, Site, Source,
    SourceRef, Structural, Wall,
)

SUPPORTED_SCHEMA_VERSIONS = {1}


def save_project(project: Project, path: Path) -> None:
    """Serialize a Project to JSON matching the spec schema."""
    data = _project_to_dict(project)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


def load_project(path: Path) -> Project:
    """Deserialize a Project from JSON."""
    data = json.loads(path.read_text())
    version = data.get("schema_version")
    if version not in SUPPORTED_SCHEMA_VERSIONS:
        raise ValueError(
            f"Unsupported schema_version: {version}. "
            f"Supported: {SUPPORTED_SCHEMA_VERSIONS}"
        )
    return _dict_to_project(data)


def _project_to_dict(p: Project) -> dict:
    """Convert Project to spec-format dict."""
    return {
        "schema_version": p.schema_version,
        "project": p.project_name,
        "address": p.address,
        "coordinate_system": asdict(p.coordinate_system),
        "lot": {
            "boundaries": p.lot.boundaries,
            "setbacks": p.lot.setbacks,
            "slope": p.lot.slope,
        },
        "structure": {
            "floors": [_floor_to_dict(f) for f in p.floors],
        },
        "structural": {
            "posts": [asdict(post) for post in p.structural.posts],
            "beams": [_beam_to_dict(b) for b in p.structural.beams],
        },
        "roof": {
            "planes": [_roof_plane_to_dict(rp) for rp in p.roof.planes],
        },
        "site": asdict(p.site),
        "sources": [_source_to_dict(s) for s in p.sources],
        "conflicts": [asdict(c) for c in p.conflicts],
    }


def _floor_to_dict(f: Floor) -> dict:
    return {
        "level": f.level,
        "label": f.label,
        "plate_height": f.plate_height,
        "z_origin": f.z_origin,
        "rooms": [_room_to_dict(r) for r in f.rooms],
        "walls": [_wall_to_dict(w) for w in f.walls],
    }


def _room_to_dict(r: Room) -> dict:
    d = {
        "id": r.id,
        "label": r.label,
        "polygon": r.polygon,
        "wall_refs": r.wall_refs,
    }
    if r.fixtures:
        d["fixtures"] = [{"type": f.fixture_type, "position": f.position} for f in r.fixtures]
    return d


def _wall_to_dict(w: Wall) -> dict:
    d = {
        "id": w.id,
        "from": w.from_pt,
        "to": w.to_pt,
        "type": w.wall_type,
        "thickness_in": w.thickness_in,
        "rooms": w.rooms,
    }
    if w.openings:
        d["openings"] = [_opening_to_dict(o) for o in w.openings]
    if w.sources:
        d["sources"] = [asdict(s) for s in w.sources]
    return d


def _opening_to_dict(o: Opening) -> dict:
    return {
        "type": o.opening_type,
        "position_along_wall": o.position_along_wall,
        "width": o.width,
        "height": o.height,
        "sill_height": o.sill_height,
    }


def _source_to_dict(s: Source) -> dict:
    d = {"id": s.id, "type": s.source_type, "file": s.file}
    if s.page is not None:
        d["page"] = s.page
    return d


def _roof_plane_to_dict(rp: RoofPlane) -> dict:
    return {
        "label": rp.label,
        "type": rp.roof_type,
        "slope": rp.slope,
        "overhang": rp.overhang,
        "boundary": rp.boundary,
        "z_base": rp.z_base,
    }


def _beam_to_dict(b: Beam) -> dict:
    return {
        "from": b.from_pt,
        "to": b.to_pt,
        "width_in": b.width_in,
        "depth_in": b.depth_in,
        "z": b.z,
    }


def _dict_to_project(d: dict) -> Project:
    """Convert spec-format dict to Project."""
    floors = [_dict_to_floor(f) for f in d.get("structure", {}).get("floors", [])]
    structural_data = d.get("structural", {})
    posts = [Post(**p) for p in structural_data.get("posts", [])]
    beams = [
        Beam(from_pt=b["from"], to_pt=b["to"], width_in=b["width_in"],
             depth_in=b["depth_in"], z=b["z"])
        for b in structural_data.get("beams", [])
    ]
    roof_data = d.get("roof", {})
    roof_planes = [
        RoofPlane(label=rp["label"], roof_type=rp["type"], slope=rp["slope"],
                  overhang=rp["overhang"], boundary=rp["boundary"], z_base=rp["z_base"])
        for rp in roof_data.get("planes", [])
    ]
    sources = [
        Source(id=s["id"], source_type=s["type"], file=s["file"], page=s.get("page"))
        for s in d.get("sources", [])
    ]
    conflicts = [Conflict(**c) for c in d.get("conflicts", [])]
    lot_data = d.get("lot", {})
    cs_data = d.get("coordinate_system", {})

    return Project(
        schema_version=d["schema_version"],
        project_name=d["project"],
        address=d.get("address", ""),
        coordinate_system=CoordinateSystem(**cs_data),
        lot=LotInfo(
            boundaries=lot_data.get("boundaries", []),
            setbacks=lot_data.get("setbacks", {}),
            slope=lot_data.get("slope"),
        ),
        floors=floors,
        sources=sources,
        structural=Structural(posts=posts, beams=beams),
        roof=Roof(planes=roof_planes),
        site=Site(**d.get("site", {})),
        conflicts=conflicts,
    )


def _dict_to_floor(d: dict) -> Floor:
    rooms = [_dict_to_room(r) for r in d.get("rooms", [])]
    walls = [_dict_to_wall(w) for w in d.get("walls", [])]
    return Floor(
        level=d["level"],
        label=d["label"],
        plate_height=d["plate_height"],
        z_origin=d.get("z_origin", 0.0),
        rooms=rooms,
        walls=walls,
    )


def _dict_to_room(d: dict) -> Room:
    fixtures = [Fixture(fixture_type=f["type"], position=f["position"]) for f in d.get("fixtures", [])]
    return Room(
        id=d["id"],
        label=d["label"],
        polygon=d["polygon"],
        wall_refs=d.get("wall_refs", []),
        fixtures=fixtures,
    )


def _dict_to_wall(d: dict) -> Wall:
    openings = [
        Opening(
            opening_type=o["type"],
            position_along_wall=o["position_along_wall"],
            width=o["width"],
            height=o["height"],
            sill_height=o["sill_height"],
        )
        for o in d.get("openings", [])
    ]
    sources = [SourceRef(**s) for s in d.get("sources", [])]
    return Wall(
        id=d["id"],
        from_pt=d["from"],
        to_pt=d["to"],
        wall_type=d["type"],
        thickness_in=d["thickness_in"],
        rooms=d.get("rooms", {}),
        openings=openings,
        sources=sources,
    )
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_spatial_model.py -v
```

Expected: all tests PASS

- [ ] **Step 5: Commit**

```bash
git add ARC/arc/model/serialization.py ARC/tests/test_spatial_model.py
git commit -m "feat(arc): spatial model JSON serialization — save/load with schema versioning"
```

---

### Task 4: Model Validator

**Files:**
- Create: `ARC/arc/model/validator.py`
- Test: `ARC/tests/test_validator.py`

- [ ] **Step 1: Write failing tests for validator**

```python
# tests/test_validator.py
"""Tests for spatial model validation."""
import pytest
from arc.model.spatial_model import (
    Floor, Opening, Room, Wall, Project, CoordinateSystem, LotInfo, Source,
)
from arc.model.validator import validate_floor, validate_project, ValidationError


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
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_validator.py -v
```

Expected: FAIL — `ImportError`

- [ ] **Step 3: Implement validator**

```python
# arc/model/validator.py
"""Spatial model consistency checks.

Validates that a model is internally consistent before
generating SketchUp Ruby scripts from it.
"""
from __future__ import annotations

from dataclasses import dataclass

from arc.model.spatial_model import Floor, Project


@dataclass
class ValidationError:
    level: str  # "error" or "warning"
    entity_id: str  # e.g., "wall-south"
    message: str


def validate_project(project: Project) -> list[ValidationError]:
    """Run all validation checks on a project."""
    errors: list[ValidationError] = []
    for floor in project.floors:
        errors.extend(validate_floor(floor))
    return errors


def validate_floor(floor: Floor) -> list[ValidationError]:
    """Validate all walls and rooms in a floor."""
    errors: list[ValidationError] = []
    wall_ids = {w.id for w in floor.walls}

    for wall in floor.walls:
        # Zero-length wall check
        if wall.length_ft < 0.01:
            errors.append(ValidationError(
                level="error",
                entity_id=wall.id,
                message=f"Wall '{wall.id}' has zero length",
            ))
            continue

        # Opening fits within wall
        for opening in wall.openings:
            if opening.end_position > wall.length_ft + 0.01:
                errors.append(ValidationError(
                    level="error",
                    entity_id=wall.id,
                    message=(
                        f"Opening at {opening.position_along_wall}' + "
                        f"{opening.width}' wide = {opening.end_position}' "
                        f"exceeds wall length {wall.length_ft:.1f}'"
                    ),
                ))

            # Opening height exceeds plate height
            if opening.sill_height + opening.height > floor.plate_height + 0.01:
                errors.append(ValidationError(
                    level="warning",
                    entity_id=wall.id,
                    message=(
                        f"Opening top ({opening.sill_height + opening.height:.1f}') "
                        f"exceeds plate height ({floor.plate_height}') in wall '{wall.id}'"
                    ),
                ))

    for room in floor.rooms:
        # Room wall_refs point to existing walls
        for ref in room.wall_refs:
            if ref not in wall_ids:
                errors.append(ValidationError(
                    level="error",
                    entity_id=room.id,
                    message=f"Room '{room.id}' references non-existent wall '{ref}'",
                ))

    return errors
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_validator.py -v
```

Expected: all tests PASS

- [ ] **Step 5: Commit**

```bash
git add ARC/arc/model/validator.py ARC/tests/test_validator.py
git commit -m "feat(arc): model validator — opening fit, wall length, room ref checks"
```

---

### Task 5: CLI Skeleton

**Files:**
- Create: `ARC/arc/cli.py`
- Create: `ARC/tests/conftest.py`

- [ ] **Step 1: Implement CLI with Click**

```python
# arc/cli.py
"""ARC CLI — AI Draftsman pipeline commands."""
import click
from pathlib import Path

PROJECTS_DIR = Path(__file__).parent.parent / "projects"


@click.group()
@click.version_option(package_name="arc")
def main():
    """ARC — AI Draftsman. Blueprint to SketchUp pipeline."""
    pass


@main.command()
@click.argument("project")
def ingest(project: str):
    """Normalize inputs (PDFs, photos, descriptions) for a project."""
    project_dir = PROJECTS_DIR / project
    if not project_dir.exists():
        click.echo(f"Project directory not found: {project_dir}")
        raise SystemExit(1)
    click.echo(f"Ingesting inputs for project: {project}")
    # TODO: implement ingest pipeline


@main.command()
@click.argument("project")
def extract(project: str):
    """Extract dimensions from blueprints using vision AI."""
    click.echo(f"Extracting dimensions for project: {project}")
    # TODO: implement extract pipeline


@main.command()
@click.argument("project")
def model(project: str):
    """Build spatial model from extraction data."""
    click.echo(f"Building spatial model for project: {project}")
    # TODO: implement model builder


@main.command()
@click.argument("project")
def validate(project: str):
    """Validate spatial model consistency."""
    from arc.model.serialization import load_project
    from arc.model.validator import validate_project

    model_path = PROJECTS_DIR / project / "model" / "spatial_model.json"
    if not model_path.exists():
        click.echo(f"Model not found: {model_path}")
        raise SystemExit(1)

    proj = load_project(model_path)
    errors = validate_project(proj)

    if not errors:
        click.echo("Model is valid. No errors found.")
    else:
        for err in errors:
            icon = "ERROR" if err.level == "error" else "WARN"
            click.echo(f"  [{icon}] {err.entity_id}: {err.message}")
        error_count = sum(1 for e in errors if e.level == "error")
        if error_count:
            click.echo(f"\n{error_count} error(s) found.")
            raise SystemExit(1)


@main.command()
@click.argument("project")
def generate(project: str):
    """Generate SketchUp Ruby scripts from spatial model."""
    click.echo(f"Generating Ruby scripts for project: {project}")
    # TODO: implement generate pipeline
```

- [ ] **Step 2: Create conftest.py with shared fixtures**

```python
# tests/conftest.py
"""Shared test fixtures for ARC."""
import pytest
from pathlib import Path
from arc.model.spatial_model import (
    Project, Floor, Wall, Room, Opening, CoordinateSystem,
    LotInfo, Source, SourceRef, Fixture, Post, Beam,
    Structural, Roof, RoofPlane,
)


@pytest.fixture
def sample_project() -> Project:
    """A minimal but complete Seacove-like project for testing."""
    wall_south = Wall(
        id="wall-south", from_pt=[0, 0], to_pt=[28, 0],
        wall_type="exterior", thickness_in=6,
        rooms={"interior": "living-01", "exterior": None},
        openings=[
            Opening("door", position_along_wall=14.0, width=3.0,
                    height=6.67, sill_height=0.0),
        ],
        sources=[SourceRef(ref="as-built", confidence=0.95)],
    )
    wall_north = Wall(
        id="wall-north", from_pt=[0, 18], to_pt=[28, 18],
        wall_type="exterior", thickness_in=6,
        rooms={"interior": "living-01", "exterior": None},
    )
    wall_west = Wall(
        id="wall-west", from_pt=[0, 0], to_pt=[0, 18],
        wall_type="exterior", thickness_in=6,
        rooms={"interior": "living-01", "exterior": None},
    )
    wall_east = Wall(
        id="wall-east", from_pt=[28, 0], to_pt=[28, 18],
        wall_type="exterior", thickness_in=6,
        rooms={"interior": "living-01", "exterior": None},
        openings=[
            Opening("window", position_along_wall=4.0, width=6.0,
                    height=4.0, sill_height=3.0),
        ],
    )
    room = Room(
        id="living-01", label="Living Room",
        polygon=[[0, 0], [28, 0], [28, 18], [0, 18]],
        wall_refs=["wall-south", "wall-east", "wall-north", "wall-west"],
        fixtures=[Fixture("fireplace", [2, 9])],
    )
    floor = Floor(
        level=0, label="Ground Floor", plate_height=8.0, z_origin=0.0,
        rooms=[room],
        walls=[wall_south, wall_north, wall_west, wall_east],
    )
    return Project(
        schema_version=1,
        project_name="test-project",
        address="25 Seacove Dr, RPV",
        coordinate_system=CoordinateSystem("east", "north", "up", "SW corner"),
        lot=LotInfo(
            boundaries=[[0, 0], [80, 0], [80, 60], [0, 60]],
            setbacks={"front": 20, "rear": 15, "side_left": 5, "side_right": 5},
        ),
        floors=[floor],
        sources=[Source("as-built", "blueprint", "inputs/plan.pdf", page=1)],
        structural=Structural(
            posts=[Post([2, 0], 4, "douglas_fir"), Post([8, 0], 4, "douglas_fir")],
            beams=[Beam([-2, 9], [30, 9], 4, 10, 8.0)],
        ),
        roof=Roof(planes=[
            RoofPlane("Living Wing", "flat", 0.25, 3.5,
                      [[0, 0], [28, 0], [28, 18], [0, 18]], 8.83),
        ]),
    )


@pytest.fixture
def arc_root() -> Path:
    return Path(__file__).parent.parent
```

- [ ] **Step 3: Test CLI runs**

```bash
cd /Users/gclyle/GrowDirect/ARC
source .venv/bin/activate
arc --version
arc validate seacove  # should fail with "Model not found" since no JSON yet
```

Expected: version prints `0.1.0`, validate exits with "Model not found"

- [ ] **Step 4: Commit**

```bash
git add ARC/arc/cli.py ARC/tests/conftest.py
git commit -m "feat(arc): CLI skeleton with Click — ingest, extract, model, validate, generate commands"
```

---

## Chunk 2: Ruby Code Generation + Jinja2 Templates

This chunk builds the generate stage — the part that takes a spatial model
and produces SketchUp Ruby scripts. After this chunk, you can hand-build
a spatial model JSON, run `arc generate seacove`, and get .rb files that
run in SketchUp Pro.

### Task 6: Jinja2 Template — Helpers Module

**Files:**
- Create: `ARC/templates/ruby/helpers.rb.j2`

- [ ] **Step 1: Create helpers template**

Port the existing `sketchup-ruby/00_helpers.rb` into a Jinja2 template that
can be parameterized with project-specific settings:

```ruby
{# templates/ruby/helpers.rb.j2 #}
# {{ project_name }} — SketchUp Ruby Helpers
# Generated by ARC AI Draftsman
# Load this FIRST before any other scripts.
#
# Usage: load '{{ output_path }}/00_helpers.rb'

module {{ module_name }}

  def self.ft(feet)
    feet * 12.0
  end

  def self.arch(dim_string)
    if dim_string.is_a?(Numeric)
      return dim_string * 12.0
    end
    s = dim_string.strip
    if s =~ /(\d+)'-?\s*(\d+)?[" ]*/
      feet = $1.to_f
      inches = $2 ? $2.to_f : 0.0
      return (feet * 12.0) + inches
    elsif s =~ /^[\d.]+$/
      return s.to_f * 12.0
    end
    0.0
  end

  def self.pt(x_ft, y_ft, z_ft = 0)
    Geom::Point3d.new(ft(x_ft), ft(y_ft), ft(z_ft))
  end

  def self.draw_rect(group, x, y, w, d, z = 0)
    pts = [pt(x, y, z), pt(x + w, y, z), pt(x + w, y + d, z), pt(x, y + d, z)]
    group.entities.add_face(pts)
  end

  def self.make_box(group, x, y, z, w, d, h)
    face = draw_rect(group, x, y, w, d, z)
    if face
      face.reverse! if face.normal.z < 0
      face.pushpull(ft(h))
    end
    face
  end

  def self.make_wall(group, p1, p2, thickness, height, z = 0)
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    len = Math.sqrt(dx * dx + dy * dy)
    return if len < 0.01
    nx = -dy / len * thickness / 2.0
    ny = dx / len * thickness / 2.0
    pts = [
      pt(p1[0] - nx, p1[1] - ny, z),
      pt(p2[0] - nx, p2[1] - ny, z),
      pt(p2[0] + nx, p2[1] + ny, z),
      pt(p1[0] + nx, p1[1] + ny, z)
    ]
    face = group.entities.add_face(pts)
    if face
      face.reverse! if face.normal.z < 0
      face.pushpull(ft(height))
    end
    face
  end

  def self.make_post(group, x_ft, y_ft, size_inches, height_ft, z_ft = 0)
    half = (size_inches / 2.0) / 12.0
    make_box(group, x_ft - half, y_ft - half, z_ft, half * 2, half * 2, height_ft)
  end

  def self.make_beam(group, p1, p2, width_in, depth_in, z_ft)
    w = width_in / 12.0 / 2.0
    d = depth_in / 12.0
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    len = Math.sqrt(dx * dx + dy * dy)
    return if len < 0.01
    nx = -dy / len * w
    ny = dx / len * w
    pts = [
      pt(p1[0] - nx, p1[1] - ny, z_ft),
      pt(p2[0] - nx, p2[1] - ny, z_ft),
      pt(p2[0] + nx, p2[1] + ny, z_ft),
      pt(p1[0] + nx, p1[1] + ny, z_ft)
    ]
    face = group.entities.add_face(pts)
    if face
      face.reverse! if face.normal.z < 0
      face.pushpull(ft(d))
    end
    face
  end

  def self.get_tag(model, name)
    tag = model.layers[name]
    tag = model.layers.add(name) unless tag
    tag
  end

  def self.tagged_group(parent_entities, model, tag_name)
    group = parent_entities.add_group
    group.layer = get_tag(model, tag_name)
    group
  end

  def self.set_color(group, r, g, b, alpha = 255)
    mat = group.model.materials.add("color_#{r}_#{g}_#{b}")
    mat.color = Sketchup::Color.new(r, g, b, alpha)
    group.material = mat
  end

end

puts "{{ module_name }} loaded. Usage: {{ module_name }}.ft(10), {{ module_name }}.pt(x,y,z), etc."
```

- [ ] **Step 2: Commit**

```bash
git add ARC/templates/ruby/helpers.rb.j2
git commit -m "feat(arc): Jinja2 helpers.rb template — ported from hand-written SeacoveHelpers"
```

---

### Task 7: Jinja2 Template — Walls with Boolean Cuts

**Files:**
- Create: `ARC/templates/ruby/walls.rb.j2`

- [ ] **Step 1: Create walls template**

```ruby
{# templates/ruby/walls.rb.j2 #}
# {{ project_name }} — Walls
# Generated by ARC AI Draftsman
#
# Walls are top-level per floor. Openings cut via boolean subtract (Pro only).
# Load helpers first: load '{{ output_path }}/00_helpers.rb'

model = Sketchup.active_model
ents = model.active_entities
model.start_operation("{{ project_name }} - Walls", true)

{% for floor in floors %}
# === {{ floor.label }} (Z: {{ floor.z_origin }}') ===
{% for wall in floor.walls %}
# {{ wall.id }} — {{ wall.wall_type }} ({{ "%.1f"|format(wall.length_ft) }}')
wall_grp = {{ module_name }}.tagged_group(ents, model, "Walls/{{ wall.wall_type | capitalize }}")
wall_grp.name = "{{ wall.id }}"
{{ module_name }}.make_wall(
  wall_grp,
  [{{ wall.from_x }}, {{ wall.from_y }}],
  [{{ wall.to_x }}, {{ wall.to_y }}],
  {{ wall.thickness_ft }},
  {{ floor.plate_height }}{% if floor.z_origin != 0.0 %},
  {{ floor.z_origin }}{% endif %}

)
{% if wall.openings %}

# Openings in {{ wall.id }}
{% for opening in wall.openings %}
cutter_{{ loop.index0 }} = {{ module_name }}.tagged_group(ents, model, "Temp")
{{ module_name }}.make_box(cutter_{{ loop.index0 }},
  {{ opening.cut_x }}, {{ opening.cut_y }}, {{ opening.sill_height }},
  {{ opening.cut_w }}, {{ opening.cut_d }}, {{ opening.height }}
)
wall_grp = wall_grp.subtract(cutter_{{ loop.index0 }})
{% endfor %}
{% endif %}

{% endfor %}
{% endfor %}
model.commit_operation
puts "Walls complete: {{ wall_count }} walls across {{ floors|length }} floor(s)"
```

- [ ] **Step 2: Commit**

```bash
git add ARC/templates/ruby/walls.rb.j2
git commit -m "feat(arc): Jinja2 walls.rb template — wall generation with boolean opening cuts"
```

---

### Task 8: Jinja2 Templates — Structure, Roof, Scenes

**Files:**
- Create: `ARC/templates/ruby/structure.rb.j2`
- Create: `ARC/templates/ruby/roof.rb.j2`
- Create: `ARC/templates/ruby/scenes.rb.j2`

- [ ] **Step 1: Create structure template (posts + beams)**

```ruby
{# templates/ruby/structure.rb.j2 #}
# {{ project_name }} — Structural: Posts & Beams
# Generated by ARC AI Draftsman

model = Sketchup.active_model
ents = model.active_entities
model.start_operation("{{ project_name }} - Structure", true)

# === POSTS ===
{% for post in posts %}
post_grp = {{ module_name }}.tagged_group(ents, model, "Structure/Posts")
post_grp.name = "Post_{{ loop.index0 }}"
{{ module_name }}.make_post(post_grp, {{ post.x }}, {{ post.y }}, {{ post.size_in }}, {{ plate_height }})
{% endfor %}

# === BEAMS ===
{% for beam in beams %}
beam_grp = {{ module_name }}.tagged_group(ents, model, "Structure/Beams")
beam_grp.name = "Beam_{{ loop.index0 }}"
{{ module_name }}.make_beam(beam_grp,
  [{{ beam.from_x }}, {{ beam.from_y }}],
  [{{ beam.to_x }}, {{ beam.to_y }}],
  {{ beam.width_in }}, {{ beam.depth_in }}, {{ beam.z }}
)
{% endfor %}

model.commit_operation
puts "Structure complete: {{ posts|length }} posts, {{ beams|length }} beams"
```

- [ ] **Step 2: Create roof template**

```ruby
{# templates/ruby/roof.rb.j2 #}
# {{ project_name }} — Roof Planes
# Generated by ARC AI Draftsman

model = Sketchup.active_model
ents = model.active_entities
model.start_operation("{{ project_name }} - Roof", true)

{% for plane in roof_planes %}
# {{ plane.label }} ({{ plane.type }}, slope {{ plane.slope }}:12, overhang {{ plane.overhang }}')
roof_grp = {{ module_name }}.tagged_group(ents, model, "Roof")
roof_grp.name = "Roof_{{ plane.label | replace(' ', '_') }}"
pts = [
{% for pt in plane.expanded_boundary %}
  {{ module_name }}.pt({{ pt[0] }}, {{ pt[1] }}, {{ plane.z_base }}),
{% endfor %}
]
face = roof_grp.entities.add_face(pts)
if face
  face.reverse! if face.normal.z < 0
  face.pushpull({{ module_name }}.ft(0.4))  # roof thickness
end
{% endfor %}

model.commit_operation
puts "Roof complete: {{ roof_planes|length }} plane(s)"
```

- [ ] **Step 3: Create scenes template**

```ruby
{# templates/ruby/scenes.rb.j2 #}
# {{ project_name }} — Scenes for Drawing Views
# Generated by ARC AI Draftsman
# Creates scenes used by LayOut for permit drawing viewports.

model = Sketchup.active_model
model.start_operation("{{ project_name }} - Scenes", true)

{% for scene in scenes %}
# === {{ scene.name }} ===
page = model.pages.add("{{ scene.name }}")
cam = Sketchup::Camera.new(
  Geom::Point3d.new({{ scene.eye | join(', ') }}),
  Geom::Point3d.new({{ scene.target | join(', ') }}),
  Geom::Vector3d.new({{ scene.up | join(', ') }})
)
{% if not scene.perspective %}
cam.perspective = false
cam.height = {{ scene.view_height }}
{% endif %}
page.use_camera = true
page.camera = cam

{% if scene.hidden_tags %}
# Hide tags for this view
{% for tag_name in scene.hidden_tags %}
tag = model.layers["{{ tag_name }}"]
page.set_visibility(tag, false) if tag
{% endfor %}
{% endif %}

{% if scene.section_plane %}
# Section cut
sp = model.active_entities.add_section_plane(
  [Geom::Point3d.new({{ scene.section_plane.point | join(', ') }}),
   Geom::Vector3d.new({{ scene.section_plane.normal | join(', ') }})]
)
{% endif %}

{% endfor %}

model.commit_operation
puts "Scenes created: {{ scenes|length }} view(s)"
model.pages.selected_page = model.pages["{{ scenes[0].name }}"] if model.pages["{{ scenes[0].name }}"]
```

- [ ] **Step 4: Commit**

```bash
git add ARC/templates/ruby/structure.rb.j2 ARC/templates/ruby/roof.rb.j2 ARC/templates/ruby/scenes.rb.j2
git commit -m "feat(arc): Jinja2 templates — structure, roof, scenes for SketchUp generation"
```

---

### Task 9: Ruby Generator — Spatial Model to Rendered Scripts

**Files:**
- Create: `ARC/arc/generate/sketchup_ruby.py`
- Test: `ARC/tests/test_ruby_generation.py`

- [ ] **Step 1: Write failing tests for Ruby generation**

```python
# tests/test_ruby_generation.py
"""Tests for SketchUp Ruby code generation from spatial model."""
import pytest
from pathlib import Path
from arc.generate.sketchup_ruby import generate_ruby_scripts


class TestRubyGeneration:
    def test_generates_helpers_file(self, sample_project, tmp_path):
        generate_ruby_scripts(sample_project, tmp_path)
        helpers = tmp_path / "00_helpers.rb"
        assert helpers.exists()
        content = helpers.read_text()
        assert "module " in content
        assert "def self.ft(feet)" in content
        assert "def self.make_wall" in content

    def test_generates_walls_file(self, sample_project, tmp_path):
        generate_ruby_scripts(sample_project, tmp_path)
        walls = tmp_path / "04_walls.rb"
        assert walls.exists()
        content = walls.read_text()
        assert "wall-south" in content
        assert "start_operation" in content
        assert "commit_operation" in content
        # Should have the door opening cut
        assert "subtract" in content

    def test_generates_structure_file(self, sample_project, tmp_path):
        generate_ruby_scripts(sample_project, tmp_path)
        structure = tmp_path / "05_structure.rb"
        assert structure.exists()
        content = structure.read_text()
        assert "make_post" in content
        assert "make_beam" in content

    def test_generates_roof_file(self, sample_project, tmp_path):
        generate_ruby_scripts(sample_project, tmp_path)
        roof = tmp_path / "06_roof.rb"
        assert roof.exists()
        content = roof.read_text()
        assert "Living_Wing" in content

    def test_wall_opening_positions_computed(self, sample_project, tmp_path):
        """Opening cut positions must be pre-computed from wall geometry."""
        generate_ruby_scripts(sample_project, tmp_path)
        walls = tmp_path / "04_walls.rb"
        content = walls.read_text()
        # The door is at position 14.0 along wall-south (from [0,0] to [28,0])
        # So cut_x should be 14.0, cut_y should be offset for wall thickness
        assert "14.0" in content  # position along wall

    def test_ruby_syntax_no_python_artifacts(self, sample_project, tmp_path):
        """Generated Ruby should not contain Python/Jinja2 artifacts."""
        generate_ruby_scripts(sample_project, tmp_path)
        for rb_file in tmp_path.glob("*.rb"):
            content = rb_file.read_text()
            assert "{{" not in content, f"Unrendered Jinja2 in {rb_file.name}"
            assert "{%" not in content, f"Unrendered Jinja2 in {rb_file.name}"
            assert "None" not in content, f"Python None in {rb_file.name}"
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_ruby_generation.py -v
```

Expected: FAIL — `ImportError`

- [ ] **Step 3: Implement the Ruby generator**

```python
# arc/generate/sketchup_ruby.py
"""Generate SketchUp Ruby scripts from a spatial model.

Reads the spatial model, pre-computes derived geometry fields,
and renders Jinja2 templates to produce .rb files.
"""
from __future__ import annotations

import math
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from arc.model.spatial_model import Project, Wall, Opening

TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates" / "ruby"


def generate_ruby_scripts(project: Project, output_dir: Path) -> list[Path]:
    """Generate all .rb scripts for the project.

    Returns list of generated file paths.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    module_name = _module_name(project.project_name)
    output_path = str(output_dir)
    generated: list[Path] = []

    # 00_helpers.rb
    ctx = {"project_name": project.project_name, "module_name": module_name,
           "output_path": output_path}
    generated.append(_render(env, "helpers.rb.j2", output_dir / "00_helpers.rb", ctx))

    # 04_walls.rb
    floors_ctx = _prepare_floors_context(project)
    wall_count = sum(len(f["walls"]) for f in floors_ctx)
    ctx = {"project_name": project.project_name, "module_name": module_name,
           "floors": floors_ctx, "wall_count": wall_count, "output_path": output_path}
    generated.append(_render(env, "walls.rb.j2", output_dir / "04_walls.rb", ctx))

    # 05_structure.rb
    posts_ctx = [{"x": p.position[0], "y": p.position[1], "size_in": p.size_in}
                 for p in project.structural.posts]
    beams_ctx = [{"from_x": b.from_pt[0], "from_y": b.from_pt[1],
                  "to_x": b.to_pt[0], "to_y": b.to_pt[1],
                  "width_in": b.width_in, "depth_in": b.depth_in, "z": b.z}
                 for b in project.structural.beams]
    plate_height = project.floors[0].plate_height if project.floors else 8.0
    ctx = {"project_name": project.project_name, "module_name": module_name,
           "posts": posts_ctx, "beams": beams_ctx, "plate_height": plate_height}
    generated.append(_render(env, "structure.rb.j2", output_dir / "05_structure.rb", ctx))

    # 06_roof.rb
    roof_ctx = _prepare_roof_context(project)
    ctx = {"project_name": project.project_name, "module_name": module_name,
           "roof_planes": roof_ctx}
    generated.append(_render(env, "roof.rb.j2", output_dir / "06_roof.rb", ctx))

    # 08_scenes.rb (deferred — requires scene definitions in spatial model)
    # Scenes will be generated when the model includes camera/section data.
    # For v0, scenes are created manually in SketchUp.

    return generated


def _render(env: Environment, template_name: str, output_path: Path, context: dict) -> Path:
    template = env.get_template(template_name)
    content = template.render(**context)
    output_path.write_text(content + "\n")
    return output_path


def _module_name(project_name: str) -> str:
    """Convert project name to Ruby module name: seacove → SeacoveHelpers."""
    return project_name.replace("-", "_").title().replace("_", "") + "Helpers"


def _prepare_floors_context(project: Project) -> list[dict]:
    """Pre-compute derived wall/opening geometry for template rendering."""
    floors = []
    for floor in project.floors:
        walls = []
        for wall in floor.walls:
            wall_ctx = {
                "id": wall.id,
                "wall_type": wall.wall_type,
                "from_x": wall.from_pt[0],
                "from_y": wall.from_pt[1],
                "to_x": wall.to_pt[0],
                "to_y": wall.to_pt[1],
                "thickness_ft": wall.thickness_ft,
                "length_ft": wall.length_ft,
                "openings": [_compute_opening_cut(wall, o) for o in wall.openings],
            }
            walls.append(wall_ctx)
        floors.append({
            "label": floor.label,
            "z_origin": floor.z_origin,
            "plate_height": floor.plate_height,
            "walls": walls,
        })
    return floors


def _prepare_roof_context(project: Project) -> list[dict]:
    """Pre-compute expanded roof boundaries (with overhangs applied)."""
    planes = []
    for rp in project.roof.planes:
        expanded = _expand_boundary(rp.boundary, rp.overhang)
        planes.append({
            "label": rp.label,
            "type": rp.roof_type,
            "slope": rp.slope,
            "overhang": rp.overhang,
            "boundary": rp.boundary,
            "expanded_boundary": expanded,
            "z_base": rp.z_base,
        })
    return planes


def _expand_boundary(boundary: list[list[float]], overhang: float) -> list[list[float]]:
    """Expand a polygon boundary outward by overhang distance.

    Simple approach: compute centroid, then move each vertex away from
    centroid by overhang distance along the vertex-centroid vector.
    Works well for convex polygons (most roof planes).
    """
    n = len(boundary)
    if n < 3:
        return boundary
    cx = sum(p[0] for p in boundary) / n
    cy = sum(p[1] for p in boundary) / n
    expanded = []
    for p in boundary:
        dx = p[0] - cx
        dy = p[1] - cy
        dist = math.sqrt(dx * dx + dy * dy)
        if dist < 0.001:
            expanded.append(p)
            continue
        scale = (dist + overhang) / dist
        expanded.append([round(cx + dx * scale, 4), round(cy + dy * scale, 4)])
    return expanded


def _compute_opening_cut(wall: Wall, opening: Opening) -> dict:
    """Compute the 3D cut box for an opening, oriented along the wall.

    Uses make_wall-style geometry (oriented along wall direction) rather
    than axis-aligned make_box, so cuts work for walls running in any
    direction. The template uses make_box for axis-aligned walls and
    falls back to make_wall-style cuts for angled walls.

    For simplicity in v0, we compute axis-aligned cut boxes that work
    correctly for cardinal-direction walls (N-S, E-W). The cut box
    dimensions are swapped based on wall direction to stay axis-aligned.
    """
    dx, dy = wall.direction
    pos = opening.position_along_wall

    # Position along the wall from start point
    wall_start_x = wall.from_pt[0] + dx * pos
    wall_start_y = wall.from_pt[1] + dy * pos

    # Determine if wall runs primarily in X or Y direction
    # and compute axis-aligned cut box accordingly
    half_t = wall.thickness_ft / 2.0 + 0.005  # slight oversize for clean cut
    if abs(dx) >= abs(dy):
        # Wall runs primarily E-W: opening width along X, thickness along Y
        cut_x = wall_start_x
        cut_y = wall_start_y - half_t
        cut_w = opening.width
        cut_d = wall.thickness_ft + 0.01
    else:
        # Wall runs primarily N-S: opening width along Y, thickness along X
        cut_x = wall_start_x - half_t
        cut_y = wall_start_y
        cut_w = wall.thickness_ft + 0.01
        cut_d = opening.width

    return {
        "cut_x": round(cut_x, 4),
        "cut_y": round(cut_y, 4),
        "cut_w": round(cut_w, 4),
        "cut_d": round(cut_d, 4),
        "sill_height": opening.sill_height,
        "height": opening.height,
        "width": opening.width,
        "type": opening.opening_type,
    }
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_ruby_generation.py -v
```

Expected: all tests PASS

- [ ] **Step 5: Commit**

```bash
git add ARC/arc/generate/sketchup_ruby.py ARC/tests/test_ruby_generation.py
git commit -m "feat(arc): Ruby code generator — spatial model to SketchUp .rb via Jinja2 templates"
```

---

### Task 10: Wire Generate Command into CLI

**Files:**
- Modify: `ARC/arc/cli.py` — replace `generate` command stub

- [ ] **Step 1: Update the generate command**

Replace the `generate` command in `cli.py`:

```python
@main.command()
@click.argument("project")
def generate(project: str):
    """Generate SketchUp Ruby scripts from spatial model."""
    from arc.model.serialization import load_project
    from arc.model.validator import validate_project
    from arc.generate.sketchup_ruby import generate_ruby_scripts

    model_path = PROJECTS_DIR / project / "model" / "spatial_model.json"
    if not model_path.exists():
        click.echo(f"Model not found: {model_path}")
        raise SystemExit(1)

    proj = load_project(model_path)

    # Validate first
    errors = validate_project(proj)
    error_count = sum(1 for e in errors if e.level == "error")
    if error_count:
        click.echo(f"Model has {error_count} error(s). Fix before generating:")
        for err in errors:
            click.echo(f"  [{err.level.upper()}] {err.entity_id}: {err.message}")
        raise SystemExit(1)

    output_dir = PROJECTS_DIR / project / "output"
    generated = generate_ruby_scripts(proj, output_dir)
    click.echo(f"Generated {len(generated)} Ruby scripts in {output_dir}/")
    for path in generated:
        click.echo(f"  {path.name}")
```

- [ ] **Step 2: Test end-to-end with a manual JSON model**

Create `ARC/projects/seacove/model/spatial_model.json` by running:

```bash
cd /Users/gclyle/GrowDirect/ARC
source .venv/bin/activate
python3 -c "
from arc.model.serialization import save_project
from tests.conftest import *
# Build the fixture manually
from arc.model.spatial_model import *
# (use the sample_project fixture code from conftest.py)
# ... save to projects/seacove/model/spatial_model.json
"
```

Or write a small script that saves the sample project. Then:

```bash
arc generate seacove
```

Expected: generates .rb files in `projects/seacove/output/`

- [ ] **Step 3: Commit**

```bash
git add ARC/arc/cli.py
git commit -m "feat(arc): wire generate command — validates model then renders Ruby scripts"
```

---

## Chunk 3: Ingest + Extract + Seacove Ground Truth

This chunk builds the input side of the pipeline: reading blueprints,
calling Ollama vision, and comparing against Seacove ground truth.
After this chunk, the full v0 pipeline works end-to-end.

### Task 11: LLM Vision Client

**Files:**
- Create: `ARC/arc/llm/vision.py`
- Create: `ARC/arc/llm/embeddings.py` (stub)

- [ ] **Step 1: Implement Ollama vision client**

```python
# arc/llm/vision.py
"""Ollama vision API client for blueprint analysis."""
from __future__ import annotations

import base64
import os
import httpx
from pathlib import Path

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
DEFAULT_VISION_MODEL = os.environ.get("ARC_VISION_MODEL", "llava:34b")


def analyze_image(
    image_path: Path,
    prompt: str,
    model: str = DEFAULT_VISION_MODEL,
    timeout: float = 120.0,
) -> dict:
    """Send an image to Ollama vision model with a prompt.

    Returns: {"response": str, "model": str, "done": bool}
    """
    image_data = base64.b64encode(image_path.read_bytes()).decode("utf-8")

    payload = {
        "model": model,
        "prompt": prompt,
        "images": [image_data],
        "stream": False,
    }

    with httpx.Client(timeout=timeout) as client:
        resp = client.post(f"{OLLAMA_URL}/api/generate", json=payload)
        resp.raise_for_status()
        return resp.json()


def check_model_available(model: str = DEFAULT_VISION_MODEL) -> bool:
    """Check if the vision model is available in Ollama."""
    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(f"{OLLAMA_URL}/api/tags")
            resp.raise_for_status()
            models = [m["name"] for m in resp.json().get("models", [])]
            return any(model in m for m in models)
    except httpx.HTTPError:
        return False
```

- [ ] **Step 2: Create `arc/llm/__init__.py`**

```python
# arc/llm/__init__.py
"""LLM service layer — all Ollama communication goes through here."""
```

- [ ] **Step 3: Create embeddings stub**

```python
# arc/llm/embeddings.py
"""Ollama embeddings client — stub for future use."""
```

- [ ] **Step 4: Commit**

```bash
git add ARC/arc/llm/__init__.py ARC/arc/llm/vision.py ARC/arc/llm/embeddings.py
git commit -m "feat(arc): Ollama vision client — image analysis for blueprint extraction"
```

---

### Task 12: Blueprint Ingest

**Files:**
- Create: `ARC/arc/ingest/blueprint_reader.py`
- Create: `ARC/arc/ingest/description.py`
- Create: `ARC/arc/ingest/photo_reader.py` (stub)
- Test: `ARC/tests/test_ingest.py`

- [ ] **Step 1: Write failing tests for blueprint reader**

```python
# tests/test_ingest.py
"""Tests for the ARC ingest pipeline."""
import pytest
from pathlib import Path
from unittest.mock import patch
from arc.ingest.blueprint_reader import extract_pages_from_pdf, normalize_image


class TestBlueprintReader:
    def test_extract_pages_returns_images(self, tmp_path, arc_root):
        """PDF extraction should produce one image per page."""
        # Use a real blueprint if available, otherwise skip
        bp_dir = arc_root / "25 Seacove Blueprints"
        test_pdf = bp_dir / "25 Seacove Original Plan Page 3 - Floor Plan.pdf"
        if not test_pdf.exists():
            pytest.skip("Blueprint PDF not available")

        images = extract_pages_from_pdf(test_pdf, tmp_path)
        assert len(images) >= 1
        for img in images:
            assert img.exists()
            assert img.suffix == ".png"

    def test_normalize_image_resizes(self, tmp_path):
        """Normalize should produce a consistent size for vision model."""
        # Create a test image
        from PIL import Image
        test_img = tmp_path / "test.png"
        Image.new("RGB", (4000, 3000)).save(test_img)

        result = normalize_image(test_img, tmp_path / "normalized.png")
        assert result.exists()
        img = Image.open(result)
        assert max(img.size) <= 2048  # max dimension for vision model
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_ingest.py -v
```

- [ ] **Step 3: Implement blueprint reader**

```python
# arc/ingest/blueprint_reader.py
"""Read blueprint PDFs and normalize images for vision AI extraction."""
from __future__ import annotations

from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image


def extract_pages_from_pdf(pdf_path: Path, output_dir: Path, dpi: int = 300) -> list[Path]:
    """Extract each page of a PDF as a PNG image.

    Args:
        pdf_path: Path to the PDF file.
        output_dir: Directory to save extracted images.
        dpi: Resolution for rendering (300 for architectural drawings).

    Returns: List of paths to extracted PNG images.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(str(pdf_path))
    images: list[Path] = []

    for i, page in enumerate(doc):
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat)
        stem = pdf_path.stem.replace(" ", "_")
        out_path = output_dir / f"{stem}_page{i + 1}.png"
        pix.save(str(out_path))
        images.append(out_path)

    doc.close()
    return images


def normalize_image(image_path: Path, output_path: Path, max_dim: int = 2048) -> Path:
    """Resize image so max dimension is max_dim. Preserves aspect ratio."""
    img = Image.open(image_path)
    w, h = img.size
    if max(w, h) > max_dim:
        scale = max_dim / max(w, h)
        new_size = (int(w * scale), int(h * scale))
        img = img.resize(new_size, Image.LANCZOS)
    img.save(output_path)
    return output_path
```

- [ ] **Step 4: Create description.py and photo_reader.py stubs**

```python
# arc/ingest/description.py
"""Parse natural language descriptions into structured intent."""
from __future__ import annotations


def parse_description(text: str) -> dict:
    """Parse a natural language description of a space.

    Returns structured intent dict with extracted room names,
    dimensions (if mentioned), and modifications requested.
    """
    # v0: return raw text for manual processing
    return {"raw_text": text, "rooms": [], "modifications": []}
```

```python
# arc/ingest/photo_reader.py
"""Process site photos — normalize and tag for reference."""
from __future__ import annotations

from pathlib import Path
from arc.ingest.blueprint_reader import normalize_image


def process_photos(photo_dir: Path, output_dir: Path) -> list[Path]:
    """Normalize all photos in a directory."""
    output_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for photo in sorted(photo_dir.iterdir()):
        if photo.suffix.lower() in (".jpg", ".jpeg", ".png"):
            out = output_dir / f"photo_{photo.stem}.png"
            normalize_image(photo, out)
            results.append(out)
    return results
```

- [ ] **Step 5: Run tests**

```bash
pytest tests/test_ingest.py -v
```

Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add ARC/arc/ingest/ ARC/tests/test_ingest.py
git commit -m "feat(arc): ingest pipeline — PDF extraction, image normalization, description parser"
```

---

### Task 13: Dimension Extractor (Vision AI)

**Files:**
- Create: `ARC/arc/extract/dimension_extractor.py`
- Create: `ARC/arc/extract/sheet_classifier.py`
- Create: `ARC/arc/extract/element_detector.py` (stub)

- [ ] **Step 1: Implement dimension extractor**

```python
# arc/extract/dimension_extractor.py
"""Extract dimensions from blueprint images using Ollama vision."""
from __future__ import annotations

import json
from pathlib import Path

from arc.llm.vision import analyze_image

DIMENSION_PROMPT = """You are an architectural draftsman reading a blueprint scan.

Analyze this architectural drawing and extract ALL dimensions you can read.
For each dimension, provide:
- description: what the dimension measures (e.g., "south wall length", "room width")
- value_ft: the dimension in feet (convert from feet-inches notation)
- value_raw: the original notation as written on the drawing
- confidence: 0.0-1.0 how confident you are in the reading
- location: where on the drawing (e.g., "bottom dimension string", "room label")

Return ONLY valid JSON in this format:
{
  "sheet_type": "floor_plan" | "elevation" | "section" | "site_plan" | "foundation",
  "scale": "1/4 inch = 1 foot" or similar,
  "dimensions": [
    {
      "description": "south wall total length",
      "value_ft": 41.58,
      "value_raw": "41'-7\\"",
      "confidence": 0.7,
      "location": "bottom dimension string"
    }
  ],
  "notes": ["any observations about scan quality or unreadable areas"]
}
"""


def extract_dimensions(image_path: Path, model: str | None = None) -> dict:
    """Extract dimensions from a blueprint image.

    Returns structured dimension data with confidence scores.
    """
    kwargs = {"image_path": image_path, "prompt": DIMENSION_PROMPT}
    if model:
        kwargs["model"] = model

    result = analyze_image(**kwargs)
    response_text = result.get("response", "")

    # Try to parse JSON from the response
    try:
        # Find JSON in the response (model may include text before/after)
        start = response_text.index("{")
        end = response_text.rindex("}") + 1
        data = json.loads(response_text[start:end])
        return data
    except (ValueError, json.JSONDecodeError):
        return {
            "sheet_type": "unknown",
            "scale": "unknown",
            "dimensions": [],
            "notes": [f"Failed to parse vision response: {response_text[:200]}"],
            "raw_response": response_text,
        }


def save_extraction(data: dict, output_path: Path) -> None:
    """Save extraction results to JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(data, indent=2) + "\n")
```

- [ ] **Step 2: Create sheet classifier**

```python
# arc/extract/sheet_classifier.py
"""Classify blueprint sheet type using vision AI."""
from __future__ import annotations

from pathlib import Path
from arc.llm.vision import analyze_image

CLASSIFY_PROMPT = """Look at this architectural drawing and classify it.

Return ONLY one of these types:
- floor_plan
- foundation_plan
- elevation
- section
- site_plan
- interior_elevation
- detail
- hvac
- electrical
- schedule

Return just the type, nothing else."""


def classify_sheet(image_path: Path, model: str | None = None) -> str:
    kwargs = {"image_path": image_path, "prompt": CLASSIFY_PROMPT}
    if model:
        kwargs["model"] = model
    result = analyze_image(**kwargs)
    response = result.get("response", "").strip().lower()
    valid_types = {
        "floor_plan", "foundation_plan", "elevation", "section",
        "site_plan", "interior_elevation", "detail", "hvac",
        "electrical", "schedule",
    }
    return response if response in valid_types else "unknown"
```

- [ ] **Step 3: Create element detector stub**

```python
# arc/extract/element_detector.py
"""Detect architectural elements (doors, windows, fixtures) in blueprints.

Stub for v0 — full implementation will use vision AI to identify
and locate elements on floor plans.
"""
from __future__ import annotations

from pathlib import Path


def detect_elements(image_path: Path) -> dict:
    """Detect architectural elements in a blueprint image."""
    return {"doors": [], "windows": [], "fixtures": [], "notes": ["stub — not yet implemented"]}
```

- [ ] **Step 4: Commit**

```bash
git add ARC/arc/extract/
git commit -m "feat(arc): extract pipeline — dimension extractor, sheet classifier, element detector stub"
```

---

### Task 14: Seacove Ground Truth + Accuracy Test

**Files:**
- Create: `ARC/projects/seacove/ground_truth/dimensions.json`
- Test: `ARC/tests/test_extract_accuracy.py`

- [ ] **Step 1: Create ground truth JSON from blueprint-dimensions-reference.md**

Convert the known dimensions from the reference doc into structured JSON:

```json
{
  "source": "blueprint-dimensions-reference.md",
  "note": "Dimensions marked with [?] have low confidence and need field verification",
  "dimensions": [
    {"description": "overall width E-W", "value_ft": 41.58, "raw": "41'-7\"", "confidence": 0.5, "sheet": "floor_plan"},
    {"description": "garage width", "value_ft": 19.0, "raw": "19'-0\"", "confidence": 0.6, "sheet": "floor_plan"},
    {"description": "living room width", "value_ft": 22.5, "raw": "22'-6\"", "confidence": 0.5, "sheet": "floor_plan"},
    {"description": "living room depth segment", "value_ft": 11.42, "raw": "11'-5\"", "confidence": 0.5, "sheet": "floor_plan"},
    {"description": "roof overhang", "value_ft": 3.5, "raw": "3'-6\"", "confidence": 0.5, "sheet": "elevation"},
    {"description": "ceiling height", "value_ft": 8.0, "raw": "8'-0\"", "confidence": 0.5, "sheet": "section"},
    {"description": "existing storage area width", "value_ft": 8.0, "raw": "8'-0\"", "confidence": 0.7, "sheet": "A-2"},
    {"description": "existing storage area depth", "value_ft": 14.0, "raw": "14'-0\"", "confidence": 0.7, "sheet": "A-2"},
    {"description": "1960 addition width", "value_ft": 36.0, "raw": "36'-0\"", "confidence": 0.5, "sheet": "addition"},
    {"description": "garage addition width", "value_ft": 20.0, "raw": "20'-0\"", "confidence": 0.5, "sheet": "garage"}
  ]
}
```

- [ ] **Step 2: Write accuracy test**

```python
# tests/test_extract_accuracy.py
"""Tests for extraction accuracy against Seacove ground truth.

These tests require Ollama running with a vision model.
Skip if Ollama is not available.
"""
import json
import pytest
from pathlib import Path

from arc.llm.vision import check_model_available


ARC_ROOT = Path(__file__).parent.parent
GROUND_TRUTH_PATH = ARC_ROOT / "projects/seacove/ground_truth/dimensions.json"
BLUEPRINT_DIR = ARC_ROOT / "25 Seacove Blueprints"


@pytest.fixture
def ground_truth():
    if not GROUND_TRUTH_PATH.exists():
        pytest.skip("Ground truth file not found")
    return json.loads(GROUND_TRUTH_PATH.read_text())


@pytest.mark.skipif(
    not check_model_available(),
    reason="Ollama vision model not available"
)
class TestExtractionAccuracy:
    def test_floor_plan_dimensions_within_tolerance(self, ground_truth, tmp_path):
        """Extracted floor plan dimensions should be within 6 inches of ground truth."""
        from arc.ingest.blueprint_reader import extract_pages_from_pdf
        from arc.extract.dimension_extractor import extract_dimensions

        floor_plan = BLUEPRINT_DIR / "25 Seacove Original Plan Page 3 - Floor Plan.pdf"
        if not floor_plan.exists():
            pytest.skip("Floor plan PDF not found")

        # Extract pages
        images = extract_pages_from_pdf(floor_plan, tmp_path)
        assert len(images) >= 1

        # Run dimension extraction
        result = extract_dimensions(images[0])
        extracted_dims = {d["description"]: d["value_ft"] for d in result.get("dimensions", [])}

        # Compare against ground truth
        gt_floor = [d for d in ground_truth["dimensions"] if d["sheet"] == "floor_plan"]
        matches = 0
        for gt_dim in gt_floor:
            # Find closest match in extracted dimensions
            for desc, value in extracted_dims.items():
                if abs(value - gt_dim["value_ft"]) <= 0.5:  # within 6 inches
                    matches += 1
                    break

        # v0 target: pipeline produces at least one matching dimension
        # This will improve as we tune prompts and models
        print(f"Matched {matches}/{len(gt_floor)} floor plan dimensions within 6 inches")
        assert matches > 0, (
            f"No dimensions matched within 6 inches. "
            f"Extracted: {list(extracted_dims.keys())}"
        )
```

- [ ] **Step 3: Commit**

```bash
git add ARC/projects/seacove/ground_truth/dimensions.json ARC/tests/test_extract_accuracy.py
git commit -m "feat(arc): Seacove ground truth + extraction accuracy test framework"
```

---

### Task 15: Wire Ingest + Extract into CLI

**Files:**
- Modify: `ARC/arc/cli.py` — replace `ingest` and `extract` stubs

- [ ] **Step 1: Implement ingest command**

```python
@main.command()
@click.argument("project")
def ingest(project: str):
    """Normalize inputs (PDFs, photos, descriptions) for a project."""
    from arc.ingest.blueprint_reader import extract_pages_from_pdf, normalize_image

    project_dir = PROJECTS_DIR / project
    if not project_dir.exists():
        click.echo(f"Project directory not found: {project_dir}")
        raise SystemExit(1)

    inputs_dir = project_dir / "inputs"
    inputs_dir.mkdir(exist_ok=True)

    # Find PDFs in the project's blueprints directory
    blueprint_dir = project_dir / "blueprints"
    if not blueprint_dir.exists():
        click.echo(f"No blueprints directory at {blueprint_dir}")
        click.echo("Create it and add PDF/image files, or symlink to your blueprint folder:")
        click.echo(f"  ln -s /path/to/blueprints {blueprint_dir}")
        raise SystemExit(1)

    pdf_count = 0
    for pdf in sorted(blueprint_dir.glob("*.pdf")):
        images = extract_pages_from_pdf(pdf, inputs_dir / "pages")
        for img in images:
            normalize_image(img, inputs_dir / "normalized" / img.name)
        pdf_count += 1
        click.echo(f"  {pdf.name} → {len(images)} page(s)")

    click.echo(f"Ingested {pdf_count} PDFs into {inputs_dir}/")
```

- [ ] **Step 2: Implement extract command**

```python
@main.command()
@click.argument("project")
@click.option("--model", default=None, help="Ollama vision model name")
def extract(project: str, model: str | None):
    """Extract dimensions from blueprints using vision AI."""
    from arc.extract.dimension_extractor import extract_dimensions, save_extraction

    inputs_dir = PROJECTS_DIR / project / "inputs" / "normalized"
    if not inputs_dir.exists():
        click.echo(f"No normalized inputs found. Run 'arc ingest {project}' first.")
        raise SystemExit(1)

    extract_dir = PROJECTS_DIR / project / "extractions"
    extract_dir.mkdir(exist_ok=True)

    for image in sorted(inputs_dir.glob("*.png")):
        click.echo(f"Extracting: {image.name}...")
        kwargs = {"image_path": image}
        if model:
            kwargs["model"] = model
        result = extract_dimensions(**kwargs)
        dims = result.get("dimensions", [])
        high_conf = sum(1 for d in dims if d.get("confidence", 0) >= 0.7)
        save_extraction(result, extract_dir / f"{image.stem}_extraction.json")
        click.echo(f"  {len(dims)} dimensions ({high_conf} high-confidence)")

    click.echo(f"Extractions saved to {extract_dir}/")
    click.echo("Review and correct extractions before running 'arc model'.")
```

- [ ] **Step 3: Test end-to-end**

```bash
cd /Users/gclyle/GrowDirect/ARC
source .venv/bin/activate
arc ingest seacove
arc extract seacove  # requires Ollama with vision model
```

- [ ] **Step 4: Commit**

```bash
git add ARC/arc/cli.py
git commit -m "feat(arc): wire ingest + extract CLI commands — full input pipeline"
```

---

### Task 16: Final Integration — Create Seacove Spatial Model by Hand

This task creates the initial Seacove spatial model JSON manually from the
blueprint reference data. This is the "prove the generate stage works" step.

**Files:**
- Create: `ARC/scripts/create_seacove_model.py`

- [ ] **Step 1: Write a script that builds the Seacove spatial model from known dimensions**

Build a Python script that creates the Seacove Project from the dimensions
in `blueprint-dimensions-reference.md` and the hand-written Ruby scripts.
This is manual data entry — the Extract pipeline will automate this later.

Use the Wall/Room/Floor data from `25-Seacove-As-Built.rb` (lines 38-109)
as the source of truth for wall positions.

- [ ] **Step 2: Save the model**

```bash
python3 scripts/create_seacove_model.py
# Outputs: projects/seacove/model/spatial_model.json
```

- [ ] **Step 3: Validate the model**

```bash
arc validate seacove
```

Expected: "Model is valid"

- [ ] **Step 4: Generate Ruby scripts**

```bash
arc generate seacove
```

Expected: .rb files in `projects/seacove/output/`

- [ ] **Step 5: Compare generated vs hand-written**

Manually diff `projects/seacove/output/04_walls.rb` against
`25-Seacove-As-Built.rb`. The generated version should have:
- Same wall positions and dimensions
- Proper wall thickness (not make_box approximations)
- Boolean opening cuts where the original had none
- Tag folders instead of flat tags

- [ ] **Step 6: Commit**

```bash
git add ARC/scripts/ ARC/projects/seacove/model/
git commit -m "feat(arc): Seacove spatial model (manual) + generated Ruby scripts — v0 pipeline complete"
```

---

## Summary

| Chunk | Tasks | What You Get |
|-------|-------|-------------|
| 1: Scaffold + Model | 1-5 | Project structure, spatial model with validation, JSON serialization, CLI skeleton |
| 2: Generate | 6-10 | Jinja2 templates for all Ruby scripts, generator that produces runnable .rb files |
| 3: Ingest + Extract | 11-16 | Blueprint PDF reading, Ollama vision extraction, Seacove ground truth, full v0 pipeline |

After all 16 tasks: `arc ingest seacove && arc extract seacove && arc model seacove && arc validate seacove && arc generate seacove` produces SketchUp Ruby scripts from Seacove blueprints.
