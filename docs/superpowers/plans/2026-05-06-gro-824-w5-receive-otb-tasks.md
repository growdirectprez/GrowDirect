# GRO-824 W5 — Receiving / OTB / Tasks Workflow Surfaces

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Wire the operator-facing POST surfaces over engines that already exist — receiving close (with three-way-match workflow trigger), receiving line discrepancy, directed-task queue page, OTB report read + period lock, and suggested-orders placeholder POSTs.

**Architecture:** Six new POST handlers + one new GET page (`/tasks`) on the existing chi router in `internal/web/`. Three new optional `Deps` fields (`TaskStore`, `WorkflowStore`, `BillingStore`) — same nil-safe shape as W6/W7. Three new write methods on existing stores: `inventory.Store.UpdateDocumentStatus`, `inventory.Store.MarkLineDiscrepancy`, `billing.Store.UpdateBudgetStatus`. One new read helper on workflow store: `Store.GetDefinitionByCode(code, version)` to resolve `three_way_match` → `workflow_id` at handler-time.

**Tech Stack:** Go 1.22 · Chi v5 · pgx/v5 · existing `internal/task`, `internal/inventory`, `internal/workflow`, `internal/billing` packages · existing `internal/web` portal scaffolding.

---

## Scope clarification

The dispatch's six "Done when" lines map to concrete surfaces as follows:

| Done-when | Implementation |
|---|---|
| `/receiving/*` POST: claim task, complete line, mark discrepancy | `POST /receiving/{id}/close` (close action, triggers workflow), `POST /receiving/{id}/lines/{lineID}/discrepancy` (mark variance). "Claim task" is the directed-task queue claim — covered by `/tasks/{id}/claim`. |
| `/orders/suggested` POST: approve / reject / send to vendor | `POST /orders/suggested/{id}/approve`, `.../reject`, `.../send`. No backing PO store today (W11 is out of scope per backlog) — handlers redirect with flash, persisting nothing. |
| `/reports/otb` real calculation with action buttons | GET wires to `billing.Store.ListBudgets`. `POST /reports/otb/{budgetID}/lock` flips status active → locked via new `billing.Store.UpdateBudgetStatus`. "Re-run" is purely a UI cue — there's no client-side OTB calc to recompute; the budget rows are already authoritative. |
| Directed-task queue surfaces | New `GET /tasks` page over `task.Store`. POSTs: `/tasks/{id}/claim`, `/tasks/{id}/complete`, `/tasks/{id}/exception`. |
| Workflow integration: receiving close triggers three-way-match | `POST /receiving/{id}/close` calls `workflow.Store.GetDefinitionByCode("three_way_match", 1)` then `KickOff` with `external_ref=<doc_number>` and `initial_context={"goods_receipt_id": "...", "tenant_id": "..."}`. |
| Tests cover full receive → OTB flow | Unit tests against the mounted router with optional stores nil for empty-state, plus real-DB integration where the schema matters (close + discrepancy + budget lock). |

**What's out of scope (per dispatch):**
- New directed task types — there are three (receiving / replenishment / cycle_count) and we use the existing receiving type only.
- Vendor integration for actual order send — `POST /orders/suggested/{id}/send` is placeholder.

**What's not in the dispatch but worth flagging:**
- "Re-run OTB" with no client-side calc engine is a UI placeholder. Real merchandising OTB (planned receipts vs commitments vs on-hand) is a different concept from `ledger.l402_otb_budgets` (the L402 satoshi spend gate). Per `internal/billing/dto.go` the only OTB substrate today is the L402 budgets. The dispatch's reference card `canary-l402-otb.md` and the existing schema agree — `/reports/otb` reads L402 budgets. Merchandising OTB lives in W11 territory.

---

## File structure

**Modify:**

- `CanaryGo/internal/inventory/document.go` — `UpdateDocumentStatus(tenantID, id, status, performedBy)` and `MarkLineDiscrepancy(tenantID, lineID, reason)` write methods.
- `CanaryGo/internal/billing/store.go` — `UpdateBudgetStatus(tenantID, id, status)` method (active ↔ locked).
- `CanaryGo/internal/workflow/workflow.go` — `GetDefinitionByCode(code string, version int)` helper.
- `CanaryGo/internal/web/deps.go` — three new fields: `TaskStore *task.Store`, `WorkflowStore *workflow.Store`, `BillingStore *billing.Store`.
- `CanaryGo/internal/web/handler.go` — register one template (`tasks`), six new routes, six new handlers, OTB GET wiring.
- `CanaryGo/internal/web/templates/receiving/detail.html` — discrepancy buttons per line.
- `CanaryGo/internal/web/templates/receiving/close.html` — close action button.
- `CanaryGo/internal/web/templates/reports/otb.html` — real budget rows + lock button.
- `CanaryGo/internal/web/templates/reports/suggested_orders.html` — approve/reject/send buttons.
- `CanaryGo/internal/web/templates/partials/sidebar.html` — Tasks link in Ops section.
- `CanaryGo/cmd/gateway/main.go` — wire `TaskStore`, `WorkflowStore`, `BillingStore` into `webDeps`.

**Create:**

- `CanaryGo/internal/web/templates/tasks.html` — directed-task list with claim/complete/exception buttons.
- `CanaryGo/internal/web/handler_w5_test.go` — tests (no-store empty state, with-store real DB).

**Untouched:**

- `internal/task/handler.go` — existing JSON API stays. Portal handlers will reuse `task.Store` directly.
- `internal/replenishment/` — Min/Max trigger is a stream consumer (cmd/bull); the portal doesn't talk to it.
- `internal/workflow/three_way_match.go` — `RegisterThreeWayMatch` already exists; gateway boot already registers (assumed; verify in Task 7).

---

## Execution order

Each chunk is an independent commit. Order chosen so each step compiles + tests pass without depending on later work.

### Chunk 1: Substrate writes

- **Task 1:** `inventory.Store.UpdateDocumentStatus` + `MarkLineDiscrepancy` + tests.
- **Task 2:** `billing.Store.UpdateBudgetStatus` + tests.
- **Task 3:** `workflow.Store.GetDefinitionByCode` + tests.

### Chunk 2: Deps wiring (no behavior change)

- **Task 4:** Add three optional Deps fields. Build verifies.

### Chunk 3: Receiving POSTs (close + discrepancy)

- **Task 5:** `POST /receiving/{id}/close` — calls `UpdateDocumentStatus` + workflow KickOff. Updates `receiving/close.html` to render an action form.
- **Task 6:** `POST /receiving/{id}/lines/{lineID}/discrepancy` — calls `MarkLineDiscrepancy`. Updates `receiving/detail.html` with per-line buttons.

### Chunk 4: Tasks page + POSTs

- **Task 7:** New `tasks.html` template + `GET /tasks` handler listing pending tasks.
- **Task 8:** `POST /tasks/{id}/claim`, `/tasks/{id}/complete`, `/tasks/{id}/exception` — call `task.Store` methods.

### Chunk 5: OTB report

- **Task 9:** Wire `GET /reports/otb` to real budgets via `billing.Store.ListBudgets`. Update `reports/otb.html`.
- **Task 10:** `POST /reports/otb/{budgetID}/lock` — toggles status via `UpdateBudgetStatus`.

### Chunk 6: Suggested orders placeholder

- **Task 11:** `POST /orders/suggested/{id}/approve`, `.../reject`, `.../send` — three thin handlers that 302-redirect with a flash query param. Update `reports/suggested_orders.html` with action buttons.

### Chunk 7: Sidebar + gateway

- **Task 12:** Add "Tasks" link to `sidebar.html` Ops section.
- **Task 13:** Wire `TaskStore`, `WorkflowStore`, `BillingStore` into `cmd/gateway/main.go` `webDeps`.

### Chunk 8: Final verification

- **Task 14:** Full `go test ./...`, `go vet ./...`, `go build ./...`. Push branch, close ticket.

---

## Test strategy

Same shape as W6 (W7 protocol-portal pattern):

- **No-store path** — handler returns 200 with empty-state copy when relevant Deps field is nil.
- **With-store path** — connects to `canary_gcp_test`, exercises the new write methods (close → status update, mark discrepancy → variance_reason, lock → status flip).
- **Workflow trigger** — close-receiving handler calls KickOff; integration test asserts a row lands in `app.workflow_executions` with `external_ref` matching the document number.

Tests live in `internal/web/handler_w5_test.go` plus inline `_test.go` for the three new store methods (`inventory/document_w5_test.go`, `billing/store_w5_test.go`, `workflow/workflow_w5_test.go`).

---

## Notes on intent

This dispatch turns engines that already work in headless mode (replenishment trigger, directed-task queue, three-way-match registration, OTB budgets) into operator-clickable surfaces. The work is mostly POST-handler glue + small store-write methods to fill the remaining write gaps, plus a tasks list page that mirrors the existing JSON API but in HTML form.

Three architectural calls reflected in this plan:
1. **Re-use the existing tenant-scoped pattern from W6.** Every POST takes `tenantID` from `tenantIDFromCtx(r.Context())` — same as `alertListPage` and the W6 portal handlers.
2. **Don't build a real PO model for `/orders/suggested`.** W11 owns suppliers/POs; W5's role is the placeholder UI gesture.
3. **Workflow KickOff at receiving close, not full advance.** `RegisterThreeWayMatch` is registration-only per its comment; full step evaluation is Wave C. Kicking off the execution row is the right level of integration for W5.
