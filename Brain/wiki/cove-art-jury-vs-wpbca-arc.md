---
type: wiki
tags: [cove, wpbca, arc, art-jury, declaration-100, governance, comparison, bylaws-2012]
created: 2026-04-19
sources: [Brain/raw/processed/council/2026-04-19-art-jury-vs-wpbca-arc.md, Cove/docs/archive/originals/transcriptions/bylaws-full.md, Cove/docs/archive/originals/transcriptions/1949-WPBCA-Declaration-No-One-Verbatim.md]
last-compiled: 2026-04-19
needs-review: 2026-05-03
---

# Art Jury (Declaration 100, 1929) vs. WPBCA Architectural Committee

Question: how does the 1929 Palos Verdes Art Jury — the original design-review body established under Declaration 100 — compare to the modern WPBCA Architectural Committee established under the 1949 WPBCA Declaration and refined in the 2012 Bylaws?

Answer: they are the same lineage with progressively narrower scope. The Art Jury was a peninsula-wide design authority with binding power over aesthetics and staffed by the AIA. The WPBCA ARC is a 3-member committee appointed by the HOA board with process obligations to Davis-Stirling, narrower jurisdictional reach (Tract 14649, 81 lots), and no mandate beyond its own declaration. The coercive mode has drained out. What remains is procedural.

## Side-by-side

| Dimension | Art Jury (Dec. 100, 1929) | WPBCA ARC (1949 Dec. + 2012 Bylaws) |
|---|---|---|
| **Jurisdiction** | All of Lot H — non-PVE peninsula | Tract 14649 only — 81 lots |
| **Body size** | 5 members | 3 members |
| **Composition** | 1 PV Corp nominee + 1 Association board nominee + 3 from AIA Southern California Chapter | 3 members appointed by the Board. No professional qualifications required in the declaration. "No member of said Committee need be a member, director or officer of the Association." |
| **Terms** | Staggered 1/2/2/3/3 then 3-year terms | Set by the Board |
| **Scope of review** | Construction, exterior alterations, color changes, signs, landscaping, and "works of art" | Accessory buildings, building setbacks, heights, grading, excavation, trees/shrubs >6ft, billboards/signs, clothes-drying enclosures, resubdivision readjustments |
| **Authority** | Binding on the Association and not subject to override | Subject to appeal: ARC → Board → Membership |
| **Appeals process** | None specified | Formal three-step ladder with deposit-of-costs rules, meeting notice, extensions |
| **Procedural obligations** | Approvals in writing | Civil Code §§ 4765 compliance: completeness determination, open meetings, receipt of comments, written decision, time limits |
| **Rule-making** | May promulgate regulations | May promulgate Architectural Rules as Governing Documents |
| **Financial authority** | Appointed a trust company as Treasurer; held property | "Expenditures by ARC" — bounded by Board |
| **Duration / force** | Until Jan 1, 1965, auto-renewing 20-year terms — currently in force through Jan 1, 2045 | Continuing under the Association's Governing Documents |
| **Membership pool** | AIA Southern California Chapter (practicing architects) | Any three people appointed by the Board |
| **Annual disclosures** | None | Must annually disclose Architectural Review and Approval Procedures to members (Bylaws §13.17) |
| **Required brochure** | None | ARC Brochure for Members required (Bylaws §16.5) |

## Structural observations

**The Art Jury was a design court.** Its decisions were binding and not appealable. It was staffed by a professional body (AIA SoCal). It had property authority through its trustee. It was the aesthetic conscience of the peninsula, by construction.

**The WPBCA ARC is a process function.** The 2012 Bylaws re-cast it through the lens of Civil Code obligations. Completeness determinations. Open meetings. Time limits. Written rulings. Appeals to the Board. Appeals to the Membership. Annual notice of procedures. A member brochure. The body exists; what it actually does is run a procedure that terminates in a written decision with documented appeal rights.

**The AIA composition didn't survive.** The 1929 Art Jury was specifically designed to put architectural professionals in the review seat. The 1949 WPBCA declaration dropped that requirement. The 2012 restatement did not restore it. This is the single biggest structural change — design-review authority transferred from a professional body to an HOA board's appointees, with no required expertise.

**Scope shrank but enumeration grew.** The Art Jury reviewed "construction, exterior alterations, color changes, signs, landscaping, and works of art" — broad categories. The WPBCA enumerates narrower items: setbacks, heights, trees over six feet, clothes-drying enclosures. The list reads like residue: specific 1940s-era concerns preserved verbatim into 2012.

**The appeals ladder is the most modern feature.** The Bylaws' ARC → Board → Membership appeal sequence, with cost deposits and time extensions, reflects Davis-Stirling's procedural emphasis. Nothing like it exists in Declaration 100.

## Why this matters for the Cove ARC module

The module doesn't have to invent ARC process. **The process already exists and is well-specified in the 2012 Bylaws §16.** The module's job is to *operationalize* what the Bylaws already require:

1. **Completeness determination (§16.4.1)** — the plugin's readiness check is literally this step. It tells the owner whether their application would be deemed complete.
2. **Open meeting scheduling (§16.4.2)** — the concierge view needs to surface in-flight applications and scheduled reviews.
3. **Written decision with time limits (§16.4.3–§16.4.4)** — each ARC file should store the written decision as a durable artifact keyed to the APN.
4. **Appeals (§16.4.5–§16.4.9)** — the file should track appeal status, deposits, extensions. Rare, but when it happens the record matters most.
5. **Annual Notice of Procedures (§13.17)** — the module can generate this notice automatically from the configured process. It's a yearly compliance artifact the Board has to produce anyway.
6. **ARC Brochure (§16.5)** — the "Remodel Readiness Playbook" we've been calling a consultant deliverable *is* the ARC Brochure, properly understood. Publishing it satisfies a Bylaws requirement.

This is the reframe: the Cove ARC module is not inventing a new posture for the ARC. It is **systematizing what the Bylaws already require** and making those obligations easy to meet.

## What the Art Jury comparison teaches

- **Don't re-grandify the ARC.** The Art Jury's authority came from AIA composition and binding rulings. WPBCA chose not to inherit either. The module should not simulate authority the Bylaws explicitly declined to grant.
- **The Bylaws' procedural machinery is the asset.** Completeness checks, open meetings, time limits, written decisions, appeal ladder — these are well-defined obligations the Board already has to meet. The module makes meeting them trivial.
- **Annual disclosures are a forcing function.** §13.17 and §16.5 require the ARC to publish its own procedures and a member brochure. Those are the actual deliverables the Bylaws are waiting for.
- **The ocean-access easements (§2.19.1, §2.19.2)** are ARC-adjacent artifacts that belong in the neighborhood reference library with careful visibility — the ocean path easement is a sensitive private WPBCA matter, Foundation does neutral documentation only. The module inherits that boundary.

## What to build into the Cove ARC module

- **Application intake** mapped to Bylaws §16.4 procedural steps
- **Completeness readiness report** (§16.4.1) as a first-class output
- **Written decision storage** per APN, with appeal status tracking
- **Annual Notice of Procedures** generator (§13.17)
- **ARC Brochure** generator (§16.5) — the Playbook is this artifact
- **Per-APN ARC file** as the durable record across permit cycles and owner turnovers
- **Neighborhood reference library** with explicit sensitivity tiers (ocean-path easement off-limits by default)

## The one-line read

> The Art Jury was a peninsula-wide design court staffed by architects. The WPBCA ARC is a 3-person HOA committee running a statutorily-defined process. The module's job is to run the process well, not to re-aspire to the court.

## Related

- [[cove-declaration-100]] — the 1929 framework that established the Art Jury
- [[cove-pv-declaration-scheme]] — Olmsted legacy, Declaration 100/101, the coverage gap
- [[cove-arc-posture]] — the settled WPBCA ARC posture (2026-04-19)
- [[cove-legal-framework]] — CC&R chain and enforcement authority
- [[seacove-arc-module]] — Cove ARC module design

## Primary Sources

- [[Cove/docs/archive/originals/founding/1950-12-26-arc-declaration-exercise-of-power-of-appointment-doc-1182|1950-12-26 ARC Declaration — Exercise of Power of Appointment (Doc 1182)]] — **foundational ARC instrument** signed by Frank A. Vanderlip Jr. (President, Palos Verdes Corporation) on Nov 20, 1950. Establishes the Architectural Committees under the Declarations of Protective Restrictions. References predecessor Portuguese Bend Declaration No. One (Aug 22, 1947, Book 24966, Tract 14118) and Declaration No. Two (Nov 8, 1948). Confirms "Portuguese Bend Community Association" (WPBCA predecessor) existed as early as 1947.
- [[Cove/docs/archive/originals/founding/1954-04-13-arc-members-appointment-tracts-14118-14649-doc-3529|1954-04-13 ARC Members Appointment (Doc 3529)]] — PV Corp's subsequent ARC appointment covering BOTH tracts (14118 under 1947 declaration, 14649 under 1949 declaration). Demonstrates periodic PV Corp use of recording apparatus for ARC management.
