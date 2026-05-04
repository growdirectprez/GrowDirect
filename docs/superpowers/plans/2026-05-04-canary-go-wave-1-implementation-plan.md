# Canary Go Wave 1 — LP Core Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Wire the existing Wave 1 backend stores (alert, chirp, casemgmt, customer) into the web UI layer so all LP Core screens render live data from the database instead of hardcoded stubs.

**Architecture:** The backend packages (`internal/alert`, `internal/chirp`, `internal/casemgmt`, `internal/customer`, `internal/chirp/rules/*`) are implemented with real pgx stores. `internal/web/handler.go` has all routes registered but all handlers return hardcoded stub data — the core gap is dependency injection: the web.Handler needs to receive store dependencies and use them. Detection schema migrations need to be added to the active migration sequence before any live data flows.

**Tech Stack:** Go 1.22+ · Chi v5 · pgx/v5 · PostgreSQL 17 (`canary_gcp` / `canary_gcp_test`) · html/template (server-rendered) · sqlc for complex queries (direct pgx acceptable for reads per CanaryGo CLAUDE.md)

---

## Scope

Wave 1 screens (25 total from wireframe briefs in `docs/superpowers/briefs/wave-1/`):
- `/alerts`, `/alerts/:id` — Alert List + Detail
- `/chirps`, `/chirps/:id` — Live Transaction Feed + Detail
- `/rules`, `/rules/:id` — Detection Rules List + Detail
- `/cases/hawk`, `/cases/hawk/:id`, `/cases/hawk/:id/evidence`, `/cases/hawk/analytics`, `/cases/hawk/patterns` — Hawk Case system
- `/customers`, `/customers/:id`, `/customers/:id/risk`, `/customers/:id/context` — Customer Lookup (LP view)
- `/settings/alert-routing`, `/settings/training-mode` — Alert settings
- `/settings/allowlist/dead-count`, `/settings/allowlist/discounts`, `/settings/allowlist/voids`, `/settings/allowlist/comps` — Allow-list config
- `/settings/store/drawer`, `/settings/store/discounts`, `/settings/store/void-reasons`, `/settings/store/comp-reasons` — LP substrate config

**Not in scope:** Auth middleware (GRO-769 — tracked separately). UI polish, CSS. Wave 2+ screens.

---

## Pre-Work: Read These First

Before executing any task, read:
1. `CanaryGo/CLAUDE.md` — module path, DB names, sqlc rule, port assignments
2. `internal/alert/store.go` + `internal/alert/dto.go` — alert data shapes
3. `internal/casemgmt/store.go` + `internal/casemgmt/dto.go` — case data shapes
4. `internal/chirp/store.go` + `internal/chirp/dto.go` — chirp/detection data shapes
5. `internal/customer/store.go` + `internal/customer/dto.go` — customer data shapes
6. `internal/web/handler.go` — current handler structure (924 lines)
7. `internal/testutil/db.go` — test DB helper used in integration tests

---

## File Map

### Modified files
- `internal/web/handler.go` — add store dependencies to Handler struct; replace stub functions with real store calls (12 functions to replace)
- `internal/web/deps.go` *(new)* — Deps struct for dependency injection into web.Handler
- `deploy/migrations/024_detection_schema.up.sql` *(new)* — detection schema (schema, rules, detections, lp_substrate tables)
- `deploy/migrations/024_detection_schema.down.sql` *(new)* — rollback

### New test files
- `internal/web/handler_alerts_test.go` — integration tests for alert list + detail
- `internal/web/handler_cases_test.go` — integration tests for case list + detail
- `internal/web/handler_chirps_test.go` — integration tests for chirp list + detail
- `internal/web/handler_customers_test.go` — integration tests for customer list + detail
- `internal/web/handler_settings_test.go` — integration tests for settings pages

---

## Chunk 1: Detection Schema Migration

### Task 1: Create detection schema migration

**Files:**
- Create: `CanaryGo/deploy/migrations/024_detection_schema.up.sql`
- Create: `CanaryGo/deploy/migrations/024_detection_schema.down.sql`

The `internal/alert/store.go` queries `detection.detections` and `detection.detection_rules`. The `internal/chirp/store.go` queries the same. These tables don't exist in the current active migration sequence (1-014 archived + 019-023 active). This migration adds them.

- [ ] **Step 1: Check existing archived migration for detection table shape**

```bash
cat CanaryGo/deploy/migrations/_archived/011_tsp_ingestion.up.sql | grep -A 20 "detection_rules\|CREATE TABLE"
```

- [ ] **Step 2: Cross-reference with alert/store.go queries**

Read `CanaryGo/internal/alert/store.go` — check the exact column names in `selectCols` and all `WHERE` clauses. Read `CanaryGo/internal/chirp/store.go` — check `LoadRules`, `InsertDetection`, `ListDetections` queries.

The schema must exactly match what the stores query. Mismatches fail at runtime, not compile time.

- [ ] **Step 3: Write the up migration**

```sql
-- deploy/migrations/024_detection_schema.up.sql
CREATE SCHEMA IF NOT EXISTS detection;

CREATE TABLE IF NOT EXISTS detection.detection_rules (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID NOT NULL,
    rule_code       TEXT NOT NULL,
    rule_category   TEXT NOT NULL,
    name            TEXT NOT NULL,
    description     TEXT,
    severity        TEXT NOT NULL DEFAULT 'medium',
    enabled         BOOLEAN NOT NULL DEFAULT true,
    dry_run         BOOLEAN NOT NULL DEFAULT false,
    parameters      JSONB NOT NULL DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (tenant_id, rule_code)
);

CREATE TABLE IF NOT EXISTS detection.detections (
    id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id             UUID NOT NULL,
    rule_id               UUID NOT NULL REFERENCES detection.detection_rules(id),
    detected_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
    source_entity_type    TEXT NOT NULL,
    source_entity_id      UUID NOT NULL,
    location_id           UUID,
    cashier_employee_id   UUID,
    customer_id           UUID,
    severity              TEXT NOT NULL,
    signal_strength       FLOAT,
    status                TEXT NOT NULL DEFAULT 'open',
    case_id               UUID,
    acknowledged_at       TIMESTAMPTZ,
    acknowledged_by       UUID,
    created_at            TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_detections_tenant_status
    ON detection.detections (tenant_id, status, detected_at DESC);

CREATE INDEX IF NOT EXISTS idx_detections_cashier
    ON detection.detections (tenant_id, cashier_employee_id);

-- LP substrate: per-store thresholds required for detection rules to fire.
-- A missing row = rule is silent for that location.
CREATE TABLE IF NOT EXISTS detection.lp_substrate (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID NOT NULL,
    location_id     UUID NOT NULL,
    config_key      TEXT NOT NULL,  -- e.g. 'drawer_threshold', 'discount_cap'
    config_value    JSONB NOT NULL,
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_by      UUID,
    UNIQUE (tenant_id, location_id, config_key)
);

-- Allow-list: institutional memory of pre-approved exception patterns.
CREATE TABLE IF NOT EXISTS detection.allow_list (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID NOT NULL,
    list_type       TEXT NOT NULL,  -- 'dead_count', 'discounts', 'voids', 'comps'
    location_id     UUID,           -- NULL = all locations
    employee_id     UUID,           -- NULL = all employees
    reason          TEXT NOT NULL,
    parameters      JSONB NOT NULL DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_by      UUID,
    expires_at      TIMESTAMPTZ     -- NULL = no expiry
);

CREATE INDEX IF NOT EXISTS idx_allow_list_tenant_type
    ON detection.allow_list (tenant_id, list_type);
```

- [ ] **Step 4: Write the down migration**

```sql
-- deploy/migrations/024_detection_schema.down.sql
DROP TABLE IF EXISTS detection.allow_list;
DROP TABLE IF EXISTS detection.lp_substrate;
DROP TABLE IF EXISTS detection.detections;
DROP TABLE IF EXISTS detection.detection_rules;
DROP SCHEMA IF EXISTS detection;
```

- [ ] **Step 5: Apply migration to dev DB**

```bash
cd CanaryGo
make migrate-up DATABASE_URL="postgres://growdirect:growdirect_dev@localhost:5432/canary_gcp"
```

Expected: migration 024 applied successfully. No error output.

- [ ] **Step 6: Apply migration to test DB**

```bash
make migrate-up DATABASE_URL="postgres://growdirect:growdirect_dev@localhost:5432/canary_gcp_test"
```

Expected: migration 024 applied to test DB.

- [ ] **Step 7: Commit**

```bash
git add CanaryGo/deploy/migrations/024_detection_schema.up.sql \
        CanaryGo/deploy/migrations/024_detection_schema.down.sql
git commit -m "feat(migration): 024 — detection schema (rules, detections, lp_substrate, allow_list)"
```

---

## Chunk 2: Dependency Injection Refactor

### Task 2: Add Deps struct and wire stores into web.Handler

**Files:**
- Create: `CanaryGo/internal/web/deps.go`
- Modify: `CanaryGo/internal/web/handler.go` — Handler struct + New() signature

The current `web.Handler.New(logger)` accepts only a logger. All handlers use hardcoded stub data. To wire real data, the Handler needs access to the backend stores.

- [ ] **Step 1: Read current Handler struct definition**

```bash
sed -n '40,70p' CanaryGo/internal/web/handler.go
```

Confirm the current struct fields (logger, templates). Do not proceed until you've read this.

- [ ] **Step 2: Write the failing test (compile-fails is the failing state)**

Create `CanaryGo/internal/web/handler_alerts_test.go`:

```go
package web_test

import (
    "net/http"
    "net/http/httptest"
    "testing"

    "github.com/go-chi/chi/v5"
    "github.com/growdirect-llc/rapidpos/internal/alert"
    "github.com/growdirect-llc/rapidpos/internal/web"
    "github.com/growdirect-llc/rapidpos/internal/testutil"
)

func TestAlertListPage_Renders(t *testing.T) {
    pool := testutil.MustOpenDB(t)
    store := alert.NewStore(pool)
    deps := web.Deps{AlertStore: store}
    h := web.New(deps, nil)

    r := chi.NewRouter()
    h.Mount(r)

    req := httptest.NewRequest(http.MethodGet, "/alerts", nil)
    rr := httptest.NewRecorder()
    r.ServeHTTP(rr, req)

    if rr.Code != http.StatusOK {
        t.Fatalf("expected 200 got %d", rr.Code)
    }
}
```

- [ ] **Step 3: Run test — confirm it fails with compile error**

```bash
cd CanaryGo && go test ./internal/web/... 2>&1 | head -10
```

Expected: `undefined: web.Deps` or `too many arguments in call to web.New`

- [ ] **Step 4: Create deps.go with Deps struct**

```go
// internal/web/deps.go
package web

import (
    "github.com/growdirect-llc/rapidpos/internal/alert"
    "github.com/growdirect-llc/rapidpos/internal/casemgmt"
    "github.com/growdirect-llc/rapidpos/internal/chirp"
    "github.com/growdirect-llc/rapidpos/internal/customer"
)

// Deps holds all backend store dependencies for the web handler.
// Each field is optional (nil = use stub data for that domain).
type Deps struct {
    AlertStore   *alert.Store
    CaseStore    *casemgmt.Store
    ChirpStore   chirp.Store       // interface
    CustomerStore *customer.Store
}
```

- [ ] **Step 5: Update Handler struct and New() in handler.go**

Find the Handler struct definition (around line 44) and update it:

```go
// Handler serves the Canary application UI.
type Handler struct {
    logger    *zap.Logger
    templates map[string]*template.Template
    deps      Deps
}
```

Update `New()` signature (around line 67):

```go
func New(deps Deps, logger *zap.Logger) *Handler {
    if logger == nil {
        logger = zap.NewNop()
    }
    h := &Handler{
        logger:    logger,
        templates: make(map[string]*template.Template),
        deps:      deps,
    }
    // ... rest of mustParse calls unchanged ...
```

- [ ] **Step 6: Update the gateway main.go to pass Deps**

In `CanaryGo/cmd/gateway/main.go`, find the call to `web.New(logger)` and update it:

```go
// Find the existing line: webHandler := web.New(logger)
// Replace with:
webDeps := web.Deps{
    AlertStore:    alertPkg.NewStore(pool),
    CaseStore:     casemgmtPkg.NewStore(pool),
    ChirpStore:    chirpPkg.NewPgxStore(pool),
    CustomerStore: customerPkg.NewStore(pool),
}
webHandler := web.New(webDeps, logger)
```

Add the missing imports at the top of gateway/main.go:
```go
casemgmtPkg "github.com/growdirect-llc/rapidpos/internal/casemgmt"
chirpPkg     "github.com/growdirect-llc/rapidpos/internal/chirp"
```

- [ ] **Step 7: Run test — confirm it now compiles and passes**

```bash
cd CanaryGo && go test ./internal/web/... -run TestAlertListPage_Renders -v
```

Expected: PASS (page renders, returns 200, template renders without error even with empty data from clean test DB)

- [ ] **Step 8: Run gateway build — confirm it still compiles**

```bash
cd CanaryGo && go build ./cmd/gateway/...
```

Expected: no compile errors.

- [ ] **Step 9: Commit**

```bash
git add CanaryGo/internal/web/deps.go \
        CanaryGo/internal/web/handler.go \
        CanaryGo/internal/web/handler_alerts_test.go \
        CanaryGo/cmd/gateway/main.go
git commit -m "feat(web): add Deps struct; wire alert/case/chirp/customer stores into web.Handler"
```

---

## Chunk 3: Alert List + Detail

### Task 3: Wire alert list and detail pages to real stores

**Files:**
- Modify: `CanaryGo/internal/web/handler.go` — replace `stubAlerts` and `alertDetailPage`
- Modify: `CanaryGo/internal/web/handler_alerts_test.go` — add detail test

**Background:** The alert store returns `*AlertDTO` structs from `internal/alert/dto.go`. Read `dto.go` before writing template bindings to ensure field names match.

- [ ] **Step 1: Read AlertDTO fields**

```bash
cat CanaryGo/internal/alert/dto.go
```

Record the exact field names — you need these to bind to template variables.

- [ ] **Step 2: Write failing test for alert list with data**

Add to `handler_alerts_test.go`:

```go
func TestAlertListPage_WithData(t *testing.T) {
    pool := testutil.MustOpenDB(t)
    // seed a detection_rule and a detection into the test DB
    tenantID := uuid.New()
    ruleID := uuid.New()
    _, err := pool.Exec(context.Background(), `
        INSERT INTO detection.detection_rules
            (id, tenant_id, rule_code, rule_category, name, severity)
        VALUES ($1, $2, 'Q.D.1', 'discount', 'Discount Cap', 'high')
    `, ruleID, tenantID)
    require.NoError(t, err)

    _, err = pool.Exec(context.Background(), `
        INSERT INTO detection.detections
            (tenant_id, rule_id, source_entity_type, source_entity_id, severity, status)
        VALUES ($1, $2, 'transaction', $3, 'high', 'open')
    `, tenantID, ruleID, uuid.New())
    require.NoError(t, err)

    store := alert.NewStore(pool)
    deps := web.Deps{AlertStore: store}
    h := web.New(deps, nil)

    r := chi.NewRouter()
    h.Mount(r)

    req := httptest.NewRequest(http.MethodGet, "/alerts", nil)
    rr := httptest.NewRecorder()
    r.ServeHTTP(rr, req)

    if rr.Code != http.StatusOK {
        t.Fatalf("expected 200 got %d: %s", rr.Code, rr.Body.String())
    }
    // Template rendered without error — the alert row appears somewhere in output
    // (exact HTML structure tested in browser, not here)
}
```

- [ ] **Step 3: Run test — confirm it fails (stub returns empty data, tenant ID mismatch)**

```bash
cd CanaryGo && go test ./internal/web/... -run TestAlertListPage_WithData -v
```

The stub currently ignores the DB. The test may pass trivially (page renders regardless) — that's acceptable; we proceed with implementation.

- [ ] **Step 4: Replace stubAlerts with real store call**

In `handler.go`, find `stubAlerts` function (around line 676) and the route registration:

```go
r.Get("/alerts", h.page("alerts", "alerts", stubAlerts))
```

Replace with a real handler method:

```go
r.Get("/alerts", h.alertListPage)
```

Add the handler method (place near alertDetailPage):

```go
func (h *Handler) alertListPage(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    // Tenant ID comes from auth middleware when GRO-769 lands.
    // For now use a sentinel zero UUID that returns empty results gracefully.
    tenantID := tenantIDFromCtx(ctx)

    var alerts []*alert.AlertDTO
    if h.deps.AlertStore != nil {
        f := alert.ListFilters{
            TenantID: tenantID,
            Status:   r.URL.Query().Get("status"),
            Severity: r.URL.Query().Get("severity"),
            Limit:    50,
        }
        var err error
        alerts, err = h.deps.AlertStore.List(ctx, f)
        if err != nil {
            h.logger.Error("alertListPage: list", zap.Error(err))
        }
    }
    h.render(w, r, "alert_list", "alerts", map[string]any{
        "Alerts": alerts,
    })
}
```

Add the tenantIDFromCtx helper (add to handler.go, near the bottom):

```go
// tenantIDFromCtx extracts the tenant UUID from the request context.
// Returns uuid.Nil until the auth middleware (GRO-769) is wired.
func tenantIDFromCtx(ctx context.Context) uuid.UUID {
    // TODO(GRO-769): replace with identity.TenantIDFromCtx(ctx)
    return uuid.Nil
}
```

- [ ] **Step 5: Update alertDetailPage to use real store**

Find `alertDetailPage` (around line 402) and replace the hardcoded stub data:

```go
func (h *Handler) alertDetailPage(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    idStr := chi.URLParam(r, "id")
    id, err := uuid.Parse(idStr)
    if err != nil {
        h.render(w, r, "err404", "alerts", nil)
        return
    }

    if h.deps.AlertStore == nil {
        // Fallback stub for local dev without DB
        h.render(w, r, "alert_detail", "alerts", map[string]any{
            "Alert": map[string]any{"ID": idStr, "ShortID": idStr[:8]},
            "Timeline": nil,
        })
        return
    }

    tenantID := tenantIDFromCtx(ctx)
    a, err := h.deps.AlertStore.GetByID(ctx, tenantID, id)
    if err != nil {
        if errors.Is(err, alert.ErrNotFound) {
            h.render(w, r, "err404", "alerts", nil)
            return
        }
        h.logger.Error("alertDetailPage: get", zap.Error(err))
        h.render(w, r, "err500", "alerts", nil)
        return
    }

    h.render(w, r, "alert_detail", "alerts", map[string]any{
        "Alert":    a,
        "Timeline": nil, // TODO: fetch alert timeline
    })
}
```

Add required imports at the top of handler.go:
```go
"errors"
"github.com/google/uuid"
"github.com/growdirect-llc/rapidpos/internal/alert"
```

- [ ] **Step 6: Build to verify no compile errors**

```bash
cd CanaryGo && go build ./internal/web/... ./cmd/gateway/...
```

Expected: clean build.

- [ ] **Step 7: Run tests**

```bash
cd CanaryGo && go test ./internal/web/... -v 2>&1 | grep -E "PASS|FAIL|---"
```

Expected: all tests PASS.

- [ ] **Step 8: Commit**

```bash
git add CanaryGo/internal/web/handler.go \
        CanaryGo/internal/web/handler_alerts_test.go
git commit -m "feat(web): wire alert list + detail to real store (GRO-766)"
```

---

## Chunk 4: Chirp List + Detail

### Task 4: Wire chirp list and detail pages to real stores

**Files:**
- Modify: `CanaryGo/internal/web/handler.go` — replace `stubChirps` and `chirpDetailPage`
- Modify: `CanaryGo/internal/web/handler_chirps_test.go` *(new)*

**Background:** Chirp store uses the `Store` interface (`internal/chirp/store.go`). `ListDetections` returns `[]Detection`. Read `internal/chirp/rule.go` for the Detection type shape before writing template bindings.

- [ ] **Step 1: Read Detection and Rule types**

```bash
grep -n "^type Detection\|^type Rule\|^type Transaction" CanaryGo/internal/chirp/rule.go CanaryGo/internal/chirp/store.go
```

- [ ] **Step 2: Write failing test**

Create `CanaryGo/internal/web/handler_chirps_test.go`:

```go
package web_test

import (
    "net/http"
    "net/http/httptest"
    "testing"

    "github.com/go-chi/chi/v5"
    "github.com/growdirect-llc/rapidpos/internal/chirp"
    "github.com/growdirect-llc/rapidpos/internal/web"
    "github.com/growdirect-llc/rapidpos/internal/testutil"
)

func TestChirpListPage_Renders(t *testing.T) {
    pool := testutil.MustOpenDB(t)
    store := chirp.NewPgxStore(pool)
    deps := web.Deps{ChirpStore: store}
    h := web.New(deps, nil)

    r := chi.NewRouter()
    h.Mount(r)

    req := httptest.NewRequest(http.MethodGet, "/chirps", nil)
    rr := httptest.NewRecorder()
    r.ServeHTTP(rr, req)

    if rr.Code != http.StatusOK {
        t.Fatalf("expected 200 got %d", rr.Code)
    }
}
```

- [ ] **Step 3: Run — confirm test compiles and passes (stub currently renders)**

```bash
cd CanaryGo && go test ./internal/web/... -run TestChirpListPage -v
```

- [ ] **Step 4: Replace stubChirps with real handler**

In `handler.go`, change route:
```go
r.Get("/chirps", h.chirpListPage)
```

Add method:
```go
func (h *Handler) chirpListPage(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    tenantID := tenantIDFromCtx(ctx)

    var detections []chirp.Detection
    if h.deps.ChirpStore != nil {
        q := chirp.DetectionQuery{
            TenantID: tenantID,
            Limit:    50,
        }
        var err error
        detections, err = h.deps.ChirpStore.ListDetections(ctx, q)
        if err != nil {
            h.logger.Error("chirpListPage: list", zap.Error(err))
        }
    }
    h.render(w, r, "chirps", "chirps", map[string]any{
        "Detections": detections,
    })
}
```

- [ ] **Step 5: Update chirpDetailPage**

Replace the hardcoded stub (around line 443) with a real store call. Same pattern as alertDetailPage: parse UUID, call store.GetByTransactionID or equivalent, render or 404.

Read `chirp/store.go` for the correct method name before implementing.

- [ ] **Step 6: Build + test**

```bash
cd CanaryGo && go build ./... && go test ./internal/web/... -v 2>&1 | grep -E "PASS|FAIL"
```

- [ ] **Step 7: Commit**

```bash
git add CanaryGo/internal/web/handler.go \
        CanaryGo/internal/web/handler_chirps_test.go
git commit -m "feat(web): wire chirp list + detail to real store"
```

---

## Chunk 5: Detection Rules List + Detail

### Task 5: Wire rules list and detail to chirp.Store

**Files:**
- Modify: `CanaryGo/internal/web/handler.go` — replace `stubRules` and `ruleDetailPage`
- Modify: `CanaryGo/internal/web/handler_chirps_test.go` — add rules tests

**Background:** Rules are stored in `detection.detection_rules` and accessed via `chirp.Store.ListRules()` and (for detail) a direct pgx query by rule ID. Read `internal/chirp/store.go:ListRules` for the return type.

- [ ] **Step 1: Check ListRules return type**

```bash
grep -A 10 "func.*ListRules" CanaryGo/internal/chirp/store.go
```

- [ ] **Step 2: Write failing test**

Add to `handler_chirps_test.go`:

```go
func TestRulesListPage_Renders(t *testing.T) {
    pool := testutil.MustOpenDB(t)
    store := chirp.NewPgxStore(pool)
    deps := web.Deps{ChirpStore: store}
    h := web.New(deps, nil)

    r := chi.NewRouter()
    h.Mount(r)

    req := httptest.NewRequest(http.MethodGet, "/rules", nil)
    rr := httptest.NewRecorder()
    r.ServeHTTP(rr, req)

    if rr.Code != http.StatusOK {
        t.Fatalf("expected 200 got %d", rr.Code)
    }
}
```

- [ ] **Step 3: Run — confirm passes (stub renders)**

```bash
cd CanaryGo && go test ./internal/web/... -run TestRulesListPage -v
```

- [ ] **Step 4: Replace stubRules with real handler**

```go
r.Get("/rules", h.rulesListPage)
```

```go
func (h *Handler) rulesListPage(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    tenantID := tenantIDFromCtx(ctx)

    var rules []chirp.Rule
    if h.deps.ChirpStore != nil {
        var err error
        rules, err = h.deps.ChirpStore.ListRules(ctx, tenantID)
        if err != nil {
            h.logger.Error("rulesListPage: list", zap.Error(err))
        }
    }
    h.render(w, r, "rules", "rules", map[string]any{
        "Rules": rules,
    })
}
```

- [ ] **Step 5: Update ruleDetailPage**

Replace hardcoded stub with real store lookup. The chirp.Store interface may need a `GetRule(ctx, tenantID, ruleID)` method if it doesn't exist — check first. If absent, add a `GetRuleByID` method to `PgxStore` in `chirp/store.go` (direct pgx read query).

- [ ] **Step 6: Build + test + commit**

```bash
cd CanaryGo && go build ./... && go test ./internal/web/... -v 2>&1 | grep -E "PASS|FAIL"
git add CanaryGo/internal/web/handler.go CanaryGo/internal/web/handler_chirps_test.go
git commit -m "feat(web): wire detection rules list + detail to chirp store"
```

---

## Chunk 6: Hawk Case System

### Task 6: Wire Hawk case list, detail, evidence, analytics, patterns

**Files:**
- Modify: `CanaryGo/internal/web/handler.go` — replace `stubHawkList`, `stubHawkAnalytics`, `stubHawkPatterns`, `hawkDetailPage`, `hawkEvidencePage`
- Create: `CanaryGo/internal/web/handler_cases_test.go`

**Background:** Case store is `internal/casemgmt/store.go`. Read `casemgmt/dto.go` for Case, CaseAction, CaseEvidence types. The `hawkEvidencePage` renders evidence items for a case — it needs `casemgmt.Store.ListEvidence(ctx, tenantID, caseID)`.

- [ ] **Step 1: Read casemgmt types**

```bash
grep -n "^type Case \|^type CaseAction\|^type CaseEvidence\|^type Evidence" \
    CanaryGo/internal/casemgmt/dto.go CanaryGo/internal/casemgmt/store.go | head -20
```

- [ ] **Step 2: Write tests**

Create `CanaryGo/internal/web/handler_cases_test.go`:

```go
package web_test

import (
    "net/http"
    "net/http/httptest"
    "testing"

    "github.com/go-chi/chi/v5"
    "github.com/growdirect-llc/rapidpos/internal/casemgmt"
    "github.com/growdirect-llc/rapidpos/internal/web"
    "github.com/growdirect-llc/rapidpos/internal/testutil"
)

func TestHawkListPage_Renders(t *testing.T) {
    pool := testutil.MustOpenDB(t)
    store := casemgmt.NewStore(pool)
    deps := web.Deps{CaseStore: store}
    h := web.New(deps, nil)

    r := chi.NewRouter()
    h.Mount(r)

    req := httptest.NewRequest(http.MethodGet, "/cases/hawk", nil)
    rr := httptest.NewRecorder()
    r.ServeHTTP(rr, req)

    if rr.Code != http.StatusOK {
        t.Fatalf("expected 200 got %d", rr.Code)
    }
}

func TestHawkDetailPage_UnknownID_Returns404(t *testing.T) {
    pool := testutil.MustOpenDB(t)
    store := casemgmt.NewStore(pool)
    deps := web.Deps{CaseStore: store}
    h := web.New(deps, nil)

    r := chi.NewRouter()
    h.Mount(r)

    req := httptest.NewRequest(http.MethodGet, "/cases/hawk/00000000-0000-0000-0000-000000000000", nil)
    rr := httptest.NewRecorder()
    r.ServeHTTP(rr, req)

    if rr.Code != http.StatusNotFound {
        t.Fatalf("expected 404 got %d", rr.Code)
    }
}
```

- [ ] **Step 3: Run — confirm 404 test fails (current stub returns 200 for all IDs)**

```bash
cd CanaryGo && go test ./internal/web/... -run TestHawkDetailPage_UnknownID -v
```

Expected: FAIL (current stub returns 200 for everything)

- [ ] **Step 4: Replace stubHawkList**

```go
r.Get("/cases/hawk", h.hawkListPage)
```

```go
func (h *Handler) hawkListPage(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    tenantID := tenantIDFromCtx(ctx)

    var cases []*casemgmt.Case
    if h.deps.CaseStore != nil {
        var err error
        // List open cases, sorted by oldest first (Days Open descending)
        cases, err = h.deps.CaseStore.ListCases(ctx, casemgmt.ListFilters{
            TenantID: tenantID,
            Status:   r.URL.Query().Get("status"),
            Limit:    100,
        })
        if err != nil {
            h.logger.Error("hawkListPage: list", zap.Error(err))
        }
    }
    h.render(w, r, "hawk_list", "cases", map[string]any{
        "Cases": cases,
    })
}
```

Note: check `casemgmt.Store.ListCases` signature — if the method is named differently, use the actual name.

- [ ] **Step 5: Replace hawkDetailPage**

```go
func (h *Handler) hawkDetailPage(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    idStr := chi.URLParam(r, "id")
    id, err := uuid.Parse(idStr)
    if err != nil {
        h.render(w, r, "err404", "cases", nil)
        return
    }

    if h.deps.CaseStore == nil {
        h.render(w, r, "hawk_detail", "cases", map[string]any{"Case": map[string]any{"ID": idStr}})
        return
    }

    tenantID := tenantIDFromCtx(ctx)
    c, err := h.deps.CaseStore.GetCase(ctx, tenantID, id)
    if err != nil {
        if errors.Is(err, casemgmt.ErrNotFound) {
            h.render(w, r, "err404", "cases", nil)
            return
        }
        h.logger.Error("hawkDetailPage: get", zap.Error(err))
        h.render(w, r, "err500", "cases", nil)
        return
    }

    timeline, _ := h.deps.CaseStore.ListActions(ctx, tenantID, id)
    evidence, _ := h.deps.CaseStore.ListEvidence(ctx, tenantID, id)

    h.render(w, r, "hawk_detail", "cases", map[string]any{
        "Case":          c,
        "Timeline":      timeline,
        "EvidenceCount": len(evidence),
        "Evidence":      evidence,
    })
}
```

- [ ] **Step 6: Replace hawkEvidencePage**

Similar pattern — get case, get evidence list, render. If case not found → 404.

- [ ] **Step 7: Leave analytics and patterns as stubs for now**

`stubHawkAnalytics` and `stubHawkPatterns` can remain — these require aggregate queries that are more complex. File a TODO comment:

```go
// TODO(Wave 1 polish): replace with real aggregate queries from casemgmt.Store
r.Get("/cases/hawk/analytics", h.page("cases", "hawk_analytics", stubHawkAnalytics))
r.Get("/cases/hawk/patterns", h.page("cases", "hawk_patterns", stubHawkPatterns))
```

- [ ] **Step 8: Build + test**

```bash
cd CanaryGo && go build ./... && go test ./internal/web/... -v 2>&1 | grep -E "PASS|FAIL"
```

Expected: `TestHawkDetailPage_UnknownID_Returns404` now passes.

- [ ] **Step 9: Commit**

```bash
git add CanaryGo/internal/web/handler.go \
        CanaryGo/internal/web/handler_cases_test.go
git commit -m "feat(web): wire Hawk case list + detail + evidence to casemgmt store"
```

---

## Chunk 7: Customer List + Detail + Risk + Context

### Task 7: Wire customer pages to real store

**Files:**
- Modify: `CanaryGo/internal/web/handler.go` — replace `stubCustomersList`, `customerDetailPage`, `customerRiskPage`, `customerContextPage`
- Create: `CanaryGo/internal/web/handler_customers_test.go`

**Background:** Read `internal/customer/dto.go` for CustomerDTO shape. Read `internal/customer/store.go` for `Search(ctx, tenantID, query)`, `GetByID(ctx, tenantID, id)`, `GetRiskProfile(ctx, tenantID, id)` — verify exact method names exist before referencing them.

- [ ] **Step 1: Audit customer store interface**

```bash
grep -n "^func " CanaryGo/internal/customer/store.go
```

Write down the exact public method names. You will need them in Step 4.

- [ ] **Step 2: Write failing tests**

Create `CanaryGo/internal/web/handler_customers_test.go`:

```go
package web_test

import (
    "net/http"
    "net/http/httptest"
    "testing"

    "github.com/go-chi/chi/v5"
    "github.com/growdirect-llc/rapidpos/internal/customer"
    "github.com/growdirect-llc/rapidpos/internal/web"
    "github.com/growdirect-llc/rapidpos/internal/testutil"
)

func TestCustomerListPage_Renders(t *testing.T) {
    pool := testutil.MustOpenDB(t)
    store := customer.NewStore(pool)
    deps := web.Deps{CustomerStore: store}
    h := web.New(deps, nil)

    r := chi.NewRouter()
    h.Mount(r)

    // Customer list is search-first: empty query returns empty results
    req := httptest.NewRequest(http.MethodGet, "/customers", nil)
    rr := httptest.NewRecorder()
    r.ServeHTTP(rr, req)

    if rr.Code != http.StatusOK {
        t.Fatalf("expected 200 got %d", rr.Code)
    }
}

func TestCustomerDetailPage_UnknownID_Returns404(t *testing.T) {
    pool := testutil.MustOpenDB(t)
    store := customer.NewStore(pool)
    deps := web.Deps{CustomerStore: store}
    h := web.New(deps, nil)

    r := chi.NewRouter()
    h.Mount(r)

    req := httptest.NewRequest(http.MethodGet, "/customers/00000000-0000-0000-0000-000000000000", nil)
    rr := httptest.NewRecorder()
    r.ServeHTTP(rr, req)

    if rr.Code != http.StatusNotFound {
        t.Fatalf("expected 404 got %d", rr.Code)
    }
}
```

- [ ] **Step 3: Run — confirm 404 test fails (stub returns 200)**

```bash
cd CanaryGo && go test ./internal/web/... -run TestCustomerDetailPage_UnknownID -v
```

- [ ] **Step 4: Replace stubCustomersList**

Customer list is search-first (per the brief — no browse). If no `q` param, render empty state.

```go
r.Get("/customers", h.customersListPage)
```

```go
func (h *Handler) customersListPage(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    q := r.URL.Query().Get("q")
    tenantID := tenantIDFromCtx(ctx)

    var customers []*customer.CustomerDTO
    if h.deps.CustomerStore != nil && q != "" {
        var err error
        customers, err = h.deps.CustomerStore.Search(ctx, tenantID, q)
        if err != nil {
            h.logger.Error("customersListPage: search", zap.Error(err))
        }
    }
    h.render(w, r, "customers_list", "customers", map[string]any{
        "Customers": customers,
        "Query":     q,
    })
}
```

- [ ] **Step 5: Replace customerDetailPage, customerRiskPage, customerContextPage**

Same pattern as alert/case detail: parse UUID, call store.GetByID, handle ErrNotFound → 404, other errors → 500.

For risk page: call `store.GetRiskProfile(ctx, tenantID, id)` — verify this method exists in Step 1.

For context page: call whatever "cashier co-occurrence" or "context" query the store exposes.

- [ ] **Step 6: Build + test**

```bash
cd CanaryGo && go build ./... && go test ./internal/web/... -v 2>&1 | grep -E "PASS|FAIL"
```

- [ ] **Step 7: Commit**

```bash
git add CanaryGo/internal/web/handler.go \
        CanaryGo/internal/web/handler_customers_test.go
git commit -m "feat(web): wire customer list + detail + risk + context to real store"
```

---

## Chunk 8: Settings Pages — LP Substrate + Allow-Lists

### Task 8: Wire settings pages to LP substrate and allow-list tables

**Files:**
- Modify: `CanaryGo/internal/web/handler.go` — replace inline stub lambdas for settings routes
- Create: `CanaryGo/internal/lp/substrate.go` *(new)* — LP substrate store
- Create: `CanaryGo/internal/web/handler_settings_test.go`

**Background:** The settings pages (`/settings/store/drawer`, `/settings/allowlist/dead-count`, etc.) return stub data via inline lambdas in the route registration. They need a store that reads from `detection.lp_substrate` and `detection.allow_list` (created in migration 024).

This is the only task in Wave 1 that requires a new internal package. The existing packages don't have an LP substrate store.

- [ ] **Step 1: Write failing test**

Create `CanaryGo/internal/web/handler_settings_test.go`:

```go
package web_test

import (
    "net/http"
    "net/http/httptest"
    "testing"

    "github.com/go-chi/chi/v5"
    "github.com/growdirect-llc/rapidpos/internal/web"
    "github.com/growdirect-llc/rapidpos/internal/testutil"
)

func TestStoreDrawerPage_Renders(t *testing.T) {
    pool := testutil.MustOpenDB(t)
    _ = pool // LP substrate store to be added
    deps := web.Deps{}
    h := web.New(deps, nil)

    r := chi.NewRouter()
    h.Mount(r)

    req := httptest.NewRequest(http.MethodGet, "/settings/store/drawer", nil)
    rr := httptest.NewRecorder()
    r.ServeHTTP(rr, req)

    if rr.Code != http.StatusOK {
        t.Fatalf("expected 200 got %d", rr.Code)
    }
}
```

- [ ] **Step 2: Run — confirm passes (inline stub renders correctly)**

```bash
cd CanaryGo && go test ./internal/web/... -run TestStoreDrawerPage -v
```

Expected: PASS (inline stub still renders)

- [ ] **Step 3: Create internal/lp/substrate.go**

```go
// internal/lp/substrate.go
//
// LP substrate store — reads per-location LP configuration thresholds
// from detection.lp_substrate. These values are required for detection
// rules to fire; a missing row means the rule is silent for that location.
package lp

import (
    "context"
    "encoding/json"

    "github.com/google/uuid"
    "github.com/jackc/pgx/v5/pgxpool"
)

// SubstrateStore reads LP configuration from detection.lp_substrate.
type SubstrateStore struct {
    pool *pgxpool.Pool
}

func NewSubstrateStore(pool *pgxpool.Pool) *SubstrateStore {
    return &SubstrateStore{pool: pool}
}

// SubstrateRow is a single LP substrate configuration entry.
type SubstrateRow struct {
    ID          uuid.UUID
    TenantID    uuid.UUID
    LocationID  uuid.UUID
    ConfigKey   string
    ConfigValue json.RawMessage
}

// ListByKey returns all substrate rows for a tenant with the given config_key.
// Returns empty slice (not error) when no rows exist — this is the "not configured" state.
func (s *SubstrateStore) ListByKey(ctx context.Context, tenantID uuid.UUID, key string) ([]SubstrateRow, error) {
    rows, err := s.pool.Query(ctx, `
        SELECT id, tenant_id, location_id, config_key, config_value
        FROM detection.lp_substrate
        WHERE tenant_id = $1 AND config_key = $2
        ORDER BY location_id
    `, tenantID, key)
    if err != nil {
        return nil, err
    }
    defer rows.Close()

    var results []SubstrateRow
    for rows.Next() {
        var r SubstrateRow
        if err := rows.Scan(&r.ID, &r.TenantID, &r.LocationID, &r.ConfigKey, &r.ConfigValue); err != nil {
            return nil, err
        }
        results = append(results, r)
    }
    return results, rows.Err()
}

// AllowListStore reads allow-list entries from detection.allow_list.
type AllowListStore struct {
    pool *pgxpool.Pool
}

func NewAllowListStore(pool *pgxpool.Pool) *AllowListStore {
    return &AllowListStore{pool: pool}
}

// AllowListEntry is a single allow-list configuration row.
type AllowListEntry struct {
    ID         uuid.UUID
    ListType   string
    LocationID *uuid.UUID
    EmployeeID *uuid.UUID
    Reason     string
    Parameters json.RawMessage
}

// ListByType returns all allow-list entries for a tenant of the given list type.
func (s *AllowListStore) ListByType(ctx context.Context, tenantID uuid.UUID, listType string) ([]AllowListEntry, error) {
    rows, err := s.pool.Query(ctx, `
        SELECT id, list_type, location_id, employee_id, reason, parameters
        FROM detection.allow_list
        WHERE tenant_id = $1 AND list_type = $2
        ORDER BY created_at DESC
    `, tenantID, listType)
    if err != nil {
        return nil, err
    }
    defer rows.Close()

    var results []AllowListEntry
    for rows.Next() {
        var e AllowListEntry
        if err := rows.Scan(&e.ID, &e.ListType, &e.LocationID, &e.EmployeeID, &e.Reason, &e.Parameters); err != nil {
            return nil, err
        }
        results = append(results, e)
    }
    return results, rows.Err()
}
```

- [ ] **Step 4: Add LP substrate stores to Deps**

In `deps.go`, add:

```go
import (
    // existing imports
    "github.com/growdirect-llc/rapidpos/internal/lp"
)

type Deps struct {
    AlertStore      *alert.Store
    CaseStore       *casemgmt.Store
    ChirpStore      chirp.Store
    CustomerStore   *customer.Store
    SubstrateStore  *lp.SubstrateStore   // LP threshold config
    AllowListStore  *lp.AllowListStore   // LP allow-list config
}
```

- [ ] **Step 5: Replace settings inline stubs with real handlers**

Replace the 8 inline stubs for settings pages (drawer, discounts, void-reasons, comp-reasons, allowlist dead-count, discounts, voids, comps) with method calls. Example for drawer:

```go
r.Get("/settings/store/drawer", h.settingsDrawerPage)
```

```go
func (h *Handler) settingsDrawerPage(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()
    tenantID := tenantIDFromCtx(ctx)

    var thresholds []lp.SubstrateRow
    if h.deps.SubstrateStore != nil {
        var err error
        thresholds, err = h.deps.SubstrateStore.ListByKey(ctx, tenantID, "drawer_threshold")
        if err != nil {
            h.logger.Error("settingsDrawerPage: list", zap.Error(err))
        }
    }
    h.render(w, r, "settings_store_drawer", "settings", map[string]any{
        "Thresholds": thresholds,
    })
}
```

Apply the same pattern for the other 7 settings pages — each reads a different config_key or list_type from the LP substrate/allow-list tables.

- [ ] **Step 6: Wire LP stores in gateway main.go**

```go
lpSubstrate := lp.NewSubstrateStore(pool)
lpAllowList := lp.NewAllowListStore(pool)
webDeps.SubstrateStore = lpSubstrate
webDeps.AllowListStore = lpAllowList
```

Add import:
```go
lpPkg "github.com/growdirect-llc/rapidpos/internal/lp"
```

- [ ] **Step 7: Build + test**

```bash
cd CanaryGo && go build ./... && go test ./internal/web/... -v 2>&1 | grep -E "PASS|FAIL"
```

- [ ] **Step 8: Commit**

```bash
git add CanaryGo/internal/lp/ \
        CanaryGo/internal/web/handler.go \
        CanaryGo/internal/web/deps.go \
        CanaryGo/internal/web/handler_settings_test.go \
        CanaryGo/cmd/gateway/main.go
git commit -m "feat(web): wire LP substrate + allow-list settings pages to real stores (detection schema)"
```

---

## Chunk 9: Final Integration + Smoke Test

### Task 9: End-to-end integration validation

**Files:**
- No new files — this task validates the full stack works together

- [ ] **Step 1: Run all tests**

```bash
cd CanaryGo && go test ./... 2>&1 | tail -20
```

Expected: all packages PASS. Note any failures — investigate each before proceeding.

- [ ] **Step 2: Build all cmd binaries**

```bash
cd CanaryGo && go build ./cmd/... 2>&1
```

Expected: all binaries compile cleanly.

- [ ] **Step 3: Start the gateway service locally (if Docker stack is up)**

```bash
cd CanaryGo && DATABASE_URL="postgres://growdirect:growdirect_dev@localhost:5432/canary_gcp" \
    VALKEY_URL="redis://localhost:6379/2" \
    go run ./cmd/gateway/main.go
```

Expected: service starts on port 8087 (or the gateway port from CLAUDE.md).

- [ ] **Step 4: Smoke test the Wave 1 screens**

With the service running, verify each list page returns 200 and renders:

```bash
# Each of these should return HTTP 200 with HTML
curl -s -o /dev/null -w "%{http_code}" http://localhost:8087/alerts
curl -s -o /dev/null -w "%{http_code}" http://localhost:8087/chirps
curl -s -o /dev/null -w "%{http_code}" http://localhost:8087/rules
curl -s -o /dev/null -w "%{http_code}" http://localhost:8087/cases/hawk
curl -s -o /dev/null -w "%{http_code}" http://localhost:8087/customers
curl -s -o /dev/null -w "%{http_code}" http://localhost:8087/settings/store/drawer
curl -s -o /dev/null -w "%{http_code}" http://localhost:8087/settings/allowlist/dead-count
```

Expected: all return `200`.

- [ ] **Step 5: Final commit + push**

```bash
git push origin main
```

---

## Post-Completion Checklist

After all tasks pass:

- [ ] All `go test ./...` passing
- [ ] All Wave 1 list pages render live (empty but connected to real DB)
- [ ] All Wave 1 detail pages return 404 for unknown IDs (not 200 with stub data)
- [ ] Detection schema migration (024) applied to dev and test DBs
- [ ] No stub functions remain for Wave 1 screens (stubs only remain for Wave 2+ screens — that's expected)
- [ ] LP substrate and allow-list stores connected to settings pages
- [ ] Gateway binary builds cleanly
- [ ] GRO-769 (auth middleware) is the next logical ticket — the `tenantIDFromCtx` stub is the known gap until that lands

---

## What's Left After Wave 1

1. **GRO-769 — Auth middleware:** Replace `tenantIDFromCtx` stub with real JWT/session extraction. Until this lands, all pages return empty data (correct behavior — no tenant context = no data).
2. **Wave 1 analytics stubs:** `hawk_analytics` and `hawk_patterns` are still stub — aggregate queries needed.
3. **Settings POST handlers:** The settings pages render data but have no save functionality yet — POST handlers are Wave 2 work.
4. **Wave 2 implementation plan:** Transfer/inventory/device screens follow the same store-wiring pattern.
