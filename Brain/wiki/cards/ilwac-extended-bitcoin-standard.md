---
date: 2026-04-28
type: founder-intent
status: active
classification: confidential
tags: [ilwac, bitcoin-standard, satoshi, rib, mcp, provenance, cost-accounting, founder-intent, canary]
last-compiled: 2026-04-28
needs-review: 2026-07-28
---

**Wiki:** [[Brain/Home|Home]] · [[Brain/wiki/cards/platform-thesis|Platform Thesis]] · [[Brain/wiki/cards/portable-store-founder-intent|Portable Store — Founder Intent]]

# IL(Device/MCP/Port/)WAC — Extended Cost Model on a Bitcoin Standard

> **Scope.** Founder intent and architectural direction. Not a sales claim. Not yet implemented. Captures the design decision before it evaporates. No downstream code or SDD should declare a hard dependency on this until a formal design pass produces a GRO ticket.

---

## The Claim

No one has this.

Retail cost accounting has always been fiat-denominated, device-agnostic, and channel-blind. A unit cost is a number in dollars, attached to an item and a location, updated when a PO is received. That is ILWAC as the industry knows it.

This is not that.

---

## The Bitcoin Standard

**Canary retail is on a Bitcoin standard. Everything else is an abstraction.**

Satoshi is the native monetary denominator at the system level. Fiat prices — the dollar amounts on receipts, on purchase orders, on the OTB budget — are the display layer. The accounting layer runs in satoshis.

This is not cosmetic. It has structural consequences:

- L402 Lightning payments are already denominated in satoshis. The payment loop and the cost loop close in the same unit. No currency conversion at the system level. No exchange rate embedded in the cost model.
- OTB wallets are funded in satoshis. The constraint is a Lightning wallet balance, not a number in a database. Overspending is not a policy violation — it is a payment failure. Mathematically impossible, not merely prohibited.
- COGS postings to Module F run in satoshis. Fiat equivalents are computed at the presentation layer using the exchange rate at the time of the event — the same way Bitcoin-standard accounting works in every other domain that has adopted it.
- The cost loop (receipt → ILWAC recalculate) and the payment loop (L402 → Lightning settlement) are now denominated in the same unit. The closed loop economy is internally consistent at the monetary level.

The enterprise retail world runs on fiat with all the currency risk, conversion complexity, and accounting abstraction that implies. Canary runs on satoshis. Fiat is the abstraction.

---

## The RIB Extension

**RIB = Retail Inventory Batch.** The Retek/Oracle RMS concept: inventory adjustment events are not processed individually at the time they occur — they are batched, validated, and posted as structured messages to the stock ledger in domain-organized runs.

The extension: **batched JSON RIB messages, organized by domain, rolled up into the extended WAC calculation.**

Instead of individual events firing ILWAC recalculates in real time, each domain (T, V, M, D, and others in the spine) produces structured RIB messages — JSON batches of inventory adjustment events scoped to that domain. Those batches are the inputs to the WAC recalculation.

The domain organization matters. A receiving event from Module M (Merchandising) carries different provenance than a transfer adjustment from Module D (Distribution) or a sale event from Module T (Transaction). The RIB message carries its domain origin. The WAC calculation knows where the adjustment came from.

SHA-256 seals each batch. The batch is tamper-evident before it touches the cost model.

---

## IL(Device/MCP/Port/)WAC

Standard ILWAC: **Item × Location × Weighted Average Cost.**

Extended: **Item × Location × Device × MCP × Port × Weighted Average Cost.**

| Dimension | What it captures |
|---|---|
| **Item** | The SKU — unchanged from standard ILWAC |
| **Location** | The store or warehouse — unchanged from standard ILWAC |
| **Device** | The terminal, mobile device, or hardware that processed the originating event |
| **MCP** | The MCP tool call that authorized the action — which agent, which server, which tool |
| **Port** | The POS connector — Square, Counterpoint, Lightspeed, or any future source |
| **WAC** | Weighted average cost — recalculated on every RIB batch, denominated in satoshis |

This is **provenance-weighted cost.** The cost carries its own audit trail — not appended as metadata, but embedded as dimensions in the calculation itself. The WAC for an item at a location is not one number. It is a vector: one value per (Device, MCP, Port) combination that has contributed to the cost basis.

**Why this matters:**

- A receiving event processed through the Counterpoint connector on a fixed POS terminal authorized by the `register_source` MCP tool produces a different provenance signature than the same event processed through the Square connector on a mobile device authorized by a different tool. The cost model tracks both — and the difference is auditable.
- When a Fox case investigation needs to trace a cost anomaly, the provenance dimensions tell the investigator not just what the cost was, but how it was established, by which channel, through which agent action.
- SHA-256 seals the RIB batch that produced the WAC update. The cost is not just a number — it is a hashed, domain-attributed, provenance-stamped value anchored to the event that created it.

---

## The Full Stack

```
Event occurs (sale, receipt, transfer, adjustment)
  → Domain RIB batch assembled (JSON, domain-tagged)
  → SHA-256 seals the batch
  → IL(Device/MCP/Port/)WAC recalculates in satoshis
  → L402 gates any spend authorized by the new cost basis
  → RaaS namespace owns the updated cost record
  → Merchant takes the cost history with them when they leave
```

Every step is hashed. Every authorization is paid. Every cost is receipted. Every record is portable.

---

## Commercial Implications

The IL(Device/MCP/Port/)WAC model generates three downstream commercial mechanisms. Each has its own standalone card:

- **[[Brain/wiki/cards/canary-cost-center-cross-charge|Cost Center Cross-Charge]]** — each endpoint dimension carries a satoshi-denominated fee that settles immediately via L402. Cost center = L402 wallet. Balance is real-time P&L. No period-end allocation.
- **IT Project Self-Funding** — covered in [[Brain/wiki/cards/canary-meter-model-token-plan|Token Plan and Meter Model]]. Project costs (endpoint fees) and project results (ILWAC improvements, Fox recoveries) are in the same unit, on the same system, sealed by the same hash chain. The ROI model is a wallet balance.
- **[[Brain/wiki/cards/canary-meter-model-token-plan|Token Plan and Meter Model]]** — every account gets a fixed token allocation and L402 budget ceiling. The variable meter runs on one ratio only: payroll to revenue. Platform revenue is aligned with merchant operational efficiency.

---

## What Does Not Exist Yet

This is architectural direction, not current implementation. What exists today:

- ILWAC (Item × Location × WAC) in Module V — functional, documented in `Canary/docs/sdds/v2/module-v.md`
- Satoshi-cost-accounting as a CATz substrate primitive — documented
- RaaS namespace resolution — functional, documented in `docs/sdds/canary/raas.md`
- SHA-256 hash chain in Sub 1 — functional, documented in `Canary/docs/sdds/v2/webhook-pipeline.md`
- L402 middleware (Goose) — documented in `docs/sdds/canary/goose.md`

What does not exist yet:

- The Device, MCP, and Port dimensions added to the WAC calculation
- Batched JSON RIB message format by domain
- Satoshi denomination at the system accounting level (currently fiat, with satoshi as a parallel substrate)
- The unified IL(Device/MCP/Port/)WAC recalculation engine

The design pass that produces GRO tickets for these items has not happened. This note is the record that the vision exists and the direction is set. The implementation follows a formal architecture session.

---

## Why No One Has This

Standard retail cost accounting:
- Fiat-denominated (dollar risk embedded in the cost model)
- Device-agnostic (no record of which terminal processed the event)
- Channel-blind (Square events and Counterpoint events produce identical WAC inputs)
- Agent-invisible (no record of which system authorized the cost-affecting action)
- Batch-less (most modern systems process individual events, losing the domain-organization benefit of RIB)

IL(Device/MCP/Port/)WAC on a Bitcoin standard:
- Satoshi-denominated (fiat is the display layer)
- Device-aware (terminal is a cost dimension)
- Channel-aware (POS port is a cost dimension)
- Agent-aware (MCP tool authorization is a cost dimension)
- RIB-batched by domain (domain origin is preserved and hashed)

The combination does not exist in any retail cost model in production today.

---

## Related

- [[Brain/wiki/cards/portable-store-founder-intent|Portable Store — Founder Intent]] — the vision this cost model serves
- [[Brain/wiki/cards/platform-thesis|Platform Thesis — Every Entity Has a Meter]] — the accountability model
- [[Brain/wiki/cards/canary-cost-center-cross-charge|Cost Center Cross-Charge]] — endpoint fee → immediate L402 settlement; cost center as wallet
- [[Brain/wiki/cards/canary-meter-model-token-plan|Token Plan and Meter Model]] — account-level billing; payroll/revenue meter; IT project self-funding
- [[Brain/wiki/canary-raas-positioning|Canary RaaS — Positioning Guardrail]] — audit constraints on cryptographic claims
- `Canary/docs/sdds/v2/module-v.md` — current ILWAC implementation (Item × Location)
- `Canary/docs/sdds/v2/module-i.md` — Item master; vendor cost as input to V (I.9.2)
- `docs/sdds/canary/raas.md` — namespace resolution that owns the portable cost record
- `docs/sdds/canary/goose.md` — L402 payment middleware
- Canary-Retail-Brain: `platform/satoshi-cost-accounting.md` — existing substrate primitive
- Canary-Retail-Brain: `platform/satoshi-precision-operating-model.md` — existing substrate primitive
