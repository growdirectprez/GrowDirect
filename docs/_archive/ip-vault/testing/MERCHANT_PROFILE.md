---
type: spec
domain: canary
status: active
created: 2026-03-14
updated: 2026-03-19
---
# Canary LP — Test Merchant Profile

> Source of truth for all demo data, seed scripts, and integration tests.
> Pulled from live Square sandbox API on 2026-03-04.

---

## Merchant

| Field | Value |
|-------|-------|
| Square Merchant ID | `MLE55GCYANCYT` |
| Business Name | Default Test Account |
| Country | US |
| Currency | USD |
| Status | ACTIVE |
| Created | 2026-02-13 |
| MCC | 7299 (Miscellaneous Recreation Services) |

**Business type:** Multi-location farmers market vendor — housewarming gift items (sage bundles, decorative matches, crystal sets, smudge kits).

---

## Locations (4)

| Name | Address | Square Location ID | Schedule |
|------|---------|-------------------|----------|
| Default Test Account | 1600 Pennsylvania Ave NW, Washington DC 20500 | `LETAP23P9VEWB` | — |
| Penn High School Farmers Market | 27118 Silver Spur Rd, Rolling Hills Estates, CA 90275 | `LV8F86CJMY0CY` | Sun 10am–3pm |
| Redondo Beach Farmers Market | 200 N Harbor Dr, Redondo Beach, CA 90277 | `L3SCZQBGYB2JM` | Thu 8am–1pm |
| Torrance Certified Farmers Market | 2200 Crenshaw Blvd, Torrance, CA 90501 | `L6JHDV1G8X7JF` | Sat 9am–2pm |

**Geography:** South Bay, Los Angeles — all locations within 15 miles.

---

## Catalog (6 items)

| Item | Price(s) | Square Catalog ID |
|------|----------|-------------------|
| White Sage Smudge Stick Bundle - Lavender | $12.99 | `F3S65X6FKPNU5MWCMGYIHCCV` |
| Sage Smudge Spray - Cleansing & Protection | $14.99 | (see API) |
| Decorative Matchbox - California Poppies | $4.99 | (see API) |
| Novelty Matchbox - Red Onion Design | $2.99 | (see API) |
| Abalone Shell Sage Smudge Kit | $19.98 / $24.99 | (see API) |
| Healing Crystal Home Protection Set | $19.98 / $29.99 / $39.99 | (see API) |

**Price range:** $2.99–$39.99. Average ticket ~$15–$25. Cash and card mix typical for farmers market retail.

---

## Team Members (6)

| Name | Square Team ID | Role | Email |
|------|---------------|------|-------|
| Alejandro Castillo | `TMSPD-CxVxX1lPyf` | Staff | alex@growdirect.io |
| James Chen | `TMVd4EGbinQsXnac` | Staff | james@growdirect.io |
| Sofia Rodriguez | `TM5_NpkYj2BsDrbt` | Staff | sofia@growdirect.io |
| **Suspicious Steve** | `TMG0yZMV-I0a1VlI` | Staff | steve@growdirect.io |
| David Thompson | `TMI1xcEknr2EJQwJ` | Staff | david@growdirect.io |
| Sandbox Seller (Owner) | `TMc02nYKOgm_e2XL` | Owner | (sandbox default) |

**Suspicious Steve** — designated test employee for triggering Chirp alerts. Use this team member ID when seeding fraudulent transaction patterns.

---

## Day in the Life — Integration Test Scenario

**Saturday at Torrance Certified Farmers Market** (Location: `L6JHDV1G8X7JF`)

| Time | Event | Actor | Chirp |
|------|-------|-------|-------|
| 9:00am | Market opens. Sofia opens cash drawer with $200 float. | Sofia Rodriguez | — |
| 9:15am | Customer buys Sage Bundle ($12.99) + Matchbox ($4.99) = $17.98 | Sofia Rodriguez | — |
| 10:30am | Steve sells Crystal Set ($29.99), refunds it 7 min later | **Suspicious Steve** | **C-001** rapid refund (7 min < 15 min) |
| 11:00am | Steve sells Smudge Kit ($24.99) | Suspicious Steve | — |
| 11:45am | Steve refunds Smudge Spray ($14.99) from earlier | Suspicious Steve | — |
| 12:15pm | Steve sells Matchbox ($2.99), refunds it 4 min later | Suspicious Steve | **C-001** rapid refund (4 min) |
| 12:30pm | Sweep runs — Steve has 3 refunds out of 8 txns (37.5%) | Suspicious Steve | **C-002** excessive refund rate |
| 2:00pm | Market closes. Sofia closes drawer — $23 short. | Sofia Rodriguez | **C-102** cash variance |
| 11:30pm | Someone processes a $39.99 Crystal Set sale | ??? | **C-004** after hours |

**Result:** 4 alerts on the dashboard next morning. Owner reviews, acknowledges C-102 (will check tape), escalates C-001 + C-002 on Steve, opens Fox case.

---

## Canary Internal IDs

Used in seed scripts and demo data. These are our database IDs, not Square IDs.

| Entity | Canary ID |
|--------|-----------|
| Merchant | `demo-sq-farmers-market-0001` |
| Location (Torrance) | `demo-loc-torrance-farmers-0001` |
| Location (Redondo) | `demo-loc-redondo-farmers-0001` |
| Location (Rolling Hills) | `demo-loc-rollinghills-0001` |
| Employee (Steve) | `demo-emp-suspicious-steve-001` |
| Employee (Sofia) | `demo-emp-sofia-rodriguez-001` |
| Employee (Alejandro) | `demo-emp-alejandro-castillo-01` |
| Employee (James) | `demo-emp-james-chen-00000001` |
| Employee (David) | `demo-emp-david-thompson-00001` |

---

*Canary LP | GrowDirect Inc. | Confidential*
