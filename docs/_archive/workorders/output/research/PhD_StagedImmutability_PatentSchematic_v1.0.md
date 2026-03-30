---
type: research
domain: protocol
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Universal Webhook Notarization Patent Schematic
## Staged Immutability Pipeline with Proof-of-Work Base-Layer Anchoring

**Patent Claim (Single Sentence):**
A system and method for universal event notarization via cryptographic hash inscription on a distributed proof-of-work time chain, applicable to any webhook-originated event stream, combining dual/triple subscriber message queueing with write-once immutable evidence storage and Bitcoin-inscribed Merkle tree batching for permanent, trustless verification.

---

## Six-Node Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│ NODE 1: UNIVERSAL WEBHOOK ORIGINATION                                  │
│ • Any network: payment processor, healthcare system, supply chain,      │
│   legal registry, insurance platform, government agency                 │
│ • Raw payload transmitted in standard webhook format                    │
│ • Source-agnostic: protocol-independent event stream                    │
└────────────────────────────┬────────────────────────────────────────────┘
                             │ (raw payload, unmodified)
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ NODE 2: API GATEWAY & QUEUE PUBLICATION                                │
│ • Single point of ingestion                                             │
│ • Publishes to message queue (fan-out point)                            │
│ • Three independent subscribers attached to queue (triple pattern)      │
│ INNOVATION: Decoupled consumption — no cross-dependency                 │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
    ┌─────────────────┐ ┌──────────────┐ ┌─────────────────┐
    │ SUB 1           │ │ SUB 2        │ │ SUB 3           │
    │ (Immutable      │ │ (Parse &     │ │ (Merkle &       │
    │  Evidence)      │ │ Route)       │ │ Ordinal)        │
    └────────┬────────┘ └──────┬───────┘ └────────┬────────┘
             │                  │                  │
             ▼                  ▼                  ▼
┌──────────────────────┐ ┌─────────────┐ ┌──────────────────┐
│ NODE 3: HASH & SEAL  │ │ NODE 4:     │ │ NODE 5/6:        │
│ Write-Once Store     │ │ APPLICATION │ │ BITCOIN          │
│                      │ │ PROJECTION   │ │ INSCRIPTION      │
│ • PostgreSQL         │ │             │ │                  │
│ • Immediate seal     │ │ • Queryable │ │ • Batch Merkle   │
│ • Hash chain links   │ │ • Indexed   │ │   root           │
│   each record to     │ │ • Replayable│ │ • Ordinal        │
│   previous (SHA256)  │ │   from Sub1 │ │   inscription    │
│ • Bilateral verify:  │ │             │ │ • Bitcoin block  │
│   hash vs. network   │ │ • Rebuild   │ │   space custodied│
│   send log           │ │   on deploy │ │   by treasury    │
│                      │ │             │ │                  │
│ IMMUTABILITY: write- │ │ RESILIENCE: │ │ PERMANENCE:      │
│ once, never altered, │ │ derived     │ │ inscribed,       │
│ never deleted        │ │ state       │ │ queryable via    │
│                      │ │             │ │ block explorer,  │
│                      │ │             │ │ no trusted       │
│                      │ │             │ │ intermediary     │
└──────────────────────┘ └─────────────┘ └──────────────────┘
             │                  │                  │
             └──────────────────┼──────────────────┘
                                ▼
                 ┌───────────────────────────────┐
                 │ NODE 6: PERMANENT EVENT       │
                 │ RECORD (DUAL FORM)            │
                 │                               │
                 │ • Application Form            │
                 │   - Structured, queryable     │
                 │   - API-ready, indexed        │
                 │   - Application database      │
                 │                               │
                 │ • Bitcoin Form                │
                 │   - Inscription ID            │
                 │   - Block explorer URL        │
                 │   - Trustless verification    │
                 │   - No trust required         │
                 └───────────────────────────────┘
```

---

## Cryptographic Mechanisms & Novelty vs. Prior Art

### Triple Subscriber Pattern (Core Innovation)

**What it is:**
Three independent message queue subscribers consuming the same raw webhook payload in parallel:
- **Subscriber 1 (Sub 1):** Consumes → immediately hashes → writes once to immutable evidence store → never touched again
- **Subscriber 2 (Sub 2):** Consumes → parses domain-specific fields → routes to application database → queryable, indexed, replayable
- **Subscriber 3 (Sub 3):** Consumes → batches hashes → computes Merkle tree → inscribes root to Bitcoin → produces Ordinal

**Why this is novel:**
- Fan-out messaging alone is not novel. Financial systems use pub-sub.
- Immutable append-only logs are well-known (event sourcing, CQRS).
- **The novelty is the COMBINATION:** Triple subscriber decoupling applied to webhook notarization where each subscriber serves a distinct purpose AND where the evidence store (Sub 1) is cryptographically linked to the Bitcoin base layer (Sub 3) via hash chain and Merkle batching.
- Prior art decouples subscribers but does not anchor the evidence to proof-of-work.

### Hash Chain Immutability (NODE 3)

**Mechanism:**
- Each event hashed with SHA256, using verbatim raw payload (never normalized).
- Each new record includes hash of previous record.
- Forms cryptographic chain: Event N contains hash(Event N-1).
- Chain is per-merchant (not global), so length is bounded and computable.

**Novelty:**
- Hash chains are known (blockchain, Git, merkle trees).
- **The novelty is applying hash chains to write-once webhook evidence** combined with **bilateral verification against the source network's send log.**
- If a merchant disputes a record, the evidence store can prove the exact bytes transmitted, and the network's send log can confirm it sent those exact bytes.

### Bilateral Verification Claim (NODE 3 ↔ SOURCE NETWORK)

**Mechanism:**
- On receipt, Node 3 hashes the raw payload byte-for-byte.
- Merchant/network provides their send log (what they recorded when they sent it).
- Their hash + timestamp is compared to our hash + timestamp.
- Byte-for-byte match = immutable proof both parties saw the same event.
- Mismatch = evidence of tampering or transmission error.

**Novelty:**
- Prior art: webhooks assumed trusted. No notion of cryptographic proof of what was sent vs. what was received.
- **This system treats webhook transmission like financial settlement finality: bilateral verification, not unilateral trust.**

### Ordinal Inscription (NODE 5/6)

**Mechanism:**
- Sub 3 batches hashes from NODE 3 (evidence store).
- Computes Merkle tree root of batch.
- Inscribes root to Bitcoin using Ordinal protocol (~10 min latency).
- Ordinal ID: permanent, immutable, verifiable via any Bitcoin block explorer.
- Each event in batch independently verifiable via Merkle proof path.

**Novelty:**
- Bitcoin inscriptions are known (Ordinal protocol, 2023+).
- **The novelty is applying Ordinal inscription to webhook notarization with a write-once evidence store in Layer 2 (PostgreSQL) and controlling the inscription pool via Layer 1 treasury custody.**
- Competitors cannot recreate this record because they do not control the inscription keys.

### Key Custody Layer (GrowDirect Treasury)

**Mechanism:**
- GrowDirect mints Ordinal pool at formation using treasury keys.
- All inscription operations use keys held in custody by the company.
- No third-party signer required for inscriptions.
- Pool grows programmatically via treasury asset allocation.

**Novelty:**
- **Cryptographic proof of custody.** The company controls the authoritative record of who inscribed what, when.
- Prior art: inscriptions on Bitcoin are quasi-public. **This system asserts that the custodying entity's key material IS the notarization authority.**
- Merchants cannot dispute the inscription because they cannot forge a Bitcoin transaction with someone else's keys.

---

## Why This Combination Is Non-Obvious

### Incumbent Polling Architecture (Competitive Context)

The largest enterprise retail technology platforms globally rely on **polling architecture**:
- Client makes periodic HTTP requests to service asking "do you have data for me?"
- Service waits, buffers, responds to poll.
- No true event-driven notification.
- High latency, high compute cost, weak evidentiary chain.

**Why polling is hard to abandon:**
- Backward compatible with legacy systems.
- No subscription state to manage.
- No queue infrastructure required.
- Feels simpler operationally.

**Why this architecture is a departure:**
1. **Event-driven triple subscriber pattern** requires message queue (RabbitMQ, Kafka, etc.).
2. **Write-once evidence store** requires schema design discipline (no updates, no deletes).
3. **Bitcoin base-layer inscription** requires:
   - Understanding of Ordinal protocol.
   - Bitcoin key management.
   - Fee-market modeling.
   - Block space allocation strategy.
4. **Bilateral verification** requires negotiation with source networks to share their send logs (non-obvious partnership model).

**Non-obviousness summary:**
The event-driven triple subscriber pattern with cryptographic receipt verification and Bitcoin base-layer inscription represents a departure that incumbent practitioners have not achieved. The technical sophistication required to implement hash chains, Merkle batching, Ordinal custody, and bilateral verification across heterogeneous networks exceeds the engineering complexity of polling. The combination is non-obvious because it requires mastery of six distinct domains (distributed systems, cryptography, PostgreSQL design, Bitcoin protocol, Ordinal inscriptions, and commercial partnership architecture). A POSITA (person of ordinary skill in the art) would not be motivated to combine these unless they understood that the moat lies in **permanent, trustless, network-agnostic notarization**, not in faster polling.

---

## Multiple Embodiments

This system applies to any webhook-originated event stream:

1. **Retail** (primary): Transactions, refunds, chargebacks, inventory updates
2. **Healthcare**: Medical record events, prescription fills, insurance claims
3. **Supply Chain**: Shipment updates, custody transfers, quality checks
4. **Legal**: Contract execution, document signing, notarization
5. **Insurance**: Claims events, underwriting steps, payout notifications
6. **Government**: Regulatory events, licensing, public records

Each embodiment has identical architecture; only application database (NODE 4) schema differs.

---

## Key Claims Summary

| Claim | Novel Element | Prior Art Gap |
|-------|---------------|---------------|
| Universal webhook notarization | Event-agnostic, any network | Polling-based incumbents only handle their own events |
| Triple subscriber decoupling | Sub 1/2/3 independent consumption | Fan-out messaging exists but not applied to notarization |
| Write-once evidence store | PostgreSQL with no updates/deletes + hash chain | Immutable logs exist but not with bilateral verification |
| Bilateral verification | Network send log + our evidence hash match | Webhooks assumed trusted; no cryptographic proof |
| Merkle batching + Ordinal | Batch hashes into Merkle root, inscribe to Bitcoin | Inscriptions exist; notarization application is novel |
| Key custody moat | GrowDirect treasury controls inscription pool | No competitor has pre-minted Ordinal pool with custodial keys |
| Permanent, trustless validation | L402-gated access to validation API | No incumbent offers proof-of-work anchored notarization |

---

## Conclusion

This patent covers a system for converting ephemeral webhook events into permanent, cryptographically verified records that require no trust in the notarization service. The combination of write-once evidence storage, hash chain linking, Merkle batching, Ordinal inscription, and bilateral network verification is non-obvious and represents a new category of infrastructure: **trustless event notarization across any network.**

The competitive moat derives from:
1. Key custody of the inscription pool (can't be replicated without treasury assets).
2. Bilateral verification partnerships with source networks (requires commercial relationships).
3. Proof-of-work anchoring (requires Bitcoin block space, which only accrues value over time).

This is patent-eligible subject matter under 35 U.S.C. § 101 (process + machine-readable medium) and claims priority to the date of this application.

**MAXIMUM CONFIDENTIAL**
