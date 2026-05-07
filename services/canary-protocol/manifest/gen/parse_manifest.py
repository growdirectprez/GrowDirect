#!/usr/bin/env python3
"""Canary Protocol — manifest parser.

Reads the service-inventory sections of `Brain/wiki/canary-go-portal.md`
plus the SDD references and emits `services/canary-protocol/manifest/manifest.yaml`.

The portal markdown is the human editing surface. The YAML is the machine
intermediate that downstream artifacts (OpenAPI, devops catalog, Brain
capability cards, CRB endpoint library, gateway tier middleware) read.

Schema reference: docs/superpowers/specs/2026-05-07-sysadmin-module-design.md
§"manifest.yaml structure" + §"Validation rules".

Run:
    python3 services/canary-protocol/manifest/gen/parse_manifest.py
    python3 services/canary-protocol/manifest/gen/parse_manifest.py --strict

Phase-1 posture: validation rules are warn-by-default; --strict opts in to
exit-1 on hard fails for ahead-of-time testing. Phase 4 wires hard fails
into the build step.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_PORTAL = REPO_ROOT / "Brain/wiki/canary-go-portal.md"
DEFAULT_MICROSVC = REPO_ROOT / "docs/sdds/go-handoff/microservice-architecture.md"
DEFAULT_CANONICAL = REPO_ROOT / "docs/sdds/go-handoff/canonical-data-model.md"
DEFAULT_OUTPUT = REPO_ROOT / "services/canary-protocol/manifest/manifest.yaml"
DEFAULT_CATALOG = REPO_ROOT / "services/canary-protocol/manifest/devops-catalog.json"

VALID_TIERS = ("stream", "change-feed", "daily-batch", "bulk-window", "reference")
VALID_AXES = ("A", "B", "C")
VALID_PRIORITIES = ("P0", "P1", "P2")
VALID_SCOPES = ("cross-tenant", "tenant-scoped", "both")

MANIFEST_VERSION = "1.0"


@dataclass
class Issue:
    severity: str
    rule: str
    message: str
    where: str = ""


@dataclass
class Endpoint:
    method: str
    path: str
    tier: str
    axis: str
    auth: str
    status: str
    notes: str = ""
    rate_limit: str | None = None
    cache_ttl: str | None = None
    handler: str | None = None


@dataclass
class Cell:
    axis: str
    tier: str

    def to_str(self) -> str:
        return f"{self.axis}×{self.tier}"


@dataclass
class Service:
    name: str
    port: int | None
    owner: str
    card: str
    priority: str
    scope: str
    category: str
    python_prior_art: str | None
    cells: list[Cell] = field(default_factory=list)
    depends_on: list[str] = field(default_factory=list)
    endpoints: list[Endpoint] = field(default_factory=list)


SERVICE_HEADER_RE = re.compile(
    r"^##\s+([a-z][a-z0-9\-]*)"
    r"\s*·\s*"
    r"(?:no-port|:(\d+))"
    r"\s*·\s*"
    r"([a-z\- ]+?)"
    r"\s*·\s*"
    r"(P[012])\s*$",
    re.IGNORECASE,
)

OWNER_LINE_RE = re.compile(
    r"^Owner:\s*([^·]+?)\s*·\s*Card:\s*([^·]+?)\s*·\s*Cells:\s*(.+?)\s*$",
    re.IGNORECASE,
)

SCOPE_LINE_RE = re.compile(
    r"^([a-z\-]+(?:\s*\|\s*[a-z\-]+)*)\s*·\s*Python prior art:\s*(.+?)\s*$",
    re.IGNORECASE,
)

DEPENDS_LINE_RE = re.compile(r"^Depends on:\s*(.+?)\s*$", re.IGNORECASE)

CELL_RE = re.compile(r"\[\s*([ABC])\s*[×x]\s*([a-z\-]+)\s*\]", re.IGNORECASE)
TABLE_ROW_RE = re.compile(r"^\|(.+)\|\s*$")
TABLE_SEP_RE = re.compile(r"^\|[\s\-:|]+\|\s*$")


def _extract_service_blocks(md: str) -> list[str]:
    lines = md.splitlines()
    blocks: list[list[str]] = []
    current: list[str] | None = None
    for line in lines:
        is_h2 = line.startswith("## ")
        is_h1 = line.startswith("# ") and not line.startswith("## ")
        is_service_header = is_h2 and SERVICE_HEADER_RE.match(line) is not None
        if is_service_header:
            if current is not None:
                blocks.append(current)
            current = [line]
        elif is_h1 or (is_h2 and current is not None):
            if current is not None:
                blocks.append(current)
                current = None
        elif current is not None:
            current.append(line)
    if current is not None:
        blocks.append(current)
    return ["\n".join(b) for b in blocks]


def _parse_endpoint_table(lines: list[str], issues: list[Issue], svc_name: str) -> list[Endpoint]:
    eps: list[Endpoint] = []
    in_table = False
    header_seen = False
    for ln in lines:
        if not in_table:
            if TABLE_ROW_RE.match(ln) and "Endpoint" in ln and "Method" in ln:
                in_table = True
                header_seen = False
            continue
        if TABLE_SEP_RE.match(ln):
            header_seen = True
            continue
        if not TABLE_ROW_RE.match(ln):
            in_table = False
            continue
        if not header_seen:
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) < 6:
            issues.append(
                Issue(
                    "warning",
                    "table-row-short",
                    f"endpoint row had {len(cells)} columns, expected 7",
                    svc_name,
                )
            )
            continue
        path, method, tier, axis, auth, status, *rest = cells
        notes = rest[0] if rest else ""
        eps.append(
            Endpoint(
                method=method.upper().strip(),
                path=path.strip(),
                tier=tier.strip().lower(),
                axis=axis.strip().upper(),
                auth=auth.strip(),
                status=status.strip().lower(),
                notes=notes.strip(),
            )
        )
    return eps


def _parse_service_block(block: str, issues: list[Issue]) -> Service | None:
    lines = block.splitlines()
    if not lines:
        return None
    header = lines[0]
    m = SERVICE_HEADER_RE.match(header)
    if not m:
        return None
    name = m.group(1).lower()
    port_str = m.group(2)
    port = int(port_str) if port_str else None
    category = m.group(3).strip().lower()
    priority = m.group(4).upper()

    owner = ""
    card = ""
    cells: list[Cell] = []
    scope = ""
    python_prior_art: str | None = None
    depends_on: list[str] = []

    for ln in lines[1:]:
        s = ln.strip()
        if not s or s.startswith("|"):
            continue
        m_owner = OWNER_LINE_RE.match(s)
        if m_owner:
            owner = m_owner.group(1).strip()
            card = m_owner.group(2).strip()
            cells_text = m_owner.group(3).strip()
            cells = [
                Cell(axis=c.group(1).upper(), tier=c.group(2).lower())
                for c in CELL_RE.finditer(cells_text)
            ]
            continue
        m_scope = SCOPE_LINE_RE.match(s)
        if m_scope:
            scope = m_scope.group(1).strip().lower()
            ppa = m_scope.group(2).strip()
            python_prior_art = (
                None if ppa.lower() in ('"none"', "none", "—", "-") else ppa
            )
            continue
        m_deps = DEPENDS_LINE_RE.match(s)
        if m_deps:
            depends_on = [d.strip() for d in m_deps.group(1).split(",") if d.strip()]
            continue

    endpoints = _parse_endpoint_table(lines, issues, name)
    return Service(
        name=name,
        port=port,
        owner=owner,
        card=card,
        priority=priority,
        scope=scope,
        category=category,
        python_prior_art=python_prior_art,
        cells=cells,
        depends_on=depends_on,
        endpoints=endpoints,
    )


def parse_portal(portal_md: str, issues: list[Issue]) -> list[Service]:
    blocks = _extract_service_blocks(portal_md)
    services: list[Service] = []
    for blk in blocks:
        svc = _parse_service_block(blk, issues)
        if svc is not None:
            services.append(svc)
    return services


def validate(services: list[Service], repo_root: Path) -> list[Issue]:
    issues: list[Issue] = []
    seen_ports: dict[int, str] = {}
    seen_methods: dict[tuple[str, str], str] = {}

    for svc in services:
        ctx = svc.name
        if svc.port is None:
            issues.append(Issue("error", "missing-port", "service has no port", ctx))
        elif svc.port in seen_ports:
            issues.append(
                Issue(
                    "error",
                    "port-collision",
                    f"port {svc.port} already used by '{seen_ports[svc.port]}'",
                    ctx,
                )
            )
        else:
            seen_ports[svc.port] = svc.name

        if not svc.owner:
            issues.append(Issue("error", "missing-owner", "service has no owner", ctx))
        if not svc.card:
            issues.append(
                Issue("error", "missing-card", "service has no capability card path", ctx)
            )
        elif not (repo_root / svc.card).exists():
            issues.append(
                Issue(
                    "error",
                    "missing-card-file",
                    f"card path does not exist: {svc.card}",
                    ctx,
                )
            )

        if svc.cells and not svc.endpoints:
            issues.append(
                Issue(
                    "error",
                    "cells-without-endpoints",
                    "service has cells declared but no endpoints",
                    ctx,
                )
            )

        for ep in svc.endpoints:
            ep_ctx = f"{svc.name} {ep.method} {ep.path}"
            if ep.tier not in VALID_TIERS:
                issues.append(
                    Issue(
                        "error",
                        "missing-or-invalid-tier",
                        f"tier '{ep.tier}' not in {VALID_TIERS}",
                        ep_ctx,
                    )
                )
            if ep.axis not in VALID_AXES:
                issues.append(
                    Issue(
                        "error",
                        "missing-or-invalid-axis",
                        f"axis '{ep.axis}' not in {VALID_AXES}",
                        ep_ctx,
                    )
                )
            mkey = (ep.method, ep.path)
            if mkey in seen_methods:
                issues.append(
                    Issue(
                        "error",
                        "path-method-collision",
                        f"{ep.method} {ep.path} also declared by '{seen_methods[mkey]}'",
                        ep_ctx,
                    )
                )
            else:
                seen_methods[mkey] = svc.name

        cell_endpoint_count: dict[str, int] = {}
        for ep in svc.endpoints:
            key = f"{ep.axis}×{ep.tier}"
            cell_endpoint_count[key] = cell_endpoint_count.get(key, 0) + 1
        for cell, n in cell_endpoint_count.items():
            if n > 30:
                issues.append(
                    Issue(
                        "warning",
                        "cell-concentration",
                        f"cell {cell} has {n} endpoints (>30 — consider splitting)",
                        svc.name,
                    )
                )

        tiers_in_svc = {ep.tier for ep in svc.endpoints if ep.tier in VALID_TIERS}
        if len(tiers_in_svc) >= 3:
            issues.append(
                Issue(
                    "warning",
                    "tier-mix",
                    f"service spans {len(tiers_in_svc)} tiers ({sorted(tiers_in_svc)}) "
                    "— will become hard fail in Phase 4",
                    svc.name,
                )
            )

    return issues


def to_dict(svc: Service) -> dict:
    return {
        "name": svc.name,
        "port": svc.port,
        "owner": svc.owner,
        "card": svc.card,
        "priority": svc.priority,
        "scope": svc.scope,
        "category": svc.category,
        "python_prior_art": svc.python_prior_art,
        "cells": [c.to_str() for c in svc.cells],
        "depends_on": svc.depends_on,
        "endpoints": [
            {
                "method": ep.method,
                "path": ep.path,
                "tier": ep.tier,
                "axis": ep.axis,
                "auth": ep.auth,
                "status": ep.status,
                "notes": ep.notes,
                "rate_limit": ep.rate_limit,
                "cache_ttl": ep.cache_ttl,
                "handler": ep.handler,
            }
            for ep in svc.endpoints
        ],
    }


def build_catalog(services: list[Service]) -> dict:
    """UI-optimized projection of the manifest, consumed by the
    /devops/catalog page. Pre-computes axis × tier cell occupancy plus
    per-service summaries so the Go handler can render the grid heat-map
    via stdlib encoding/json (no Go YAML dep needed).

    No generated_at timestamp — the file is content-addressable via
    `generated_from` SHA hashes in manifest.yaml. Including a timestamp
    causes git churn on every `make manifest` run for no reproducibility
    benefit."""
    cells: dict[tuple[str, str], dict] = {}
    for axis in VALID_AXES:
        for tier in VALID_TIERS:
            cells[(axis, tier)] = {
                "axis": axis,
                "tier": tier,
                "endpoint_count": 0,
                "services": [],
            }
    service_summaries: list[dict] = []
    for svc in services:
        cell_set: set[tuple[str, str]] = set()
        for ep in svc.endpoints:
            if ep.axis in VALID_AXES and ep.tier in VALID_TIERS:
                key = (ep.axis, ep.tier)
                cells[key]["endpoint_count"] += 1
                cell_set.add(key)
        for key in cell_set:
            if svc.name not in cells[key]["services"]:
                cells[key]["services"].append(svc.name)
        service_summaries.append(
            {
                "name": svc.name,
                "port": svc.port,
                "priority": svc.priority,
                "category": svc.category,
                "scope": svc.scope,
                "owner": svc.owner,
                "card": svc.card,
                "cells": [c.to_str() for c in svc.cells],
                "endpoint_count": len(svc.endpoints),
                "python_prior_art": svc.python_prior_art,
            }
        )
    cell_list = [cells[(a, t)] for a in VALID_AXES for t in VALID_TIERS]
    return {
        "axes": [
            {"key": "A", "name": "Adapter", "direction": "POS → Canary"},
            {"key": "B", "name": "Resource", "direction": "Canary → external"},
            {"key": "C", "name": "Agent", "direction": "Canary → AI agents"},
        ],
        "tiers": list(VALID_TIERS),
        "cells": cell_list,
        "services": service_summaries,
        "totals": {
            "service_count": len(services),
            "endpoint_count": sum(len(s.endpoints) for s in services),
        },
    }


def emit_catalog(catalog: dict, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
        f.write("\n")


def emit_manifest(services: list[Service], inputs: list[Path], output: Path) -> dict:
    generated_from = []
    for p in inputs:
        if p.exists():
            data = p.read_bytes()
            try:
                rel = str(p.relative_to(REPO_ROOT)) if p.is_absolute() else str(p)
            except ValueError:
                rel = str(p)
            generated_from.append(
                {
                    "path": rel,
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "bytes": len(data),
                }
            )
    payload = {
        "version": MANIFEST_VERSION,
        "generated_from": generated_from,
        "tiers": list(VALID_TIERS),
        "axes": [
            {"key": "A", "name": "Adapter", "direction": "POS → Canary"},
            {"key": "B", "name": "Resource", "direction": "Canary → external"},
            {"key": "C", "name": "Agent", "direction": "Canary → AI agents"},
        ],
        "services": [to_dict(s) for s in services],
        "tenants": [],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w") as f:
        yaml.safe_dump(payload, f, sort_keys=False, default_flow_style=False, width=120)
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Parse Brain canary-go-portal.md → manifest.yaml"
    )
    parser.add_argument("--portal", default=str(DEFAULT_PORTAL))
    parser.add_argument("--microsvc", default=str(DEFAULT_MICROSVC))
    parser.add_argument("--canonical", default=str(DEFAULT_CANONICAL))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--catalog", default=str(DEFAULT_CATALOG),
                        help="Path for devops-catalog.json (UI-optimized projection)")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero on hard-fail rule violations "
        "(default: warn only — Phase 4 will enforce)",
    )
    args = parser.parse_args(argv)

    portal = Path(args.portal)
    if not portal.exists():
        print(f"error: portal not found: {portal}", file=sys.stderr)
        return 2

    portal_md = portal.read_text()
    issues: list[Issue] = []
    services = parse_portal(portal_md, issues)
    issues.extend(validate(services, REPO_ROOT))

    errors = [i for i in issues if i.severity == "error"]
    warnings = [i for i in issues if i.severity == "warning"]
    for i in issues:
        prefix = "ERROR" if i.severity == "error" else "WARN"
        loc = f" [{i.where}]" if i.where else ""
        print(f"{prefix} {i.rule}{loc}: {i.message}", file=sys.stderr)

    output = Path(args.output)
    catalog_out = Path(args.catalog)
    inputs = [Path(args.portal), Path(args.microsvc), Path(args.canonical)]
    emit_manifest(services, inputs, output)
    catalog = build_catalog(services)
    emit_catalog(catalog, catalog_out)
    print(f"wrote {output}", file=sys.stderr)
    print(f"wrote {catalog_out}", file=sys.stderr)
    print(f"  services:  {len(services)}", file=sys.stderr)
    print(
        f"  endpoints: {sum(len(s.endpoints) for s in services)}", file=sys.stderr
    )
    print(f"  errors:    {len(errors)}", file=sys.stderr)
    print(f"  warnings:  {len(warnings)}", file=sys.stderr)

    if args.strict and errors:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
