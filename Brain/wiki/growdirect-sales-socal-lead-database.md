---
date: 2026-04-22
type: wiki
tags: [growdirect, sales, lead-database, canary, socal, square-merchants]
sources:
  - docs/_archive/ip-vault/sales/Canary_SoCal_Lead_Database_v1.0.xlsx
last-compiled: 2026-04-22
needs-review: 2026-05-06
---

**Wiki:** [[Brain/Home|Home]]

# Canary SoCal Lead Database v1.0

> ⚠️ **Volatile data caveat.** The xlsx source contains live prospecting data (contacts, outreach status, next-action dates). This wiki card captures the *structure and methodology* of the database — not the row-level data, which belongs in the spreadsheet and will drift from any snapshot. Go to the xlsx for current lead state.

## Purpose

Canary's initial SMB lead database, compiled from the Jeffe / Grok advisory session on February 20, 2026, to seed the Square Marketplace beta-merchant outreach. Owner: **Will (Lead Generation)**. Geography: 200mi radius of 90275 (Rancho Palos Verdes).

Classification: Internal — Sales Pipeline. Status: Active Prospecting.

## Database Shape

Four tabs in the workbook:

### 1. Lead Database

The primary table. Each row is one prospect chain. Fields:

| Field | Purpose |
|---|---|
| Tier | TIER 1 (full engagement, 10–50+ locations) / TIER 2 (beta candidates, 3–10 locations) |
| Chain Name | Brand name |
| Type | Vertical (fast-casual, specialty coffee, etc.) |
| Locations | Total / SoCal count |
| Square Products Used | POS stack depth |
| Key Decision Maker | Name / role / franchise HQ |
| Website | URL |
| Nearest Location to 90275 | Geographic proximity |
| Distance (mi) | Driving distance |
| Annual GPV Est. | Revenue signal for tier sizing |
| Pain Points (Likely) | Merchant pain from Reddit/BBB analysis |
| Outreach Strategy | Channel + angle |
| Status | Research / Verify POS / Contacted / etc. |

### 2. Outreach Tracker

Contact-attempt log. Fields: Date, Chain, Contact Name, Role, Channel, Action Taken, Response, Next Step, Next Date, Notes. Owned by Will.

### 3. Square Ecosystem Intel

TAM / SAM / SOM context. Reference metrics:
- ~4M active U.S. Square merchants
- ~$210B annual GPV
- ~6M connected endpoints (terminals/devices)
- 124M BFCM 2025 transactions (+10% YoY)
- Canary TAM 400K merchants (10%), SAM 40K (SoCal focus), beta SOM 6 merchants

### 4. Pain Point Map

Merchant complaints → Canary feature alignment. Each row maps a real merchant pain (from Reddit / BBB / Trustpilot / Jeffe-Grok Feb 20) to a Canary feature ID (MPA-1 Hold/Freeze Alert, MPA-2 Deactivation Radar, MPA-3 Outage Detector, MPA-4 Fee Spike Watch, MPA-5 Support Queue Tracker, E1-F2 Chirp Detection) with MVP status and the sales hook.

## Tier 1 Targets (snapshot, Feb 2026)

- **The Kebab Shop** — 50+ locations, 20+ SoCal. Full Square stack. $20M–$50M GPV est. Square case-study subject.
- **7 Leaves Cafe** — 44 locations, 22 drive-thrus. Just announced Square partnership Jan 2026. $15M–$35M GPV est.

## Tier 2 Targets (snapshot, Feb 2026)

- **Offset Coffee** — 5–6 locations, South Bay. 40% YoY growth. Closest to Jeffe's zip — in-person walk-in opportunity.
- **Go Get Em Tiger** — 8 LA locations. Craver app integration (verify Square vs. Toast first).
- **Wally's Cafe** — 3 locations. Roni Matar (operator). Square for Restaurants + DoorDash.
- **Steelhead Coffee** — 2–3 Long Beach locations. Verify Square vs. Toast at SteelCraft.

See the xlsx for current tier assignments and outreach status — these change.

## How It's Used

1. Will prospects each tier, starting with closest-first (Offset Coffee for in-person).
2. Outreach Tracker logs every touch and next-step.
3. Pain Point Map is the sales-conversation crib sheet.
4. Square Ecosystem Intel underpins investor / TAM positioning.

The beta gate is 5 active Square merchants (Marketplace listing requirement). The six Tier 2 candidates are sized to clear that gate with slack.

## Related

- [[Brain/projects/GrowDirect|GrowDirect MOC]]
- [[Brain/wiki/growdirect-working-papers|Working Papers Structure]]
- [[Brain/wiki/growdirect-the-rollout|The Rollout]] — go-to-market phasing
- [[Brain/wiki/growdirect-the-market|The Market]] — 4.5M Square merchants
- [[Brain/wiki/growdirect-white-paper|Canary White Paper v1.3]] — Section 6.5 customer segmentation

## Sources

- `docs/_archive/ip-vault/sales/Canary_SoCal_Lead_Database_v1.0.xlsx` — the workbook (live prospecting data)
