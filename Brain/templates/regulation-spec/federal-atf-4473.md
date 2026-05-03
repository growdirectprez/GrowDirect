---
regulation-id: federal-atf-4473
name: ATF Form 4473 (Firearms Transaction Record)
description: Federal record of every firearm transfer by an FFL holder; mandatory documentation under 27 CFR 478.124 carrying buyer identity, firearm description, NICS check disposition, and FFL attestation.
geo-scope: federal
effective-date: 1968-06-19
expires-date: ""
supersedes: []
source-citation: 27 CFR 478.124
source-url: https://www.ecfr.gov/current/title-27/chapter-II/subchapter-B/part-478/subpart-G/section-478.124
verticals: [gun, sporting-goods]
payload-schema: atf-form-4473-v5.7
cadence-tier: stream
enforcement:
  authority: ATF (Bureau of Alcohol, Tobacco, Firearms and Explosives)
  consequences:
    - FFL license revocation
    - Civil penalties up to $10,000 per violation
    - Criminal liability (knowing violation): felony, up to 10 years prison
case-type-links:
  - lp-firearms-missing-4473
  - lp-firearms-straw-purchase
  - lp-firearms-4473-violation
  - lp-firearms-inspection
canary-modules:
  - canary-compliance
  - canary-fox
  - canary-blockchain-anchor
  - canary-hawk
sources:
  - 27 CFR 478.124 (federal regulatory text)
  - ATF Form 4473 instructions (current revision)
  - Brain/raw/.extract/CaseManagement/Incident Types.xlsx.md (DSG case-type catalog — rows 13, 19, 30, 46)
last-compiled: 2026-05-02
needs-review: false
---

# Regulation: ATF Form 4473 (Firearms Transaction Record)

## What this is

Form 4473 is the **federal record of every firearm transfer by an FFL holder.** Required under 27 CFR 478.124 for every transfer including dealer-to-customer, dealer-to-dealer, and private-party (when conducted through an FFL). The form captures buyer identity (name, DOB, address, citizenship, license), firearm description (serial, manufacturer, model, type, caliber), NICS background check disposition (proceed / delay / denied), and FFL attestation. Retained at the FFL premises for 20 years (active dealers) or transferred to ATF on FFL surrender.

## Geographic scope

| Field | Value |
|---|---|
| Geo level | federal |
| Geo identifier | country:US |
| Population covered | All ~50,000+ active FFLs nationwide |

## Effective dates

| Date | Event |
|---|---|
| 1968-06-19 | Originally enacted (Gun Control Act of 1968) |
| Various | Revisions to Form 4473 (most recent revision 5.7 / 2020-08); regulatory updates per CFR amendments |

## Source citation

**27 CFR 478.124** — *"Firearms transaction record."* Authoritative text at https://www.ecfr.gov/current/title-27/chapter-II/subchapter-B/part-478/subpart-G/section-478.124. Form template and instructions at https://www.atf.gov/firearms/docs/form/atf-form-4473-firearms-transaction-record-revisions.

## What it requires

For every firearm transfer:

1. Buyer completes Section A (identity, citizenship, criminal/mental-health questions, attestation)
2. FFL completes Section B (firearm description, NICS check, disposition)
3. NICS background check performed (or 4473 + state-issued permit if applicable)
4. Form retained at FFL premises (paper or approved electronic system per 27 CFR 478.125e)
5. Form available for ATF inspection on demand
6. Form submitted to ATF on FFL going out of business (Form 5300.5)

## Payload schema

ATF Form 4473 has a defined field structure (Section A fields A.1 through A.34; Section B fields B.1 through B.27). **Adopt schema verbatim.** Partner with **4473 Cloud** for compliant electronic storage (registered ATF approved system) per 27 CFR 478.125e.

Key field groups:

- **Transferee (Section A):** Name, DOB, address, ID type/number, citizenship, prohibited-person attestation (29 questions)
- **Firearm description (Section B):** Manufacturer, model, serial, type, caliber, courtesy NICS check
- **NICS:** Transaction number, date, response (proceed / delay / denied / cancelled)
- **Disposition:** Disposition date, FFL signature, transferee signature

## Verticals affected

Gun retailers (FFL holders), sporting goods retailers selling firearms, gun ranges with retail FFL operations, any retailer in `verticals/gun-shooting-range-pos` or `verticals/sporting-goods-pos` selling firearms.

## Cadence tier

**Stream** — every firearm transfer is a real-time event. Form completion, NICS check, and disposition all occur during the customer transaction (or held for delayed/denied dispositions per ATF rules).

## Enforcement

| Field | Value |
|---|---|
| Enforcement authority | ATF (Bureau of Alcohol, Tobacco, Firearms and Explosives) |
| Civil penalties | Up to $10,000 per violation; FFL license suspension or revocation |
| Criminal liability | Knowing violation: felony, up to 10 years prison; willful failure to maintain records: felony, up to 5 years prison |
| Audit trigger | ATF compliance inspections (random + risk-based + complaint-driven); FFL renewal; transferee complaints |

## Case-type linkage

| Case type | Trigger |
|---|---|
| `lp-firearms-missing-4473` | 4473 cannot be located during ATF audit or internal cycle |
| `lp-firearms-straw-purchase` | Straw indicators identified during transaction or post-transaction review |
| `lp-firearms-4473-violation` | 4473 review reveals associate violation (incomplete form, NICS bypass, etc.) |
| `lp-firearms-inspection` | ATF compliance inspection initiated at the location |
| `lp-firearms-unaccounted-firearm` | Firearm in eBound Book cannot be located + 4473 missing |

## Canary module integrations

- **canary-compliance** — hosts the 4473 protocol adapter and validation logic
- **canary-hawk** — fires `lp-firearms-*` case types when violations detected
- **canary-fox** — anchors every 4473 event (transferee submitted, NICS run, disposition recorded) to evidence chain
- **canary-blockchain-anchor** — daily batch anchors the 4473 event chain to Bitcoin L2 for audit-grade evidentiary record
- **DriftPOS register** — captures Section A buyer entry and NICS submission at the till
- **Partner integration** — 4473 Cloud for compliant electronic storage (ATF approved electronic system)

## Operator UX

At sale time, the operator sees:

- *"Firearm transfer in progress. Complete Section A on the customer-facing screen, then scan customer ID for verification."*
- *"NICS check submitted. Awaiting response — typical 30 seconds."*
- *"NICS: PROCEED. Dispositioning firearm and finalizing 4473."*
- *"NICS: DELAY. Customer must wait up to 3 business days. Schedule pickup."*
- *"NICS: DENIED. Transfer cancelled. Customer notified per ATF rules."*

After the transaction:

- *"4473 stored. Anchored to evidence chain. Available for ATF inspection on demand."*

## Sources

- 27 CFR 478.124 (regulatory text)
- ATF Form 4473 instructions, current revision (5.7)
- DSG LPMS case-type catalog (`Brain/raw/.extract/CaseManagement/Incident Types.xlsx.md`) — rows for Missing F4473, Firearms 4473 Violation, Straw Purchase, Inspection: Firearms, Unaccounted for Firearm
- RapidPOS gun-store-pos page (verticals/gun-shooting-range-pos) — partner integration with 4473 Cloud and NICS eCheck
- GRO-721 capability map — capability rows #104–107 for firearm-vertical compliance

## See also

- Card: [[platform-geographic-compliance-resolver]] — federal layer of the resolver
- Card: [[platform-federal-compliance-spine]] — federal protocol adoption pattern
- Card: [[platform-parcel-as-anchor]] — every parcel inherits federal automatically
- Card: [[canary-compliance]] — the module that runs the 4473 adapter
- Case types: `Brain/templates/case-type/lp-firearms-missing-4473.md`, `lp-firearms-straw-purchase.md`
