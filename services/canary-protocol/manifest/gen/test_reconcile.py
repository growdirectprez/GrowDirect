"""Tests for reconcile.py — covers each categorization bucket."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from reconcile import (
    EndpointKey,
    categorize,
    load_manifest,
    load_openapi,
    load_routes_seen,
    render_report,
)


def _write_manifest(p: Path, services: list[dict]) -> Path:
    p.write_text(yaml.safe_dump({"services": services}))
    return p


def _write_routes(p: Path, routes: list[dict]) -> Path:
    p.write_text(json.dumps({"routes": routes, "count": len(routes)}))
    return p


def _write_openapi(p: Path, paths: dict) -> Path:
    p.write_text(yaml.safe_dump({"paths": paths}))
    return p


def test_load_manifest_extracts_endpoints(tmp_path: Path):
    p = _write_manifest(
        tmp_path / "m.yaml",
        [
            {
                "name": "catalog",
                "endpoints": [
                    {"method": "GET", "path": "/devops/catalog", "status": "proposed"}
                ],
            }
        ],
    )
    eps, _ = load_manifest(p)
    key = EndpointKey("GET", "/devops/catalog")
    assert key in eps
    assert eps[key]["service"] == "catalog"
    assert eps[key]["status"] == "proposed"


def test_load_routes_seen_returns_set(tmp_path: Path):
    p = _write_routes(
        tmp_path / "r.json",
        [{"method": "GET", "path": "/health"}, {"method": "POST", "path": "/v1/foo"}],
    )
    routes = load_routes_seen(p)
    assert EndpointKey("GET", "/health") in routes
    assert EndpointKey("POST", "/v1/foo") in routes
    assert len(routes) == 2


def test_load_openapi_walks_paths(tmp_path: Path):
    p = _write_openapi(
        tmp_path / "o.yaml",
        {"/v1/foo": {"get": {"summary": "x"}, "post": {"summary": "y"}}},
    )
    eps = load_openapi(p)
    assert EndpointKey("GET", "/v1/foo") in eps
    assert EndpointKey("POST", "/v1/foo") in eps


def test_load_missing_files_returns_empty(tmp_path: Path):
    assert load_manifest(tmp_path / "missing.yaml") == ({}, {})
    assert load_routes_seen(tmp_path / "missing.json") == set()
    assert load_openapi(tmp_path / "missing.yaml") == set()


def test_categorize_matched(tmp_path: Path):
    k = EndpointKey("GET", "/v1/x")
    cat = categorize(
        {k: {"service": "x", "status": "mounted"}},
        {k},
        {k},
    )
    assert len(cat.matched) == 1


def test_categorize_routes_only_is_unaccounted():
    k = EndpointKey("GET", "/v1/orphan")
    cat = categorize({}, {k}, set())
    assert k in cat.routes_only
    assert len(cat.routes_only) == 1


def test_categorize_manifest_only():
    k = EndpointKey("GET", "/v1/proposed")
    cat = categorize(
        {k: {"service": "x", "status": "proposed"}},
        set(),
        set(),
    )
    assert len(cat.manifest_only) == 1


def test_categorize_openapi_only():
    k = EndpointKey("GET", "/v1/orphan-spec")
    cat = categorize({}, set(), {k})
    assert k in cat.openapi_only


def test_categorize_routes_openapi_no_manifest():
    k = EndpointKey("GET", "/v1/built")
    cat = categorize({}, {k}, {k})
    assert k in cat.routes_openapi_no_manifest


def test_endpointkey_method_case_insensitive():
    a = EndpointKey("get", "/v1/x")
    b = EndpointKey("GET", "/v1/x")
    assert a == b
    assert hash(a) == hash(b)


def test_render_report_passes_gate_when_unaccounted_low():
    cat = categorize({}, set(), set())
    sources = {"manifest:": Path("m.yaml"), "routes-seen:": Path("r.json"), "openapi:": Path("o.yaml")}
    report = render_report(cat, {}, set(), set(), sources)
    assert "Phase 1 Gate" in report
    assert "PASS" in report
    assert "## matched  (0)" in report
    assert "## routes-only — UNACCOUNTED (Phase 2 backfill)  (0)" in report


def test_render_report_fails_gate_when_unaccounted_high():
    routes = {EndpointKey("GET", f"/v1/x/{i}") for i in range(15)}
    cat = categorize({}, routes, set())
    sources = {"manifest:": Path("m.yaml"), "routes-seen:": Path("r.json"), "openapi:": Path("o.yaml")}
    report = render_report(cat, {}, routes, set(), sources)
    assert "FAIL" in report
    assert len(cat.routes_only) == 15
