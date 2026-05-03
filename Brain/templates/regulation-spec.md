---
regulation-id: <% tp.file.title.toLowerCase().replace(/\s+/g, '-') %>
name: <% tp.file.title %>
description: ""
geo-scope: ""
effective-date: ""
expires-date: ""
supersedes: []
source-citation: ""
source-url: ""
verticals: []
payload-schema: ""
cadence-tier: ""
enforcement:
  authority: ""
  consequences: []
case-type-links: []
canary-modules: []
sources: []
last-compiled: <% tp.date.now("YYYY-MM-DD") %>
needs-review: false
---

# Regulation: <% tp.file.title %>

> Operational template for instantiating a regulation-spec entry in the geographic compliance resolver. Filled instances live at `Brain/templates/regulation-spec/<regulation-id>.md` — flat directory, one file per regulation, registered into the resolver registry at build/deploy time.

## What this is

<!-- One paragraph: what does this regulation cover? Concrete, operational, citation-grounded. ≤ 60 words. -->

## Geographic scope

<!-- Which geographic level applies? federal / state:<XX> / county:<name> / city:<name> / zip:<XXXXX> / parcel:<id>. Cite Census TIGER feature where applicable. -->

| Field | Value |
|---|---|
| Geo level | <federal / state / county / city / zip / parcel> |
| Geo identifier | <state:CA, county:LA-CA, etc.> |
| Population covered | <# of merchants / # of locations affected — directional> |

## Effective dates and supersession

| Date | Event |
|---|---|
| <YYYY-MM-DD> | Originally effective |
| <YYYY-MM-DD> | Last amendment / supersession |
| <YYYY-MM-DD> | Expiration / sunset (if any) |

## Source citation

<!-- The authoritative source. CFR section / state code / county code / city code. Public URL where possible. -->

## What it requires

<!-- The actual operational requirement. What does the retailer have to do? What records must be kept? What forms submitted? What thresholds tracked? -->

## Payload schema (if data exchange required)

<!-- If the regulation requires submitting a form, sending a record, or maintaining a structured log, name the schema and its fields. Otherwise note "No data-exchange schema required." -->

## Verticals affected

<!-- Which Canary verticals does this touch? gun / liquor / grocery / pet / feed / pesticide / hazmat / tobacco / general-retail / etc. -->

## Cadence tier

<!-- Per the cadence ladder: stream / change-feed / daily-batch / bulk-window / reference. When does compliance check happen? -->

## Enforcement

| Field | Value |
|---|---|
| Enforcement authority | <ATF / state AG / county sheriff / city / etc.> |
| Civil penalties | <fines, license suspension, etc.> |
| Criminal liability | <misdemeanor / felony / none> |
| Audit trigger | <random / risk-based / annual / complaint-driven> |

## Case-type linkage

<!-- Which Hawk case types fire when this regulation is tripped? Cite case-type-id for each. -->

## Canary module integrations

<!-- Which Canary modules adapt to or carry data for this regulation? canary-compliance, canary-fox, etc. -->

## Operator UX (the agent prompt)

<!-- What does the operator at the register / back-office see? In operator language, not regulator language. -->

## Sources

<!-- Citation chain: regulator authoritative source, secondary sources (NRA-ILA, Giffords, AAFCO, EPA registries), prior art (DSG case types, Counterpoint integrations). -->

## See also

- Card: [[platform-geographic-compliance-resolver]]
- Card: [[platform-federal-compliance-spine]] (if federal)
- Card: [[platform-parcel-as-anchor]]
- Template: `Brain/templates/case-type.md` (for linked case types)
