---
type: spec
domain: canary
status: active
created: 2026-03-14
updated: 2026-03-19
---
# elJeffe Protocol Specification v1.0

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]

**Version:** 1.0
**Date:** March 2, 2026
**Authors:** Tom (Systems Architect), ALX (Chief of Staff)
**Directive:** Jeffe — "It's the modern day wax seal for the individual."
**Classification:** MAXIMUM CONFIDENTIAL — Core Protocol
**Status:** DRAFT — Pending Tom validation, Syd legal review, PhD patent review
**Source Issues:** GRO-46, GRO-47, GRO-13, GRO-45

---

> *"The seal doesn't need the seal-maker to still be alive for you to verify it's authentic."*
> — Jeffe, March 2, 2026

---

## 1. Problem Statement

Every digital receipt, transaction record, and verification credential in commerce today depends on a server. If the server goes offline, the proof disappears. If the company shuts down, the records vanish. If the database is compromised, the history is rewritten. There is no permanent, self-verifying, server-independent proof of commercial events.

Merchants need a verification system that is permanent (survives company failure), sovereign (no single operator dependency), and self-verifying (proof is mathematical, not institutional). Investors, auditors, insurers, and regulators need to verify receipt authenticity without trusting the merchant's infrastructure.

The cost of not solving this: receipt fraud remains a trust-the-database problem, loss prevention evidence is only as reliable as the merchant's server uptime, and every POS-specific verification system creates vendor lock-in.

---

## 2. Protocol Overview

The elJeffe Protocol is a self-describing, server-independent verification protocol that inscribes commercial events on Bitcoin as Ordinal inscriptions. It defines four inscription types, a namespace system for merchant identity, a Merkle batch format for efficient event anchoring, and a three-layer resolution stack that degrades gracefully from fast cloud operations to permanent on-chain truth.

### 2.1 Design Principles

| # | Principle | Meaning |
|---|-----------|---------|
| 1 | **Sovereign by default** | The protocol functions without any server. GrowDirect operates the fastest resolver, not the only possible resolver. |
| 2 | **Self-describing** | The Genesis inscription contains the full protocol spec. A developer reading one inscription can build a complete resolver. |
| 3 | **POS-agnostic** | The protocol operates on canonical event hashes. It does not know or care which POS system generated the event. |
| 4 | **Accumulative** | Every use of the namespace adds to its history. History compounds value. Namespace value grows with usage. |
| 5 | **Non-consumable** | The Ordinal is not spent when used. One key, infinite doors. The gate travels across contexts. |
| 6 | **Layered degradation** | Three resolution layers (L1 Bitcoin, L2 Avalanche, L3 Postgres). Any layer can fail without breaking the others. |
| 7 | **Math, not trust** | Verification is SHA-256 Merkle proof reconstruction, not a database lookup. Anyone can verify without trusting anyone. |

### 2.2 Protocol Vocabulary

| Term | Definition |
|------|-----------|
| **Inscription** | A JSON payload inscribed on Bitcoin as an Ordinal. Permanent, immutable, publicly readable. |
| **Namespace** | A pseudonymous merchant identity in the format `{guid}.jeffe`. Inscribed on Bitcoin L1. GUID-only — no human-readable name on-chain. |
| **Alias** | A human-readable name in the format `name.jeffe` registered on L2 (Avalanche). Maps to a namespace GUID. Owner can have many aliases per GUID. |
| **Burner** | A disposable sub-address minted on Avalanche L2. Format: `label.name.jeffe`. Has a TTL. |
| **Merkle Batch** | A set of commercial events batched into a Merkle tree. The root hash is inscribed on Bitcoin. |
| **Chain** | The `chain.previous` field links each inscription to the prior one, forming an immutable sequence. |
| **Genesis** | The first inscription. Contains the full protocol spec. Root of the trust chain. |
| **Revocation** | An inscription that marks a namespace as expired, suspended, or transferred. |
| **Attestation** | Optional device integrity metadata included in a Merkle batch inscription. |
| **Serializable Gate** | The core property of the .jeffe Ordinal: portable, non-consumable, context-agnostic identity. |

---

## 3. Inscription Types

The protocol defines four inscription types. All inscriptions share a common header and chain linkage. Any inscription with `protocol: "jeffe"` and a `type` not in this list is invalid.

### 3.1 Common Header (All Inscription Types)

```json
{
  "protocol": "jeffe",
  "version": "1.0",
  "type": "<genesis | namespace | merkle_batch | revocation>",
  "chain": {
    "previous": "<inscription_id of prior inscription, or null for Genesis>",
    "sequence": "<integer, 0-indexed, monotonically increasing>"
  }
}
```

**Validation rules:**
- `protocol` MUST be `"jeffe"` (case-sensitive)
- `version` MUST be a valid semver string. Current: `"1.0"` or `"1.1"`
- `type` MUST be one of the four defined types
- `chain.previous` MUST be `null` only for Genesis. All other inscriptions MUST reference a valid prior inscription.
- `chain.sequence` MUST be monotonically increasing and is **per-namespace-global** — all inscription types for a given namespace share one counter. Example: namespace inscription (seq 0), first merkle_batch (seq 1), second merkle_batch (seq 2), revocation (seq 3). Enforced by UNIQUE constraint `(namespace_guid, chain_sequence)` on `merkle_batches` table. (Tom Review T-3)

### 3.2 Genesis Inscription

Created once. Contains the full protocol specification. Root of the trust chain for all .jeffe inscriptions.

```json
{
  "protocol": "jeffe",
  "version": "1.0",
  "type": "genesis",
  "created": "2026-03-XX",
  "root_authority": "<GrowDirect treasury public key>",
  "spec": {
    "namespace_format": "^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\\.jeffe$",
    "alias_format": "^[a-z0-9-]+\\.jeffe$",
    "subdomain_format": "^[a-z0-9-]+\\.[a-z0-9-]+\\.jeffe$",
    "inscription_types": ["genesis", "namespace", "merkle_batch", "revocation"],
    "verification_method": "sha256_merkle_proof",
    "payment_gate": "L402",
    "chain_rule": "Each inscription links to previous via chain.previous field, forming immutable sequence",
    "name_rules": {
      "min_length": 3,
      "max_length": 63,
      "allowed_chars": "a-z, 0-9, hyphen (not leading or trailing)",
      "reserved_prefix": ["xn--"]
    }
  },
  "resolver_hint": "https://api.eljeffe.io/v1/resolve/",
  "chain": {
    "previous": null,
    "sequence": 0
  }
}
```

**Constraints:**
- Only ONE Genesis inscription may exist. It is identified by `type: "genesis"` and `chain.previous: null`.
- `root_authority` is the GrowDirect treasury public key. All subsequent registrar signatures must chain to this key.
- `spec` contains the full grammar. A third party reading this JSON can build a resolver.
- `resolver_hint` is a convenience pointer, not a dependency. Resolvers MAY ignore it.
- Approximate size: ~500 bytes. Inscription cost at 10 sat/vbyte: ~$1–$3.

### 3.3 Namespace Inscription

Registers a pseudonymous merchant identity on Bitcoin. One inscription per namespace GUID. Permanent. The GUID provides the anonymity wall — no human-readable merchant identity exists on L1.

> **Privacy by design (Jeffe directive, March 3, 2026):** L1 is pseudonymous. Human-readable names live exclusively on L2 (Avalanche). The owner controls how many L2 identities point to their L1 GUID. On-chain data reveals event counts and Merkle roots — never merchant identity.

```json
{
  "protocol": "jeffe",
  "version": "1.0",
  "type": "namespace",
  "namespace_guid": "a3f9b2c1-7d4e-4f8a-9c6b-2e1d0f3a5b7c",
  "owner_pubkey": "<merchant's Bitcoin public key>",
  "registered_by": "<GrowDirect registrar public key>",
  "tier": "standard",
  "resolver_hint": "https://api.eljeffe.io/v1/resolve/",
  "chain": {
    "previous": "<genesis inscription_id or prior chain inscription_id>",
    "sequence": 1
  }
}
```

**Constraints:**
- `namespace_guid` MUST be a valid UUID v4 string. Format: `{uuid}.jeffe` (the `.jeffe` suffix is implicit in the inscription; the `namespace_guid` field contains only the UUID).
- No human-readable name, display name, category, region, or POS system metadata is inscribed on L1. These are L2 concerns.
- `owner_pubkey` is the namespace owner's public key. This is the pseudonymous identity anchor. Anyone can verify ownership of the GUID, but cannot determine merchant identity without L2 access.
- `registered_by` is the registrar's public key. MUST chain to Genesis `root_authority` (directly or via delegation).
- `tier` is one of: `free`, `standard`, `enterprise`. Determines L402 gate behavior and SLA.
- Approximate size: ~300 bytes (smaller than prior design — no metadata block). Inscription cost: ~$0.50–$2.00.

**Resolution:** A third party resolves a namespace GUID by scanning Bitcoin for `type: "namespace"` inscriptions matching the GUID, then verifying the `registered_by` key chains to the Genesis `root_authority`. To resolve a human-readable name to a GUID, the party MUST query L2 (Avalanche NameRegistry contract). GrowDirect's L3 cache provides fast lookup but is not authoritative for name→GUID mapping.

**Multi-identity:** A single L1 GUID can have many L2 human-readable aliases. Example: one merchant GUID maps to `sunrise-coffee`, `my-taco-truck`, `catering-co` on L2. Each alias is an L2 NameRegistry entry, not an L1 inscription. Creating or removing aliases does not touch Bitcoin.

### 3.4 Merkle Batch Inscription

Anchors a batch of commercial events to Bitcoin. The Merkle root of the batch is inscribed. Individual events are NOT inscribed — they are leaves in the Merkle tree, verifiable via proof reconstruction.

```json
{
  "protocol": "jeffe",
  "version": "1.1",
  "type": "merkle_batch",
  "namespace_guid": "a3f9b2c1-7d4e-4f8a-9c6b-2e1d0f3a5b7c",
  "batch_id": "<uuid>",
  "merkle_root": "<sha256 hash of event Merkle tree>",
  "event_count": 42,
  "time_range": {
    "first": "2026-03-01T00:00:00Z",
    "last": "2026-03-01T01:30:00Z"
  },
  "proof_data": {
    "tree_depth": 6,
    "algorithm": "sha256",
    "leaf_format": "sha256(event_id || event_hash || timestamp)"
  },
  "attestation": null,
  "chain": {
    "previous": "<prior inscription_id>",
    "sequence": 47
  }
}
```

**Constraints:**
- `namespace_guid` MUST match an existing namespace inscription's GUID
- `merkle_root` is the SHA-256 hash of the root node of the event Merkle tree
- `event_count` is the number of leaf events in the batch
- `time_range` defines the temporal boundary of the batch
- `proof_data` contains everything needed for deterministic proof reconstruction:
  - `tree_depth`: height of the Merkle tree
  - `algorithm`: hash algorithm used (always `sha256` in v1.0/v1.1)
  - `leaf_format`: describes how each leaf hash is computed
  - Note: `event_count` at the top level provides the leaf count. Per Tom Review T-5, `leaf_count` is consolidated into `event_count` (they are always equal).
- `attestation`: optional device integrity block (see Section 4)
- Approximate size: ~350 bytes (without attestation), ~450 bytes (with attestation)

**Verification flow (server-independent):**
1. Receive `event_hash` from the party requesting verification
2. Scan Bitcoin for `type: "merkle_batch"` inscriptions matching the namespace
3. For each batch: reconstruct the Merkle tree using `proof_data`
4. Check if `event_hash` exists as a leaf
5. Verify the reconstructed `merkle_root` matches the on-chain inscription
6. If match: event is verified. Return block height + inscription_id as proof.

### 3.5 Revocation Inscription

Marks a namespace as expired, suspended, or transferred. Required for sovereign expiry enforcement — without this, third-party resolvers would assume every namespace is permanently active.

```json
{
  "protocol": "jeffe",
  "version": "1.0",
  "type": "revocation",
  "target": "<inscription_id of the namespace being revoked>",
  "reason": "expired",
  "revoked_by": "<registrar public key>",
  "effective_at": "2027-03-15T00:00:00Z",
  "chain": {
    "previous": "<prior inscription_id>",
    "sequence": 48
  }
}
```

**Constraints:**
- `target` MUST reference a valid `type: "namespace"` inscription
- `reason` MUST be one of: `expired` (renewal lapsed), `suspended` (admin action), `transferred` (ownership change — disabled through Phase 2 per GRO-13 Decision 4)
- `revoked_by` MUST chain to Genesis `root_authority`
- `effective_at` is the timestamp after which the namespace no longer resolves
- Historical Merkle batch inscriptions anchored BEFORE `effective_at` remain valid. Revocation affects namespace resolution, not receipt verification. The seal doesn't break because the seal-holder's subscription lapsed.

**Resolution impact:** A third-party resolver checking a namespace MUST also check for revocation inscriptions targeting that namespace. If a revocation exists and `effective_at` is in the past, the namespace is no longer active.

---

## 4. Device Attestation (Protocol v1.1)

Device attestation is an optional extension that seals device integrity metadata alongside the event Merkle tree. It is feature-flagged per merchant.

### 4.1 Attestation Block

When enabled, the `attestation` field in a Merkle batch inscription is populated:

```json
"attestation": {
  "device_integrity": true,
  "device_count": 3,
  "device_root": "<sha256 hash of device Merkle tree>",
  "flags": ["C-901", "C-904"]
}
```

When disabled, the field is `null` or omitted entirely.

### 4.2 Behavior Matrix

| Merchant Setting | `attestation` Block | Inscription Behavior |
|---|---|---|
| `device_attestation = off` | `null` or omitted | Device-blind. Pure event hash chain. |
| `device_attestation = on`, clean batch | Present, `flags: []` | Device tree sealed. No anomalies detected. |
| `device_attestation = on`, anomalies | Present, `flags: ["C-901", ...]` | Device tree sealed. Chirp rule codes permanently recorded. |

### 4.3 Parallel Merkle Trees

When device attestation is ON, Sub 3 builds two parallel Merkle trees over the same batch boundary:

**Event Tree** (always built):
- Leaf hash: `sha256(event_id || event_hash || timestamp)`
- Root stored in `merkle_root`

**Device Tree** (built when attestation is ON):
- Leaf hash: `sha256(device_id || device_type || transaction_id || timestamp)`
- Root stored in `attestation.device_root`

Both trees share the same batch boundary. Verification can check either root independently.

### 4.4 Chirp Flag Codes (Device-Related)

| Code | Rule | Signal |
|------|------|--------|
| C-901 | `GHOST_DEVICE` | Transaction from unregistered device |
| C-902 | `DEVICE_LOCATION_MISMATCH` | Device transacting at wrong location |
| C-903 | `OFFLINE_BATCH_ANOMALY` | Suspicious offline batch timing/volume |
| C-904 | `DEVICE_SWAP` | Different device used mid-shift |
| C-905 | `UNAUTHORIZED_PAIRING` | Unknown peripheral paired to known POS |
| C-906 | `STALE_FIRMWARE` | Device firmware below minimum version |
| C-907 | `ORPHAN_PERIPHERAL` | Peripheral reporting without parent POS |
| C-908 | `CUSTOMER_DEVICE_VELOCITY` | Same customer device across too many locations |
| C-909 | `CAPABILITY_DOWNGRADE` | Device lost capabilities (NFC, camera, etc.) |

---

## 5. Three-Layer Resolution Architecture

### 5.1 Layer Stack

```
┌──────────────────────────────────────────────────────────┐
│  L3 — GrowDirect API (Hot Cache)                         │
│  Postgres namespace_registrations table                   │
│  Caches: GUID → merchant_id (internal ops only)           │
│  Resolution: < 1ms | Rebuildable from L1                  │
│  If offline: fall back to L2                              │
├──────────────────────────────────────────────────────────┤
│  L2 — Avalanche Subnet (Name Layer + Fast Operations)    │
│  NameRegistry smart contract                              │
│  Authoritative for: human-readable name → GUID mapping    │
│  Resolution: < 2s | Alias management | Burner minting     │
│  Owner controls: create/remove aliases, set visibility     │
│  If offline: GUID verification falls back to L1           │
│  Burners and aliases are L2-native — they die with L2     │
├──────────────────────────────────────────────────────────┤
│  L1 — Bitcoin Ordinals (Permanent Pseudonymous Truth)    │
│  Inscriptions with protocol: "jeffe"                      │
│  GUID-only namespace identifiers — no merchant identity   │
│  Resolution: minutes | Anyone with a node                 │
│  Cannot die unless Bitcoin dies                           │
│  Anonymized retail data: mine away, can't deanonymize     │
└──────────────────────────────────────────────────────────┘
```

### 5.2 Resolution Cascade

Two resolution paths: **Name Resolution** (human-readable → GUID) and **GUID Verification** (GUID → on-chain proof).

```
Name Resolution — "sunrise-coffee.jeffe" → GUID:

1. L3 (Postgres): SELECT namespace_guid FROM namespace_aliases
                   WHERE alias_name = 'sunrise-coffee.jeffe'
                   AND status = 'active'
   → Hit? Return namespace_guid. Continue to GUID verification.
   → Miss? Try L2.

2. L2 (Avalanche): NameRegistry.resolveAlias("sunrise-coffee")
   → Hit? Return namespace_guid. Done.
   → Miss? Alias does not exist.

NOTE: L1 cannot resolve human-readable names. Names do not exist on Bitcoin.
      Name resolution is L2-authoritative. L3 is a cache of L2 state.

GUID Verification — "a3f9b2c1-...jeffe" → on-chain proof:

1. L3 (Postgres): SELECT merchant_id FROM namespace_registrations
                   WHERE namespace_guid = 'a3f9b2c1-...'
                   AND status = 'active'
   → Hit? Return merchant_id. Use for internal operations.
   → Miss? Try L1.

2. L1 (Bitcoin): Scan ord index for type:"namespace",
                  namespace_guid:"a3f9b2c1-..."
   → Found? Verify chain to Genesis. Check for revocations. Return.
   → Not found? GUID does not exist.
```

### 5.3 Layer Roles

| Layer | Source of Truth? | What It Stores | What Happens If It Dies |
|-------|-----------------|----------------|------------------------|
| L1 (Bitcoin) | **YES — for GUID identity + Merkle proofs** | All inscription types (GUID-only). Full protocol history. Anonymized event anchors. | Bitcoin dies. Everything dies. |
| L2 (Avalanche) | **YES — for name→GUID mapping** | NameRegistry: alias→GUID mappings, burner lifecycle, payment gate. Owner-controlled alias visibility. | Name resolution stops. GUID verification falls back to L1. Burners and aliases expire. |
| L3 (Postgres) | No — performance cache | namespace_registrations (GUID→merchant_id), alias cache, hot indices | Resolution slows. GUID cache rebuilt from L1. Alias cache rebuilt from L2. |

### 5.4 Third-Party Resolver (Server-Independent)

Any party can build a .jeffe GUID verifier without GrowDirect involvement:

1. Run a Bitcoin full node (or connect to a trusted node)
2. Install `ord` indexer (or equivalent)
3. Filter for inscriptions matching `"protocol": "jeffe"`
4. Build local index of GUID → owner_pubkey mappings
5. Check revocations for each GUID
6. Serve GUID verification queries from local index
7. Optionally wire L402 payment gate and charge for verification

**What a third-party resolver CANNOT do:** Resolve human-readable names to GUIDs without L2 access. The anonymity wall is by design. On-chain data shows GUIDs, event counts, Merkle roots, timestamps — never merchant identity.

GrowDirect's moat: first-mover advantage, deepest index, sole registrar (through Phase 2), the fastest L3 cache, AND exclusive access to the anonymized retail dataset behind the GUID wall.

---

## 6. Namespace Rules

Per GRO-13 decisions (locked by Jeffe, March 1, 2026):

### 6.1 Six Locked Decisions

| # | Decision | Rule |
|---|----------|------|
| 1 | Reserved Names | Fortune 500 + top 100 categories pre-registered. First-come-first-served for all others. |
| 2 | Subdomain Depth | One level at launch: `store-42.walmart.jeffe`. No arbitrary depth. |
| 3 | Pricing | Annual renewal only. No perpetual ownership. 3-year prepay max. 30-day grace period. |
| 4 | Transferability | Non-transferable at launch. Transfer function exists but is admin-gated. 10% fee when enabled. |
| 5 | Registrars | GrowDirect only through Phase 2. No secondary registrars. Phase 3 DAO consideration. |
| 6 | Network | Private Avalanche subnet through Phase 2. Public C-Chain is Phase 3. |

### 6.2 Name Format

**L1 (Bitcoin) — GUID format:**
```
GUID:       ^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$
Full name:  {guid}.jeffe
```

- UUID v4 format, lowercase hex
- Generated at registration time by the registrar
- Permanently inscribed on Bitcoin. Never changes.

**L2 (Avalanche) — Alias format (human-readable names):**
```
Alias:      ^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$
Full alias: {alias}.jeffe
Subdomain:  {sublabel}.{alias}.jeffe  (one level only)
```

- Minimum 3 characters, maximum 63 characters (alias label only, excluding `.jeffe`)
- Lowercase alphanumeric and hyphens only
- Cannot start or end with a hyphen
- `xn--` prefix reserved (internationalized domain compatibility)
- Owner can create multiple aliases pointing to one GUID
- Aliases are L2-native: created, managed, and revoked on Avalanche

### 6.3 Namespace Lifecycle

**L1 GUID lifecycle:**
```
REGISTERED ──→ ACTIVE ──→ EXPIRED ──→ RELEASED
                  │          │
                  │          └── 30-day grace ──→ ACTIVE (renewed)
                  │                              or RELEASED (forfeit)
                  └── SUSPENDED (admin action) ──→ ACTIVE (resolved)
```

| Status | GUID Verifies? | Receives Merkle batches? | On-chain state |
|--------|----------------|-------------------------|----------------|
| Registered | Yes (limited) | No | Namespace inscription exists, `owner_pubkey` assigned |
| Active | Yes | Yes | Full operations |
| Expired | No (after grace) | No | Revocation inscription with `reason: "expired"` |
| Suspended | No | No | Revocation inscription with `reason: "suspended"` |
| Released | No | No | GUID available for re-registration |

**L2 Alias lifecycle (independent of L1 GUID):**

| Action | Where | Effect |
|--------|-------|--------|
| Create alias | L2 NameRegistry | New human-readable name → GUID mapping. Owner-initiated. |
| Remove alias | L2 NameRegistry | Name → GUID mapping deleted. Alias released. |
| Transfer alias | L2 NameRegistry | Alias reassigned to different GUID (if enabled, Phase 3+). |
| GUID expired | L1 Bitcoin | All L2 aliases for that GUID stop resolving. |

---

## 7. Revenue Architecture

### 7.1 Five Revenue Streams

| # | Stream | Trigger | Gate | Estimated Unit |
|---|--------|---------|------|----------------|
| 1 | **Subscription** | Canary LP merchant signs up | Stripe/traditional | $49–$299/month |
| 2 | **Validation** | External party verifies a receipt | L402 (1 sat) | ~$0.00085/call |
| 3 | **RaaS API** | POS integrator queries receipt history | L402 (1 sat/call) | ~$0.00085/call |
| 4 | **Namespace** | Merchant registers .jeffe name | BTC (annual) | TBD |
| 5 | **Burner Minting** | Merchant creates disposable endpoint | Avalanche (per-mint) | TBD |

### 7.2 Three-Tier Service Architecture

| Tier | Domain | Auth | Hash Chain | Inscription | Price |
|------|--------|------|------------|-------------|-------|
| Free | eljeffe.org | API key | Postgres hash only | None | $0 |
| Standard | eljeffe.io | L402 | Postgres + Merkle | Bitcoin Ordinal | 1 sat/verification |
| Enterprise | eljeffe.io | L402 + SLA | Postgres + Merkle + Avalanche | Bitcoin + Avalanche dual-anchor | Custom |

---

## 8. RaaS API Endpoints

### 8.1 POST /v1/verify — Verify a Receipt

Accepts `namespace_guid` (direct) or `alias` (triggers L2 lookup first).

```
POST /v1/verify
Authorization: L402 [macaroon + preimage]

Request (by GUID — direct, fastest):
{
  "event_hash": "sha256:a3f9...",
  "namespace_guid": "a3f9b2c1-7d4e-4f8a-9c6b-2e1d0f3a5b7c",
  "include_device": false
}

Request (by alias — triggers L2 name resolution first):
{
  "event_hash": "sha256:a3f9...",
  "alias": "sunrise-coffee",
  "include_device": false
}

Flow:
→ If alias provided: L2 NameRegistry.resolveAlias → namespace_guid
→ 402 Payment Required (Lightning invoice: 1 sat)
→ Client pays invoice
→ 200 OK

Response:
{
  "verified": true,
  "block": 884201,
  "merkle_position": 4721,
  "inscription_id": "i39f7a...",
  "namespace_guid": "a3f9b2c1-7d4e-4f8a-9c6b-2e1d0f3a5b7c",
  "canonical_authority": "eljeffe.io",
  "device_attestation": null
}
```

**Note:** Response never returns the alias or human-readable name. GUID only. The caller already knows the alias (they provided it). Third parties verifying by GUID alone cannot determine merchant identity.

### 8.2 GET /v1/receipt/{namespace_guid} — Receipt History

```
GET /v1/receipt/a3f9b2c1-7d4e-4f8a-9c6b-2e1d0f3a5b7c?range=2026-03-01&limit=100
Authorization: L402 [macaroon + preimage]

Response:
{
  "namespace_guid": "a3f9b2c1-7d4e-4f8a-9c6b-2e1d0f3a5b7c",
  "receipts": [
    {
      "event_hash": "sha256:a3f9...",
      "timestamp": "2026-03-01T14:32:15Z",
      "verified": true,
      "inscription_id": "i39f7a...",
      "merkle_proof": ["sha256:b2c4...", "sha256:d8e1..."]
    }
  ],
  "total": 187,
  "anchor_block": 884201,
  "pagination": {
    "cursor": "eyJ0IjoiMjAyNi0wMy0wMVQxNDozMjoxNVoifQ==",
    "has_more": true
  }
}
```

**Alias convenience route:** `GET /v1/receipt/sunrise-coffee` triggers L2 alias lookup → GUID → same response. Alias is not echoed in the response.

### 8.3 GET /v1/resolve/{identifier} — Namespace Resolution (Public)

Two modes: resolve an alias (human-readable → GUID), or look up a GUID directly.

```
GET /v1/resolve/sunrise-coffee  (alias mode — hits L2)

Response:
{
  "alias": "sunrise-coffee.jeffe",
  "namespace_guid": "a3f9b2c1-7d4e-4f8a-9c6b-2e1d0f3a5b7c",
  "registered": true,
  "tier": "standard",
  "receipt_count": 12847,
  "last_receipt": "2026-03-01T14:32:15Z",
  "inscription_id": "<Bitcoin inscription ID>"
}

GET /v1/resolve/a3f9b2c1-7d4e-4f8a-9c6b-2e1d0f3a5b7c  (GUID mode — hits L1/L3)

Response:
{
  "namespace_guid": "a3f9b2c1-7d4e-4f8a-9c6b-2e1d0f3a5b7c",
  "registered": true,
  "tier": "standard",
  "receipt_count": 12847,
  "last_receipt": "2026-03-01T14:32:15Z",
  "inscription_id": "<Bitcoin inscription ID>"
}
```

No L402 gate. Public resolution. Drives traffic to paid verification endpoints. Note: GUID resolution returns activity stats but never merchant identity. Alias resolution confirms the alias→GUID mapping exists.

### 8.4 API Standards

- All endpoints use `/v1/` prefix. Breaking changes get `/v2/`.
- No sunset without 6-month notice.
- Rate limiting: 1,000 req/min per API key. Burst: 100 req/10sec.
- Pagination required for >100 results.
- OpenAPI/Swagger spec published at `/v1/docs`.

---

## 9. Data Model Integration (CRDM v1.1)

### 9.1 Key Tables

| Table | Schema | Role in Protocol |
|-------|--------|-----------------|
| `namespace_registrations` | `canary_app` | L3 cache: .jeffe GUID → merchant_id UUID resolution |
| `external_identities` | `canary_app` | POS-agnostic entity mapping (any source → canonical ID) |
| `source_systems` | `canary_app` | Reference table for source system codes (POS, EHR, IoT, etc.) |
| `evidence_records` | `canary_sales` | Sub 1 sealed event hashes |
| `merkle_batches` | `canary_sales` | Sub 3 Merkle tree roots + inscription references |
| `devices` | `canary_app` | Device registry (GRO-45 Amendment 8) |
| `transaction_devices` | `canary_app` | Many-to-many: transaction ↔ device linkage |

### 9.2 External Identity Resolution (POS → Canonical)

```
Clover payment_id → external_identities (source='clover') → canonical transaction_id
Toast order_id    → external_identities (source='toast')  → canonical transaction_id
Square payment_id → external_identities (source='square') → canonical transaction_id
```

Per CRDM v1.1 Amendment 1: the `external_identities` table replaces all `square_*_id` columns. Adding a new POS is an INSERT into `source_systems` + a new parser, not a schema change.

### 9.3 Namespace Resolution (GUID → Merchant)

```
GUID Resolution (direct):
"a3f9b2c1-...jeffe" → namespace_registrations → merchant_id (UUID)
                                                → evidence_records → merkle_batches
                                                → inscription proof

Name Resolution (via L2):
"sunrise-coffee.jeffe" → L2 NameRegistry → namespace_guid
                                          → namespace_registrations → merchant_id
```

The `namespace_registrations` table is a GUID→merchant_id cache. Source of truth for GUIDs is the Bitcoin inscription. Source of truth for alias→GUID mapping is L2 (Avalanche NameRegistry).

---

## 10. Pipeline Integration (TSP)

### 10.1 Event Flow

```
POS Webhook (any source)
  │
  ▼
API Gateway (L402 / JWT / HMAC)
  │
  ▼
canary:events (Valkey Stream — TSP-01 v1.1)
  │
  ├─→ Sub 1: SEAL (hash the event, store in evidence_records)
  ├─→ Sub 2: PARSE (route to vendor-specific parser, output canonical CRDM)
  └─→ Sub 3: MERKLE (batch events into tree, inscribe root on Bitcoin)
                │
                ├─→ Event Merkle Tree → merkle_root → Ordinal inscription
                └─→ Device Merkle Tree (optional) → device_root → attestation block
```

### 10.2 Inscription Trigger

Sub 3 inscribes a Merkle batch when:
- Batch reaches configurable event count threshold (default: 100), OR
- Batch age exceeds configurable time limit (default: 1 hour), OR
- Manual flush is triggered (admin/debug)

Whichever condition fires first triggers the inscription.

---

## 11. Security Model

### 11.1 Trust Chain

```
Genesis inscription (root_authority pubkey)
  └── Registrar signature (registered_by pubkey — must chain to root_authority)
        └── Namespace inscription (owner_pubkey — merchant's key)
              └── Merkle batch inscriptions (chained via chain.previous)
```

Any party can verify the full trust chain by:
1. Finding the Genesis inscription (type: "genesis", chain.previous: null)
2. Extracting `root_authority`
3. For any namespace: verifying `registered_by` chains to `root_authority`
4. For any Merkle batch: verifying `chain.previous` links back through the namespace's chain

### 11.2 Threat Model

| Threat | Mitigation |
|--------|-----------|
| Forged inscription | Requires registrar key (root_authority chain). Attacker cannot forge without private key. |
| Merkle proof tampering | SHA-256 collision resistance. Altering any leaf changes the root. On-chain root is immutable. |
| Namespace squatting | Reserved names (Decision 1). Annual renewal (Decision 3). Non-transferable (Decision 4). |
| Replay attack | `chain.sequence` is monotonically increasing. Duplicate sequence numbers are invalid. |
| Server compromise | L3 (Postgres) is a cache. L2 (Avalanche) is operational. L1 (Bitcoin) is immutable. Compromise L3 and L2 — L1 is still correct. |
| GrowDirect disappears | Protocol is self-describing on L1. Any party can rebuild resolver from Bitcoin data. |

---

## 12. Open Questions

### Blocking (Must resolve before Genesis inscription)

| # | Question | Owner | Context |
|---|----------|-------|---------|
| Q-1 | What is the exact Genesis inscription payload? | Tom | This is permanent — one shot. Every field must be validated. |
| Q-2 | Key management: how is the treasury private key stored? | Tom + Jeffe | Paper only per Wax Seal capture. Need formal key ceremony process. |
| Q-3 | Bitcoin testnet vs. mainnet for Phase 0? | Tom + Jeffe | Testnet for dev, mainnet for Genesis. When do we cross? |
| Q-4 | `ord` vs. hosted inscription service for Phase 0? | Jeremy | Self-hosted = sovereignty. Hosted = speed. Recommendation: hosted for PoC, self-hosted for production. |

### Non-Blocking (Resolve during implementation)

| # | Question | Owner | Context |
|---|----------|-------|---------|
| Q-5 | Merkle batch size optimization | Tom | Default 100 events / 1 hour. Needs load testing to optimize. |
| Q-6 | Avalanche subnet validator requirements | Tom | How many validators? GrowDirect-only or trusted partners? |
| Q-7 | L402 middleware implementation | Tom + Jeremy | LND REST? CLN? Voltage LSP? Minimum viable gate. |
| Q-8 | Configurable anti-spam floor per namespace | Tom | 1 sat default. Owner-configurable? Per GRO-46 open question. |

### Legal (Syd)

| # | Question | Source |
|---|----------|--------|
| L-1 through L-6 | RaaS legal questions | GRO-13 Section 4 |
| N-1 through N-6 | Namespace decision legal questions | GRO-13 Section 4 |
| S-1 through S-4 | Sovereignty legal questions | GRO-46 Sovereign Architecture Section 10 |
| S-5 | Device attestation OFF liability | Alignment Amendment B |

### Patent (PhD)

| # | Claim | Source |
|---|-------|--------|
| P-1 | Serializable gate: portable, non-consumable, context-agnostic identity on Bitcoin Ordinal | GRO-46 |
| P-2 | Self-describing protocol inscription | Sovereign Architecture |
| P-3 | Three-layer degradation-tolerant resolution | Sovereign Architecture |
| P-4 | On-chain revocation for off-chain state | Sovereign Architecture |

---

## 13. Phased Delivery

| Phase | Timeline | What Ships | Dependencies |
|-------|----------|------------|-------------|
| 0: Foundation | Week 1–2 | Genesis inscription, wallet, tools, namespace record format | Q-1 through Q-4 resolved |
| 1: Pipeline | Week 2–4 | Square sandbox webhook → Merkle batch → Ordinal inscription. L1-only verification round-trip. | Phase 0 complete |
| 2: Avalanche | Week 4–8 | Private subnet, NameRegistry contract, first burner mint | Phase 1 proven |
| 3: End-to-End | Week 6–10 | Full loop + L402 payment gate. All three resolution layers operational. | Phase 2 operational |
| 4: First Merchant | Week 10–16 | One real Square merchant, live webhooks, real inscriptions | Phase 3 QA'd by Jim |
| 5: Multi-POS | Week 16–28 | Second POS connected (Clover or Toast) via polling adapter + external_identities | Phase 4 stable |
| 6: Culture | Week 28–40 | "You got jeffe'd" in the wild. In the culture by Christmas '26. | Phase 5 running |

---

## 14. Document Lineage

This spec synthesizes and supersedes the following work orders:

| Document | What It Contributed | Status |
|----------|-------------------|--------|
| `GRO-46_Sovereign_Namespace_Architecture.md` | Three-layer resolution, self-describing Genesis, revocation type | Absorbed into Sections 3, 5 |
| `GRO-13_RaaS_Strategic_Reframe_Namespace_Decisions.md` | RaaS API, 6 namespace decisions, revenue model, legal questions | Absorbed into Sections 6, 7, 8 |
| `CRDM_v1.1_Amendment_POS_Agnostic_Entity_Model.md` | external_identities, device graph, POS-agnostic schema | Referenced in Section 9 |
| `CRDM_v1.1_Alignment_Amendment_Namespace_Bridge_Device_Attestation.md` | namespace_registrations, device attestation, source_systems | Absorbed into Sections 4, 9 |
| `Jeffe_NamespaceIdentityPrimitive_2026-03-02.md` | Serializable gate, three identity layers, "you got jeffe'd" | Absorbed into Section 2 |
| `Jeffe_ModernWaxSeal_ExecutionDirective_2026-03-02.md` | Execution plan, inscription payloads, architecture diagram, timeline | Absorbed into Sections 3, 10, 13 |

---

*elJeffe Protocol Specification v1.0 | March 2, 2026*
*MAXIMUM CONFIDENTIAL*
*Tom validates. Syd clears. PhD reviews patent claims. Jim QA's test plan.*
