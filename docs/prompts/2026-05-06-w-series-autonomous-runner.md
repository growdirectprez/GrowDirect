# Canary.GO W-Series Autonomous Runner

**Purpose:** Grind through the remaining W-series Canary.GO portal dispatches (W8 → W16) using the same working pattern that shipped W5 and W6. One ticket per session, full lifecycle (read substrate → plan → implement → test → commit → push → close), then move to the next. No human handoff between tickets unless something genuinely blocks.

**How to invoke:**
- **One-shot:** paste this whole file as a fresh prompt; the agent grinds through every Ready ticket in priority order until the queue is empty or a hard block is hit.
- **Cron / loop:** `/loop 30m <paste this file>` — the agent fires every 30 min, picks up exactly one ticket if any are Ready, ships it, and goes back to sleep. (`<<autonomous-loop-dynamic>>` works too if you'd rather let the agent self-pace.)

---

## Operating Posture

You are running unattended. The user has authorized you to:
- Move Linear dispatches through the lifecycle (Todo / Backlog → In Progress → Done) and post dispatch comments without per-ticket confirmation.
- Add fields to `internal/web/deps.go`, write methods to existing stores (`internal/inventory`, `internal/billing`, `internal/task`, `internal/workflow`, etc.), new handler shards (`internal/web/handler_w<N>.go`), new templates, sidebar updates, and `cmd/gateway/main.go` wiring without per-change confirmation.
- Push the working branch after each ticket. **Do not merge to main, do not open PRs**, do not force-push, do not modify CI/CD.
- Skip-cut to a placeholder when the substrate genuinely doesn't exist for a "Done when" line, document the gap in the close-out comment, and continue.

You are NOT authorized to:
- Build a new substrate package from scratch unless the dispatch explicitly asks for it (W11 is the only one that does in this batch).
- Modify code outside the Canary.GO scope (no Cove/, Angel/, Brain/, etc.).
- Add new MCP servers, change Docker compose, or touch CI/CD config.
- Refactor or "clean up" code that isn't in the dispatch scope.
- Skip tests. Every commit must build and every new POST handler needs at minimum a no-store empty-state / 303-redirect contract test.

If you hit a real block (build error you can't fix, test failure you can't reproduce, missing schema/migration the dispatch implicitly assumes, ambiguity that would change the architecture), **stop**, comment on the Linear issue with what you tried and what's blocking, leave the issue in `In Progress`, and exit. The user picks it up from there.

---

## Working Branch

The current branch is **`claude/ecstatic-bell-2ace85`** (laptop worktree at `/Users/gclyle/GrowDirect/.claude/worktrees/ecstatic-bell-2ace85`). It already carries W5 (GRO-824) and W6 (GRO-825). New work continues on this branch — do not create a new branch per ticket; do not rebase. Each ticket gets its own commit(s) and a single `git push`.

If `git status` shows anything uncommitted at session start, treat that as a hand-off in progress: read the diff, decide whether it's mid-work for one of the W-series tickets you're about to pick up, and either continue or commit-then-continue. Do not blow it away.

---

## Ticket Queue

Pick up tickets in this exact order. Each is in the `Canary.GO` project on the `Growdirect` Linear team (status `Backlog` unless noted; all labeled `laptop`, `ALX`, `Feature` unless noted).

| # | Ticket | Title | Difficulty | Notes |
|---|---|---|---|---|
| 1 | [GRO-827](https://linear.app/growdirect/issue/GRO-827) | W8: Asset + Billing portal | Medium | Portal-over-existing-substrate. `internal/asset` + `internal/billing` already exist with stores + handlers. |
| 2 | [GRO-828](https://linear.app/growdirect/issue/GRO-828) | W9: Compliance + Admin (audit, ISO27001, tax, users) | Medium | Same shape as W8. Audit log viewer, ISO27001 controls dashboard, tax report (real data this time), user admin (depends on identity middleware — that's still GRO-769; ship users page as a thin tenant-scoped read). |
| 3 | [GRO-829](https://linear.app/growdirect/issue/GRO-829) | W10: Multi-store intelligence | Medium | Hierarchy admin + cross-store dashboards + network integrity surface + store switcher. Reuse aggregation primitives in `internal/owl` where useful; do NOT add new ones. |
| 4 | [GRO-830](https://linear.app/growdirect/issue/GRO-830) | W11: Supplier + Purchase Order lifecycle | **High — NEW MODULE** | This is net-new code: `internal/supplier/` and `internal/po/`. Pgx store + handler + tests, plus portal pages + actions. Plan accordingly — this ticket is roughly 2× the others. |
| 5 | [GRO-832](https://linear.app/growdirect/issue/GRO-832) | W13: Onboarding wizard | Medium | 4-step wizard. Reuses existing `/connect` (Square OAuth), config import progress, default rule pack seed, welcome dashboard. |
| 6 | [GRO-833](https://linear.app/growdirect/issue/GRO-833) | W14: Mobile / Android POS UX | Medium | Mobile-first responsive cut of the directed-task surfaces (`/m/tasks`, `/m/receiving`, `/m/cycle-count`, `/m/alerts/{id}`). Reuses W5 substrate; new templates only. |
| 7 | [GRO-834](https://linear.app/growdirect/issue/GRO-834) | W15: Ecom channel surface | Low (build last) | New `internal/ecom/` adapter shape mirroring `internal/squareauth/`. Skip-cut to channel-aware order ingestion + sync health view; defer Shopify SDK wiring. |
| 8 | [GRO-835](https://linear.app/growdirect/issue/GRO-835) | W16: Cross-domain case management capstone | Low | Wires up the 5 currently-stub case routes (`casesNewPage`, `casesEvidencePage`, etc.) over `internal/casemgmt`. Final capstone — assumes everything before it has shipped. |

When all eight are Done (or you exit on a block), your work is finished. Do not invent a "W17"; do not pull in non-W tickets; do not file new dispatches as follow-ons unless one is genuinely needed for safety/correctness (a real bug surfaced mid-implementation).

---

## Per-Ticket Lifecycle

For each ticket, run this exact sequence:

### 1. Pick up

- Linear: `save_issue` → state `In Progress` (state id `bf1984d9-ca85-4030-9548-97bbee727381`).
- Linear: `save_comment` with a short pickup note that names the branch and the planned scope. Same shape as W5/W6 pickup comments. ≤200 words.

### 2. Read the substrate

Read every package the dispatch's "Done when" lines reference. Do not skip. Examples for the upcoming tickets:

- W8: `internal/asset/`, `internal/billing/` (handler.go, store.go, dto.go).
- W9: `internal/protocol/audit/`, plus look for ISO27001 + tax-related code via grep.
- W10: `internal/web/templates/partials/sidebar.html` (where store-switcher lives), `internal/owl/` for cross-store reuse.
- W11: `Brain/wiki/cards/canary-purchase-order-lifecycle.md`, then grep for any pre-existing `supplier_*` / `purchase_order_*` schema in `deploy/migrations/`.
- W13: `internal/web/handler.go` `/connect` and `/welcome` handlers; `internal/squareauth/`.
- W14: existing `/tasks`, `/receiving`, `/cases` handlers and templates.
- W15: `internal/squareauth/` (interface model), `cmd/owl/` for sync-health pattern.
- W16: `internal/casemgmt/` plus stub handlers in handler.go (search `casesNewPage`).

If a referenced reference card exists at `Brain/wiki/cards/<name>.md`, skim it. Don't guess from the card title.

### 3. Plan

Write a tight plan to `docs/superpowers/plans/2026-05-06-gro-XXX-w<N>-<slug>.md`. Keep it under ~400 lines (W5's plan is the right reference — W6's was longer than necessary). The plan must include:

- Scope clarification: how each "Done when" line maps to a concrete handler / template / store method.
- File structure (modify / create) with exact paths.
- Execution chunks (each → one logical commit).
- An honest list of out-of-scope cuts. If any cut would surprise the user, note it explicitly.

### 4. Implement

Follow the W5/W6 pattern:
- New handlers go in a sharded file `internal/web/handler_w<N>.go` (precedent: `handler_w5.go`, `handler_lp_settings.go`). Don't grow `handler.go`.
- New templates land under `internal/web/templates/<scope>/<name>.html`. Use the existing design language: `ops-card`, `page-header`, period pills, badge styles. Don't invent a new visual vocabulary.
- New `Deps` fields are nil-safe and render an empty-state path when the store is nil. Same shape as `OwlDashboard`, `TaskStore`, `BillingStore`.
- All POST handlers redirect with `?flash=<verb>` and 303 status.
- Sidebar: add new pages to the appropriate section; mirror the "Intelligence" section pattern from W6 if a new section is warranted.
- `cmd/gateway/main.go`: add the new store wiring inside the existing `webDeps := web.Deps{...}` literal. No new env vars, no new config knobs.

Do not add `_test.go` integration tests against `canary_gcp_test` for surface that doesn't have schema yet (W11's supplier table will need a migration; if you can't write+run the migration cleanly in the autonomous loop, ship the store + handler + no-store tests and file the migration as a follow-on).

### 5. Test

Every new handler needs at minimum:
- A no-store empty-state test (`Deps{}` with relevant field nil).
- A 303-redirect contract test for any POST handler.
- For complex GET handlers, a status/filter selector test (W6 period selector is the reference).

Run: `DATABASE_URL="postgres://growdirect:growdirect_dev@localhost:5432/canary_gcp_test?sslmode=disable" VALKEY_URL=redis://:valkey_dev@localhost:6379/2 SESSION_SECRET="test-session-secret-at-least-32-bytes!" go test ./...`

Vet: `go vet ./...`. Build: `go build ./...`. All must be clean before commit. Do not run `go test -tags=integration` — that's the heavyweight suite and is not in scope for this loop.

### 6. Commit + push + close

- Single commit (or 2–3 if substrate writes + portal wiring are clearly separate logical units). Subject: `feat(scope): <verb> — GRO-XXX W<N>`.
- Body: one short paragraph + bullet list of files touched. Always include `Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>`.
- `git push` (no `--force`, no `--force-with-lease`).
- Linear: `save_comment` with the artifact comment in the same shape as the W5/W6 closeouts (Done summary table + files + tests + plan link + scope-cut). Then `save_issue` → state `Done` (state id `d6795b15-1452-4b57-92f3-ac36c566b66e`).
- Move on to the next ticket. Do not stop to summarize the batch unless you've hit the last ticket.

---

## Quality Gates (must hold per ticket)

- `go test ./...` exits 0 with all packages reporting `ok`.
- `go vet ./...` produces no output.
- `go build ./...` produces no output.
- New routes pass `tenantIDFromCtx` (no merchant_id-keyed handlers in the portal — that contract belongs to the JSON API surface).
- New POST handlers parse forms, redirect with `flash=`, never 500 on a missing dep (always nil-safe with `?flash=no_store`).
- No raw SQL in `cmd/`. Direct pgx + inline SQL is fine in `internal/<store>` packages per `CanaryGo/CLAUDE.md`'s amended sqlc rule.
- Sidebar updated if the surface is operator-facing.
- No new dependencies (`go get`, `go.mod` changes) without an explicit dispatch sign-off — none of these tickets need new deps; if you think one does, that's a flag to escalate.

---

## Project Patterns (cheat sheet)

**Handler shard file template** (use as a starting point for `handler_w<N>.go`):

```go
// internal/web/handler_w<N>.go
//
// W<N> / GRO-XXX — <one-line summary>.

package web

import (
	"errors"
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/google/uuid"
	"go.uber.org/zap"
)

func (h *Handler) <foo>Page(w http.ResponseWriter, r *http.Request) {
	view := map[string]any{
		"Flash": r.URL.Query().Get("flash"),
		"Items": nil,
	}
	if h.deps.<X>Store != nil {
		// ...read, populate view...
	}
	h.render(w, r, "<tmpl>", "<active_page>", view)
}

func (h *Handler) <foo>Action(w http.ResponseWriter, r *http.Request) {
	id, err := uuid.Parse(chi.URLParam(r, "id"))
	if err != nil {
		http.Error(w, "invalid id", http.StatusBadRequest)
		return
	}
	if h.deps.<X>Store == nil {
		http.Redirect(w, r, "/<scope>?flash=no_store", http.StatusSeeOther)
		return
	}
	if err := r.ParseForm(); err != nil {
		http.Error(w, "invalid form", http.StatusBadRequest)
		return
	}
	tenantID := tenantIDFromCtx(r.Context())
	// ...store call...
	if errors.Is(err, <Pkg>.ErrNotFound) {
		w.WriteHeader(http.StatusNotFound); h.render(w, r, "err404", "<active_page>", nil); return
	}
	if err != nil {
		h.logger.Error("<foo>Action", zap.Error(err))
		http.Redirect(w, r, "/<scope>?flash=error", http.StatusSeeOther)
		return
	}
	http.Redirect(w, r, "/<scope>?flash=<verb>", http.StatusSeeOther)
	_ = id
}
```

**Template skeleton** (page-level, reusing the design language):

```html
{{template "base.html" .}}
{{define "title"}}<Title> — Canary{{end}}
{{define "content"}}
{{with .Data}}
<div class="page-header">
  <h1><Title></h1>
  <p class="page-subtitle"><One-line subtitle></p>
</div>
{{if .Flash}}
<div style="margin-bottom:16px;padding:10px 14px;background:rgba(234,179,8,0.08);border:1px solid var(--signal-yellow);border-radius:6px;font-size:12px;color:var(--signal-yellow);">
  Action: {{.Flash}}
</div>
{{end}}
<div class="ops-card">
  {{if .Items}}
  <!-- table -->
  {{else}}
  <p style="font-size:13px;color:var(--text-muted);padding:16px 0;">No data yet.</p>
  {{end}}
</div>
{{end}}
{{end}}
```

**Test pattern** (see `internal/web/handler_w5_test.go` and `handler_owl_test.go` for full examples):

```go
func Test<Foo>_NoStore_RendersEmptyState(t *testing.T) {
	h := New(Deps{}, nil); r := chi.NewRouter(); h.Mount(r)
	req := httptest.NewRequest(http.MethodGet, "/<path>", nil)
	rr := httptest.NewRecorder(); r.ServeHTTP(rr, req)
	if rr.Code != http.StatusOK { t.Fatalf("expected 200 got %d", rr.Code) }
	if !strings.Contains(rr.Body.String(), "No <thing> yet") { t.Errorf("missing empty-state copy") }
}
```

---

## Standing Constraints

These come from CLAUDE.md / AGENTS.md / user feedback memory and apply across every ticket:

- **Build, don't organize.** Ship features, not scaffolding.
- **Code is ahead of SDDs.** Use `Brain/wiki/cards/` (capability cards) as the spec surface, not `docs/sdds/go-handoff/`.
- **No hand-rolling outside core IP.** If a "Done when" line implies a generic infra concern (auth, cache, queue), use what's already wired.
- **No volatile data in wiki.** Don't write counts/stats into Brain markdown. Code is the inventory.
- **Skip MVP/v1 scope debates.** Build the full surface and let navigation control exposure.
- **Stop overproducing artifacts.** When a dispatch closes, close it — don't file three follow-on tickets unless something specific is broken.
- **Professional tone.** Direct and substantive in commit messages and Linear comments. No casual energy. No "great work!" / "exciting!" / hype phrasing.
- **Founder communication is conversational.** If you do need to surface something to the user (a real block), keep it tight: one paragraph, what's blocking, what you tried, what you'd recommend.

---

## Memory Bus (optional, not required)

Memory bus is reachable at `http://127.0.0.1:8003/mcp` via the registered `memory-bus` MCP. Use `memory_recall` if you need ground truth from a wiki article and grep over the local files isn't surfacing it. Don't use it as a primary source — read the file directly when you can.

If the memory bus is down, that's not a block for this loop. Continue. The loop touches portal code, not memory-bus internals.

---

## Exit Conditions

You're done when one of these is true:
1. **All eight tickets are Done.** Post a summary comment on GRO-826 (the W7 protocol portal — closest spiritual sibling) noting the W-series march completed and which commits land where. Then exit.
2. **You hit a hard block on a ticket.** Leave that ticket in `In Progress` with a block comment, do not pick up the next ticket, and exit. The user picks it up.
3. **A safety rule trips.** If you find yourself wanting to do something that isn't authorized above (open a PR, modify CI, install a new dependency, refactor unrelated code), stop and ask. Do not work around the rule.

When you exit cleanly, output a single short message that:
- Lists tickets closed this run (with GRO links).
- Lists tickets remaining (if any).
- Names the branch tip SHA.

That's the entire deliverable. The user reads the Linear comments, reviews the diff at their pace, and merges (or asks for changes) outside this loop.
