---
screen: /reports/cases
title: Case Report
role: LP | ADM
wave: W5
origin: N
cp_equivalent: "None — CP has no case management system; no case reporting"
---

# Case Report

**URL:** `/reports/cases`  
**Primary role:** LP; ADM  
**Entry points:** Primary sidebar nav (Reports section → LP/Cases); case analytics link

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Case Report", date range selector, store selector, case type filter | |
| Top section | Case KPI tiles | |
| Main content | Case performance table | |
| Bottom section | Age distribution chart + resolution type breakdown | |

## Key Elements

### Case KPI Tiles
Six tiles for the selected period:
- **Cases Opened:** Total new cases
- **Cases Closed:** Total resolved/closed
- **Open Cases (current):** Still active at end of period
- **Avg Days to Close:** Mean resolution time for closed cases
- **Recovery Rate ($):** Dollar value recovered or documented from closed cases (prosecution referrals, vendor credits, insurance claims)
- **Unknown Loss in Open Cases ($):** Estimated remaining financial exposure in open cases

**Recovery Rate vs Estimated Loss:** These two metrics together define LP program ROI. If the LP program cost X to operate and recovered Y, the net is assessable. Most retail LP programs track only case counts; Canary tracks dollar outcomes.

### Case Performance Table
Rows: one per case type (Hawk / B2B / Vendor / Compliance / Other) or per store. Columns: Cases Opened, Cases Closed, Avg Resolution Time, Closure Rate (%), Recovery ($), Estimated Open Exposure ($).

**Closure Rate:** Closed ÷ (Opened + Previously Open). A program with a 30% closure rate and 70% backlog is understaffed or under-resourced. A 90%+ closure rate means the queue is healthy.

### Age Distribution Chart
Histogram: how old are currently open cases? Bucket by age (0-7 days, 7-14, 14-30, 30-60, 60+ days). A program with many 60+-day-old open cases has a velocity problem — cases are being opened faster than they're being closed, or cases are stalling without resolution.

### Resolution Type Breakdown (closed cases)
Pie chart: No Action Required / Case Opened → Closed with Evidence / Prosecution Referral / Vendor Credit / Insurance Claim / Other. Shows what the LP program is producing — most cases closed as "no action required" might indicate alert quality issues (too many false positives escalating to cases).

**Empty state:** "No case data for the selected period."

## Interaction Flows

1. **Quarterly LP review:** LP manager opens case report → last 90 days → 18 cases opened, 14 closed, avg 11 days to close → 3 prosecution referrals, $2,400 recovery → presents to ADM as LP program performance summary
2. **Backlog analysis:** ADM opens case report → age distribution shows 6 cases > 60 days old → drills into those cases → 4 are waiting on external responses (HR, legal) → not an LP velocity problem; external dependencies are the bottleneck
3. **Alert quality check:** LP sees 72% of closed cases are "No Action Required" → too many false positives escalating to cases → reviews detection rule configurations → adjusts 3 rules to reduce false alert volume

## UX Callout

Case reporting is the LP program's accountability layer. Without it, a retail LP program is a collection of investigation activities with no aggregate view of what it's costing and what it's producing. The Recovery Rate vs. Estimated Open Exposure comparison is the financial argument for LP investment: a program that recovers $15,000 per quarter on a $8,000 operating cost has a clear ROI case. This calculation has never been available to small business retail LP programs — it requires exactly what Canary provides: cases with evidence, dollar amounts, and resolution outcomes tracked in one system.

## Navigation Exits

- `/cases/all` — case list
- `/cases/hawk/analytics` — LP-specific case analytics (W1)
- `/reports/shrink` — inventory-side loss context

## Open Questions

None.
