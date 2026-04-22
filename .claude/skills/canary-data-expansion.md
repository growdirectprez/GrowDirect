---
name: canary-data-expansion
roles-primary:[Engineer]
roles-assist:[Architect]
description: |
  Factory process for expanding the Canary data model. Use when adding a new
  Square data domain, enriching an existing parser with dropped fields, wiring
  a log-only event to a parser, creating new CRDM tables, or reconciling the
  field registry against the live database. Ensures field registry, parsers,
  models, dispatch routes, Chirp rules, Owl search, metrics aggregation, and
  reference docs stay in sync. Four patterns: Registry Reconciliation
  (Pattern 0), Parser Enrichment (Tier 1), Parser Wiring (Tier 2), New
  Domain (Tier 3).
allowed-tools:
  - Read
  - Bash
  - Edit
  - Write
  - Grep
  - Glob
---

# Canary Data Expansion — Square Data Model Factory Process

> "We are missing entire data domains." — Jeffe, Mar 19, 2026

## Overview

Repeatable process for expanding Canary's coverage of the Square API data
universe. Every Square webhook event type should flow through TSP, land in
a CRDM table, feed Chirp detection, surface in Owl search, aggregate into
metrics, and appear in the field registry. When any of these layers is
missing, the system has a gap.

**Announce at start:** "I'm using canary-data-expansion to [add/enrich/wire] the [domain] data pipeline."

**Reference doc:** `docs/field-registry/square-coverage-matrix.md`
**Field registry:** `docs/field-registry.json`
**Dispatch registry:** `canary/services/webhook_dispatch.py`

---

## When to Use This Skill

- **Reconciling** the field registry against the live database (Pattern 0)
- Adding a new Square data domain (e.g., subscriptions, bookings, vendors)
- Enriching an existing parser with fields Square sends but we drop
- Wiring a log-only webhook event to a parser and CRDM table
- Creating new CRDM tables for data we receive but don't store
- After a Square API changelog reveals new fields we should capture
- After any migration or model change that adds/removes tables or columns

## When NOT to Use This Skill

- Building UI features (use canary-blueprint)
- Writing Chirp detection rules (use canary-tdd with chirp marker)
- Fixing parser bugs (use canary-debug)

---

## The Four Patterns

### Pattern 0: Registry Reconciliation

**When:** The field registry may be out of sync with the live database.

Diff `pg_tables` against `docs/field-registry.json`. Classify gaps as
merchant-facing data (MUST add), internal infrastructure (exclusion list),
metrics/analytics (add under metrics domain), or deprecated (investigate).
Get column metadata, add missing tables, update ERDs, validate and rebuild.

### Pattern 1: Parser Enrichment (Tier 1)

**When:** Data flows through TSP, a parser exists, but fields are dropped.

Document the gap, extend the model if needed, enrich the parser, update
field registry, update Owl search, update Chirp rules, evaluate metrics
impact, test end-to-end, rebuild and seed.

### Pattern 2: Parser Wiring (Tier 2)

**When:** Model and table exist, webhook events flow but are `log_only=True`.

Write the parser, update dispatch registry, add field registry entries,
add Owl search fields, evaluate metrics impact, test end-to-end, rebuild.

### Pattern 3: New Domain (Tier 3)

**When:** Square sends webhook events for a domain we have no model for.

Research Square API, design model, create Alembic migration, write parser,
update dispatch, add field registry, add Owl search, evaluate Chirp rules,
define and wire metrics, test end-to-end, rebuild and seed.

---

## The Sync Contract — 8 Layers

Every data expansion MUST update ALL of these layers:

1. **Dispatch Registry** — `canary/services/webhook_dispatch.py`
2. **Parser** — `canary/services/parsers/square_*_parser.py`
3. **CRDM Model** — `canary/models/sales/*.py` or `canary/models/app/*.py`
4. **Field Registry** — `docs/field-registry.json`
5. **Owl Search** — `canary/services/owl/search/registry.py`
6. **Chirp Detection** — `canary/services/chirp/rule_definitions.py` (if LP-relevant)
7. **Metrics Aggregation** — `canary/models/metrics/facts.py` + `canary/services/metrics_etl.py`
8. **Coverage Matrix** — `docs/field-registry/square-coverage-matrix.md`

If you touch ANY layer, verify ALL downstream layers are in sync.

---

## Parser Standards — EVERY FIELD ALWAYS NO EXCEPTIONS

> "EVERY FIELD ALWAYS NO EXCEPTIONS into the Parser." — Jeffe, Mar 19, 2026

When Square sends a field in a payload, we parse it and store it. Period.

Rules:
1. EVERY FIELD — if Square's API reference lists it, the parser extracts it
2. ALWAYS — not "when convenient" or "in phase 2"
3. NO EXCEPTIONS — not even for fields that seem useless today
4. Use our canonical UUID as the primary key — never Square's ID (GRO-237)
5. Store Square's ID as `external_id` or `square_*_id` — for reconciliation only
6. Resolve transaction links — lookup by external_id if needed, populate our UUID
7. Handle missing fields gracefully — `payload.get("field")` with sensible defaults
8. Parse nested objects — Square nests heavily
9. Parse money objects — always extract `.amount`, store as `_cents`
10. Parse arrays into child tables — discounts[], taxes[], modifiers[]
11. Log warnings for unexpected structure — don't silently drop data

---

## Transaction Linking Rule

Every entity that relates to a transaction MUST populate its transaction link field.
This is non-negotiable. The entire LP value chain depends on connecting events
to transactions.

---

## Decision Tree

```
Is this a reconciliation / backfill task?
  YES -> Pattern 0: Registry Reconciliation
  NO  -> Does webhook_dispatch.py have a route?
    YES -> Is it log_only=True?
      YES -> Does a CRDM model exist?
        YES -> Pattern 2: Parser Wiring
        NO  -> Pattern 3: New Domain
      NO  -> Does parser extract ALL fields?
        YES -> Check field registry + Owl completeness
        NO  -> Pattern 1: Parser Enrichment
    NO  -> Does Square send webhooks for this domain?
      YES -> Pattern 3: New Domain
      NO  -> Design batch sync job or check RAAS
```

---

*Canary Data Expansion v1.2 — Square Data Model Factory Process*
*GRO-266: Data model completeness | GRO-270: Registry reconciliation*
