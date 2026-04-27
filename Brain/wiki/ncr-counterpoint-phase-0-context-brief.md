---
classification: internal
type: wiki
status: active
date: 2026-04-25
last-compiled: 2026-04-25
needs-review: 2026-05-09
purpose: paste at the start of a fresh session for instant Phase 0 NCR Counterpoint context
----

# NCR Counterpoint Phase 0 — Session Context Brief

Canonical handoff for any fresh session picking up the NCR Counterpoint retail-spine integration work. Paste the body of this article into a new session to bootstrap context fast.

## What this branch is doing

Phase 0 documentation for NCR Counterpoint retail-spine integration into Canary. The Counterpoint REST API surface (95 documented endpoints across 71 paths, v2.4) has been fully extracted, mapped to Canary's CRDM + 13-module spine, and turned into a Phase 0 dispatch package.

Branch: `gclyle/gro-549-solex-c2-productionize-scenario-runner-ux` (ahead of origin; not yet pushed).

## Artifact set (read in this order)

| Order | File | What it carries |
|---|---|---|
| 1 | `docs/sdds/canary/ncr-counterpoint-retail-spine-integration.md` | The SDD. Architecture (§1), source-of-truth refs (§2), auth (§3), CRDM alignment (§4 — recently corrected), ARTS (§5), 13 module maps (§6), cross-cutting concerns (§7), phasing (§8), risks (§10), open questions (§11). Status draft-1 with in-text refinement note. |
| 2 | `Brain/wiki/ncr-counterpoint-api-reference.md` | Catalog overview — endpoint groupings, spine coverage summary by module letter. Companion to the SDD. |
| 3 | `Brain/wiki/ncr-counterpoint-document-model.md` | Document/transaction model deep-dive (PS_DOC_HDR, line items, voids, returns). |
| 4 | `Brain/wiki/ncr-counterpoint-endpoint-spine-map.md` | Per-endpoint × CRDM × spine table (97 rows, 12 grouped sub-tables) + 4-section coverage gap report. **Authoritative for per-endpoint mapping; SDD §4 is the class-level summary.** |
| 5 | `Brain/wiki/ncr-counterpoint-connection-runbook.md` | Windows-host stand-up: prereqs → install → configure → smoke tests. Auth bootstrap (APIKey + `<company>.<user>` Basic). 401/403/404 disambiguation. ErrorCode meanings. |
| 6 | `docs/sdds/canary/ncr-counterpoint-openapi.yaml` | Derived OpenAPI 3.0 spec — 71 paths, 95 operations, 49 schemas. Counterpoint table prefixes preserved (`AR_CUST`, `IM_ITEM`, `PS_DOC_HDR`, `PS_STR`, `EC_*`, `SY_*`). Sample-derived schemas tagged `x-source: sample-derived`. Validates clean. |
| 7 | `docs/superpowers/plans/2026-04-25-ncr-counterpoint-spine-build.md` | Companion build plan — phasing, dispatch packages, acceptance criteria. |

**Source corpus (read-only):** `Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/` — cloned from `github.com/NCRCounterpointAPI/APIGuide` v2.4.

## Phase 0 dispatches already on disk

- `Brain/dispatches/2026-04-25-tsp-crdm-counterpoint-flow.md` — Phase 0 (TSP rebuild + CRDM + adapter shell)
- `Brain/dispatches/2026-04-25-ncr-counterpoint-priority-modules.md` — Phase 1 (T R F L N)
- `Brain/dispatches/2026-04-25-ncr-counterpoint-catalog-modules.md` — Phase 2 (P S)
- `Brain/dispatches/2026-04-25-ncr-counterpoint-operations-modules.md` — Phase 3 (D J; W out of scope per SDD §6.13)
- `Brain/dispatches/2026-04-25-ncr-counterpoint-tertiary-modules.md` — Phase 4 (A C Q)
- `Brain/dispatches/2026-04-25-ncr-counterpoint-cutover.md` — Phase 5 (per-customer deployment runbook + monitoring + H&G first deployment)

## Mapping decisions worth knowing (CRDM × spine)

- **People** = customer entities only (`Customer*`, `Customer_Address`, `Customer_Note`, `Customer_OpenItems`) → Spine R, C
- **Places** = stores + devices + inventory locations → N (stores/devices) + **D primary for InventoryLocations**
- **Things** = items + categories + serials + images + base inventory → S, A. GiftCard codes/templates are secondary here, not primary.
- **Events** = `Document*` (sales tickets, returns, voids embedded) + `GiftCard*` transaction/tender activity (**F primary**) → T, F, Q
- **Workflows** = EC, forecasting/ordering, tasks → W, J, C
- **Platform / cross-cutting** (new row, not original CRDM) = `AdminUser*`, `Roles`, `APIKey`, `Database`, `SystemInfo`, `CACHE` → no spine letter; out of CRDM

## Counterpoint surface quirks worth not rediscovering

- **97 files on disk → 95 documented endpoints.** Two header-only stubs (`GET_Customer_Address.md`, `GET_Customer_Note.md`) inflate the count; README chart correctly omits both.
- **`/DeviceConfig/{WorkstationID}` exists** as a real endpoint (`GET_Device_Config.md`) but is missing from the README chart entirely. **Walk the directory, don't trust the chart.**
- **v2.4 broke price-override semantics:** now `USR_ENTD_PRC=Y` drives, with `HAS_PRC_OVRD` derived. Adapters written against ≤v2.3 must switch. (Source: `Release_Notes/API_2.4_Release_Notes.md`)
- **Three company-scoped endpoints don't require an APIKey** (tokenization-flow design implication):
  - `POST /NSPTransaction`
  - `POST /Store/{StoreId}/Tokenize`
  - `GET /Store/{StoreId}/TokenizeInfo`
- **`DELETE /CACHE`** is referenced in `Basics/Requests.md` (line 79) but has no per-endpoint file — operational contract, undocumented at endpoint level.
- **README chart has multiple chart-vs-files defects** (POST→PUT mislinks, casing drift, `Document_Note` POST hyperlinks to a PUT file). All filed as **GRO-550** (Backlog, Parked).
- **Modules L (Labor) and W (Work Execution) have NO Counterpoint coverage.** Confirmed during extraction. **Don't go looking — it's not there.** Module L has an "option (d) Canary-native labor module" sketch in the SDD; Module W has the same parallel sketch. See memory `project_canary_native_labor_module_opportunity.md`.

## Operating posture

- **OpenAPI YAML is the working contract for adapter dev.** Not the README chart.
- **Per-endpoint wiki overrides the SDD §4 table** when you need per-endpoint detail. SDD §4 is class-level only.
- **Schema names are intentional** — `AR_CUST`, `PS_DOC_HDR`, etc. Don't prettify; they're the natural Counterpoint table names and they're searchable across the corpus.
- **~25 of the 95 endpoints actually need adapter coverage in steady state** per SDD §10. The other 70 are setup/admin/edge-case.

## Strategic context (non-technical, but load-bearing)

- **NCR Voyix is a competitor, not a partner.** Per memory `project_ncr_voyix_is_competitor.md`: integration access strategy routes through customer (license holder), not via NCR partnership. Frame any NCR-facing communication neutrally (data access / connector), not LP/analytics.
- **Bart is a friendly VAR channel** — whitelabel Rapid POS reseller; his customers run Counterpoint underneath. Per memory `project_bart_var_partnership.md`: Monday 2026-04-27 1pm PST call has VAR-partnership dimension beyond sparring.
- **Canonical positioning** (per memory `project_canary_canonical_positioning.md`):
  - **WHAT:** Multi-store merchandising and store ops for SMB, on top of the Counterpoint API backbone
  - **WHO:** Rapid POS delivery experts
  - **HOW:** Our method is CATz

## Open decisions (cross-session)

1. PR the README chart corrections upstream to NCR's APIGuide repo? (GRO-550) — fraught given Voyix-as-competitor framing
2. SDD draft-2 status bump or stay draft-1 with in-text refinement note?
3. Memory-bus chunking of the SDD + spine-map wiki before Phase 1 dispatches start (not done yet — `services/memory-bus/scripts/seed_clean.py` was extended to ingest these globs; needs a run)
4. Push the ahead-of-origin commits when ready

## Phase 0 ready-to-go

TSP rebuild → CRDM → adapter shell. Runbook gives auth bootstrap; OpenAPI gives surface; spine-map tells you which 25 endpoints matter in steady state. **Pick up at `Brain/dispatches/2026-04-25-tsp-crdm-counterpoint-flow.md`** — but read the strategic refinement below first; the original dispatch was reshaped on 2026-04-25.

## 2026-04-25 strategic refinement (added end-of-day)

Phase 0 was reshaped during scoping. The original dispatch ("rebuild TSP for Counterpoint") implied invasive surgery on the working Square pipeline. Today's posture is **surgical, not architectural**: leave Square as-is (the working baseline / proof case); generalize the downstream consumers so Counterpoint plugs in alongside.

**Phase 0 is now three sub-phases:**

| Sub-phase | Title | Status | Deliverable |
|---|---|---|---|
| 0a | Square-coupling audit | **complete 2026-04-25** | `docs/sdds/canary/ncr-counterpoint-square-coupling-audit.md` — registry of 18 Layer 1 + 25 Layer 2 + 12 Layer 3 touchpoints, with severity, effort, and proposed generalization for each |
| 0b | Generalize app-layer touchpoints | **in progress** | Source-aware ingress, dispatch, validators, resolvers; `external_identities`-mediated lookups; per-source schema-drift fingerprinting |
| 0c | Counterpoint adapter (the original Phase A) | not started | Polling worker + Counterpoint parsers + fixtures; plugs into now-source-aware downstream |

**"Park Square" decision:** the existing Square pipeline (`webhooks_tsp.py`, `validators/square.py`, `enrichers/square.py`, `square_oauth_wired.py`, `square_oauth_tokens` table, 17 Square parser modules) stays untouched. Counterpoint gets parallel files. Don't refactor Square.

**Modular monolith, not microservice — yet.** Counterpoint adapter ships as a standalone Python package inside the Canary repo, with Canary as its first import. When consumer #2 surfaces (Cove, Angel, future Foundation app), the package becomes a service with minimal refactoring. Don't extract framework-from-product before there's a second caller.

**Critical insight from the audit:** Canary already has the source-agnostic bones — `source_systems`, `external_identities` (built per GRO-267), `merchant_sources`, namespaced enrichers, `payload_normalizer(source, ...)`. **The runtime paths bypass them.** So Phase 0b is largely "make the runtime use what we already designed," not "design something new." That's a meaningfully smaller lift than original-dispatch framing implied.

**Top-3 concerning audit findings (high-blast-radius):**
1. Chirp engine + `sub2_parse` read `Employee.square_employee_id` / `Location.square_location_id` directly across 12+ modules, bypassing the existing `external_identities` bridge
2. `_check_schema_fingerprint` will spuriously fire drift alerts on every Counterpoint event (different payload shape); `SchemaFingerprint` has no `source` column
3. Multi-company-per-tenant (Counterpoint `<company-alias>.<user>`) is incompatible with `Merchant.source_merchant_id UNIQUE` — data-model decision required before adapter writes any rows

**Top-3 quickest wins (Phase 0b first slice):**
1. Insert `'counterpoint'` row in `source_systems`; extend `external_identities.entity_type` CHECK constraint
2. Add `'counterpoint': counterpoint_validator` entry to `SOURCE_VALIDATORS` / `SOURCE_SIGNATURE_HEADERS` / `REGISTERED_SOURCES`
3. Generalize the stateless Chirp gate from `source == "square"` to per-rule `applicable_sources`

**Phase 0b ordering (9 steps):** (1) register source + CHECK constraints; (2) credentials table + multi-company decision; (3) `external_identities`-mediated resolvers; (4) `source_code` on `sales.transactions`; (5) per-source dispatch tables; (6) per-rule source applicability; (7) Counterpoint poller as sibling ingress; (8) Counterpoint validators/parsers; (9) source-aware drift detection.

**The audit ratifies the strategic shift.** Coupling intensity is MEDIUM-HIGH but bounded — the Square parsers, validators, OAuth wiring, and OAuth-shaped tables can all stay Square-only forever. Counterpoint gets sibling files. The cross-cutting work is in the resolvers and the schema-drift fingerprinting, not in the parsers or validators.

## Companion artifacts (Monday call prep + research)

- `Brain/raw/inbox/monday-call-script.md` — HIDE-scope founder script for 2026-04-27 1pm PST Bart call (gitignored, lives locally)
- `Brain/wiki/rapid-pos-counterpoint-user-pain-points.md` — 10 pain themes + 10 FAQs from public-community research
- `Brain/wiki/rapid-pos-counterpoint-market-research-tam.md` — TAM ~1,200 US garden centers / ~9,000 SMB across all Counterpoint VAR verticals
- `Brain/wiki/garden-center-operating-reality.md` — H&G domain reality (vendor mix, cash-and-paper, alt payment rails)
- `Brain/wiki/canary-module-q-counterpoint-rule-catalog.md` — 23 Q rules grouped by 10 categories, all Counterpoint-substrate-aware, with garden-center allow-list framework
- `Brain/wiki/ncr-counterpoint-rapid-pos-relationship.md` — Counterpoint vs Rapid POS clarification
- `Brain/wiki/ncr-counterpoint-sandbox-setup-checklist.md` — operator action items for credentials + sandbox stand-up (revised for NCR-as-competitor framing)
- `CATz/method/artifacts/solution-map.md` — Phase II Solution Map artifact template
- `CATz/proof-cases/specialty-smb-counterpoint-solution-map.md` — sanitized worked example

## How to use this brief in a fresh session

Paste the body of this article (everything below the frontmatter, above this line) into a new Claude Code session. The session will have full context to pick up Phase 0 work, validate adapter design, or extend any of the dispatches.

For external-facing communication (Bart, partners, VARs), use the canonical positioning lines from §"Strategic context"; do NOT paste the full brief — it's internal.
