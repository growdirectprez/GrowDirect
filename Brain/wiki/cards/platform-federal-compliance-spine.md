---
card-type: platform-thesis
card-id: platform-federal-compliance-spine
card-version: 1
domain: platform
layer: cross-cutting
status: approved
agent: ALX
tags: [federal-compliance, atf, usda, fda, epa, ttb, dot, registry-as-data, public-standards, adoption-pattern, dsg-prior-art, differentiation]
last-compiled: 2026-05-02
needs-review: false
---

# Pattern: Federal Compliance Spine

## What this is

Federal compliance for retailers is a registry of public, documented protocols. ATF Form 4473, NICS eCheck, ATF eBound Book, ATF Form 3310 (multi-handgun sale reporting), USDA AAFCO feed labeling, FDA VFD (Veterinary Feed Directive), EPA pesticide RUP authorization, TTB alcohol reporting, DOT hazmat — all of these are federal protocols whose specifications are publicly available. **Canary adopts each protocol verbatim into the interface registry and case-type registry** — no reverse engineering, no vendor lock, no proprietary IP exposure. Same composition-over-invention pattern as ARTS POSLog adoption for retail data interchange.

## Purpose

Federal compliance is a high-stakes domain (license suspension, fines, criminal liability) that retailers handle today via a mix of: vendor-specific compliance products (4473 Cloud for firearms, ShipCompliant for alcohol shipping), in-house manual processes (Bart's 60+ field staff), and Counterpoint customizations layered over 41 years. The federal compliance spine collapses that into a clean adoption pattern — one canonical registry entry per federal protocol, one Hawk case-type for each compliance event, one MCP tool per protocol interaction.

## The adoption rule

> **If it's federal, it's documented. Adopt the standard verbatim. Same as ARTS.**

Two corollaries:

1. **No proprietary fork.** Canary doesn't extend or wrap federal protocols beyond what the protocol itself specifies. If the ATF e4473 schema requires fields A, B, C, our protocol carries fields A, B, C — not "Canary's version of e4473."
2. **No reverse engineering.** Federal protocols are public. The CFR text is public. The forms are public. The submission endpoints (NICS eCheck, AAFCO state portals) are documented. We read the documentation; we don't decompile vendor products.

## Federal compliance scope (Murdoch's-class proof case)

| Federal area | Protocol / form | CFR / source | Adoption lever |
|---|---|---|---|
| ATF firearms | Form 4473 (Firearms Transaction Record) | 27 CFR 478.124 | Adopt schema; partner with 4473 Cloud for storage; native field validation |
| ATF firearms | NICS eCheck | 28 CFR 25 | Adopt API; sit between register and FBI |
| ATF firearms | eBound Book (Acquisition & Disposition log) | 27 CFR 478.121–.125 | Adopt bound-book schema; native ledger; Fox-anchored |
| ATF firearms | Form 3310.4 / 3310.12 (multi-firearm sale) | 27 CFR 478.126a | Adopt 3310 schema; auto-generate from sale events meeting threshold |
| ATF firearms | FFL transfer + private-party transfer | 27 CFR 478.125 | Adopt FFL transfer protocol |
| USDA / state ag | AAFCO feed labeling | 21 CFR 501 + state-specific | Adopt AAFCO label schema; per-state overlay (50 versions) |
| FDA / USDA | VFD (Veterinary Feed Directive) | 21 CFR 558 | Adopt VFD electronic format |
| TTB | Alcohol federal reporting | 27 CFR 31 | Already partial via ShipCompliant integration |
| EPA | Pesticide retailing (RUP authorization) | 40 CFR 171 | Adopt EPA RUP licensing schema |
| DOT | Hazmat retailing | 49 CFR 172 | Adopt DOT placard schema |
| FDA | Tobacco / RACS retailer compliance | 21 CFR 1140 | Adopt RACS compliance schema |

This is the starter set for Murdoch's vertical mix (firearms + feed + AG + alcohol + hazmat). Other verticals add or subtract from this set.

## Composition with the platform

| Layer | Federal compliance role |
|---|---|
| [[platform-parcel-as-anchor]] | Federal applies to every parcel; no geo-resolution needed at federal layer |
| [[platform-geographic-compliance-resolver]] | Federal is the top (always-applicable) layer of the resolver |
| [[platform-case-type-registry-pattern]] | Each federal protocol can fire a Hawk case (Missing 4473, NICS denial follow-up, VFD attestation, RUP renewal) |
| [[canary-compliance]] | Module that hosts federal interface adapters and registry |
| [[canary-fox]] | Federal-protocol events anchor to Fox |
| [[canary-blockchain-anchor]] | Federal-event anchors land on Bitcoin L2 (audit-grade) |

## Prior art (commercial-grade, production-proven)

The DSG Loss Prevention Management System (~2015, 700+ stores) ran several federal-firearms case types **in production**:

- **Missing F4473** — flag a gun sold without a recoverable 4473 form
- **Firearms 4473 Violation** — 4473 review reveals associate violation
- **Inspection: Firearms** — ATF compliance audit at the location
- **Unaccounted for Firearm** — firearm booked to location cannot be located
- **Straw Purchase** — third-party-attempted purchase circumvention
- **Reported to ATF** — closure outcome that escalates to law enforcement

These map directly to the Hawk case-type registry. **The federal-compliance spine inherits a commercially-proven catalog for the firearms vertical**, not a theoretical model. See `Brain/raw/.extract/CaseManagement/Incident Types.xlsx.md` for the full source.

## Differentiation

Vertical specialists handle federal compliance for ONE vertical (Coreware/AmmoReady for gun, Cellar Tools for liquor). Each invests deep federal-vertical knowledge but doesn't generalize. Counterpoint handles federal compliance via per-customer customization (50+ integrations including 4473 Cloud, ShipCompliant, RACS — the integration tax). NCR Voyix, Lightspeed, Heartland don't claim federal compliance as a rail.

**Canary is the first SMB retail platform to package federal-compliance adoption as a first-class registry primitive across all regulated verticals simultaneously.** Combined with parcel-anchored geographic resolution for state/county/city layers, the result is a unified compliance surface no competitor has built. The DSG production-proven catalog for firearms is the credibility moat — the founder's team built and deployed it; we're not theorizing.

## Anti-pattern

Don't build a "compliance feature" per vertical. Don't fork federal protocols into vendor variants. Don't hide federal protocol details inside POS adapters. The registry is the single source of truth; every protocol is adopted once at the platform layer; every register reads the resolved set via the resolver MCP tool.

## See also

- Card: [[platform-geographic-compliance-resolver]] — federal is one layer of the resolver
- Card: [[platform-parcel-as-anchor]] — every store's parcel inherits federal automatically
- Card: [[canary-compliance]] — hosts federal protocol adapters
- Card: [[platform-architectural-continuity]] — the adoption rule (compose, don't invent) is its general form
- Card: [[platform-case-type-registry-pattern]] — federal protocols fire Hawk cases
- Card: [[canary-hawk]] — universal case envelope; federal compliance cases instance here
- Source: DSG LPMS firearm case types — `Brain/raw/.extract/CaseManagement/Incident Types.xlsx.md`
- Source: TOM Property Pack — `Brain/raw/inbox/tom-top-down-design---property-pack-template-jul-06-v5.md`
