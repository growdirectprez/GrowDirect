---
type: wiki
tags: [cove, lessons-learned, ledger, governance, permits, legal, land-use, habitat, community, cross-cutting]
created: 2026-04-19
sources:
  - Brain/wiki/cove-rpv-planning-framework-2026.md
  - Brain/wiki/cove-case-law-lessons.md
  - Brain/wiki/cove-endangered-species-constraints.md
  - Brain/wiki/cove-rpv-safety-element-2018.md
  - Brain/wiki/cove-legal-framework.md
  - Brain/wiki/cove-colyear-2024.md
  - Brain/wiki/coac-rpv-housing-elements.md
  - Brain/wiki/cove-lot-h-discovery.md
  - Brain/wiki/claim-lot-h-scope-correction.md
  - Brain/wiki/coac-pv-endangered-species.md
status: ledger
visibility: internal
last-compiled: 2026-04-19
needs-review: 2026-07-19
---

# Cove Lessons Learned — Running Ledger

Dense, domain-organized ledger of lessons that survive past session. Each entry: **lesson** — *how we know* — link. Keep entries tight. No prose. Append; do not rewrite.

Format: `L-<domain>-<n>. Lesson statement. — How we know: <source>. → [[wiki]]`

## Governance

- **L-gov-1.** WPBCA enforcement standing is clean inside Tract 14649 and doubtful outside it. — How we know: [[cove-colyear-2024]] + [[claim-lot-h-scope-correction]]. → [[cove-case-law-lessons]] R17/R18.
- **L-gov-2.** The 1950 Lot H Declaration's only substantive content was a racial covenant, now void under Cal. Civ. Code § 12955. It provides no enforceable building controls. — How we know: [[claim-lot-h-scope-correction]] confirmed April 2026. → [[cove-case-law-lessons]] R7.
- **L-gov-3.** Secret-ballot separation is non-negotiable: the `ballots` table has no `member_id` column; link via `ballot_envelopes` sealed by PostgreSQL RLS. — How we know: Cove/CLAUDE.md hard rule; Davis-Stirling §5100–5145. → [[cove-governance]].
- **L-gov-4.** APN is the primary key for every Cove entity (parcel → member → vote; parcel → assessment; parcel → ARC application). — How we know: Cove/CLAUDE.md architecture rule. → [[cove-platform]].
- **L-gov-5.** Davis-Stirling was recodified in 2014 (AB 805): old §1350–1378 → §4000+; every pre-2014 bylaw reference is outdated. — How we know: Cove/CLAUDE.md legislative table. → [[cove-governance]].
- **L-gov-6.** Reactivation work under Declaration 100 Article II §5 is surprise-based and intentionally private-until-board-authorized. `coac-*` reactivation articles are not Foundation public voice. — How we know: feedback memory + [[coac-reactivation-framework]]. → [[coac-reactivation-framework]] (visibility: private).
- **L-gov-7.** Ocean path easement is a private WPBCA governance matter (Hollister/Bixby parallel). Foundation does neutral archival documentation only; no public voice. — How we know: feedback memory + [[wpbca-ocean-path-easement]]. → [[wpbca-ocean-path-easement]] (visibility: private).

## Permits / ARC

- **L-arc-1.** ARC posture is concierge + transparency: city permits the work; ARC helps members through the city's process. ARC is not a parallel reviewer. — How we know: [[cove-arc-posture]]. → [[cove-arc-posture]].
- **L-arc-2.** 1929 Art Jury (Dec. 100, AIA-staffed, binding) differs from 2012 Bylaws ARC (3 appointees, Davis-Stirling process). Operationalize the 2012 framework; the 1929 framework is historical. — How we know: [[cove-art-jury-vs-wpbca-arc]]. → [[cove-art-jury-vs-wpbca-arc]].
- **L-arc-3.** The 40-foot bluff setback in Declaration One-A (1950) is now validated by the 2018 Safety Element §5.9 Coastal Cliff Retreat. Private restriction aligned with municipal finding. — How we know: [[cove-rpv-safety-element-2018]] §5.9. → [[cove-rpv-planning-framework-2026]].
- **L-arc-4.** WPBCA parcels on the upland margin fall within Very High Fire Hazard Severity Zone. Fuel modification under Safety Element Policy 4 is legally enforceable on private property and overrides ARC aesthetic preferences. — How we know: [[cove-rpv-safety-element-2018]] §3. → [[cove-rpv-planning-framework-2026]].
- **L-arc-5.** Expedited review exists for reconstruction of fire-damaged structures. — How we know: [[cove-rpv-safety-element-2018]] §2 Policy 5. → [[cove-rpv-safety-element-2018]].
- **L-arc-6.** Emergency-access obligations apply to cul-de-sacs and narrow streets (Sea Cove, Packet, Barkentine, Clipper, Peppertree). ARC applications affecting street width or driveway spacing should verify against Safety Element §8 before approval. — How we know: [[cove-rpv-safety-element-2018]] §2 Policy 11 + §8. → [[cove-rpv-safety-element-2018]].

## Legal / Case law

- **L-legal-1.** CC&Rs are presumed valid; the burden of proving unreasonableness falls on the challenger. — How we know: *Nahrstedt v. Lakeside Village* (1994) 8 Cal. 4th 361. → [[cove-case-law-lessons]] R1.
- **L-legal-2.** Restrictions recorded in the chain of title bind all subsequent purchasers. Restrictions not in the chain don't. — How we know: *Citizens for Covenant Compliance v. Anderson* (1995) + *Colyear v. RHCA* (2024). → [[cove-case-law-lessons]] R2/R5.
- **L-legal-3.** Extrinsic evidence of PV Corp's intent cannot cure a recording defect. — How we know: *Colyear* (2024). → [[cove-case-law-lessons]] R6.
- **L-legal-4.** Kelvin Vanderlip admitted in November 1947 that PVC attorneys stripped provisions from later declarations starting with the Flying Triangle Declaration (160, 1939) "for the purpose of simplification." The master General Plan was broken on purpose. — How we know: [[cove-colyear-2024]]. → [[cove-case-law-lessons]].
- **L-legal-5.** Inverse condemnation under CA Const. Art. I §14 is independent of common-law tort. A public entity is liable for damage caused by public improvements regardless of negligence, if the damage is the necessary effect of operation. — How we know: *Albers v. County of Los Angeles* (1965) 62 Cal. 2d 250. → [[cove-case-law-lessons]] R9.
- **L-legal-6.** The 1946 federal geological report on the Portuguese Bend prehistoric slide plane "was known to both the county and the developers." The city cannot plead ignorance about landslide hazard. — How we know: *Albers* (1965) opinion. → [[cove-case-law-lessons]] R10.
- **L-legal-7.** Landslide moratorium is a legally defensible "not buildable" designation. — How we know: *Monks v. City of Rancho Palos Verdes* (2008) 167 Cal. App. 4th 263. → [[cove-case-law-lessons]] R11.
- **L-legal-8.** Builder's Remedy constrains government zoning, not private covenants. — How we know: Gov. Code § 65589.5; [[cove-legal-framework]] statutory analysis. → [[cove-case-law-lessons]] R14.
- **L-legal-9.** No California law currently preempts pre-existing CC&Rs for this project (HE/RHNA, BR, SB 9, AB 721, §4751, AB 1050, Coastal Act). CC&R-vs-HE-rezoning is a case of first impression. — How we know: [[cove-legal-framework]]. → [[cove-case-law-lessons]] R8.
- **L-legal-10.** RPV residents filed SCOTUS cert petitions on city land-use matters in 1994 (Stuart), late 1990s (Teng Lee), and 2001 (Echevarrieta). 23-year arc of community-vs-city friction predates current work. — How we know: [[coac-rpv-scotus-petitions]]. → [[cove-case-law-lessons]] R15/R16.
- **L-legal-11.** The "litigation-hold secret meetings" vector was raised by an RPV resident in 1994 (Stuart Q5) and is the same line behind the 2024 Cruikshank FPPC complaint. Not novel politics — 30-year pattern. — How we know: [[coac-rpv-scotus-petitions]] + 2024-08-07 FPPC complaint transcription. → [[cove-case-law-lessons]] R15.
- **L-legal-12.** *Colyear* (2024) was certified for partial publication. Unpublished reasoning is not safe to cite under CA citation rules. — How we know: [[cove-colyear-2024]] opinion header. → [[cove-case-law-lessons]] C3.

## Land use / Planning

- **L-lu-1.** The city's own 1990 and 2001 Housing Elements explicitly designated Portuguese Bend / moratorium parcels as "Not buildable" and assigned them zero RHNA capacity. Estoppel-style argument lives here against current BR upzoning. — How we know: [[coac-rpv-housing-elements]] verbatim inventory entries. → [[cove-rpv-planning-framework-2026]].
- **L-lu-2.** The 1975 General Plan defined 9 resource-management overlays (RM-1 through RM-9). WPBCA parcels along the bluff fall into RM-1 (Sea Cliff Erosion), RM-3 (High Slopes), RM-4 / RM-5 (Active / Old Landslide), and RM-7 (Marine Resource) simultaneously. These overlays are citable in Restated Declaration recitals. — How we know: [[coac-1975-general-plan-eir]]. → [[cove-rpv-planning-framework-2026]].
- **L-lu-3.** The Coastal Specific Plan (1978, GP-A3 → Resolution 78-81) — Subregion 4 covers Abalone Cove. View corridors, beach access, coastal-zone standards. Independent of the Coastal Commission but subject to CCC concurrence. — How we know: [[coac-1975-general-plan-eir]] amendment trail + [[cove-coastal-specific-plan-s4]]. → [[cove-rpv-planning-framework-2026]].
- **L-lu-4.** The 0.57-acre creek / flood hazard area at 0 Clipper is identified as "habitat area in excellent condition" in the Coastal Specific Plan. Citable anchor for the PVPLC conservation-easement ask. — How we know: [[cove-pvplc-partnership]] + Coastal Specific Plan Policy 4 sources. → [[cove-pvplc-partnership]].
- **L-lu-5.** The Portuguese Bend landslide's **upper boundary** is explicitly under debate in the 2018 Safety Element (Valley View Graben vs. Dibblee 1999 interpretations). The city cannot quietly push the boundary downslope to free up upzoning capacity — its own element preserves the uncertainty. — How we know: [[cove-rpv-safety-element-2018]] §5.3. → [[cove-rpv-safety-element-2018]].
- **L-lu-6.** Landslide moratorium was made **permanent** in 2025. Defensive asset (can't quietly lapse) and tension point (state RHNA pressure doesn't defer to it). — How we know: [[cove-pvplc-partnership]] timeline entry. → [[cove-rpv-planning-framework-2026]].
- **L-lu-7.** Palos Verdes Fault maximum-credible-earthquake is Mw 7.3 at 0.691g PGA, Modified Mercalli XI, at 1–4 miles distance — on the city's own record as of 2018. — How we know: [[cove-rpv-safety-element-2018]] §5.1 Table 1. → [[cove-rpv-safety-element-2018]].
- **L-lu-8.** City control ≠ WPBCA control. City permits what can be built; WPBCA enforces CC&Rs on what members may build on Tract 14649 lots. Neither preempts the other — this is the foundation of the 0 Clipper defense posture. — How we know: [[cove-legal-framework]] + [[cove-rpv-planning-framework-2026]]. → [[cove-rpv-planning-framework-2026]].

## Habitat / Species

- **L-hab-1.** Palos Verdes blue butterfly (*Glaucopsyche lygdamus palosverdesensis*) is federally endangered. Any project affecting deerweed (*Lotus scoparius*) or *Astragalus trichopodus* host-plants triggers Section 7 or Section 10 review. — How we know: [[coac-pv-endangered-species]] + 2005 pupae-salvage paper. → [[cove-endangered-species-constraints]].
- **L-hab-2.** PVPLC is the NCCP Habitat Manager for the 1,400-acre PV Nature Preserve and holds 1,700 acres across the Peninsula. Natural partner for Sub Region 4 implementation, adjacent to Abalone Cove. — How we know: [[cove-pvplc-partnership]]. → [[cove-endangered-species-constraints]].
- **L-hab-3.** Filiorum Reserve (191 acres) is named after the Filiorum Corporation — the Vanderlip land-holding entity that incorporated Declarations 100 and 101 via the 1930 grant deed (Book 10226, Page 170). The family's speculation vehicle became a nature preserve. — How we know: [[cove-pvplc-partnership]]. → [[cove-pvplc-partnership]].
- **L-hab-4.** RPV adopted NCCP/HCP in 2019. Compliance is a condition for covered activities within the planning area. — How we know: [[cove-pvplc-partnership]] timeline. → [[cove-endangered-species-constraints]].
- **L-hab-5.** Rule of thumb: if a scope touches native vegetation anywhere near Portuguese Bend, Abalone Cove Reserve, Filiorum Reserve, or the Three Sisters corridor, consult PVPLC and assume NCCP compliance review. Pre-consultation is cheap; surprise enforcement is not. — How we know: [[cove-endangered-species-constraints]] default rule. → [[cove-endangered-species-constraints]].
- **L-hab-6.** *Phillippe v. Shapell* (1987) — a 1973 Filiorum land purchase failed "due to geological problems." Shapell walked; 51 years later Clipper Development bought adjacent land. Same geology, different answer. — How we know: [[cove-colyear-2024]]. → [[cove-case-law-lessons]] R12.

## Community / Context

- **L-com-1.** WPBCA was incorporated in 1949 (Tract 14649) — 81 lots across Sea Cove, Packet, Barkentine, Clipper, Peppertree. Two private ocean-access easements (1949/1952, Sea Cove Dr to Pacific) are the critical community asset. — How we know: Cove/CLAUDE.md community context + [[cove-legal-framework]]. → [[cove-community-history]].
- **L-com-2.** Dues are <$20/month as of 2026; WPBCA is severely underfunded. — How we know: Cove/CLAUDE.md. → [[cove-governance]].
- **L-com-3.** Baughey 1947 — PV Corp's own staff historian wrote the official corporate history 34 years after Vanderlip's purchase. Primary source for chain of title Dominguez (1784) → Sepulveda → Bixby → Vanderlip. — How we know: [[cove-baughey-1947]]. → [[cove-baughey-1947]].
- **L-com-4.** Vanderlip "conducted all of the negotiations and assumed full responsibility in the purchase of Rancho Palos Verdes, closed the deal without first having seen the property." — PV Corp's own officer. — How we know: [[cove-baughey-1947]] verbatim. → [[cove-baughey-1947]].
- **L-com-5.** Cabrillo (1542) named the area "The Bay of Smokes" — smoke attributed to fires set by Indians (rabbit hunting or welcoming signal). Baughey: "Cabrillo, among other 'firsts,' was the first visitor to our shores to be greeted by smog." — How we know: [[cove-baughey-1947]]. → [[cove-baughey-1947]].

## Interview findings — not present

No interview transcripts are in the vault as of 2026-04-19. When interviews are recorded and transcribed, append a **Interview Findings** section here organized by subject, each finding tagged `[confirms | contradicts | adds | open]` with link to the relevant wiki article. See Phase 4 section of the synthesis session report for the framework; [[cove-interview-findings]] article not yet created because no source exists to harvest.

## Open contradictions / judgment calls flagged

### OC-1 — Carlsbad ruling citation needed

Referenced in spec commit 5721905 as bearing on HOA enforcement paralysis. No source in vault. Needs citation and pull before any rule is built on it. — Source: commit log. → [[cove-case-law-lessons]] C1.

### OC-2 — SCOTUS docket status on Stuart / Teng Lee / Echevarrieta

[[coac-rpv-scotus-petitions]] presumes cert denial but does not confirm. Materially changes R13 strength. — Source: [[coac-rpv-scotus-petitions]] open thread. → [[cove-case-law-lessons]] C2.

### OC-3 — *Colyear* published-vs-unpublished scope

Before citing *Colyear* in any brief, confirm which portions are published. — Source: [[cove-colyear-2024]] — "Certified for partial publication." → [[cove-case-law-lessons]] C3.

### OC-4 — Current HCD certification status for RPV 6th-cycle HE

Builder's Remedy applicability depends on certification status. Pull the current HCD letter before any strategic decision. — Source: [[cove-rpv-planning-framework-2026]] ambiguity #1.

### OC-5 — 2024 HE sites inventory treatment of moratorium parcels

Whether the 6th cycle preserves the 2001 "Not buildable" zero-capacity treatment or assigns partial capacity under HCD pressure. Pull the sites inventory spreadsheet. — Source: [[cove-rpv-planning-framework-2026]] ambiguity #2 + [[coac-rpv-housing-elements]].

## Cross-references

- [[cove-rpv-planning-framework-2026]]
- [[cove-case-law-lessons]]
- [[cove-endangered-species-constraints]]
- [[cove-rpv-safety-element-2018]]
- [[cove-legal-framework]]
- [[cove-governance]]
- [[cove-pvplc-partnership]]
- [[cove-baughey-1947]]
- [[cove-colyear-2024]]
- [[coac-rpv-housing-elements]]
- [[coac-pv-endangered-species]]
- [[coac-rpv-scotus-petitions]]
- [[cove-lot-h-discovery]]
- [[claim-lot-h-scope-correction]]

## Append discipline

When adding new lessons:
1. Use the exact `L-<domain>-<n>` format (governance, arc, legal, lu, hab, com; add new domains only if genuinely new).
2. One sentence lesson + one-phrase "how we know" + one link.
3. No prose. No narrative. No "furthermore" or "importantly."
4. Open contradictions get OC-numbered entries until resolved; then move resolution into the relevant lesson and delete the OC entry.
5. Never rewrite existing lessons — supersede with a new numbered lesson that references the old one if the old understanding changed.
