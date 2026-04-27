---
title: "Hawk + Bull Design Spec"
date: 2026-04-27
status: approved
modules: [Hawk, Bull, Fox, Owl, ALX]
spine_domains: [Q, D, F]
---

# Hawk + Bull: Case Management Factory + DSD Vendor Accountability

## Executive Summary

Two modules. One governing thesis.

**Hawk** is a full-service case management card factory for Canary back-office investigators — replacing Fox Lite as the primary investigator surface on Module Q's spine node. Fox doesn't disappear; it becomes `incident_class = 'EBR'` inside Hawk. Every case class produces a structured, entity-tagged card that ingests to the pgvector memory bus. The cards are the intelligence substrate.

**Bull** is a DSD vendor accountability analytics layer that sits on top of Module D's existing inventory movement substrate. No parallel tracking. Bull computes credit/delivery ratios, variant ratios, and delivery-to-sales ratios, surfaces exceptions, feeds Hawk vendor cases and Chirp alert rules.

**The governing thesis:** the primary value is not analytics — it's field data quality. High-turnover retail workforces produce inconsistent incident documentation. Wizard-driven capture enforces completeness, terminology consistency, and structured output regardless of the associate's experience level. Clean input → reliable cards → trustworthy analytics.

---

## 1. Context and Problem Statement

### 1.1 Prior Art: The LPMS Reference Dataset

A 2015 production LPMS from a large specialty sporting goods retailer (NFR deployment archetype; client references scrubbed) was analyzed as the primary design input. The dataset contains:

- **65 incident types** across 4 classes: Critical Smart Alert (17), External (7), Internal (30 with DE/PV classification), Incident (9)
- **15 resolution action codes** across two tracks: Internal (9) and External (6)
- **30+ sources of information** spanning CCTV/LPTV, EBR variants, GLI variants, tip variants, cycle counts, implication, and observation
- Wizard-driven form templates — one per incident type — enforcing required fields at data entry time

The most important thing this dataset communicates is implicit: every field, every required input, every picklist is a constraint on what an associate can leave blank or get wrong. The forms are the data quality policy, and the data quality policy is the analytics foundation.

### 1.2 Canary's Current State

Fox (Module Q.5) handles EBR-triggered case management with a seven-table schema, a PostgreSQL-trigger hash chain for evidence integrity, and a three-tier audit architecture (operational / immutable audit / evidentiary chain). Fox is working and deployed. It is scoped to transaction-based exception analysis.

There is no Canary case management surface for:
- LP external (shoplifting, vendor theft, trespass)
- LP internal (DE + PV incidents)
- Compliance (ATF/FFL violations, firearms regulation)
- Liability (slip-and-fall, customer incidents)
- Insurance claims
- Facilities (CCTV install, equipment repair)
- Vendor accountability (DSD exceptions)

Fox Lite plus a spreadsheet is the current workaround.

### 1.3 Hawk's Position on the Spine

Hawk expands Q.5 (investigator surface) within RBIS Domain 4 — Store Operations. The spine mapping:

| BST | Module | Hawk Role |
|-----|--------|-----------|
| Loss Prevention | Q | Primary case workflow surface (Q.5.4 = Hawk case engine) |
| Suspicious Activity Analysis | Q | Alert → case bundling (Q.3.3 feeds Hawk) |
| Vendor Performance Analysis | D + F | Bull signals surface as Hawk vendor cases |
| Service Delivery Analysis | Q + F | Facilities and liability case classes |

No new spine letters. No CATz violations.

### 1.4 Bull's Position on the Spine

Bull is an analytics-only layer. It reads from Module D's substrate (stock_movements, RECVR/RTV document records, TRANSFER-VARIANCE events) and Module F's invoice data. It does not duplicate tracking. It computes.

Spine interfaces consumed:
- D.6.1 SOH snapshots
- D.6.3 TRANSFER-VARIANCE events
- D.6.5 UNATTRIBUTED-MOVEMENT events
- T pipeline: DOC_TYP = RECVR, RTV documents
- F004 / F013: vendor invoice + acknowledgment
- C008 + F012: vendor master

---

## 2. System Architecture

### 2.1 Four MCP Servers

| Server | Role | Primary Tools |
|--------|------|---------------|
| `canary-hawk` | Case intake, wizard state, card generation, timeline | `create_case`, `advance_workflow`, `attach_evidence`, `generate_card` |
| `canary-bull` | DSD analytics, vendor scoring, exception surface | `vendor_scorecard`, `exception_report`, `flag_vendor`, `push_chirp_signal` |
| `canary-owl` | Semantic search, NL analytics, health reports | `recall`, `nl_query`, `health_report`, `find_similar_cases` |
| `canary-alx` | VSM coordinator, diagnostic mode, cutover-aware queries | `diagnose`, `route_query`, `check_cutover_status` |

**Memory bus** is shared infrastructure underneath all four — not a fifth MCP. `growdirect_memory_bus:8003` serves pgvector similarity search over the card corpus. Hawk cards and Bull signals ingest here. Owl queries here.

### 2.2 Data Flow

```
LPMS Event (associate intake via Hawk wizard)
    │
    ▼
hawk_cases + incident_type-driven wizard form
    │ required fields enforced at entry
    ▼
hawk_cards (structured markdown, entity-tagged frontmatter)
    │
    ├─► pgvector memory bus (Owl queries)
    │
    └─► fox_evidence chain (evidentiary classes)

DSD Movement (Module D substrate)
    │
    ▼
Bull analytics layer
    │ credit/delivery ratio, variant ratio, D/S ratio
    ▼
bull_vendor_scores + bull_exceptions
    │
    ├─► Hawk vendor case (automatic if threshold breached)
    └─► Chirp DSD rule signal
```

### 2.3 ALX as VSM Coordinator

ALX (Virtual Store Manager) does not hold the intelligence — it routes to it. Before answering any performance question, ALX reads `app.merchant_module_cutover_status` to determine which modules are live (parallel-observer / partial-cutover / full-cutover). It queries Owl's MCP tools for semantic search, queries module MCPs for live data, and synthesizes responses using the Clarks seven-section diagnostic frame for open-ended performance questions.

ALX does not watch data streams. Owl does not watch data streams. The intelligence is in the cards.

---

## 3. Hawk: Case Management Card Factory

### 3.1 Incident Taxonomy

Four classes, sourced from the LPMS reference dataset and adapted for Canary deployment:

**Critical Smart Alert** — LP visibility events surfaced by Chirp/Owl automatic detection. System-initiated; associate completes case from alert. 17 incident types including: Bulk / Sweeper, Grab-and-Run, Refund Abuse, Return Fraud, High Loss Transaction, Void/No-Sale Pattern, Register Variance, Price Manipulation.

**External** — Customer-facing and third-party incidents. 7 types: Shoplifting (Apprehension, Observation, Attempted), Vendor Theft, Trespass, Robbery, External Fraud.

**Internal** — Employee-related incidents. 30 types split by classification:
- **DE (Dishonesty/Ethics)**: Cash theft, Merchandise theft, Refund manipulation, Sweet-hearting, Discount abuse, Fraudulent return, Till shortages (deliberate), Vendor collusion, Data theft
- **PV (Policy Violation)**: Register discrepancies (negligent), Procedural non-compliance, POS bypass, Documentation falsification, Unauthorized markdowns

**Incident** — Non-LP events: Slip and Fall, Customer Injury, Property Damage, ATF/FFL Compliance, Insurance Claim, CCTV Installation, Equipment Repair, Vendor Dispute, Other Facilities.

### 3.2 Case Schema (`hawk` schema)

```sql
hawk_cases
  case_id           UUID PK
  merchant_id       UUID FK → app.merchants
  location_id       UUID FK → app.locations
  incident_class    TEXT  -- 'critical_smart_alert' | 'external' | 'internal' | 'incident'
  incident_type     TEXT  -- FK → hawk_incident_types.type_code
  de_pv_flag        TEXT  -- 'DE' | 'PV' | NULL (internal only)
  case_status       TEXT  -- open | investigating | pending_review | escalated | closed | referred_to_le
  opened_at         TIMESTAMPTZ
  closed_at         TIMESTAMPTZ
  opened_by         UUID FK → app.users
  assigned_to       UUID FK → app.users
  source_id         UUID FK → hawk_sources
  fox_case_id       UUID FK → app.fox_cases NULL  -- populated if incident_class='EBR'
  chirp_alert_id    UUID NULL  -- originating Chirp alert if system-initiated
  bull_exception_id UUID NULL  -- originating Bull exception if vendor case
  narrative         TEXT
  card_id           UUID NULL FK → hawk_cards  -- nullable; card generated post-wizard completion
  created_at        TIMESTAMPTZ
  updated_at        TIMESTAMPTZ

hawk_incident_types
  type_code         TEXT PK
  incident_class    TEXT
  de_pv_flag        TEXT
  display_name      TEXT
  wizard_template   JSONB  -- field definitions + required flags
  resolution_track  TEXT   -- 'internal' | 'external'
  active            BOOLEAN

hawk_actions
  action_id         UUID PK
  case_id           UUID FK → hawk_cases
  action_code       TEXT  -- see resolution action taxonomy below
  action_track      TEXT  -- 'internal' | 'external'
  actioned_by       UUID FK → app.users
  actioned_at       TIMESTAMPTZ
  notes             TEXT

hawk_sources
  source_id         UUID PK
  source_code       TEXT  -- 'CCTV' | 'EBR' | 'GLI' | 'TIP_ASSOCIATE' | 'TIP_CUSTOMER' | etc.
  source_class      TEXT  -- 'internal' | 'external'
  display_name      TEXT

hawk_subjects
  subject_id        UUID PK
  case_id           UUID FK → hawk_cases
  subject_type      TEXT  -- 'employee' | 'customer' | 'vendor' | 'unknown'
  employee_id       UUID NULL FK → app.employees
  vendor_entity_id  TEXT NULL  -- Counterpoint vendor code (from C008/F012 vendor master); app.vendors is a deferred FK target
  external_name     TEXT NULL
  external_dob      DATE NULL
  external_id_type  TEXT NULL
  external_id_num   TEXT NULL
  notes             TEXT

hawk_compliance_obligations
  obligation_id     UUID PK
  case_id           UUID FK → hawk_cases
  obligation_type   TEXT  -- 'ATF_REPORT' | 'INSURANCE_CLAIM' | 'LEGAL_HOLD'
  due_date          DATE
  filed_at          TIMESTAMPTZ NULL
  reference_num     TEXT NULL
  notes             TEXT

hawk_cards
  card_id           UUID PK
  case_id           UUID FK → hawk_cases
  card_body         TEXT  -- structured markdown
  frontmatter       JSONB  -- entity tags (see 3.3)
  vector            VECTOR(1024)  -- Ollama qwen3-embedding:8b
  card_version      INTEGER
  generated_at      TIMESTAMPTZ
  invalidated_at    TIMESTAMPTZ NULL

hawk_timeline
  event_id          UUID PK
  case_id           UUID FK → hawk_cases
  event_type        TEXT
  event_data        JSONB
  created_by        UUID FK → app.users
  created_at        TIMESTAMPTZ
```

### 3.3 Card Frontmatter Schema

Every Hawk card carries entity-tagged frontmatter enabling cross-case relationship analysis in Owl:

```yaml
---
card_type: hawk_case
case_id: <uuid>
merchant_id: <uuid>
location_id: <uuid>
incident_class: internal
incident_type: refund_manipulation
de_pv_flag: DE
subject_type: employee
employee_id: <uuid>
vendor_id: null
opened_at: 2026-04-27T14:22:00Z
case_status: investigating
source_codes: [EBR, TIP_MANAGER]
---
```

### 3.4 Resolution Action Taxonomy

**Internal track** (9 codes): `CLOSED_UNFOUNDED`, `CORRECTIVE_ACTION`, `INTERVIEWED_NO_CASE`, `QUIT_BEFORE_INTERVIEW`, `QUIT_DURING_INTERVIEW`, `REPORTED_TO_ATF`, `TERMINATED_PROSECUTED`, `TERMINATED_RELEASED`, `UNDER_INVESTIGATION`

**External track** (6 codes): `CLOSED_UNFOUNDED`, `PROSECUTED`, `RELEASED_ADULT`, `RELEASED_TO_GUARDIAN`, `RELEASED_TO_POLICE`, `UNDER_INVESTIGATION`

`CLOSED_UNFOUNDED` and `UNDER_INVESTIGATION` appear in both tracks. They carry the same semantic but are tracked separately per case record — the track is determined by `incident_class`, not the action code itself.

Action track is determined by `incident_class`. Internal classes use the internal track. External classes use the external track. Incident class cases may use either depending on compliance obligations.

### 3.5 Evidence Chain

Hawk uses the existing Fox evidence infrastructure. Hash chain computed by PostgreSQL trigger, not application code.

**EBR cases:** `fox_case_id` is populated. Evidence records link directly through the existing `app.fox_evidence → app.fox_cases` FK chain. Nothing changes in Fox.

**Non-EBR evidentiary cases** (e.g., shoplifting apprehension with CCTV, liability with incident footage): `fox_evidence` gains a nullable `hawk_case_id UUID FK → hawk.hawk_cases` column. Non-EBR Hawk cases attach evidence directly without a synthetic `fox_cases` row. The hash chain trigger fires on both FK paths. This is a Phase 2 migration addition to the Fox evidence table — Phase 1 Hawk (no Fox bridge) does not require it.

`fox_evidence_access_log` is unchanged — it logs by `evidence_id` regardless of which case type originated the evidence record.

### 3.6 Wizard-Driven Intake

Incident type selection is Step 1. The wizard form is loaded from `hawk_incident_types.wizard_template` (JSONB). Required fields are server-side enforced — the case record cannot transition from `open` to `investigating` without all required fields populated. The wizard does not ask what it doesn't need: form fields are scoped precisely to the incident type.

Auto-population priorities:
- Employee ID: populated from session / lookup if associate name entered
- Merchant/location: populated from auth context
- Chirp alert ID: pre-linked if case originated from system alert
- Bull exception ID: pre-linked if case originated from vendor exception

---

## 4. Bull: DSD Vendor Accountability Analytics

### 4.1 Design Principle

Bull does not track deliveries. Module D tracks deliveries. Bull reads Module D's substrate and computes accountability metrics across vendors, merchant locations, and time periods. Bull is a read-heavy analytics layer; it writes only to its own aggregate and exception tables.

### 4.2 Primary Metrics

**Credit/Delivery Ratio** — `SUM(credit_dollars) / SUM(delivery_dollars)` per vendor per period. Industry context: high ratios flag potential delivery inflation or credit manipulation.

**Variant Ratio** — `(delivery_invoice_count - credit_invoice_count) / delivery_invoice_count`. Benchmark: −63% (from iRED analytics reference, large specialty sporting goods deployment). Ratios significantly worse than benchmark trigger exception flags.

**Delivery-to-Sales Ratio** — Delivery dollars vs net sales for vendor's SKUs at the location. Trend analysis: deliveries growing faster than sales signals over-delivery or inventory build.

**Credits as % of Sales** — Maps to DSD6 (Kroger requirements reference). Vendors above threshold flagged automatically.

**Duplicate Invoice Detection** — Maps to DSD1. Invoice number + vendor + amount + date matching across locations.

### 4.3 Bull Schema (`bull` schema)

```sql
bull_vendor_scores
  score_id          UUID PK
  merchant_id       UUID FK → app.merchants
  location_id       UUID FK → app.locations NULL  -- NULL = merchant-level aggregate
  vendor_entity_id  TEXT  -- Counterpoint vendor code (C008/F012 vendor master); deferred FK when app.vendors is created
  period_start      DATE
  period_end        DATE
  delivery_count    INTEGER
  delivery_dollars  NUMERIC(12,4)
  credit_count      INTEGER
  credit_dollars    NUMERIC(12,4)
  credit_delivery_ratio  NUMERIC(8,4)
  variant_ratio     NUMERIC(8,4)
  delivery_sales_ratio   NUMERIC(8,4)
  credits_pct_sales NUMERIC(8,4)
  computed_at       TIMESTAMPTZ
  created_at        TIMESTAMPTZ

bull_benchmarks
  benchmark_id      UUID PK
  benchmark_key     TEXT  -- 'variant_ratio_industry' | 'credits_pct_sales_threshold' | etc.
  benchmark_value   NUMERIC(10,4)
  benchmark_source  TEXT  -- 'iRED_NFR_2015' | 'Kroger_DSD_2024' | 'Canary_observed'
  effective_from    DATE
  effective_to      DATE NULL
  notes             TEXT

bull_exceptions
  exception_id      UUID PK
  merchant_id       UUID FK → app.merchants
  location_id       UUID FK → app.locations NULL
  vendor_entity_id  TEXT  -- free-text vendor ref; deferred FK
  exception_type    TEXT  -- 'HIGH_CREDIT_RATIO' | 'VARIANT_RATIO_BREACH' | 'DUPLICATE_INVOICE' | etc.
  exception_severity TEXT  -- 'low' | 'medium' | 'high' | 'critical'
  detected_at       TIMESTAMPTZ
  score_id          UUID FK → bull_vendor_scores NULL
  detail            JSONB
  hawk_case_id      UUID FK → hawk.hawk_cases NULL  -- populated when case created
  chirp_signal_id   UUID NULL
  resolved          BOOLEAN DEFAULT FALSE
  resolved_at       TIMESTAMPTZ NULL

bull_chirp_signals
  signal_id         UUID PK
  exception_id      UUID FK → bull_exceptions
  merchant_id       UUID FK → app.merchants
  rule_code         TEXT  -- maps to Chirp rule registry
  signal_payload    JSONB
  pushed_at         TIMESTAMPTZ
  acknowledged_at   TIMESTAMPTZ NULL
```

### 4.4 Upstream Data Sources

Bull reads these D/T/F interfaces at compute time (batch or on-demand). **Note: Module D tables (`stock_movements`, `movement_audit_log`, etc.) are designed but not yet built** — they exist as decomposition artifacts, not live schema. Bull Phase 3 is gated on Module D implementation completing first.

| Source | Interface | Purpose |
|--------|-----------|---------|
| D.6.1 SOH snapshots | `stock_movements` aggregates | Delivery-to-sales ratio baseline |
| D.6.3 TRANSFER-VARIANCE | `movement_audit_log` | Unattributed movement detection |
| D.6.5 UNATTRIBUTED-MOVEMENT | `stock_movements` (UNATTRIBUTED type) | Vendor delivery attribution gap |
| T pipeline RECVR | `stock_movements` (DOC_TYP=RECVR) | Delivery invoice records |
| T pipeline RTV | `stock_movements` (DOC_TYP=RTV) | Return-to-vendor credit records |
| F004/F013 | vendor invoice + acknowledgment | Invoice-side credit data |
| C008/F012 | vendor master | Vendor identity matching |

### 4.5 Exception-to-Case Bridge

When a `bull_exceptions` record exceeds severity threshold (configurable per exception_type in `bull_benchmarks`), Bull can:

1. Auto-create a Hawk case (`incident_class='incident'`, `incident_type='vendor_dispute'`) with Bull exception pre-linked
2. Push a Chirp signal to the DSD rule family for surfacing in the alert feed
3. Both (default for `critical` severity)

The Hawk wizard pre-populates from the Bull exception detail, giving the investigator the full vendor scorecard at case open.

---

## 5. Fox Positioning

Fox is not decommissioned. Fox Lite becomes the EBR incident class within Hawk.

- Existing Fox tables (`fox_cases`, `fox_case_alerts`, `fox_subjects`, `fox_case_actions`, `fox_case_timeline`, `fox_evidence`, `fox_evidence_access_log`) are unchanged
- Existing Fox Flask service and routes are unchanged
- EBR alerts that previously opened Fox cases now open Hawk cases with `incident_class='EBR'` and `fox_case_id` populated
- Fox evidence chain is shared: `fox_evidence` serves as the evidence store for all Hawk evidentiary case classes
- Fox UI remains as the EBR review surface; Hawk investigator surface is the upgrade path for investigators working multi-class cases

---

## 6. CATz Compliance

Each module follows the three-layer CATz artifact pattern:

| Layer | Hawk | Bull |
|-------|------|------|
| Canonical spec | `Canary-Retail-Brain/modules/hawk.md` | `Canary-Retail-Brain/modules/bull.md` |
| Canary crosswalk | `Brain/wiki/canary-module-hawk-*.md` | `Brain/wiki/canary-module-bull-*.md` |
| Functional decomposition | `Brain/wiki/canary-module-hawk-functional-decomposition.md` | `Brain/wiki/canary-module-bull-functional-decomposition.md` |

Spine module letters are not invented. Hawk expands Q (Loss Prevention). Bull extends D (Distribution) analytics. The functional decomposition wiki articles will register the new L2 nodes against the existing Q.5 and D.6 spine nodes.

---

## 7. Open Questions

**ASSUMPTION-A-01 — Module A Scope Conflict (unresolved)**

CATz canonical definition for Module A = item-asset-management (`IM_ITEM.ITEM_TYP` = firearms, optics, high-value accessories). CRB canonical definition = Bubble (device-anomaly detection over Module N security hardware, CCTV, access control).

CCTV and device anomaly incidents under Hawk Facilities class are the natural home for device-flagged events. But the Module A conflict needs a founder decision before Hawk Facilities workflows are finalized:

- **Option A** (recommended): Module A = item-asset-management only. Device anomaly detection is a Chirp rule family fed by Module N. Hawk Facilities handles CCTV install/repair cases; it does not have a live detection dependency on A.
- **Option B**: Module A = Bubble (device-anomaly). Device events become a Chirp source that opens Hawk Facilities cases automatically. Item-asset-management moves to a Module D subtype.

This does not block Hawk development. Facilities case intake works without the detection dependency. Flag for founder decision before Q3 planning.

**Implementation assumption:** The Hawk Facilities case wizard (CCTV Installation, Equipment Repair, device-anomaly incident types) is being built against **Option A** (Module A = item-asset-management only; device anomaly detection routes through Chirp rules, not a Module A dependency). If Option B is selected, the Facilities case intake will require rework to wire device-anomaly auto-case-open logic. Scope of rework: one new Chirp rule family + one auto-open pathway in the Hawk wizard state machine.

---

## 8. Implementation Sequence

Phase 1 — Hawk core (unblocked):
1. `hawk` schema DDL + Alembic migration
2. Incident type seed data (65 types, 14 action codes, 30+ sources)
3. Wizard state machine (Flask routes + Jinja2 templates)
4. Card generation pipeline + pgvector ingest
5. Case list / case detail investigator UI
6. `canary-hawk` MCP server (create_case, advance_workflow, attach_evidence, generate_card)

Phase 2 — Fox bridge:
7. EBR alert → Hawk case routing (replaces direct Fox case open)
8. Fox evidence chain wiring: Alembic migration adding `hawk_case_id UUID NULL FK → hawk.hawk_cases` to `fox_evidence`; application-layer routing for non-EBR Hawk evidentiary case classes
9. Hawk investigator UI Fox evidence panel

Phase 3 — Bull (requires Module D substrate):
10. Bull schema DDL + Alembic migration
11. Bull compute jobs (credit/delivery ratio, variant ratio, D/S ratio)
12. Exception detection + severity thresholds seeded from benchmarks
13. Exception-to-Hawk-case bridge
14. Chirp DSD signal push
15. `canary-bull` MCP server (vendor_scorecard, exception_report, flag_vendor, push_chirp_signal)

Phase 4 — Owl + ALX wiring:
16. `canary-owl` MCP tools updated to query hawk + bull card corpus
17. ALX VSM diagnostic mode updated to include Hawk case context and Bull vendor risk
