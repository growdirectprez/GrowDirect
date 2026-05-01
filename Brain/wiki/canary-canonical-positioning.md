---
tags: [canary, positioning, market, who-what-how, positioning-doctrine]
last-compiled: 2026-05-01
needs-review: 2026-08-01
related: [canary-go-portal, canary-market-positioning, canary-go-satoshi-cost-model, ncr-counterpoint-rapid-pos-relationship]
---

# Canary — Canonical Positioning

> **Governing thesis.** Canary's lane is **multi-store merchandising + store ops for SMB on Counterpoint API**. Delivered through **Rapid POS as the VAR / channel of record**. Methodology is the **CATz playbook**. This card is the canonical statement of who Canary serves, what Canary delivers, and how Canary delivers it. Three sentences; the entire commercial framing flows from them.

This card consolidates the founder-locked positioning. Memory `project_canary_canonical_positioning` anchors the same statement. Any future deviation (e.g., "we should also pursue Square restaurant merchants") gets compared against this card before commitment.

## WHAT — multi-store merchandising + store ops

Canary is **not** a POS, not a payment processor, not a marketing platform, not an HR/payroll system. Canary is the **intelligence layer that observes the POS** and runs the merchant's:

- **Multi-store merchandising** — assortment per location, item-level performance correlation, transfer-loss intelligence, multi-location anomaly detection, cross-store cost attribution.
- **Store operations** — loss prevention (Chirp 37-rule + Bull transfer-loss), case management (Fox forensic chain), evidence-anchored compliance (compliance MCP, blockchain-anchor), real-time inventory truth (IaaS), agent-mediated workflows (store-brain).

Two domains, deliberately scoped. Phase 4 of the long arc (5-7 years out) extends Canary into POS by absorption (per `project_canary_replaces_counterpoint_long_arc`). Until then, lane discipline.

## WHO — SMB on Counterpoint API (V1) + Square (V0/V2)

Primary V1 ICP: **Specialty retail SMB running NCR Counterpoint** with multi-store ops (3-50 locations typical, $5M-$50M annual revenue). Counterpoint is the wedge — its REST API is thin enough that Canary's intelligence layer adds material capability the POS itself can't.

V0 / continuing: Square merchants — the reference adapter target. Lower-friction onboarding (webhook-native, no edge agent). Many Square merchants are first-step ICP candidates; conversion to multi-store specialty retail is the upmarket motion.

V2+: Shopify, WooCommerce, additional VARs. Architecture is POS-agnostic; commercial focus stays Counterpoint-first through V1.

**NOT in lane:** Restaurant POS (Toast, Square for Restaurants), enterprise (Square Enterprise, big-box), pure e-commerce without physical retail.

## HOW — Rapid POS as channel of record + CATz playbook

**Rapid POS is the V1 distribution channel.** Canary onboards Counterpoint merchants through the RapidPOS VAR relationship — RapidPOS holds the customer relationship, issues Counterpoint API keys, runs the on-prem deployment alongside their existing software-delivery pipeline. Canary earns; RapidPOS earns proportional rev-share via Lightning at period close (see [[canary-go-rapidpos-crosswalk]] for the architecture).

**CATz is the methodology.** The Canary Agent Taskforce playbook — a five-phase consulting-grade engagement model that takes a merchant from discovery → diagnosis → deployment → daily operations → durable improvement. CATz is what makes Canary a **delivered-service experience** rather than just software. The vault at [catz.growdirect.io](https://catz.growdirect.io) publishes the playbook for partner / client / investor reference.

## What this card decides

Three lane decisions that constrain every subsequent commitment:

1. **Counterpoint-first, not Square-first.** Square is V0 (reference adapter, easier onboarding). Counterpoint is V1 (commercial focus, RapidPOS channel, multi-store ICP). Resourcing favors Counterpoint completeness over Square breadth.
2. **VAR channel-aligned, not direct-sales-aligned.** Canary does not field a direct sales force chasing Counterpoint customers. RapidPOS is the channel; future regional VARs follow the same architecture (see [[canary-go-ncr-counterpoint-crosswalk]] for multi-VAR rev-share model).
3. **Multi-store SMB sweet spot, not enterprise.** A 3-store specialty retailer is the canonical buyer. A 100-store regional chain is upper-bound; a single-store mom-and-pop is lower-bound and needs different onboarding (V0 Square path).

## What this card explicitly excludes

- **NCR Voyix is a competitor, not a partner.** Per memory `project_ncr_voyix_is_competitor` — they compete in the LP/analytics layer. Integration access strategy routes through the customer, not via NCR partnership.
- **Restaurant vertical is not Canary's lane.** Different POS ecosystem (Toast, Resy), different operating model, different ICP.
- **Pure-ecommerce merchants without physical retail are not Canary's lane.** Canary's value is in store-floor and multi-location operations; pure-online merchants get less benefit per-dollar of integration cost.

## See also

- Memory: `project_canary_canonical_positioning` (founder-locked statement)
- [[canary-go-portal]] — project portal
- [[canary-market-positioning]] — broader market context
- [[canary-go-rapidpos-crosswalk]] — RapidPOS channel architecture
- [[canary-go-ncr-counterpoint-crosswalk]] — multi-VAR commercial model
- [[canary-go-satoshi-cost-model]] — pricing mechanism (replaces $25/seat conversation)
- [[catz-rapidpos-alignment-notes]] · [[crb-rapidpos-alignment-notes]] — RapidPOS relationship context
- [[ncr-counterpoint-rapid-pos-relationship]] — operational relationship doc
- Memory: `project_canary_replaces_counterpoint_long_arc` (Phase 4 long-arc destination — internal only)
- Memory: `project_canary_rapidpos_primary_shift` (2026-04-25 commercial pivot)
