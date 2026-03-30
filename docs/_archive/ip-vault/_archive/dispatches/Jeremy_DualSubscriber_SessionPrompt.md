---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Jeremy Session Prompt — Dual Subscriber Pipeline: Engineering Assessment + B-036 Square SDK Audit
*Issued by: ALX | February 26, 2026 | CONFIDENTIAL*
*Priority: 🔴 CRITICAL*

---

## Two Tasks This Session

This session has two connected workstreams. Do them in order — the architecture assessment informs the SDK audit.

---

## TASK 1: Dual Subscriber Architecture — Engineering Assessment

### What Was Decided This Morning

Jeffe and ALX had an alignment session this morning. A key architectural decision emerged that affects B-035, B-036, and the patent filing. Here is what was decided:

**The raw evidence store architecture:**

When a Square webhook arrives, two things happen simultaneously:

```
Square webhook
      ↓
Message Queue (publisher — single receipt point)
      ↓
   ┌──┴──┐
   ↓     ↓
Sub 1   Sub 2
```

**Sub 1 — Raw Evidence Store (immutable)**
- Receives the raw webhook payload verbatim
- Never transforms, never normalizes
- Computes hash on receipt via pgcrypto on INSERT
- Chains hash to previous record (same pattern as fox_evidence)
- Writes to a write-once key-value store
- Never touched again. Ever.

**Sub 2 — Structured Store (canary.orders)**
- Receives the same message from the queue
- Parses and normalizes
- Routes to merchant partition
- Loads structured tables
- Triggers Chirp evaluation
- Can be redeployed, replaced, upgraded — Sub 1 is never affected

**The evidence store schema:**

```sql
CREATE TABLE raw_events (
    key             TEXT PRIMARY KEY,  -- merchant_id + ':' + square_event_id
    payload         JSONB NOT NULL,    -- raw webhook blob, verbatim
    hash            VARCHAR(64),       -- pgcrypto SHA-256, computed on INSERT
    chain_hash      VARCHAR(64),       -- links to previous record
    received_at     TIMESTAMPTZ DEFAULT NOW()
    -- NO UPDATE ever. INSERT only. Trigger enforces this.
);
```

Key is deterministic from Square's own identifiers. Write-once enforced by INSERT-only trigger.

**Why raw payload — not normalized:**

The hash must be computed on the verbatim payload. If we normalize before hashing, the evidentiary chain breaks — we cannot prove the stored record matches what Square transmitted. The raw payload IS the evidence. The hash IS the seal.

**The upgrade-in-place implication:**

Sub 2 is a projection of Sub 1. If a schema migration breaks Sub 2's parser, we replay from Sub 1. Sub 2 can be replaced entirely — new version deploys against the same queue, processes the backlog, catches up. Sub 1 never touched. Hash chain never interrupted. No rollback required. No downtime required.

### Your Engineering Deliverables — Task 1

**File:** `_ALX/WorkOrders/output/Jeremy/Jeremy_DualSubscriber_EngineeringAssessment.md`

**1. Message Queue Selection**

At Phase 1 (GrowDirect Lab — one merchant, low volume) what is the right queue implementation?

Options:
- PostgreSQL LISTEN/NOTIFY — already in stack, zero new infrastructure, limited throughput
- Redis Streams — lightweight, fast, Valkey already in stack (Redis-compatible)
- Kafka — correct at scale, heavy for Phase 1

Recommendation with rationale. Consider: Valkey already running. Redis Streams may be Phase 1 answer with Kafka as Phase 3 upgrade path.

**2. pgcrypto Hash Performance Under Spike Load**

We compute SHA-256 on INSERT for every raw_events record via pgcrypto trigger. At Black Friday peak for a large-format specialty retailer — NRF data suggests 10x-50x normal daily volume in 6-8 hours — what does pgcrypto hash computation cost per INSERT? Is there a throughput ceiling where hash-on-INSERT becomes the bottleneck?

If there is a ceiling: what is it approximately, and does it matter at Phase 1-2 SMB scale (under 10 locations)?

**3. Write-Once Enforcement**

The INSERT-only trigger pattern is proven on fox_evidence and canary_sales. Confirm the same pattern applies cleanly to raw_events with JSONB payload column. Any gotchas with JSONB and the existing trigger implementation?

**4. Replay Mechanism**

Describe the replay pattern: scan raw_events for merchant_id prefix, order by received_at, feed payload sequence back through Sub 2's parser. Manual operation or named recovery procedure?

**5. Zero-Downtime Sub 2 Upgrade**

Walk through the upgrade scenario:
- Sub 2 v1 processing from queue
- Deploy Sub 2 v2
- Sub 2 v1 drains and stops
- Sub 2 v2 picks up
- No events lost, no hash chain interrupted, no downtime

Achievable with your recommended queue technology? What is the operational procedure?

**6. Sub 3 — Ordinal Minter: Engineering Assessment**

This is the new sixth node. The product has been fully identified this session.

Jeffe's description: *"An API gateway that accepts any webhook, publishes it to a queue, mints an Ordinal inscription on the Bitcoin time chain, and returns both the raw event and the Bitcoin inscription reference — instantly, permanently, to any application that needs it."*

Sub 3 is the minter. After Sub 1 seals in PostgreSQL, Sub 3 runs asynchronously:

```
Sub 3 flow:
1. Collect recent raw_events hashes (batch window — you define)
2. Build Merkle tree from batch
3. Inscribe Merkle root as Ordinal on Bitcoin base layer
4. Store inscription_id + block_number against each event in the batch
5. Return inscription_id via API (the "Bitcoin form" of the notarized event)
```

Assess the following:

**A. Ordinals inscription API**
What is the current best Python library or API for programmatically inscribing data onto Bitcoin via Ordinals? Options include ord (the reference implementation), third-party inscription APIs (Ordinalsbot, Xverse API, Hiro). What is the right choice for a production system that needs to inscribe reliably and cheaply at scale?

**B. Cost model**
Ordinals inscription fees are denominated in sats, proportional to data size and Bitcoin mempool congestion. A Merkle root is 32 bytes — tiny. What is the approximate cost in sats and USD to inscribe a 32-byte Merkle root at normal mempool conditions? At congested conditions (Christmas, halving events)? At what batch size does cost per notarized event become negligible?

**C. Batching interval**
What is the right batching window? Options: time-based (every 10 min, every block), count-based (every 1000 events), hybrid. The window determines inscription frequency and cost. Recommend with rationale.

**D. Merkle proof per event**
Every event in a batch must be provably in the Merkle tree. The API must return: inscription_id + merkle_proof (the path from the event hash to the root). Describe the data structure. What does Jeremy store in raw_events to support this? A new column: `inscription_id`, `merkle_proof`, `bitcoin_block`.

**E. Latency expectation**
Sub 1 seals in milliseconds. Sub 3 confirms in ~10 minutes (one Bitcoin block). The API returns two responses — instant seal confirmation and Bitcoin confirmation when the block arrives. How does the system notify the caller when the Bitcoin confirmation arrives? Webhook callback? Polling endpoint? Recommend.

**F. Kubernetes readiness for Sub 3**
Sub 3 is a stateless batch worker — same constraints as Sub 1 and Sub 2. Confirm it satisfies the Kubernetes readiness checklist. One additional constraint: Sub 3 must handle Bitcoin network unavailability gracefully. If the inscription fails (network down, mempool full), the batch must be retried without duplicating inscriptions. Idempotency mechanism?

**G. The universal claim**
Sub 3 does not care what the webhook contains. It only cares about the hash. This means the minting service works for ANY webhook from ANY source — Square, Epic MyChart, FedEx, any network. The architecture is source-agnostic at Sub 3. Confirm this is correct and note any exceptions.

---

**7. Superset + dbt Footprint**

B-035 addendum proposes Superset as query surface and dbt for materialized view computation. Quick gut check: does Superset deploy cleanly into existing Docker stack? Approximate memory footprint on iMac? Does dbt conflict with existing Airflow patterns or is it additive?

One paragraph. Not a full assessment. Just your read before Tom commits.

**7. Kubernetes Readiness — Design Constraints (NON-NEGOTIABLE)**

We are on Docker Compose now. We will be on Kubernetes in Phase 3. The architectural decisions you make today must not require refactoring when we containerize for K8s.

The following are hard constraints on every component you design in this session:

**Sub 1 and Sub 2 workers must be stateless.**
- No local state. No in-memory caches that cannot be distributed.
- No assumption of a single running instance.
- All state lives in the queue (input) or the database (output). Never in the worker process itself.
- If Kubernetes kills a worker pod mid-processing and restarts it on a different node, no data is lost and no hash chain is corrupted.

**All workers must be horizontally scalable.**
- Running 3 Sub 2 pods simultaneously must produce identical results to running 1.
- No race conditions on concurrent writes to raw_events. The primary key (merchant_id + event_id) is the idempotency guard — duplicate processing of the same event must be a no-op, not a conflict.
- Queue consumption must support competing consumers — multiple Sub 2 pods pulling from the same queue without double-processing.

**The message queue must support competing consumers.**
- This is a queue technology selection constraint. PostgreSQL LISTEN/NOTIFY does not support competing consumers cleanly. Redis Streams consumer groups do. Kafka consumer groups do.
- Your Phase 1 recommendation must support the competing consumer pattern even if we only run one consumer at Phase 1. We are not redesigning the queue at Phase 3.

**No hardcoded infrastructure assumptions.**
- No hardcoded hostnames, ports, or IP addresses in worker code.
- All configuration via environment variables (already the pattern — confirm it holds here).
- A worker pod must be able to start on any node in the cluster and find its dependencies via service discovery.

**Rolling deployment must be safe.**
- Sub 2 v1 and Sub 2 v2 must be able to run simultaneously during a rolling deploy without corrupting canary.orders.
- This means: Sub 2 v2 must be able to parse any event that Sub 2 v1 would have parsed, and vice versa, during the transition window.
- If a schema migration in Sub 2 v2 is incompatible with Sub 2 v1, that is a breaking change and must be flagged before deployment.

**Kubernetes readiness deliverable:**
Add a section to your engineering assessment: **Kubernetes Readiness Checklist** — confirm each constraint above is satisfied by your proposed design, or flag where it is not. This checklist is the gate before Tom finalizes DDL. If a constraint cannot be satisfied, ALX needs to know before we build, not after.

**The Kubernetes architecture in plain terms:**

```
Kubernetes cluster (Phase 3)
├── Webhook receiver   — Deployment, scales under spike
├── Message queue      — Valkey/Redis Streams or Kafka
├── Sub 1 workers      — Deployment, stateless, competing consumers
├── Sub 2 workers      — Deployment, stateless, competing consumers, autoscales
├── Chirp evaluation   — Deployment, stateless
└── PostgreSQL         — NOT in K8s. Managed service (RDS/Neon) or StatefulSet.
                         Database is the one stateful component. K8s handles everything else.
```

Sub 2 is where horizontal scaling earns its money. Under Black Friday load Kubernetes autoscales Sub 2 pods. Queue backlog drives the scaling metric — more backlog, more pods. Spike ends, pods terminate. Toy store pays for 4 pods in December and 1 pod in February. This is only possible if Sub 2 is stateless from day one.

PostgreSQL is explicitly NOT inside Kubernetes for production. It sits on stable managed infrastructure. Kubernetes orchestrates elastic compute. The database provider handles elastic storage. Clean separation. Jeremy's design must never assume PostgreSQL is co-located with the worker pods.

---

## TASK 2: B-036 Square SDK Audit

**Read the full work order:** `_ALX/WorkOrders/WORKORDER_Jeremy_SquareSDK_CRDMAlignment.md`

### Updated P0 Findings (Four)

Flag each immediately when you have an answer — do not wait for the full audit.

**P0-1: Labor API webhook availability**

C-301 is now two Chirps:
- C-301A: Sale or return outside scheduled shift hours — end-of-day reconciliation acceptable
- C-301B: Return processed by employee with NO shift record that day — real-time target, high severity

C-301B is the loss prevention signal that matters. If Labor API is push (webhook), C-301B is real-time. If pull-only, C-301B needs a different detection mechanism. Flag the moment you have this answer.

**P0-2: card_fingerprint scope**

Scope is now: **card tenders only** (card-present and card-not-present). Cash and gift card tenders excluded.

Critical question: is Square's card_fingerprint **merchant-scoped** (different token for same physical card at different merchants) or **network-universal** (same token across all Square merchants)?

Jeffe's instinct: network-universal. If confirmed, route to Syd immediately — legal exposure and strategic opportunity both change significantly.

**P0-3: Raw payload storage — Square ToS**

The dual subscriber architecture requires storing Square's raw webhook payload verbatim — JSONB blob, immutable, hash-chained. Verify: does Square's Developer ToS permit verbatim storage? Any data retention restrictions? Any field-level restrictions?

If restricted: flag immediately. ALX routes to Syd. Tom holds DDL on raw_events until Syd clears it. Architecture-blocking.

**P0-4: Square webhook send log retention**

For bilateral verification to work: how long does Square retain webhook delivery logs? Is there an API or support mechanism to request a specific event's send record?

If Square purges after 30 days, the verification window is limited and the patent claim needs scoping accordingly.

### P1 Items

Remaining 6 items from original work order (timestamp precision, cash drawer events, timecard state, inventory adjustments, line item detail, gift card webhooks, loyalty webhooks). Complete after P0s. Flag material gaps to Tom (schema) or Syd (legal) as found.

### Partition Boundary Addition

From this morning: partition boundary is **midnight in the location's time zone** — not merchant time zone, not UTC. Timezone derived from `location.timezone` on the webhook payload (or from location_id lookup).

Verify: does Square deliver `location.timezone` on webhook payloads, or only on the Location object (requiring a separate API call)? P1 finding, but flag early if you see it.

### Output

`_ALX/WorkOrders/output/Jeremy/Jeremy_SquareSDK_CRDMAlignment.md`

P0 findings at top, clearly labeled, routed immediately. P1 findings below. Summary gap table at end.

---

## Deadline

**Task 1:** Before Tom's next B-035 session. Tom cannot finalize partition DDL without knowing the queue architecture and raw_events schema.

**Task 2 P0s:** Flag each immediately on confirmation. P0-3 (ToS) needs Syd's attention ASAP.

**Task 2 P1s:** Complete this session if possible. End of day at latest.

---

## Competitive Context — Why This Architecture Matters

**CONFIDENTIAL. Do not reference externally.**

Jeffe met directly with Oracle Retail OCI engineers. They could not articulate how they would scale a polling architecture on Oracle Cloud to aggregate feeds from all other clouds.

Oracle is the enterprise incumbent. Their engineers do not have a credible answer to the scaling problem at the heart of their own architecture.

**What this means for your session:**

The stateless, event-driven, Kubernetes-ready dual subscriber architecture you are designing is not just better than Oracle's approach — it is architecturally in a different class. Oracle polls. We receive. Oracle is the man in the middle. We are the endpoint. Oracle has latency floors, thundering herd problems, and no settlement finality. We have webhook-native receipt, hash-on-INSERT, and bilateral verification.

The Kubernetes readiness constraints in this prompt are not academic. They are what separates an architecture that works at Black Friday scale from one that Oracle's own engineers couldn't figure out how to scale.

Build it right. This is the moat.

Full intelligence note: `Canary_IP/Markdown/Strategy/CompetitiveIntel_Oracle_OCI_Polling.md`

---

## Standing Rules

- Plan mode before any code.
- Log session to timelog on close.
- P0 findings route to ALX immediately — don't wait.

---

*ALX | Chief of Staff | February 26, 2026*
*Gates: Tom B-035 DDL | Routes to: Syd (P0-2, P0-3) | Tom (schema gaps)*
