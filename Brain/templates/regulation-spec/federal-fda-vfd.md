---
regulation-id: federal-fda-vfd
name: FDA Veterinary Feed Directive (VFD)
description: FDA requirement that medicated animal feed containing certain antimicrobials be sold only with a valid Veterinary Feed Directive on file from a licensed veterinarian for a specific patient under 21 CFR 558.
geo-scope: federal
effective-date: 2017-01-01
expires-date: ""
supersedes: []
source-citation: 21 CFR 558 (revised effective 2017-01-01 by FDA Guidance for Industry #213)
source-url: https://www.fda.gov/animal-veterinary/development-approval-process/veterinary-feed-directive-vfd
verticals: [pet, feed-tack, garden-nursery]
payload-schema: fda-vfd-electronic-form-v2
cadence-tier: stream
enforcement:
  authority: FDA Center for Veterinary Medicine (CVM)
  consequences:
    - Civil penalties for distribution without VFD
    - Criminal liability (knowing violation under FFDCA § 301)
    - State feed control license review (per state-specific overlay)
case-type-links:
  - ag-vfd-violation
  - ag-vfd-expired-on-file
  - ag-feed-inspection
canary-modules:
  - canary-compliance
  - canary-fox
  - canary-hawk
  - canary-item
sources:
  - 21 CFR 558 (regulatory text)
  - FDA Guidance for Industry #213
  - AAFCO state-by-state feed control overlays
  - RapidPOS feed-tack-pet-pos and pet-store-pos pages (compliance feature references)
last-compiled: 2026-05-02
needs-review: false
---

# Regulation: FDA Veterinary Feed Directive (VFD)

## What this is

FDA-mandated requirement that medicated animal feed containing **certain antimicrobials** (those classified as medically important to human medicine) may be distributed to a livestock owner ONLY with a valid Veterinary Feed Directive — a written or electronic order from a licensed veterinarian, specific to a named animal/herd under that veterinarian's care, for a defined indication and duration. Effective in current form January 1, 2017 per FDA Guidance for Industry #213; codified at 21 CFR 558.

## Geographic scope

| Field | Value |
|---|---|
| Geo level | federal |
| Geo identifier | country:US |
| Population covered | All distributors of VFD-class medicated feed products (~10,000+ feed retailers nationwide) |

## Effective dates

| Date | Event |
|---|---|
| 2015-06-03 | Final rule (80 FR 31707) |
| 2017-01-01 | Effective for all VFD drugs |

## Source citation

- **21 CFR 558** — Veterinary Feed Directive regulations
- **FDA Guidance for Industry #213** — Judicious Use of Antimicrobials
- Public reference: https://www.fda.gov/animal-veterinary/development-approval-process/veterinary-feed-directive-vfd

## What it requires

For VFD feed distributors (retailers selling medicated feeds in the VFD class):

1. **VFD on file before sale** — receive a valid VFD from the veterinarian (or veterinarian's facility) before distributing the feed
2. **Feed label match** — the VFD must reference the specific feed product being sold
3. **Recordkeeping** — retain the VFD for **2 years** after distribution (paper or electronic; FDA-acceptable systems)
4. **No distribution without VFD** — sale to customer prohibited if no valid VFD on file
5. **Acknowledgment letter** — receive an Acknowledgment Letter from FDA before first distribution of VFD feed (one-time onboarding)
6. **Available for FDA inspection** — VFD records must be available on demand

## Payload schema

VFD has FDA-specified content (21 CFR 558.6(b)) — adopt schema verbatim:

- Veterinarian (name, license, signature, contact)
- Client / livestock owner (name, contact)
- Animal/herd identification (species, production class, location)
- Drug (active ingredient, level in feed, indication, duration)
- Dates (issuance, expiration; max 6 months from issue per 21 CFR 558.6(b)(6))
- Feed product (referenced by approved manufacturer label)
- Cautionary statement and refill prohibition

Electronic VFDs are FDA-accepted; multiple commercial vendors provide VFD electronic systems.

## Verticals affected

Pet retailers (selling species-medicated feeds), feed & tack stores, garden/nursery centers selling livestock feed.

## Cadence tier

**Stream** — VFD validity check fires at every sale of a VFD-class feed product (real-time at register).

## Enforcement

| Field | Value |
|---|---|
| Enforcement authority | FDA Center for Veterinary Medicine (CVM) |
| Civil penalties | Per FFDCA § 303 — civil monetary penalty per violation |
| Criminal liability | Knowing violation: misdemeanor / felony per FFDCA § 301 |
| Audit trigger | FDA inspections (random + risk-based + complaint-driven); state feed control officer joint audits |

## Case-type linkage

| Case type | Trigger |
|---|---|
| `ag-vfd-violation` | VFD-class feed sold without valid VFD on file |
| `ag-vfd-expired-on-file` | VFD on file but expired before sale (>6 months from issue) |
| `ag-feed-inspection` | FDA / state feed control inspection initiated at the location |

## Canary module integrations

- **canary-compliance** — VFD validity checking; AAFCO state overlay (state feed control acts add layer)
- **canary-item** — `app.item_attributes` flags for VFD-class feed SKUs
- **canary-hawk** — fires `ag-vfd-violation` case at register block or post-sale review
- **canary-fox** — anchors VFD events (validation, distribution, expiration) to evidence chain
- **DriftPOS register** — VFD-class items trigger sale-time prompt; sale blocked if no valid VFD

## Operator UX

At sale time when a VFD-class feed is scanned:

- *"This feed contains a VFD-class antimicrobial. A valid VFD on file is required (21 CFR 558). Scan veterinarian VFD reference or upload digital VFD."*
- *"VFD validated. Distribution authorized. Recording for 2-year retention."*
- *"VFD expired. Sale blocked. Direct customer to obtain renewal from veterinarian."*
- *"No VFD on file. Cannot sell this product without a valid VFD."*

## Sources

- 21 CFR 558 (regulatory text)
- FDA Guidance for Industry #213
- AAFCO state-by-state feed control overlays
- RapidPOS feed-tack-pet-pos page (vertical compliance feature reference)
- RapidPOS pet-store-pos page (state/federal feed compliance tools reference)

## See also

- Card: [[platform-geographic-compliance-resolver]] — federal layer of the resolver
- Card: [[platform-federal-compliance-spine]] — federal protocol adoption
- Card: [[platform-parcel-as-anchor]]
- Case type: `ag-vfd-violation.md`
- Card: [[canary-compliance]]
- Card: [[canary-item]]
