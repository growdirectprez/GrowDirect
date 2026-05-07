# GRO-827 W8 — Asset + Billing Portal Plan

> **For agentic workers:** Use superpowers:subagent-driven-development or superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Five read-only operator surfaces — asset registry, asset detail, billing overview, invoices, payment method — over `internal/asset` and `internal/billing` substrate. No CRUD; per dispatch, asset/plan management is W9 territory.

**Architecture:** Five GET pages on the existing chi router. One new optional `Deps` field (`AssetStore *asset.Store`); `BillingStore` already wired (W5). All five surfaces nil-safe with empty-state copy.

**Tech Stack:** Go 1.22 · Chi v5 · existing `internal/asset`, `internal/billing` packages.

---

## Substrate reality check

The dispatch's "Done when" line `/assets — registry per tenant: devices, locations, equipment, services` describes a hardware/asset taxonomy that lives in the capability card (`Brain/wiki/cards/canary-asset.md` → `app.assets`, `app.asset_lifecycle_events`, `app.asset_types`). **None of those tables exist in the migrations today.** What `internal/asset/` actually wraps is `inventory.inventory_positions` + `catalog.items` — an inventory-positions reader.

Pragmatic call: ship `/assets` as an inventory-positions registry. Document the naming gap in the close-out so a future dispatch can build the hardware-asset substrate when it lands.

For invoices: there is no `invoices` table today either. `ledger.ildwac_positions` carries an `invoiced_at` field that the L402 charge-cycle workflow stamps. `/billing/invoices` renders an aggregate view of invoiced/unbilled position groups — not individual invoice documents — and links to /protocol portal for per-charge audit.

For `/billing/payment-method`: LNURL is the wallet binding (`internal/auth/lnurl`). Read-only display of the linked key for the tenant.

These three skip-cuts are pre-authorized by the dispatch's "Out of scope" list (no CRUD, no plan upgrade, no invoice engine work).

---

## File structure

**Modify:**
- `internal/web/deps.go` — add `AssetStore *asset.Store`.
- `internal/web/handler.go` — register 5 templates, mount 5 routes.
- `internal/web/templates/partials/sidebar.html` — add Assets + Billing entries.
- `cmd/gateway/main.go` — wire `AssetStore`.

**Create:**
- `internal/web/handler_w8.go` — five GET handlers (list, detail, billing overview, invoices, payment-method).
- `internal/web/templates/assets/list.html`
- `internal/web/templates/assets/detail.html`
- `internal/web/templates/billing/overview.html`
- `internal/web/templates/billing/invoices.html`
- `internal/web/templates/billing/payment_method.html`
- `internal/web/handler_w8_test.go` — 5 no-store empty-state tests + 1 status filter test.

**Untouched:**
- `internal/asset/`, `internal/billing/`, `internal/auth/lnurl/` — read-only.

---

## Quality gates

- `go test ./...` clean.
- `go vet ./...` clean.
- `go build ./...` clean.
- All 5 routes return 200 with empty-state copy when stores are nil.
- Sidebar updated.

---

## Closeout note

Document in the Linear comment:
- "asset" semantic today = inventory positions; hardware-asset registry is future work (no `app.assets` migration today).
- `/billing/invoices` shows invoiced/unbilled position groups since there is no invoice document table; per-charge audit lives at `/protocol`.
- `/billing/payment-method` is read-only; rotation/connect flow stays at `/connect`.
