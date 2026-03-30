---
type: workorder
domain: raas
status: active
created: 2026-03-18
updated: 2026-03-19
---
# CRDM v1.1 Alignment Amendment — Namespace Bridge + Device Attestation + Source System Refactor

**Issue Context:** GRO-47, GRO-46, GRO-13, GRO-45
**Prepared By:** ALX (Chief of Staff)
**Date:** March 2, 2026
**Classification:** MAXIMUM CONFIDENTIAL — Architecture Amendment
**Origin:** Jeffe alignment review of 4-issue stack (GRO-47/46/13/45)
**Routes To:** Tom (schema + contract), Jeremy (implementation), Jim (QA)
**Gate:** Tom validates DDL, Jim QA reviews

---

## 0. Purpose

During top-down alignment review of the four foundational issues (GRO-46 Serializable Gate → GRO-13 RaaS Reframe → GRO-45 CRDM v1.1 → GRO-47 Namespace PoC), three seam gaps were identified. This amendment closes all three.

**The stack:**
```
GRO-46  Serializable Gate (DESIGN — the WHY)
   ↓    "Portable non-consumable identity gate on a Bitcoin Ordinal"
GRO-13  RaaS Reframe + Namespace Decisions (BUSINESS — the HOW)
   ↓    6 locked decisions, RaaS API spec, revenue model, L402 gate
GRO-45  CRDM v1.1 (DATA — the WHAT)
   ↓    external_identities, device graph, POS-agnostic schema
GRO-47  Namespace PoC (PROOF — the BUILD)
        Webhook → inscription → verify round-trip
```

---

## Amendment A: Namespace → CRDM Merchant Bridge

### Problem

GRO-13's RaaS API receives `merchant_id: "sunrise-coffee.jeffe"` (namespace string). The CRDM uses `merchant_id` (UUID). No join point exists between the two identity systems.

### Solution: `namespace_registrations` Table

```sql
CREATE TABLE canary_app.namespace_registrations (
    id                  UUID            NOT NULL DEFAULT gen_random_uuid(),
    merchant_id         UUID            NOT NULL,
    namespace_name      TEXT            NOT NULL,   -- 'sunrise-coffee.jeffe'
    namespace_root      TEXT            NOT NULL,   -- 'jeffe' (supports future roots)
    inscription_id      TEXT,                       -- Bitcoin Ordinal inscription ID
    inscription_block   BIGINT,                     -- Block height of inscription
    avalanche_address   TEXT,                       -- NameRegistry contract address on subnet
    tier                TEXT            NOT NULL DEFAULT 'standard',
    status              TEXT            NOT NULL DEFAULT 'active',
    registered_at       TIMESTAMPTZ     NOT NULL DEFAULT now(),
    expires_at          TIMESTAMPTZ,                -- Annual renewal (GRO-13 Decision 3)
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),

    CONSTRAINT pk_namespace_registrations PRIMARY KEY (id),
    CONSTRAINT fk_nr_merchant FOREIGN KEY (merchant_id)
        REFERENCES merchants(merchant_id) ON DELETE CASCADE,
    CONSTRAINT uix_nr_namespace_name UNIQUE (namespace_name),
    CONSTRAINT chk_nr_tier CHECK (tier IN ('free', 'standard', 'enterprise')),
    CONSTRAINT chk_nr_status CHECK (status IN (
        'reserved', 'claimed', 'active', 'expired', 'suspended'
    ))
);

-- Hot lookup: resolve namespace → merchant_id (RaaS /v1/verify critical path)
CREATE INDEX idx_nr_namespace_lookup
    ON namespace_registrations (namespace_name) WHERE status = 'active';

-- Reverse: what namespaces does this merchant own?
CREATE INDEX idx_nr_merchant
    ON namespace_registrations (merchant_id);

-- RLS
ALTER TABLE namespace_registrations ENABLE ROW LEVEL SECURITY;
ALTER TABLE namespace_registrations FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON namespace_registrations
    USING (merchant_id = current_setting('app.current_merchant_id')::uuid);
```

### RaaS Verification Flow (Updated)

```
POST /v1/verify { merchant_id: "sunrise-coffee.jeffe", event_hash: "sha256:..." }
  │
  ├─ 1. L402 middleware validates payment (1 sat)
  ├─ 2. namespace_registrations WHERE namespace_name = 'sunrise-coffee.jeffe' AND status = 'active'
  │     → returns canonical merchant_id (UUID)
  ├─ 3. evidence_records WHERE merchant_id = <uuid> AND event_hash = <hash>
  ├─ 4. merkle_batches → inscription proof
  └─ 5. Return { verified: true, block: XXXXXX, namespace: "sunrise-coffee.jeffe" }
```

### Status Values (Maps to GRO-13 Decision 1)

| Status | Meaning | Transition |
|--------|---------|------------|
| `reserved` | Pre-minted for Fortune 500 / top categories | → `claimed` when enterprise engages |
| `claimed` | Assigned to merchant, no receipts yet | → `active` on first inscription |
| `active` | Live namespace with receipts flowing | → `expired` if renewal lapses |
| `expired` | Past renewal date, 30-day grace period | → `active` on renewal; released after grace |
| `suspended` | Admin action (dispute, abuse, legal hold) | → `active` on resolution |

### Design Rationale

- **Lives in CRDM, not on-chain.** The Avalanche NameRegistry handles ownership + payment gating. The CRDM table handles operational mapping. Cross-references (`inscription_id`, `avalanche_address`) link the two worlds.
- **`namespace_root` field.** Supports future namespace roots beyond `.jeffe`. If the protocol expands, the root column enables routing without schema changes.
- **Partial index on active namespaces.** The RaaS hot path only needs active registrations. The partial index keeps the lookup fast as the table grows with expired/suspended records.

---

## Amendment B: Configurable Device Attestation in Inscription Payload

### Problem

GRO-47's Merkle batch inscription doesn't include device context from GRO-45's device graph (Amendment 8: `devices` + `transaction_devices`). Jeffe's directive: "We should be able to enforce device integrity or not" — configurable per merchant.

### Solution: Optional `attestation` Block in Inscription Payload

**Protocol version bump:** 1.0 → 1.1

```json
{
  "protocol": "jeffe",
  "version": "1.1",
  "type": "merkle_batch",
  "namespace": "sunrise-coffee",
  "batch_id": "<uuid>",
  "merkle_root": "<sha256 hash of event Merkle tree>",
  "event_count": 42,
  "time_range": {
    "first": "2026-03-01T00:00:00Z",
    "last": "2026-03-01T01:30:00Z"
  },
  "chain": {
    "previous": "<prior inscription_id>",
    "sequence": 1
  },
  "attestation": {
    "device_integrity": true,
    "device_count": 3,
    "device_root": "<sha256 hash of device Merkle tree>",
    "flags": ["C-901", "C-904"]
  }
}
```

### Feature Flag Behavior

| Merchant Setting | `attestation` Block | Behavior |
|---|---|---|
| `device_attestation = off` | **Omitted entirely** | Inscription is device-blind. Pure event hash chain. ~300 bytes. |
| `device_attestation = on` | **Present, no flags** | Sub 3 builds parallel device Merkle tree from `transaction_devices`. `device_root` seals which devices processed this batch. ~400 bytes. |
| `device_attestation = on` + Chirp triggers | **Present, flags populated** | If any event triggered device Chirp rules (C-901 ghost device, C-904 device swap, C-905 unauthorized pairing, etc.), flag codes appear in array. Anomalies are on Bitcoin permanently. ~450 bytes. |

### Parallel Merkle Trees

When device attestation is ON, Sub 3 builds two parallel Merkle trees over the same batch boundary:

```
Event Merkle Tree:                    Device Merkle Tree:
    merkle_root                           device_root
      /     \                               /     \
   h(e1+e2)  h(e3+e4)                 h(d1+d2)  h(d3+d4)
   /    \      /    \                  /    \      /    \
 h(e1) h(e2) h(e3) h(e4)          h(d1) h(d2) h(d3) h(d4)

Where:
  e(n) = sha256(event_id || event_hash || timestamp)
  d(n) = sha256(device_id || device_type || transaction_id || timestamp)
```

Both trees share the same batch boundary (same events, same time range). Verification can check either root independently.

### Verification Flow (Updated for Device Attestation)

```
POST /v1/verify { event_hash: "sha256:...", include_device: true }

Response (device_attestation = on):
{
  "verified": true,
  "block": 884201,
  "inscription_id": "i39f7a...",
  "namespace": "sunrise-coffee.jeffe",
  "device_attestation": {
    "integrity": true,
    "device_count": 3,
    "flags": [],
    "device_proof_available": true
  }
}

Response (device_attestation = off):
{
  "verified": true,
  "block": 884201,
  "inscription_id": "i39f7a...",
  "namespace": "sunrise-coffee.jeffe",
  "device_attestation": null
}
```

### Use Case Mapping

| Consumer | Device Attestation Value |
|----------|------------------------|
| Small coffee shop (Canary LP basic) | OFF — doesn't need device tracking |
| Multi-location retailer (Canary LP pro) | ON — ghost device detection is LP gold |
| External insurer (RaaS consumer) | Reads the `attestation` block to assess claim risk |
| Auditor (RaaS consumer) | Requires `device_integrity: true` + zero flags for clean audit |
| Franchise compliance team | ON + flags = automatic escalation for device anomalies |

### Inscription Cost Impact

| Config | Payload Size | Inscription Cost (~10 sat/vbyte) |
|--------|-------------|----------------------------------|
| Device OFF | ~300 bytes | ~$0.50–$2.00 |
| Device ON, no flags | ~400 bytes | ~$0.75–$2.50 |
| Device ON, with flags | ~450 bytes | ~$0.85–$3.00 |

Trivial cost difference. The feature flag is a product decision, not a cost decision.

---

## Amendment C: Source System Reference Table

### Problem

GRO-45's `external_identities.source_system` uses a CHECK constraint with hardcoded POS list. GRO-46's cross-vertical vision (retail → healthcare → supply chain → IoT) means source systems will include non-POS platforms. CHECK constraints require DDL migrations to add new sources.

### Solution: `source_systems` Reference Table

```sql
CREATE TABLE canary_app.source_systems (
    code                TEXT            NOT NULL,
    display_name        TEXT            NOT NULL,
    category            TEXT            NOT NULL DEFAULT 'pos',
    is_active           BOOLEAN         NOT NULL DEFAULT true,
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),

    CONSTRAINT pk_source_systems PRIMARY KEY (code),
    CONSTRAINT chk_ss_category CHECK (category IN (
        'pos',              -- Square, Clover, Toast, Shopify, etc.
        'ehr',              -- Healthcare (Epic, Cerner, Allscripts, etc.)
        'logistics',        -- Supply chain (SAP, Oracle SCM, etc.)
        'iot',              -- IoT platforms (AWS IoT, Azure IoT Hub, etc.)
        'financial',        -- Banking, insurance, payment processors
        'identity',         -- OAuth providers, SSO, identity platforms
        'manual'            -- Human-entered data
    ))
);

-- Seed current POS systems
INSERT INTO canary_app.source_systems (code, display_name, category) VALUES
    ('square',      'Square',           'pos'),
    ('clover',      'Clover',           'pos'),
    ('toast',       'Toast',            'pos'),
    ('shopify',     'Shopify POS',      'pos'),
    ('dutchie',     'Dutchie',          'pos'),
    ('cova',        'Cova',             'pos'),
    ('lightspeed',  'Lightspeed',       'pos'),
    ('revel',       'Revel',            'pos'),
    ('micros',      'Oracle MICROS',    'pos'),
    ('ncr',         'NCR',              'pos'),
    ('manual',      'Manual Entry',     'manual');

-- Migration: Replace CHECK with FK
ALTER TABLE canary_app.external_identities
    DROP CONSTRAINT chk_ei_source_system;

ALTER TABLE canary_app.external_identities
    ADD CONSTRAINT fk_ei_source_system
    FOREIGN KEY (source_system) REFERENCES canary_app.source_systems(code);
```

### What Changes

| Before (v1.1) | After (v1.1 + Amendment C) |
|---|---|
| Adding a POS requires ALTER TABLE (DDL migration) | Adding a source is INSERT (data migration) |
| Only POS sources supported | Any source category supported |
| No metadata about source capabilities | `category` enables pipeline routing by source type |
| CHECK constraint validates at DB level | FK validates at DB level (same integrity, more flexible) |

### Category-Based Pipeline Routing (Future)

The `category` field enables different pipeline behavior per source type:

| Category | Parser Pipeline | Compliance Layer | Device Graph |
|----------|----------------|-----------------|-------------|
| `pos` | Standard CRDM parse | PCI DSS | POS + peripheral devices |
| `ehr` | HIPAA-compliant parse | HIPAA, HITECH | Medical devices |
| `logistics` | Supply chain parse | Customs, trade compliance | IoT sensors, GPS |
| `financial` | Financial parse | SOX, PCI | ATM, terminal, mobile |
| `iot` | Raw telemetry parse | Varies | Full device graph |

This is GRO-46's cross-vertical vision made concrete in the data layer. Same `external_identities` table, different routing.

### Note: entity_type CHECK

The `entity_type` CHECK constraint on `external_identities` has the same rigidity problem. Flagging for a future GRO — the same reference table pattern should apply. Not doing it in this amendment to keep scope tight.

---

## Summary of Changes

| Amendment | Table | Change | Impact |
|-----------|-------|--------|--------|
| A | `namespace_registrations` (NEW) | Bridge .jeffe names to CRDM merchant_id | Unblocks GRO-47 /v1/verify flow |
| B | Inscription payload schema | Optional `attestation` block with device Merkle tree | Feature-flagged device integrity on inscription |
| B | /v1/verify response schema | Optional `device_attestation` in response | RaaS consumers can read device integrity |
| C | `source_systems` (NEW) | Reference table for source system codes | Enables cross-vertical expansion (GRO-46) |
| C | `external_identities` | CHECK → FK on source_system | Adding sources is INSERT, not DDL |

## Routing

| Agent | Action |
|-------|--------|
| **Tom** | Validate all DDL. Confirm `namespace_registrations` fits NameRegistry contract design. Confirm parallel Merkle tree approach for device attestation. |
| **Jeremy** | Implementation estimate for: (1) namespace resolution in RaaS middleware, (2) feature-flagged device tree in Sub 3, (3) source_systems migration. |
| **Jim** | QA review: migration plan for CHECK → FK swap on external_identities. Test plan for device attestation ON/OFF. |
| **Syd** | Review: Does optional device attestation create liability if a merchant turns it OFF and an incident occurs? "You could have known" argument. |

---

*ALX | GRO-47/46/13/45 Alignment Amendment | March 2, 2026*
*MAXIMUM CONFIDENTIAL*
