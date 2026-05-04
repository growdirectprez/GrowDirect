---
screen: /reports/executive
title: Executive Summary
role: ADM | MGR
wave: W5
origin: N
cp_equivalent: "None — CP has no cross-module executive summary report"
---

# Executive Summary

**URL:** `/reports/executive`  
**Primary role:** ADM; MGR  
**Entry points:** Primary sidebar nav (Reports section → Executive); home dashboard → executive summary link

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Executive Summary", period selector, store selector | Default: last 30 days / all stores |
| Top section | Business health scorecard | |
| Main content | Six-domain summary grid | |
| Bottom section | Period comparison table + export | |

## Key Elements

### Business Health Scorecard
Single row of six color-coded tiles, one per operational domain:
- **Sales:** Net sales vs prior period (green = up, red = down), discount rate flag if > threshold
- **Inventory:** Overall shrink rate, days-on-hand health flag
- **Purchasing:** OTB utilization, vendor on-time delivery %
- **Labor:** Labor efficiency, overtime flag
- **LP:** Alert volume, case closure rate, unknown loss %
- **Loyalty:** Active membership trend, redemption rate

Each tile is a one-KPI indicator with a traffic-light color and a one-line insight. The scorecard answers "what does the business look like?" in six squares.

### Six-Domain Summary Grid
One section per domain. Each section: 2-3 primary KPIs with sparklines (trend over the period), key insight in plain English ("Discount rate at Store 3 is 3× the network average — LP flag active"), and a link to the relevant detail module.

**Plain-English insights:** Each domain section auto-generates one insight sentence from the data. These are templated narratives, not free-form AI text: "Category Tropicals sell-through is 18% below plan" or "2 of 6 stores have No LP substrate configured — detection rules silent." The sentence is based on the most prominent anomaly in each domain.

**This is not a drill-down screen.** Executive Summary is the 10-second overview that tells ADM or the founder whether to keep reading. The domain links navigate to the actual detail screens for investigation.

### Period Comparison Table
Side-by-side of all primary KPIs: This Period vs Prior Period vs Prior Year (if data is available). Used for board presentations, investor updates, or LP program performance reporting.

### Export
PDF export of the full executive summary. Generated as a formatted report suitable for printing or sharing with stakeholders. Includes the scorecard, domain grid, and comparison table.

**Empty state:** "Insufficient data for an executive summary. The summary will populate once the platform has been live for a full reporting period."

## Interaction Flows

1. **Founder weekly review:** Founder opens executive summary → 30-second scan of scorecard → Sales up, Inventory clean, LP flag on Store 3 → clicks LP domain link → opens shrink report filtered to Store 3 → sees the pattern — acts
2. **Board reporting:** ADM exports executive summary PDF → period = last quarter → presents in board meeting as operational performance summary → one document covers all six domains
3. **New tenant review:** ADM reviews a tenant's executive summary 60 days post-launch → LP domain shows "LP substrate missing for 2 stores" → reminder to complete LP configuration → follows link to admin → config

## UX Callout

CP has no cross-module summary. An owner of a multi-store retail operation in CP produces their operational overview by running five different reports in five different modules, formatting them in a spreadsheet, and summarizing in a slide deck — probably once a month, if at all. The Canary executive summary computes the same synthesis continuously. It's not replacing the investigation tools; it's the signal flare that tells the owner which module to open first. The plain-English insight sentences are the important innovation: they translate KPIs into action triggers. "Discount rate at Store 3 is 3× the network average — LP flag active" is not a dashboard; it's a directive.

## Navigation Exits

- All module entry points — from domain section links

## Open Questions

None.
