---
type: spec
title: Canary Go — CRB L4 Gap Delta
status: draft
date: 2026-05-04
source: Brain/wiki/canary-module-*-functional-decomposition.md × 2026-05-04-canary-go-sitemap.md
gro: TBD
purpose: L4 process steps with no sitemap screen. Input for sitemap amendment v2 and wave plan revisions before wireframe briefs begin.
---

# Canary Go — CRB L4 Gap Delta

**Governing thesis:** The sitemap was built bottom-up from the Counterpoint surface. Running it against the CRB module functional decompositions (Canary-native, top-down) surfaces gaps that have nothing to do with Counterpoint — capabilities Canary is designed to do that no existing POS handles, which therefore don't appear in any CP-derived crosswalk.

**Method:** Read all 12 available module functional decomp files; identify L3/L4 process steps with no plausible sitemap screen; classify as Add / Skip / Already-covered.

---

## Structural Gaps — Must Address Before Wireframe Briefs

Three gaps large enough to require sitemap amendment before a single brief is written. If these stay unresolved, the Wave 3–4 briefs will be wrong.

---

### Gap 1 — OTB Entirely Absent (Module O)

**Process coverage:** O.3.1–O.3.7 — Open-to-Buy management: budget pyramid, committed receipts, remaining OTB headroom, approval gates, period close.

**Why it matters:** OTB is one of Canary's primary Canary-native differentiators. Counterpoint has no OTB surface at all. This is not an improvement over a CP form — it's a net-new capability. Buyers at any multi-location L&G operator use OTB to control purchasing against a seasonal plan. Without a screen, the O.3 module has no user-facing entry point.

**Gap scope:** 1 section (dashboard + period drilldown), not just one screen.

**Recommended addition:**
- `/otb` — OTB Dashboard (period summary: budget, committed, remaining, variance vs plan)
- `/otb/:period` — Period Detail (category/vendor breakdown, approval queue for over-limit POs)

**Wave:** 3 (alongside Finance). Prerequisite for Suggested Orders and PO Create briefs — those screens need to reference OTB headroom.

---

### Gap 2 — B2B / Commercial Layer Absent (Module M)

**Process coverage:** M.1–M.4 — B2B customer classification, credit posture tracking, commercial AR, and the Q-M alert family (credit utilization, AR aging, tier deviation, payment pattern).

**Why it matters:** For garden-center operators, 20–40% of gross revenue is commercial (landscapers, contractors, municipal accounts). The investigator and operator both need a commercial lens — the investigator to catch credit abuse and AR fraud; the operator to manage terms and credit risk. Currently the sitemap has no B2B surface at all.

**Gap scope:** 2 additions to existing screens + 1 new report.

**Recommended additions:**
- `/customers/:id` — add **"Commercial" tab**: B2B classification tier, credit limit, credit posture signal (CURRENT / WATCH / PAST-DUE / AT-LIMIT), open AR summary
- `/settings/alert-routing` — add **"B2B / Account Management" alert class**: routes Q-M rule family alerts (credit, AR, tier, payment-pattern) separately from LP fraud alerts. Without this, B2B alerts flood the LP queue.
- `/reports/ar-aging` — aggregate AR aging across all commercial accounts; Wave 3 alongside Finance

**Wave:** 3 (Customer commercial tab + AR aging report), 1 setting update (alert routing classification in Wave 1 backfill).

---

### Gap 3 — Distribution Recommendations Absent (Module D)

**Process coverage:** D.5.1–D.5.6 — multi-store distribution recommendations: excess-at-location + deficit-at-location identification → transfer recommendation generation → buyer approval → auto-PO or transfer initiation.

**Why it matters:** The module decomp calls this "the highest-ROI D deliverable for multi-location operators." It is a Canary-native intelligence layer with no Counterpoint equivalent. The sitemap has `/transfers/new` (manual transfer initiation) but no screen for the recommendation engine that tells the buyer *which* transfers to make. The `/orders/suggested` pattern (review queue → approve → action) applies exactly here.

**Gap scope:** 1 new screen mirroring the Suggested Orders pattern.

**Recommended addition:**
- `/orders/distribution` — Distribution Recommendations Queue: excess-location, deficit-location, suggested transfer qty, estimated days-of-supply improvement, approve → creates transfer draft

**Wave:** 3 (alongside Suggested Orders — same buyer workflow, adjacent in nav).

---

## Lower-Priority Gaps — Address in Wave Planning or Backlog

### Module Q — Rule Tuning Layer

| Process | Gap | Recommended Action | Priority |
|---|---|---|---|
| Q.4.1 | No threshold parameter editing on `/rules/:id` — enable/disable only | Add "Parameters" panel tab on `/rules/:id` with threshold edit + audit log | P1 Wave 2 |
| Q.4.2–Q.4.3 | Allow-list management is 4 preset store screens; no per-rule allow-list or expiration management | Expand `/settings/allowlist/*` or add to `/rules/:id` allow-list tab | P1 Wave 2 |
| Q.4.5 / Q.5.5 | No dry-run / observation mode UI for rules before promotion to alerting | Add status control on `/rules/:id`: Dry Run → Observe → Alert; dry-run results panel | P1 Wave 2 |
| Q.5.7 | No digest recipient configuration | Add "Digest Recipients" tab on `/settings/alert-routing` | P2 Wave 2 |
| Q.6.6–Q.6.8 | No vertical-pack management screen | Add `/settings/vertical-pack` in Admin section | P2 Wave 5 |
| Q.7.1–Q.7.7 | No deployment-phase management UI per tenant | Add `/admin/tenants/:id/lp-rollout` or rollout-phase column on `/admin/config` | P2 Wave 5 |

### Module T — Operational Observability

| Process | Gap | Recommended Action | Priority |
|---|---|---|---|
| T.1.9 | Adapter connectivity health surface unclear — `/admin/config` may cover this but scope is vague | Confirm `/admin/config` includes per-tenant adapter last-poll + connection status; expand if not | P0 confirm |
| T.6.7 | No backfill progress surface | Add "Backfill Status" panel to `/admin/config` or `/admin/tenants/:id` | P1 Wave 2 |

### Module D — Distribution Intelligence

| Process | Gap | Recommended Action | Priority |
|---|---|---|---|
| D.4.1–D.4.4 | No aggregate transfer-loss rollup — per-transfer variance covered; route-level patterns not | Add tab on `/transfers` — "Loss Patterns" (multi-transfer variance rollup) | P1 Wave 3 |
| D.1.6 | Stale-location flagging | Surface as a dashboard warning tile or `/inventory` banner | P2 Wave 3 |
| D.3.6 | In-transit timeout alerts | Add filter on `/transfers` — "Overdue In-Transit"; or surface via `/exceptions` | P1 Wave 3 |

### Module S — Catalog Intelligence

| Process | Gap | Recommended Action | Priority |
|---|---|---|---|
| S.3.1–S.3.5 | No bundle/mix-and-match catalog surface | Add tab on `/items/:id` — "Bundle Groups"; or `/catalog/bundles` screen | P1 Wave 3 |
| S.6.1–S.6.6 | No eCommerce catalog sync surface | Add `/ecommerce/catalog` or EC-health tab on `/items`; tenant-conditional | P2 Wave 4 |
| S.4.5 | Fractional-unit normalization not explicit in analytics | Add to item detail analytics panel; minimal surface cost | P2 Wave 3 |

### Module F — Finance Config + AR

| Process | Gap | Recommended Action | Priority |
|---|---|---|---|
| F.1.4–F.1.5 | No PayCode → tender classification mapping screen | Add `/settings/payment` — "Tender Classification" | P1 Wave 3 |
| F.3.1–F.3.6 | No gift card outstanding liability / balance screen | Add `/reports/gift-cards` | P2 Wave 3 |
| F.5.1–F.5.5 | No tokenization / PCI compliance status surface | Add to `/admin/config` — "PCI / Tokenization Status" | P1 Wave 3 |

### Module P — Promotion Intelligence

| Process | Gap | Recommended Action | Priority |
|---|---|---|---|
| P.2.1 | No "detected but unconfirmed" promotion queue | Add tab on `/promotions` — "Detected (Unconfirmed)" | P1 Wave 4 |
| P.3.2–P.3.4 | No markdown proposal workflow (create + approve) | Add `/markdowns/new` + `/markdowns/:id` or tab on `/promotions` | P1 Wave 4 |
| P.4.1–P.4.4 | No elasticity view | Add to `/items/:id` analytics panel or `/reports/elasticity` | P2 Wave 4 |
| P.5.1–P.5.2 | No bulk price change detection/review | Add "Bulk Changes" filter on `/reports/price-history` | P2 Wave 3 |

### Module C — Compliance + Identity

| Process | Gap | Recommended Action | Priority |
|---|---|---|---|
| C.4.5 | No right-to-be-forgotten admin surface | Add "Data Deletion Requests" panel to `/admin/audit` or `/admin/users` | P2 Wave 5 |
| C.5.3 | No manual identity-link surface | Add "Identity Links" tab on `/customers/:id` | P2 Wave 4 |

### Module N — Device Registry

| Process | Gap | Recommended Action | Priority |
|---|---|---|---|
| N.2.1–N.2.3 | No station/workstation registry | Add "Stations & Devices" tab on `/settings/store/*` | P1 Wave 2 |
| N.3.1–N.3.5 | No drawer-session query surface | Add `/reports/drawer-sessions` or "Sessions" tab on `/transactions` | P1 Wave 3 |

### Module O — Planning Layer

| Process | Gap | Recommended Action | Priority |
|---|---|---|---|
| O.1.1–O.1.8 | No demand forecast view | Add `/reports/forecast` — per-item/location forecast + MAPE tracking | P1 Wave 3 |
| O.2.1–O.2.7 | No replenishment parameter screen | Add tab on `/items/:id` — "Replenishment Params" (ROP, EOQ, safety stock, WOS target) | P1 Wave 3 |
| O.5.1–O.5.2 | No "recommendation approved but no PO matched" status | Add status column on `/orders/suggested` — "Pending Entry" | P2 Wave 3 |
| O.4.8 | No what-if simulation for replenishment | Add "Simulate" mode on `/orders/suggested` | P2 Wave 4 |

### Module A — Asset Classification

| Process | Gap | Recommended Action | Priority |
|---|---|---|---|
| A.1.3–A.1.5 | No asset-item filter on items list | Add filter on `/items` — "Asset Items Only" | P2 Wave 2 |
| A.2.3–A.2.4 | Asset movement anomaly has no alert type | Surface via existing alert system with A-module flag | P2 Wave 3 |

---

## Deliberate Skips Confirmed

| Process | Module | Reason |
|---|---|---|
| C.6.4 — Owl conversational Q&A | C | Chat surface, not a nav route |
| C.6.6 — Cohort projection | C | Explicitly deferred v3 |
| Most T-module L3s | T | Pipeline-internal; no user-facing UI needed |
| L module — Labor decomp | L | No decomp file authored; Wave 4 labor screens cover the surface adequately |
| W module — Execution decomp | W | No decomp file authored; Wave 5 Operations screens cover exception + case management |

---

## Sitemap Amendment Summary (v2 additions)

Structural gaps require 4 new screens and 3 additions to existing screens before briefs:

| Addition | Type | URL | Wave |
|---|---|---|---|
| OTB Dashboard | New screen | `/otb` | W3 |
| OTB Period Detail | New screen | `/otb/:period` | W3 |
| Distribution Recommendations | New screen | `/orders/distribution` | W3 |
| Aggregate AR Aging | New screen | `/reports/ar-aging` | W3 |
| Customer Commercial Tab | Tab on `/customers/:id` | `/customers/:id` → Commercial† | W3 |
| B2B Alert Class | Setting addition | `/settings/alert-routing` → B2B class | W1 backfill |
| Demand Forecast | New screen | `/reports/forecast` | W3 |

**Revised total: ~91 screens** (84 sitemap v1 + 7 structural additions).

---

*Source: Brain/wiki/canary-module-*-functional-decomposition.md (12 files) × docs/superpowers/specs/2026-05-04-canary-go-sitemap.md*
