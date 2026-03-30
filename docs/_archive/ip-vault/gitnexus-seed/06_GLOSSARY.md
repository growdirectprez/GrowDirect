---
type: research
domain: canary
status: active
created: 2026-03-19
updated: 2026-03-19
---
# Canary LP — Glossary & Entity Reference

> **Domain:** Terms, acronyms, entity definitions, enum values, GRO issue references
> **Last Updated:** 2026-03-19 | **Classification:** Confidential

---

## Core Terms

**Canary LP** — AI-powered loss prevention platform for Square merchants. The primary product of GrowDirect Inc.

**GrowDirect** — The company building Canary LP. Founded by Jeffe.

**elJeffe Protocol** — Self-describing, server-independent verification protocol that inscribes commercial events on Bitcoin as Ordinal inscriptions. Named after the founder's vision of a "modern day wax seal for the individual."

**gLog** — The immutable, Bitcoin-native transaction log created by the elJeffe protocol. Successor to the IBM tLog. Permanent event sourcing where verification is mathematical, not institutional.

**tLog** — IBM 4690 transaction log (1986–2017). Mutable, database-dependent. The legacy approach that gLog replaces.

**CRDM** — Canary Retail Data Model. The canonical data format that normalizes heterogeneous POS data into typed, searchable fields. Current version: v1.1.

**Factory Process** — Canary's development methodology: Blueprint → Parts → Assembly → QC → Packaging → Ship. Enforced by the Canary skill set.

**Completeness Gate** — The four-check verification before any service is marked done: data IN, data OUT, row counts match, route responds.

**No Lazy Pipes** — The delivery standard requiring every service, route, and pipeline to be complete end-to-end. No hardcoded returns, no stubbed services, no half-built pipelines.

---

## Service Names

**TSP** — Triple Subscriber Pipeline. Data ingestion backbone: webhooks → Valkey Streams → three sequential subscribers (Seal, Parse, Merkle).

**Chirp** — Detection engine. 26+ rules across 8 categories evaluating transactions for loss prevention anomalies.

**Fox** — Case management system with hash-chain evidence locker for investigations.

**Owl** — AI intelligence layer. Natural language search, drill analysis, daily digest ("The One Thing"), business health monitoring ("Heartbeat").

**ALX** — Agent memory system. pgvector knowledge graph with 954+ curated memories for contextual recall.

**RaaS** — Rule-as-a-Service. Public verification API for the elJeffe protocol. Micropayment-based (1 sat per call via L402).

**Identity** — Square OAuth onboarding and JWT session management service.

**Analytics** — Star schema metrics layer powering dashboards with aggregated data.

---

## Protocol Terms

**Namespace** — Pseudonymous merchant identity in format `{guid}.jeffe`. GUID-only on Bitcoin L1. No human-readable names on-chain.

**Alias** — Human-readable name in format `name.jeffe` registered on Avalanche L2. Maps to a namespace GUID. One GUID can have many aliases.

**Burner** — Disposable sub-address: `label.name.jeffe`. Minted on Avalanche L2 with a TTL (time-to-live).

**Genesis Inscription** — First inscription in the elJeffe chain. Contains the full protocol spec. Root of trust.

**Merkle Batch** — Set of commercial events batched into a binary Merkle tree. Root hash inscribed on Bitcoin.

**Serializable Gate** — The core property of the .jeffe Ordinal: portable, non-consumable, context-agnostic identity.

**L1 / L2 / L3** — Three-layer resolution stack. L1 = Bitcoin (permanent, GUID-only). L2 = Avalanche (human-readable aliases). L3 = PostgreSQL (GrowDirect's cache for fast lookups).

**L402** — Lightning Network micropayment protocol used for RaaS API billing (1 sat per verification call).

---

## Database Terms

**app schema** — PostgreSQL schema for master data: merchants, employees, locations, detection rules, alerts, Fox cases, namespaces, feature flags.

**sales schema** — PostgreSQL schema for immutable transaction data. Written only by TSP pipeline (canary_tsp role). Contains: transactions, line items, tenders, refunds, evidence records, Merkle batches.

**metrics schema** — PostgreSQL schema for aggregated analytics. Star schema design with daily/hourly/period metrics.

**canary_memory** — Separate PostgreSQL database for ALX's pgvector knowledge graph.

**RLS** — Row-Level Security. Enforced on all tenant-scoped tables via merchant_id. Array-aware for multi-merchant organizations.

**Guardian** — The critical-file-guardian skill that controls modifications to protected files (.env, wsgi.py, session_factory.py, Dockerfiles) with approval workflow and SHA256 manifest tracking.

---

## Enum Values

### transaction_type
SALE, RETURN, VOID, POST_VOID, NO_SALE, PAID_IN, PAID_OUT, EXCHANGE

### cancel_context
SELLER_CANCELED, BUYER_CANCELED, TIMED_OUT, DECLINED, FAILED

### source_type
WEBHOOK, POLLING, BATCH

### entry_method
KEYED, SWIPED, CHIP, CONTACTLESS, ON_FILE, MANUAL

### risk_level
LOW, MEDIUM, HIGH, CRITICAL

### rule_category
payment, cash_drawer, void, gift_card, loyalty, timecard, order, composite

### severity
INFO, LOW, MEDIUM, HIGH, CRITICAL

### case_status
open, investigating, pending_review, resolved, closed

### case_priority
low, medium, high, urgent

---

## Target Tables (Not Yet Built)

These tables are specified in CRDM v1.1 or required by GRO-266 data coverage expansion:

**line_item_discounts** — Discount identity, type (percentage/fixed), rate, scope (line/order), reward link, pricing_rule_id. Required for Chirp C-201 (excessive discount).

**line_item_taxes** — Tax identity, type, rate, scope per line item. Required for tax-aware analytics.

**line_item_modifiers** — Modifier identity, price delta, quantity per line item. Required for Chirp C-203 (sweethearting detection).

**order_service_charges** — Service charge identity, type, amount per order. Required for fee-based anomaly detection.

**order_returns** — Full return detail with source order link and line item mapping. Currently only is_voided flag captured.

**order_rewards** — Loyalty reward links per order, bridging loyalty-to-transaction data.

**product_identifiers** — Multi-barcode registry (UPC, EAN, ISBN, SKU, PLU per product). CRDM v1.1 Amendment 2. Required for barcode swap detection.

**product_compositions** — Bundle and kit decomposition mapping. CRDM v1.1 Amendment 3. Makes bundled items transparent to Chirp.

**categories** — Self-referential category hierarchy with materialized path. CRDM v1.1 Amendment 4. Required for category-scoped detection rules.

**location_product_authorizations** — Authorized product list per location. CRDM v1.1 Amendment 7. Required for diversion and unauthorized sales detection.

---

## Key GRO Issues

**GRO-237** — Canonical UUID Principle. All entities use Canary's UUID as primary identifier; Square's external_id for reconciliation only.

**GRO-47** — Core pipeline build (Square OAuth → webhook → seal → parse → Merkle → inscribe).

**GRO-18** — Multi-tenant architecture (organization → merchant hierarchy).

**GRO-46** — elJeffe protocol specification.

**GRO-13** — Namespace registration system.

**GRO-45** — Source system abstraction (reference table replacing hardcoded POS checks).

**GRO-265** — Field Registry: canonical metadata layer for Owl, i18n, UI, and search. DONE. Delivered field-registry.json + field-registry.md + ERDs.

**GRO-266** — Data model completeness: Square API full coverage. HIGH priority. 28% schema coverage → 6 new tables, parser enrichment across all tiers. Introduces `canary-data-expansion` skill.

**GRO-267** — CRDM gap scan: v1.1 amendments vs current models. Only 2 of 11 amendments implemented. P1: external_identities migration to eliminate 25 `square_*` columns across 14 model files.

**GRO-73** — Operations Console build.

**GRO-257** — Cancel context implementation (void/post-void classification).

**GRO-74, GRO-96, GRO-93** — Related multi-tenant integration issues.

**B-058** — War Chest content dispatch (investor site, tLog/gLog narrative, legal review).

---

## Chirp Rule Ranges

| Range | Category | Examples |
|-------|----------|----------|
| C-001–C-009 | Payment anomalies | Excessive refund rate, high-value voids, split tender |
| C-010–C-019 | Void patterns | Rapid voids, post-void timing, void-after-close |
| C-020–C-029 | Gift card | Activation anomalies, reload patterns, cross-location |
| C-030–C-039 | Loyalty abuse | Point inflation, redemption without sale |
| C-040–C-042 | Timecard | Off-clock transactions, ghost shifts |
| C-050–C-059 | Order integrity | Discount stacking, below-cost, price override frequency |
| C-063–C-068 | Cash drawer | Variance per shift, expected vs. actual |
| C-070+ | Composite | Multi-signal employee risk scoring |
| C-080–C-085 | Inventory | Adjustment anomalies, discrepancy detection |
| C-901–C-909 | Device integrity | Device attestation flags for Merkle batches |

---

## File Paths (Canonical)

| Asset | Path |
|-------|------|
| Agent instructions | `~/GrowDirect/Canary/CLAUDE.md` |
| Field registry | `~/GrowDirect/Canary/docs/field-registry.md` |
| Team profiles | `~/GrowDirect/Canary/docs/profiles/TEAM.md` |
| Owl profile | `~/GrowDirect/Canary/docs/profiles/Owl.md` |
| SDDs | `~/GrowDirect/Canary/docs/sdds/` |
| elJeffe spec | `~/GrowDirect/IP/specs/elJeffe_Protocol_Spec_v1.0.md` |
| CRDM v1.1 | `~/GrowDirect/IP/specs/CRDM_v1.1_Addendum.md` |
| Inscription pipeline | `~/GrowDirect/IP/specs/Inscription_Pipeline_Design_Spec_v1.0.md` |
| Field mappings | `~/GrowDirect/IP/specs/field_mappings.md` |
| ADR-001 | `~/GrowDirect/IP/adr/ADR-001_Multi_Tenant_Partition_Architecture.md` |
| Deploy pipeline | `~/GrowDirect/IP/infra/deployment_pipeline.md` |
| Work orders | `~/GrowDirect/IP/workorders/` |
| GitNexus seed | `~/GrowDirect/IP/gitnexus-seed/` |
| GitNexus index | `~/GrowDirect/Canary/.gitnexus/meta.json` |

---

*Canary LP | GrowDirect Inc. | Confidential*
