---
type: pitch
domain: tsp
status: active
created: 2026-03-18
updated: 2026-03-19
---
# The Triple Subscriber Pipeline
*Spine: ACT 5B | Manifesto: V.2*

**Status:** 📝 DRAFT — Extracted from Condor PRDs TSP-01 through TSP-09 + Manifesto V.2. Awaiting Jeffe review.

---

## Three Subscribers. One Queue. Competing Consumers.

Every event that enters elJeffe's pipeline — every Square webhook, every healthcare encounter, every supply chain handoff — passes through a single durable message queue and fans out to three independent subscribers. Each subscriber has a different job. Each operates independently. Each can fail without affecting the others.

- **Sub 1 (Hash & Seal):** The evidence writer. Receives the raw payload, computes a SHA-256 hash on the unnormalized bytes, and writes the event to an append-only PostgreSQL evidence store. Every record is INSERT-only — no updates, no deletes, triggers enforced at the database level. Each record's chain hash links cryptographically to the previous entry, creating an unbroken sequence per merchant. This is the immutable witness. It happens in milliseconds.

- **Sub 2 (Parse & Route):** The application writer. Parses the raw event into structured fields and routes them to the CRDM — the queryable retail data warehouse that powers dashboards, detection rules, and Chirp alerts. This store is mutable by design. It can be replayed from Sub 1's evidence store at any time. If the schema changes, if a parser improves, if a disaster strikes — replay from the evidence chain and reconstruct the application layer from scratch.

- **Sub 3 (Merkle & Ordinal):** The Bitcoin inscription engine. Accumulates event hashes into batches, builds a Merkle tree, and inscribes the root as an Ordinal on the Bitcoin time chain. Each individual event is independently verifiable via its Merkle proof path — a set of sibling hashes that lets anyone recompute the root from a single leaf. The inscription makes the batch permanent. Bitcoin confirms in approximately ten minutes.

## Why Three Subscribers Matter

The triple subscriber pattern separates three concerns that traditional systems conflate: evidence integrity, application utility, and permanent anchoring.

Sub 1 is the legal witness. It proves what was received, byte for byte, in the order it was received. It cannot be rebuilt because it IS the source of truth.

Sub 2 is the business layer. It makes the data useful — searchable, queryable, alertable. It can be rebuilt entirely from Sub 1 because it is derived, not original.

Sub 3 is the anchor. It makes the record permanent beyond GrowDirect's own infrastructure. Even if every GrowDirect server were destroyed, the Merkle roots on Bitcoin would prove what events were notarized at what times.

No single subscriber is the system. The system is the combination — and the combination is the novel architecture protected by the patent.

## Stateless. Scalable. Kubernetes-Ready.

Each subscriber is stateless and horizontally scalable. The queue is the contract between them. Subscribers compete for messages within their consumer group. No single point of failure exists. If a subscriber pod crashes, another picks up the next message. The queue guarantees at-least-once delivery. Idempotency handling in each subscriber ensures exactly-once semantics at the application level.

The infrastructure runs on Kubernetes. Scaling is automatic. The bottleneck is Bitcoin's ten-minute block time — and that is by design, not by limitation.

---

**Source:** Condor PRDs TSP-01 through TSP-09 + Manifesto V.2
**Manifesto tag:** `Manifesto: V.2`
**Filled:** February 27, 2026 — ALX (B-059 Phase 1)
