# TSP Sub 3 -- Merkle Batcher & Ordinal Minter

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]
**Architecture:** [[docs/sdds/canary/architecture|Canary Architecture SDD]]
**Method:** [[Brain/projects/Method|Method MOC]]
**Author role:** [[docs/team/Architect|Architect]] · **Operator role:** [[docs/team/Engineer|Engineer]]

> **Type:** App Service (Canary) -- Stream Consumer
> **Parent SDD:** [[docs/sdds/canary/tsp|TSP Pipeline Overview]]
> **Status:** Production Readiness Review -- 2026-04-13
> **Code location:** `Canary/canary/services/tsp/consumers/sub3_merkle.py`, `Canary/canary/services/tsp/merkle.py`
> **Patent:** FIG. 1 Nodes 5/6

---

## Purpose

Sub 3 is the Merkle tree batcher and (future) Bitcoin inscription submitter. It accumulates event hashes from the `canary:events` stream into batches, constructs deterministic Merkle trees from the accumulated hashes, writes the tree root and per-event proofs to PostgreSQL, and (in Sprint 6) generates mock Bitcoin inscription data. Real OrdinalsBot API integration requires spend gate approval and is deferred to Sprint 7+.

The Merkle tree construction algorithm is confidential (patent-covered). Each event's inclusion in a batch can be independently verified using only the event hash, the proof path, and the Merkle root -- no network access required.

## Dependencies

| Dependency | Role | Required |
|------------|------|----------|
| Valkey DB 4 | Reads from `canary:events`, uses sorted set `canary:batch:current` as accumulator | Yes |
| PostgreSQL (`canary` DB, `canary_sales` schema) | Writes to `inscription_pool` and `event_inscriptions` | Yes |
| `merkle.build_tree()` | Deterministic Merkle tree construction (algorithm v1) | Yes |
| ULID library | Generates `batch_id` for each Merkle batch | Yes |

---

## Data Flow & PII Map

### What Enters

9-field queue message from `canary:events`. Sub 3 uses only:
- `event_hash` (hex SHA-256) -- the leaf input for the Merkle tree
- `event_id` (ULID) -- maps events to their batch
- `merchant_id` -- stored in `event_inscriptions` for per-merchant queries

### What's Stored

**`inscription_pool`** table (one row per batch):

| Field | Classification | Encryption | Notes |
|-------|---------------|------------|-------|
| `batch_id` | public | N/A | ULID batch identifier |
| `merkle_root` | public | N/A | SHA-256 root (32 bytes BYTEA) |
| `batch_event_count` | public | N/A | Original event count before padding |
| `padded_leaf_count` | public | N/A | After power-of-2 padding |
| `tree_depth` | public | N/A | Balanced tree depth |
| `inscription_id` | public | N/A | OrdinalsBot ID (mock in Sprint 6) |
| `bitcoin_txid` | public | N/A | Bitcoin TX hash (mock) |
| `bitcoin_block` | public | N/A | Block number (mock) |
| `fee_sats` | public | N/A | Inscription fee (mock: 2500 sats) |
| `status` | public | N/A | pending / tree_built / submitted / confirmed / verified |

**`event_inscriptions`** table (one row per event per batch):

| Field | Classification | Encryption | Notes |
|-------|---------------|------------|-------|
| `event_hash` | public | N/A | SHA-256 of the event (BYTEA, unique) |
| `event_id` | public | N/A | ULID from pipeline |
| `merchant_id` | internal | NONE | Tenant key |
| `batch_id` | public | N/A | References inscription_pool |
| `leaf_index` | public | N/A | Position in sorted leaf array |
| `merkle_proof_path` | public | N/A | JSONB: {siblings, root, leaf_hash, tree_depth} |

**No PII in Sub 3 storage.** Sub 3 operates exclusively on event hashes (derived, non-reversible) and identifiers. The raw payloads from the stream message are not read or stored by Sub 3.

### What Exits

Nothing downstream. Sub 3 is a terminal writer. Inscription data is queried by receipt endpoints and the `verify_merkle` MCP tool.

---

## API Contract

Sub 3 exposes no HTTP endpoints. It is a Valkey stream consumer only.

**Consumer Group:** `sub3-merkle`
**Stream:** `canary:events` (Valkey DB 4)
**Block Timeout:** `SUB3_BLOCK_MS` (default 2000ms -- shorter than Sub 1/2 for faster threshold checks)

### Batch Thresholds

| Trigger | Default | Env Var |
|---------|---------|---------|
| Count threshold | 100 events | `BATCH_COUNT_THRESHOLD` |
| Time threshold | 600 seconds (10 min) | `BATCH_TIME_THRESHOLD_SECONDS` |

Whichever threshold is reached first triggers a batch flush.

---

## Operations

### Processing Sequence

**Accumulation phase (per message):**
1. `XREADGROUP sub3-merkle` reads one message from `canary:events`
2. Extract `event_hash`, `event_id`, `merchant_id`. Malformed -> ACK and skip.
3. Add to Valkey sorted set accumulator (`canary:batch:current`, scored by timestamp, member = `hash:id:merchant`)
4. Track message ID in `pending_msg_ids` list. DO NOT XACK during accumulation.
5. Check thresholds: count >= `BATCH_COUNT_THRESHOLD` OR elapsed >= `BATCH_TIME_THRESHOLD_SECONDS`

**Flush phase (on threshold):**
6. Read all entries from accumulator sorted set
7. Parse entries, extract event hashes as bytes
8. Build Merkle tree: sort hex-ascending, pad to next power of 2 (duplicate-last-leaf), construct tree
9. Generate `batch_id` (ULID)
10. BEGIN PostgreSQL transaction
11. INSERT `inscription_pool` row (status = `tree_built`)
12. INSERT `event_inscriptions` row for each event with proof path
13. COMMIT
14. XACK all accumulated message IDs in bulk
15. DELETE accumulator sorted set
16. Mock inscription update (Sprint 6): UPDATE `inscription_pool` with deterministic fake Bitcoin data

### Startup Sequence

1. Consumer app created via `create_consumer_app()`
2. Database session factory initialized
3. Consumer group created defensively
4. **Orphaned accumulator check:** If `canary:batch:current` has entries from a previous crash, delete it. Messages will be redelivered from PEL.
5. Blocking loop begins

### Health Checks

- Valkey heartbeat: `canary:heartbeat:sub3` (TTL 120s)
- Docker healthcheck: `devops/scripts/tsp_healthcheck.py` (15s interval)

### Failure Modes

| Failure | Behavior | Recovery |
|---------|----------|----------|
| Malformed message (no hash/id) | ACK and skip | Normal -- poison message cleared |
| Merkle tree construction failure | Log error, do NOT ACK batch | Messages stay in PEL, redelivered on restart |
| PostgreSQL commit failure | Rollback, do NOT ACK | Messages redelivered. Accumulator is stale but will be cleared on restart. |
| Duplicate events in batch | Partial commit with unique constraint warning | Logged; non-duplicate events committed |
| Shutdown with unACK'd messages | Warning logged | Messages remain in PEL, redelivered on restart. Orphaned accumulator cleared. |
| 10 consecutive errors | Consumer stops | Docker restart |

### XACK Timing (Key Design Decision)

Messages are NOT ACK'd during the accumulation window (up to 10 minutes). All accumulating messages appear in the Pending Entry List (PEL). This means:
- `get_stream_health` MCP tool will show high pending counts for Sub 3 -- this is normal
- If Sub 3 crashes mid-batch, all accumulated messages are redelivered from PEL
- The orphaned accumulator check on startup prevents stale batch state

---

## Deployment

### Docker Service

```yaml
tsp-sub3:
  image: canary-flask
  container_name: canary_localhost_tsp_sub3
  command: python -m canary.services.tsp.run_consumer --consumer sub3
  healthcheck:
    test: ["CMD", "python", "devops/scripts/tsp_healthcheck.py"]
    interval: 15s
  depends_on:
    flask: { condition: service_healthy }
  restart: unless-stopped
```

### AWS Target

- ECS Fargate task (1 task -- single batcher per deployment)
- Memory: 256 MB (tree construction is in-memory but bounded by batch size)
- CPU: 0.25 vCPU (hash computation is fast)

---

## Merkle Tree Algorithm (v1)

- **Leaf ordering:** Sorted by `event_hash` hex string ascending (deterministic -- same inputs always produce same tree)
- **Padding:** Duplicate-last-leaf to next power of 2
- **Leaf hashing:** `SHA-256(event_hash)` -- double-hashing prevents second-preimage attacks
- **Internal nodes:** `SHA-256(left_child || right_child)`
- **Proof path:** Array of sibling hashes from leaf to root, sufficient for independent verification
- **Verification:** `verify_proof(event_hash, proof, expected_root)` recomputes root from proof path

---

## Code Review Findings

### P0 -- Blocks Production

| # | Finding | Recommended Fix |
|---|---------|-----------------|
| P0-S3-01 | **Mock inscription is the default.** `MOCK_INSCRIPTION=true` means no real Bitcoin notarization. Production requires live OrdinalsBot API keys (spend gate pending). The mock generates deterministic fake `bitcoin_txid` and `bitcoin_block` values that could be confused with real data. | Gate on `CANARY_ENV`: refuse to start in production with `MOCK_INSCRIPTION=true`. Add clear `[MOCK]` prefix to mock data. |

### P1 -- Before GA

| # | Finding | Recommended Fix |
|---|---------|-----------------|
| P1-S3-01 | **Accumulator not persisted across restarts.** The `canary:batch:current` sorted set is deleted on startup if orphaned. Messages are redelivered from PEL, but any ordering/timing metadata from the accumulator is lost. | Acceptable for correctness (PEL redelivery works). Document that batch boundaries may shift on restart. |
| P1-S3-02 | **`leaf_index` computed by re-sorting inside flush loop.** `sorted_hashes.index(hash_hex)` is O(n) per event, making the total O(n^2). For batch size 100, negligible. For larger batches, could be slow. | Pre-compute a hash->index mapping before the event loop. |
| P1-S3-03 | **No monitoring for batch flush frequency.** No metric or log aggregation for how often batches flush and by which threshold. | Add structured log or metric for flush events with trigger reason, batch size, and elapsed time. |

### P2 -- Post-Launch

| # | Finding | Recommended Fix |
|---|---------|-----------------|
| P2-S3-01 | **OrdinalsBot integration not implemented.** Real inscription requires: API key management, fee estimation, submission retry logic, confirmation polling, spend gate enforcement. | Complete when spend gate approved (Sprint 7+). This is the business decision, not a code gap. |
| P2-S3-02 | **Single batcher -- no horizontal scaling.** Only one Sub 3 instance can run because the accumulator sorted set is a shared resource. | If throughput requires scaling, shard by merchant_id (each shard has its own accumulator). |
| P2-S3-03 | **Accumulator entry format is colon-delimited string.** `event_hash_hex:event_id:merchant_id` -- if any field contains a colon, parsing breaks. | Use a separator that cannot appear in hex strings or ULIDs (e.g., `|`), or use a structured format. |

---

## Production Readiness Checklist

- [x] No PII stored by Sub 3 (operates on hashes only)
- [ ] Mock inscription gated by environment (P0-S3-01)
- [ ] Secrets in AWS Secrets Manager (OrdinalsBot API key, when available)
- [x] Health check functional (Valkey heartbeat + Docker healthcheck)
- [ ] Batch flush monitoring (P1-S3-03)
- [x] Error handling with exponential backoff
- [x] Orphaned accumulator recovery on startup
- [x] PEL-based message redelivery on crash
- [x] Merkle proof verification function (`verify_proof`)
