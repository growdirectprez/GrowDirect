---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Work Order: B-052 — Sprint 6 Parallel Tracks
*Issued by: ALX | February 27, 2026 | Approved by: Jeffe*
*Classification: INTERNAL — MAXIMUM CONFIDENTIAL*

---

## Decision

**Jeffe directive (Feb 27):** Sprint 6 runs two parallel tracks. Protocol proof AND Canary beachhead. Neither waits for the other.

**The investor story:** "Watch me buy a coffee. Watch me return it. Watch Canary flag it. Watch the evidence get sealed. Watch it land on Bitcoin. Here's the TX ID — go verify it yourself. That record exists forever."

---

## Track 1: Protocol Pipe — End-to-End Evidence on Chain

**Objective:** One webhook → one seal → one inscription → one TX ID on mainnet. The smallest thing that proves the protocol.

**The full vertical slice:**

```
1. MERCHANT CONNECTS (OAuth)
   Merchant → Square OAuth 2.0 → Canary gets access token
   Phase 1: Jeffe authorizes GrowDirect's own Square app (self-auth)

2. ORDER FEED (Webhooks)
   Square fires webhooks → Canary API gateway receives:
   - payment.completed
   - order.updated
   - refund.created

3. CHIRP RULE (Flag)
   Refund received → amount > $10 → FLAG
   One rule. The simplest one.
   Output: flagged event with merchant_id, amount, timestamp, employee_id

4. EVIDENCE SEAL (PostgreSQL — Sub 1)
   Flagged event → SHA-256 hash of full payload
   → INSERT into fox_evidence
   → previous_chain_hash links to last entry (hash chain)
   → Immutability triggers prevent UPDATE/DELETE
   STATUS: ALREADY BUILT (Sprint 5, 22 triggers verified)

5. BITCOIN INSCRIPTION (Sub 3)
   Batch sealed hashes → Merkle tree
   → Inscribe Merkle root into GrowDirect Ordinal pool
   → Map each event hash to its Merkle position
   → Return: inscription_id, block height, TX ID

6. RECEIPT
   Return to caller:
   - "Refund of $14.50 flagged at 2:31 PM"
   - "Evidence sealed: hash abc123..."
   - "Bitcoin proof: TX [txid], Block 884,201"
   - Block explorer link (mempool.space)
```

### Build Matrix — Track 1

| # | Component | Exists? | Owner | Work Required |
|---|---|---|---|---|
| 1 | Square OAuth 2.0 flow | No | Jeremy | New — Square SDK well-documented. Self-auth for Phase 1. |
| 2 | Webhook receiver + signature verification | Partial | Jeremy | API gateway skeleton exists. Add Square webhook signature verification. |
| 3 | Chirp rule: refund > $10 | Yes | Jeremy | Rule engine exists. Wire one rule to live webhook data. |
| 4 | Evidence seal (Sub 1) | **Yes — DONE** | — | PostgreSQL hash chain + immutability triggers. Sprint 5 complete. |
| 5 | Inscription bridge (Sub 3) | No | Jeremy | OrdinalsBot API Phase 1 (per B-041 assessment). Valkey Streams queue. |
| 6 | Receipt/return endpoint | No | Jeremy | Thin — TX ID + block explorer URL + sealed hash reference. |

### Dependencies

- **B-032 (Square Developer + Merchant accounts)** — Jeffe, ~30 min. GATES BOTH TRACKS.
- **B-041 (OrdinalsBot API assessment)** — Jeremy delivered. Ready to build.
- **B-048 (card_fingerprint scope)** — Not required for Track 1 MVP. Runs in parallel.

### Demo Environment

Runs on the QA iMac (192.168.10.117). Same box as the existing demo stack.

**Testnet first.** Mainnet inscription only after testnet proves the pipe works end-to-end.

### Estimate

Jeremy: 1-2 weeks for the three new components (OAuth, webhook verification, inscription bridge). Middle of pipe is done.

---

## Track 2: Canary Slim — Beachhead Momentum

**Objective:** Keep the merchant-facing product moving without overloading Sprint 6.

### Scope (trimmed from original Sprint 6)

| # | Deliverable | Owner | Status |
|---|---|---|---|
| 1 | B-032: Square Developer + Merchant accounts | Jeffe | 30 min signup — GATES EVERYTHING |
| 2 | B-036: Square SDK → CRDM alignment audit | Jeremy | Work order written, ready to execute |
| 3 | Chirp Config MVP: one config page, one merchant, one webhook type | Art (design) + Jeremy (build) | Trimmed from full PRD scope |
| 4 | Jim dry-run on existing demo stack | Jim | Demo stack live at 192.168.10.117:5002 |

### Deferred to Sprint 7

- Full API Gateway (multi-merchant)
- Full Chirp Config (all webhook types)
- Kubernetes deployment
- Multi-tenant partition implementation

---

## The Gate

**B-032 unlocks both tracks.** Track 1 needs a real webhook. Track 2 needs the SDK to validate against. Jeffe's 30-minute Square signup is the single dependency.

---

## Routing

| Agent | Track | Action |
|---|---|---|
| **Jeffe** | Both | B-032: Square Developer + Merchant account signup. This week. |
| **Jeremy** | Track 1 | Build the protocol pipe: OAuth → webhook verification → inscription bridge. Testnet first. |
| **Jeremy** | Track 2 | B-036 SDK alignment audit (can run in parallel with Track 1). |
| **Art** | Track 2 | Chirp Config MVP — one page, one merchant. Minimal viable design. |
| **Jim** | Track 2 | Dry-run existing demo stack. Validate smoke test still passes after Track 1 integration. |
| **Tom** | Advisory | Available for schema questions if Track 1 surfaces CRDM gaps. |

---

*ALX | Chief of Staff | February 27, 2026*
*Supersedes: original Sprint 6 scope*
*Reference: ElJeffe_BusinessModel_Addendum.md, B-041 Jeremy assessment, B-036 SDK alignment work order*
