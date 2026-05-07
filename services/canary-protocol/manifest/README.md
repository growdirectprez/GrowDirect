# Canary Protocol — Manifest

Single source of truth for the API gateway: every endpoint declares its cell
on the cadence-ladder grid (axis × tier), its capability card, port, owner,
auth posture, and status.

## Pipeline

```
Brain/wiki/canary-go-portal.md           ──┐
docs/sdds/go-handoff/microservice-arch.md ─├─→ gen/parse_manifest.py
docs/sdds/go-handoff/canonical-data.md   ──┘                │
                                                            ▼
                                              services/canary-protocol/manifest/manifest.yaml
                                                            │
                                                            ├─→ openapi/openapi.yaml (regenerated)
                                                            ├─→ devops-catalog.json (UI)
                                                            ├─→ endpoint-library.md (CRB)
                                                            ├─→ service-cards/*.md (Brain)
                                                            └─→ cell-occupancy.txt (CI)
```

## Run

```bash
python3 services/canary-protocol/manifest/gen/parse_manifest.py
```

Add `--strict` to exit non-zero on hard-fail rule violations (default: warn
only — Phase 4 wires hard-fail into CI).

## Tests

```bash
cd services/canary-protocol/manifest/gen
python3 -m pytest -q
```

## Schema

See `docs/superpowers/specs/2026-05-07-sysadmin-module-design.md`
§"manifest.yaml structure" + §"Validation rules".

## Phase status

- **Phase 1 (Bootstrap)** — parser + routewalk + reconcile shipped. Skeleton
  manifest contains `catalog`, `manifest`, `observability`, `pipeline`,
  `qa-agent` so the parser has working examples.
- **Phase 2 (Backfill)** — one ticket per existing service backfills its
  manifest entry. Drift report goes to zero.
- **Phase 3 (Tier middleware)** — gateway boot reads manifest, picks
  tier-aware middleware stack per route. Feature-flagged.
- **Phase 4 (Hard enforcement)** — validation rules become build errors;
  pre-commit hook runs `make manifest`; route-walk vs manifest mismatch
  fails the build.
