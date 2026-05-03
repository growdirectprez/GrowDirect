---
regulation-id: state-ca-assault-weapons-control-act
name: California Assault Weapons Control Act (AWCA)
description: California state restrictions on possession, sale, and transfer of firearms classified as "assault weapons" under Cal. Penal Code §§30500–30530, with definitional updates and registration mandates governed by California Department of Justice Bureau of Firearms.
geo-scope: state:CA
effective-date: 1989-05-24
expires-date: ""
supersedes: []
source-citation: California Penal Code §§30500–30530 + 11 CCR §§5471–5500
source-url: https://oag.ca.gov/firearms/regassaultweapons
verticals: [gun, sporting-goods]
payload-schema: ca-doj-bof-aw-determination-v3
cadence-tier: reference
enforcement:
  authority: California Department of Justice — Bureau of Firearms (CA-DOJ-BOF)
  consequences:
    - California firearm dealer license suspension or revocation
    - Civil penalties (varies by section; up to $5,000+ per violation)
    - Criminal liability (illegal sale): felony per §30600 — up to 8 years prison
case-type-links:
  - lp-firearms-restricted-attempted-sale
  - lp-firearms-aw-classification-uncertainty
  - lp-firearms-4473-violation
canary-modules:
  - canary-compliance
  - canary-fox
  - canary-hawk
  - canary-item
sources:
  - California Penal Code §§30500–30530
  - 11 CCR §§5471–5500
  - California DOJ Bureau of Firearms — Roster of Assault Weapons
  - Giffords Law Center — California assault weapon overview
  - NRA-ILA California fact sheet
last-compiled: 2026-05-02
needs-review: false
---

# Regulation: California Assault Weapons Control Act (AWCA)

## What this is

California's Assault Weapons Control Act (AWCA) restricts the possession, sale, transfer, and import of firearms classified as **"assault weapons"** under state law. The CA-DOJ Bureau of Firearms maintains the Roster of Assault Weapons. Retailers in California cannot sell listed assault weapons to non-exempt buyers; certain features (named/model lists, characteristic-based definitions) shift the classification. **This is a STATE OVERLAY on top of federal ATF compliance — federal Form 4473 is still required for every firearm transfer; CA AWCA adds an additional restriction layer.**

## Geographic scope

| Field | Value |
|---|---|
| Geo level | state |
| Geo identifier | state:CA |
| Population covered | All ~2,800 California-licensed firearms dealers |

## Effective dates

| Date | Event |
|---|---|
| 1989-05-24 | Originally enacted (post-Stockton schoolyard shooting) |
| 1999-09-28 | Revised list, named-model approach replaced with feature-based test |
| 2016-07-01 | Bullet-button assault weapons regulations expanded |
| 2018-07-01 | Registration deadline for grandfathered firearms |
| 2024-09-13 | SB 2 signed (concealed carry / sensitive places); related AW provisions updated |

(Versioned via `supersedes` chain in the registry; effective-date reflects current operational version.)

## Source citation

- **California Penal Code §§30500–30530** — definitions, restrictions, registration
- **11 CCR §§5471–5500** — implementing regulations (CA Code of Regulations)
- **CA-DOJ Bureau of Firearms** — official Roster of Assault Weapons + identification guidance
- Public reference: https://oag.ca.gov/firearms/regassaultweapons

## What it requires

For California firearms retailers:

1. **Item authorization check** — every firearm SKU must be classified against the AW list before sale. Listed assault weapons cannot be sold to non-exempt buyers.
2. **Feature-based screening** — even unlisted firearms are subject to feature-based test (detachable magazine + certain features = AW under §30515).
3. **Buyer eligibility** — exempt categories (active law enforcement, certain license holders) require additional documentation.
4. **DROS (Dealer's Record of Sale)** — every CA firearm transfer requires DROS submission to CA-DOJ-BOF (separate from federal NICS).
5. **10-day waiting period** — California mandates a 10-day waiting period between purchase and pickup (Cal. Penal Code §27540).
6. **Registration** — pre-existing assault weapon ownership requires CA-DOJ registration (windows specific to AW class).

## Payload schema

State-level data exchange via **CA-DOJ DROS** (Dealer's Record of Sale) electronic system. Form fields include buyer details (name, DOB, ID), firearm description (serial, manufacturer, model, type, AW classification flag), eligibility certificate, exemption claims.

## Verticals affected

Gun retailers operating in California; sporting goods retailers with FFL operations in California.

## Cadence tier

**Reference** — AW Roster is updated periodically by CA-DOJ-BOF; lookups are cached and refreshed change-feed-tier on roster updates. **Sale-time check is real-time** but consults the cached roster.

## Enforcement

| Field | Value |
|---|---|
| Enforcement authority | California Department of Justice Bureau of Firearms (CA-DOJ-BOF) |
| Civil penalties | Dealer license suspension or revocation; civil fines per violation |
| Criminal liability | Illegal manufacture/import/sale: felony per §30600 — up to 8 years state prison |
| Audit trigger | DROS submissions reviewed; CA-DOJ inspections (compliance + complaint-driven); license renewal checks |

## Case-type linkage

| Case type | Trigger |
|---|---|
| `lp-firearms-restricted-attempted-sale` | Customer attempts to purchase a listed assault weapon (or feature-based AW); blocked at register |
| `lp-firearms-aw-classification-uncertainty` | Item-level AW classification uncertain — held for compliance review |
| `lp-firearms-4473-violation` | DROS or 4473 review reveals associate violation |

## Canary module integrations

- **canary-compliance** — state-overlay rule application; AW Roster cache; feature-based screening logic
- **canary-item** — `app.item_authorizations` table holds per-item AW classification (CA-specific)
- **canary-hawk** — fires `lp-firearms-restricted-attempted-sale` case at register block
- **canary-fox** — anchors every AW-classification check and DROS submission to evidence chain
- **DriftPOS register** — CA-store registers receive resolved compliance set including AWCA at boot; sale-time block triggered by item AW flag

## Operator UX

At sale time in a California store, the operator sees:

- *"This firearm is classified as a CA-restricted assault weapon. Sale to non-exempt buyer not permitted (Cal. Penal Code §30605). Confirm exemption certificate or refuse sale."*
- *"DROS submission pending. CA-DOJ response typical 5–15 minutes."*
- *"10-day waiting period applies (Cal. Penal Code §27540). Pickup not before [date]."*
- *"This firearm has detachable magazine + feature combination that may trigger AWCA classification. Hold for compliance review (canary-compliance MCP tool)."*

## Sources

- California Penal Code §§30500–30530 (statutory text)
- 11 CCR §§5471–5500 (regulatory text)
- CA-DOJ Bureau of Firearms — Roster + identification guides
- Giffords Law Center — California assault weapon overview
- NRA-ILA California fact sheet
- RapidPOS gun-store-pos page — firearm vertical compliance reference

## See also

- Card: [[platform-geographic-compliance-resolver]] — state layer of the resolver
- Card: [[platform-parcel-as-anchor]] — CA parcels inherit state regulation
- Card: [[platform-federal-compliance-spine]] — ATF + NICS run UNDER state-overlay
- Regulation: `Brain/templates/regulation-spec/federal-atf-4473.md` — federal layer this stacks on
- Card: [[canary-compliance]]
- Card: [[canary-item]]
