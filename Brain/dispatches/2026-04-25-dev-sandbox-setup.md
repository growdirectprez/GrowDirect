---
type: dispatch
status: ready-for-execution
date: 2026-04-25
target: agent team running Canary Counterpoint adapter dev sandbox setup
priority: medium-high (unblocks Phase 0-4 build work)
recommended-path: mock-first
gates-on: nothing — start today
phase-fit: prerequisite for Phase 0 (TSP/CRDM/Counterpoint adapter shell)
tags: [dev-sandbox, mock-server, openapi, counterpoint, phase-0-prereq]
---

# Dispatch — Canary Counterpoint Dev Sandbox Setup

## TL;DR

Build the Counterpoint TSP adapter against an OpenAPI mock server, NOT against a live Counterpoint Windows installation. The mock-first path unblocks Phase 0-4 dev work today; the real Windows sandbox is a Phase 5 cutover-validation concern, not a Phase 0 blocker.

**Why mock-first:** the OpenAPI 3.0 spec at `docs/sdds/canary/ncr-counterpoint-openapi.yaml` is validated, contract-complete (95 operations, 71 paths, 49 schemas), and good enough for adapter scaffolding + fixture-driven testing. Real Counterpoint behavior surfaces during Phase 5 when we hit a customer's actual instance. NCR Voyix is a competitor (per memory `project_ncr_voyix_is_competitor.md`); minimizing NCR-side dependencies is strategically correct.

## Inputs (everything the agent team needs is on disk)

| What | Where | Use |
|---|---|---|
| OpenAPI 3.0 spec | `docs/sdds/canary/ncr-counterpoint-openapi.yaml` | Mock server source; adapter contract |
| Counterpoint API source corpus | `Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/` | Cross-reference; sample payloads in endpoint docs |
| SDD (architecture + module mappings) | `docs/sdds/canary/ncr-counterpoint-retail-spine-integration.md` | What the adapter targets |
| Endpoint × spine map | `Brain/wiki/ncr-counterpoint-endpoint-spine-map.md` | Per-endpoint coverage detail |
| Document model | `Brain/wiki/ncr-counterpoint-document-model.md` | Document omnibus type-routing logic |
| Connection runbook | `Brain/wiki/ncr-counterpoint-connection-runbook.md` | Auth bootstrap (for real-instance work later) |
| API reference | `Brain/wiki/ncr-counterpoint-api-reference.md` | Catalog + caching + LIN_TYP + Store config detail |

## Path A — Mock server (RECOMMENDED, start today)

### Step 1 — Stand up Prism mock from the OpenAPI spec

```bash
# From repo root
npx @stoplight/prism-cli mock docs/sdds/canary/ncr-counterpoint-openapi.yaml
# Mock listens on http://localhost:4010 by default
```

Verifies: spec parses; mock returns spec-conformant sample data per endpoint.

### Step 2 — Adapter scaffolding

Generate Python client from the OpenAPI spec OR write the adapter by hand against the contract. Either works.

```bash
# Optional: openapi-generator route
npx @openapitools/openapi-generator-cli generate \
  -i docs/sdds/canary/ncr-counterpoint-openapi.yaml \
  -g python \
  -o services/canary-tsp/counterpoint_client
```

Adapter targets the priority subset (~25 of 95 endpoints per SDD §10):

- `Customer*`, `CustomerControl`, `Customer_Address`, `Customer_Note`, `Customer_OpenItems` — Module R
- `Document` (GET single), `Document_Lines`, `Document_Note`, `Document_Contact`, `Document_Payments` — Module T (omnibus)
- `Item`, `Items`, `ItemCategories`, `Item_Inventory`, `Inventory_*` — Module S
- `Store`, `Store_Station`, `Device_Config`, `Workgroup` — Module N
- `PayCode`, `PayCodes`, `TaxCodes`, `GiftCard*` — Module F
- `VendorItem` — Module J support

### Step 3 — Fixture-driven tests

For every priority endpoint, the source-corpus `Endpoints/<NAME>.md` file contains a `Sample Response Body` JSON block. Extract those into JSON fixtures.

```bash
# Fixture extraction script — run once
python3 scripts/extract-counterpoint-fixtures.py \
  --source Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/Endpoints \
  --output services/canary-tsp/tests/fixtures/counterpoint
```

Then drive adapter tests off the fixtures. Catches schema-level issues without needing a live server.

### Step 4 — CRDM mapping verification

Adapter writes go into Canary's CRDM. Per SDD §4 + spine-map wiki, every priority endpoint maps to specific CRDM entities. Tests verify:

- Idempotency: replay same fixture → no duplicate CRDM rows
- Type-routing: `Document` with different `DOC_TYP` codes routes to correct CRDM event entity (`Events.transactions` vs `Events.transfers` vs `Events.purchase_orders`)
- Multi-tenancy: per-tenant `tenant_id` × `counterpoint_company_alias` isolation

### Step 5 — Smoke flow against the mock

End-to-end: mock server returns sample → adapter ingests → CRDM populated → MCP tool surface returns expected shape. No NCR involvement.

## Path B — Real Windows sandbox (DEFERRED)

Stand up a Windows VM + Counterpoint API server + test database. **Not needed for Phase 0-4 work.**

Activate this path only if/when:
- Bart shares developer credentials (per Monday call) — gives access to a real Counterpoint instance
- Phase 5 cutover validation needs real-customer data behavior verification
- Spec-vs-reality discrepancies surface during mock-driven dev that need live-server verification

If activated, follow `Brain/wiki/ncr-counterpoint-sandbox-setup-checklist.md` (deferred-actions section) and `Brain/wiki/ncr-counterpoint-connection-runbook.md` (technical bring-up).

## Path C — Bart's developer credentials (CONTINGENT)

If Bart shares his APIKey + access to a customer's Counterpoint API server (Monday call outcome), Canary's adapter points at his customer's real instance via SSH-tunneled HTTPS or Cloudflare Tunnel. Skips the standalone Windows sandbox entirely.

This is the **cleanest production-validation path** and bypasses the NCR-direct APIKey-application risk (NCR Voyix is competitive; their APIKey approval is manual review).

## What NOT to do

- Do NOT submit an APIKey application to NCR Voyix yet. Wait for Monday's outcome with Bart. If he shares his APIKey or sponsors us under his VAR umbrella, the NCR direct application becomes unnecessary or can be framed neutrally afterward.
- Do NOT request FTP test DB credentials from NCR. Mock-first path skips this.
- Do NOT provision a Windows cloud VM yet. Defer until Path B / C are needed.
- Do NOT modify the OpenAPI YAML or source-corpus files. They're read-only inputs.
- Do NOT commit code without code review. Adapter quality matters; rule-driven LP downstream depends on adapter correctness.

## Acceptance criteria (Phase 0 sandbox readiness)

- [ ] Prism mock server running locally; returns spec-conformant data for all priority endpoints
- [ ] Adapter scaffolding (manual or generated) compiles + connects to mock
- [ ] Fixture suite extracted from source-corpus sample payloads (~25 endpoints)
- [ ] Adapter end-to-end test: mock → adapter → CRDM → MCP tool returns expected shape
- [ ] Document type-routing tested for at least 3 DOC_TYP codes (T, XFER, PO)
- [ ] Idempotency verified (replay produces no duplicates)
- [ ] Multi-tenancy verified (two simulated tenants don't bleed)
- [ ] Documentation: a `services/canary-tsp/README.md` describing local dev setup

## Reporting cadence

- Status checkpoint after Step 1 (mock running) — confirm + iterate spec issues if any
- Status checkpoint after Step 4 (CRDM mapping verified) — founder review of CRDM-extension decisions
- Final report at acceptance: what's working, what's pending, what surprised you

Surface blockers immediately. Don't grind through ambiguity. Don't fabricate spec content if the OpenAPI is gappy — flag the gap, mark the test as pending.

## Related

- `Brain/wiki/ncr-counterpoint-phase-0-context-brief.md` — full Phase 0 context (paste this into a fresh session to bootstrap)
- `Brain/dispatches/2026-04-25-tsp-crdm-counterpoint-flow.md` — Phase 0 dispatch (consumes this sandbox)
- `Brain/wiki/ncr-counterpoint-sandbox-setup-checklist.md` — operator-facing prerequisites for Path B (deferred)
- `Brain/wiki/ncr-counterpoint-connection-runbook.md` — Path B technical bring-up
- `Brain/wiki/socal-home-garden-target-customers-brief.md` — customer-side context (Bart, Rapid POS, target customer landscape)
- Memory `project_ncr_voyix_is_competitor.md` — why mock-first / customer-side / VAR-channel routes are strategically correct over NCR-direct partnership

---

**Dispatch author:** Senior ALX (laptop), 2026-04-25
**Executor:** Agent team running Canary Counterpoint adapter dev sandbox setup
**Review gate:** Founder reviews after Step 1 (mock running), Step 4 (CRDM mapping verified), and final acceptance
