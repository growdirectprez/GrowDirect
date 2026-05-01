"""Tests for arc.components — registry, framing, structural."""
from __future__ import annotations

import pytest

from arc.components.base import ComponentRegistry, ComponentSpec, SnapPoint
from arc.components.framing import (
    stud_2x4, stud_2x6, stud, plate_2x4, plate_2x6, plate,
    header, blocking, cripple, ACTUAL_SIZES,
)
from arc.components.structural import (
    post, beam, rafter,
)


# ---------------------------------------------------------------------------
# ComponentRegistry
# ---------------------------------------------------------------------------

def test_registry_register_and_get():
    reg = ComponentRegistry()
    spec = ComponentSpec(
        name="test_widget",
        category="test",
        description="A test widget",
        params={},
        snap_points=[SnapPoint("base", 0, 0, 0)],
        definition_code="pass",
    )
    reg.register(spec)
    assert reg.has("test_widget")
    assert reg.get("test_widget") is spec


def test_registry_duplicate_raises():
    reg = ComponentRegistry()
    spec = ComponentSpec("dup", "test", "d", {}, [], "pass")
    reg.register(spec)
    with pytest.raises(ValueError, match="already registered"):
        reg.register(spec)


def test_registry_register_or_get_idempotent():
    reg = ComponentRegistry()
    spec = ComponentSpec("widget", "test", "d", {}, [], "pass")
    r1 = reg.register_or_get(spec)
    r2 = reg.register_or_get(spec)
    assert r1 is r2


def test_registry_get_missing_raises():
    reg = ComponentRegistry()
    with pytest.raises(KeyError, match="not registered"):
        reg.get("nonexistent")


def test_registry_list_by_category():
    reg = ComponentRegistry()
    reg.register(ComponentSpec("a", "framing", "", {}, [], "pass"))
    reg.register(ComponentSpec("b", "structural", "", {}, [], "pass"))
    reg.register(ComponentSpec("c", "framing", "", {}, [], "pass"))
    framing = reg.list_by_category("framing")
    assert len(framing) == 2
    assert all(s.category == "framing" for s in framing)


def test_registry_categories():
    reg = ComponentRegistry()
    reg.register(ComponentSpec("a", "framing", "", {}, [], "pass"))
    reg.register(ComponentSpec("b", "structural", "", {}, [], "pass"))
    assert set(reg.categories) == {"framing", "structural"}


def test_registry_all_definition_code_contains_names():
    reg = ComponentRegistry()
    reg.register(ComponentSpec("comp_a", "framing", "", {}, [], 'x = 1  # comp_a'))
    reg.register(ComponentSpec("comp_b", "framing", "", {}, [], 'x = 2  # comp_b'))
    code = reg.all_definition_code()
    assert "comp_a" in code
    assert "comp_b" in code
    assert "_arc_defs" in code


def test_registry_all_definition_code_filtered_by_category():
    reg = ComponentRegistry()
    reg.register(ComponentSpec("framing_a", "framing", "", {}, [], "pass"))
    reg.register(ComponentSpec("struct_b", "structural", "", {}, [], "pass"))
    code = reg.all_definition_code(categories=["framing"])
    assert "framing_a" in code
    assert "struct_b" not in code


# ---------------------------------------------------------------------------
# SnapPoint
# ---------------------------------------------------------------------------

def test_snappoint_offset_from():
    a = SnapPoint("top", 0, 0, 96)
    b = SnapPoint("base", 0, 0, 0)
    dx, dy, dz = a.offset_from(b)
    assert dx == 0
    assert dy == 0
    assert dz == 96


def test_componentspec_snap_lookup():
    spec = ComponentSpec(
        name="thing",
        category="test",
        description="",
        params={},
        snap_points=[
            SnapPoint("base", 0, 0, 0),
            SnapPoint("top", 0, 0, 10),
        ],
        definition_code="pass",
    )
    top = spec.snap("top")
    assert top.z == 10


def test_componentspec_snap_missing_raises():
    spec = ComponentSpec("t", "test", "", {}, [SnapPoint("base", 0, 0, 0)], "pass")
    with pytest.raises(KeyError, match="Snap point"):
        spec.snap("nonexistent")


# ---------------------------------------------------------------------------
# instance_code
# ---------------------------------------------------------------------------

def test_instance_code_no_rotation():
    spec = ComponentSpec("widget_a", "test", "", {}, [], "pass")
    code = spec.instance_code(tx=12.0, ty=24.0, tz=0.0)
    assert '"widget_a"' in code
    assert "12.0000" in code
    assert "SUTransformation" in code
    assert "add_instance" in code


def test_instance_code_with_rotation():
    spec = ComponentSpec("widget_b", "test", "", {}, [], "pass")
    code = spec.instance_code(tx=0.0, ty=0.0, tz=0.0, rotation_z_deg=90.0)
    assert "math.cos" in code or "_arc_cos" in code
    assert "90.0" in code


def test_instance_code_with_name():
    spec = ComponentSpec("widget_c", "test", "", {}, [], "pass")
    code = spec.instance_code(tx=0, ty=0, tz=0, instance_name="my_inst")
    assert 'set_name("my_inst")' in code


# ---------------------------------------------------------------------------
# Framing components
# ---------------------------------------------------------------------------

class TestStud:
    def test_stud_2x6_registered(self):
        reg = ComponentRegistry()
        s = stud_2x6(96.0, reg)
        assert reg.has(s.name)
        assert s.category == "framing"
        assert s.params["width_in"] == 1.5
        assert s.params["depth_in"] == 5.5
        assert s.params["height_in"] == 96.0

    def test_stud_2x4_registered(self):
        reg = ComponentRegistry()
        s = stud_2x4(92.625, reg)
        assert s.params["depth_in"] == 3.5

    def test_stud_idempotent(self):
        reg = ComponentRegistry()
        s1 = stud_2x6(96.0, reg)
        s2 = stud_2x6(96.0, reg)
        assert s1 is s2
        assert len(reg.names) == 1

    def test_stud_has_base_and_top_snaps(self):
        reg = ComponentRegistry()
        s = stud_2x6(96.0, reg)
        base = s.snap("base")
        top = s.snap("top")
        assert base.z == 0.0
        assert top.z == 96.0

    def test_stud_definition_code_no_imports(self):
        reg = ComponentRegistry()
        s = stud_2x6(96.0, reg)
        assert "import" not in s.definition_code

    def test_stud_definition_code_has_component_name(self):
        reg = ComponentRegistry()
        s = stud_2x6(96.0, reg)
        assert s.name in s.definition_code

    def test_stud_definition_code_has_correct_dimensions(self):
        reg = ComponentRegistry()
        s = stud_2x6(96.0, reg)
        assert "5.5" in s.definition_code   # depth
        assert "1.5" in s.definition_code   # width

    def test_stud_unknown_nominal_raises(self):
        reg = ComponentRegistry()
        with pytest.raises(ValueError, match="Unknown nominal"):
            stud("2x3", 96.0, reg)


class TestPlate:
    def test_plate_2x6_registered(self):
        reg = ComponentRegistry()
        p = plate_2x6(240.0, reg)
        assert reg.has(p.name)
        assert p.category == "framing"
        assert p.params["length_in"] == 240.0

    def test_plate_has_end_snaps(self):
        reg = ComponentRegistry()
        p = plate_2x6(240.0, reg)
        left = p.snap("left_end")
        right = p.snap("right_end")
        assert left.x == 0.0
        assert right.x == 240.0

    def test_plate_definition_code_no_imports(self):
        reg = ComponentRegistry()
        p = plate_2x4(120.0, reg)
        assert "import" not in p.definition_code


class TestHeader:
    def test_header_registered(self):
        reg = ComponentRegistry()
        h = header(span_in=36.0, header_height_in=9.25, registry=reg)
        assert reg.has(h.name)
        assert h.params["span_in"] == 36.0

    def test_header_has_end_snaps(self):
        reg = ComponentRegistry()
        h = header(span_in=36.0, header_height_in=9.25, registry=reg)
        assert h.snap("left_end").x == 0.0
        assert h.snap("right_end").x == 36.0

    def test_header_requires_registry():
        with pytest.raises(ValueError, match="registry is required"):
            header(36.0, 9.25, registry=None)

    def test_header_requires_registry(self):
        with pytest.raises(ValueError, match="registry is required"):
            header(36.0, 9.25, registry=None)


class TestBlocking:
    def test_blocking_registered(self):
        reg = ComponentRegistry()
        b = blocking("2x6", 13.0, reg)
        assert reg.has(b.name)

    def test_blocking_different_lengths_different_names(self):
        reg = ComponentRegistry()
        b1 = blocking("2x6", 13.0, reg)
        b2 = blocking("2x6", 14.5, reg)
        assert b1.name != b2.name


# ---------------------------------------------------------------------------
# Structural components
# ---------------------------------------------------------------------------

class TestPost:
    def test_post_4x4_registered(self):
        reg = ComponentRegistry()
        p = post(size_in=3.5, height_in=96.0, registry=reg, nominal="4x4")
        assert reg.has(p.name)
        assert p.category == "structural"
        assert p.params["size_in"] == 3.5
        assert p.params["height_in"] == 96.0

    def test_post_has_base_top_snaps(self):
        reg = ComponentRegistry()
        p = post(3.5, 96.0, reg)
        assert p.snap("base").z == 0.0
        assert p.snap("top").z == 96.0
        assert p.snap("beam_seat").z == 96.0

    def test_post_definition_code_no_imports(self):
        reg = ComponentRegistry()
        p = post(3.5, 96.0, reg)
        assert "import" not in p.definition_code

    def test_post_definition_code_correct_size(self):
        reg = ComponentRegistry()
        p = post(3.5, 96.0, reg)
        assert "3.5" in p.definition_code
        assert "96" in p.definition_code

    def test_post_idempotent(self):
        reg = ComponentRegistry()
        p1 = post(3.5, 96.0, reg)
        p2 = post(3.5, 96.0, reg)
        assert p1 is p2


class TestBeam:
    def test_beam_registered(self):
        reg = ComponentRegistry()
        b = beam(width_in=3.5, depth_in=9.25, span_in=144.0, registry=reg)
        assert reg.has(b.name)
        assert b.category == "structural"

    def test_beam_has_end_and_top_snaps(self):
        reg = ComponentRegistry()
        b = beam(3.5, 9.25, 144.0, reg)
        assert b.snap("left_end").x == 0.0
        assert b.snap("right_end").x == 144.0
        assert b.snap("top_left").z == 9.25
        assert b.snap("base_center").z == 0.0

    def test_beam_definition_code_no_imports(self):
        reg = ComponentRegistry()
        b = beam(3.5, 9.25, 144.0, reg)
        assert "import" not in b.definition_code

    def test_different_spans_different_names(self):
        reg = ComponentRegistry()
        b1 = beam(3.5, 9.25, 100.0, reg)
        b2 = beam(3.5, 9.25, 200.0, reg)
        assert b1.name != b2.name


class TestRafter:
    def test_rafter_2x6_registered(self):
        reg = ComponentRegistry()
        r = rafter("2x6", 120.0, reg)
        assert reg.has(r.name)
        assert r.category == "structural"
        assert r.params["depth_in"] == 5.5

    def test_rafter_2x8(self):
        reg = ComponentRegistry()
        r = rafter("2x8", 144.0, reg)
        assert r.params["depth_in"] == 7.25

    def test_rafter_bad_nominal_raises(self):
        reg = ComponentRegistry()
        with pytest.raises(ValueError, match="Unknown rafter"):
            rafter("2x3", 100.0, reg)
