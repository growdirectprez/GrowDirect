---
classification: internal
type: wiki
status: active
date: 2026-04-25
last-compiled: 2026-04-25
needs-review: 2026-05-09
companion: Brain/wiki/ncr-counterpoint-api-reference.md
----

# Counterpoint vs Rapid Garden POS — Relationship + What This Means for Canary

The Boutique Home & Garden chain (Engagement 2 retailer) is described as running "Rapid Garden POS." Important: **Rapid Garden POS is not a separate POS product; it is NCR Counterpoint, deployed and configured by Rapid POS as a value-added reseller for the green industry.** This article clarifies the relationship + what it means for Canary's integration approach.

## The relationship

| Layer | Owner | What it is |
|---|---|---|
| **NCR Counterpoint** | NCR Voyix | The POS platform itself — database schema, REST API, business logic, runtime |
| **Rapid POS** | Rapid POS LLC (independent VAR) | NCR-authorized Value-Added Reseller. Installs, configures, trains, supports, customizes. Multiple verticals: garden centers, gun stores, specialty food, wine, feed-and-tack |
| **Rapid Garden POS** | Rapid POS LLC | Rapid's specialization for garden centers + nurseries. Sub-brand of Rapid POS, same VAR org |
| **Customer deployment** | The retailer | Customer runs Counterpoint, deployed by Rapid POS, possibly with Rapid POS-proprietary customizations on top |

A Rapid Garden POS customer is NOT running a separate codebase — they are running Counterpoint with garden-center-tailored configuration + Rapid POS's value-added layer.

## Other NCR Partner-Network specialization VARs

Same pattern as Rapid POS but different verticals; all built on Counterpoint:

- Retail Control Systems (RCS) — multiple verticals
- AMS Retail Solutions — multiple verticals
- Mariner Business Solutions — general retail
- Various regional resellers

For Canary, all of these customers run Counterpoint underneath. Same integration target.

## What this means for Canary integration

**The integration target is the Counterpoint REST API.** Canary's TSP Counterpoint adapter built against the public API works for any Counterpoint customer regardless of which VAR deployed them. The "garden center features" the customer experiences are configurations + behaviors within Counterpoint, observable through standard API fields.

## Garden-center features → Counterpoint API surface mapping

Rapid Garden POS markets these features. Where they live in Counterpoint's standard data model:

| Marketed feature | Counterpoint API surface | Status |
|---|---|---|
| Multi-tier customer pricing (retail / landscaper / commercial) | `AR_CUST.CATEG_COD` (per-customer tier code) + `AR_CTL.USE_LOY_PGMS` system config | **Verified** — visible in GET_Customer + GET_CustomerControl sample payloads |
| Mix-and-match flats / bundle pricing | `IM_ITEM.MIX_MATCH_COD` (item's mix-and-match group) + `PS_DOC_LIN.MIX_MATCH_COD`, `MIX_MATCH_CONTRIB`, `MIX_MATCH_PRC_BASED_ON` (per-line) | **Verified** — visible in GET_Item + GET_Document |
| Bulk-to-fractional sales (sell flat or sell individual plant from flat) | `IM_ITEM.PREF_UNIT_NUMER/DENOM/NAM`, `STK_UNIT`, `PS_DOC_LIN.QTY_NUMER/QTY_DENOM/QTY_UNIT/SELL_UNIT` | **Verified** — fractional quantity model present |
| Multi-store inventory transfers | Document type XFER (via POST_Document) + `Inventory_ByLocation`, `Items_ByLocation`, `InventoryLocations` | **Verified** — Document omnibus handles transfers |
| Vendor management + automated purchasing | `VendorItem` endpoint + Document types PO / PREQ / RECVR / RTV | **Verified** — Workgroup next-numbers confirm types |
| Multi-name plants (common / botanical / Spanish) | Likely uses `IM_ITEM.ADDL_DESCR_1/2/3` (3 additional description slots) or `ATTR_COD_1/ATTR_COD_2` (2 attribute codes); aliases may need additional handling | **Unverified** — need to inspect a real garden-center DB to confirm convention |
| Loyalty programs (points, cards) | `AR_CUST.LOY_PGM_COD/LOY_PTS_BAL/LOY_CARD_NO` etc. (12 loyalty fields per customer) + `AR_CTL.USE_LOY_PGMS` | **Verified** — full loyalty model in Customer record |
| Per-store discount caps / void-comp reasons | `PS_STR_CFG_PS.MAX_DISC_AMT/MAX_DISC_PCT/USE_VOID_COMP_REAS` | **Verified** — store config exposes thresholds |
| Cash drawer / day-end discipline | `PS_STR_CFG_PS.AUTO_DRW_*` + `DRW_ID/DRW_SESSION_ID` on Documents | **Verified** — drawer-session correlation possible |
| Outdoor-rated POS hardware | Physical hardware, not API | Not relevant to Canary integration |
| Vertical-specific reports | UI / Crystal Reports layer, not API | Not relevant to Canary integration |
| Dead-count / shrink tracking for live goods | Likely uses Document type RTV (return-to-vendor) or write-off workflows; specific to garden centers | **Unverified** — may live in Counterpoint's adjustment / write-off paths; need real-customer inspection |

## What might be OUTSIDE the standard Counterpoint API

Rapid POS as a VAR may have added proprietary capabilities that don't surface through the standard Counterpoint REST API:

- Custom Rapid-specific tables in the customer's Counterpoint database (their own additions to the schema)
- Rapid-built UI extensions, reports, dashboards
- Integration glue between Counterpoint and other Rapid-specific tooling
- Customer-bespoke custom fields beyond Counterpoint's stock 5×4 profile slots

If a customer has Rapid-specific data Canary should ingest, that's outside the public API surface. Two options to handle:

1. **Ask Rapid POS directly** — they may expose proprietary data through their own integration channels, or via direct database access agreements
2. **Direct database read** — if the customer permits, query the Counterpoint database directly via SQL for fields/tables not exposed by the REST API. Brittle; customer-permission-dependent; out of scope for the standard build plan but available as an integration fallback.

For Phase 0–4 of the build plan, **ignore Rapid-specific extensions**. Build against the standard Counterpoint API. Address Rapid-proprietary surface in Phase 5+ on a customer-by-customer basis.

## Is Canary mapping the right thing?

**Yes.** The standard Counterpoint REST API is the canonical integration target. Rapid Garden POS customers run Counterpoint; the API is the same. The H&G-specific behaviors that matter are observable through standard endpoints. The few features that may live outside the standard API (multi-name plant aliases, dead-count tracking) are either:
- Visible through extended fields once we inspect a real garden-center database
- Or handled via direct DB read / Rapid-direct integration as a Phase 5+ concern

The build plan and SDD remain correct. No re-targeting needed.

## Open questions to verify against a real Rapid Garden POS customer

When Phase 5 cutover-validation begins (or if we get sandbox access from Rapid POS):

1. Multi-name plant convention — which fields hold botanical / Spanish / common names?
2. Dead-count / live-goods write-off — specific Document type or distinct workflow?
3. Whether Rapid POS has added custom tables we should know about
4. Whether Rapid POS exposes any non-Counterpoint integration channels
5. Whether the H&G chain customer uses Rapid Garden POS specifically OR another Counterpoint VAR (relevant for any Rapid-specific assumptions)

## Source

- Rapid Garden POS — homepage: https://rapidgardenpos.com
- Rapid POS — corporate: https://rapidpos.com
- Lawn Garden Marketing — Rapid Garden POS as NCR Partner Network: https://www.lawngardenmarketing.org/rapid-garden-pos-NCRcounterpoint.aspx
- NCR Voyix Counterpoint product page: https://www.ncrvoyix.com/retail/counterpoint
- NCR Counterpoint API repo: https://github.com/NCRCounterpointAPI/APIGuide

---

## Hub-and-Spoke Distributed Agent Model

The Canary agent network mirrors how human LP organizations are actually structured — store lead, regional manager, LP director. Each tier operates with independent decision authority; higher tiers set policy, lower tiers execute.

```
┌─────────────────────────────────────┐
│          Cloud ALX (LP Director)    │
│  Cross-chain pattern detection      │
│  Model updates + fleet telemetry    │
│  Sees all stores, not individual    │
│  transactions                       │
└──────────────┬──────────────────────┘
               │ policy down / patterns up
    ┌──────────┴──────────┐
    │                     │
┌───▼────────┐     ┌──────▼──────┐
│ Store ALX  │     │ Store ALX   │   ← one per location
│ (LP Lead)  │     │  (LP Lead)  │
│ Local infer│     │ Local infer │
│ Real-time  │     │ Real-time   │
│ alerts     │     │ alerts      │
│ Offline OK │     │ Offline OK  │
└────────────┘     └─────────────┘
```

**Phase 2 addition — Regional ALX (LP Manager):** Aggregates 5–15 stores. Detects cross-store patterns (organized retail crime, vendor fraud across a district) that neither the store agent nor the cloud director would see alone. Regional tier sits between store and cloud; same independent-decision-authority model.

| Tier | Scope | Primary job | Offline behavior |
|------|-------|------------|-----------------|
| Store ALX | Single location | Real-time detection, local Fox cases, associate dispatch | Fully autonomous — runs on local Counterpoint SQL Server |
| Regional ALX (Phase 2) | 5–15 stores | Cross-store pattern detection, regional LP analytics | Degrades to store-level isolation; syncs on reconnect |
| Cloud ALX | Full chain | Fleet telemetry, model updates, chain-wide LP direction | Aggregates when stores reconnect |

**Design rule:** A store agent that cannot make a decision without cloud confirmation has failed its design contract. Cloud connectivity is enhancement, not dependency.

---

## VAR Fleet Deployment Pattern

A Counterpoint VAR who has RMM (remote monitoring/management) infrastructure already in place — standard for managed-services VARs — can deploy the Canary edge agent across their entire fleet in a single motion. Docker install via RMM removes the per-store manual deployment step.

**Deployment sequence for a VAR-led rollout:**

| Step | Actor | Action |
|------|-------|--------|
| 1 | VAR | Canary added to standard Counterpoint install bundle |
| 2 | VAR | Docker image pushed via RMM to existing store Windows Server |
| 3 | Edge agent | Connects to local Counterpoint SQL Server directly |
| 4 | Edge agent | Runs in shadow mode (read-only) for 7+ days |
| 5 | Cloud ALX | Validates detection baseline against shadow data |
| 6 | VAR + retailer | Sign-off on shadow run quality → LP alerts go live |

**Commercial structure:** Canary pricing rides on top of the VAR's margin structure. The VAR owns the customer relationship and bundles Canary into their recurring services revenue. GrowDirect is the platform layer; the VAR is the delivery and support channel.

**Pilot path (single-VAR launch):**
- VAR sandbox environment → 48-hour diagnostic run
- Single pilot store → shadow mode → detection live
- Full chain rollout → weeks, not months (RMM fleet deploy)

The VAR's existing Counterpoint expertise removes the integration consulting burden from GrowDirect. The VAR knows the schema quirks, the customer's configuration, and the edge cases in their vertical. Canary provides the detection intelligence; the VAR provides the deployment capability.

**last-compiled:** 2026-04-28
