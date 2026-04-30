---
classification: public
type: wiki
status: active
sub-type: positioning
date: 2026-04-30
last-compiled: 2026-04-30
needs-review: 2026-05-30
audience: NCR Counterpoint VARs (principals, lead architects, engagement leads)
projects-to: ncr.growdirect.io (NCR companion vault)
companion: Brain/wiki/voyix-counterpoint-rapid-pos-engagement-context.md
companion: Brain/wiki/ncr-counterpoint-rapid-pos-relationship.md
companion: Brain/wiki/catz-method.md
---

# Counterpoint Modernization — Without the Rip-and-Replace

NCR Counterpoint customers don't need to migrate off Counterpoint to get cloud-native, AI-native, multi-store enterprise capabilities. The right path is incremental: an observer layer first, a spine of record second, an agentic interface third, modules taken over fourth, front-end replacement only at the end — and only when the customer is ready. The VAR collects services revenue at every phase. The customer never sees a migration; they see capability arriving. That's the platform thesis behind Canary.

This article is for the NCR Counterpoint VAR principal asking three questions at once. *How do I give my customers the cloud-native modernization they're asking for, without forcing a register-UI rip-and-replace I can't sell? Where does my services revenue come from in that transition? And what's my answer when a customer asks "can my AI assistant query my POS?"*

## The pressure VARs are absorbing right now

| Pressure | Origin | What customers expect |
|---|---|---|
| Cloud-native UX | Mid-market specialty retailers benchmarking against Shopify, Lightspeed, Square in adjacent verticals | Mobile back-office, browser-based admin, no Windows Server dependency for daily ops |
| Multi-store enterprise control | Operators with 10-100 locations who graduated past single-store needs | Real-time inventory position, cross-store transfers planned not whiteboarded, OTB enforcement not just reporting |
| AI / agentic interfaces | Customers seeing Claude, ChatGPT, and Cursor in adjacent business tools | "I want to ask my assistant what's selling and have it act" |
| License-cliff anxiety | Voyix renewal conversations | "Is there a path forward that isn't paying NCR more?" |
| Modernization roadmap drag | Voyix's own NextGen roadmap is paced for enterprise, not SMB | "We can't wait three years" |

Every one of these pressures is solvable today. The hard part has been finding a path that doesn't ask the VAR to become a platform vendor or the customer to become a migration project. **That's the gap Canary fills.**

## The principle — Counterpoint stays as the edge node

NCR's own Voyix Connected Services architecture says it explicitly: **inference at the edge, intelligence in the cloud, fleet management between them.** Counterpoint already runs on a Windows Server in-store. It already is the edge node. It already does the fast, offline-capable, register-side work the architecture calls for. The piece NCR hasn't shipped fast enough is the cloud spine that wraps the edge.

Canary is the cloud spine. The register stays where it is. The Windows Server stays where it is. The customer's cashiers don't retrain. The customer's IT team doesn't migrate. The cloud capabilities arrive around the existing footprint, not on top of it. **The only thing that gets replaced — eventually, optionally, under VAR control — is the back-office surface, and only when the customer asks for it.**

## The wedge — an MCP layer the customer's agents call first

The technical entry is not an API gateway, a database connector, or a data warehouse. It's a **Model Context Protocol (MCP) layer** — the AI-callable surface that customers' agents (Claude, ChatGPT, Cursor, in-house copilots) need a real retail backend to talk to.

Three things make MCP the right wedge:

1. **It's non-disruptive.** Counterpoint's REST API stays as it is. The customer's existing integrations stay. MCP is additive — a new surface for new consumers.
2. **It's customer-pulled.** Customers are already asking for AI-callable retail data; if the VAR doesn't deliver an answer, the customer finds one elsewhere. Canary has the answer on the shelf.
3. **It becomes the API gateway one abstraction up.** Once the customer's humans and agents both call Canary MCP for retail truth, the source-of-truth question is decided. The platform shift happens without ever calling itself a platform shift.

## The five phases — observer to spine to platform

| Phase | Window | Canary owns | Counterpoint owns | Customer-visible change |
|---|---|---|---|---|
| **0 — Read-side observer** | Months 0-3 | MCP read tools (inventory lookup, transaction inquiry, customer history, OTB status, distribution recommendation, LP alert search), perpetual ledger as a shadow | System of record; Canary reads via REST + reconciles | "Our AI assistant can answer questions about my stores. We're seeing LP cases and OTB violations we couldn't see before." |
| **1 — Spine of record** | Months 3-9 | Perpetual ledger becomes authoritative; cost truth, inventory position, OTB enforcement | Transactional front-end; pushes events to Canary; receives back-write for vendor PO release and item cost updates | "Inventory and cost truth live in Canary. Counterpoint is one input among many. Buyers plan in Canary, execute in Counterpoint." |
| **2 — MCP gateway** | Months 9-18 | Canonical agentic + human interface; new apps target Canary, not Counterpoint | Wrapped as a legacy backend service consumed by Canary | "Our store managers, buyers, and back-office teams operate through Canary. Counterpoint is invisible." |
| **3 — Module takeover** | Months 18-30 | Catalog, CRM, Purchasing, Forecast, Pricing fully native; Labor and Work Execution built where Counterpoint and adjacent platforms have no answer | Reduced to register transactions and edge-side execution | "We've stopped logging into Counterpoint for back-office work. Voyix renewal becomes optional." |
| **4 — Front-end replacement** | Months 30-42 | Full platform end-to-end | Decommissioned, optionally; or kept as a register UI on a Canary backend if customer prefers | "We're on Canary. Counterpoint was the bridge, not the destination." |

Each phase ships standalone value. Each phase is a billable VAR engagement. **No big-bang risk; no go-live cliff; no customer training crisis.**

## CRB module activation across the phases

The Canary Retail Brain spine (13 modules — A, C, D, F, J, L, N, P, Q, R, S, T, W) lights up incrementally:

| Module | Activates | What it delivers |
|---|---|---|
| T (transaction pipeline) | Phase 0 | Real-time read of every Counterpoint document, mapped to ARTS POSLog v6 |
| S (space/range) | Phase 0 | Item master read, mix-and-match, fractional units, multi-tier pricing |
| R (customer) | Phase 0 | Unified customer entity with address, history, loyalty |
| Q (loss prevention) | Phase 0 | Rule catalog firing on real transaction data |
| F (finance) | Phase 0-1 | Sales aggregation, cost ledger, satoshi-precision cost truth |
| J (forecast/order) | Phase 1 | OTB enforcement, vendor PO recommendations |
| D (distribution) | Phase 1 | Multi-store transfer recommendations, RTV, ASN |
| C (commercial) | Phase 1-2 | Vendor management, B2B/landscaper commercial intelligence |
| P (pricing/promotion) | Phase 2 | Promotional planning and execution |
| A (asset management) | Phase 2 | Device + asset lifecycle |
| N (device/network) | Phase 2 | Store + workstation + drawer-session config |
| L (labor) | Phase 3 | Native scheduling, time, compliance — the gap Counterpoint and adjacent platforms leave open |
| W (work execution) | Phase 3-4 | Generalized detection-and-case-management across operations, capstone of the spine |

The five-module gap most VARs feel today (Q, J, D, L, W) is the gap the customer is asking the VAR to fill. **That's where the value capture sits.** Canary's spine fills it.

## What the VAR sees — services revenue across the phases

Each phase is an engagement, with a distinct services profile:

| Phase | VAR engagement type | Revenue shape |
|---|---|---|
| 0 | Tenant standup, Counterpoint connector configuration, MCP rollout, initial training | Implementation fee + recurring platform subscription |
| 1 | Ledger reconciliation, write-back proof, satoshi-cost migration, controller/CFO sign-off | Major implementation fee + expanded subscription |
| 2 | App migration, agentic workflow rollout, store-manager and back-office retraining | Multi-quarter implementation + subscription tier upgrade |
| 3 | Native module deployment, Labor build, Work Execution rollout | Long engagement, multi-team training, subscription tier upgrade |
| 4 | Counterpoint decommission, register UI cutover, Voyix license sunset planning | Significant migration engagement, multi-year platform subscription |

**Total customer LTV across 36 months is meaningfully larger than a static Counterpoint VAR relationship**, because each phase opens a new services scope. The customer doesn't churn; they expand.

## The accountability rails — what makes this defensible

Three rails run through the platform end-to-end. They are why a customer trusts Canary with their inventory, cost, and operational truth:

| Rail | What it ensures |
|---|---|
| **Operational** | No unknown loss. Every movement is captured, every reconciliation is transparent, every variance has a verb |
| **Financial** | Open-to-buy is gated, not just reported. Spend constraints are enforced at the moment of decision, not after the fact |
| **Evidentiary** | Critical state changes are anchored to a tamper-evident record. Audit conversations become reads, not investigations |

A commodity competitor — a Counterpoint replacement, a generic ERP, a single-store cloud POS — provides none of these. They are intentional design choices in Canary's spine, not commodity primitives.

## What this is not

- **Not a migration off NCR.** Customers can run on Counterpoint indefinitely. Phases 0-2 require no Counterpoint changes at all.
- **Not a rip-and-replace.** No register downtime. No cashier retraining. No inventory cutover.
- **Not a forklift.** No data migration project. Canary reads what's already there.
- **Not a white-label.** The VAR keeps the customer relationship. Canary is the platform layer; the VAR is the delivery and trust layer.
- **Not a Voyix competitor for transaction processing.** Counterpoint stays the transaction processor. Canary owns the spine around it.

## What we'd want to know to start a conversation

If a VAR principal is reading this and the shape resonates:

1. **Top three customers asking the modernization question.** Vertical, store count, current Counterpoint footprint, what specifically they're asking for.
2. **The VAR's services revenue mix today.** Where the implementation, training, and support dollars currently come from. Phase 0 has to fit inside that mix to be a real engagement.
3. **The VAR's existing custom layer over Counterpoint.** Proprietary tables, vertical extensions, in-house tooling. Phase 0 honors all of it; Phase 1+ surfaces it.
4. **The decision-maker in a 90-day pilot.** Whose calendar gets the kickoff meeting.

## How to reach us

The Canary platform is delivered through a partner channel. Canary Retail Brain (`crb.growdirect.io`) is the open-access reference for the 13-module spine. NCR-specific content lives at `ncr.growdirect.io`. To start a VAR conversation, reach out to the GrowDirect team via the public contact path on either site.

## Related reading

- [[ncr-counterpoint-rapid-pos-relationship]] — how Counterpoint, the VAR, and the customer fit together
- [[voyix-counterpoint-rapid-pos-engagement-context]] — NCR Voyix backstory and the unified-commerce thesis
- [[catz-method]] — the diagnostic and delivery method behind every engagement
