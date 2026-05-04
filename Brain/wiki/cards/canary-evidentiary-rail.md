---
last-compiled: 2026-05-04
needs-review: false
type: reference
status: active
tags: [canary, evidentiary, blockchain, audit, accountability, functional-requirements, architecture]
created: 2026-05-04
---
last-compiled: 2026-05-04
needs-review: false

# Canary — Evidentiary Rail

The Evidentiary Rail is Canary's third accountability rail (alongside Operational and Financial). Every inventory event, every POS transaction, every task completion, every receiving record, every range decision — each gets a cryptographic hash anchored on a public blockchain. The result: an immutable audit chain that no party can alter unilaterally, including Canary itself.

This is not a compliance feature. It is the commercial differentiation. An operator can prove, to anyone, what happened in their store, when, and in what sequence. A supplier can verify that a receiving quantity was logged accurately. An insurer can verify that inventory controls were in place. A lender can verify revenue and inventory patterns. An acquirer can verify the accuracy of operational records. No enterprise WMS offered this. No SMB tool offers this.

---
last-compiled: 2026-05-04
needs-review: false

## The Problem It Solves

**For the operator:** when there's a dispute — with a supplier about a short shipment, with an insurer about a theft claim, with a lender about inventory levels — the operator needs an indisputable record. Spreadsheets can be edited. POS reports can be regenerated. Database records can be altered. A blockchain anchor cannot.

**For the channel:** Bart's VAR operation delivers Canary to merchants. When a merchant asks "can I trust this system's records?", the answer is: the records are anchored on a public chain. Anyone can verify them. The merchant holds the keys. Canary doesn't control the record — it created it, hashed it, and anchored it. Even if Canary disappears tomorrow, the record exists.

**For compliance:** at Phase 4 (full SaaS data steward), Canary will be under SOC 2 and potentially ISO 27001 scrutiny. The evidentiary rail is the architectural foundation for demonstrating data integrity — not just policy claims, but a verifiable cryptographic record.

---
last-compiled: 2026-05-04
needs-review: false

## The Four-Tier Storage Model

Every Canary data event flows through a four-tier storage architecture:

```
S1 — Hot (operational)
  PostgreSQL (Canary Go DB)
  → Live queries, real-time dashboard, task queue, SOH
  → Retention: 90 days

S2 — Warm (recent history)
  Cloudflare R2 or GCP Cloud Storage (structured)
  → Analytics queries, trend data, month-over-month
  → Retention: 2 years

S3 — Cold (archive)
  GCP Cloud Storage (compressed, encrypted)
  → Long-term archive, audit trail
  → Merchant holds the encryption key — Canary holds the data
  → Retention: 7 years (meets IRS + most commercial audit requirements)

S4 — Chain (permanent)
  Public blockchain (Bitcoin L2 — Lightning or Ordinals for data anchoring)
  → Hash of S3 blob per batch
  → Immutable, permanent, permissionless to verify
  → No data on chain — only the hash (privacy preserved)
```

**The merchant's posture:** the merchant's data is in S3 (encrypted with their key). The proof that the data is unchanged is on S4 (the hash). Canary can't see the plaintext data without the merchant's key. And the merchant can verify, independently, that Canary hasn't modified the data by checking the S4 hash against the S3 blob. This is the "custodian of flow, not observer of content" architecture referenced in the platform thesis.

---
last-compiled: 2026-05-04
needs-review: false

## What Gets Hashed

Not every database write needs to be hashed — that would be computationally expensive and produce an unmanageable volume of chain transactions. The hash is applied at the **event batch** level.

**Hashed event categories:**

| Category | Batch frequency | Examples |
|---|---|---|
| POS transactions | End of day | All sales, returns, voids for the day |
| Receiving records | Per PO close | All scanned quantities for a completed PO |
| SOH adjustments | Per shift | Cycle count results, damage disposals, manual adjustments |
| Task completions | Per shift | Who completed what, when, exceptions logged |
| Range changes | Per event | Item activated, phased out, location changed |
| Planogram implementations | Per event | Which planogram, when implemented, who confirmed |
| Order submissions | Per event | PO submitted to supplier, quantities, transmission method |

**Batch structure:**

```
Daily batch record (example):
{
  "batch_id": "uuid-v4",
  "store_id": "store-001",
  "date": "2026-05-04",
  "event_types": ["pos.sale", "pos.return", "pos.void"],
  "event_count": 847,
  "event_merkle_root": "sha256:a3f7c...",
  "created_at": "2026-05-05T00:01:23Z"
}
```

The Merkle root is a single hash that summarizes all 847 events in the batch. If any single event is altered, the Merkle root changes. The Merkle root is what gets anchored on the blockchain — not the raw events (which stay in S3, encrypted).

---
last-compiled: 2026-05-04
needs-review: false

## The Chain Anchor

**Why Bitcoin L2?** Bitcoin's base layer (L1) is the most secure, most decentralized public blockchain. L2 (Lightning Network, Ordinals/Taproot, or Bitcoin-native timestamp services like OpenTimestamps) provides:
- Lower transaction cost (not $5–50 per anchor like L1 in congested conditions)
- Faster finality for timestamp purposes
- Verified anchoring back to Bitcoin L1 security

The specific L2 mechanism is TBD in implementation — OpenTimestamps is the simplest for pure hash-anchoring (it batches hash submissions and anchors to Bitcoin L1 via merkle tree). The key requirement: anyone can verify the anchor without trusting Canary.

**Verification UX for the merchant:**

```
Audit Verification — Canary

Store: [Store Name]
Period: May 4, 2026

Batch: pos_transactions_2026-05-04
  Events: 847
  Hash: a3f7c8d2e1...
  Anchored: 2026-05-05 00:08:41 UTC
  Block: Bitcoin block #895,241
  [Verify on chain →]  (opens block explorer)

Receiving record: PO #12847
  Items received: 14 lines, 48 cases
  Hash: 9b2e1f4a7c...
  Anchored: 2026-05-04 14:22:17 UTC
  Block: Bitcoin block #895,231
  [Verify on chain →]
```

The merchant can click "Verify on chain" and independently confirm that the hash recorded in Canary matches what's on the Bitcoin blockchain. No trust required. If Canary modified the record, the hash would change and the verification would fail.

---
last-compiled: 2026-05-04
needs-review: false

## Functional Implications — What the Rail Enables

**Supplier dispute resolution:**
"Your delivery was 40 cases, not 48." The operator opens Canary, pulls the receiving record for that PO, and shows the blockchain-verified log: 48 cases scanned, each confirmed by the associate at [timestamp]. The anchor is the evidence. Disputes resolve faster and more clearly when there is an immutable record both parties can verify.

**Insurance claims:**
A theft event is logged as a cycle count discrepancy with a shrinkage reason code. The sequence of events (last SOH record, the discrepancy, the timestamp, the associated POS records from the same period) is all anchored. An insurance adjuster reviewing a claim can verify that the records are unaltered — Canary didn't create the theft log after the claim was filed. The record predates the claim, cryptographically provable.

**Lender / investor diligence:**
An operator seeking a line of credit or SBA loan can share an audit report generated by Canary: inventory levels, sales velocity, days-of-stock, supplier reliability — all backed by blockchain-anchored records. The lender is not taking the operator's word for it. The records are verifiable.

**Regulatory compliance:**
If a regulatory authority (FDA for food safety, state alcohol control board for a liquor section, any trace-and-recall requirement) needs to verify when a specific product lot was received, where it was stored, and when it was sold — Canary's evidentiary chain provides that record with cryptographic integrity.

---
last-compiled: 2026-05-04
needs-review: false

## The Satoshi Billing Connection

The evidentiary rail and the satoshi billing model are the same mechanism viewed from different angles.

Every event that traverses a Canary MCP junction pays a satoshi toll. That toll payment is itself a blockchain transaction — it IS the anchor. The billing and the evidentiary record are generated by the same act: a transaction on the Bitcoin L2 network.

This is architecturally elegant and commercially significant. The merchant isn't paying extra for the audit trail — the audit trail is the billing mechanism. Every satoshi paid is a proof of event. The cost-to-serve model and the evidentiary model are unified.

**Example:**

```
Event: pos.sale processed
Junction toll: 1 satoshi (~$0.00001 at current rates)
Transaction ID: b7e3a2...
Timestamp: 2026-05-04T10:32:19Z

This transaction ID is both:
  - The billing record for the event
  - The anchor for the evidentiary trail
```

At scale, this produces a self-funding, self-verifying audit trail where the cost of verification is embedded in the cost of operation. No separate "audit service." No separate "compliance module." The evidentiary rail is the commercial model running.

---
last-compiled: 2026-05-04
needs-review: false

## Privacy Architecture

**What is NOT on chain:** raw data — item names, quantities, prices, customer information, employee activity. All of that is in S3, encrypted with the merchant's key.

**What IS on chain:** hashes. A hash reveals nothing about the underlying data. The blockchain anchor proves that a specific set of data existed at a specific time and has not been altered. It does not expose the contents.

**The merchant's key:** the merchant holds the encryption key for their S3 data. Canary holds the ciphertext. If the merchant leaves Canary, they take their key, they can decrypt their data, and Canary retains only the ciphertext (useless without the key). This is a meaningful data portability guarantee — unusual in SaaS, important for operator trust.

**The "el jefe" agent principle:** Canary operates as the merchant's agent — processing data on their behalf, not analyzing it for Canary's benefit. The MCP junction architecture is designed so that event payloads are processed and hashed without Canary holding a cleartext copy beyond the operational window (S1 → encrypted S3 transition). Canary is the custodian of flow, not the owner of content.

---
last-compiled: 2026-05-04
needs-review: false

## Build Sequence for the Evidentiary Rail

The rail should be live from day one — not deferred to Phase 3. The reason: if it's added later, you have a gap in the evidentiary record that cannot be filled retroactively. The blockchain anchor only works if it's continuous. A chain with a gap is a chain that can be questioned.

1. **Event hashing** — every inbound event (POS sale, receiving scan, task completion) gets a SHA-256 hash at ingestion. Stored in S1 alongside the event record.
2. **Daily batch aggregation** — end-of-day job aggregates daily events into a Merkle tree; root stored as the day's batch hash.
3. **S3 archival** — batch encrypted with merchant key, written to S3.
4. **Chain anchor** — batch hash submitted to Bitcoin L2 via OpenTimestamps or equivalent. Anchor transaction ID stored in Canary DB.
5. **Verification UI** — merchant can query any batch by date, see the hash, see the anchor, click through to block explorer.

Steps 1–2 can ship in Wave 1. Steps 3–5 follow in Wave 2. The hash infrastructure should be in from day one even if the chain anchor lags by one wave.

[[Brain/wiki/cards/store-ops-capability-model]] · [[Brain/wiki/cards/canary-android-pos-integration]] · [[Brain/projects/Canary]]
