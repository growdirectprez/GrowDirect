---
regulation-id: county-la-firearm-storage-ordinance
name: Los Angeles County Firearm Safe Storage Ordinance
description: Los Angeles County requirement that firearms in residences be stored in a locked container or disabled by a trigger lock when not in immediate possession of an authorized adult; retailer-side disclosure and signage requirements at point of sale.
geo-scope: county:LA-CA
effective-date: 2018-09-25
expires-date: ""
supersedes: []
source-citation: LA County Code Title 13, Chapter 13.66
source-url: https://library.municode.com/ca/los_angeles_county/codes/code_of_ordinances
verticals: [gun, sporting-goods]
payload-schema: ""
cadence-tier: reference
enforcement:
  authority: Los Angeles County Sheriff's Department
  consequences:
    - Civil penalty for non-compliant storage (subject owner)
    - Retailer disclosure failure: civil penalty + license review
case-type-links:
  - lp-firearms-storage-disclosure-missed
  - lp-firearms-inspection
canary-modules:
  - canary-compliance
  - canary-hawk
sources:
  - LA County Code Title 13 Chapter 13.66
  - LA County Sheriff's Department compliance guidance
  - LA County firearm dealer permit conditions
last-compiled: 2026-05-02
needs-review: false
---

# Regulation: Los Angeles County Firearm Safe Storage Ordinance

## What this is

Los Angeles County requires firearms kept in residences to be stored in a locked container OR disabled by a trigger lock when not in immediate possession of an authorized adult. **Retailer obligation:** at the point of sale of any firearm, the retailer must provide a written disclosure to the buyer summarizing the safe-storage requirements, and post signage at the sales counter. Failure to provide disclosure is a separate violation. **This is a COUNTY OVERLAY on top of federal ATF + state CA AWCA.**

## Geographic scope

| Field | Value |
|---|---|
| Geo level | county |
| Geo identifier | county:LA-CA (Los Angeles County, California) |
| Population covered | All firearm retailers operating in unincorporated LA County + LA County cities that have adopted the ordinance |

## Effective dates

| Date | Event |
|---|---|
| 2018-09-25 | Originally adopted by LA County Board of Supervisors |

## Source citation

- **LA County Code Title 13, Chapter 13.66** — *Firearm Safe Storage*
- LA County Sheriff's Department compliance guidance (issued post-adoption)
- Public reference: LA County Code of Ordinances (municode.com)

## What it requires

**For the customer (subject of the regulation):**

- Firearms kept in residences must be in a locked container OR disabled by trigger lock when not in immediate possession.

**For the retailer (point-of-sale obligation):**

1. **Disclosure at sale** — at every firearm transfer, provide written disclosure summarizing the safe-storage ordinance.
2. **Signage** — post LA County safe-storage signage at the sales counter.
3. **Documentation** — retain proof of disclosure (acknowledgment slip or receipt notation) for inspection.

## Payload schema

No structured data exchange required. Disclosure is a printed/digital document; acknowledgment is a checkbox/signature; signage is a printed poster.

## Verticals affected

Gun retailers and sporting goods retailers with FFL operations in Los Angeles County.

## Cadence tier

**Reference** — the ordinance text is stable; the retailer obligation fires at every firearm transfer (stream-tier event in the operational flow). The regulation entry refreshes change-feed-tier on amendment.

## Enforcement

| Field | Value |
|---|---|
| Enforcement authority | Los Angeles County Sheriff's Department |
| Civil penalties | Subject owner: civil penalty for non-compliant storage; retailer: civil penalty for disclosure failure |
| Criminal liability | Generally civil; may escalate if combined with other firearm offenses |
| Audit trigger | LA County Sheriff dealer compliance inspections; firearm-recovery cases trace back to dealer |

## Case-type linkage

| Case type | Trigger |
|---|---|
| `lp-firearms-storage-disclosure-missed` | Sale completed without recorded disclosure acknowledgment |
| `lp-firearms-inspection` | LA County Sheriff dealer compliance inspection initiated |

## Canary module integrations

- **canary-compliance** — county-overlay rule loaded for parcels resolving to LA County
- **canary-hawk** — fires disclosure-missed case if disclosure step skipped at sale
- **DriftPOS register** — LA County-resolved registers add disclosure prompt to firearm-transfer flow
- **canary-fox** — anchors disclosure acknowledgment events to evidence chain (proof of compliance for inspection)

## Operator UX

At sale time in an LA County store, the operator sees:

- *"This sale is in Los Angeles County. Provide LA County safe-storage disclosure to customer (print or digital). Get acknowledgment signature."*
- *"Disclosure acknowledged. Documented for compliance audit."*
- *"⚠ Disclosure step incomplete. Sale cannot finalize without acknowledgment under LA County Code 13.66."*

If a sale is attempted without disclosure step completed, the register blocks the transaction and the agent surfaces the requirement in operator language.

## Sources

- LA County Code Title 13 Chapter 13.66 (ordinance text)
- LA County Sheriff's Department compliance guidance
- LA County firearm dealer permit conditions
- RapidPOS gun-store-pos page — firearm vertical compliance reference

## See also

- Card: [[platform-geographic-compliance-resolver]] — county layer of the resolver
- Card: [[platform-parcel-as-anchor]] — LA County parcels inherit county regulation
- Regulation: `federal-atf-4473.md` — federal layer this stacks on
- Regulation: `state-ca-assault-weapons-control-act.md` — state layer this stacks on
- Card: [[canary-compliance]]
