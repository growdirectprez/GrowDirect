---
type: spec
domain: protocol
status: active
created: 2026-03-18
updated: 2026-03-19
---
# PRD: Sub 3 — Ordinal Minter
**Version:** 1.0
**Owner:** Jeremy
**Depends on:** Message queue, Bitcoin RPC node, Ordinals API, cryptographic key management, Merkle tree library
**Gates:** Permanent notarization, Validation API revenue model, blockchain immutability
**Sprint target:** Sprint 6

---

## Purpose

Sub 3 is the third queue subscriber. It batches recent event hashes from the queue, builds a Merkle tree rooted at all hashes, inscribes the Merkle root as a Bitcoin Ordinal, and maps every event to its tree position. Events are sealed twice: once in Sub 1 (database immutability) and once in Sub 3 (Bitcoin permanence). Sub 3 is asynchronous and never blocks Sub 1 or Sub 2.

Every event ever notarized generates perpetual revenue via the Validation API (PRD_08): users pay sats to verify that their event was inscribed on Bitcoin.

**North Star Alignment:** One permanent record, globally verifiable, forever.

---

## Acceptance Criteria

1. **Batch Accumulation:** Sub 3 collects event hashes from queue within batch window (default 10 minutes, tunable). Collects all unique event_id:hash pairs in window.

2. **Merkle Tree Construction:** Builds Merkle tree from batch hashes. Root = merkle_root(hash1, hash2, ..., hashN). Tree is deterministic (same hashes → same root).

3. **Ordinal Inscription:** Inscribes Merkle root as Bitcoin Ordinal:
   - Data content: merkle_root (32 bytes, hex)
   - Metadata: GrowDirect treasury inscription
   - Ownership: treasury address controls all keys
   - Immutability: once inscribed, cannot be changed

4. **Inscription Response:** Two-part response pattern:
   - **Response 1 (milliseconds):** Hash sealed and batched. Return to caller: { event_id, status: "batched", merkle_position, root_hash }
   - **Response 2 (~10 minutes):** Bitcoin block confirms (avg 10 min). Return: { event_id, inscription_id, bitcoin_block, timestamp_confirmed }

5. **Merkle Proof Storage:** For each event in batch, store:
   - merkle_proof: siblings needed to reconstruct root from leaf
   - merkle_position: index in tree (0 to N-1)
   - root_hash: Merkle root of batch
   - inscription_id: Bitcoin inscribed object identifier
   - bitcoin_block: block height + hash of confirmation

6. **Idempotent Inscriptions:** If Sub 3 crashes after hashing but before Bitcoin broadcast, retry. Idempotency: same batch hashes → same root → same inscription. No duplicate inscriptions on Bitcoin.

7. **Sub 1 + Sub 2 Independence:** Sub 3 failure does not affect Sub 1 (evidence) or Sub 2 (detection). Events without Ordinals still have database immutability.

8. **Source-Agnostic Batching:** Merkle tree includes hashes from any webhook source (Stripe, Square, PayPal, custom). No source-specific logic.

9. **Key Custody (Crown Jewels):** GrowDirect treasury controls all inscription keys. No merchant, no user, no third party. Perpetual ownership guaranteed.

10. **Pool Utilization Monitoring:** Track Bitcoin block space (sat supply). Alert when utilization nears limit. Trigger programmatic expansion (buy more block space).

11. **Programmatic Pool Scaling:** Auto-expand inscription capacity as needed. Do not require manual key purchases or capacity provisioning.

12. **Validation Revenue AC (from business model addendum):** Every inscription enables perpetual revenue stream via Validation API (PRD_08). Sat micropayment per verification call. Design must support this model.

---

## Two-Response API Pattern

**Response 1: Batch Acknowledgment (< 100ms)**
```json
POST /notarize
{
  "event_ids": ["evt_1", "evt_2", ..., "evt_500"]
}

202 Accepted (Batched, not yet on chain)
{
  "batch_id": "batch_20260226_001",
  "status": "batched",
  "event_confirmations": [
    {
      "event_id": "evt_1",
      "status": "batched",
      "merkle_position": 0,
      "root_hash": "a3c7f9e2...",
      "estimated_bitcoin_confirmation": "2026-02-26T14:35:00Z"
    },
    ...
  ]
}
```

**Response 2: Bitcoin Confirmation (~10 minutes)**
- Event available for polling: GET /notarize/{event_id}
- Returns full proof (inscription_id, block height, merkle_proof)
- Can also push to webhook (merchant configurable)

```json
GET /notarize/evt_1

200 OK (Confirmed on Bitcoin)
{
  "event_id": "evt_1",
  "status": "confirmed",
  "inscription_id": "i7f9a2c8...",
  "bitcoin_block": {
    "height": 850100,
    "hash": "00000000...",
    "timestamp": "2026-02-26T14:35:22Z"
  },
  "merkle_proof": [
    "b4d8f0e3...",
    "d9e1a3c7...",
    ...
  ],
  "merkle_position": 0,
  "root_hash": "a3c7f9e2...",
  "verified": true
}
```

---

## Test Cases

### Happy Path
- 500 event hashes in batch window
- Merkle tree constructed: 500 leaves → balanced tree, depth ~9
- Root inscribed as Ordinal (transaction broadcast to Bitcoin mempool)
- ~10 minutes later: transaction confirmed in block 850100
- All 500 events have inscription_id, merkle_proof, bitcoin_block
- Batch completes: all events notarized permanently

### Edge Cases
- **Single Event Batch:** 1 event hash. Merkle root = hash of single event. Inscribed normally.
- **Duplicate Hash in Batch:** Same hash appears twice (clock skew). Merkle tree deduplicates. 1 merkle_position per unique hash. No duplicate inscriptions.
- **Batch Timeout:** Batch window expires with < 100 events. Inscribe partial batch anyway (do not wait for full batch).
- **Bitcoin Unavailability:** Broadcast fails (network down, no peers). Retry every 30 seconds. Queue message remains until success.
- **Slow Confirmation:** Transaction stays in mempool > 1 hour (congestion). Eventually confirms. Merchant polling sees status="pending" until block confirmation. No data loss.
- **Large Batch:** 10,000 events in batch (e.g., spike period). Merkle tree depth ~14. Inscribe full root. All 10,000 inscribed in single Ordinal.

### Toy Store Spike Scenario (REQUIRED)
- 5,000 toy_store events in 6-hour window
- Sub 3 collects hashes every 10 minutes:
  - Batch 1 (0–10 min): ~800 hashes → inscribed
  - Batch 2 (10–20 min): ~800 hashes → inscribed
  - ...
  - Batch 6 (50–60 min): ~200 hashes → inscribed
- 6 Ordinal inscriptions total (one per batch window)
- All 5,000 events mapped to inscription_id + merkle_proof + bitcoin_block
- No duplicate inscriptions
- All inscriptions confirmed on Bitcoin within ~60 minutes of end of spike
- Merkle proofs independently verifiable: any event can be proven to be in the inscribed root

### Failure Modes
- **Sub 3 Crash After Hash:** Batch accumulated, hash computed. Process crashes before Bitcoin broadcast. On restart, recompute batch from queue, same hashes → same root → retry broadcast. Idempotent.
- **Bitcoin Transaction Failure:** Broadcast succeeds, but transaction gets double-spent or dropped from mempool. Monitor mempool. Rebroadcast. Eventually confirms.
- **Merkle Tree Computation Error:** Merkle root computation throws exception. Log error, halt batch. Manual intervention (ops). No data loss: hashes remain in queue for next batch.
- **Key Custody Compromise:** (Security scenario) If treasury key stolen, attacker can forge Ordinals. Mitigation: hot/cold key separation (cold key holds bulk, hot key mints pool). (Advanced, Sprint 7.)

---

## Integration Points

**Reads from:**
- Message queue (same queue as Sub 1 and Sub 2, independently)
- Queue message format: { event_id, merchant_id, received_at, hash }

**Writes to:**
- Bitcoin blockchain: Ordinals (inscription_id, merkle_root)
- Evidence store (Sub 1 output): inscription_id, merkle_proof, merkle_position, bitcoin_block per event
- Structured logging: batch construction, tree building, inscription broadcast, confirmation

**Merkle Proof Storage Update (to evidence_store):**
```sql
ALTER TABLE evidence_store ADD COLUMN IF NOT EXISTS (
  ordinal_inscription_id VARCHAR(255),
  merkle_position INT,
  merkle_proof TEXT[],  -- array of sibling hashes
  merkle_root VARCHAR(64),
  bitcoin_block_height INT,
  bitcoin_block_hash VARCHAR(64),
  bitcoin_confirmation_time TIMESTAMP,
  CONSTRAINT ordinal_proof_check CHECK (
    (ordinal_inscription_id IS NULL) OR
    (ordinal_inscription_id IS NOT NULL AND merkle_position IS NOT NULL)
  )
);
```

**Bitcoin RPC Integration:**
```
RPC Node: standard Bitcoin Core node (or service)
Endpoints:
  - sendrawtransaction(tx_hex) → txid
  - getrawtransaction(txid) → tx details
  - getblock(block_hash) → block details
  - getmempoolinfo() → mempool stats
  - estimatefee(n_blocks) → sat/vB estimate
```

**Ordinals API Integration:**
```
Endpoint: ordinals.com or self-hosted indexer
- inscribe(data, metadata) → inscription_id
- get_inscription(inscription_id) → {data, owner, block, timestamp}
- getUtxo(inscription_id) → current satoshi location
```

---

## Non-functional Requirements

| Requirement | Target | Notes |
|-------------|--------|-------|
| **Batch Window** | 10 minutes (tunable) | Balance batching efficiency vs. latency |
| **Merkle Tree Depth** | < 20 | Support 1M+ events per batch if needed |
| **Inscription Latency** | < 5 min from batch close to broadcast | Allow headroom before next batch starts |
| **Bitcoin Confirmation Latency** | ~10 min avg (network dependent) | No control over Bitcoin network |
| **Idempotency Window** | Permanent | Same batch hashes → same inscription |
| **Key Custody Model** | Cold storage for bulk, hot pool for minting | Minimize compromise risk |
| **Block Space Utilization** | Monitored per batch | Alert if > 90% of pool exhausted |
| **Throughput** | 1M+ events/batch possible | Support spike scenarios |
| **Cost per Event** | ~0.01 sat / 100 events (tuned per Bitcoin fees) | Programmatically adjusted |

---

## Kubernetes Readiness

1. **Is this component stateless?**
   - **Mostly.** Sub 3 reads from queue, writes to Bitcoin blockchain (external). Local state: current batch accumulation. Pod restart during batch window would lose in-memory batch. Mitigation: persist batch state to queue or cache. For Sprint 6, assume batch completes before pod eviction.

2. **Does it scale horizontally?**
   - **No.** Sub 3 is single-instance. Multiple instances would create duplicate inscriptions (same batch minted twice). Use leader-election (Kubernetes coordination) if horizontal scaling needed (Sprint 7).

3. **Does it support rolling deployment?**
   - **Yes.** Old Sub 3 completes current batch, then drains. New Sub 3 starts fresh batch. No collision. Batch state must be passed or re-accumulated.

4. **What is the scaling trigger?**
   - **N/A for throughput.** Sub 3 is not throughput-limited. Scaling is resource-limited (Bitcoin RPC connections, key material). One instance is sufficient even at 1M events/batch.

5. **Toy store scaling profile?**
   - **Single instance.** 5,000 events over 6 hours = 6 batches of 800 events. One instance easily handles. No scaling needed.

---

## Merkle Tree Example (Toy Store Spike)

**Batch 1: Events 1–800**
```
Hashes: h1, h2, h3, ..., h800 (800 leaves)

Merkle tree (balanced):
                    root_hash_1
                   /           \
              level9_L         level9_R
             /       \        /        \
          ...
         /\
        h1 h2  h3 h4 ... h799 h800

merkle_proof for h1: [hash(h2), hash(h3,h4), hash(h5..h8), ..., level9_R]
                      = path from h1 to root (9 siblings)

Inscribe: root_hash_1 on Bitcoin
Inscription ID: i7f9a2c8d3e4f5a6b7c8d9e0f1a2b3c4d

Store per-event:
  h1 → merkle_position=0, merkle_proof=[...], inscription_id=i7f9a2c8...
  h2 → merkle_position=1, merkle_proof=[...], inscription_id=i7f9a2c8...
  ...
  h800 → merkle_position=799, merkle_proof=[...], inscription_id=i7f9a2c8...
```

---

## Business Model Integration (Crown Jewels)

Sub 3 enables the revenue model:
1. Every event inscribed on Bitcoin
2. Inscription is permanent, immutable, globally verifiable
3. Validation API allows any user to verify: given inscription_id + event_hash, prove membership in Ordinal
4. Verification requires payment (L402 Lightning invoice)
5. Every verification = perpetual revenue stream

**Design Constraint:** Sub 3 must support high-volume Validation API queries (PRD_08). Merkle proofs must be compact (< 1KB per event) and independently verifiable.

---

## IP Protection Notes

**Crown Jewels (do not expose in external docs):**
- Merkle batching strategy (competitive, proprietary)
- Batch window size (10 min tuning, performance secret)
- Tree construction algorithm (not standard Merkle, possibly proprietary compression)
- Key custody implementation (cold/hot separation strategy)
- Pool scaling automation logic (when to expand, how much, pricing)
- Two-response API design (latency model)
- Programmatic expansion triggers (threshold values)

**Safe to document externally:**
- Ordinal inscriptions (public Bitcoin feature)
- Merkle root concept (industry standard)
- Permanent blockchain immutability (Bitcoin property)
- Notarization narrative (public blockchain use case)

---

## Success Criteria

- [ ] 5,000 events batched into 6 Ordinal inscriptions over spike period
- [ ] All inscriptions confirmed on Bitcoin
- [ ] Merkle proofs independently verifiable: sample verification succeeds
- [ ] No duplicate inscriptions on Bitcoin
- [ ] Merkle positions correct: event N at position N in tree
- [ ] Sub 3 failure does not affect Sub 1 or Sub 2
- [ ] Idempotency: retry of failed batch produces same inscription
- [ ] Integration with Validation API (PRD_08): can verify events

---

## Open Questions

1. **Batch Window Optimization:** Is 10 minutes optimal? Trade-off: larger batches save block space, but increase latency. Test different windows.
2. **Bitcoin Congestion Handling:** During Bitcoin network congestion, fee estimation may spike. Should we dynamically adjust batch size to manage costs?
3. **Ordinal Indexing:** Do we maintain our own indexer or rely on public ordinals.com? Dependency and performance?
4. **Key Management:** Cold key stored where (hardware wallet, air-gapped, vault)? Hot key rotation policy?
5. **Pool Scaling Automation:** At what utilization % do we trigger expansion? How much block space do we buy at once?
