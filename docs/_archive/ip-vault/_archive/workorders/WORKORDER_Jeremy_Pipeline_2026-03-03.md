---
type: spec
domain: canary
status: active
created: 2026-03-03
updated: 2026-03-19
---
# Work Order — Core Pipeline Build
**To:** Jeremy (Developer / Quant)
**From:** ALX (Chief of Staff), authorized by Jeffe (CEO)
**Date:** March 3, 2026
**Classification:** INTERNAL
**Linear Parent:** GRO-47
**Spec References:** CRDM v1.1-B Addendum, elJeffe Protocol Spec v1.0, Inscription Pipeline Design Spec v1.0

---

## Directive

Build the core data pipeline end-to-end: Square OAuth through webhook receipt to sealed evidence records to canonical CRDM tables. No front-end. No dashboards. No inscription yet. Focus entirely on data flow, DB integrity, and test tooling.

**Jeffe's words:** *"Less front-end functionality, more DB query capability and data flow validating triggers testing and tools for monitoring app config and membership framework. As we do this we can layer dashboarding as we iterate and understand the data. Data pumps for each webhook to unit test it and see tables populate and then knitting those into integration tests to tie into user stories. Very solid and documented along the way. No rush — I want to get it right."*

---

## Build Sequence

Each phase depends on the one before it. Do not skip ahead. Each phase ships with its own data pump, unit tests, and documentation before moving to the next.

### Phase 0-A: Square OAuth + Sandbox Credentials

**What:** Stand up the Square OAuth2 token exchange. Sandbox first.

**Deliverables:**
- OAuth2 authorization code flow → access token + refresh token
- Automatic token refresh before expiry
- Credentials stored in environment variables (never DB, never repo)
- Sandbox merchant ID configured and tested

**Done when:** You can programmatically obtain a valid Square sandbox access token, refresh it, and use it to call any Square API endpoint.

**Test:** Manual trigger of OAuth flow → token received → token refreshed → Square API call succeeds.

---

### Phase 0-B: Webhook Receiver + Monitor

**What:** Stand up the API gateway webhook endpoint. Receive Square sandbox webhooks, HMAC-verify signatures, log events to structured monitoring.

**Deliverables:**
- HTTP endpoint that receives Square webhook POST requests
- HMAC-SHA256 signature verification against Square's webhook signature key
- Structured JSON logging per event (timestamp, event type, merchant ID, signature status)
- Rejection + logging for failed HMAC verification
- Health check endpoint

**Data Pumps:**
Create one data pump per Square webhook event type. Each pump replays a canned JSON payload (captured from sandbox) through the receiver.

| Pump | Event Type | Canned Payload Source |
|------|-----------|----------------------|
| pump-payment-created | `payment.created` | Square sandbox capture |
| pump-payment-updated | `payment.updated` | Square sandbox capture |
| pump-order-created | `order.created` | Square sandbox capture |
| pump-order-updated | `order.updated` | Square sandbox capture |
| pump-refund-created | `refund.created` | Square sandbox capture |
| pump-inventory-count | `inventory.count.updated` | Square sandbox capture |

**Done when:** Each pump fires independently. Each event is received, HMAC-verified, and logged. Unit test per pump proves the receiver handles the event type correctly. Failed HMAC payloads are rejected and logged.

---

### Phase 1-A: Sub 1 — Hash and Seal

**What:** Implement TSP Subscriber 1. Event arrives from webhook receiver → SHA-256 hash the raw payload → write to `evidence_records`.

**Deliverables:**
- SHA-256 hash of the raw webhook payload body (before any parsing)
- Row written to `canary_sales.evidence_records`:
  - `event_hash`: the SHA-256 digest
  - `sealed_at`: timestamp of sealing
  - `source_system`: `'square'` (from `source_systems` reference)
  - `raw_payload`: the original JSON (stored for replay/audit)
- Valkey stream integration: event published to `canary:events` stream after sealing

**Data Pumps:** Extend Phase 0-B pumps. Each pump now flows through Sub 1 and verifies a row lands in `evidence_records`.

**Done when:**
- For each canned payload, `evidence_records` contains a row with correct hash
- DB query confirms: `SELECT event_hash, sealed_at, source_system FROM evidence_records WHERE id = ?` returns expected values
- Hash is deterministic: same payload → same hash every time
- Unit test per pump: fire pump → assert row exists → assert hash matches manual computation

---

### Phase 1-B: Sub 2 — Parse to CRDM

**What:** Implement TSP Subscriber 2. Sealed event → route to Square parser → transform to canonical CRDM records.

**Deliverables:**
- Square-specific parser that reads raw payload and produces CRDM records
- External identity mapping: Square object IDs → CRDM UUIDs via `external_identities` table
- Records written to CRDM tables:
  - `transactions` (from payment/order events)
  - `line_items` (from order item details)
  - `payments` (from payment events)
  - `refunds` (from refund events)
  - `inventory_snapshots` (from inventory count events)
- Idempotency: re-processing the same event does not create duplicate records (use `external_identities` dedup)

**Field Mapping Documentation:**
Document every field mapping from Square → CRDM. Format:

```
Square: payment.amount_money.amount (integer, cents)
CRDM:   payments.amount (numeric, dollars — divide by 100)
```

Every mapped field gets this treatment. No undocumented transformations.

**Data Pumps:** Extend Phase 1-A pumps. Each pump now flows end-to-end (webhook → seal → parse) and verifies CRDM tables populate.

**Done when:**
- For each canned payload, correct CRDM tables contain correct rows
- `external_identities` maps Square IDs to CRDM UUIDs
- Re-running a pump does NOT create duplicate records
- DB query per CRDM table confirms field values match expected mappings
- Unit test per pump per CRDM table: fire pump → assert rows → assert field values
- Integration test: fire all pumps in sequence → query all CRDM tables → verify cross-table FK integrity

---

## Integration Test Environment

Build this in parallel with the pipeline phases. Each phase adds to the toolchain.

### DB Query Tool
- CLI or script that queries any CRDM table and returns formatted output
- Supports: table inspection, row counts, specific row lookup by ID, FK validation
- Jeremy and Jim both use this to verify pipeline output

### Trigger Validation
- Verify `updated_at` triggers fire on all tables that have them (namespace_registrations, merchant_feature_flags)
- Verify FK cascades work (merchant delete → cascades correctly)
- Verify CHECK constraints reject bad data (invalid status values, invalid tiers)
- Each constraint gets its own negative test (insert bad data → assert rejection)

### Data Flow Validation
- End-to-end trace: given a webhook event ID, trace it through evidence_records → CRDM tables
- Orphan detection: find evidence_records with no corresponding CRDM records (parse failures)
- Duplicate detection: find CRDM records with duplicate external_identities

### App Config Framework
- `merchant_feature_flags` table working and queryable
- Feature flags toggle correctly in tests (device_attestation on/off, tier checks)
- Config changes don't require restart

### Monitoring
- Structured logs per pipeline stage (webhook received, sealed, parsed)
- Error logging with full context (which event, which stage, what failed)
- No stdout-only logging — everything goes to queryable structured format

---

## Architectural Constraints

1. **Schema JSON extensibility.** The inscription payload JSON (when we get to Sub 3) must be forward-compatible. No rigid enums, no strict validators that break on unknown keys. The merchant's ordinal is the first write, not the only write. Design all JSON handling to pass through unknown fields.

2. **GUID namespace.** All namespace references use `namespace_guid` (UUID), not human-readable names. The DDL in CRDM v1.1-B already reflects this. Don't build anything that assumes human-readable namespace strings on the data path.

3. **Idempotency everywhere.** Every pipeline stage must handle replays gracefully. Same event twice → same result, not duplicate records.

4. **Document as you build.** Every data pump, every field mapping, every test — documented in the code and in a companion test manifest. Jim will use this manifest to build QA test plans. If it's not documented, it doesn't count as done.

5. **No dashboard work.** Dashboarding layers in later once we understand the data through iteration. If you need to visualize something for debugging, use the DB query tool.

---

## Spec File Locations

| Document | Path |
|----------|------|
| CRDM v1.1-B Addendum (DDL) | `Canary_IP/Markdown/Specs/CRDM_v1.1_Addendum_Namespace_DeviceAttestation_SourceSystems.md` |
| elJeffe Protocol Spec | `Canary_IP/Markdown/Specs/elJeffe_Protocol_Spec_v1.0.md` |
| Inscription Pipeline Spec | `Canary_IP/Markdown/Specs/Inscription_Pipeline_Design_Spec_v1.0.md` |

The CRDM Addendum is the DDL source of truth. Build tables from that file. If the spec and the DDL disagree, the DDL wins — flag the discrepancy.

---

## Delivery Cadence

No sprint deadline. Quality over speed. But each phase should produce:

1. Working code
2. Passing data pumps + unit tests
3. Passing integration tests (cumulative — each phase adds to the suite)
4. Updated test manifest
5. Linear issue updated with findings

Jim gets a QA handoff at each phase gate. Nothing moves to the next phase without Jim confirming the data pumps work and the DB state is correct.

---

## Questions / Blockers → ALX

If you hit an ambiguity in the specs, a missing DDL, or a Square API behavior that doesn't match assumptions — log it in Linear and tag ALX. Don't guess. Don't work around it. Surface it.

---

*Work Order — Core Pipeline Build | March 3, 2026*
*INTERNAL — GrowDirect*
