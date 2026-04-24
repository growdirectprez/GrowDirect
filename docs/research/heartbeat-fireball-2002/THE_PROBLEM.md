# THE_PROBLEM — what Heartbeat / Fireball (2002) was solving for

A 2000–2001 proof-of-concept and 2001–2003 production system that
detected out-of-stock conditions in live grocery stores from
near-real-time POS transaction data, then notified store personnel via
wireless devices to take corrective action.

The problem statement is two-layer: the *technical* problem (detect
OOS from POS feed in near-real-time and route the alert to a human
holding a pager) and the *thesis-level* problem (replace forecast-driven
supply chains with consumer-demand-driven supply chains by surfacing
the demand signal directly from the point of sale).

## Target NFR archetype

| Dimension | Archetype profile |
|---|---|
| Scale | US Tier-1 grocery chain, super-format stores (≥250k sq ft), ~120k SKU assortment, 24×7 operations · OR US southeastern multi-state supermarket chain, ~1,100 stores, ~24k SKU assortment |
| Vertical | Grocery / supermarket — high SKU velocity, perishable mix, frequent restocking |
| Geography | US (Tier-1 super-format upper-Midwest deployment + southeastern multi-state deployment) |
| Regulatory surface | Standard US grocery (no specific regulated-product carveouts named in the source) |
| Concurrent monitored items per pilot store | ~1,000 SKUs (single-department pilot scope at the Tier-1; full-store at the southeastern chain) |
| Sponsor | Global FMCG manufacturer (consumer products giant) — not a retailer, but a manufacturer-driven push for visibility into retail demand |
| Integrator | An enterprise integration vendor + a specialized analytics vendor (the OOS-algorithm IP holder) |

## Non-functional requirements

| NFR | Target |
|---|---|
| Data latency | Near-real-time. Source describes "trickled TLOGs and daily Item Tables." The analytic model rebuilds every **15 minutes to 24 hours** depending on installation. |
| Notification cadence | Configurable per store. Pilot used **15-minute heartbeat at the southeastern chain, hourly at the Tier-1**. |
| Notification channel | Wireless pager devices worn by key store personnel. Two device families evaluated: handheld push-email devices and traditional alphanumeric pagers. SMTP delivery to both. |
| Operator skill | Store stockers and store managers. The pager UX presumed *zero application training* — open email, browse, delete. No new application to learn. |
| Integration with retailer stack | Non-obtrusive. Read-only on POS data. Two collection patterns evaluated: in-store autonomous device (with HTTP reports) vs centralized hosted service (with SMTP notifications). |
| Scalability | Hosted service was designed for "internet scale" — multi-server web cluster + EAI bus group + application server cluster + clustered SQL with Analysis Services. |
| Capacity in pilot | Single-store throughput proved at 1,000 monitored SKUs with 15-minute model rebuilds. |

## Explicitly out of scope

- **Acting on the alert.** The system detected and notified. Reorder,
  replenishment, supplier signaling were future-phase commitments, not
  delivered in the proof of concept.
- **Customer-side analytics.** The signal was operator-facing
  (stocker / manager) only. No customer-segment analyses, loyalty
  integration, or basket analytics in the system. The signal was meant
  to flow *upstream* to the supply chain, not sideways to customer
  systems.
- **Multi-channel.** Brick-and-mortar grocery only. No e-commerce surface.
- **Self-service onboarding.** Every retailer onboarding required a
  paid integrator engagement to install the EAI infrastructure, the POS
  collection routines, and the notification subsystem. The economics of
  the consulting engagement were a recurring concern in the Phase-I
  retrospective.
- **Vertical generalization beyond grocery.** Pilots were grocery only.
  Specialty apparel, general merchandise, hardlines were future
  hypotheticals.

## What "the problem" really was

In the source's own framing: *"the supply chain must have a real-time
consumer-demand-driven signal that initiates the supply chain
response."* OOS detection was the wedge to prove that a real-time
demand signal could be captured, processed, and acted on. The OOS use
case was the most viscerally measurable instance of "the supply chain
is not synchronized to consumer demand" — a stockout is a lost sale
that everyone in the chain (manufacturer, retailer, consumer) feels
immediately.

The deeper thesis — *"forecasts are inferior to actual demand
signals; latency between consumer purchase and supply-chain response
is the inefficiency we should be attacking"* — is the architectural
DNA the system carries. Everything in the design (trickle feed, 15-
minute model rebuild, push notification to a human at the rack)
follows from prioritizing *time-to-actionable-signal* over batch
sophistication.

## Why this matters for Canary

Canary's Chirp module solves the *exception-detection-at-the-point-of-
sale* problem for the same reason: latency between the event and the
operator-attention is where loss compounds. The 2002 work validated
the basic architectural choice that a near-real-time signal pipeline
plus a low-friction notification surface to an operator at the
physical point of action is a workable shape — at enterprise scale,
on commodity infrastructure, with manual-effort onboarding. Canary
inherits the shape and changes the substrate (commodity SaaS) and
the onboarding (self-service) — not the design DNA.
