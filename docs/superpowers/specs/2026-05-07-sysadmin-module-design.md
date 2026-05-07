# Sysadmin Module + Manifest-Driven API Gateway — Design Spec

**Date:** 2026-05-07
**Status:** Approved (brainstorm complete)
**Owner:** Founder
**Scope:** Build the platform-operator sysadmin module at `/devops/*`, anchored on a manifest-driven API gateway that occupies one cell of a 3×5 cadence-ladder grid per endpoint and ports forward ~12,000 LOC of Python prior art skipped during the Go migration.

---

## Why this exists

The Canary platform has three drift problems that compound:

1. **Spec ↔ implementation drift.** The auto-generated OpenAPI describes 135 entity-CRUD paths (`/v1/m/`, `/v1/l/`, `/v1/s/`, `/v1/c/`); the gateway actually mounts ~111 domain-shaped routes (`/v1/alerts/*`, `/v1/owl/*`, etc.). They don't overlap. Partner-facing claims of "we have an API" are not defensible against the running code.

2. **Operator-surface drift.** The Python prototype shipped a substantial devops module — `devops_monitor.py` (pipeline visibility), `ops_console.py` (test-lab UI), `scenario_runner.py` + `scenario_fire.py` (Live Fire test harness), `health_check/*` (~5,000 LOC of merchant simulator + chirp lab + heartbeat + data factory + 9 generators), `qa_agent/*` (1,071 LOC of page-aware operator agent), `atlas/*` (Mermaid diagram engine), `goose/*` (1,311 LOC of L402 wallet + treasury + Strike Lightning), `metrics_etl.py` (1,203 LOC star-schema pipeline). All of it skipped during the Go port. ~12,000 LOC of operator-facing infrastructure missing in the new platform.

3. **Tier discipline drift.** The cadence ladder (Stream / Change-feed / Daily batch / Bulk window / Reference) is documented at `crb.growdirect.io/engineering/cadence-ladder.html` as the platform's organizing principle: every endpoint occupies exactly one cell of a 3×5 grid (Adapter / Resource / Agent × five tiers). "Mixing tiers in one endpoint makes health unmonitorable." Today the discipline is folklore — no build check enforces it; every route gets the same middleware stack.

This spec resolves all three with one coherent build.

---

## Architecture

### The cadence ladder is the organizing principle

Every endpoint declares its cell on the 3×5 grid. The grid is data, not opinion — it lives in the manifest and drives everything downstream.

| | Stream (ms–s) | Change-feed (min–hr) | Daily batch | Bulk window (weekly) | Reference (monthly+) |
|---|---|---|---|---|---|
| **A · Adapter** (POS → Canary) | webhook receivers, scan events | RapidPOS poll, Shopify sync | — | — | vendor catalog |
| **B · Resource** (Canary → external) | — | `/v1/alerts`, `/v1/owl/*` | `/v1/billing/cost-rollup` | `/v1/protocol/anchors` | `/v1/m/items`, `/v1/l/locations` |
| **C · Agent** (Canary → AI agents) | — | `canary.alert.list`, `canary.owl.cases` | — | — | `canary.catalog.lookup` |

The grid has axis × tier coverage — each cell has its own protocol, auth posture, rate limit, health-check semantics, cache strategy, recovery model.

### Manifest is the single source of truth

A YAML artifact generated from the existing Brain markdown endpoint library + canonical SDDs. Drives:

- **Gateway routing** at boot — picks tier-specific middleware stack per route
- **OpenAPI spec generation** — `services/canary-protocol/openapi/openapi.yaml` regenerated, no longer drifts from impl
- **Devops catalog UI** — `/devops/catalog` reads `devops-catalog.json` for the grid heat-map and service list
- **Per-tier observability rollups** — five separate health surfaces, not one
- **Brain capability cards** — frontmatter generated; body human-edited
- **Public partner doc** at `crb.growdirect.io/engineering/endpoint-library` — generated, not curated

Markdown stays the human editing surface (existing Brain wiki workflow). YAML is the machine intermediate. Generator runs in CI on every commit.

### Sysadmin module at `/devops/*`

Platform-operator UI surface (founder + future devops team). Cross-tenant by default; tenant-scoped services (the existing W9 `/admin/*` fold-in) require explicit tenant context selection.

Shape: side nav with grouped services + a canonical service-detail-page that every `/devops/<service>` instance renders.

### Service-detail-page common shape (six zones)

```
┌─ HEADER ─────────────────── name · port · status · tenant/env selectors ─┐
├─ CAPABILITY ─────────── owner · card · cells on the 3×5 grid · mounted? ─┤
├─ KPI STRIP ───────────────────────── 4 service-specific metric tiles ─────┤
├─ ENDPOINTS ──────────────── endpoints in this service's cells, by tier ───┤
├─ SERVICE BODY ─────────────────── operator-workflow UI specific to service ┤
├─ ACTIVITY ─────────────────────── recent events / mutations · audit slice ┤
└─ LINKED ────────────────────────── depends-on · used-by service graph ────┘
```

Adapts across the three categories:
- **Cross-tenant infra**: tenant=all, KPIs are aggregate, endpoints are global
- **Test & validation**: env=lab|live-fire, KPIs are pass-rate / runs-today
- **Tenant-scoped**: tenant=required, KPIs and endpoints are filtered to selected tenant

---

## Service inventory

**~37 `/devops/*` UI sections** + **~50 catalog entries** (the latter includes ~20 catalog-only services with no dedicated UI section, monitored via observability + manifest).

### Cross-tenant infra (19 services, 18 with UI)

`catalog · manifest · observability · pipeline · api-docs · qa-agent · etl · wallet (goose) · evidence · vault · flags · notifications · risk-vocab · parsers · rule-packs · atlas · method · alx-agent · condor · integrations · devices · keys · tenants`

### Test & validation (11 services)

`test-lab · scenarios · pos-lab · live-fire · merchant-simulator · heartbeat · fixtures · payload-factory · sandbox-seeder · capability-explorer · scenario-verify`

### Tenant-scoped (7 services — existing `/admin/*` fold-in)

`audit · compliance · users · config · hierarchy · network-integrity · cross-store`

### Catalog-only (~20 — monitored, no /devops UI section)

Merchant-facing services and small utilities: `alert · owl · chirp · fox · hawk · identity · analytics · customer · employee · item · location · transaction · inventory · billing-meter · raas · bff · tsp (engine) · velocity-engine · employee-risk-scoring · heatmap-scoring · impact-scoring · period-aggregation · fact-builder · fiscal-calendar`

### Build-priority cuts

| Wave | Services | LOC est. | What it unlocks |
|---|---|---|---|
| **P0** | 10 — catalog · manifest · observability · pipeline · api-docs · qa-agent · etl · wallet · test-lab · live-fire+pos-lab+scenarios | ~6,500 | Sysadmin module exists, operator can see + monitor + test, billing infra functional, qa-agent restored |
| **P1** | 22 — net-new infra + secondary recovery + tenant-scoped fold-in | ~5,000 | Full operator workflows, /admin/* fold-in, complete test suite |
| **P2** | 5 — keys, users (blocked on GRO-769/770), alx-agent, condor, capability-explorer + risk-vocab | ~500 | Polish + specialty + blocked surfaces unblock when upstream lands |

15 of the 37 UI sections have Python prior art to port forward (~12,000 LOC of recovery work).

---

## Per-tier infrastructure

Each of the five tiers gets its own routing pipeline at the gateway:

| Tier | Protocol | Auth | Rate limit | Health | Cache | Recovery |
|---|---|---|---|---|---|---|
| **Stream** | SSE / WebSocket / Valkey XREAD tail | Long-lived token | Concurrent connections | Heartbeat (no msg in N sec) | N/A | Replay from queue |
| **Change-feed** | REST polling with cursor / sub with watermark | API key per request | Requests/min per key | Lag exceeded / queue depth | Short TTL (~5 min) | Catch up from watermark |
| **Daily batch** | Cron-driven export | Service-to-service signed | Rate-of-runs | Schedule missed / checksum diff | N/A | Rerun the job |
| **Bulk window** | Scheduled file drop / blob | Signed URL | Window-bounded | Didn't land / row count off | N/A | Reschedule |
| **Reference** | REST GET with strong cache headers | API key (anon-read possible) | High requests/min | Version drift | Long TTL (~60s hot) | Force resync |

### Built today vs net-new

- **Built**: chi router, API key middleware, audit middleware
- **Partial**: Valkey streams (internal, not edge-exposed); Bitcoin L2 anchor (sub3, hourly/daily ad-hoc); pgxpool (no edge cache)
- **Net-new in P0**: tier declaration + tier-aware middleware swap, reference cache (Valkey TTL), stream layer at edge (SSE/WS), per-tier health rollups
- **Net-new in P1**: cursor/watermark proxy, cron framework, bulk-window dispatcher, per-tier rate-limit policies

### Architecture

One `chi.Router` fans out into five middleware stacks based on the manifest's `tier:` declaration per route. Five separate health rollups feed into `/devops/observability`.

---

## Manifest schema

### Pipeline

```
Brain/wiki/canary-go-portal.md       ──┐
Brain/wiki/cards/<service>.md         ─├─→ services/canary-protocol/manifest/gen/
docs/sdds/go-handoff/microservice...  ─├─→   parse_manifest.py
docs/sdds/go-handoff/canonical-data... ┘                │
                                                        ▼
                                            ┌────────── 6 outputs ─────────────┐
                                            │ manifest.yaml         (machine)  │
                                            │ openapi.yaml          (Redoc)    │
                                            │ devops-catalog.json   (UI)       │
                                            │ endpoint-library.md   (CRB)      │
                                            │ service-cards/*.md    (Brain)    │
                                            │ cell-occupancy.txt    (CI)       │
                                            └──────────────────────────────────┘
```

### manifest.yaml structure

Top-level: `version`, `generated_at`, `generated_from`, `tiers`, `axes`, `services`, `tenants`.

Each service: `name · port · owner · card · priority · scope · category · python_prior_art · cells · depends_on · endpoints[]`.

Each endpoint: `method · path · tier · axis · auth · rate_limit · cache_ttl · status · handler`.

### Validation rules

**Hard fails** (build aborts): missing tier/axis on any endpoint; missing port/owner/card on any service; service has cells but no matching endpoints; capability card path doesn't exist; port collision; path+method collision.

**Warnings** (build continues): proposed-but-mounted; mounted-but-not-found; missing python_prior_art when porting; cell concentration > 30 endpoints; tier-mix endpoints (loud, will become hard fail in Phase 4).

### Repo layout

```
services/canary-protocol/
├── openapi/                       (existing — regenerated)
│   ├── openapi.yaml
│   └── gen/generate.py
└── manifest/                      (NEW)
    ├── manifest.yaml
    ├── devops-catalog.json
    ├── README.md
    └── gen/
        ├── parse_manifest.py
        ├── emit_openapi.py
        ├── emit_catalog.py
        ├── validate.py
        └── routewalk.go        (compiled into gateway, emits routes-seen.json at boot)
```

---

## Migration path

Four phases. Each independently shippable. Gateway never down. Dev never frozen.

### Phase 1 — Bootstrap (~3 days, zero runtime change)

- Build `parse_manifest.py` (markdown → YAML)
- Build `routewalk.go` (chi.Walk over live gateway)
- Build `reconcile.py` (diff manifest vs routes-seen vs openapi)
- Skeleton manifest with 3-5 hand-authored core services
- **Gate:** drift-report.txt has fewer than 10 unaccounted endpoints

### Phase 2 — Backfill + read-only consumers (~2 weeks)

- Backfill all 33 existing services into manifest (one PR per service)
- Devops catalog UI starts reading `devops-catalog.json`
- Redoc starts reading regenerated `openapi.yaml`
- CRB endpoint-library publishes from generator
- **Constraint going forward:** new endpoints must add a manifest row in the same PR
- **Gate:** all 33 services covered, drift-report empty

### Phase 3 — Tier-aware middleware (~2 weeks, feature-flagged)

Per-tier flag (default off until proved stable):
- `TIER_REFERENCE_CACHE=1` — Valkey TTL cache for `/v1/m/*`, `/v1/l/*` (cheapest, biggest win)
- `TIER_CHANGE_FEED=1` — cursor + watermark middleware
- `TIER_STREAM=1` — SSE/WS at edge (required for chirp + replenishment)
- Daily-batch + bulk-window deferred to P1 (existing Valkey-stream patterns suffice)
- Per-tier health rollups light up at `/devops/observability`
- **Gate:** all 5 tier flags default-on stable for one week

### Phase 4 — Hard enforcement (~3 days)

- CI hard-fail on validate errors (was warning in Phase 2)
- Route-walk vs manifest mismatch fails the build
- Tier-mix endpoints rejected at gateway boot
- Pre-commit hook runs `make manifest`
- **End state:** adding an endpoint = one Go handler + one markdown row · drift impossible

### Reconciling the existing 24-endpoint gap

| Category | Manifest status | Resolution |
|---|---|---|
| Spec'd but not built | `status: proposed` | Stays in spec; gateway doesn't mount; CRB renders dimmed |
| Built but not spec'd | `status: mounted` | Add to manifest in P2 backfill; openapi regenerates with these |
| Wrong-spec mismatches | `status: drift` | PR to align — usually impl is right, spec wrong |
| Test/dev only | `env: lab\|live-fire` | Stays mounted but tagged so prod traffic doesn't see it |

### Total scope

| Phase | Duration | Tickets est. | Risk |
|---|---|---|---|
| P1 · Bootstrap | ~3 days | 3 | Low — pure tooling |
| P2 · Backfill + read-only | ~2 weeks | ~33 | Low — one PR per service |
| P3 · Tier middleware | ~2 weeks | 5–8 | Medium — feature-flagged refactor |
| P4 · Hard enforcement | ~3 days | 2 | Low — flips warnings to errors |

~5 weeks elapsed across migration. The sysadmin module UI work (~36 services × varying complexity) overlays Phase 2 + Phase 3, adding ~50–80 additional tickets across the build wave.

---

## Out of scope

- **`Canary/devops/` directory** in the Python prototype (deployment infra: migrations, nginx, cloudflared, seeders, pgadmin). Already lives in `CanaryGo/deploy/`. A future `/devops/deploys` view that reads CI/CD output is possible but not part of this spec.
- **Merchant-facing portal changes.** Existing `/admin/*` paths stay live during Phase 2 as 301-redirects to `/devops/*`. Merchant dashboard, alerts, cases, owl, etc. unchanged.
- **GRO-769 identity middleware + GRO-770 admin module.** Required for tenant-scoped service auth (`/devops/users` blocked on these). P2.
- **Cross-tenant data migration.** No data moves; we're adding a UI layer over what's already there.
- **CI/CD changes** beyond adding the manifest build step. No deploy pipeline rewrite.

---

## Acceptance criteria

The package ships when:

1. `make manifest` produces all 6 artifacts, exits clean
2. Gateway boots successfully reading manifest.yaml; route mount is deterministic
3. `/devops/catalog` renders the 3×5 grid heat-map with live counts
4. Every P0 service has a `/devops/<service>` page rendering the canonical six-zone shell
5. Spec/impl drift count is zero (validated by reconcile.py)
6. Five per-tier health rollups are visible at `/devops/observability`
7. Reference cache layer (Valkey TTL) is live for `/v1/m/*` and `/v1/l/*`
8. Stream layer at edge (SSE/WS) supports at least one consumer (chirp event stream)
9. CI hard-fails on validate errors
10. Adding a new endpoint is one Go handler + one markdown row, verified by a sample shopify adapter walkthrough

---

## References

Brainstorm visuals at `.superpowers/brainstorm/88823-1778133944/`:
- `cadence-management.html` — three management approaches; manifest-driven picked
- `catalog-ui.html` — three layout options; grid-first picked
- `sysadmin-module.html` — two-surface carve (`/admin/*` merchant, `/devops/*` platform)
- `service-inventory.html` + `python-prior-art.html` + `python-prior-art-v2.html` + `python-prior-art-v3.html` + `python-prior-art-final.html` + `inventory-floor.html` — the five-pass walk through the Python prototype
- `priority-cuts.html` — P0/P1/P2 wave structure
- `service-page-shape.html` — canonical six-zone page
- `per-tier-infra.html` — five middleware pipelines
- `manifest-schema.html` + `manifest-walkthrough.html` — manifest design + worked example
- `migration-path.html` — four-phase migration

External references:
- `crb.growdirect.io/engineering/cadence-ladder.html` — cadence ladder doc
- `crb.growdirect.io/engineering/endpoint-library.html` — current hand-curated endpoint library
- Python Canary prototype at `~/GrowDirect/Canary/` — frozen at v0-python-prototype tag
