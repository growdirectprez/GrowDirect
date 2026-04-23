---
date: 2026-04-21
type: wiki
tags: [secure, omnichannel, appriss, ecommerce, bopis, boris, fraud-detection, canary-lineage]
sources:
  - Brain/raw/inbox/secure-omnichannel-overview-oct2018-pdf.md
  - Brain/raw/inbox/appriss-retail-data-specification-v1-1-pdf.md
  - Brain/raw/inbox/5-1-requirements-xlsx.md
  - Brain/raw/inbox/kroger-dsd-requirements-docx.md
last-compiled: 2026-04-21
needs-review: 2026-05-05
---

**Wiki:** [[Brain/Home|Home]]

# Secure Omnichannel

## Summary

Secure Omnichannel (Fall 2018) extended Secure from in-store post-transaction analytics into **ecommerce loss prevention** — the risk areas that open up after the "buy" button for retailers with multi-channel presence. Target patterns: Buy Online Return In-Store (BORIS), Buy Online Pickup In-Store (BOPIS), order cancellation from store-fulfilled orders, returns of off-range products, fictitious damaged/missing goods, resellers hoarding stock, and collusive store-associate fraud in the pickup flow. The data surface widened accordingly — the Appriss Retail Data Specification v1.1 documents the schema Secure Omnichannel expected.

## Details

### The omnichannel problem

In-store LP worked on POS transactions. Omnichannel retail introduced a second transaction type: the ecommerce order, with distinct steps (purchase, pick, pack, ship or reserve-for-pickup, receive, return). Each step exposes its own fraud surface. The classic EBR exception patterns — refund without receipt, void at register, employee purchase at discount — don't translate directly. Omnichannel needed new detection logic and new data inputs.

### Order flow + fraud surfaces

Source doc diagrams the flow:

```
Consumer:  Purchase → (ship or pickup option)
Retailer:  Process Order → Ship | Hold for Pickup
Consumer:  Receive → Keep | Return (in-store / call center / online) | Cancel
```

Each arrow is a fraud vector:

| Surface | Pattern |
|---|---|
| Purchase | Synthetic-identity purchases, stolen card, reseller bulk orders |
| Ship | Lost-in-shipping claims, porch-piracy claims for never-ordered goods |
| In-store pickup (BOPIS) | Collusive associate fraud — "customer never showed up" + employee takes the goods |
| In-store return (BORIS) | Buy online with stolen card → return in-store for store credit |
| Call-center / online return | Fictitious damage claims, empty-box returns, wardrobing |
| Cancel | Cancel after the item is held / shipped → shrinkage + payroll cost |

Plus the human-behavior surfaces:
- Associates colluding with external actors
- "Divorce customer" framing: some customers cost more than they contribute (frequent fraudulent returns, habitual policy abuse)
- Wardrobing / renting (buy, use, return as "unworn")
- Reseller stock-hoarding (BOPIS reservations blocking real inventory)

### Inbound / Fulfillment / Outbound taxonomy

The source doc groups all shrink sources under a three-stage process model:

- **Inbound** — warehouse shipments, vendor-direct-to-site, positive adjustments
- **Fulfillment** — sales, transfers to store/DC, internal theft, waste
- **Outbound** — customer returns (in-store, online, call center), return to vendor, negative adjustments, website metrics

Secure Omnichannel's detection targets every one of these. This three-stage decomposition is a durable way to think about retail shrink — Canary could adopt it as an organizing framework for its own detection-rule taxonomy.

### Data requirements (Appriss Retail Data Specification v1.1)

The Appriss Retail Data Specification v1.1 (Sept 2018) documents the full schema Secure Omnichannel expected from retailers. Source types covered: POS transaction, ecommerce order, fulfillment event, return event, inventory movement, employee action, customer identity. This spec is the **schema contract that CRDM materializes** — retailer data must land here to be usable by Secure detection.

(Full schema extraction is deferred — the intake is at `Brain/raw/inbox/appriss-retail-data-specification-v1-1-pdf.md`. A future Canary-specific extraction pass should compare field-by-field against Canary's current schema to surface gaps.)

### 5.1 Requirements workbook

The `5.1 Requirements.xlsx` workbook catalogs Secure 5.1 functional requirements — the pre-release scope for the 5.1 version. This is raw FR material: module-by-module requirements with ACs, which is directly usable as source for Canary SDD-level writing.

(Full requirements are in the intake at `Brain/raw/inbox/5-1-requirements-xlsx.md`. Candidate for deeper extraction during a Canary SDD-writing pass.)

### DSD requirements (top-5 grocery chain)

The `Kroger DSD requirements.docx` intake (top-5 US grocery chain) is the concrete spec for Direct Store Delivery — a specific omnichannel adjacency where vendor trucks deliver inventory directly to stores, bypassing the DC. This creates its own fraud surface: vendor-driver collusion with store receivers, shorted deliveries, damaged-goods claims. The doc is a worked example of how Secure extended its base model to a retailer-specific workflow.

See [[Brain/wiki/secure-client-top5-grocery-chain|Secure Client: Top-5 Grocery Chain]] for the full grocery-chain deep-dive.

### What this teaches Canary

- **Ecommerce is its own fraud surface.** In-store POS fraud detection does not generalize to BOPIS/BORIS/cancel. Canary's current detection is POS-focused; the omnichannel surface is an expansion vector when Canary moves beyond pure-retail Square merchants into merchants with ecommerce + pickup flows.
- **Inbound / Fulfillment / Outbound as rule taxonomy.** Classic retail shrink decomposition. Canary's Chirp rule grouping could adopt this structure to make rule intent legible to operators.
- **The "divorce customer" concept.** Not every customer should be retained. Canary's customer-level risk scoring may benefit from a "cost-to-serve-exceeds-contribution" signal.
- **Appriss Retail Data Specification as SDD source.** v1.1 is a 2018 schema for retail LP data. Comparing it field-by-field against Canary's current schema surfaces gaps in what Canary captures. Candidate for future SDD extraction work.
- **DSD as a worked-example pattern for client extensions.** Secure's base model plus retailer-specific extensions (grocery-chain DSD) is a delivery pattern Canary can adopt for its largest merchants — core rules + merchant-specific rule packs.

## Related

- [[Brain/projects/Secure|Secure]] MOC
- [[Brain/wiki/secure-platform-overview|Secure Platform Overview]]
- [[Brain/wiki/secure-architecture|Secure Architecture]]
- [[Brain/wiki/secure-client-top5-grocery-chain|Secure Client: Top-5 Grocery Chain]] — DSD example
- [[Brain/projects/Canary|Canary]] — forward project
- [[docs/superpowers/briefs/2026-04-secure-to-canary-handoff|Secure → Canary Handoff]]

## Sources

- `/Users/gclyle/secure/Secure Omnichannel Overview-Oct2018.pdf` — product overview, risk surfaces, order flow
- `/Users/gclyle/secure/Appriss Retail Data Specification v1.1.pdf` — data schema contract
- `/Users/gclyle/secure/5.1 Requirements.xlsx` — Secure 5.1 functional requirements
- `/Users/gclyle/secure/Kroger DSD requirements.docx` — retailer-specific DSD extension (top-5 grocery chain — raw intake retains original client identifier as source of record per `feedback_scrub_client_names.md`)
