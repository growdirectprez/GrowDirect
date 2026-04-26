---
classification: internal
type: wiki
sub-type: master-dispatch
date: 2026-04-26
last-compiled: 2026-04-26
needs-review: 2026-05-10
status: active — Week 0 Discovery & Alignment complete; prototype execution begins Week 1
project: Canary LP → RapidPOS L&G Enterprise Backend
pm: Eva (external health check + research; dispatches reviewed and diffed against Brain)
---

# Prototype Prep Master Dispatch
## Canary + Rapid Garden POS — L&G Initiative

Governing thesis: Canary is the non-disruptive enterprise layer on top of Counterpoint. It doesn't replace Rapid Garden POS — it adds the perpetual ledger, LP rules, OTB enforcement, and distribution intelligence that Counterpoint's UI doesn't surface. The external positioning anchors to vault (the ledger) and quartz (the intelligence surface). The method is CATz.

---

## Project State — Week 0 Complete

| Dimension | Status |
|---|---|
| Research baseline | ✓ Complete — functional decomposition, garden-center operating reality, TAM, pain points, Counterpoint API spine, endpoint map |
| Partner contact | ✓ Bart McCleskey / Rapid Garden POS — contact card in Brain |
| Advisor contact | ✓ Tim Mooney / Maonach Group — contact card in Brain |
| Module decomposition | ✓ All spine modules decomposed (D, A, C, P complete this sprint; T, S, R, F, N, Q, J pre-existing) |
| L & W modules | ⏸ Deferred — strategic decision (native build vs. external vendor) pending Bart call |
| Monday call | ✓ Confirmed — Bart McCleskey, 2026-04-27 1:00 PM PST |
| Outreach | Pending — Tim Mooney first advisor contact not yet initiated |

---

## Partners & Advisors

### Bart McCleskey — Rapid Garden POS
**Role:** Primary VAR contact and decision-maker for any Canary partnership bundled into Rapid POS's L&G customer base.
**Contact:** bart@rapidpos.com · (619) 754-4100
**Call:** 2026-04-27 1:00 PM PST — confirmed
**Full profile:** `Brain/wiki/bart-mccleskey-rapid-garden-pos.md`

The Monday call has two jobs: VAR partnership conversation (customer count, bundling interest, proprietary Counterpoint extensions) and assumption resolution (L/W strategic decision, ASSUMPTION-D-03/04, C-05, J-12, J-08).

**The ask from Bart:** Sandbox access · Sample L&G dataset · Integration landscape walkthrough (proprietary tables, customer configuration conventions). In return: working prototype on his data.

### Tim Mooney — The Maonach Group
**Role:** Potential advisor for org design, facilitation, and CATz Phase II workshop delivery.
**Contact:** tim.mooney@maonach.com · (360) 739-1486
**Status:** Profile validated; outreach not yet initiated
**Full profile:** `Brain/wiki/tim-mooney-maonach-group.md`

Gap to confirm in first call: domain familiarity with SMB retail / POS / L&G vertical. Strong org design and technology strategy fit; no visible vertical-specific experience.

---

## Spine Module Gating

### Phase 0 — Ship Now (pre-Bart-call baseline)

| Module | Coverage | Status | LG Guardrails |
|---|---|---|---|
| T — Transaction Pipeline | ● Full | Ready | Fractional units, mix-and-match, dead-count write-offs, cash-paid receipts |
| S — Item Master / Range | ● Full | Ready | Multi-name plant attributes, item-code drift detection, seasonal churn |
| Q — Loss Prevention Rules | ● Full | Ready | Garden-tuned rules: dead-count, live-goods shrinkage, fractional tolerance |
| R — Receivings | ◐ Partial | Ready (basics) | Cash-paid vendor receipts, direct-store delivery, no-invoice receipts |
| F — Finance / Tenders | ◐ Partial | Ready (basics) | Multi-tier pricing, promotion isolation substrate |

**Phase 0 success gate:** Sandbox connection healthy + sample L&G dataset loads with T+S ingest clean.

### Phase 1 — Gate on Bart Call + Sandbox Results (Week 1–2)

| Module | Coverage | Gate Condition |
|---|---|---|
| P — Pricing / Promotion | ◐ Derived | Bart confirms promotion distortion as top-3 pain |
| J — Forecast / OTB | ◐ Partial | P promotion calendar populated; Bart confirms OTB pain |
| N — Device / Stores | ◐ Partial | T+S baseline healthy; multi-location rebalancing confirmed as pain |
| D — Distribution | ◐ Partial | Bart confirms rebalancing across locations as top-3 pain (note: likely Phase 1, not Phase 2 — validate Monday) |

### Phase 2 — Post First Pilot

| Module | Coverage | Gate Condition |
|---|---|---|
| A — Asset Management | ◐ Derived | Pilot customer catalog inspection confirms IM_ITEM.ITEM_TYP=N in use; ASSUMPTION-A-01 scope conflict resolved |
| C — B2B Commercial Intelligence | ◐ Derived | AR module confirmed in use (ASSUMPTION-C-05); B2B account tier confirmed as pain |
| L — Labor Scheduling | ★ / ◯ TBD | Strategic decision post-Bart call — native build vs. external vendor |
| W — Workforce / Scheduling | ★ / ◯ TBD | Strategic decision post-Bart call — native build vs. external vendor |

---

## Open Assumption Markers — Highest Leverage

These are the assumption markers with the most downstream impact. Bart call is the primary resolution opportunity for the top four.

| ID | Assumption | Resolution path |
|---|---|---|
| ASSUMPTION-L/W | Native labor scheduling vs. Homebase/Deputy/TimeForge vendor integration | Bart call — shapes whether L/W are ★ Canary-native or ◯ external vendor cells |
| ASSUMPTION-D-03 | DOC_TYP=XFER is the correct Counterpoint transfer document type | Sandbox schema inspection |
| ASSUMPTION-D-04 | RECVR document confirms transfer receipt at destination | Sandbox schema inspection |
| ASSUMPTION-C-05 | AR module is in active use at target L&G customer sites | Bart call |
| ASSUMPTION-J-12 | Live-goods write-off uses a specific DOC_TYP | Bart call |
| ASSUMPTION-J-08 | Buyers will tolerate "plan in Canary, execute in Counterpoint" UX for OTB | Bart call |
| ASSUMPTION-P-01 | PS_DOC_LIN_PRICE is populated for Rapid Garden POS customers | Sandbox schema inspection |
| ASSUMPTION-A-01 | **SCOPE CONFLICT** — Module A = item-asset-management (this decomp) vs. Bubble/device-anomaly (canonical spec) | Founder decision required |

---

## Engagement Shape

**Method:** CATz Phase II compressed into 100-day deployment model.
**Resource model:** ~2.4 FTE — remains valid.
**Prototype posture:** Parallel-observer on Counterpoint Document omnibus. First slice = T + S ingest + garden-specific Q rules + basic VSM diagnostic.

---

## Related

- `Brain/wiki/bart-mccleskey-rapid-garden-pos.md` — VAR partner profile + Monday call agenda
- `Brain/wiki/tim-mooney-maonach-group.md` — advisor profile
- `Brain/wiki/voyix-counterpoint-rapid-pos-engagement-context.md` — three-actor engagement context
- `Brain/wiki/rapid-pos-counterpoint-market-research-tam.md` — TAM ~1,200 US garden centers
- `Brain/wiki/garden-center-operating-reality.md` — vertical domain context
- `CATz/proof-cases/specialty-smb-counterpoint-solution-map.md` — solution map (module coverage ratings)
- `canary-module-[t|s|r|f|n|q|j|d|a|c|p]-functional-decomposition.md` — per-module L2/L3 decomposition cards
