#!/usr/bin/env python3
"""Canary Protocol — manifest reconciler.

Reads three artifacts and reports drift between them:
  - manifest.yaml      (the spec — what we say is built)
  - routes-seen.json   (the live router — what is actually mounted)
  - openapi.yaml       (the contract — what partners can call)

For each (METHOD, PATH) tuple, classifies into one of these buckets:

  matched              all three sources agree (the goal)
  manifest+routes      mounted + spec'd in manifest, but not in OpenAPI
                       → regenerate openapi from manifest (Phase 2 closes this)
  manifest+openapi     in spec layers but not actually mounted
                       → "proposed" status; build later or remove
  routes+openapi       mounted + in OpenAPI but missing from manifest
                       → backfill manifest entry (Phase 2)
  manifest-only        in manifest but neither mounted nor in OpenAPI
                       → "proposed" — informational
  routes-only          mounted but completely undeclared
                       → unaccounted; needs manifest + spec backfill (Phase 2)
  openapi-only         in OpenAPI only — orphan spec; remove or build it

Phase 1 Gate (per design spec): unaccounted ≤ 10. "Unaccounted" =
routes-only — endpoints on the live router that nothing else describes.

Outputs a plain-text drift report to <output>/drift-report.txt by default.

Phase-1 / GRO-839 sub-task T1.3 of the sysadmin module epic (GRO-836).
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_MANIFEST = REPO_ROOT / "services/canary-protocol/manifest/manifest.yaml"
DEFAULT_ROUTES_SEEN = REPO_ROOT / "services/canary-protocol/manifest/build/routes-seen.json"
DEFAULT_OPENAPI = REPO_ROOT / "services/canary-protocol/openapi/openapi.yaml"
DEFAULT_OUTPUT = REPO_ROOT / "services/canary-protocol/manifest/build/drift-report.txt"

GATE_UNACCOUNTED_MAX = 10


@dataclass
class EndpointKey:
    method: str
    path: str

    def __hash__(self) -> int:
        return hash((self.method.upper(), self.path))

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, EndpointKey)
            and self.method.upper() == other.method.upper()
            and self.path == other.path
        )

    def __str__(self) -> str:
        return f"{self.method.upper():<7} {self.path}"


@dataclass
class Categorized:
    matched: list[tuple[EndpointKey, str]] = field(default_factory=list)
    manifest_routes_no_openapi: list[tuple[EndpointKey, str]] = field(default_factory=list)
    manifest_openapi_no_routes: list[tuple[EndpointKey, str]] = field(default_factory=list)
    routes_openapi_no_manifest: list[EndpointKey] = field(default_factory=list)
    manifest_only: list[tuple[EndpointKey, str]] = field(default_factory=list)
    routes_only: list[EndpointKey] = field(default_factory=list)
    openapi_only: list[EndpointKey] = field(default_factory=list)


def load_manifest(path: Path) -> tuple[dict[EndpointKey, dict], dict]:
    """Returns (endpoint_map, raw_manifest). endpoint_map keys to a
    {service, status} dict for each endpoint declared in the manifest."""
    if not path.exists():
        return {}, {}
    with path.open() as f:
        doc = yaml.safe_load(f) or {}
    endpoints: dict[EndpointKey, dict] = {}
    for svc in doc.get("services") or []:
        svc_name = svc.get("name", "?")
        for ep in svc.get("endpoints") or []:
            key = EndpointKey(method=ep.get("method", ""), path=ep.get("path", ""))
            endpoints[key] = {"service": svc_name, "status": ep.get("status", "")}
    return endpoints, doc


def load_routes_seen(path: Path) -> set[EndpointKey]:
    if not path.exists():
        return set()
    with path.open() as f:
        doc = json.load(f)
    out: set[EndpointKey] = set()
    for r in doc.get("routes") or []:
        out.add(EndpointKey(method=r.get("method", ""), path=r.get("path", "")))
    return out


def load_openapi(path: Path) -> set[EndpointKey]:
    if not path.exists():
        return set()
    with path.open() as f:
        doc = yaml.safe_load(f) or {}
    out: set[EndpointKey] = set()
    paths = doc.get("paths") or {}
    for path_str, ops in paths.items():
        if not isinstance(ops, dict):
            continue
        for verb in ("get", "post", "put", "patch", "delete", "head", "options"):
            if verb in ops:
                out.add(EndpointKey(method=verb.upper(), path=path_str))
    return out


def categorize(
    manifest: dict[EndpointKey, dict],
    routes_seen: set[EndpointKey],
    openapi: set[EndpointKey],
) -> Categorized:
    cat = Categorized()
    manifest_keys = set(manifest.keys())
    all_keys = manifest_keys | routes_seen | openapi
    for k in all_keys:
        in_m = k in manifest_keys
        in_r = k in routes_seen
        in_o = k in openapi
        m_status = manifest.get(k, {}).get("status", "") if in_m else ""
        m_service = manifest.get(k, {}).get("service", "") if in_m else ""
        if in_m and in_r and in_o:
            cat.matched.append((k, m_service))
        elif in_m and in_r and not in_o:
            cat.manifest_routes_no_openapi.append((k, m_service))
        elif in_m and not in_r and in_o:
            cat.manifest_openapi_no_routes.append((k, m_service))
        elif not in_m and in_r and in_o:
            cat.routes_openapi_no_manifest.append(k)
        elif in_m and not in_r and not in_o:
            cat.manifest_only.append((k, f"{m_service} [{m_status}]"))
        elif not in_m and in_r and not in_o:
            cat.routes_only.append(k)
        elif not in_m and not in_r and in_o:
            cat.openapi_only.append(k)
    return cat


def render_report(
    cat: Categorized,
    manifest: dict[EndpointKey, dict],
    routes_seen: set[EndpointKey],
    openapi: set[EndpointKey],
    sources: dict[str, Path],
) -> str:
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    unaccounted = len(cat.routes_only)
    gate_status = "PASS" if unaccounted <= GATE_UNACCOUNTED_MAX else "FAIL"
    lines: list[str] = []
    lines.append(f"# Drift Report — {now}")
    lines.append("")
    lines.append("Sources")
    for label, path in sources.items():
        existed = path.exists()
        size = path.stat().st_size if existed else 0
        flag = "" if existed else " [MISSING — defaulting to empty]"
        try:
            rel = str(path.relative_to(REPO_ROOT))
        except ValueError:
            rel = str(path)
        lines.append(f"  {label:<14} {rel} ({size:,} bytes){flag}")
    lines.append("")
    lines.append("Counts")
    lines.append(f"  manifest endpoints:   {len(manifest)}")
    lines.append(f"  mounted endpoints:    {len(routes_seen)}")
    lines.append(f"  openapi endpoints:    {len(openapi)}")
    lines.append("")
    lines.append("Categories")
    lines.append(f"  matched:                       {len(cat.matched)}")
    lines.append(f"  manifest+routes (no openapi):  {len(cat.manifest_routes_no_openapi)}")
    lines.append(f"  manifest+openapi (no routes):  {len(cat.manifest_openapi_no_routes)}")
    lines.append(f"  routes+openapi (no manifest):  {len(cat.routes_openapi_no_manifest)}")
    lines.append(f"  manifest-only:                 {len(cat.manifest_only)}")
    lines.append(f"  routes-only (UNACCOUNTED):     {len(cat.routes_only)}")
    lines.append(f"  openapi-only:                  {len(cat.openapi_only)}")
    lines.append("")
    lines.append(f"Phase 1 Gate: unaccounted ≤ {GATE_UNACCOUNTED_MAX}  ·  current: {unaccounted}  ·  {gate_status}")
    lines.append("")

    def _section(title: str, rows: list, fmt) -> None:
        lines.append(f"## {title}  ({len(rows)})")
        if not rows:
            lines.append("  (none)")
            lines.append("")
            return
        for r in sorted(rows, key=lambda x: (str(x[0]) if isinstance(x, tuple) else str(x))):
            lines.append(f"  {fmt(r)}")
        lines.append("")

    _section("matched", cat.matched, lambda r: f"{r[0]}  — {r[1]}")
    _section(
        "manifest+routes (regenerate openapi from manifest)",
        cat.manifest_routes_no_openapi,
        lambda r: f"{r[0]}  — {r[1]}",
    )
    _section(
        "manifest+openapi (proposed — not yet mounted)",
        cat.manifest_openapi_no_routes,
        lambda r: f"{r[0]}  — {r[1]}",
    )
    _section(
        "routes+openapi (BACKFILL manifest)",
        cat.routes_openapi_no_manifest,
        lambda k: str(k),
    )
    _section("manifest-only (informational)", cat.manifest_only, lambda r: f"{r[0]}  — {r[1]}")
    _section("routes-only — UNACCOUNTED (Phase 2 backfill)", cat.routes_only, lambda k: str(k))
    _section("openapi-only (orphan spec)", cat.openapi_only, lambda k: str(k))

    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Reconcile manifest.yaml × routes-seen.json × openapi.yaml → drift-report.txt"
    )
    p.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    p.add_argument("--routes-seen", default=str(DEFAULT_ROUTES_SEEN))
    p.add_argument("--openapi", default=str(DEFAULT_OPENAPI))
    p.add_argument("--output", default=str(DEFAULT_OUTPUT))
    p.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if Phase 1 Gate fails (unaccounted > 10)",
    )
    args = p.parse_args(argv)

    manifest_path = Path(args.manifest)
    routes_path = Path(args.routes_seen)
    openapi_path = Path(args.openapi)
    output_path = Path(args.output)

    manifest, _ = load_manifest(manifest_path)
    routes_seen = load_routes_seen(routes_path)
    openapi = load_openapi(openapi_path)

    cat = categorize(manifest, routes_seen, openapi)

    report = render_report(
        cat,
        manifest,
        routes_seen,
        openapi,
        {
            "manifest:": manifest_path,
            "routes-seen:": routes_path,
            "openapi:": openapi_path,
        },
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report)

    print(f"wrote {output_path}", file=sys.stderr)
    print(f"  matched:        {len(cat.matched)}", file=sys.stderr)
    print(f"  unaccounted:    {len(cat.routes_only)}  (Phase 1 Gate ≤ {GATE_UNACCOUNTED_MAX})", file=sys.stderr)
    print(f"  manifest-only:  {len(cat.manifest_only)}", file=sys.stderr)
    print(f"  openapi-only:   {len(cat.openapi_only)}", file=sys.stderr)

    if args.strict and len(cat.routes_only) > GATE_UNACCOUNTED_MAX:
        print(
            f"FAIL: {len(cat.routes_only)} unaccounted endpoints exceeds gate ({GATE_UNACCOUNTED_MAX})",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
