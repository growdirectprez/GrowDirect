# Sysadmin Module + Manifest-Driven Gateway — Autonomous Runner

**Purpose:** Deliver the whole package — manifest-driven API gateway, tier-aware middleware, sysadmin module UI at `/devops/*`, and recovery of ~12,000 LOC of Python prior art skipped during the Go port. Four phases, ~5 weeks elapsed, ~85–115 tickets total. Gateway never down; dev never frozen; every step independently shippable.

**Design spec:** [`docs/superpowers/specs/2026-05-07-sysadmin-module-design.md`](../superpowers/specs/2026-05-07-sysadmin-module-design.md). Read it before starting any phase. The spec is the contract.

**How to invoke:**
- **One-shot grind:** paste this whole file into a fresh Claude session. The agent runs phases in order, ships each, exits when done or blocked.
- **Cron / loop:** `/loop 60m <paste contents>` — agent fires every hour, picks up the next ready ticket in the active phase, ships it, sleeps. (Sixty-minute interval because tickets are larger than the W-series.)

---

## Operating Posture

You are running unattended on a multi-week initiative. The user has authorized you to:

- Move Linear dispatches through their lifecycle (Backlog/Todo → In Progress → Done). Create new sub-issues under the umbrella epic for tickets that emerge during execution. Post status comments without per-ticket confirmation.
- Make code changes in: `services/canary-protocol/manifest/` (new), `services/canary-protocol/openapi/` (regenerate), `internal/web/` (devops module + handlers + templates), `cmd/gateway/main.go` (route grouping by tier), `Brain/wiki/canary-go-portal.md` (manifest source), `Brain/wiki/cards/<service>.md` (capability frontmatter), `deploy/migrations/` (only if a service genuinely needs new schema — the spec calls these out explicitly).
- Add new packages under `internal/` for services that don't have a Go implementation yet. Each new package follows the existing pattern: store + handler + tests.
- Push the working branch after each phase gate. **Do not merge to main, do not open PRs**, do not force-push, do not modify CI/CD config beyond adding the manifest build step.
- Skip-cut to placeholder when substrate genuinely doesn't exist. Document the gap in the close-out comment for that ticket and continue. The W6/W5/W8/W9/W10/W11 closeouts are the reference for how to document a skip-cut.

You are NOT authorized to:

- Modify or delete code outside the Canary.GO scope (no Cove/, Angel/, Brain/* outside wiki/canary-go-portal.md and wiki/cards/).
- Touch the Python `Canary/` directory at all. It's frozen at v0-python-prototype. Read-only research source.
- Skip the design spec. If a ticket asks you to do something the spec doesn't authorize, stop and surface it.
- Add new top-level dependencies (`go get`, `go.mod` mutations) without explicit user sign-off. The spec accounts for what we have; net-new deps are a flag.
- Open PRs to main, force-push, modify CI pipelines, change Docker compose, change deploy/migrations beyond what's explicitly in the spec.
- Skip tests. Every commit must build clean. Every new POST handler needs a no-store empty-state test + a 303-redirect contract test (W5–W11 patterns).

If you hit a real block — build error you can't fix, test failure you can't reproduce, schema migration the spec didn't anticipate, ambiguity that would change the architecture — **stop**, comment on the active Linear issue with what you tried and what's blocking, leave the issue in `In Progress`, and exit. The user picks it up from there.

---

## Working Branch

Phase 1 work happens on a **new branch** off `main`: `claude/sysadmin-module-bootstrap`. Each subsequent phase branches off the prior phase's tip:

- Phase 1 → `claude/sysadmin-module-bootstrap`
- Phase 2 → `claude/sysadmin-module-backfill` (off Phase 1 tip after merge to main)
- Phase 3 → `claude/sysadmin-module-tier-middleware`
- Phase 4 → `claude/sysadmin-module-enforcement`

If `git status` at session start shows uncommitted changes on a phase branch, treat that as a hand-off in progress: read the diff, decide whether it's mid-work for the active ticket, and either continue or commit-then-continue. Do not blow it away.

If the user has merged a phase branch to main between sessions, branch the next phase off main, not off the prior phase tip.

---

## Linear Setup

At session start of Phase 1, **create a Linear epic**:

- **Project:** Canary.GO
- **Title:** "Sysadmin Module + Manifest-Driven Gateway"
- **Description:** Link to design spec at `docs/superpowers/specs/2026-05-07-sysadmin-module-design.md` + brief summary
- **Status:** In Progress
- **Labels:** `laptop`, `ALX`, `Feature`

All sub-tickets created during execution attach to this epic via `parentId`. The epic is the umbrella; sub-tickets are the work.

If an epic with this title already exists in Canary.GO, reuse it.

---

## Phase Queue

Run phases in order. Each phase has a Gate at the end — **do not advance without confirming the Gate is met.**

### Phase 1 — Bootstrap (~3 days, 3 tickets)

**T1.1: Build `parse_manifest.py`**
- Path: `services/canary-protocol/manifest/gen/parse_manifest.py`
- Reads: `Brain/wiki/canary-go-portal.md`, `docs/sdds/go-handoff/microservice-architecture.md`, `docs/sdds/go-handoff/canonical-data-model.md`
- Emits: `services/canary-protocol/manifest/manifest.yaml`
- Schema: per spec §"manifest.yaml structure"
- Validation: per spec §"Validation rules" — implement hard fails as exit-1, warnings as stderr; do NOT enforce the hard fails yet (Phase 4)
- Tests: pytest covering each validation rule (provide synthetic markdown fixtures)

**T1.2: Build `routewalk.go`**
- Path: `services/canary-protocol/manifest/gen/routewalk.go` (compiled into the gateway)
- At gateway boot (under flag `MANIFEST_ROUTEWALK=1`), `chi.Walk` over the live router, emit `build/routes-seen.json` listing every mounted route + method
- Does NOT change runtime behavior. Strictly observation.

**T1.3: Build `reconcile.py`**
- Path: `services/canary-protocol/manifest/gen/reconcile.py`
- Reads: `manifest.yaml`, `routes-seen.json`, `services/canary-protocol/openapi/openapi.yaml`
- Emits: `build/drift-report.txt` categorizing every endpoint by status (mounted-and-spec'd, spec'd-but-not-built, built-but-not-spec'd, drift)
- Skeleton manifest: hand-author entries for `catalog`, `manifest` (self-reference), `observability`, `pipeline`, `qa-agent` so the parser has working examples

**Gate to Phase 2:** `make manifest` runs clean; `drift-report.txt` exists and is reviewed; ≤ 10 unaccounted endpoints. Commit + push to branch tip; do not advance until you've left a Linear comment on the umbrella epic with the drift report contents.

### Phase 2 — Backfill + read-only consumers (~2 weeks, ~35 tickets)

**T2.0: Mount the devops module shell**
- New package `internal/web/devops/`. Side nav per spec §"Sysadmin module at `/devops/*`". Top nav switches tenant + env (per spec §"Service-detail-page common shape"). Empty service pages render the six-zone shell; service body section says "TODO".
- This is the chrome that all subsequent service pages render inside.

**T2.1–T2.33: Backfill manifest entries (one ticket per existing service)**
For each of the 33 services in the spec inventory, one PR that:
- Adds a section to `Brain/wiki/canary-go-portal.md` declaring the service's name, port, owner, card, priority, scope, category, cells, depends_on, endpoints
- Runs `make manifest` to regenerate manifest.yaml + openapi.yaml + devops-catalog.json + service-cards/<name>.md
- Verifies via `reconcile.py` that the service's drift count goes to zero
- Adds the service to `internal/web/devops/services/<name>.go` as a stub page (empty body, common shell renders)
- Commits

These can ship in parallel by service. Do not block one on another.

**T2.34: Wire `/devops/catalog`**
- Service: catalog (P0). Reads `devops-catalog.json` at gateway boot, renders the 3×5 grid heat-map with live counts per cell. Drill-down to cell shows endpoints in that cell.
- Three view tabs (Grid · Services · Capabilities) per `catalog-ui.html` brainstorm visual.

**T2.35: Wire `/devops/api-docs`**
- Service: api-docs (P0). Embeds Redoc rendering `services/canary-protocol/openapi/openapi.yaml` (regenerated from manifest). Same pattern as Python `devops_monitor.py` `_REDOC_TEMPLATE`.

**T2.36: Publish `endpoint-library.md` to CRB**
- Generated artifact. Replaces the hand-curated `crb.growdirect.io/engineering/endpoint-library.html`. Pushed via the existing CRB workflow (clone → write → commit → push transient pattern in CLAUDE.md).

**T2.37: Add CI step**
- Modify `Makefile` (only) to add `make manifest` target. Run on every PR. Validation rules light up as warnings; hard-fail only triggered on missing tier or missing axis (the bare minimum). Full hard-fail comes in Phase 4.

**Gate to Phase 3:** All 33 services have manifest entries; `drift-report.txt` is empty; W6/W5/W8/W9/W10/W11 services are confirmed in the manifest; `/devops/catalog`, `/devops/api-docs`, and the published endpoint-library.md all render. Commit + push.

### Phase 3 — Tier-aware middleware + P0 service UI (~3 weeks, ~25 tickets)

Two parallel tracks running in this phase. Both must complete before Gate.

**Track A: Tier middleware refactor (5–8 tickets, feature-flagged)**

- **T3A.1: Reference tier first** (cheapest, biggest cache win). Add Valkey TTL cache layer for `/v1/m/*` and `/v1/l/*`. Flag: `TIER_REFERENCE_CACHE=1`. Default off until proved stable across a full week.
- **T3A.2: Change-feed tier middleware.** Cursor + watermark + lag-tracking middleware. Flag: `TIER_CHANGE_FEED=1`. Apply to `/v1/alerts/*`, `/v1/owl/*`, `/v1/chirp/detections`, etc.
- **T3A.3: Stream tier at edge.** SSE for chirp event stream consumers; WebSocket optional. Flag: `TIER_STREAM=1`.
- **T3A.4: Per-tier health rollups.** Five separate health surfaces in `/devops/observability`. Each tier reports its own status independently per spec §"Per-tier infrastructure".
- **T3A.5: Refactor `cmd/gateway/main.go` into tier groups.** Each tier gets its own `r.Group(...)` with the right middleware stack. Manifest tells the router which group a route belongs to.
- Daily-batch + bulk-window tiers explicitly deferred to Phase 4 / P1 follow-up. Existing Valkey-stream-driven patterns suffice for now.

**Track B: P0 service UI (10 services × 1 ticket each = 10 tickets)**

Each ticket builds the full canonical service-detail-page (six zones) for one P0 service:

- T3B.1 `/devops/manifest` — manifest editor + validator + history viewer
- T3B.2 `/devops/observability` — five-tier health rollup + per-service drill-down
- T3B.3 `/devops/pipeline` — Recovery from `devops_monitor.py`. TSP pipeline visualization (Webhook → Sub1 → Sub2 → Sub3). Read substrate from existing tsp/ Go package + audit_log.
- T3B.4 `/devops/qa-agent` — Recovery from `qa_agent/*` (1,071 LOC). Page-aware operator agent. Build sidecar architecture matching the Python pattern; consume cross-service MCP tools; Linear bug filing via `mcp__a018de2b-...__save_issue`.
- T3B.5 `/devops/etl` — Recovery from `metrics_etl.py` (1,203 LOC). Daily-batch ETL runner with run history, retry, schedule status.
- T3B.6 `/devops/wallet` — Recovery from `goose/*` (1,311 LOC). L402 wallet + treasury + Strike Lightning + gas schedule + macaroon revoke. New migration for wallet tables (spec §"Out of scope" calls migrations as exception).
- T3B.7 `/devops/test-lab` — Recovery from `ops_console.py` test_lab single-screen UI.
- T3B.8 `/devops/scenarios` — Recovery from `scenario_runner.py` + `scenario_verify.py`. Scripted scenarios + randomizers + verification.
- T3B.9 `/devops/pos-lab` — Recovery from `health_check/chirp_lab.py`. Local Fire (DB-direct, ~50ms) and Live Fire (real Square sandbox).
- T3B.10 `/devops/live-fire` — Recovery from `scenario_fire.py`. Real Square sandbox round-trip via SDK; webhooks come back through the live pipeline.

For each P0 service: read the Python prior art at `~/GrowDirect/Canary/canary/...` first, port the operator workflow forward (not the implementation — adapt to Go idioms), build the UI section, write tests, commit, post Linear close-out.

**Existing `/admin/*` fold-in:** in this phase, add 301-redirects from `/admin/audit`, `/admin/iso27001`, `/admin/users`, `/admin/config`, `/admin/hierarchy`, `/admin/network-integrity` to the corresponding `/devops/*` routes. The handlers stay the same; the URL changes. Sidebar updates to point to `/devops/*`.

**Gate to Phase 4:** All 10 P0 services have `/devops/<service>` pages live; all 5 tier flags default-on for ≥7 days; `/admin/*` redirect cleanly; per-tier health rollups render in `/devops/observability`. No regressions. Commit + push.

### Phase 4 — P1 services + hard enforcement (~3 weeks + 3 days, ~30 tickets)

**Track A: P1 service UI (22 services × 1 ticket each = 22 tickets)**

Build the canonical six-zone page for each P1 service per spec inventory. Same pattern as Phase 3 Track B. Recovery work where applicable.

**Track B: Daily-batch + bulk-window tier infra (3 tickets)**

- T4B.1 Daily-batch tier — cron framework + schedule-adherence tracking
- T4B.2 Bulk-window tier — window-aware dispatcher + completeness check
- T4B.3 Per-tier rate-limit policies

**Track C: Hard enforcement (2 tickets)**

- T4C.1 CI hard-fail on validate errors; route-walk vs manifest mismatch fails the build; tier-mix endpoints rejected at gateway boot
- T4C.2 Pre-commit hook runs `make manifest` locally

**Gate to Phase 5 (optional P2 polish):** All P1 services live; hard enforcement on; drift impossible; `make manifest` runs in pre-commit hook. Commit + push.

### Phase 5 — P2 polish (~1 week, ~5 tickets, optional)

5 P2 services + remaining nice-to-haves. Build only if priorities warrant. Most P2 services are blocked on GRO-769/770 (identity middleware + admin module); revisit when those land.

---

## Per-Ticket Lifecycle

For each ticket in any phase, follow this exact sequence:

### 1. Pick up

- Linear: `save_issue` → state `In Progress` (state id `bf1984d9-ca85-4030-9548-97bbee727381`). Confirm parent epic is set.
- Linear: `save_comment` with pickup confirmation, branch name, planned scope. ≤200 words. Same shape as W5/W6/W8/W9/W10/W11 pickup comments.

### 2. Read substrate

For T3B.X (P0 service ports): read the Python source at `~/GrowDirect/Canary/canary/services/<dir>/` and `~/GrowDirect/Canary/canary/blueprints/<file>.py`. Catalog the operator workflow before porting.

For Track A (tier middleware): read `cmd/gateway/main.go` and the spec §"Per-tier infrastructure" carefully. The middleware swap is a structural refactor.

For T2.X (manifest backfill): read the existing `internal/<service>/handler.go` to enumerate routes, then write the markdown row.

### 3. Plan

Write a tight plan to `docs/superpowers/plans/2026-05-07-<ticket-slug>.md` for any ticket > 200 LOC of expected change. Smaller tickets can skip the plan. The W6/W5 plans are the reference.

### 4. Implement

Follow established patterns:
- New handlers go in sharded files: `internal/web/handler_devops_<service>.go` (precedent: `handler_w5.go`, `handler_w11.go`).
- New templates land under `internal/web/templates/devops/<service>/*.html`.
- Use the existing design language: `ops-card`, `page-header`, period pills, badge styles. Don't invent new visuals.
- New `Deps` fields are nil-safe with empty-state path.
- All POST handlers redirect with `?flash=<verb>` and 303 status (W5 pattern).
- Sidebar updates land in `internal/web/templates/partials/sidebar.html`.
- `cmd/gateway/main.go` wires new stores inside the existing `webDeps := web.Deps{...}` literal.
- New migrations only if the spec explicitly calls for them. The wallet ticket (T3B.6) is the only known case.

### 5. Test

Every new handler needs at minimum:
- A no-store empty-state test (`Deps{}` with relevant field nil)
- A 303-redirect contract test for any POST handler
- For complex GET handlers, a status/filter selector test (W6 period selector pattern)

Run before commit:
```
DATABASE_URL="postgres://growdirect:growdirect_dev@localhost:5432/canary_gcp_test?sslmode=disable" \
VALKEY_URL=redis://:valkey_dev@localhost:6379/2 \
SESSION_SECRET="test-session-secret-at-least-32-bytes!" \
go test ./...
```

`go vet ./...` clean. `go build ./...` clean.

For tier middleware tickets (T3A.X): integration test against `canary_gcp_test` exercising the full flag-on path.

### 6. Commit + push + close

- Single commit (or 2–3 if substrate writes + portal wiring are clearly separate). Subject: `feat(scope): <verb> — <ticket-id>`. Always include `Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>`.
- `git push` (no `--force`).
- Linear: `save_comment` with the artifact comment in the same shape as W5/W6 closeouts (Done summary table + files + tests + plan link + scope-cut). Then `save_issue` → state `Done` (state id `d6795b15-1452-4b57-92f3-ac36c566b66e`).
- Move on to the next ticket. Do not stop to summarize the batch unless you've hit a phase Gate.

---

## Quality Gates (must hold per ticket)

- `go test ./...` exits 0; all packages report `ok`
- `go vet ./...` clean
- `go build ./...` clean
- `make manifest` exits clean; no new validation errors introduced
- New routes pass `tenantIDFromCtx` for tenant-scoped services; cross-tenant services skip the tenant filter
- New POST handlers parse forms, redirect with `flash=`, never 500 on missing dep
- No new top-level deps without sign-off
- Sidebar updated where the new surface is operator-facing
- Phase Gate criteria met before advancing

---

## Reference Patterns (cheat sheet)

**Service detail page handler skeleton** (use as starting point for `handler_devops_<service>.go`):

```go
package devops

func (h *Handler) <foo>Page(w http.ResponseWriter, r *http.Request) {
    view := map[string]any{
        "Service":    serviceFromManifest("<name>"),  // header data
        "Capability": capabilityFromManifest("<name>"),
        "KPIs":       nil,
        "Endpoints":  nil,
        "Activity":   nil,
        "LinkedTo":   nil,
        "Flash":      r.URL.Query().Get("flash"),
    }
    if h.deps.<X>Store != nil {
        // Fill view with real data per spec §"Service-detail-page common shape"
    }
    h.render(w, r, "devops_<name>", "devops", view)
}
```

**Manifest entry skeleton** (for adding a service to `Brain/wiki/canary-go-portal.md`):

```markdown
## <name> · :<port> · <category> · <P0|P1|P2>

Owner: <agent>  ·  Card: Brain/wiki/cards/<name>.md  ·  Cells: [<axis> × <tier>] [<axis> × <tier>]
<scope: cross-tenant | tenant-scoped | both>  ·  Python prior art: <path or "none">

| Endpoint | Method | Tier | Axis | Auth | Status | Notes |
|----------|--------|------|------|------|--------|-------|
| /v1/<name>/<route> | <METHOD> | <tier> | <axis> | <auth> | mounted | <one line> |
```

**Test pattern** (see `internal/web/handler_w5_test.go`, `handler_w6_test.go` for full examples):

```go
func Test<Foo>_NoStore_RendersEmptyState(t *testing.T) {
    h := New(Deps{}, nil); r := chi.NewRouter(); h.Mount(r)
    req := httptest.NewRequest(http.MethodGet, "/devops/<path>", nil)
    rr := httptest.NewRecorder(); r.ServeHTTP(rr, req)
    if rr.Code != http.StatusOK { t.Fatalf("expected 200 got %d", rr.Code) }
    for _, want := range []string{"<expected>"} {
        if !strings.Contains(rr.Body.String(), want) { t.Errorf("body missing %q", want) }
    }
}
```

---

## Standing Constraints

- **Build, don't organize.** Ship a service per ticket. Don't refactor unrelated code.
- **Code is ahead of SDDs.** Use `Brain/wiki/cards/` (capability cards) as the spec surface, not `docs/sdds/go-handoff/`.
- **No hand-rolling outside core IP.** If a "Done when" line implies generic infra (auth, cache, queue), use what's wired.
- **No volatile data in wiki.** Counts, stats, timestamps belong in DB. Markdown captures structure, decisions, contracts.
- **Stop overproducing artifacts.** Per ticket: a single commit + a Linear comment. The brainstorm visuals exist; don't recreate them.
- **Professional tone.** Direct in commit messages and Linear comments. No casual energy. No hype phrasing.
- **Don't extend the Python `Canary/` directory.** It's research source only. Frozen.
- **Phase Gates are real.** Don't advance to Phase N+1 if Phase N's Gate isn't met. Surface to user instead.

---

## Memory Bus (optional, not required)

`memory-bus` MCP at `http://127.0.0.1:8003/mcp` — semantic search over Brain wiki + SDDs. Use `memory_recall("manifest schema")` or `memory_recall("cadence ladder")` if you need ground truth and grep isn't surfacing it. Don't make it a primary source — read files directly when you can.

If the memory bus is down, that's not a block. Continue.

---

## Exit Conditions

You're done when one of these is true:

1. **All four phases shipped.** Post a summary comment on the umbrella epic listing every ticket closed, total LOC delivered, all Gates passed. Move umbrella status → Done. Exit.
2. **You hit a hard block on a ticket.** Leave it `In Progress` with a block comment, do not pick up the next ticket, exit. User picks it up.
3. **A Phase Gate fails.** Stop, comment on the umbrella epic with what's blocking the Gate, exit. Do not advance.
4. **A safety rule trips.** If you're about to do something that isn't authorized above (open PR to main, modify CI, install new dep, refactor unrelated code), stop and ask. Do not work around the rule.

When you exit cleanly, output a single short message that:
- Names the active phase + tickets closed this run (with GRO links)
- Names tickets remaining in the active phase + what blocks the Gate (if any)
- Names the branch tip SHA

That's the deliverable. The user reads Linear comments, reviews the diff at their pace, merges (or asks for changes) outside this loop.
