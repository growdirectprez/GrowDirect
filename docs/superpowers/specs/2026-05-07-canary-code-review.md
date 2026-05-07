# CanaryGo — Code Health Audit (sprint 2 input)

## Executive summary

CanaryGo at 67k lines across 328 Go files builds and `vet`s clean — there is no signal noise to wade through, which is rare for a codebase moving at this clip. The shape of the problem is concentrated, not diffuse. Three themes dominate. **First, the merchant UI under `internal/web/` is operationally unsafe**: the entire module ships with no auth (`tenantIDFromCtx` always returns `uuid.Nil`, `merchantIDFromCtx` reads from URL query/form), 15+ POST mutations have no CSRF or body-size limits, and a duplicate route registration silently shadows a real handler with a stub. **Second, the test corpus has a category error**: 65 "unit tests" in `internal/web/` and `internal/lp/` connect to a real database via `testutil.MustConnect`, fail under bare `go test ./...`, and lack the `//go:build integration` tag the conventions doc mandates. **Third, `internal/web/handler.go` is a 3,423-line / 97-function fat handler** that absorbs every new W-series wave; W16 was wired inline rather than getting its own file like W5/W8/W10/W11/W13/W14/W15. **If you only read one section, read the P0 list** — the four findings there are pre-merge tenant-isolation hazards that compound each other.

## Findings by severity

### P0 (4)

#### Web UI runs with no tenant isolation

- **Location**: `internal/web/handler.go:3418-3423` (`tenantIDFromCtx`); `internal/web/handler.go:27` (docstring)
- **Evidence**:
  ```go
  // tenantIDFromCtx extracts the tenant UUID from the request context.
  // Returns uuid.Nil until auth middleware (GRO-769) is wired.
  func tenantIDFromCtx(ctx context.Context) uuid.UUID {
      // TODO(GRO-769): replace with identity.TenantIDFromCtx(ctx)
      return uuid.Nil
  }
  ```
  Called from 30+ handler sites for tenant-scoped reads (transactions, alerts, items, employees, etc.). Comment at line 27: "Auth: placeholder — all routes are open until the identity middleware is wired (GRO-769)."
- **Risk**: With production data loaded, every web request reads as the null tenant — either silently returning empty results (best case) or returning every row in the table (worst case, depending on per-store query semantics).
- **Remediation**: Land GRO-769 identity middleware before any tenant onboards beyond demo. Gate all `internal/web/` routes behind the middleware in `cmd/gateway/main.go` instead of mounting on the root router.
- **Sprint estimate**: M

#### Tenant ID readable from URL query parameter

- **Location**: `internal/web/handler_w10.go:37-47`
- **Evidence**:
  ```go
  func merchantIDFromCtx(_ http.ResponseWriter, r *http.Request) uuid.UUID {
      v := r.URL.Query().Get("merchant_id")
      if v == "" {
          return uuid.Nil
      }
      id, err := uuid.Parse(v)
      if err != nil {
          return uuid.Nil
      }
      return id
  }
  ```
  Used by `adminHierarchyPage`, `adminHierarchyCreate`, `adminNetworkIntegrityPage`, `dashboardsCrossStorePage`, `suppliersListPage`, `suppliersCreate`, `poListPage`, `poCreate`, `poDetailPage`, `poStatusAction`, `poMatchPage`.
- **Risk**: `?merchant_id=<any-uuid>` lets an unauthenticated caller read or create rows for any merchant. The POST handlers (`adminHierarchyCreate`, `suppliersCreate`, `poCreate`, `poStatusAction`) write rows under whatever merchant_id is supplied.
- **Remediation**: Delete this helper. Fold merchant resolution into the same identity middleware as P0 #1 — read from the authenticated session/JWT, never from the request body or query string.
- **Sprint estimate**: S (deletion); M (depends on identity middleware)

#### POST mutations have no CSRF protection

- **Location**: 15+ routes mounted in `internal/web/handler.go:281-408`; only `internal/squareauth/` implements CSRF state
- **Evidence**: Routes include `r.Post("/cases/hawk", ...)`, `r.Post("/admin/hierarchy", ...)`, `r.Post("/po", ...)`, `r.Post("/po/{id}/status", ...)`, `r.Post("/orders/suggested/{id}/approve", ...)`, etc. Search for `csrf|CSRF` returns hits only in `internal/squareauth/handler.go` and `internal/squareauth/squareauth.go`.
- **Risk**: Once auth ships and these routes are session-protected, any cross-origin form submit creates POs, locks OTB budgets, approves suggested orders, opens cases, etc. against the victim's session.
- **Remediation**: Add a CSRF middleware wrapping the merchant UI route group in `cmd/gateway/main.go`. Either gorilla/csrf or chi's recommended approach (double-submit cookie + form token).
- **Sprint estimate**: M

#### Duplicate route registration silently disables the real `/reports/category` handler

- **Location**: `internal/web/handler.go:316-319`
- **Evidence**:
  ```go
  r.Get("/reports/category", h.reportCategoryPage)
  r.Get("/reports/category", h.page("reports", "report_category", func(_ *http.Request) any {
      return map[string]any{"TotalCategories": 0, "TopCategory": "—", "AvgMargin": "—", "SKUsTracked": 0, "Categories": nil}
  }))
  ```
  Chi v5's `tree.InsertRoute` calls `setEndpoint` which silently overwrites — the second registration wins. The real handler at `internal/web/handler.go:2192-2280` (which actually queries `ItemStore.ListCategories` + `ItemStore.List` and aggregates) is dead on the wire.
- **Risk**: `/reports/category` always renders empty stats regardless of seeded data. A reviewer testing the page sees zeroes and assumes the handler is unwired; the real handler quietly rots.
- **Remediation**: Delete line 317-319 stub registration. The real handler at line 316 already returns the correct shape with empty fallbacks via `h.deps.ItemStore == nil` guard.
- **Sprint estimate**: S

### P1 (6)

#### `handler.go` is a 3,423-line fat handler with 97 functions

- **Location**: `internal/web/handler.go` (whole file)
- **Evidence**: 97 functions including 50+ page handlers, plus the entire W16 cross-domain case management flow (`exceptionDetailPage`, `casesNewPage`, `casesEvidencePage`, `casesCorrelationPage`, `casesRemediatePage`) inlined at lines 3184-3415. Every other recent W-series wave (W5/W8/W9/W10/W11/W13/W14/W15) sits in its own `handler_wN.go` file.
- **Risk**: Single-file diff conflicts every time someone touches the merchant UI. Hard to find handlers; hard to test in isolation; reviewer fatigue.
- **Remediation**: Extract `handler_w16.go` for the W16 cases capstone. Consider further splits by domain: `handler_inventory.go`, `handler_reports.go`, `handler_settings.go`. The `Mount()` method already has the partition lines — the section comments (`// Hawk case management`, `// Customer investigator`) map directly to file boundaries.
- **Sprint estimate**: M

#### 65 "unit tests" in `internal/web/` and `internal/lp/` are integration tests in disguise

- **Location**: 58 calls to `testutil.MustConnect` in `internal/web/handler_*_test.go` + 7 in `internal/lp/*_test.go`; convention at `docs/conventions.md:144-152`
- **Evidence**:
  ```go
  // internal/testutil/db.go:14-19
  func MustConnect(t *testing.T) *pgxpool.Pool {
      t.Helper()
      url := os.Getenv("DATABASE_URL")
      if url == "" {
          t.Fatal("testutil: DATABASE_URL not set — run tests via 'make test'")
      }
  ```
  `go test ./...` from a clean checkout produces 40+ web failures and 7 lp failures with `DATABASE_URL not set — run tests via 'make test'`. None of those test files have `//go:build integration` (the convention applied correctly to `internal/fox/integration_test.go`, `internal/owl/integration_test.go`, etc.).
- **Risk**: CI either runs `go test ./...` and these all fail (current behavior), or it special-cases `make test` and a future contributor expecting `go test ./...` to be the gate is left holding a broken build. Conventions drift erodes trust in the test suite.
- **Remediation**: Add `//go:build integration` tags to all `internal/web/handler_*_test.go` and `internal/lp/*_test.go` files. Migrate them off `DATABASE_URL` onto `GATEWAY_TEST_DATABASE_URL` to align with the rest. Update `Makefile` to build-tag select. Or — better — add table-driven nil-store tests so the handler-level tests run unit-clean and exercise the empty-state codepaths.
- **Sprint estimate**: M

#### Per-request argon2 scan over every active API key

- **Location**: `internal/identity/apikey.go:144-176`
- **Evidence**:
  ```go
  const q = `
      SELECT id, tenant_id, agent_name, key_hash, scopes, status, expires_at
        FROM app.api_keys
       WHERE status = 'active'
         AND (expires_at IS NULL OR expires_at > now())`
  rows, err := pool.Query(ctx, q)
  // ...
  for rows.Next() {
      // scan, then VerifyAPIKey() — argon2id verify per row
  }
  ```
  Comment at line 142-143 acknowledges it: "For dev/test scale this is fine; production scale gets a per-prefix sharding optimization when key counts cross 10⁴ per tenant."
- **Risk**: The MCP endpoint (`POST /mcp` on the gateway) is API-key gated. Every tool call hits this. Argon2id is intentionally slow (~50-200ms per verify); at 100 active keys that's 5-20 seconds of CPU per auth. The MCP discovery doc advertises 28 tools — partner agents will call this surface in tight loops.
- **Remediation**: Two options. Cheap: add a key prefix column (first 8 chars of plaintext, indexed) and filter the candidate set to ≤1 row per prefix. Better: switch to a per-key derivation where `prefix → key_id` is a unique lookup, then verify a single hash.
- **Sprint estimate**: M

#### Handler POST endpoints lack `MaxBytesReader`

- **Location**: All 15 POST handlers in `internal/web/handler*.go` (vs `internal/casemgmt/handler.go:45`, `internal/transaction/handler.go:51,190,222`, `cmd/identity/handlers.go:138` which do limit)
- **Evidence**: `internal/web/handler_w10.go:99` calls `r.ParseForm()` directly with no body cap; `handler_w11.go:223,299`, `handler_w5.go` all the same. By contrast `internal/casemgmt/handler.go:45` reads with `http.MaxBytesReader(w, r.Body, 1<<16)`.
- **Risk**: A 1GB POST body exhausts gateway memory before any application logic runs. Form parsing reads the entire body into memory.
- **Remediation**: Add a 1<<16 (64KB) `MaxBytesReader` wrapper to every POST handler in `internal/web/`, or better, install a chi middleware that caps body size for the whole web group.
- **Sprint estimate**: S

#### `reportCategoryPage` aggregates over a 500-row truncation

- **Location**: `internal/web/handler.go:2209`
- **Evidence**:
  ```go
  items, err := h.deps.ItemStore.List(ctx, item.ListFilters{TenantID: tenantID, Limit: 500})
  ```
  Followed by an in-memory bucket aggregation at lines 2222-2236 that sums per-category margin into a `map[uuid.UUID]*bucket`.
- **Risk**: For tenants with >500 items, the aggregate is silently incomplete — users see "TopCategory" computed from a bounded subset, no warning. (Currently moot because of the P0 #4 stub-shadow bug, but once that's fixed this becomes user-visible.)
- **Remediation**: Push the aggregation into SQL: `SELECT category_id, COUNT(*), AVG(...) FROM app.items WHERE tenant_id = $1 GROUP BY category_id`. Add an `ItemStore.AggregateByCategory(ctx, tenantID)` method.
- **Sprint estimate**: S

#### Dockerfile Go version drift

- **Location**: `deploy/Dockerfile.gateway:15`, `deploy/Dockerfile.dbcheck:4`, `deploy/Dockerfile.identity:2`, `deploy/Dockerfile.hello:4`
- **Evidence**: All four Dockerfiles use `FROM golang:1.24-alpine AS builder` while `go.mod` declares `go 1.25.0`. `Dockerfile.gateway` line 17-25 sets `GOTOOLCHAIN=auto` to compensate.
- **Risk**: Builds work because Go downloads the 1.25 toolchain at build time, but the base image bumps mean every image build pulls a fresh toolchain over the network. CI cache layer for `go mod download` invalidates whenever the auto-toolchain decides to refresh. Version-skew bugs are silent.
- **Remediation**: Bump all four Dockerfiles to `FROM golang:1.25-alpine AS builder`. Drop `GOTOOLCHAIN=auto` once aligned (or keep it as a defense-in-depth).
- **Sprint estimate**: S

### P2 (5)

#### CLAUDE.md migration footnote is stale

- **Location**: `CanaryGo/CLAUDE.md:43`
- **Evidence**: "Path: `deploy/migrations/` (flat numbered, 001–014 for M1)". The actual `deploy/migrations/` directory contains 019-030 only; 001-018 are in `_archived/`. The declarative `deploy/schema/00_*.sql` through `12_*.sql` are now the foundation.
- **Risk**: A new contributor follows CLAUDE.md, runs `migrate up` against a clean DB, and gets nothing because there's no 001-018 to apply. They have to discover `make db-reset` separately.
- **Remediation**: Update CLAUDE.md migration section to describe the actual two-tier model: `deploy/schema/` declarative (source of truth, applied by `make db-reset`) + `deploy/migrations/019+` incremental (applied by `make migrate-up` to live envs).
- **Sprint estimate**: S

#### Four unused stub functions in `handler.go`

- **Location**: `internal/web/handler.go:2807,2815,2841,2861`
- **Evidence**: `stubChirps`, `stubAlerts`, `stubRules`, `stubHawkList` are defined but referenced nowhere. Confirmed by `grep -rn "stubChirps\|stubAlerts\|stubRules\|stubHawkList" --include="*.go"` — only the definitions match. Real handlers replaced them: `chirpListPage`, `alertListPage`, `rulesListPage`, `hawkListPage`.
- **Risk**: Dead code. Maintainers grep for "stub" and find handlers that look unwired but aren't.
- **Remediation**: Delete all four. ~25 lines.
- **Sprint estimate**: S

#### `internal/ecom` defines an interface and DTO surface no implementation references

- **Location**: `internal/ecom/ecom.go:35-69`
- **Evidence**: `ecom.Adapter` (5-method interface), `ecom.Order` (DTO with 8 fields), `ecom.ChannelHealth` (DTO with 5 fields) defined but unreferenced. Only `ecom.Channel` (4-field static) and `ecom.Registry()` are used, by `internal/web/handler_w15.go`. No `internal/ecom/shopify/`, `internal/ecom/bigcommerce/`, etc. exist yet.
- **Risk**: Speculative scaffolding. The interface shape may not survive contact with a real adapter; freezing it now adds drag.
- **Remediation**: Strip the file down to the registry + `Channel` struct. Re-add the interface when the first adapter ships and the contract is informed by reality.
- **Sprint estimate**: S

#### `routewalk.Output.GeneratedAt` directly contradicts the no-timestamp convention in the same epic

- **Location**: `internal/manifest/routewalk/routewalk.go:40,80`; `internal/web/devops/devops.go:36-38`
- **Evidence**: `routewalk.go` writes `GeneratedAt: time.Now().UTC().Format(time.RFC3339)`. `devops.go` lines 36-38 in the sibling sysadmin module: "Deliberately no GeneratedAt field — the catalog is content-addressable… Including a wall-clock timestamp causes git churn on every `make manifest` run." Both are part of the GRO-836 sysadmin epic.
- **Risk**: If `build/routes-seen.json` is ever committed (it's not in `.gitignore`), every `MANIFEST_ROUTEWALK=1` boot churns the diff.
- **Remediation**: Either add `build/` to `.gitignore` (cheapest) or drop `GeneratedAt` from `Output` to align with the catalog convention.
- **Sprint estimate**: S

#### `internal/po/store.go` has no transactional PO+lines write

- **Location**: `internal/po/store.go` (whole file, 222 lines)
- **Evidence**: Contains `Create`, `List`, `Get`, `UpdateStatus`, `ListLines` but no method that writes a PO and its lines together. `grep -c "Begin\|tx\." internal/po/store.go` returns 0. The CanaryGo CLAUDE.md sqlc rule says "Complex writes (multi-statement tx, cross-table, ≥3 callers): SHOULD use sqlc."
- **Risk**: When PO + lines need to land atomically (3-way match flow), there's no API. Today's `poCreate` handler in `handler_w11.go:217-252` only writes the PO; lines never get inserted.
- **Remediation**: Add `Store.CreateWithLines(ctx, req, lines)` wrapped in `pool.BeginTx` once line UI lands. Once it crosses 3 callers, define it in `internal/db/sqlc/po.sql` per the convention.
- **Sprint estimate**: M

### P3 (5)

#### `.env.example` documents 8 vars; code references 30

- **Location**: `CanaryGo/.env.example` (8 lines of vars); search `grep -rn "os.Getenv" --include="*.go" | grep -v _test.go` returns 42 sites across 30 unique env vars
- **Evidence**: `.env.example` covers `LANGGRAPH_URL`, `SQUARE_*`, `DATABASE_URL`, `VALKEY_URL`, `DEV_CONSOLE`, `SECRET_BACKEND`. Code also uses `CANARY_ENCRYPTION_KEY`, `IDENTITY_JWKS_*`, `IDENTITY_JWT_*`, `LNURL_*`, `MANIFEST_ROUTEWALK*`, `ORDINALSBOT_API_KEY`, `OTEL_*`, `VALIDATOR_*`, `GCP_PROJECT_ID`, `SECRET_BACKEND_REQUIRE_SM`, `SUBJECTS_RESOLVE_MODE`, `ENV`.
- **Risk**: New developer copies `.env.example`, can't boot the gateway because `INTERNAL_SERVICE_SECRET` and `SESSION_SECRET` (both `require()`d in `config.go:25-29`) aren't even mentioned.
- **Remediation**: Sweep `.env.example` to cover all 30 vars with sensible dev defaults. Group by subsystem.
- **Sprint estimate**: S

#### 21 `TODO/FIXME` markers in production paths

- **Location**: 21 instances across `internal/web/handler.go`, `internal/web/devops/devops.go` (10 of them), `internal/db/types/ledger.go`, `internal/db/types/l.go`, `internal/db/types/m.go`
- **Evidence**: `internal/db/types/ledger.go:34,55,70` all carry "tstzrange — string with TODO: tstzrange-aware type for Loop 3"; `internal/db/types/l.go:51,74` carry "ltree — string with TODO: ltree-aware type for Loop 3". Loop 3 is referenced as if it's a known phase; no Loop 3 ticket is currently open in the dispatch board.
- **Risk**: Tracker rot — the TODO comment is now the only record. If "Loop 3" ever lands, no one will know to come back to these strings.
- **Remediation**: File a Linear dispatch for "tstzrange + ltree typed-shim retrofit (Loop 3 cleanup)" and reference its GRO ID inline. Promote the TODO to a tracked ticket.
- **Sprint estimate**: S

#### Type ambiguity in `Deps` between optional pointer and interface

- **Location**: `internal/web/deps.go:30-90`
- **Evidence**: Mixed nil-shape: `*alert.Store`, `chirp.Store` (interface), `validate.ValidationStore` (interface), `pricing.Store` (interface), `item.Store` (interface), `*casemgmt.Store`, etc. Comment at line 29 says "Each field is optional (nil = use stub data for that domain)" but the nil check semantics differ between pointer and interface (nil-typed vs nil interface).
- **Risk**: An interface assigned with a typed-nil concrete (`var s *foo.Store; deps.Field = s`) compares as `!= nil`. Today the constructors all return concrete pointers (no typed-nil hazard) but the inconsistency is a future footgun.
- **Remediation**: Pick one — interfaces everywhere (better for testability, lets stubs swap in) or pointers everywhere. Document the choice.
- **Sprint estimate**: M

#### Detail page short-IDs depend on UUID string length

- **Location**: `internal/web/handler_w10.go:77,162`; `internal/web/handler_w11.go` line ~263 etc.
- **Evidence**: `parent = n.ParentID.String()[:8]` and similar at multiple sites. UUID string is always 36 chars, so the slice is safe — but the pattern is brittle.
- **Risk**: A future ID format change (custom prefix, shorter scheme) panics on a substring index.
- **Remediation**: Extract `func shortID(id uuid.UUID) string` once and reuse. `handler.go` already has `shortHex(s string, n int)` (line 1965) — promote it.
- **Sprint estimate**: S

#### `gateway` binary committed in worktree (not tracked)

- **Location**: `CanaryGo/gateway` (40MB)
- **Evidence**: `ls -la` shows a 40,938,978-byte `gateway` executable in the repo root. `git ls-files | grep gateway` confirms it's not tracked, and `.gitignore` lists `/gateway`.
- **Risk**: None to git; some to disk. If a worktree-cleanup script ever runs `git clean`, it removes this. Mostly noise.
- **Remediation**: Local-only artifact; leave alone.
- **Sprint estimate**: N/A (no action)

## Themes / patterns

**Theme 1 — Auth shipped last, not first.** The merchant UI was built end-to-end (16 W-series waves, 200+ routes) without the identity middleware (GRO-769) that gates it. The placeholder helpers `tenantIDFromCtx` (returns `uuid.Nil`) and `merchantIDFromCtx` (reads from URL) were sized as "we'll fix this when GRO-769 lands" but they've now been baked into 30+ handlers. The recovery path is straightforward — land GRO-769 and the placeholders evaporate — but the longer the UI runs in this state, the more handlers accrete with the wrong tenant-resolution shape. P0 #1 + P0 #2 are the same root cause.

**Theme 2 — Test classification has drifted from convention.** `docs/conventions.md` lays out a clean three-tier model: unit tests (table-driven, no DB), integration tests (`//go:build integration` + `GATEWAY_TEST_DATABASE_URL`), Tier-3 (excluded by tag). Most service domains follow this — `internal/fox/`, `internal/owl/`, `internal/inventory/`, `internal/protocol/*` all properly tag their integration tests. But `internal/web/` and `internal/lp/` keep `testutil.MustConnect` with no tag, so they fail under bare `go test ./...` while looking like unit tests. The recent W-series handlers add to this bucket every wave. Either the W-series authors didn't read the convention or chose to skip it for speed; either way, it's now a recognisable pattern.

**Theme 3 — `handler.go` is the absorbent.** Every recent W-series wave got its own `handler_wN.go` file *except* W16 — and W16 happens to be the most complex (cross-domain case management with evidence aggregation, correlation, remediation). The split discipline broke at exactly the wrong dispatch. The same file also carries dead stub functions (`stubChirps`, `stubAlerts`, `stubRules`, `stubHawkList`) and the duplicate-route bug. These three smells share a cause: one giant file is too easy to add to and too hard to clean. It's not a critical defect on its own, but every successive sprint that doesn't address it makes the next sprint slower.

**Theme 4 — Convention vs implementation drift in three places.** `CLAUDE.md` advertises migrations 001-014 (actually archived); `routewalk` emits `generated_at` while the sister sysadmin module declares timestamps verboten; sqlc convention says complex writes "SHOULD use sqlc" but only 3 services (identity/transaction/tsp) actually do. None individually are critical — together they suggest the convention docs are aspirational rather than enforced. A linter pass for "files matching `_test.go` that import `testutil` must have a build tag" would have caught Theme 2.

**Theme 5 — Defense-in-depth gaps that compound.** P0 (no auth) + P0 (no CSRF) + P1 (no body size limit) + P1 (slow argon2 scan) collectively turn the gateway into a target. None alone is fatal; together they say "this surface was built optimising for build speed, not for the day a real request hits it." Sprint 2 should treat these as a unit, not as four separate cleanups.

## Sprint-2 ticket-shape recommendations

1. **Land GRO-769 identity middleware + retire placeholder tenant helpers**
   - Scope: Wire `identity.TenantIDFromCtx` into the gateway web route group. Replace `tenantIDFromCtx` (handler.go:3418) and `merchantIDFromCtx` (handler_w10.go:37) with the real middleware extractor. Delete URL-query merchant_id reading.
   - Effort: M
   - Files: `cmd/gateway/main.go`, `internal/web/handler.go`, `internal/web/handler_w10.go`, all callers of those two helpers
   - Closes: P0 #1, P0 #2

2. **CSRF + MaxBytesReader middleware for the merchant UI route group**
   - Scope: Add a chi middleware group that wraps all `internal/web/` POST routes with CSRF (double-submit cookie or gorilla/csrf) and 64KB body cap. Decision in an ADR for which lib.
   - Effort: M
   - Files: `cmd/gateway/main.go`, new `internal/web/middleware.go`, every POST handler test
   - Closes: P0 #3, P1 #4

3. **Delete stub-shadow + dead stubs + W16 file extraction**
   - Scope: Remove duplicate `/reports/category` registration (handler.go:317-319). Delete `stubChirps`, `stubAlerts`, `stubRules`, `stubHawkList`. Move W16 case-management handlers (handler.go:3184-3415) into `internal/web/handler_w16.go`.
   - Effort: S
   - Files: `internal/web/handler.go`, new `internal/web/handler_w16.go`
   - Closes: P0 #4, P2 #2, P1 #1 (partial)

4. **Tag integration-shaped tests properly**
   - Scope: Add `//go:build integration` to all 65 `testutil.MustConnect` test files in `internal/web/` and `internal/lp/`. Migrate from `DATABASE_URL` to `GATEWAY_TEST_DATABASE_URL` to align with the rest of the integration corpus.
   - Effort: M
   - Files: `internal/web/handler_*_test.go` (15 files), `internal/lp/*_test.go` (~5 files), `internal/testutil/db.go`, `Makefile`, `docs/conventions.md`
   - Closes: P1 #2

5. **API key lookup — prefix-indexed verification**
   - Scope: Add a `key_prefix` column to `app.api_keys` (migration 031), populate on creation, index it. Change `AuthenticateAPIKey` to `WHERE key_prefix = $1` filter so each request runs at most one argon2id verify.
   - Effort: M
   - Files: `deploy/migrations/031_api_key_prefix.{up,down}.sql`, `internal/identity/apikey.go`, `cmd/identity/handlers.go`
   - Closes: P1 #3

6. **Dockerfile Go version sweep**
   - Scope: Bump all four Dockerfiles from `golang:1.24-alpine` to `golang:1.25-alpine`. Drop `GOTOOLCHAIN=auto` once verified.
   - Effort: S
   - Files: `deploy/Dockerfile.gateway`, `deploy/Dockerfile.dbcheck`, `deploy/Dockerfile.identity`, `deploy/Dockerfile.hello`
   - Closes: P1 #6

7. **`.env.example` + CLAUDE.md sweep**
   - Scope: Update `.env.example` to cover all 30 referenced env vars with dev defaults. Update `CanaryGo/CLAUDE.md` to describe the actual two-tier migration model (declarative schema + 019+ incremental).
   - Effort: S
   - Files: `CanaryGo/.env.example`, `CanaryGo/CLAUDE.md`
   - Closes: P3 #1, P2 #1

8. **`reportCategoryPage` SQL aggregation**
   - Scope: Add `ItemStore.AggregateByCategory(ctx, tenantID)` that returns per-category counts + avg margin in one query. Replace the 500-row truncated in-memory aggregate.
   - Effort: S
   - Files: `internal/item/store.go`, `internal/web/handler.go:2192-2280`, item store tests
   - Closes: P1 #5

9. **Trim `internal/ecom` to the parts actually used**
   - Scope: Remove unreferenced `Adapter` interface, `Order`, `ChannelHealth` from `internal/ecom/ecom.go`. Keep `Channel` and `Registry()`. Re-add the interface when the first real adapter ships and the contract is informed by use.
   - Effort: S
   - Files: `internal/ecom/ecom.go`
   - Closes: P2 #3

10. **routewalk timestamp + gitignore**
    - Scope: Add `build/` to `.gitignore`. Optionally drop `GeneratedAt` from `routewalk.Output` to align with the sysadmin module's no-timestamp convention.
    - Effort: S
    - Files: `CanaryGo/.gitignore`, optionally `internal/manifest/routewalk/routewalk.go`
    - Closes: P2 #4

## What I did NOT review

- **Live database schema vs `deploy/schema/*.sql`**: I read the declarative schema files and the 019-030 migrations but did not connect to a running Postgres to compare actual `\d+` output against the SQL. If a migration was applied with `force` after a partial failure, drift is possible.
- **MCP tool flow end-to-end**: I confirmed `cmd/gateway/main.go:152-159` registers 26 tools across 7 modules and that `mcpHandler.Mount(r)` sits behind API-key middleware, but did not trace a single tool call from `POST /mcp` through the registry to a store and back.
- **Triple Subscriber pipeline (Sub1/Sub2/Sub3) protocol correctness**: The Merkle batching and ordinal inscription paths in `internal/protocol/sub3/` are dense; I did not verify the Merkle proof construction matches the L2 anchor format expected downstream.
- **Square OAuth, LNURL, L402 cryptographic correctness**: I noted CSRF state handling exists in `squareauth/` but did not audit signature schemes, token lifetimes, or replay protection.
- **Race conditions in `internal/identity/apikey.go` `last_used_at` goroutine** beyond noting the pattern. The 2s timeout is reasonable but no backpressure if many requests fan out.
- **OpenTelemetry instrumentation completeness** in `internal/obs/`. I confirmed the env vars and that `obs.Logger` is wired in mains, but did not check span coverage on the data path.
- **Cloud Build / Cloud Run deploy scripts** under `deploy/cloud-run/` and `deploy/cloudbuild.gateway.yaml`.
- **Frontend templates** in `internal/web/templates/` (115 `.html` files). I read the parsed-template registration list but did not open the templates themselves to check for XSS/escaping issues. Go's `html/template` is safe by default but custom funcs can break that.
- **`cmd/edge/`** (the binary mentioned as 20th in CLAUDE.md). I noted its presence but did not review the offline-edge architecture.
- **Test coverage by package**. I ran `go test ./...` once and observed pass/fail per package, but did not run with `-cover` to surface percentage. Many `internal/web/handler_*_test.go` are integration-shaped (Finding P1 #2) and skip in unit mode, so apparent coverage of the handler layer is misleading.
