---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Condor Session Prompt — Staged Immutability Pipeline: Component PRDs
*Issued by: ALX | February 26, 2026 | CONFIDENTIAL*
*Supervisor: PhD (primary) | Legal gate: Syd | Quality gate: Jess*
*Priority: 🔴 HIGH — Patent filing and Sprint 6 architecture depend on these*

---

## Your Mission This Session

Canary has a novel architecture. PhD is documenting the patent schematic. Jeremy is assessing the engineering. Your job is to break the architecture into **component-level PRDs** — granular enough that each component can be built, tested, and validated independently.

Jeffe's requirement, stated explicitly this morning:

> "It has to be rock solid and scalable at incredible peak volumes — that's the hard part about retail. The spikes, daily and seasonally, are all killers. A toy store that sells 95% of their business in 6 weeks has the infrastructure sitting around the rest of the year. We need to flex up and down seamlessly. But it has to work and never fail and never roll back and also be upgraded in place."

Every PRD you produce must include the toy store spike scenario as a named test case. If a component cannot be tested under simulated Black Friday load, it is not complete.

---

## The Architecture — What You Are Decomposing

```
NODE 1: Payment network transmits raw webhook payload
             ↓
NODE 2: Message Queue (publisher — single receipt point)
             ↓
          ┌──┴──┐
          ↓     ↓
NODE 3:  Sub 1  NODE 4: Sub 2
         Hash &          Parse &
         Seal            Load
         (raw            (structured
         evidence        store)
         store)
             ↓
NODE 5: Detection engine fires against structured store
```

**The dual subscriber pattern is the core innovation.** Two subscribers receive the same message from the publisher. They operate independently. Sub 1 never transforms. Sub 2 does all application work. Sub 1 is the immutable witness. Sub 2 is the replayable projection.

**The raw evidence store (Sub 1's target):**

Write-once key-value store:
```
Key:    merchant_id + payment_network_event_id
Value:  raw_payload (verbatim) + hash (SHA-256) + chain_hash + received_at
```

Write-once enforced by INSERT-only trigger. Hash computed on INSERT. Chain links to previous record. Never updated. Never deleted.

**The bilateral verification claim:**

The hash computed on the raw payload can be compared to the payment network's send log byte-for-byte. If they match, the record is proven unaltered. The raw payload must never be transformed before hashing.

**The upgrade-in-place requirement:**

Sub 2 is a projection of Sub 1. Sub 2 can be replaced, redeployed, or rebuilt from Sub 1's raw store at any time. No rollback. No downtime. The hash chain is never interrupted because Sub 1 is never touched during a Sub 2 upgrade.

**The volume requirement:**

The message queue absorbs spikes. Sub 1 and Sub 2 process at their own pace from the queue. A toy store's Black Friday spike hits the queue, not the database directly. No events lost. No hashes skipped. The system degrades gracefully under load — detection latency may increase, but evidence integrity never breaks.

---

## Your Deliverables — Six Component PRDs

Each PRD follows this structure:

```markdown
# PRD: [Component Name]
**Version:** 1.0
**Owner:** [Jeremy / Tom / as appropriate]
**Depends on:** [list dependencies]
**Gates:** [what this component gates]
**Sprint target:** [Sprint 6 / Sprint 7]

## Purpose
One paragraph.

## Acceptance Criteria
Numbered list. Each AC is binary — pass or fail.

## Test Cases
- Happy path
- Edge cases
- **Toy store spike scenario** (required in every PRD)
- Failure mode

## Integration Points
What this component reads from and writes to.

## Non-functional Requirements
- Throughput
- Latency
- Durability
- Upgrade path

## IP Protection Notes
Flag what must not appear in external documentation.
```

---

### PRD 1: Webhook Receipt + Queue Ingestion
Entry point. Square webhook arrives, HMAC validated, published to queue. No transformation.

Key ACs: signature validated before processing, failed validation never enters queue, raw payload published verbatim, Square event ID idempotency handled, 200 returned to Square within 3 seconds.

Toy store spike: 500 webhooks in 60 seconds. All queued. None dropped. System does not OOM.

---

### PRD 2: Sub 1 — Raw Evidence Store Writer
First subscriber. Reads from queue. Writes verbatim payload. Computes hash on INSERT. Chains to previous record. Never transforms.

Key ACs: payload written verbatim, hash computed by database trigger (not application), chain hash links to preceding record for same merchant_id, write-once enforced, transaction atomicity on failure (no partial writes), key = merchant_id + ':' + payment_network_event_id.

Toy store spike: 500 records written in burst. All hashes correct. Chain integrity verified first to last. No partial writes.

Upgrade-in-place AC: Sub 1 stopped, upgraded, restarted. Events queued during downtime processed on restart. Hash chain continuous.

---

### PRD 3: Sub 2 — Structured Store Writer
Second subscriber. Reads same messages from queue. Parses. Routes to merchant partition. Loads structured store. Triggers detection.

Key ACs: reads from same queue as Sub 1 independently, parses into structured schema fields, routes to correct merchant partition, applies location timezone for partition boundary, failed parse does not affect Sub 1.

Replay AC: given merchant_id and time range, Sub 2 can replay from Sub 1's raw store. Output identical to original processing.

Upgrade-in-place AC: Sub 2 v2 deployed while v1 running. v1 drains. v2 picks up. No events processed twice. No events lost. Sub 1 never touched.

Toy store spike: 500 events queued. Sub 2 processes at sustainable rate. Queue backlog clears within defined SLA. Detection may be delayed but no events lost.

---

### PRD 4: Bilateral Verification Procedure
On-demand forensic procedure. Given an event identifier, retrieve raw evidence record, verify hash, produce evidentiary report.

Key ACs: given payment_network_event_id + merchant_id → retrieve by key, recompute hash independently, compare stored hash to recomputed hash, output structured evidentiary report, procedure is read-only, audit log entry on every invocation.

Test cases: unaltered record (hashes match), simulated tamper (hashes diverge — tamper detected), chain gap (missing record — gap reported).

---

### PRD 5: Replay Procedure
Operational procedure for rebuilding Sub 2's structured store from Sub 1's raw evidence store.

Key ACs: given merchant_id and time range → scan raw evidence store ordered by received_at, feed each payload through current Sub 2 parser, idempotent (running twice produces identical output), read-only against Sub 1, failed parses logged and skipped (do not halt procedure), progress tracking throughout.

Toy store spike: replay 10,000 records for single merchant (full Black Friday dataset). Completes within defined SLA. Output matches original state.

---

### PRD 6: Volume Spike Handling — Queue Backpressure
Cross-cutting behavior specification for system under spike load.

Key ACs: 10x normal volume in 60 seconds — all events enqueued, none dropped, Sub 1 processes at maximum sustainable INSERT rate, Sub 2 processes independently, detection latency degrades gracefully (best effort during spike, return to <2 min within 15 min of spike end), evidence integrity never degrades regardless of backlog depth, no manual intervention required to recover.

Toy store spike (PRIMARY): baseline 100 events/day, spike 5,000 events in 6 hours (50x), expected: all 5,000 in evidence store with valid hashes and chain integrity, canary.orders populated within defined SLA, system returns to normal within 15 minutes, zero operator intervention.

---

### PRD 7: Sub 3 — Ordinal Minter

This is the new sixth node. The product has been fully identified this session. Jeffe is building a universal webhook notarization service. Sub 3 is what makes it universal.

Sub 3 batches recent event hashes, builds a Merkle tree, inscribes the root as an Ordinal on Bitcoin base layer, and maps every event hash back to its position in the tree. One inscription covers thousands of events. Every notarized event is then available in two forms permanently: Canary form (structured, queryable) and Bitcoin form (inscription ID, block explorer URL, trustless, forever).

Key ACs:
- Collects raw_events hashes within defined batch window
- Builds Merkle tree from batch
- Inscribes Merkle root on Bitcoin via Ordinals
- Stores inscription_id + merkle_proof + bitcoin_block against each event in batch
- Returns inscription_id to API caller when block confirms
- Idempotent: inscription failure retried without duplicating inscriptions
- Sub 3 failure does not affect Sub 1 or Sub 2
- Source-agnostic: Sub 3 does not care what the webhook contains, only the hash

Two-response API contract AC:
- Response 1 (milliseconds): hash sealed, chain position assigned
- Response 2 (one Bitcoin block ~10 min): inscription_id, block_number, block_explorer_url

Toy store spike scenario: 5,000 events in 6 hours. All hashes batched and inscribed within defined SLA. No inscriptions lost. No duplicate inscriptions. Bitcoin network unavailability handled gracefully with retry.

Kubernetes readiness: stateless batch worker. Scales independently of Sub 1 and Sub 2. Bitcoin network unavailability does not cascade to Sub 1 or Sub 2.

IP note: the Merkle batching approach, the two-response API contract, and the universal source-agnostic claim are all Crown Jewels. Describe behavior only.

---

## Kubernetes Readiness — Required in Every PRD

Every PRD must include a **Kubernetes Readiness** section. This is non-negotiable. Jeffe's requirement — flex up and down seamlessly, never fail, never roll back, upgraded in place — is only achievable if every component is designed for Kubernetes from day one, even though we are running Docker Compose now.

For each component, answer these questions in the PRD:

**1. Is this component stateless?**
Can Kubernetes kill this pod and restart it on a different node without data loss or chain corruption? If no — explain what state exists and how it is externalized.

**2. Does this component scale horizontally?**
Can we run 3 instances simultaneously without race conditions or duplicate processing? If the component writes to a database, the primary key must be the idempotency guard. Duplicate processing of the same event must be a no-op.

**3. Does this component support rolling deployment?**
Can v1 and v2 run simultaneously during a Kubernetes rolling update? If a schema change makes them incompatible, that is a breaking change — flag it as a deployment gate, not a runtime assumption.

**4. What is the scaling trigger?**
What metric does Kubernetes watch to scale this component up or down?
- Webhook receiver: incoming request rate
- Sub 1 workers: queue depth (raw_events backlog)
- Sub 2 workers: queue depth (canary.orders backlog) — this is the primary autoscale target
- Chirp evaluation: Sub 2 write rate
- PostgreSQL: NOT in Kubernetes. Managed service. Does not autoscale via K8s.

**5. What is the toy store scaling profile?**
Every PRD must state: at 50x normal volume (Black Friday), how many instances of this component are required, and how quickly must Kubernetes provision them to keep the system within its SLA?

**The Kubernetes picture for reference:**

```
Kubernetes cluster (Phase 3)
├── Webhook receiver   — scales on request rate
├── Message queue      — Valkey/Redis Streams (consumer groups required)
├── Sub 1 workers      — stateless, competing consumers, scales on queue depth
├── Sub 2 workers      — stateless, competing consumers, PRIMARY autoscale target
├── Chirp evaluation   — stateless, scales with Sub 2
└── PostgreSQL         — NOT in K8s. Managed service (RDS/Neon).
                         The one stateful component. Lives outside the cluster.
```

The key insight: **the queue is the buffer between elastic compute and stable storage.** Kubernetes scales the workers. The workers drain the queue. The queue absorbs the spike. PostgreSQL never sees the raw spike — it sees a steady, metered write rate from however many worker pods Kubernetes has provisioned. This is how the toy store's Black Friday works without the database falling over.

---

## IP Protection — Before You Write

Crown Jewels check on each PRD:
- No internal schema names in external-facing language (use "evidence store," "structured store," "detection engine")
- No trigger implementation details (describe behavior, not mechanism)
- No hash chain specifics beyond "cryptographic hash chain"
- Flag any AC that reveals threshold values, rule logic, or algorithm details

Each PRD has an IP Protection Notes section. Use it.

---

## What To Read First

1. This prompt
2. `_ALX/WorkOrders/B035_Addendum_TemporalPartition_QueryGovernor.md`
3. `_ALX/WorkOrders/PRD_ChirpConfig_APIGateway_v1.0.md` — PRD format standard
4. PhD's output when available: `_ALX/WorkOrders/output/PhD/PhD_StagedImmutability_PatentSchematic_v1.0.md`

Do NOT read Jeremy's assessment before writing. Write from first principles. Jeremy's numbers populate the non-functional requirement fields when available.

---

## Output Location

`_ALX/WorkOrders/output/Condor/PRD_StagedImmutabilityPipeline/`

Files:
- `PRD_00_Index.md`
- `PRD_01_WebhookReceipt.md`
- `PRD_02_Sub1_EvidenceStore.md`
- `PRD_03_Sub2_StructuredStore.md`
- `PRD_04_BilateralVerification.md`
- `PRD_05_ReplayProcedure.md`
- `PRD_06_VolumeSpikeHandling.md`

---

## Deadline

**End of today.** PhD delivers patent schematic today. Your PRDs feed Jeremy's Sprint 6 planning and Tom's DDL design. Three outputs converge at ALX.

---

## Competitive Context — Why These PRDs Must Be Rock Solid

**CONFIDENTIAL. Do not reference externally.**

Jeffe met directly with Oracle Retail OCI engineers. They could not articulate how they would scale a polling architecture on Oracle Cloud to aggregate feeds from all other clouds.

Oracle is the enterprise incumbent. Their engineers — not the salespeople, the engineers — do not have a credible answer to the scaling problem at the heart of their own architecture.

**What this means for your PRDs:**

The components you are specifying represent an architecture that Oracle has not built and apparently cannot build on their current foundation. The toy store spike scenario in every PRD is not a theoretical edge case — it is the exact problem Oracle's polling architecture cannot solve. A polling system asking "what happened?" across thousands of merchants simultaneously collapses under Black Friday load. Our event-driven dual subscriber pipeline absorbs the spike in the queue and processes it at a metered rate.

Every acceptance criterion you write, every test case you specify, every Kubernetes readiness question you answer is building the evidentiary foundation that this architecture works where Oracle's does not.

Write the PRDs as if they will be read by an expert witness in a patent proceeding. Because they might be.

Full intelligence note: `Canary_IP/Markdown/Strategy/CompetitiveIntel_Oracle_OCI_Polling.md`

---

## Standing Rules

- PhD supervises. Unsure about Crown Jewels — stop, flag to PhD.
- Syd reviews all six PRDs before any go external.
- Jess quality-checks for readability and brand compliance.
- Log session to timelog on close.

---

*ALX | Chief of Staff | February 26, 2026*
*Routes to: Jeremy (Sprint 6) | Tom (DDL) | Syd (patent + IP) | Jess (quality gate)*
