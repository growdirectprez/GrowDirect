"""Tests for parse_manifest.py — covers each validation rule with synthetic
markdown fixtures."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from parse_manifest import (
    Cell,
    Endpoint,
    Issue,
    Service,
    parse_portal,
    validate,
    emit_manifest,
    build_catalog,
    emit_catalog,
)


def _portal(text: str) -> str:
    """Strip leading whitespace from a fixture and return as portal markdown."""
    return textwrap.dedent(text).lstrip()


def _has(issues: list[Issue], rule: str) -> bool:
    return any(i.rule == rule for i in issues)


def _errors(issues: list[Issue]) -> list[Issue]:
    return [i for i in issues if i.severity == "error"]


# ---------------------------------------------------------------------------
# Parse — happy path
# ---------------------------------------------------------------------------


def test_parses_well_formed_service():
    md = _portal(
        """
        ## catalog · :9100 · cross-tenant infra · P0

        Owner: ALX  ·  Card: Brain/wiki/cards/canary-go-portal.md  ·  Cells: [B × reference] [C × reference]
        cross-tenant  ·  Python prior art: none

        | Endpoint | Method | Tier | Axis | Auth | Status | Notes |
        |----------|--------|------|------|------|--------|-------|
        | /devops/catalog | GET | reference | B | apikey | mounted | grid heat-map |
        | /v1/catalog/services | GET | reference | B | apikey | mounted | service list |
        """
    )
    issues: list[Issue] = []
    services = parse_portal(md, issues)
    assert len(services) == 1
    svc = services[0]
    assert svc.name == "catalog"
    assert svc.port == 9100
    assert svc.priority == "P0"
    assert svc.scope == "cross-tenant"
    assert svc.python_prior_art is None
    assert len(svc.cells) == 2
    assert svc.cells[0].axis == "B"
    assert svc.cells[0].tier == "reference"
    assert len(svc.endpoints) == 2
    assert svc.endpoints[0].method == "GET"
    assert svc.endpoints[0].path == "/devops/catalog"
    assert svc.endpoints[0].tier == "reference"


def test_parses_multiple_services():
    md = _portal(
        """
        ## catalog · :9100 · cross-tenant infra · P0

        Owner: ALX  ·  Card: Brain/wiki/cards/canary-go-portal.md  ·  Cells: [B × reference]
        cross-tenant  ·  Python prior art: none

        | Endpoint | Method | Tier | Axis | Auth | Status | Notes |
        |----------|--------|------|------|------|--------|-------|
        | /devops/catalog | GET | reference | B | apikey | mounted | grid heat-map |

        ## manifest · :9101 · cross-tenant infra · P0

        Owner: ALX  ·  Card: Brain/wiki/cards/canary-go-portal.md  ·  Cells: [B × reference]
        cross-tenant  ·  Python prior art: none

        | Endpoint | Method | Tier | Axis | Auth | Status | Notes |
        |----------|--------|------|------|------|--------|-------|
        | /devops/manifest | GET | reference | B | apikey | mounted | manifest editor |
        """
    )
    issues: list[Issue] = []
    services = parse_portal(md, issues)
    assert len(services) == 2
    assert {s.name for s in services} == {"catalog", "manifest"}


def test_ignores_non_service_h2():
    md = _portal(
        """
        ## Architecture SDDs

        Some narrative content. Should not be parsed as a service.

        ## catalog · :9100 · cross-tenant infra · P0

        Owner: ALX  ·  Card: Brain/wiki/cards/canary-go-portal.md  ·  Cells: [B × reference]
        cross-tenant  ·  Python prior art: none
        """
    )
    issues: list[Issue] = []
    services = parse_portal(md, issues)
    assert len(services) == 1
    assert services[0].name == "catalog"


def test_python_prior_art_recorded_when_present():
    md = _portal(
        """
        ## etl · :9105 · cross-tenant infra · P0

        Owner: ALX  ·  Card: Brain/wiki/cards/canary-go-portal.md  ·  Cells: [B × daily-batch]
        cross-tenant  ·  Python prior art: Canary/canary/services/metrics_etl.py

        | Endpoint | Method | Tier | Axis | Auth | Status | Notes |
        |----------|--------|------|------|------|--------|-------|
        | /devops/etl | GET | daily-batch | B | apikey | mounted | etl runner |
        """
    )
    issues: list[Issue] = []
    services = parse_portal(md, issues)
    assert services[0].python_prior_art == "Canary/canary/services/metrics_etl.py"


# ---------------------------------------------------------------------------
# Validation — hard fails (warn-by-default in Phase 1)
# ---------------------------------------------------------------------------


def test_missing_port_emits_error(tmp_path: Path):
    svc = Service(
        name="x",
        port=None,
        owner="ALX",
        card="dummy.md",
        priority="P2",
        scope="cross-tenant",
        category="cross-tenant infra",
        python_prior_art=None,
    )
    issues = validate([svc], tmp_path)
    assert _has(issues, "missing-port")


def test_missing_owner_emits_error(tmp_path: Path):
    svc = Service(
        name="x",
        port=9100,
        owner="",
        card="dummy.md",
        priority="P2",
        scope="cross-tenant",
        category="cross-tenant infra",
        python_prior_art=None,
    )
    issues = validate([svc], tmp_path)
    assert _has(issues, "missing-owner")


def test_missing_card_emits_error(tmp_path: Path):
    svc = Service(
        name="x",
        port=9100,
        owner="ALX",
        card="",
        priority="P2",
        scope="cross-tenant",
        category="cross-tenant infra",
        python_prior_art=None,
    )
    issues = validate([svc], tmp_path)
    assert _has(issues, "missing-card")


def test_missing_card_file_emits_error(tmp_path: Path):
    svc = Service(
        name="x",
        port=9100,
        owner="ALX",
        card="does/not/exist.md",
        priority="P2",
        scope="cross-tenant",
        category="cross-tenant infra",
        python_prior_art=None,
    )
    issues = validate([svc], tmp_path)
    assert _has(issues, "missing-card-file")


def test_existing_card_file_passes(tmp_path: Path):
    card = tmp_path / "card.md"
    card.write_text("# stub")
    svc = Service(
        name="x",
        port=9100,
        owner="ALX",
        card="card.md",
        priority="P2",
        scope="cross-tenant",
        category="cross-tenant infra",
        python_prior_art=None,
    )
    issues = validate([svc], tmp_path)
    assert not _has(issues, "missing-card-file")


def test_cells_without_endpoints_emits_error(tmp_path: Path):
    svc = Service(
        name="x",
        port=9100,
        owner="ALX",
        card="card.md",
        priority="P2",
        scope="cross-tenant",
        category="cross-tenant infra",
        python_prior_art=None,
        cells=[Cell(axis="B", tier="reference")],
        endpoints=[],
    )
    (tmp_path / "card.md").write_text("# stub")
    issues = validate([svc], tmp_path)
    assert _has(issues, "cells-without-endpoints")


def test_invalid_tier_emits_error(tmp_path: Path):
    (tmp_path / "card.md").write_text("# stub")
    svc = Service(
        name="x",
        port=9100,
        owner="ALX",
        card="card.md",
        priority="P2",
        scope="cross-tenant",
        category="cross-tenant infra",
        python_prior_art=None,
        endpoints=[
            Endpoint(
                method="GET",
                path="/x",
                tier="bogus",
                axis="B",
                auth="apikey",
                status="mounted",
            )
        ],
    )
    issues = validate([svc], tmp_path)
    assert _has(issues, "missing-or-invalid-tier")


def test_invalid_axis_emits_error(tmp_path: Path):
    (tmp_path / "card.md").write_text("# stub")
    svc = Service(
        name="x",
        port=9100,
        owner="ALX",
        card="card.md",
        priority="P2",
        scope="cross-tenant",
        category="cross-tenant infra",
        python_prior_art=None,
        endpoints=[
            Endpoint(
                method="GET",
                path="/x",
                tier="reference",
                axis="Z",
                auth="apikey",
                status="mounted",
            )
        ],
    )
    issues = validate([svc], tmp_path)
    assert _has(issues, "missing-or-invalid-axis")


def test_port_collision_emits_error(tmp_path: Path):
    (tmp_path / "card.md").write_text("# stub")
    base = dict(
        owner="ALX",
        card="card.md",
        priority="P2",
        scope="cross-tenant",
        category="cross-tenant infra",
        python_prior_art=None,
    )
    a = Service(name="a", port=9100, **base)
    b = Service(name="b", port=9100, **base)
    issues = validate([a, b], tmp_path)
    assert _has(issues, "port-collision")


def test_path_method_collision_emits_error(tmp_path: Path):
    (tmp_path / "card.md").write_text("# stub")
    base = dict(
        owner="ALX",
        card="card.md",
        priority="P2",
        scope="cross-tenant",
        category="cross-tenant infra",
        python_prior_art=None,
    )
    ep = Endpoint(
        method="GET",
        path="/v1/shared",
        tier="reference",
        axis="B",
        auth="apikey",
        status="mounted",
    )
    a = Service(name="a", port=9100, endpoints=[ep], **base)
    b = Service(name="b", port=9101, endpoints=[ep], **base)
    issues = validate([a, b], tmp_path)
    assert _has(issues, "path-method-collision")


# ---------------------------------------------------------------------------
# Validation — warnings
# ---------------------------------------------------------------------------


def test_tier_mix_emits_warning(tmp_path: Path):
    (tmp_path / "card.md").write_text("# stub")
    svc = Service(
        name="x",
        port=9100,
        owner="ALX",
        card="card.md",
        priority="P2",
        scope="cross-tenant",
        category="cross-tenant infra",
        python_prior_art=None,
        endpoints=[
            Endpoint("GET", "/v1/a", "stream", "B", "apikey", "mounted"),
            Endpoint("GET", "/v1/b", "change-feed", "B", "apikey", "mounted"),
            Endpoint("GET", "/v1/c", "reference", "B", "apikey", "mounted"),
        ],
    )
    issues = validate([svc], tmp_path)
    tier_mix = [i for i in issues if i.rule == "tier-mix"]
    assert len(tier_mix) == 1
    assert tier_mix[0].severity == "warning"


def test_cell_concentration_emits_warning(tmp_path: Path):
    (tmp_path / "card.md").write_text("# stub")
    eps = [
        Endpoint(
            method="GET",
            path=f"/v1/x/{i}",
            tier="reference",
            axis="B",
            auth="apikey",
            status="mounted",
        )
        for i in range(31)
    ]
    svc = Service(
        name="x",
        port=9100,
        owner="ALX",
        card="card.md",
        priority="P2",
        scope="cross-tenant",
        category="cross-tenant infra",
        python_prior_art=None,
        endpoints=eps,
    )
    issues = validate([svc], tmp_path)
    cc = [i for i in issues if i.rule == "cell-concentration"]
    assert len(cc) == 1
    assert cc[0].severity == "warning"


# ---------------------------------------------------------------------------
# Emit
# ---------------------------------------------------------------------------


def test_emit_manifest_writes_yaml(tmp_path: Path):
    out = tmp_path / "manifest.yaml"
    (tmp_path / "card.md").write_text("# stub")
    svc = Service(
        name="catalog",
        port=9100,
        owner="ALX",
        card="card.md",
        priority="P0",
        scope="cross-tenant",
        category="cross-tenant infra",
        python_prior_art=None,
        cells=[Cell(axis="B", tier="reference")],
        endpoints=[
            Endpoint(
                method="GET",
                path="/devops/catalog",
                tier="reference",
                axis="B",
                auth="apikey",
                status="mounted",
            )
        ],
    )
    payload = emit_manifest([svc], [tmp_path / "card.md"], out)
    assert out.exists()
    assert payload["version"] == "1.0"
    assert len(payload["services"]) == 1
    assert payload["services"][0]["name"] == "catalog"
    assert payload["services"][0]["cells"] == ["B×reference"]
    assert payload["tiers"][0] == "stream"


def _sample_service() -> Service:
    return Service(
        name="catalog",
        port=9100,
        owner="ALX",
        card="card.md",
        priority="P0",
        scope="cross-tenant",
        category="cross-tenant infra",
        python_prior_art=None,
        cells=[Cell(axis="B", tier="reference")],
        endpoints=[
            Endpoint(
                method="GET",
                path="/devops/catalog",
                tier="reference",
                axis="B",
                auth="apikey",
                status="proposed",
            ),
            Endpoint(
                method="GET",
                path="/v1/catalog/services",
                tier="reference",
                axis="B",
                auth="apikey",
                status="proposed",
            ),
        ],
    )


def test_build_catalog_includes_full_3x5_grid():
    catalog = build_catalog([_sample_service()], "2026-05-07T00:00:00Z")
    assert len(catalog["cells"]) == 15  # 3 axes × 5 tiers
    assert len(catalog["axes"]) == 3
    assert len(catalog["tiers"]) == 5
    cells_by_key = {(c["axis"], c["tier"]): c for c in catalog["cells"]}
    # The sample service has 2 endpoints in B × reference.
    target = cells_by_key[("B", "reference")]
    assert target["endpoint_count"] == 2
    assert "catalog" in target["services"]
    # Other cells are zero.
    other = cells_by_key[("A", "stream")]
    assert other["endpoint_count"] == 0
    assert other["services"] == []


def test_build_catalog_summarizes_each_service():
    catalog = build_catalog([_sample_service()], "2026-05-07T00:00:00Z")
    assert len(catalog["services"]) == 1
    s = catalog["services"][0]
    assert s["name"] == "catalog"
    assert s["port"] == 9100
    assert s["priority"] == "P0"
    assert s["endpoint_count"] == 2
    assert s["cells"] == ["B×reference"]


def test_build_catalog_totals():
    svcs = [_sample_service()]
    catalog = build_catalog(svcs, "2026-05-07T00:00:00Z")
    assert catalog["totals"]["service_count"] == 1
    assert catalog["totals"]["endpoint_count"] == 2


def test_emit_catalog_writes_valid_json(tmp_path: Path):
    import json
    out = tmp_path / "devops-catalog.json"
    catalog = build_catalog([_sample_service()], "2026-05-07T00:00:00Z")
    emit_catalog(catalog, out)
    data = json.loads(out.read_text())
    assert data["generated_at"] == "2026-05-07T00:00:00Z"
    assert data["totals"]["service_count"] == 1
    assert len(data["cells"]) == 15


def test_clean_well_formed_service_has_no_errors(tmp_path: Path):
    card = tmp_path / "card.md"
    card.write_text("# stub")
    svc = Service(
        name="catalog",
        port=9100,
        owner="ALX",
        card="card.md",
        priority="P0",
        scope="cross-tenant",
        category="cross-tenant infra",
        python_prior_art=None,
        cells=[Cell(axis="B", tier="reference")],
        endpoints=[
            Endpoint(
                method="GET",
                path="/devops/catalog",
                tier="reference",
                axis="B",
                auth="apikey",
                status="mounted",
            )
        ],
    )
    issues = validate([svc], tmp_path)
    assert _errors(issues) == [], f"unexpected errors: {_errors(issues)}"
