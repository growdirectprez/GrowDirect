---
card-type: platform-thesis
card-id: platform-geographic-compliance-resolver
card-version: 1
domain: platform
layer: cross-cutting
status: approved
agent: ALX
tags: [compliance, geography, parcel, federal, state, county, city, zoning, registry-as-data, resolver, differentiation]
last-compiled: 2026-05-02
needs-review: false
---

# Pattern: Geographic Compliance Resolver

## What this is

Every retailer at a specific parcel operates under the **union of federal + state + county + city + parcel-zoning regulations**. The geographic compliance resolver computes that union by walking the parcel up the geographic hierarchy and joining every level's applicable rules. Conflicts resolve by most-specific-wins (the rule from the smallest geographic scope dominates).

## Purpose

Compliance regulations are GEOGRAPHIC. A gun retailer in California operates under ATF (federal) AND CA assault weapon ban (state) AND LA County firearm storage ordinance (county) AND city hours-of-sale (city) AND parcel-level zoning (this parcel cannot sell firearms because of school proximity). Manually tracking this layered set is the work that 50+ field-support staff at RapidPOS partially do today. **The geographic resolver collapses the work to a single function call.**

## The resolver

```
parcel (ZIP+4) ─→ city / municipality
              ─→ county
              ─→ state
              ─→ country (federal)

applicable_regulations(parcel) = ⋃ regulations at each level of the hierarchy
                                  resolved by most-specific-wins precedence
```

Same precedence rule already declared by [[canary-compliance]]: *"Operational block (most specific wins) → Item authorization at location → Regulatory zone rules → default allowed"* — extended to a five-level geographic hierarchy.

## Schema (per regulation entry — see `regulation-spec.md` template)

| Field | Purpose |
|---|---|
| `regulation-id` | Stable identifier (`ATF-4473`, `CA-AWB`, `LA-FS-001`, `NYC-FH-15`) |
| `name`, `description` | Human-readable label and one-line summary |
| `geo-scope` | `federal` / `state:CA` / `county:LA` / `city:NYC` / `parcel:<id>` / `zip:90210` |
| `effective-date` | When the regulation took effect |
| `supersedes` | Prior regulation IDs this replaces (versioning) |
| `source-citation` | CFR / state code / county code / city code reference |
| `payload-schema` | If the regulation requires data exchange (Form 4473, NICS submission, AAFCO label), the schema |
| `cadence-tier` | Real-time / event / scheduled / annual (per [[infra-cadence-ladder]]) |
| `enforcement` | License suspension, fines, criminal liability, civil penalty |
| `case-type-link` | Which Hawk case fires when this interface trips |
| `verticals` | Which retail verticals this regulation affects |

## Geography sources (all public)

| Layer | Source |
|---|---|
| Parcel | USPS ZIP+4 product; county GIS systems (parcel boundaries) |
| City | Census TIGER/Line PLACE feature |
| County | Census TIGER/Line COUNTY feature |
| State | Census TIGER/Line STATE feature |
| Country | (constant: US) |

## Regulation sources (also all public)

| Domain | Sources |
|---|---|
| Firearms | ATF (CFR 27); state AG offices; NRA-ILA tracking; Giffords Law Center |
| Feed / AG | USDA AAFCO; state feed control acts (50 versions); FDA VFD |
| Pesticide | EPA pesticide registries; state pesticide control |
| Alcohol | TTB federal; state ABC; county dry/wet rolls |
| Hazmat | DOT; state environmental |
| Tobacco | RACS; FDA tobacco; state tobacco control |
| Health code | FDA food code; state/county health departments |

The data isn't hard to GET — it's hard to INDEX and RESOLVE. **That's the platform's job, not the merchant's.**

## Worked example: Murdoch's Ranch & Home Supply

A Murdoch's store in Bozeman, MT vs the same chain's store in Spokane Valley, WA:

| Regulation layer | Bozeman MT store | Spokane Valley WA store |
|---|---|---|
| Federal | ATF 4473/NICS/eBound; AAFCO; FDA VFD; EPA RUP | Same |
| State | MT firearm laws (open carry permissive); MT feed control act | WA SB-5078 (assault weapon ban as of 2026); WA feed control |
| County | Gallatin County | Spokane County |
| City | Bozeman ordinances | Spokane Valley ordinances |
| Parcel | Specific zoning | Specific zoning |

**The platform serves both stores from the same canonical database.** Federal rules apply at both. State rules diverge. The Bozeman store doesn't apply WA AWB; the Spokane store does. Cashiers see the right prompts, the right age-verification flow, the right form submissions, the right inventory restrictions — all without per-store config drift, because the resolver computes the applicable union at parcel resolution time.

## The agent UX (the support-call killer)

Operators at the store don't see a regulation matrix. They see:

- *"Customer is buying a 6-pack of beer. Scan ID for age verification (CA state law)."*
- *"This rifle requires a 10-day waiting period (CA law). Schedule pickup."*
- *"This pesticide requires RUP authorization (EPA federal + CA state). Confirm customer license."*

The agent ([[canary-store-brain]] + [[canary-compliance]]) reads the resolved regulation set and emits the right operator prompt at the right cadence, in operator language. **Bart's 20 years of "this customer in this state has this weird rule" tribal knowledge becomes the case-type registry; the geographic resolver makes it operational at every store automatically.**

## Differentiation

Vertical-specialist competitors handle compliance for ONE vertical (Coreware/AmmoReady for gun; Spruce for garden; Cellar Tools for liquor). **None of them resolve the federal/state/county/city/parcel layered set across multiple verticals.** NCR Counterpoint handles compliance via per-customer customization that doesn't generalize. Lightspeed and Heartland don't claim compliance as a rail at all. **Canary is the first SMB-targeted retail platform to make geographic compliance resolution a first-class architectural primitive** — and the only one that handles multi-vertical retailers (Murdoch's, Bart's gun + feed + AG customers) without per-vertical product forks.

## Composition with the platform

| Layer | Role |
|---|---|
| [[platform-parcel-as-anchor]] | Parcel is the resolution key |
| [[platform-federal-compliance-spine]] | Federal is the top (always-applicable) layer |
| [[canary-compliance]] | Module that hosts the resolver and registry |
| [[canary-field-capture]] | Semantic field mapping for regulation text |
| [[infra-cadence-ladder]] | Regulation update cadence (effective-date events, scheduled refreshes) |
| [[platform-case-type-registry-pattern]] | Each regulation can fire a Hawk case when tripped |

## Anti-pattern

Don't hardcode regulations into POS adapters. Don't put federal logic in the register. Don't manage state-by-state forks of the codebase. The regulation registry is the single source of truth; every adapter reads the resolved union via the resolver MCP tool.

## See also

- Card: [[platform-parcel-as-anchor]] — the parcel is the resolution key
- Card: [[platform-federal-compliance-spine]] — federal is the top layer
- Card: [[canary-compliance]] — module that hosts the resolver
- Card: [[canary-field-capture]] — semantic field mapping for regulation text
- Card: [[infra-cadence-ladder]] — regulation update cadence
- Template: `Brain/templates/regulation-spec.md` — per-regulation schema
- Source: TOM Property Pack — `Brain/raw/inbox/tom-top-down-design---property-pack-template-jul-06-v5.md`
- Cross-project prior art: Cove parcel mapping (Cove/cove/)
