---
type: pitch
domain: business
status: active
created: 2026-03-18
updated: 2026-03-19
---
# The Record Is Broken

Every day, small merchants lose money to internal theft, refund fraud, and cash handling errors. The tools that exist were built for enterprise — expensive, complex, and designed for teams of 50, not teams of 5.

> "We don't want to add to the stress. We want to ease it."

## The Problem

Three fundamental gaps plague every point-of-sale system:

### Polling Gaps
Square webhooks fire on transactions, but the gaps between events are where fraud hides. A void issued 90 seconds after a cash sale. A refund processed during shift change. A loyalty redemption with no matching purchase.

### Mutable Records
Every POS database can be edited. Every audit trail can be altered. If the record lives in a system someone controls, the record can change. That's not proof — that's trust.

### Trust Required
Traditional loss prevention asks you to trust the system, trust the employee, trust the auditor. Canary eliminates the need for trust by making the record immutable, timestamped, and independently verifiable on the Bitcoin blockchain.

## The Solution

**Capture. Seal. Inscribe.**

| Step | What Happens | Time |
|---|---|---|
| Capture | Square webhook fires, event received | T+0ms |
| Seal | SHA-256 hash, PostgreSQL INSERT-only, chain-linked | T+15ms |
| Inscribe | Merkle batch → Bitcoin Ordinal inscription | T+~10min |

Once inscribed, the proof exists forever. No server to shut down. No database to edit. No company to subpoena. The math is the proof.

## The Economy

A closed loop: merchants pay for protection, protection generates sealed events, sealed events become inscriptions, inscriptions generate validation revenue, validation revenue funds more protection.

**Four ownership tiers:**

1. **Merchants** — Pay monthly, get loss prevention + immutable proof
2. **GrowDirect** — Owns the inscription pool, earns validation fees
3. **Validators** — Pay per-query via Lightning L402 to verify any proof
4. **Bitcoin** — The timechain anchors everything permanently

## The Market

**Beachhead:** Square merchants in food & beverage — 2M+ locations, $180B+ annual volume, highest shrinkage rates in retail.

**Why Square first:** Open API, webhook-native, dominant in SMB. One integration covers the entire merchant footprint.

## The Vision

Canary LP is the beachhead. The platform is **elJeffe** — a universal webhook notarization service. Any event, any network, any industry. If it happened, prove it.
