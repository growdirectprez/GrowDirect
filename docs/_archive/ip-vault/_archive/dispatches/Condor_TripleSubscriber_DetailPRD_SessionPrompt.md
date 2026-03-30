---
type: workorder
domain: tsp
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Condor Session Prompt — Triple Subscriber Pipeline: Detailed Component PRDs
*Issued by: ALX | February 26, 2026 | CONFIDENTIAL*
*Supervisor: PhD (primary) | Legal gate: Syd | Quality gate: Jess*
*Priority: 🔴🔴 CRITICAL — Jeremy is BLOCKED until these ship*
*Supersedes: Condor_DualSubscriber_SessionPrompt.md (architecture upgraded to Triple Subscriber)*

---

## Why This Matters Right Now

The site is live. People are seeing GrowDirect for the first time. Jeffe wants to move from marketing to product — wire up the real code. Jeremy cannot start building until he has PRDs detailed enough that he and Qwen can execute without guessing.

PhD delivered four patent-grade architecture visuals today. These are your source of truth. Every PRD you produce must trace directly to a node, component, or data flow in these figures.

**Your deliverables unblock Jeremy's entire Sprint 6 build.**

---

## The Architecture — What PhD Delivered (Your Primary References)

### FIG. 1 — Six-Node System Architecture
`_ALX/WorkOrders/output/PhD/Patent_SixNode_Architecture_v1.0.html`

Six nodes in a staged pipeline:

| Node | Name | Function |
|---|---|---|
| NODE 1 | Universal Webhook Origination | Any source network: Square, Shopify, Epic, FedEx, SAP. Raw webhook POST. Source-agnostic. |
| NODE 2 | API Gateway & Queue Publication | HMAC-SHA256 validation. SHA-256 hash at receipt. Publishes to durable queue. Fan-out to 3 subscribers. |
| NODE 3 (Sub 1) | Hash & Seal | Write-once evidence store. SHA-256 hash + chain link. Append-only. Bilateral verify. T+0. |
| NODE 4 (Sub 2) | Parse & Route | Structured queryable store. Indexed by merchant partition. Mutable. Replayable from Sub 1. |
| NODE 5/6 (Sub 3) | Merkle & Ordinal | Batch hash aggregation → Merkle tree → Ordinal inscription on Bitcoin. Key custody. ~10min confirmation. |
| OUTPUT | Permanent Event Record | **Dual Form:** Application form (structured, queryable, API-ready) + Bitcoin form (inscription ID, Merkle proof, block explorer URL). L402 sat-gated validation generates perpetual revenue. |

**Core innovation: Triple Subscriber Pattern.** Three decoupled consumers, no cross-dependency, each with independent persistence model. This is what makes the architecture source-agnostic and upgrade-safe.

### FIG. 2 — Single Transaction Data Flow
`_ALX/WorkOrders/output/PhD/Patent_DataFlow_Visual_v2.0.html`

Temporal sequence showing a single event's journey:

| Timestamp | Phase | What Happens | Cryptographic Operation |
|---|---|---|---|
| T+0ms | Event Generation | Source signs payload with HMAC-SHA256 | `HMAC-SHA256(payload, merchant_secret)` |
| T+5ms | Gateway Receipt | Validate signature. Hash raw bytes. Enqueue. 200 OK. | `SHA-256(raw_payload_bytes) → event_hash` |
| T+15ms | Triple Fan-Out | Sub 1: chain hash + write-once. Sub 2: parse + partition + detect. Sub 3: accumulate for Merkle batch. | `chain_hash = SHA-256(prev_chain_hash + event_hash)` |
| T+100ms | Detection + Query | Rules evaluate. Alerts fire. Structured store serves dashboard. | — |
| T+~10min | Bitcoin Inscription | Merkle root inscribed as Ordinal. ECDSA signed. | `ECDSA sign → Ordinal inscription` |
| T+∞ | Perpetual Validation | L402 API: 402 → Lightning invoice → sat → proof. Revenue forever. | `L402: invoice → payment → Merkle proof` |

### FIG. 3 — Component Interaction Diagram
`_ALX/WorkOrders/output/PhD/Patent_TripleSubscriber_Component_v1.0.html`

Detailed component breakdown with technology assignments:

| Layer | Component | Tech Stack |
|---|---|---|
| Ingestion | Source Network | HTTPS POST + HMAC-SHA256 |
| Ingestion | API Gateway / Webhook Receiver | Node.js + Express |
| Queue | Message Queue (Durable, Ordered) | Valkey Streams |
| Subscriber | Sub 1: Hash & Seal | PostgreSQL JSONB · Write-Once |
| Subscriber | Sub 2: Parse & Route | PostgreSQL Tables · Partitioned |
| Subscriber | Sub 3: Merkle & Ordinal | Node.js Worker · Bitcoin Core |
| Persistence | Evidence Store | PostgreSQL JSONB · Deep Blue |
| Persistence | Structured Store | PostgreSQL Tables · Partitioned |
| Persistence | Ordinal Pool Registry | PostgreSQL + Bitcoin Core |
| Application | Detection Engine + Dashboard | Node.js · React Frontend |
| Application | Validation API (L402 Sat-Gated) | L402 · Lightning Network |
| Verification | Bilateral Verification Path | SHA-256 Compare · Merkle Proof · Block Explorer |

### FIG. 2 (Sequence) — Temporal Lifecycle
`_ALX/WorkOrders/output/PhD/Patent_DataFlow_Sequence_v1.0.html`

Timeline rail with 6 phases (T+0ms → T+∞). Cryptographic operations at each phase. This is the temporal contract — Jeremy's implementation must hit these timing windows.

---

## Your Deliverables — Nine Component PRDs

**IMPORTANT:** The previous dispatch specified 7 PRDs for a "dual subscriber" architecture. PhD upgraded this to Triple Subscriber with three additional components (Sub 3 Ordinal Minter, L402 Validation API, Bilateral Verification). You are producing **9 PRDs** covering the full six-node pipeline plus application and verification layers.

Each PRD must be detailed enough that **Jeremy + Qwen can code directly from it without asking a single clarifying question.** That means:

- **API contracts** with request/response JSON shapes
- **Database schema** with column names, types, constraints, and indexes
- **Error handling** — what happens when each failure mode occurs
- **Configuration** — what environment variables, secrets, and settings are required
- **Sequence diagrams** in text (Mermaid or ASCII) showing the happy path
- **Edge cases** enumerated and dispositioned (handle, reject, or defer)

### PRD Structure (Required for Every PRD)

```markdown
# PRD: [Component Name]
**PRD ID:** TSP-[XX]
**Version:** 1.0
**Owner:** [Jeremy / Tom / as appropriate]
**Patent Figure Reference:** FIG. [X] — [Node/Component name]
**Depends on:** [list dependencies by PRD ID]
**Gates:** [what this component gates]
**Sprint target:** Sprint 6 / Sprint 7

## Purpose
One paragraph. What this component does and why it exists in the pipeline.

## Architecture Position
Where this sits in the six-node pipeline. What feeds it. What it feeds.
Reference the specific FIG. number and node.

## API Contract
Full request/response shapes. Every endpoint this component exposes or consumes.

## Data Model
Table names, columns, types, constraints, indexes.
For queue components: message shape, consumer group config.

## Acceptance Criteria
Numbered. Binary pass/fail. No ambiguity.

## Sequence Diagram
Text-based (Mermaid or ASCII). Show the happy path end-to-end.

## Error Handling
| Error | Detection | Response | Recovery |
Enumerate every failure mode.

## Test Cases
- Happy path (with specific input/output examples)
- Edge cases (enumerated)
- **Toy store spike scenario** (required — 50x volume)
- Failure modes (each error from the table above)
- Timing validation (must hit FIG. 2 temporal windows)

## Configuration
Environment variables, secrets, feature flags.

## Kubernetes Readiness
1. Stateless? (can K8s kill and restart without data loss?)
2. Horizontal scaling? (can we run N instances without races?)
3. Rolling deployment? (can v1 and v2 coexist?)
4. Scaling trigger? (what metric does K8s watch?)
5. Toy store scaling profile? (how many pods at 50x?)

## Non-Functional Requirements
- Throughput (events/second sustained and burst)
- Latency (p50, p95, p99)
- Durability (what guarantees?)
- Upgrade path (how does this component get replaced without downtime?)

## IP Protection Notes
What must not appear in external docs. Flag Crown Jewels.

## Integration Checklist
[ ] Depends on [PRD-XX] — status
[ ] Feeds [PRD-XX] — interface defined
[ ] Tested independently — test harness described
```

---

### The Nine PRDs

#### TSP-01: Webhook Receipt & HMAC Validation (NODE 1 → NODE 2 boundary)
**FIG. Reference:** FIG. 1 Node 1 + Node 2 top half, FIG. 2 T+0 → T+5ms, FIG. 3 Ingestion Layer

Entry point. Any source network POSTs a webhook. Gateway validates HMAC-SHA256 signature. Rejects invalid. Computes SHA-256 of raw payload bytes. Assigns event_id. Returns 200 OK within milliseconds.

**Detail requirements:**
- Full API endpoint spec: URL, method, headers, body format
- HMAC validation algorithm: which header carries the signature, how to reconstruct the expected signature, timing-safe comparison
- SHA-256 computation: must hash raw bytes BEFORE any JSON parsing (this is a Crown Jewel detail — the order matters)
- Idempotency: how to handle Square resending the same event (event_id dedup)
- Rate limiting: what happens when a source sends faster than gateway can process
- Health check endpoint for Kubernetes liveness/readiness probes
- Metrics: request count, validation success/fail rate, latency histogram

**Toy store spike:** 500 webhooks in 60 seconds. Zero dropped. All validated. All hashed. All enqueued. 200 OK returned to every request within 3 seconds.

---

#### TSP-02: Queue Publication & Fan-Out (NODE 2 bottom half)
**FIG. Reference:** FIG. 1 Node 2 fan-out arrows, FIG. 2 T+5ms → T+15ms, FIG. 3 Queue Layer

After gateway validates and hashes, the message is published to Valkey Streams. Three independent consumer groups subscribe. At-least-once delivery. Message ordering within merchant partition.

**Detail requirements:**
- Valkey Streams message shape (what fields are published)
- Consumer group configuration: three groups (sub1-seal, sub2-parse, sub3-merkle)
- Ordering guarantee: XADD ordering within stream, consumer group offsets
- Durability: what happens if Valkey restarts (AOF persistence config)
- Dead letter handling: what happens if a consumer fails to ACK after N retries
- Backpressure: what happens when consumers fall behind (queue depth monitoring)
- Message TTL: how long do unprocessed messages stay in the stream

**Toy store spike:** 5,000 messages enqueued in 6 hours. All three consumer groups process independently. Queue depth peaks and drains within defined SLA.

---

#### TSP-03: Sub 1 — Hash & Seal Evidence Writer (NODE 3)
**FIG. Reference:** FIG. 1 Sub 1 box, FIG. 2 T+15ms Sub 1 lane, FIG. 3 Sub 1 + Evidence Store

**The immutability anchor.** Reads from queue consumer group. Writes verbatim payload to evidence store. Computes chain hash. Write-once enforced. Never transforms. Never updates. Never deletes.

**Detail requirements:**
- Full table DDL: `evidence_records` with columns, types, constraints
  - `id` (bigserial PK)
  - `merchant_id` (text, NOT NULL)
  - `source_event_id` (text, NOT NULL) — the payment network's event ID
  - `event_hash` (bytea, NOT NULL) — SHA-256 of raw payload (computed at gateway)
  - `chain_hash` (bytea, NOT NULL) — SHA-256(prev_chain_hash + event_hash)
  - `raw_payload` (jsonb, NOT NULL) — verbatim, untransformed
  - `received_at` (timestamptz, NOT NULL, DEFAULT now())
  - UNIQUE constraint on (merchant_id, source_event_id)
- Write-once trigger: INSERT-only trigger that rejects UPDATE/DELETE
- Chain hash computation: must be done in the INSERT trigger or application code? Specify exactly.
- Consumer group offset management: how Sub 1 ACKs processed messages
- Failure handling: what if INSERT fails (duplicate, connection error, disk full)
- Batch INSERT vs single INSERT: which is correct for chain integrity?
- Index strategy: what queries will this table serve? (bilateral verification lookups)

**Toy store spike:** 5,000 records written. All hashes correct. Chain integrity verified first-to-last. No partial writes. No chain gaps.

**Upgrade-in-place:** Sub 1 stopped, code updated, restarted. Queued events during downtime processed. Chain continuous.

---

#### TSP-04: Sub 2 — Parse & Route Structured Writer (NODE 4)
**FIG. Reference:** FIG. 1 Sub 2 box, FIG. 2 T+15ms Sub 2 lane, FIG. 3 Sub 2 + Structured Store

Reads from same queue, different consumer group. Parses raw payload into structured schema. Routes to merchant partition. Loads structured store tables. Emits to detection engine.

**Detail requirements:**
- Parser specification: how each Square event type maps to structured tables
  - `payment.created` → `transactions` table columns
  - `refund.created` → `refund_links` table columns
  - `order.created` → `orders` + `order_line_items` tables
  - `cash_drawer.shift.*` → `cash_drawer_shifts` table
  - `cash_drawer.event.*` → `cash_drawer_events` table
  - `labor.shift.*` → `timecards` table
  - `gift_card.activity.*` → `gift_card_activity` table
- Partition routing: how merchant_id determines the target partition
- Timezone handling: location timezone for partition boundary calculation
- Detection emit: after structured INSERT, how is the detection engine triggered? (direct call, event bus, or query?)
- Failed parse: logged, skipped, does NOT affect Sub 1, does NOT block queue
- Replay capability: given merchant_id + time range, Sub 2 can rebuild from Sub 1's evidence store

**Toy store spike:** 5,000 events parsed and routed. Sub 2 processes at sustainable rate. Queue backlog clears within SLA. Detection may be delayed but no events lost.

**Upgrade-in-place:** Sub 2 v2 deployed while v1 drains. v2 picks up. No events processed twice. No events lost. Sub 1 never touched.

---

#### TSP-05: Sub 3 — Merkle Batcher & Ordinal Minter (NODE 5/6)
**FIG. Reference:** FIG. 1 Sub 3 box, FIG. 2 T+~10min, FIG. 3 Sub 3 + Ordinal Pool Registry

Reads from same queue, third consumer group. Accumulates event hashes. Builds Merkle tree when batch threshold reached. Inscribes Merkle root as Ordinal on Bitcoin. Maps every event to its Merkle proof path.

**Detail requirements:**
- Batch strategy: time-based (every N minutes) or count-based (every N events) or hybrid? Specify.
- Merkle tree construction: which hashing algorithm, leaf ordering, proof generation
- Ordinal inscription: how the Merkle root becomes an inscription (OrdinalsBot API? Direct Bitcoin Core RPC?)
- Pool registry table DDL:
  - `inscription_id` (text)
  - `merkle_root` (bytea)
  - `bitcoin_block` (integer)
  - `block_explorer_url` (text)
  - `batch_event_count` (integer)
  - `created_at` (timestamptz)
- Event-to-inscription mapping table DDL:
  - `event_hash` (bytea, FK to evidence_records)
  - `inscription_id` (text, FK to pool registry)
  - `merkle_proof_path` (jsonb) — array of sibling hashes for verification
  - `leaf_index` (integer)
- Two-response contract:
  - Response 1 (T+15ms): "hash sealed, chain position assigned" — from Sub 1
  - Response 2 (T+~10min): "inscription_id, block_number, block_explorer_url" — from Sub 3
- Bitcoin network unavailability: retry strategy, does NOT cascade to Sub 1 or Sub 2
- Key custody: how ECDSA signing keys are stored, rotated, backed up
- Fee estimation: how transaction fees are calculated for inscription batches

**Toy store spike:** 5,000 events in 6 hours. All hashes batched. Inscriptions complete within SLA. No lost inscriptions. No duplicates.

**Kubernetes:** Stateless batch worker. Scales independently. Bitcoin unavailability does not cascade.

---

#### TSP-06: Detection Engine (Application Layer — fed by Sub 2)
**FIG. Reference:** FIG. 2 T+100ms Detection box, FIG. 3 Application Layer left

Rules evaluate against parsed event data from Sub 2's structured store. 26 Chirp rules across 8 categories. Fires alerts. Serves merchant dashboard via WebSocket.

**Detail requirements:**
- Rule evaluation trigger: how does the detection engine know Sub 2 wrote a new record?
- Rule engine interface: input shape (structured event) → output shape (alert or no-alert)
- Alert persistence: where alerts are stored, schema
- WebSocket push: how real-time alerts reach the merchant dashboard
- ThresholdManager integration: per-merchant toggle + threshold configuration
- Chirp Config page API: full contract for GET /config and PUT /toggle (reference PRD E1-F14)
- Latency target: Chirp fires within 500ms of Sub 2 structured INSERT

**Reference:** Existing PRD E1-F14 (`_ALX/WorkOrders/PRD_ChirpConfig_APIGateway_v1.0.md`) has the Chirp Config UI spec and all 26 rule mappings. Do NOT duplicate — reference it and extend with the detection engine internals.

---

#### TSP-07: L402 Validation API (Revenue Layer)
**FIG. Reference:** FIG. 2 T+∞ phase, FIG. 3 Application Layer right

Any party requests event validation. System returns HTTP 402 with Lightning invoice. Upon sat payment: returns verification status, Bitcoin block number, Merkle proof path, inscription ID, timestamp.

**Detail requirements:**
- Full API contract:
  - `GET /validate/{event_hash}` → 402 Payment Required
  - Response includes Lightning invoice (BOLT11)
  - After payment: verification response JSON shape
- Payment flow: Lightning invoice generation, payment detection, response delivery
- What the validation response contains:
  - `verified: boolean`
  - `event_hash: string`
  - `chain_hash: string`
  - `inscription_id: string`
  - `bitcoin_block: integer`
  - `block_explorer_url: string`
  - `merkle_proof: array`
  - `timestamp: ISO 8601`
- Pricing: per-validation sat amount (configurable)
- Revenue tracking: how validation revenue is recorded
- Rate limiting: prevent abuse/scraping
- Cache: can validation results be cached? (yes — Bitcoin confirmations are permanent)

**This is the perpetual revenue engine.** Every event ever notarized generates potential revenue on every future validation request. Specify this clearly.

---

#### TSP-08: Bilateral Verification Procedure (Verification Layer)
**FIG. Reference:** FIG. 2 Bilateral Verification bar, FIG. 3 External Verification

On-demand forensic procedure. Given an event identifier: retrieve raw evidence, recompute hash, compare against source send log, verify Merkle proof against Bitcoin block explorer. No trust required.

**Detail requirements:**
- Verification steps (numbered procedure):
  1. Retrieve evidence record by merchant_id + source_event_id
  2. Recompute SHA-256 of stored raw_payload
  3. Compare recomputed hash against stored event_hash
  4. Compare stored event_hash against source network's send log hash
  5. Verify chain_hash links to adjacent records
  6. If inscribed: verify Merkle proof path against inscription on block explorer
- Output: structured evidentiary report (JSON shape specified)
- Audit logging: every invocation logged
- Read-only: procedure never modifies evidence store
- Failure modes: record not found, hash mismatch (tamper detected), chain gap, inscription not yet confirmed

---

#### TSP-09: Replay & Rebuild Procedure (Operational)
**FIG. Reference:** Sub 2 "Replayable from Sub 1" property

Operational procedure for rebuilding Sub 2's structured store from Sub 1's raw evidence store. This is what makes upgrades safe — Sub 2 is always rebuildable.

**Detail requirements:**
- Replay command interface: `replay --merchant_id=X --from=DATE --to=DATE`
- Reads from evidence_records ordered by received_at
- Feeds each raw_payload through current Sub 2 parser version
- Idempotent: running twice produces identical output
- Read-only against Sub 1
- Progress tracking: percentage complete, ETA, records processed/remaining
- Failed parses: logged and skipped (do not halt)
- Schema migration replay: if Sub 2 parser v2 changes column mappings, replay rebuilds with new schema

**Toy store spike:** Replay 10,000 records for single merchant (full Black Friday). Completes within SLA. Output matches original.

---

## What To Read (In Order)

1. **This prompt** — your mission and PRD structure
2. **PhD Patent Visuals** (all four — these are your architecture source of truth):
   - `Patent_SixNode_Architecture_v1.0.html` (FIG. 1)
   - `Patent_DataFlow_Visual_v2.0.html` (FIG. 2)
   - `Patent_TripleSubscriber_Component_v1.0.html` (FIG. 3)
   - `Patent_DataFlow_Sequence_v1.0.html` (FIG. 2 temporal)
3. **Existing PRD E1-F14:** `_ALX/WorkOrders/PRD_ChirpConfig_APIGateway_v1.0.md` — Chirp Config + OAuth spec. Reference for TSP-06, do not duplicate.
4. **CRDM v1.0:** `Canary_IP/Markdown/Specs/Canary_CRDM_v1.0.md` — canonical data model for Sub 2 structured tables
5. **B035 Addendum:** `_ALX/WorkOrders/B035_Addendum_TemporalPartition_QueryGovernor.md` — partition architecture context
6. **Jeremy's SDK Audit:** `_ALX/WorkOrders/output/Jeremy/Jeremy_SquareSDK_CRDMAlignment.md` — what Square actually delivers (gaps noted)

Do NOT read Jeremy's engineering assessment before writing. Write from the architecture first. Jeremy's numbers populate the non-functional fields when available.

---

## Output Location

`_ALX/WorkOrders/output/Condor/PRD_TripleSubscriberPipeline/`

Files:
- `TSP_00_Index.md` — master index with dependency graph
- `TSP_01_WebhookReceipt.md`
- `TSP_02_QueueFanOut.md`
- `TSP_03_Sub1_HashSeal.md`
- `TSP_04_Sub2_ParseRoute.md`
- `TSP_05_Sub3_MerkleOrdinal.md`
- `TSP_06_DetectionEngine.md`
- `TSP_07_L402_ValidationAPI.md`
- `TSP_08_BilateralVerification.md`
- `TSP_09_ReplayRebuild.md`

---

## Deadline

**End of session.** Jeremy is waiting. These PRDs feed his entire Sprint 6 build. Tom needs TSP-03 and TSP-04 for DDL finalization. Syd needs all nine for patent claim alignment.

---

## IP Protection — Before You Write

Crown Jewels check on each PRD:
- The hash-before-parse ordering (TSP-01) is a Crown Jewel — describe the requirement, not the implementation trick
- Chain hash computation mechanism (TSP-03) — describe behavior, not trigger SQL
- Merkle batching strategy (TSP-05) — describe the contract, not the tree construction algorithm
- L402 pricing model (TSP-07) — describe the flow, not the economics
- No internal schema names in external-facing language
- No threshold values or rule logic details
- Flag anything that reveals competitive advantage

Each PRD has an IP Protection Notes section. Use it.

---

## Competitive Context

CONFIDENTIAL. Same context as previous dispatch — Oracle OCI engineers could not articulate scaling for their polling architecture. Every PRD you write is building the evidentiary foundation that this event-driven triple subscriber pipeline works where polling cannot.

Write these PRDs as if they will be read by an expert witness in a patent proceeding. Because they might be.

---

## Standing Rules

- PhD supervises. Unsure about Crown Jewels — stop, flag to PhD.
- Syd reviews all nine PRDs before any go external.
- Jess quality-checks for readability.
- Every PRD must trace to a specific FIG. number and node.
- Log session to timelog on close.

---

*ALX | Chief of Staff | February 26, 2026*
*Routes to: Jeremy (Sprint 6 build) | Tom (DDL) | Syd (patent alignment) | PhD (architecture validation)*
*Blocks: Jeremy cannot start coding until these ship.*
