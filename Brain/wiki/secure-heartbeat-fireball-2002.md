---
date: 2026-04-23
type: wiki
tags: [secure, heartbeat, fireball, prior-art, canary-lineage, retail-oos, essential-design, 2002, eai, notification-subsystem]
sources:
  - docs/research/heartbeat-fireball-2002/
  - Brain/raw/inbox/Heartbeat/
last-compiled: 2026-04-23
needs-review: 2026-05-23
status: compiled
---

# Heartbeat / Fireball (2002) — Essential Design

## Summary

A 2001–2003 retail out-of-stock detection + notification system,
piloted at a US Tier-1 grocery chain (super-format stores, ~120k SKU
assortment, 24×7 ops) and a US southeastern multi-state supermarket
chain (~1,100 stores). Built on a Microsoft enterprise-integration
platform with a third-party statistical detection algorithm. The
**single most directly Canary-parallel artifact** in the prior-art
archive — the operational shape of "near-real-time POS event arrival
→ exception detection → push to operator at the physical point of
action" is essentially unchanged 25 years later.

Deep source: [docs/research/heartbeat-fireball-2002/](../../docs/research/heartbeat-fireball-2002/INDEX.md) — 5-file
extraction (THE_PROBLEM · THE_ARCHITECTURE · THE_ALGORITHM ·
THE_NOTIFICATION_SYSTEM · CANARY_LINEAGE_MAP).

## The Essential Design

**The problem.** Detect out-of-stock conditions in live grocery stores
from near-real-time POS transaction data, then notify store personnel
on wireless devices to take corrective action. Underlying thesis:
replace forecast-driven supply chains with consumer-demand-driven
supply chains by surfacing the demand signal directly from the point
of sale. OOS detection was the wedge to prove the broader thesis.

**The architecture.** Two functional domains: **Retail Integration &
Operations Services (RIO)** absorbed the retailer's POS / item /
promotional data and translated to canonical XML in (Inputs) and routed
notifications to wireless endpoints out (Outputs); the **hosted
notification + detection service** received RIO Inputs, ran the
detection algorithm, and pushed results back through RIO Outputs.
Five-cluster anatomy (web, integration bus, app server, SQL +
Analysis, OOS algorithm). Open-routing pattern (destination derived
from message body) absorbed retailer heterogeneity. Trickle POS feed
was the foundational substrate everything else depended on.

**The algorithm.** A statistical-anomaly detector against a learned
**per-(item, store) Poisson velocity model** with eight merchandising-
condition covariates (price, time-of-day, day-of-week, store name,
store traffic, promotions, in-store competition, seasonality). Five
named event types (OOS · Too Fast · Too Slow · New Item · Dropped
Item). Model retrains every 15 minutes to 24 hours per installation.
Notably — OOS is **inferred from velocity dropping below expectation**,
not from an inventory-on-hand count crossing zero. The system never
received an inventory feed.

**The notification subsystem.** The most directly inherited component.
Per-user subscription model controlling: report types · period · summary-
vs-periodic · time windows · event-type filter · promotional filter ·
sort order · report cap. Three trigger categories: OOS Report,
Threshold Alarm, **Data Flow Interrupted Alarm (non-suppressible —
the trust-the-pipeline alarm).** Multi-channel SMTP delivery to
wireless devices (handheld push-email + alphanumeric pagers).
Format-aware rendering to the 8×25-char lowest-common-denominator
display. XML event schema with documented Aug→Jan production-driven
evolution.

## Canary Lineage

Six-axis comparison against current Canary architecture:

| 2002 component | Canary (2026) | Match |
|---|---|---|
| Trickle POS feed (XML/HTTPS, retailer-side push) | TSP webhook ingest (JSON/HTTPS, push from Square) | Transformed |
| Enterprise integration bus (5-cluster) | Webhook subscription manager + Sub 1/2/3 chain (Flask + RQ + Postgres) | Transformed |
| Single statistical OOS algorithm (very tunable) | Multi-rule deterministic Chirp engine (broadly applied) | Transformed |
| Notification subsystem (subscription, filter, sort, channel-aware) | Alert notification service (severity, quiet-hours, rate-cap, digest) | **1:1 conceptually** |
| XML event schema (Aug→Jan evolution) | JSON webhook payload + CRDM | Transformed |
| Operator workflow ungated (open → browse → act → delete; no system tracking) | Full alert lifecycle (`new` → `investigating` / `escalated` / `resolved` / `dismissed` / `case_opened` / `archived`) | **Net-new in Canary** |
| Professional-services deployment per retailer | OAuth self-service onboarding | **Net-new in Canary** (largest single delta) |
| Algorithm-vendor + integration-platform-vendor partnership | Single-vendor stack | **Net-new omission** |
| (none) | Bitcoin Ordinal cryptographic evidence chain | **Net-new in Canary** |
| (none) | Fox case management | **Net-new in Canary** |

**What 2002 got right** that Canary inherits without re-litigating:
trickle feed as foundation · operator-as-final-recipient · per-(merchant,
signal) baseline · subscription tunability per user · non-suppressible
pipeline-health alarm · open-routing pattern · the shape of the
notification subsystem itself.

**What 2002 got wrong** (or right-for-2002, wrong-for-2026): per-retailer
consulting deployment cost · two-vendor partnership friction · single-
device-family delivery · no system-tracked operator acknowledgement ·
algorithm tunability hidden from operators · no event store / no replay.
These are the deltas where Canary's design represents an explicit
correction of a 2002-era constraint.

**What is genuinely new in Canary** with no 2002 precedent: self-service
onboarding · cryptographic evidence chain · investigation lifecycle
(Fox) · agent surface (Owl + MCP) · Lightning micro-payments. These
weren't possible in 2002 — they require infrastructure that arrived
later.

## Phase-I Pilot Assessment — abstracted findings

The April 2001 retrospective by the integration vendor's consulting
arm carried these findings (NFR-archetype abstracted):

- **Algorithm performance and per-retailer tuning time** named as
  scalability and adoption-rate risks. At super-format Tier-1 grocery
  scale (~120k SKUs / store) the algorithm's per-store computation cost
  was non-trivial; per-new-retailer model tuning was an adoption drag.
- **Notification subsystem itself** was on track to ship and was
  operating well. The notification half worked under retrospective
  review.
- **Algorithm independent audit** by the southeastern-chain pilot was
  on track for the same week as the retrospective.
- **Business-model risks dominated** the risk list more than technical
  risks (ROI schedule, partnership commitments, recoupment of investment,
  escalating scope without clear ROI). The system worked; the go-to-
  market was the harder problem.

The technical retrospective vindicates the design. The deployment-
economics retrospective is exactly the part Canary's self-service /
single-vendor / OAuth-onboarding architecture is designed to invert.

## Why This Matters for Canary Today

Two reasons:

1. **The detection-and-notification shape is solved.** Canary doesn't
   need to re-prove that near-real-time POS exception detection
   followed by push to a human operator is a workable architecture.
   The 2002 system shipped and worked at Tier-1 grocery scale. Canary
   inherits the validated shape and changes the substrate (commodity
   SaaS) and the onboarding (self-service) — the architectural risk is
   in those deltas, not in the core design.
2. **The deployment-economics flip is the moat.** The 2002 design
   required a paid integrator engagement per retailer because the
   infrastructure made it required. Modern infrastructure makes
   self-service onboarding the default. Canary's positioning ("an
   enterprise software stack from 2002, reshipped as self-service
   SaaS for every SMB in 2026") is grounded in this exact prior art —
   not a hypothesis but an observation about what was structurally
   inevitable once the substrate matured.

## Naming relationship — open

The 2002 system was branded *Heartbeat / Fireball*. Canary's data-
strategy NorthStar describes a *Canary Heartbeat Network* anchored to
Bitcoin's block heartbeat. The founder has confirmed the two are
related; the form of the relationship (direct homage, conceptual
lineage, architectural DNA) is unresolved and tracked as Phase-5 of
the parent extraction playbook.

## Related

- [docs/research/heartbeat-fireball-2002/INDEX.md](../../docs/research/heartbeat-fireball-2002/INDEX.md) —
  the deep 5-file extraction this card distills
- [[Brain/projects/Secure|Secure MOC]] — prior-art retail engagements
- [[Brain/projects/Canary|Canary MOC]] — current shipping product
- [[Brain/wiki/canary-tsp-pipeline|Canary TSP Pipeline]] — the
  trickle-feed successor
- [[Brain/wiki/canary-detection|Canary Detection Engine]] — the Chirp
  module
- [[Brain/wiki/canary-architecture|Canary Architecture]] — system overview
- [[Brain/wiki/growdirect-data-strategy|Data Strategy NorthStar]] —
  the *Canary Heartbeat Network* (the different "Heartbeat" that may
  be related)
- [[Brain/projects/RetailSpine|RetailSpine MOC]] — Loss Prevention
  cell density centre
- [`Canary/docs/retail-capability-model.md`](../../Canary/docs/retail-capability-model.md) —
  the canonical Loss Prevention capability that picks up the
  vanilla design pattern from this prior art

## Sources

- `Brain/raw/inbox/Heartbeat/` — full 417-file source archive
- `docs/research/heartbeat-fireball-2002/` — 5-file signal-only
  extraction (the authoritative layer for this card)
- All client names abstracted to NFR archetypes per
  `feedback_scrub_client_names.md`. Raw archive intact.
