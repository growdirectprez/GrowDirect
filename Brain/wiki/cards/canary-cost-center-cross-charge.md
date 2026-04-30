---
date: 2026-04-29
type: founder-intent
status: active
classification: confidential
tags: [cost-center, cross-charge, l402, endpoint-fee, transfer-pricing, ilwac, bitcoin-standard, canary]
last-compiled: 2026-04-29
needs-review: 2026-07-29
---

**Wiki:** [[Brain/Home|Home]] · [[Brain/wiki/cards/ilwac-extended-bitcoin-standard|IL(Device/MCP/Port/)WAC]] · [[Brain/wiki/cards/portable-store-founder-intent|Portable Store — Founder Intent]]

# Canary Cost Center Cross-Charge — Immediate Endpoint Settlement

> **Scope.** Founder intent and architectural direction. Not yet implemented. Captures the design decision before it evaporates. No downstream code or SDD should declare a hard dependency on this until a formal design pass produces a GRO ticket.

---

## The Problem With Cost Allocation Today

Cost allocation in retail IT follows a predictable failure pattern: costs are incurred in real time, allocated in batches at period end, disputed in spreadsheets after the fact, and ultimately smoothed into overhead that nobody owns. The cost center that burned the resource is never accountable in real time because the accounting system is always behind.

---

## The Model

Each endpoint dimension — Device, MCP tool call, Port/connector — carries a fee denominated in satoshis. When a cost center uses an endpoint, the L402 payment settles immediately. No invoice. No batch allocation. No period-end reconciliation.

**The payment is the authorization. The authorization is the charge. The charge flows into that cost center's dimension on the WAC in the same event.**

| Endpoint dimension | What it is | Fee mechanism | Settlement |
|---|---|---|---|
| Device | Terminal, mobile device, hardware | Per-call or per-transaction fee | L402 → cost center wallet, immediate |
| MCP | Agent tool call (which server, which tool) | Per-agent-action compute cost | L402 → cost center wallet, immediate |
| Port | POS connector (Square, Counterpoint, RapidPOS) | Per-event connector license cost | L402 → cost center wallet, immediate |

---

## Cost Center = L402 Wallet

The cost center is not an accounting code. It is a Lightning wallet with a balance.

- **Balance is the real-time P&L position.** No period close required to know where you stand.
- **Overspend is not a policy violation — it is a payment failure.** The endpoint does not respond if the wallet is empty. The constraint is mathematical, not procedural.
- **The budget ceiling is the wallet funding limit.** Finance funds the wallet; the cost center spends it. Refunds are Lightning credits. No journal entries.

---

## Endpoint Fee = Internal Transfer Pricing

The fee schedule is the pricing policy. No separate cost allocation methodology required.

- Want to model a department's true cost of shared infrastructure? Price the endpoint.
- Want to incentivize adoption? Price it low for the first 90 days, then step up.
- Want to penalize low-value agent calls? Raise the MCP fee for that tool category.
- Want to show the true cost of a POS connector? The Port fee is the license cost passed through.

The IT organization that owns the infrastructure sets the fee schedule. The cost centers pay it in real time. No spreadsheet negotiation. No shared-services chargeback disputes.

---

## Franchise Application

A franchisor mandating Canary sets the endpoint fee schedule as a brand standard.

- Franchisee associations control the fee schedule on behalf of their members — same power spectrum as the mandate-vs-association tension mapped in `canary-franchise-play.md`.
- Individual units pay per use at the association-negotiated rate.
- The fee schedule is the brand standard. Compliance is automatic — non-compliant units simply cannot use the endpoints they have not paid for.

---

## Connection to IL(Device/MCP/Port/)WAC

The endpoint fee is not just a billing event — it becomes a cost dimension on the WAC.

When Device, MCP, and Port each carry a fee, those fees flow into the IL(Device/MCP/Port/)WAC recalculation. The cost of the MCP action that authorized an inventory adjustment is part of the provenance-weighted cost of that adjustment. The cost record carries what it cost to produce it.

See: [[Brain/wiki/cards/ilwac-extended-bitcoin-standard|IL(Device/MCP/Port/)WAC — Extended Cost Model on a Bitcoin Standard]]

---

## What Does Not Exist Yet

- Device, MCP, and Port fee schedules (not yet defined)
- L402 wallet per cost center (Goose middleware exists; cost-center scoping not implemented)
- Fee-as-WAC-dimension flow (requires the full IL(Device/MCP/Port/)WAC engine)
- Franchisor fee schedule configuration surface

The design pass that produces GRO tickets for these items has not happened.

---

## Related

- [[Brain/wiki/cards/ilwac-extended-bitcoin-standard|IL(Device/MCP/Port/)WAC]] — the cost model this feeds
- [[Brain/wiki/cards/canary-meter-model-token-plan|Token Plan and Meter Model]] — the account-level billing layer above cost center
- [[Brain/wiki/canary-franchise-play|Franchise Play]] — franchise fee schedule application
- `docs/sdds/canary/goose.md` — L402 payment middleware (the settlement mechanism)
- `docs/sdds/canary/raas.md` — namespace that owns the portable cost record
