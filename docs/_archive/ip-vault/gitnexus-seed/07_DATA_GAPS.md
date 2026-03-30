---
type: research
domain: canary
status: active
created: 2026-03-19
updated: 2026-03-19
---
# Canary LP — Data Model Gap-to-Target Map

> **Domain:** Current state vs target state, migration priorities, blocked capabilities
> **Source Issues:** GRO-265 (field registry, done), GRO-266 (data coverage), GRO-267 (CRDM gap scan)
> **Last Updated:** 2026-03-19 | **Classification:** Confidential

---

## Executive Summary

The field registry audit (GRO-265) revealed Canary is at 28% coverage of its own 86-table schema. Critical LP data from Square payloads we already receive is being dropped. The CRDM v1.1 spec defined 11 architectural amendments for POS-agnostic data modeling; only 2 are implemented. 25 `square_*` columns remain hardcoded across 14 model files, locking the schema to a single POS vendor.

This document maps the gap between what is built and what the design calls for, so that contextual memory steers every development session toward the target architecture.

---

## Amendment 1: external_identities (P1 — Foundation)

**Current state:** 25 columns prefixed with `square_` hardcoded across 14 model files (transactions, employees, locations, customers, products, devices, etc.). Every column name embeds vendor identity into the schema.

**Target state:** A single `external_identities` join table that maps Canary UUIDs to any POS system's identifiers. Table structure: `(canary_id UUID, source_system_id FK, external_type TEXT, external_value TEXT)`. All existing `square_*` columns migrate to rows in this table.

**Why P1:** Amendments 5 (canonical renames), 6 (JSONB attributes), and 7 (location_product_authorizations) all depend on external_identities existing. Every parser shipped before this migration adds more vendor-locked columns. The migration gets harder with every day.

**Blocked capabilities:** All multi-POS support (Clover, Toast, Lightspeed onboarding), vendor-neutral Chirp rules, clean RaaS API contracts.

---

## Amendment 2: product_identifiers

**Current state:** Products have a single `product_id` field mapped to Square's catalog item ID. No barcode, UPC, EAN, ISBN, SKU, or PLU support.

**Target state:** `product_identifiers` table: `(product_id FK, identifier_type ENUM, identifier_value TEXT, source_system_id FK)`. One product can have many identifiers across different standards.

**Blocked capabilities:** Barcode swap detection (top-5 shrink method in LP industry). Price integrity rules that cross-reference catalog identifiers. Multi-POS product matching.

---

## Amendment 3: product_compositions

**Current state:** Bundled/kit items appear as single opaque line items. A "Gift Basket" shows as one $50 item; the 8 items inside are invisible.

**Target state:** `product_compositions` table: `(parent_product_id FK, child_product_id FK, quantity INT, relationship_type ENUM)`. Bundles decompose into individual components for shrink analysis.

**Blocked capabilities:** Bundle shrink detection (removing items from kits), component-level inventory reconciliation, accurate cost-of-goods calculation for composite products.

---

## Amendment 4: categories Hierarchy

**Current state:** Flat `category_name` string field on products. No hierarchy, no parent-child relationships.

**Target state:** Self-referential `categories` table with materialized path: `(id, parent_id FK, name, path TEXT, depth INT)`. Enables queries like "all products in Electronics > Accessories."

**Blocked capabilities:** Category-scoped Chirp rules (e.g., "alert if refund rate in category X exceeds threshold"), category-level analytics, cannabis compliance rules scoped to product categories (THC, CBD, accessories).

---

## Amendment 5: Canonical Renames

**Current state:** `square_product` column in transactions table. `*_name` suffix on employee, location, and product display fields.

**Target state:** `square_product` → `source_channel`. `*_name` → `display_name`. All field names vendor-neutral.

**Depends on:** Amendment 1 (external_identities) — can't rename until the vendor-specific columns are migrated.

---

## Amendment 6: JSONB attributes

**Current state:** No extensibility for POS-specific fields that don't fit the canonical model.

**Target state:** JSONB `attributes` column on core entity tables (transactions, employees, products, locations). Stores vendor-specific data that isn't part of the canonical CRDM. Enables future POS integrations to carry their unique fields without schema changes.

**Depends on:** Amendment 1 (external_identities) — the attributes column replaces the need for vendor-prefixed columns.

---

## Amendment 7: location_product_authorizations

**Current state:** No concept of which products are authorized for sale at which locations.

**Target state:** `location_product_authorizations` table: `(location_id FK, product_id FK, authorized BOOLEAN, effective_date, expiry_date)`. Represents the store planogram in data form.

**Blocked capabilities:** Diversion detection (product sold at unauthorized location), unauthorized sales alerts, regulatory compliance for controlled substances, cannabis dispensary product authorization tracking.

**Depends on:** Amendment 1 (external_identities) for clean product and location references.

---

## Amendment 8: Device Graph (Partial)

**Current state:** Flat `devices` table with basic fields. No hierarchy, no multi-device-per-transaction join.

**Target state:** Hierarchical device model: `devices` table with `parent_device_id` self-reference + `transaction_devices` many-to-many join table. Enables device tree construction (POS terminal → peripheral → scanner → scale).

**Partially built:** Basic device table exists. Missing: hierarchy, transaction_devices join, device graph traversal for Merkle batch attestation.

**Blocked capabilities:** Full device attestation in Merkle batches (C-901–C-909 rules), device integrity tracking, multi-device correlation analysis.

---

## Parser Enrichment Gaps (Tier 1 — Data Arrives, Fields Dropped)

These fields exist in Square webhook payloads we already receive but are discarded by the current parser:

| Data Domain | Dropped Fields | Impact |
|-------------|---------------|--------|
| Order discounts | name, type, %, scope, reward_ids, pricing_rule_id | C-201 blind |
| Order taxes | name, type, %, scope | Tax analytics blind |
| Order service charges | all fields | Fee anomaly detection blind |
| Order modifiers | all fields | C-203 blind |
| Order rewards | all fields | Loyalty-transaction link broken |
| Order fulfillments | all fields | Fulfillment fraud invisible |
| Order returns | return detail beyond is_voided | Return analysis limited |
| Gift card activity | order_id, line_item_uid, payment_id, buyer_payment_instrument_ids | C-602 blind |
| Payment details | delay_action, approved_money, card_type, bin, verification_method, processing_fee | C-009, C-010 blind |

---

## Existing Tables With No Parser (Tier 2)

| Table | Webhook Events | Current Handling |
|-------|---------------|-----------------|
| invoices | 8 invoice events | log_only (no parsing) |
| devices | device events | log_only |
| gift_cards | customer link/unlink | log_only |
| loyalty_events | account deletion | log_only |

---

## No Model, No Parser (Tier 3 — Future)

| Square Event Domain | LP Value |
|---------------------|----------|
| catalog.version.updated | Stale product prices → wrong price override detection |
| customer.* events | Stale customer profiles → broken velocity tracking |
| terminal.checkout/refund | Terminal-level fraud patterns |
| card.* events | Card-on-file fraud |
| subscription.* | Recurring billing anomalies |
| labor.scheduled_shift.* | Ghost scheduling detection |
| bank_account.* | Financial operations monitoring |
| vendor.* | Vendor relationship tracking |
| location.* | Stale location data → wrong location attribution |

---

## Migration Sequence (Recommended)

1. **external_identities** (Amendment 1) — Foundation. Unblocks Amendments 5, 6, 7. Eliminates vendor lock.
2. **line_item_discounts + line_item_taxes** (GRO-266 Tier 1) — Unblocks C-201, tax analytics.
3. **line_item_modifiers** (GRO-266 Tier 1) — Unblocks C-203.
4. **Parser enrichment** (GRO-266 Tier 1) — Capture payment.approved_money, delay_action, gift card fields.
5. **product_identifiers** (Amendment 2) — Unblocks barcode swap detection.
6. **categories hierarchy** (Amendment 4) — Unblocks category-scoped rules.
7. **location_product_authorizations** (Amendment 7) — Unblocks diversion detection.
8. **product_compositions** (Amendment 3) — Bundle transparency.
9. **Device graph completion** (Amendment 8) — Full device attestation.
10. **Canonical renames + JSONB attrs** (Amendments 5+6) — Post-migration cleanup.
11. **Tier 2 parser activation** — Invoices, devices, gift card link events.

---

## Process Deliverable

GRO-266 introduces a new skill: `canary-data-expansion` — the factory process for adding or enriching Square data domains. Ensures field-registry.json, parsers, models, dispatch routes, Chirp rules, and Owl search all stay in sync when expanding data coverage.

---

*Canary LP | GrowDirect Inc. | Confidential*
