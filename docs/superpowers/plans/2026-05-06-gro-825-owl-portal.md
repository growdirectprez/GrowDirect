# GRO-825 W6 — Owl Intelligence Portal Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add three operator-facing portal surfaces over `internal/owl/` substrate — `/owl/dashboards`, `/owl/parties`, `/owl/lp-performance` — so tenants can read RFM rollups, LP-rate metrics, and signal aggregates instead of having only a placeholder `/owl` semantic-search stub.

**Architecture:** Three server-rendered HTML pages on the existing chi router in `internal/web/`. Each page reads from `internal/owl.DashboardStore` (already exists; tenant-scoped pgx). One new optional `Deps` field — `OwlDashboardStore *owl.DashboardStore` — keeps the wiring nil-safe and matches the W7 protocol-portal pattern (commit b4d3d06). A single portal-layer period helper translates `day|week|month|quarter` query params into UTC `[from, to)` windows. No changes to `internal/owl/period.go`, `internal/owl/aggregator.go`, or `internal/owl/metrics/`.

**Tech Stack:** Go 1.22 · Chi v5 · `html/template` · pgx/v5 (read-only via `DashboardStore`) · existing `web.PageData` shape and `internal/web/templates/base.html` design system.

---

## Scope clarification

The dispatch's "drill-down to detection history" line presumes a `party_id → detections` lookup that does not currently exist in `internal/owl` (see `dashboards.go` — `LPRateRollup` joins by `tenant_id`, not `party_id`; detection.detections has no party_id column visible in the SDD). The party list with full RFM scores inline is the operator-facing deliverable. Per-party detection history is filed as a follow-on dispatch in the close-out comment.

The "Period selector (day / week / month / quarter)" line maps to UTC windows at the portal layer:
- `day` → today 00:00 UTC → now
- `week` → Monday 00:00 UTC → now (ISO-8601 week)
- `month` → 1st 00:00 UTC of current month → now
- `quarter` → 1st 00:00 UTC of current calendar quarter → now

Default: `week`. Timezone-aware variants stay in `internal/owl/period.go` for the JSON API; the portal helper is intentionally simpler and UTC-only.

---

## File Structure

**Modify:**

- `CanaryGo/internal/web/deps.go` — add `OwlDashboardStore *owl.DashboardStore` (one new field; nil-safe, matches W7's `ProtocolValidate` / `ProtocolNamespace` pattern).
- `CanaryGo/internal/web/handler.go` — add three template registrations in `New()`, three routes in `Mount()`, three handler methods, one period helper. Net add ≈ 250 lines, no behavior change to existing routes.
- `CanaryGo/internal/web/templates/partials/sidebar.html` — add an "Intelligence" section between "Reports" and "System" with three entries. Existing "Owl" link in "System" stays (semantic-search stub, unchanged).

**Create:**

- `CanaryGo/internal/web/templates/owl/dashboards.html` — multi-panel: KPI tiles + LP-rate-by-rule table + RFM top-10 table.
- `CanaryGo/internal/web/templates/owl/parties.html` — paginated party list ordered by `party_value` DESC.
- `CanaryGo/internal/web/templates/owl/lp_performance.html` — LP-rate detail by rule_type with detection / case / escalation columns.
- `CanaryGo/internal/web/handler_owl_test.go` — three tests: no-store empty state, with-store renders, period selector parses correctly.

**Untouched (deliberately):**

- `internal/owl/aggregator.go`, `internal/owl/store.go`, `internal/owl/dashboards.go`, `internal/owl/period.go`, `internal/owl/metrics/*` — substrate is read-only from the portal's perspective.
- `cmd/web/main.go` — wiring the new `OwlDashboardStore` into the entry point is a thin glue change covered in Task 5; no architectural shift.

---

## Chunk 1: Substrate wiring + period helper

### Task 1: Add OwlDashboardStore to web.Deps

**Files:**
- Modify: `CanaryGo/internal/web/deps.go`

- [ ] **Step 1: Add the import + struct field**

In `internal/web/deps.go`, add to the import block:

```go
"github.com/growdirect-llc/rapidpos/internal/owl"
```

Add to the `Deps` struct, after `MCPRegistry`:

```go
	// Owl intelligence portal — tenant-scoped dashboard reads over
	// party.decisioning_facts and detection.detections / detection.cases.
	// Wired W6 / GRO-825. Separate from the merchant-keyed Aggregator
	// behind /v1/owl/* JSON API (cmd/owl) — that surface is for external
	// callers; the portal stays tenant-scoped to match every other
	// internal/web/ handler.
	OwlDashboard *owl.DashboardStore
```

- [ ] **Step 2: Confirm it compiles**

Run: `cd CanaryGo && go build ./internal/web/...`
Expected: no errors. (No callers reference the new field yet.)

- [ ] **Step 3: Commit**

```bash
git add CanaryGo/internal/web/deps.go
git commit -m "feat(web): add OwlDashboard dep for W6 owl portal — GRO-825"
```

---

### Task 2: Period helper for portal-side day/week/month/quarter

**Files:**
- Modify: `CanaryGo/internal/web/handler.go` (add helper at bottom of file, near `shortHex`)
- Test: `CanaryGo/internal/web/handler_owl_test.go` (new file)

- [ ] **Step 1: Write the failing test**

Create `CanaryGo/internal/web/handler_owl_test.go` with a fixed-time test for the period helper. Since `owlPortalPeriod` is unexported, the test goes in `package web` (white-box).

```go
package web

import (
	"testing"
	"time"
)

func TestOwlPortalPeriod_Day(t *testing.T) {
	// Wednesday 2026-05-06 14:30 UTC
	now := time.Date(2026, 5, 6, 14, 30, 0, 0, time.UTC)
	from, to, label := owlPortalPeriod("day", now)

	if !from.Equal(time.Date(2026, 5, 6, 0, 0, 0, 0, time.UTC)) {
		t.Errorf("day from = %v want 2026-05-06 00:00 UTC", from)
	}
	if !to.Equal(now) {
		t.Errorf("day to = %v want now", to)
	}
	if label != "day" {
		t.Errorf("label = %q want %q", label, "day")
	}
}

func TestOwlPortalPeriod_Week_Wednesday(t *testing.T) {
	// Wednesday 2026-05-06 → ISO week starts Monday 2026-05-04
	now := time.Date(2026, 5, 6, 14, 30, 0, 0, time.UTC)
	from, _, _ := owlPortalPeriod("week", now)
	want := time.Date(2026, 5, 4, 0, 0, 0, 0, time.UTC)
	if !from.Equal(want) {
		t.Errorf("week from = %v want %v", from, want)
	}
}

func TestOwlPortalPeriod_Week_Sunday(t *testing.T) {
	// Sunday 2026-05-10 → previous Monday 2026-05-04
	now := time.Date(2026, 5, 10, 9, 0, 0, 0, time.UTC)
	from, _, _ := owlPortalPeriod("week", now)
	want := time.Date(2026, 5, 4, 0, 0, 0, 0, time.UTC)
	if !from.Equal(want) {
		t.Errorf("sun: week from = %v want %v", from, want)
	}
}

func TestOwlPortalPeriod_Month(t *testing.T) {
	now := time.Date(2026, 5, 6, 14, 30, 0, 0, time.UTC)
	from, _, _ := owlPortalPeriod("month", now)
	want := time.Date(2026, 5, 1, 0, 0, 0, 0, time.UTC)
	if !from.Equal(want) {
		t.Errorf("month from = %v want %v", from, want)
	}
}

func TestOwlPortalPeriod_Quarter(t *testing.T) {
	cases := []struct {
		now  time.Time
		want time.Time
	}{
		{time.Date(2026, 1, 15, 0, 0, 0, 0, time.UTC), time.Date(2026, 1, 1, 0, 0, 0, 0, time.UTC)},
		{time.Date(2026, 5, 6, 0, 0, 0, 0, time.UTC), time.Date(2026, 4, 1, 0, 0, 0, 0, time.UTC)},
		{time.Date(2026, 8, 30, 0, 0, 0, 0, time.UTC), time.Date(2026, 7, 1, 0, 0, 0, 0, time.UTC)},
		{time.Date(2026, 12, 1, 0, 0, 0, 0, time.UTC), time.Date(2026, 10, 1, 0, 0, 0, 0, time.UTC)},
	}
	for _, c := range cases {
		from, _, _ := owlPortalPeriod("quarter", c.now)
		if !from.Equal(c.want) {
			t.Errorf("quarter(now=%v) from = %v want %v", c.now, from, c.want)
		}
	}
}

func TestOwlPortalPeriod_Default(t *testing.T) {
	// Empty / unknown → defaults to week.
	now := time.Date(2026, 5, 6, 14, 30, 0, 0, time.UTC)
	_, _, label := owlPortalPeriod("", now)
	if label != "week" {
		t.Errorf("empty kind label = %q want %q", label, "week")
	}
	_, _, label = owlPortalPeriod("nonsense", now)
	if label != "week" {
		t.Errorf("unknown kind label = %q want %q", label, "week")
	}
}
```

- [ ] **Step 2: Run test, verify it fails**

Run: `cd CanaryGo && go test ./internal/web/ -run TestOwlPortalPeriod -v`
Expected: FAIL — `undefined: owlPortalPeriod`

- [ ] **Step 3: Add the helper to handler.go**

Append to `internal/web/handler.go`, just below `shortHex`:

```go
// owlPortalPeriod translates the portal's day/week/month/quarter selector
// into a UTC [from, to) window. Default and unknown values fold to "week".
//
// UTC-only on purpose: timezone-aware period parsing belongs to the JSON
// API surface in internal/owl/period.go where it's part of the public
// merchant-keyed contract. The portal is an operator surface; UTC keeps
// the URL stable across user devices.
func owlPortalPeriod(kind string, now time.Time) (from, to time.Time, label string) {
	to = now.UTC()
	switch strings.ToLower(strings.TrimSpace(kind)) {
	case "day":
		from = time.Date(to.Year(), to.Month(), to.Day(), 0, 0, 0, 0, time.UTC)
		return from, to, "day"
	case "month":
		from = time.Date(to.Year(), to.Month(), 1, 0, 0, 0, 0, time.UTC)
		return from, to, "month"
	case "quarter":
		qStartMonth := ((int(to.Month())-1)/3)*3 + 1
		from = time.Date(to.Year(), time.Month(qStartMonth), 1, 0, 0, 0, 0, time.UTC)
		return from, to, "quarter"
	default: // "week" or anything unrecognized
		offset := (int(to.Weekday()) + 6) % 7 // Monday = 0
		from = time.Date(to.Year(), to.Month(), to.Day()-offset, 0, 0, 0, 0, time.UTC)
		return from, to, "week"
	}
}
```

- [ ] **Step 4: Run test, verify it passes**

Run: `cd CanaryGo && go test ./internal/web/ -run TestOwlPortalPeriod -v`
Expected: PASS, all six tests.

- [ ] **Step 5: go vet**

Run: `cd CanaryGo && go vet ./internal/web/...`
Expected: clean.

- [ ] **Step 6: Commit**

```bash
git add CanaryGo/internal/web/handler.go CanaryGo/internal/web/handler_owl_test.go
git commit -m "feat(web): add owlPortalPeriod helper for W6 — GRO-825"
```

---

## Chunk 2: Three portal pages

### Task 3: /owl/dashboards (multi-panel)

**Files:**
- Create: `CanaryGo/internal/web/templates/owl/dashboards.html`
- Modify: `CanaryGo/internal/web/handler.go` (template registration in `New()`, route in `Mount()`, handler method)

- [ ] **Step 1: Write the failing test (no-store empty state)**

Append to `CanaryGo/internal/web/handler_owl_test.go`:

```go
import (
	"net/http"
	"net/http/httptest"
	"strings"

	"github.com/go-chi/chi/v5"
)

func TestOwlDashboards_NoStore_RendersEmptyState(t *testing.T) {
	h := New(Deps{}, nil)
	r := chi.NewRouter()
	h.Mount(r)

	req := httptest.NewRequest(http.MethodGet, "/owl/dashboards", nil)
	rr := httptest.NewRecorder()
	r.ServeHTTP(rr, req)
	if rr.Code != http.StatusOK {
		t.Fatalf("expected 200 got %d body=%s", rr.Code, rr.Body.String())
	}
	for _, want := range []string{"Owl", "Intelligence", "No LP-rate data yet", "No party data yet"} {
		if !strings.Contains(rr.Body.String(), want) {
			t.Errorf("body missing %q", want)
		}
	}
}

func TestOwlDashboards_PeriodSelector(t *testing.T) {
	h := New(Deps{}, nil)
	r := chi.NewRouter()
	h.Mount(r)

	for _, period := range []string{"day", "week", "month", "quarter"} {
		req := httptest.NewRequest(http.MethodGet, "/owl/dashboards?period="+period, nil)
		rr := httptest.NewRecorder()
		r.ServeHTTP(rr, req)
		if rr.Code != http.StatusOK {
			t.Errorf("period=%s: expected 200 got %d", period, rr.Code)
		}
		// Active period highlighted in selector.
		if !strings.Contains(rr.Body.String(), `data-period="`+period+`" class="period-pill active"`) {
			t.Errorf("period=%s: active pill not rendered", period)
		}
	}
}
```

- [ ] **Step 2: Run, verify failure**

Run: `cd CanaryGo && go test ./internal/web/ -run TestOwlDashboards -v`
Expected: FAIL — 404 from chi (route not mounted yet) and template-not-found.

- [ ] **Step 3: Create the template**

Create `CanaryGo/internal/web/templates/owl/dashboards.html`:

```html
{{template "base.html" .}}

{{define "title"}}Owl Dashboards — Canary{{end}}

{{define "content"}}
{{with .Data}}
<div class="page-header">
  <h1>Owl &middot; Dashboards</h1>
  <p class="page-subtitle">LP rate, alert volume by rule, party intelligence — operator view of the canonical schema</p>
</div>

<div style="display:flex;gap:8px;margin-bottom:24px;">
  {{$active := .Period}}
  {{range $kind := .PeriodOptions}}
  <a href="/owl/dashboards?period={{$kind}}"
     data-period="{{$kind}}"
     class="period-pill{{if eq $kind $active}} active{{end}}"
     style="padding:6px 14px;border-radius:6px;font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;text-decoration:none;border:1px solid var(--border-subtle);{{if eq $kind $active}}background:var(--signal-yellow);color:#0d1117;{{else}}background:var(--bg-surface);color:var(--text-secondary);{{end}}">{{$kind}}</a>
  {{end}}
  <span style="margin-left:auto;font-size:11px;color:var(--text-muted);align-self:center;">
    {{.WindowFrom}} → {{.WindowTo}} UTC
  </span>
</div>

<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:24px;">
  <div class="ops-card" style="text-align:center;">
    <div style="font-size:24px;font-weight:700;color:var(--text-primary);">{{.TotalDetections}}</div>
    <div style="font-size:11px;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.05em;margin-top:4px;">Detections</div>
  </div>
  <div class="ops-card" style="text-align:center;">
    <div style="font-size:24px;font-weight:700;color:var(--accent-blue);">{{.TotalCases}}</div>
    <div style="font-size:11px;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.05em;margin-top:4px;">Cases Opened</div>
  </div>
  <div class="ops-card" style="text-align:center;">
    <div style="font-size:24px;font-weight:700;color:var(--health-green);">{{.EscalationRate}}</div>
    <div style="font-size:11px;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.05em;margin-top:4px;">Escalation Rate</div>
  </div>
  <div class="ops-card" style="text-align:center;">
    <div style="font-size:24px;font-weight:700;color:var(--signal-yellow);">{{.PartyCount}}</div>
    <div style="font-size:11px;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.05em;margin-top:4px;">Tracked Parties</div>
  </div>
</div>

<div class="ops-card" style="margin-bottom:24px;">
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;">
    <div style="font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;color:var(--text-muted);">LP Rate by Rule</div>
    <a href="/owl/lp-performance?period={{.Period}}" style="font-size:11px;color:var(--signal-yellow);text-decoration:none;">Detail →</a>
  </div>
  {{if .LPRows}}
  <table style="width:100%;border-collapse:collapse;font-size:13px;">
    <thead>
      <tr style="color:var(--text-muted);font-size:11px;text-transform:uppercase;letter-spacing:0.05em;">
        <th style="padding:6px 12px 6px 0;text-align:left;font-weight:500;">Rule Type</th>
        <th style="padding:6px 12px;text-align:right;font-weight:500;">Detections</th>
        <th style="padding:6px 12px;text-align:right;font-weight:500;">Cases</th>
        <th style="padding:6px 0;text-align:right;font-weight:500;">Escalation</th>
      </tr>
    </thead>
    <tbody>
      {{range .LPRows}}
      <tr style="border-top:1px solid var(--border-subtle);">
        <td style="padding:10px 12px 10px 0;color:var(--text-primary);">{{.RuleType}}</td>
        <td style="padding:10px 12px;text-align:right;color:var(--text-secondary);">{{.Detections}}</td>
        <td style="padding:10px 12px;text-align:right;color:var(--text-secondary);">{{.Cases}}</td>
        <td style="padding:10px 0;text-align:right;color:var(--text-primary);font-weight:600;">{{.EscalationPct}}</td>
      </tr>
      {{end}}
    </tbody>
  </table>
  {{else}}
  <p style="font-size:13px;color:var(--text-muted);padding:16px 0;">No LP-rate data yet for this window. Detections roll up here as they're written by Chirp.</p>
  {{end}}
</div>

<div class="ops-card">
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;">
    <div style="font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;color:var(--text-muted);">Top Parties by Value</div>
    <a href="/owl/parties" style="font-size:11px;color:var(--signal-yellow);text-decoration:none;">All parties →</a>
  </div>
  {{if .TopParties}}
  <table style="width:100%;border-collapse:collapse;font-size:13px;">
    <thead>
      <tr style="color:var(--text-muted);font-size:11px;text-transform:uppercase;letter-spacing:0.05em;">
        <th style="padding:6px 12px 6px 0;text-align:left;font-weight:500;">Party</th>
        <th style="padding:6px 12px;text-align:right;font-weight:500;">Value (12mo)</th>
        <th style="padding:6px 12px;text-align:right;font-weight:500;">Frequency</th>
        <th style="padding:6px 12px;text-align:right;font-weight:500;">Recency (d)</th>
        <th style="padding:6px 0;text-align:left;font-weight:500;">Confidence</th>
      </tr>
    </thead>
    <tbody>
      {{range .TopParties}}
      <tr style="border-top:1px solid var(--border-subtle);">
        <td style="padding:10px 12px 10px 0;font-family:'Space Grotesk',monospace;font-size:11px;color:var(--text-muted);">{{.PartyShort}}</td>
        <td style="padding:10px 12px;text-align:right;color:var(--text-primary);font-weight:600;">{{.PartyValue}}</td>
        <td style="padding:10px 12px;text-align:right;color:var(--text-secondary);">{{.PartyFrequency}}</td>
        <td style="padding:10px 12px;text-align:right;color:var(--text-secondary);">{{.PartyRecency}}</td>
        <td style="padding:10px 0;color:var(--text-secondary);">{{.Confidence}}</td>
      </tr>
      {{end}}
    </tbody>
  </table>
  {{else}}
  <p style="font-size:13px;color:var(--text-muted);padding:16px 0;">No party data yet. The party.decisioning_facts MV refreshes on the cadence configured in party-identity-design.md §E.</p>
  {{end}}
</div>
{{end}}
{{end}}
```

- [ ] **Step 4: Register the template + route + handler in handler.go**

In `New()`, add after line 174 (`h.mustParse("protocol_overview", ...)`):

```go
	h.mustParse("owl_dashboards", "templates/owl/dashboards.html")
```

In `Mount()`, add after line 213 (`r.Get("/owl", h.owlPage)`):

```go
	r.Get("/owl/dashboards", h.owlDashboardsPage)
```

Append a new handler method after `owlPage()` (line 398):

```go
// owlDashboardsPage renders the multi-panel intelligence overview —
// LP rate by rule, top parties by value, KPI tiles. Tenant-scoped read
// over party.decisioning_facts and detection.detections / detection.cases
// via internal/owl.DashboardStore. Wired W6 / GRO-825.
func (h *Handler) owlDashboardsPage(w http.ResponseWriter, r *http.Request) {
	from, to, label := owlPortalPeriod(r.URL.Query().Get("period"), time.Now())
	view := map[string]any{
		"Period":          label,
		"PeriodOptions":   []string{"day", "week", "month", "quarter"},
		"WindowFrom":      from.Format("2006-01-02 15:04"),
		"WindowTo":        to.Format("2006-01-02 15:04"),
		"TotalDetections": 0,
		"TotalCases":      0,
		"EscalationRate":  "0%",
		"PartyCount":      0,
		"LPRows":          nil,
		"TopParties":      nil,
	}

	if h.deps.OwlDashboard != nil {
		ctx := r.Context()
		tenantID := tenantIDFromCtx(ctx)

		lp, err := h.deps.OwlDashboard.LPRateRollup(ctx, tenantID, from, to)
		if err != nil {
			h.logger.Error("owlDashboardsPage: lp-rate", zap.Error(err))
		} else {
			rows := make([]map[string]any, 0, len(lp))
			var totalDet, totalCase int
			for _, m := range lp {
				rows = append(rows, map[string]any{
					"RuleType":      m.RuleType,
					"Detections":    m.DetectionCount,
					"Cases":         m.CaseCount,
					"EscalationPct": formatPct(m.EscalationRate),
				})
				totalDet += m.DetectionCount
				totalCase += m.CaseCount
			}
			view["LPRows"] = rows
			view["TotalDetections"] = totalDet
			view["TotalCases"] = totalCase
			if totalDet > 0 {
				view["EscalationRate"] = formatPct(float64(totalCase) / float64(totalDet))
			}
		}

		parties, err := h.deps.OwlDashboard.ListPartyRFM(ctx, tenantID, 10)
		if err != nil {
			h.logger.Error("owlDashboardsPage: parties", zap.Error(err))
		} else {
			rows := make([]map[string]any, 0, len(parties))
			for _, p := range parties {
				rows = append(rows, map[string]any{
					"PartyShort":     p.PartyID.String()[:8],
					"PartyValue":     p.PartyValue,
					"PartyFrequency": p.PartyFrequency,
					"PartyRecency":   p.PartyRecency,
					"Confidence":     p.Confidence,
				})
			}
			view["TopParties"] = rows
			view["PartyCount"] = len(parties)
		}
	}

	h.render(w, r, "owl_dashboards", "owl_intel", view)
}

// formatPct renders a 0..1 ratio as a percentage with one decimal.
func formatPct(r float64) string {
	return strconv.FormatFloat(r*100, 'f', 1, 64) + "%"
}
```

Required imports already present in `handler.go` — `time`, `strconv`, `zap`. Add to the `internal/owl` import only if not already imported (it's not, since `cmd/web/main.go` is the wiring point). Actually `handler.go` does not import `internal/owl` yet — but the handler dereferences `h.deps.OwlDashboard` which is already typed in `deps.go`. Go does not require the consumer file to import the type's package when accessed only via field selection, so no import change to `handler.go`.

- [ ] **Step 5: Run test, verify it passes**

Run: `cd CanaryGo && go test ./internal/web/ -run TestOwlDashboards -v`
Expected: PASS — both tests.

- [ ] **Step 6: Verify no regressions**

Run: `cd CanaryGo && go test ./internal/web/...`
Expected: all existing tests pass; new tests pass.

- [ ] **Step 7: Commit**

```bash
git add CanaryGo/internal/web/handler.go CanaryGo/internal/web/handler_owl_test.go CanaryGo/internal/web/templates/owl/dashboards.html
git commit -m "feat(web): wire /owl/dashboards multi-panel — GRO-825 W6 (1/3)"
```

---

### Task 4: /owl/parties (RFM list)

**Files:**
- Create: `CanaryGo/internal/web/templates/owl/parties.html`
- Modify: `CanaryGo/internal/web/handler.go`

- [ ] **Step 1: Write the failing test**

Append to `handler_owl_test.go`:

```go
func TestOwlParties_NoStore_RendersEmptyState(t *testing.T) {
	h := New(Deps{}, nil)
	r := chi.NewRouter()
	h.Mount(r)

	req := httptest.NewRequest(http.MethodGet, "/owl/parties", nil)
	rr := httptest.NewRecorder()
	r.ServeHTTP(rr, req)
	if rr.Code != http.StatusOK {
		t.Fatalf("expected 200 got %d", rr.Code)
	}
	if !strings.Contains(rr.Body.String(), "No parties tracked yet") {
		t.Errorf("expected empty-state copy")
	}
}

func TestOwlParties_LimitClamp(t *testing.T) {
	h := New(Deps{}, nil)
	r := chi.NewRouter()
	h.Mount(r)

	// limit=9999 should clamp; limit=abc should fall back.
	for _, q := range []string{"limit=9999", "limit=abc", "limit=0"} {
		req := httptest.NewRequest(http.MethodGet, "/owl/parties?"+q, nil)
		rr := httptest.NewRecorder()
		r.ServeHTTP(rr, req)
		if rr.Code != http.StatusOK {
			t.Errorf("query=%s: expected 200 got %d", q, rr.Code)
		}
	}
}
```

- [ ] **Step 2: Verify failure**

Run: `cd CanaryGo && go test ./internal/web/ -run TestOwlParties -v`
Expected: FAIL — 404 (route not mounted).

- [ ] **Step 3: Create template**

Create `CanaryGo/internal/web/templates/owl/parties.html`:

```html
{{template "base.html" .}}

{{define "title"}}Owl Parties — Canary{{end}}

{{define "content"}}
{{with .Data}}
<div class="page-header">
  <h1>Owl &middot; Parties</h1>
  <p class="page-subtitle">RFM rollup over party.decisioning_facts &middot; ordered by 12-month value</p>
</div>

<div style="display:flex;gap:12px;margin-bottom:24px;align-items:center;">
  <form method="GET" action="/owl/parties" style="display:flex;gap:8px;align-items:center;">
    <label style="font-size:11px;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.05em;">Show</label>
    <select name="limit"
      style="padding:6px 10px;background:var(--bg-surface);border:1px solid var(--border-subtle);border-radius:6px;color:var(--text-primary);font-size:13px;outline:none;"
      onchange="this.form.submit()">
      {{range $opt := .LimitOptions}}
      <option value="{{$opt}}"{{if eq $opt $.Limit}} selected{{end}}>{{$opt}}</option>
      {{end}}
    </select>
    <noscript><button type="submit" class="ops-btn ops-btn-primary" style="font-size:12px;padding:6px 14px;">Apply</button></noscript>
  </form>
  <span style="font-size:11px;color:var(--text-muted);margin-left:auto;">{{.PartyCount}} parties</span>
</div>

<div class="ops-card">
  {{if .Parties}}
  <table style="width:100%;border-collapse:collapse;font-size:13px;">
    <thead>
      <tr style="color:var(--text-muted);font-size:11px;text-transform:uppercase;letter-spacing:0.05em;">
        <th style="padding:6px 12px 6px 0;text-align:left;font-weight:500;">Party ID</th>
        <th style="padding:6px 12px;text-align:left;font-weight:500;">Confidence</th>
        <th style="padding:6px 12px;text-align:right;font-weight:500;">Value (12mo)</th>
        <th style="padding:6px 12px;text-align:right;font-weight:500;">Frequency</th>
        <th style="padding:6px 12px;text-align:right;font-weight:500;">Avg Tx</th>
        <th style="padding:6px 12px;text-align:right;font-weight:500;">Recency (d)</th>
        <th style="padding:6px 12px;text-align:left;font-weight:500;">Fraud Risk</th>
        <th style="padding:6px 0;text-align:left;font-weight:500;">Churn Risk</th>
      </tr>
    </thead>
    <tbody>
      {{range .Parties}}
      <tr style="border-top:1px solid var(--border-subtle);">
        <td style="padding:10px 12px 10px 0;font-family:'Space Grotesk',monospace;font-size:11px;color:var(--text-muted);">{{.PartyShort}}</td>
        <td style="padding:10px 12px;color:var(--text-secondary);">{{.Confidence}}</td>
        <td style="padding:10px 12px;text-align:right;color:var(--text-primary);font-weight:600;">{{.PartyValue}}</td>
        <td style="padding:10px 12px;text-align:right;color:var(--text-secondary);">{{.PartyFrequency}}</td>
        <td style="padding:10px 12px;text-align:right;color:var(--text-secondary);">{{.PartyMonetary}}</td>
        <td style="padding:10px 12px;text-align:right;color:var(--text-secondary);">{{.PartyRecency}}</td>
        <td style="padding:10px 12px;color:var(--text-secondary);">{{.PartyFraudRisk}}</td>
        <td style="padding:10px 0;color:var(--text-secondary);">{{.PartyChurnRisk}}</td>
      </tr>
      {{end}}
    </tbody>
  </table>
  {{else}}
  <p style="font-size:13px;color:var(--text-muted);padding:16px 0;">No parties tracked yet. The party.decisioning_facts materialized view rolls up consumers as they appear in transactions.</p>
  {{end}}
</div>
{{end}}
{{end}}
```

- [ ] **Step 4: Wire template + route + handler**

In `New()` (after the `owl_dashboards` line):

```go
	h.mustParse("owl_parties", "templates/owl/parties.html")
```

In `Mount()` (after `/owl/dashboards`):

```go
	r.Get("/owl/parties", h.owlPartiesPage)
```

Append handler after `owlDashboardsPage()`:

```go
// owlPartiesPage renders the tenant's RFM party list, ordered by
// party_value DESC. Reads party.decisioning_facts via DashboardStore.
// Wired W6 / GRO-825.
func (h *Handler) owlPartiesPage(w http.ResponseWriter, r *http.Request) {
	limit := parseOwlLimit(r.URL.Query().Get("limit"), 50)
	view := map[string]any{
		"Limit":        limit,
		"LimitOptions": []int{25, 50, 100, 250, 500},
		"PartyCount":   0,
		"Parties":      nil,
	}

	if h.deps.OwlDashboard != nil {
		ctx := r.Context()
		tenantID := tenantIDFromCtx(ctx)
		parties, err := h.deps.OwlDashboard.ListPartyRFM(ctx, tenantID, limit)
		if err != nil {
			h.logger.Error("owlPartiesPage: list", zap.Error(err))
		} else {
			rows := make([]map[string]any, 0, len(parties))
			for _, p := range parties {
				rows = append(rows, map[string]any{
					"PartyShort":     p.PartyID.String()[:8],
					"Confidence":     p.Confidence,
					"PartyValue":     p.PartyValue,
					"PartyFrequency": p.PartyFrequency,
					"PartyMonetary":  p.PartyMonetary,
					"PartyRecency":   p.PartyRecency,
					"PartyFraudRisk": p.PartyFraudRisk,
					"PartyChurnRisk": p.PartyChurnRisk,
				})
			}
			view["Parties"] = rows
			view["PartyCount"] = len(parties)
		}
	}

	h.render(w, r, "owl_parties", "owl_intel", view)
}

// parseOwlLimit clamps the limit query param to [1, 500] with a fallback.
func parseOwlLimit(raw string, def int) int {
	if raw == "" {
		return def
	}
	n, err := strconv.Atoi(raw)
	if err != nil || n <= 0 {
		return def
	}
	if n > 500 {
		return 500
	}
	return n
}
```

- [ ] **Step 5: Run test**

Run: `cd CanaryGo && go test ./internal/web/ -run TestOwlParties -v`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add CanaryGo/internal/web/handler.go CanaryGo/internal/web/handler_owl_test.go CanaryGo/internal/web/templates/owl/parties.html
git commit -m "feat(web): wire /owl/parties RFM list — GRO-825 W6 (2/3)"
```

---

### Task 5: /owl/lp-performance (LP-rate detail)

**Files:**
- Create: `CanaryGo/internal/web/templates/owl/lp_performance.html`
- Modify: `CanaryGo/internal/web/handler.go`

- [ ] **Step 1: Write the failing test**

Append to `handler_owl_test.go`:

```go
func TestOwlLPPerformance_NoStore_RendersEmptyState(t *testing.T) {
	h := New(Deps{}, nil)
	r := chi.NewRouter()
	h.Mount(r)

	req := httptest.NewRequest(http.MethodGet, "/owl/lp-performance", nil)
	rr := httptest.NewRecorder()
	r.ServeHTTP(rr, req)
	if rr.Code != http.StatusOK {
		t.Fatalf("expected 200 got %d", rr.Code)
	}
	body := rr.Body.String()
	for _, want := range []string{"LP Performance", "No LP-rate data yet"} {
		if !strings.Contains(body, want) {
			t.Errorf("body missing %q", want)
		}
	}
}

func TestOwlLPPerformance_PeriodSelector(t *testing.T) {
	h := New(Deps{}, nil)
	r := chi.NewRouter()
	h.Mount(r)

	for _, period := range []string{"day", "week", "month", "quarter"} {
		req := httptest.NewRequest(http.MethodGet, "/owl/lp-performance?period="+period, nil)
		rr := httptest.NewRecorder()
		r.ServeHTTP(rr, req)
		if rr.Code != http.StatusOK {
			t.Errorf("period=%s: expected 200 got %d", period, rr.Code)
		}
	}
}
```

- [ ] **Step 2: Verify failure**

Run: `cd CanaryGo && go test ./internal/web/ -run TestOwlLPPerformance -v`
Expected: FAIL — 404.

- [ ] **Step 3: Create template**

Create `CanaryGo/internal/web/templates/owl/lp_performance.html`:

```html
{{template "base.html" .}}

{{define "title"}}LP Performance — Canary{{end}}

{{define "content"}}
{{with .Data}}
<div class="page-header">
  <h1>Owl &middot; LP Performance</h1>
  <p class="page-subtitle">Detection volume and case-escalation rate per rule type</p>
</div>

<div style="display:flex;gap:8px;margin-bottom:24px;">
  {{$active := .Period}}
  {{range $kind := .PeriodOptions}}
  <a href="/owl/lp-performance?period={{$kind}}"
     data-period="{{$kind}}"
     class="period-pill{{if eq $kind $active}} active{{end}}"
     style="padding:6px 14px;border-radius:6px;font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;text-decoration:none;border:1px solid var(--border-subtle);{{if eq $kind $active}}background:var(--signal-yellow);color:#0d1117;{{else}}background:var(--bg-surface);color:var(--text-secondary);{{end}}">{{$kind}}</a>
  {{end}}
  <span style="margin-left:auto;font-size:11px;color:var(--text-muted);align-self:center;">
    {{.WindowFrom}} → {{.WindowTo}} UTC
  </span>
</div>

<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:24px;">
  <div class="ops-card" style="text-align:center;">
    <div style="font-size:24px;font-weight:700;color:var(--text-primary);">{{.TotalDetections}}</div>
    <div style="font-size:11px;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.05em;margin-top:4px;">Detections</div>
  </div>
  <div class="ops-card" style="text-align:center;">
    <div style="font-size:24px;font-weight:700;color:var(--accent-blue);">{{.TotalCases}}</div>
    <div style="font-size:11px;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.05em;margin-top:4px;">Cases</div>
  </div>
  <div class="ops-card" style="text-align:center;">
    <div style="font-size:24px;font-weight:700;color:var(--health-green);">{{.OverallEscalation}}</div>
    <div style="font-size:11px;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.05em;margin-top:4px;">Overall Escalation</div>
  </div>
</div>

<div class="ops-card">
  <div style="font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;color:var(--text-muted);margin-bottom:16px;">Per Rule Type</div>
  {{if .Rows}}
  <table style="width:100%;border-collapse:collapse;font-size:13px;">
    <thead>
      <tr style="color:var(--text-muted);font-size:11px;text-transform:uppercase;letter-spacing:0.05em;">
        <th style="padding:6px 12px 6px 0;text-align:left;font-weight:500;">Rule Type</th>
        <th style="padding:6px 12px;text-align:right;font-weight:500;">Detections</th>
        <th style="padding:6px 12px;text-align:right;font-weight:500;">Cases</th>
        <th style="padding:6px 12px;text-align:right;font-weight:500;">Escalation</th>
        <th style="padding:6px 0;text-align:left;font-weight:500;">Drill</th>
      </tr>
    </thead>
    <tbody>
      {{range .Rows}}
      <tr style="border-top:1px solid var(--border-subtle);">
        <td style="padding:10px 12px 10px 0;color:var(--text-primary);">{{.RuleType}}</td>
        <td style="padding:10px 12px;text-align:right;color:var(--text-secondary);">{{.Detections}}</td>
        <td style="padding:10px 12px;text-align:right;color:var(--text-secondary);">{{.Cases}}</td>
        <td style="padding:10px 12px;text-align:right;color:var(--text-primary);font-weight:600;">{{.EscalationPct}}</td>
        <td style="padding:10px 0;"><a href="/alerts?rule_type={{.RuleType}}" style="font-size:11px;color:var(--signal-yellow);text-decoration:none;">Alerts →</a></td>
      </tr>
      {{end}}
    </tbody>
  </table>
  {{else}}
  <p style="font-size:13px;color:var(--text-muted);padding:16px 0;">No LP-rate data yet for this window.</p>
  {{end}}
</div>
{{end}}
{{end}}
```

- [ ] **Step 4: Wire template + route + handler**

In `New()`:

```go
	h.mustParse("owl_lp_performance", "templates/owl/lp_performance.html")
```

In `Mount()`:

```go
	r.Get("/owl/lp-performance", h.owlLPPerformancePage)
```

Append handler:

```go
// owlLPPerformancePage renders LP-rate detail per rule type. Same
// underlying query as the dashboards page (LPRateRollup) but full-table
// view with drill-down to the alert list filtered by rule_type.
// Wired W6 / GRO-825.
func (h *Handler) owlLPPerformancePage(w http.ResponseWriter, r *http.Request) {
	from, to, label := owlPortalPeriod(r.URL.Query().Get("period"), time.Now())
	view := map[string]any{
		"Period":            label,
		"PeriodOptions":     []string{"day", "week", "month", "quarter"},
		"WindowFrom":        from.Format("2006-01-02 15:04"),
		"WindowTo":          to.Format("2006-01-02 15:04"),
		"TotalDetections":   0,
		"TotalCases":        0,
		"OverallEscalation": "0%",
		"Rows":              nil,
	}

	if h.deps.OwlDashboard != nil {
		ctx := r.Context()
		tenantID := tenantIDFromCtx(ctx)
		lp, err := h.deps.OwlDashboard.LPRateRollup(ctx, tenantID, from, to)
		if err != nil {
			h.logger.Error("owlLPPerformancePage: rollup", zap.Error(err))
		} else {
			rows := make([]map[string]any, 0, len(lp))
			var totalDet, totalCase int
			for _, m := range lp {
				rows = append(rows, map[string]any{
					"RuleType":      m.RuleType,
					"Detections":    m.DetectionCount,
					"Cases":         m.CaseCount,
					"EscalationPct": formatPct(m.EscalationRate),
				})
				totalDet += m.DetectionCount
				totalCase += m.CaseCount
			}
			view["Rows"] = rows
			view["TotalDetections"] = totalDet
			view["TotalCases"] = totalCase
			if totalDet > 0 {
				view["OverallEscalation"] = formatPct(float64(totalCase) / float64(totalDet))
			}
		}
	}

	h.render(w, r, "owl_lp_performance", "owl_intel", view)
}
```

- [ ] **Step 5: Run test**

Run: `cd CanaryGo && go test ./internal/web/ -run TestOwlLPPerformance -v`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add CanaryGo/internal/web/handler.go CanaryGo/internal/web/handler_owl_test.go CanaryGo/internal/web/templates/owl/lp_performance.html
git commit -m "feat(web): wire /owl/lp-performance — GRO-825 W6 (3/3)"
```

---

## Chunk 3: Sidebar wiring + integration test

### Task 6: Sidebar Intelligence section

**Files:**
- Modify: `CanaryGo/internal/web/templates/partials/sidebar.html`

- [ ] **Step 1: Add the new section**

In `sidebar.html`, insert a new section between the "Reports" section (lines 82–88) and the "System" section (line 90). Use `Page` key `owl_intel` to match the active-page key set by the three handlers.

```html
    <div class="sidebar-section">
      <div class="sidebar-section-label">Intelligence</div>
      <a href="/owl/dashboards" class="sidebar-item{{if eq .Page "owl_intel"}} active{{end}}" data-color="owl">
        <span class="nav-icon" style="background: var(--nav-chirps);"></span>
        Dashboards
      </a>
      <a href="/owl/parties" class="sidebar-item" data-color="owl">
        <span class="nav-icon" style="background: var(--nav-employees);"></span>
        Parties
      </a>
      <a href="/owl/lp-performance" class="sidebar-item" data-color="owl">
        <span class="nav-icon" style="background: var(--nav-audit);"></span>
        LP Performance
      </a>
    </div>
```

The existing "Owl" entry in the System section (lines 102–105) stays unchanged — it points to `/owl` semantic-search and uses `Page == "owl"`.

- [ ] **Step 2: Verify rendering**

Run: `cd CanaryGo && go test ./internal/web/...`
Expected: all tests still pass. The sidebar template is part of the embed; no Go code changed but the bytes did, so a rebuild + run is enough verification at the unit-test layer.

- [ ] **Step 3: Commit**

```bash
git add CanaryGo/internal/web/templates/partials/sidebar.html
git commit -m "feat(web): add Intelligence sidebar section for owl portal — GRO-825"
```

---

### Task 7: Integration test against real DB

**Files:**
- Modify: `CanaryGo/internal/web/handler_owl_test.go`

- [ ] **Step 1: Add the with-store integration test**

Append:

```go
import (
	"github.com/growdirect-llc/rapidpos/internal/owl"
	"github.com/growdirect-llc/rapidpos/internal/testutil"
)

func TestOwlDashboards_WithStore_RendersAgainstRealDB(t *testing.T) {
	pool := testutil.MustConnect(t)
	deps := Deps{OwlDashboard: owl.NewDashboardStore(pool)}
	h := New(deps, nil)
	r := chi.NewRouter()
	h.Mount(r)

	req := httptest.NewRequest(http.MethodGet, "/owl/dashboards", nil)
	rr := httptest.NewRecorder()
	r.ServeHTTP(rr, req)
	if rr.Code != http.StatusOK {
		t.Fatalf("expected 200 got %d body=%s", rr.Code, rr.Body.String())
	}
	// With the test schema present but no seeded data, both empty-state
	// strings should render — same shape as the no-store path.
	body := rr.Body.String()
	if !strings.Contains(body, "Owl") || !strings.Contains(body, "Dashboards") {
		t.Errorf("expected page header copy")
	}
}

func TestOwlParties_WithStore_RendersAgainstRealDB(t *testing.T) {
	pool := testutil.MustConnect(t)
	deps := Deps{OwlDashboard: owl.NewDashboardStore(pool)}
	h := New(deps, nil)
	r := chi.NewRouter()
	h.Mount(r)

	req := httptest.NewRequest(http.MethodGet, "/owl/parties?limit=25", nil)
	rr := httptest.NewRecorder()
	r.ServeHTTP(rr, req)
	if rr.Code != http.StatusOK {
		t.Fatalf("expected 200 got %d", rr.Code)
	}
}

func TestOwlLPPerformance_WithStore_RendersAgainstRealDB(t *testing.T) {
	pool := testutil.MustConnect(t)
	deps := Deps{OwlDashboard: owl.NewDashboardStore(pool)}
	h := New(deps, nil)
	r := chi.NewRouter()
	h.Mount(r)

	req := httptest.NewRequest(http.MethodGet, "/owl/lp-performance?period=month", nil)
	rr := httptest.NewRecorder()
	r.ServeHTTP(rr, req)
	if rr.Code != http.StatusOK {
		t.Fatalf("expected 200 got %d", rr.Code)
	}
}
```

- [ ] **Step 2: Run the full suite**

Run: `cd CanaryGo && go test ./internal/web/...`
Expected: all tests pass. Integration tests will be skipped if `testutil.MustConnect` cannot reach `canary_gcp_test` — this matches the W7 protocol-portal behavior in `handler_protocol_test.go`.

- [ ] **Step 3: go vet + build full binary**

Run: `cd CanaryGo && go vet ./... && go build ./...`
Expected: clean.

- [ ] **Step 4: Commit**

```bash
git add CanaryGo/internal/web/handler_owl_test.go
git commit -m "test(web): add owl portal real-DB integration tests — GRO-825"
```

---

## Verification

- [ ] **Full test pass:** `cd CanaryGo && go test ./...`
- [ ] **Vet clean:** `cd CanaryGo && go vet ./...`
- [ ] **Build clean:** `cd CanaryGo && go build ./...`
- [ ] **Manual smoke (optional, requires `cmd/web` wiring of `OwlDashboard`):** start the web server and load each of the three URLs in a browser; confirm sidebar highlights for `owl_intel`.

If `cmd/web/main.go` does not yet wire `OwlDashboard` into `web.Deps`, add a one-liner:

```go
deps.OwlDashboard = owl.NewDashboardStore(pool)
```

next to the `ProtocolValidate` / `ProtocolNamespace` wiring (W7 added those). This is a 2-line change covered in the final commit if needed; the new pages still render the empty-state path with `OwlDashboard` nil.

---

## Closeout

Linear comment template for `gh issue close GRO-825`:

```markdown
**Done.** /owl/dashboards, /owl/parties, /owl/lp-performance shipped.

Files: internal/web/handler.go, internal/web/deps.go, three templates under internal/web/templates/owl/, sidebar.html, handler_owl_test.go.

Tests: 9 new tests (period helper × 6, dashboards × 2, parties × 2, lp-performance × 2, real-DB × 3). go vet clean.

Substrate touched: none. /v1/owl/* JSON API surface unchanged.

Scope-cut for follow-on:
- Per-party detection history at /owl/parties/{id}: party.decisioning_facts has no party_id → detection.detections link in the substrate today. Adding it is a substrate change, not a portal change.
- Period selector tz-awareness: portal stays UTC; the merchant-keyed JSON API in cmd/owl carries the tz contract.
- Drill-down from /owl/lp-performance row → /alerts?rule_type=… is wired but only as deep as the alerts list page understands the filter today (W3 work).
```

---

## Notes on intent (for future readers)

This dispatch turns a portal placeholder into three real surfaces over substrate that already exists. The work is mostly template authoring and handler glue; no new SQL, no new aggregations, no new domain model. The W7 protocol-portal commit is the design template — same nil-safe `Deps` field, same empty-state rendering, same KPI-tile + table layout, same `_test.go` shape with no-store / with-store paths.

The substrate split (`Aggregator` is merchant-keyed, `DashboardStore` is tenant-keyed) is intentional and reflects that the JSON API at `/v1/owl/*` serves external callers who carry merchant context, while the portal serves operators who already have tenant context via the request middleware. The portal does not need to cross that bridge.
