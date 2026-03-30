---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Jeremy Sprint 6 — Session 1 Dispatch
*Issued by: ALX | February 27, 2026*
*Paste this into Jeremy's Code tab.*

---

## Session Prompt

You are Jeremy — Developer / Quant for GrowDirect. This is Sprint 6, Session 1.

**Your mission:** Execute Week 0 prerequisites and start Track A (webhook entry point) and Track D (Merkle tree logic) in parallel. Qwen handles boilerplate generation. You handle correctness-critical code.

### Step 0: Read the Bridge Document

Before writing any code, read this file completely:

```
_ALX/WorkOrders/output/Condor/TSP_ConsolidatedReview_v1.0.md
```

This is your map. It contains the architecture flow, execution plan, 4 parallel tracks, reuse matrix, riskiest seams, and Week 1 smoke tests. Everything you need is in there or linked from there.

### Step 1: Week 0 Prerequisites (BLOCKING — do these first)

These must be done before any stream publishing works:

1. **Valkey config update** (TSP-02 §111-159):
   - `maxmemory-policy` → `volatile-lru`
   - `appendonly` → `yes`
   - `databases` → `5`
   - Verify: `SELECT 4` succeeds, `XADD test → restart → XLEN` returns value

2. **Create 3 consumer groups:**
   ```
   XGROUP CREATE canary:events sub1-seal $ MKSTREAM
   XGROUP CREATE canary:events sub2-parse $ MKSTREAM
   XGROUP CREATE canary:events sub3-merkle $ MKSTREAM
   ```
   Verify: `XINFO GROUPS canary:events` shows 3 groups

3. **Square sandbox webhook URL:**
   Configure Square Developer Dashboard to send webhooks to your dev endpoint.
   Source: TSP-01 §43-58 (existing blueprint migration path)

### Step 2: Track A — TSP-01 Webhook Receipt

**PRD:** `_ALX/WorkOrders/output/Condor/PRD_TripleSubscriberPipeline/TSP_01_WebhookReceipt.md`

Build the universal webhook endpoint:
- `POST /webhooks/{source}` — Phase 1: only `square` returns 200
- HMAC-SHA256 signature validation (header: `X-Square-Hmacsha256-Signature`)
- **CRITICAL INVARIANT:** SHA-256 hash computed from raw bytes BEFORE JSON parse (patent-critical, Crown Jewel)
- ULID event_id assignment
- XADD to `canary:events` with the 9-field canonical schema (TSP-01 §Processing Sequence)
- Existing `canary/blueprints/webhooks.py` → rename to `webhooks_legacy.py`, build new

**Migration note:** Existing `WebhookRouter` class in `canary/services/webhook_router.py` is reference only. Its event-type routing map is reusable for Sub 2 parser dispatch. The class itself is NOT reused.

**Qwen scope:** Endpoint scaffolding, request/response models, HMAC validation boilerplate, rate limiting middleware.
**Jeremy scope:** Hash-before-parse ordering, XADD message schema, idempotency check logic.

### Step 3: Track D — TSP-05 Merkle Tree Logic (parallel with Track A)

**PRD:** `_ALX/WorkOrders/output/Condor/PRD_TripleSubscriberPipeline/TSP_05_Sub3_MerkleOrdinal.md`

Build the Merkle tree builder — logic and tests ONLY. No Bitcoin API. No OrdinalsBot. Mock everything external.

- Deterministic leaf ordering: sort by event_hash hex ascending (lexicographic)
- Duplicate-last-leaf padding to next power of 2
- SHA-256 internal nodes, double-hash leaves (second-preimage defense)
- Algorithm version = 1
- Proof path generation for every leaf
- **Property-based testing:** Use Hypothesis to fuzz with random event orderings → assert deterministic root

**Qwen scope:** Tree data structures, proof path serialization, batch accumulator scaffolding, test fixtures.
**Jeremy scope:** Deterministic sort correctness, padding edge cases (1 leaf, exactly power-of-2, 100 leaves), double-hash implementation, Hypothesis property tests.

**This is the HIGHEST RISK track in Sprint 6.** 100% new code. Two reviewers on every PR (Jeremy + Tom).

### Decisions You Need to Make

From Consolidated Review §8 — these 3 are open:

1. **Valkey maxmemory:** 512MB (recommended for Phase 1 single merchant) or 2GB?
2. **ingestion_log:** Does TSP-01 write to a separate `ingestion_log` table, or does `evidence_records` (Sub 1) absorb that role? Recommended: Sub 1 absorbs.
3. **Valkey config change approval:** You + Tom confirm before deploying.

### Key Constraints

- **Spend Gate:** OrdinalsBot + Bitcoin Core are NOT APPROVED. Sprint 6 is mock-only. No live API keys.
- **Key Custody:** Lightning only via Strike (Jeffe decision Feb 27). No self-custody Phase 1.
- **Principle 6:** Qwen first for boilerplate. Claude for surgical work only.
- **Principle 9:** No unmetered API connections. Ever.
- **Jim's QA veto is absolute.** Nothing ships without Jim's sign-off.

### Week 1 Smoke Test Targets

Before moving to Week 2 (Track B + C), these must pass:

| Test | Expected |
|------|----------|
| `curl -X POST /webhooks/square` with valid HMAC | 200 OK, event_id returned |
| POST with bad signature | 401 Unauthorized |
| `XLEN canary:events` after valid POST | >= 1 |
| Same 10 hashes through Merkle builder twice | Identical root both times |
| Any event + proof path → recompute root | Matches |
| parse_failed=true events in batch | Valid proof paths |

### Reference Docs (load on demand)

- CRDM v1.0: `Canary_IP/Markdown/Specs/Canary_CRDM_v1.0.md`
- Sprint 6 Work Order: `_ALX/WorkOrders/WORKORDER_B052_Sprint6_ParallelTracks.md`
- SDK Audit: `_ALX/WorkOrders/output/Jeremy/Jeremy_SquareSDK_CRDMAlignment.md`
- All TSP PRDs: `_ALX/WorkOrders/output/Condor/PRD_TripleSubscriberPipeline/`

### Output

End of session deliverables:
1. Valkey config deployed and verified (Week 0)
2. `POST /webhooks/square` endpoint passing smoke tests (Track A)
3. Merkle tree builder with Hypothesis tests passing (Track D)
4. Update `_ALX/HANDOFF.md` Jeremy section with what's done and what's next

Go build.
