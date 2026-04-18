---
type: spec
domain: canary
status: active
created: 2026-03-14
updated: 2026-03-19
---
# Design Spec — Inscription Pipeline v1.0

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]

**Version:** 1.0
**Date:** March 2, 2026
**Author:** ALX (Chief of Staff)
**Classification:** MAXIMUM CONFIDENTIAL
**Protocol Reference:** `elJeffe_Protocol_Spec_v1.0.md` (Sections 3.4, 4, 10)
**Source Issues:** GRO-47, GRO-45 (Amendment 8), GRO-58 (GUID Namespace)
**Routes To:** Jeremy (implementation), Tom (Merkle validation), Jim (QA)
**Gate:** Tom validates Merkle tree design. Jim QA's round-trip verification.

---

## 1. Purpose

This spec defines how commercial events flow from POS webhook through the TSP pipeline to Bitcoin Ordinal inscription. It is the build document for GRO-47 Phases 0–3: wallet setup, Merkle batching in Sub 3, `ord` inscription, and verification round-trip.

---

## 2. Pipeline Architecture

```
POS Webhook (Square sandbox → production → any POS)
  │
  ▼
API Gateway (HMAC / JWT / L402)
  │
  ▼
canary:events (Valkey Stream — TSP-01 v1.1)
  │
  ├─→ Sub 1: SEAL
  │     Hash the raw event. Store in evidence_records.
  │     Output: event_id, event_hash, sealed_at
  │
  ├─→ Sub 2: PARSE
  │     Route to vendor-specific parser.
  │     Output: canonical CRDM records via external_identities.
  │
  └─→ Sub 3: MERKLE + INSCRIBE  ← THIS SPEC
        Batch sealed events into Merkle tree.
        Optionally build device Merkle tree.
        Inscribe root(s) on Bitcoin as Ordinal.
        Store inscription reference in merkle_batches table.
```

---

## 3. Sub 3: Merkle Batch + Inscription

### 3.1 Batch Accumulation

Sub 3 maintains an in-memory batch buffer. Events from Sub 1 are added to the buffer as they arrive.

**Batch triggers (whichever fires first):**

| Trigger | Default | Configurable |
|---------|---------|-------------|
| Event count | 100 events | Yes (env: `MERKLE_BATCH_SIZE`) |
| Time limit | 1 hour | Yes (env: `MERKLE_BATCH_INTERVAL_SEC`) |
| Manual flush | N/A | Admin endpoint: `POST /admin/merkle/flush` |

When a trigger fires:
1. Lock the buffer (no new events accepted until inscription completes or times out)
2. Build Event Merkle Tree
3. If `device_attestation = on` for the namespace: build Device Merkle Tree
4. Construct inscription payload
5. Submit inscription to Bitcoin (via `ord` CLI or API)
6. On confirmation: store inscription reference in `merkle_batches` table
7. Unlock the buffer for next batch

### 3.2 Event Merkle Tree Construction

**Input:** Array of sealed events from the batch buffer.

**Leaf computation:**
```
leaf_hash = sha256(event_id || event_hash || timestamp)
```

Where:
- `event_id`: UUID from `evidence_records.id`
- `event_hash`: SHA-256 hash from Sub 1 sealing
- `timestamp`: ISO-8601 string of `evidence_records.sealed_at`
- `||` denotes byte concatenation (UTF-8 encoded strings, no separator)

**Tree construction:**
- Binary Merkle tree (each node has 0 or 2 children)
- If leaf count is not a power of 2, duplicate the last leaf to fill the level
- Internal node: `sha256(left_child || right_child)`
- Root: the single remaining hash after all levels are computed

**Output:**
- `merkle_root`: the root hash
- `tree_depth`: number of levels (log2 of event count, rounded up)
- `event_count`: number of unique events in the batch (not including padding duplicates)

### 3.3 Device Merkle Tree Construction (Optional)

**Prerequisite:** `device_attestation = on` for the namespace (feature flag in `merchant_feature_flags` table).

**Input:** Array of `transaction_devices` rows linked to events in the batch.

**Leaf computation:**
```
leaf_hash = sha256(device_id || device_type || transaction_id || timestamp)
```

Where:
- `device_id`: UUID from `devices.id`
- `device_type`: string from `devices.device_type` (e.g., `pos_terminal`, `peripheral`, `customer_device`)
- `transaction_id`: UUID of the linked transaction
- `timestamp`: ISO-8601 string of `transaction_devices.recorded_at`

**Tree construction:** Same algorithm as Event Merkle Tree.

**Chirp flag collection:**
- Query `chirp_alerts` for any device-related rules (C-901 through C-909) triggered by events in this batch
- Collect unique rule codes into `flags` array
- If no device Chirp rules fired: `flags: []`

**Output:**
- `device_root`: the root hash of the device tree
- `device_count`: number of unique devices in the batch
- `flags`: array of Chirp rule codes (may be empty)

### 3.4 Inscription Payload Assembly

```json
{
  "protocol": "jeffe",
  "version": "1.1",
  "type": "merkle_batch",
  "namespace_guid": "<UUID from namespace_registrations.namespace_guid>",
  "batch_id": "<uuid, generated>",
  "merkle_root": "<from 3.2>",
  "event_count": "<from 3.2>",
  "time_range": {
    "first": "<earliest event timestamp in batch>",
    "last": "<latest event timestamp in batch>"
  },
  "proof_data": {
    "tree_depth": "<from 3.2>",
    "algorithm": "sha256",
    "leaf_format": "sha256(event_id || event_hash || timestamp)"
  },
  "attestation": "<from 3.3, or null if device_attestation = off>",
  "chain": {
    "previous": "<inscription_id of prior batch for this namespace_guid>",
    "sequence": "<prior sequence + 1>"
  }
}
```

### 3.5 Bitcoin Inscription

**Tool:** `ord` CLI (self-hosted for production, hosted service acceptable for Phase 0 PoC).

**Command:**
```bash
ord wallet inscribe \
  --file /tmp/batch_{batch_id}.json \
  --fee-rate ${FEE_RATE_SATS_PER_VBYTE} \
  --destination ${TREASURY_ADDRESS}
```

**Environment variables:**
- `ORD_WALLET`: wallet name (default: `jeffe-treasury`)
- `FEE_RATE_SATS_PER_VBYTE`: inscription fee rate (default: 10)
- `BITCOIN_NETWORK`: `testnet` (Phase 0–1) or `mainnet` (Phase 4+)
- `ORD_RPC_URL`: Bitcoin node RPC endpoint

**On success:** `ord` returns `inscription_id` and `txid`. Wait for 1 confirmation (next block, ~10 min).

**On failure:** Log error, retry with higher fee rate (2× backoff, max 3 retries). If all retries fail, alert operations and hold the batch in buffer (do not discard events).

### 3.6 Post-Inscription Storage

After confirmation, write to `merkle_batches` table:

```sql
INSERT INTO canary_sales.merkle_batches (
    id, merchant_id, namespace_guid, batch_id,
    merkle_root, event_count, tree_depth,
    time_range_first, time_range_last,
    inscription_id, inscription_txid, block_height, confirmed_at,
    device_attestation_enabled, device_root, device_count, device_flags,
    chain_previous, chain_sequence,
    created_at
) VALUES (...);

-- Stamp batch_id on all events included in this batch
UPDATE canary_sales.evidence_records
SET batch_id = <batch_uuid>
WHERE id IN (<list of event_ids in this batch>);
```

**Note:** The `merkle_batches` table DDL is defined in the CRDM v1.1 Addendum. If the table doesn't exist yet, this spec requires it.

---

## 4. Verification Round-Trip

This is the critical proof: given an event_hash, reconstruct the Merkle proof and verify it matches the on-chain inscription.

### 4.1 Verification Flow

```
Input: event_hash, namespace_guid (or alias — resolved via L2 → GUID first)

1. Resolve namespace_guid → merchant_id (via namespace_registrations L3 cache)
   If caller provides an alias instead, resolve alias → GUID via L2 (Avalanche NameRegistry)
   or namespace_aliases L3 cache before proceeding.
2. Find the event in evidence_records:
   SELECT id, event_hash, sealed_at
   FROM evidence_records
   WHERE merchant_id = ? AND event_hash = ?

3. Find the batch containing this event (direct join via batch_id — Tom Review T-2):
   SELECT mb.* FROM merkle_batches mb
   JOIN evidence_records er ON er.batch_id = mb.batch_id
   WHERE er.event_hash = ? AND er.merchant_id = ?

   NOTE: Time-range index is retained for dashboard queries, but verification
   MUST use the batch_id join to avoid boundary gap/overlap issues.

4. Reconstruct the Merkle proof:
   a. Recompute leaf_hash = sha256(event_id || event_hash || timestamp)
   b. Determine leaf position in the tree
   c. Collect sibling hashes up to the root
   d. Verify reconstructed root == merkle_batches.merkle_root

5. Verify on-chain:
   a. Fetch inscription content from Bitcoin (via ord indexer or API)
   b. Parse inscription JSON
   c. Compare merkle_root in inscription to merkle_batches.merkle_root
   d. If match: verified. Return block_height + inscription_id.

Output:
{
  "verified": true,
  "block": <block_height>,
  "inscription_id": "<inscription_id>",
  "merkle_position": <leaf index in tree>,
  "namespace_guid": "<uuid>.jeffe"
}
```

### 4.2 L1-Only Verification (Sovereignty Proof)

Per Jeffe's directive, the system MUST be able to verify using ONLY Bitcoin data — no Postgres, no Avalanche.

**L1-only flow:**
1. Scan Bitcoin for `type: "merkle_batch"` inscriptions matching the `namespace_guid`
2. For each batch inscription: use `proof_data` to determine tree structure
3. The verifier must have the full list of event hashes for the batch (either provided by the requester or obtained from another source)
4. Reconstruct the tree and check if the target event_hash is a valid leaf
5. Verify the reconstructed root matches the on-chain `merkle_root`

**Limitation:** L1-only verification requires the verifier to have the event hash list for the batch. In normal operation (L3), this comes from `evidence_records`. In L1-only mode, the requester must provide sufficient context.

---

## 5. Wallet and Treasury Management

### 5.1 Wallet Setup (Phase 0)

| Item | Specification |
|------|--------------|
| Wallet software | Sparrow Wallet (GUI) or Bitcoin Core + `ord` (CLI) |
| Wallet name | `jeffe-treasury` |
| Network | Testnet (Phase 0–3), Mainnet (Phase 4+) |
| Initial funding | 0.001 BTC (testnet), 0.01 BTC (mainnet — covers ~100 inscriptions at 10 sat/vbyte) |
| Key backup | Paper-only. Two keyholders: Jeffe + one other. Never digital. |
| Key ceremony | Formal process — air-gapped machine, witnessed generation, sealed backup. Tom to design. |

### 5.2 Fee Management

| Payload size | Estimated cost (10 sat/vbyte) | Notes |
|-------------|------------------------------|-------|
| ~300 bytes (no attestation) | $0.50–$2.00 | Typical batch |
| ~400 bytes (with attestation, no flags) | $0.75–$2.50 | Device integrity ON |
| ~450 bytes (with attestation + flags) | $0.85–$3.00 | Device anomalies recorded |
| ~500 bytes (Genesis inscription) | $1.00–$3.50 | One-time |

**Fee monitoring:** Track mempool fee rates. If fees spike above 50 sat/vbyte, hold batches and alert operations. Resume when fees normalize. Never overpay for non-urgent inscriptions.

---

## 6. Error Handling

| Scenario | Behavior |
|----------|----------|
| Bitcoin node unreachable | Retry 3× with exponential backoff. Hold batch in buffer. Alert operations. |
| Inscription rejected by mempool | Check fee rate. Retry with 2× fee. If rejected 3×, alert + hold. |
| Inscription unconfirmed after 1 hour | Check mempool status. If dropped, re-submit with higher fee. |
| Wallet balance insufficient | Alert operations immediately. Do not attempt inscription. Hold all batches. |
| Merkle tree construction fails | Log error with full event list. Do not inscribe. Hold batch for manual review. |
| `chain.previous` cannot be determined | Query `merkle_batches` for latest inscription_id for this `namespace_guid`. If table empty and this is the first batch, use the namespace inscription_id as previous. |

---

## 7. Testing Strategy

### Phase 0 Tests
- [ ] Genesis inscription on testnet — verify content matches spec exactly
- [ ] Namespace inscription on testnet — verify chain links to Genesis
- [ ] Read back inscription via `ord` — verify JSON parses correctly

### Phase 1 Tests
- [ ] Square sandbox webhook → Sub 1 seal → Sub 3 Merkle batch → inscription
- [ ] Verify round-trip: take any event from the batch, reconstruct Merkle proof, match on-chain root
- [ ] L1-only verification: verify using ONLY Bitcoin data (no Postgres)
- [ ] Batch trigger: event count (verify batch fires at 100 events)
- [ ] Batch trigger: time limit (verify batch fires at 1 hour)
- [ ] Manual flush (verify admin endpoint triggers immediate batch)

### Phase 2 Tests (Device Attestation)
- [ ] Device attestation ON: verify `attestation` block in inscription
- [ ] Device attestation OFF: verify `attestation` is null/omitted
- [ ] Chirp flags: trigger C-901 (ghost device), verify flag appears in inscription
- [ ] Parallel tree independence: verify event tree and device tree can be checked separately

### Failure Mode Tests
- [ ] Bitcoin node down: verify batch is held, not discarded
- [ ] Fee spike: verify batch holds until fees normalize
- [ ] Wallet empty: verify alert fires, no inscription attempted
- [ ] Duplicate event in batch: verify deduplication before tree construction

---

*Design Spec — Inscription Pipeline v1.0 | March 2, 2026*
*MAXIMUM CONFIDENTIAL*
