---
date: 2026-04-20
type: moc
tags: [moc, coac, cove, bylaws, governance, compliance, roadmap, davis-stirling]
sources: [Cove/docs/archive/originals/transcriptions/bylaws-full.md, Cove/docs/archive/originals/transcriptions/2009-Restated-Declaration-Text.md, Cove/docs/archive/originals/governance/Bylaws_Modernization_Package.docx]
last-compiled: 2026-04-20
needs-review: 2026-05-04
---

# CoAC Bylaws & Governing Instruments — MOC

Map of content for the Community of Abalone Cove's two governing documents, the 2026 compliance gap, the proposed 2026 bylaws amendment, and the eventual successor Restated Declaration. Four documents, four different amendment paths, four different timelines.

## Quick Reference — The Four Documents

| Layer | Current | Status | Amendment path |
|---|---|---|---|
| **Real-property (recorded)** | [2009 Restated Declaration](../../Cove/docs/archive/originals/transcriptions/2009-Restated-Declaration-Text.md) | In force, recorded with LA County | 67% supermajority secret ballot, re-recorded; see [[cove-legal-framework]] |
| **Corporate (operations)** | [2012 Bylaws](../../Cove/docs/archive/originals/transcriptions/bylaws-full.md) | In force, under legacy "WPBCA" name | Majority secret ballot (no quorum); Bylaws §18.1 |
| **Corporate (articles)** | Articles of Incorporation (CA nonprofit mutual benefit, 1949 original + name-change amendment pending) | Active | Board + member approval; Corp §7810 |
| **Operating rules** | Various board resolutions | Variable | Board adoption + 28-day notice; Civ §4340–4370 |

---

## 1. Current State — What Binds Today

### 1.1 The 2012 Community Bylaws (Corporate Operations)

Adopted 2012-05-16 under the legacy name "West Portuguese Bend Community Association." 77 pages. Governs internal operations — elections, board duties, assessments, meetings, committees, financial controls. See [[cove-governance]] for the operational summary.

- **Verbatim text:** [[Cove/docs/archive/originals/transcriptions/bylaws-full|2012 Bylaws — Full Text]]
- **PDF original:** [[Cove/docs/archive/originals/governance/WPBCA-Bylaws-2012|2012 Bylaws — PDF]]
- **Modernization draft in progress:** `Cove/docs/archive/originals/governance/Bylaws_Modernization_Package.docx` (16KB, authored 2026-03-26)
- **Structural gaps:** See §2 below.

### 1.2 The 2009 Restated Declaration (Recorded CC&Rs)

Recorded 2009 with the Los Angeles County Registrar-Recorder. Runs with land; binds every successor owner of the 81 lots in Tract 14649. This is the **real-property instrument** — harder to amend (67% supermajority, secret ballot, court petition available under Civ §4275) and stronger than bylaws.

- **Verbatim text:** [[Cove/docs/archive/originals/transcriptions/2009-Restated-Declaration-Text|2009 Restated Declaration]]
- **PDF original:** [[Cove/docs/archive/originals/governance/2009-Restated-Declaration|2009 Restated Declaration — PDF]]
- **Predecessor layers (still binding where not superseded):** [[cove-legal-framework]] details the 1929 / 1949 / 1950 / 1952 chain — including [[Cove/docs/archive/originals/transcriptions/1929-Declaration-100-Basic-Protective-Restrictions-Verbatim|Declaration 100]], [[Cove/docs/archive/originals/transcriptions/1949-WPBCA-Declaration-No-One-Verbatim|Declaration No. One]], and the [[Cove/docs/archive/originals/transcriptions/1949-Declaration-of-Easements-Verbatim|1949 Declaration of Easements]] (Ocean Access).

### 1.3 Two Documents, One Community

Bylaws and the Restated Declaration are **different instruments with different enforcement weights**. Bylaws can be updated relatively cheaply; the Restated Declaration requires recording fees, title work, and supermajority approval. A full modernization touches both — and the bylaws typically move first because they can be cleaned up while the Restated Declaration waits for the right legal/political moment (see §4).

---

## 2. 2026 Compliance Gap — What's Broken in the 2012 Bylaws

### 2.1 Pre-2014 Davis-Stirling Citations (AB 805 Recodification)

Every citation in the 2012 Bylaws to Civ §1350–§1378 is **superseded**. AB 805 (2014) renumbered the entire Act. Old §1363.xx → current §4000+ / §5100+. A member reading the 2012 Bylaws today gets the wrong statute if they follow the citations. Lead compliance item. See [[cove-lessons-learned]] L-gov-5.

### 2.2 Post-2014 Amendments Not Reflected

| Law | Year | Effective | What it requires |
|---|---|---|---|
| **AB 502** | 2022 | 2023 | Election by acclamation permitted for uncontested seats (lower-cost elections) |
| **AB 2159** | 2024 | 2025-01-01 | Electronic secret-ballot voting (opt-in, hybrid with paper, excludes assessments) — **the statutory hook for Cove's e-voting system** |
| **AB 2460** | 2024 | 2025-01-01 | **Reconvened-meeting quorum drops to 20%** — directly relevant to the 2026-03-21 AGM quorum failure |
| **AB 130** | 2024 | 2025-01-01 | Fine cap $100/violation unless health/safety |
| **SB 900** | 2025 | 2026-01-01 | 14-day utility-repair response; emergency assessments without member vote |

The 2012 Bylaws reference none of these. Each one is a defense against challenge.

### 2.3 Cove Platform Integration Gaps

The 2012 Bylaws authorize "electronic or electromagnetic means for meetings" (§5.10) but don't define:

- **Electronic secret ballot procedure** — AB 2159 two-envelope analog, opt-in flow, paper-alternative availability
- **Lot-based email identity** — `{lot#}{Street}@abalonecove.org` as the canonical member channel (per [Cove CLAUDE.md](../../Cove/CLAUDE.md))
- **APN as primary identifier** — one vote per parcel, combined-lot rule explicit
- **Inspector of elections under electronic voting** — key custody, audit trail, chain-of-hash
- **Cove platform as the authorized system of record** — or the neutral framework that permits designating a system

Without these, Cove can operate governance features informally but cannot issue a legally binding certified election through the platform.

### 2.4 Internal Governance Gaps (per 2026-03-21 AGM Minutes)

From [[Cove/docs/archive/originals/governance/2026-03-21-CoAC-Annual-Meeting-Minutes|2026-03-21 Annual Meeting Minutes]]:

- **Indemnification clause** missing — trail maintenance creates liability; lawyer recommended adding. §9.1.1 of minutes.
- **HOA dues authority** — 2012 language "very specific," needs amendment to allow proposed increases (management company cost + reserves + trail maintenance). §9.1.2.
- **ARC language** — committee voted to amend bylaws and develop procedures conforming to state/city law. §6, §9.1.3.
- **Management-company authority** — no current framework; board wants to delegate treasurer functions. §4.2.
- **Quorum definition** — minutes describe 51% of 80 = 41 required; AB 2460 reconvened-quorum of 20% not referenced. Michele to follow up with counsel Jill David. §2.

### 2.5 Name: WPBCA → CoAC

The 2012 Bylaws, the recorded 2009 Declaration, and the Articles of Incorporation all say "West Portuguese Bend Community Association." The 2026-03-21 AGM minutes are headed "Community of Abalone Cove HOA." Name change is pending formalization — Articles amendment, bylaws update, and eventually a notice-of-name-change recorded with LA County for title-chain continuity. See [[abalonecove-org]].

---

## 3. Proposed 2026 Bylaws — What's Being Drafted

### 3.1 Board-Identified Amendments (2026-03-21 AGM, §9)

1. **Indemnification clause** — trail/easement liability protection
2. **HOA dues framework** — increase authority + structure
3. **Architectural Committee language** — procedure-enabling, state/city conformity
4. **Quorum amendments** — pull in AB 2460's 20% reconvened-meeting threshold

Lawyer estimate: 5–10 hours at $400/hr; $8,000 budgeted (20 hours). Counsel: Jill David.

### 3.2 Statutory Compliance Updates (Must-Haves)

- **AB 805 recodification** — rewrite every §1363.xx citation to current §4000+
- **AB 502** — election-by-acclamation procedure
- **AB 2159** — electronic secret-ballot procedure (the Cove hook)
- **AB 2460** — reconvened-meeting 20% quorum
- **AB 130** — fine schedule capped at $100 unless health/safety
- **SB 900** — emergency utility-repair assessment authority

### 3.3 Platform Enablement (Cove-Specific)

- Authorize electronic secret-ballot voting under AB 2159 by designating the governance system (Cove or successor) as the association's system of record
- Recognize lot-based email (`{lot#}{Street}@abalonecove.org`) as a valid Member Notice channel under Civ §4040
- Confirm APN as the primary parcel identifier; one vote per parcel
- Define the inspector-of-elections role under electronic balloting (independent third party, key custody, result certification)
- Permit hybrid paper + electronic balloting with member opt-in/opt-out per election cycle

### 3.4 Name & Entity

- Change all references from "West Portuguese Bend Community Association" to "Community of Abalone Cove" throughout
- Confirm governing-law cites: CA Nonprofit Mutual Benefit Corporation Law (Corp Code §§7110 et seq.); Davis-Stirling (Civ Code §§4000–6150)

### 3.5 Adoption Path

- Bylaws amendment requires **majority secret ballot**, no quorum (Civ §5100, old §1363.03)
- Notice: 30-day minimum for secret ballot
- Inspector of elections required; two-envelope system
- No re-recording needed (bylaws are internal; not recorded with LA County)
- Timeline: 60–90 days from drafting complete to certified adoption

**Gating dependencies:** AB 2460's new 20% reconvened quorum can itself be added by this amendment **before** the association tries to apply it — so the bylaw amendment is the vehicle to prevent a repeat of the 2026-03-21 quorum failure.

---

## 4. Next Recorded Instrument — Successor Restated Declaration

The 2009 Restated Declaration is the real-property instrument. A successor — call it the 2027+ Restated Declaration — is the big prize, but it is **gated on the city-issue landscape resolving first**.

### 4.1 Why Timing Matters

Re-recording a Restated Declaration while Case 24TRCP00352 (Community of Abalone Cove v. City of RPV) is pending, while the 0 Clipper Builder's Remedy is unresolved, and while the RPV Housing Element / HCD posture is still fluid risks locking in concessions or creating estoppel against positions the Community is actively litigating. See [[cove-0-clipper]], [[coac-rpv-housing-elements]], [[cove-rpv-planning-framework-2026]].

### 4.2 What Must Resolve First

| Issue | Vehicle | Status |
|---|---|---|
| 0 Clipper rezoning | Case 24TRCP00352 | Active — [[cove-0-clipper]] |
| Housing Site Inventory (Clipper Lot) | HCD review + RPV rezone action | Pending HCD |
| Landslide moratorium posture | RPV code + Coastal Commission | Stable but politically contested |
| Lot H scope correction | Title/declaration research | See [[claim-lot-h-scope-correction]] |
| Tract 14649 covenant chain | Internal — [[coac-reactivation-framework]] | Pre-positioning via Declaration 100 Article II §5 blitz |

### 4.3 Substantive Content — Already Being Scoped

The successor Restated Declaration framework exists in draft across the coac-* wiki set:

- [[coac-reactivation-framework]] — the overall strategic frame
- [[coac-restated-declaration-blitz-plan]] — the tactical rollout
- [[coac-declaration-100-article-ii-section-5]] — the specific amendment lever inside the Portuguese Bend-Filiorum covenant scheme
- [[coac-article-v-equity-modernization]] — modernizing the equity provisions
- [[coac-trustee-slate-preparation]] — slate for the reactivated structure
- [[coac-15-owner-network]] — the adjacent Declaration 100/101 owner network

The successor instrument should, at minimum:

1. Acknowledge and reference the landslide moratorium as an externally-recognized entitlement constraint (not just a city administrative filing) — per [[coac-rpv-housing-elements]]
2. Re-anchor the Ocean Access Easement language to current survey descriptions (County Surveyor books 28615, 28991 — see [[cove-legal-framework]])
3. Update the ARC framework to harmonize with the WPBCA / CoAC internal committee and the Palos Verdes Art Jury scheme where applicable — see [[coac-art-jury-vs-wpbca-arc]] · [[cove-art-jury-vs-wpbca-arc]]
4. Incorporate name change (WPBCA → CoAC)
5. Update enforcement mechanics for Davis-Stirling §5800+ compliance (modern CC&R enforcement, ADR, IDR)
6. Record cleanly with LA County so title insurers can underwrite without exception

### 4.4 Recording Strategy

- Re-recording requires 67% approval per existing Restated Declaration terms (and Civ §4270)
- Court petition under Civ §4275 is a fallback if approval falls between 50% and 67%
- Coordinate with title insurer on recording format (CC&R-style vs. supplementary declaration)
- Budget: title, recording fees, notary, attorney drafting — typically $15K–$30K for a community of this size

---

## 5. Document Hierarchy

The legal weight of each instrument, top to bottom:

1. **Recorded CC&Rs (Restated Declaration + predecessor declarations)** — real-property covenants, run with land, bind all successors, highest authority among private instruments
2. **Articles of Incorporation** — corporate-existence authority; amendment requires member vote + SOS filing
3. **Bylaws** — operational rules; amendment per bylaws' own terms (2012: majority secret ballot)
4. **Operating Rules / Board Resolutions** — administrative; board adoption + member notice; subordinate to all three above and to statute

Statute (Davis-Stirling + Corp Code + local ordinances) sits above all four and controls where they conflict.

---

## Related Wiki

- [[cove-governance]] — operational governance summary
- [[cove-legal-framework]] — CC&R chain history (1929 → 2009)
- [[cove-document-retention]] — record-keeping obligations across all four layers
- [[foundation-bylaws]] — separate 501(c)(3) Abalone Cove Foundation bylaws (parallel entity)
- [[cove-lessons-learned]] — L-gov-5 Davis-Stirling recodification
- [[cove-0-clipper]] — Case 24TRCP00352 and the gating city issues
- [[coac-reactivation-framework]] — strategic frame for the successor Restated Declaration
- [[coac-restated-declaration-blitz-plan]] — tactical rollout
- [[coac-declaration-100-article-ii-section-5]] — specific reactivation lever
- [[coac-15-owner-network]] — adjacent CC&R network

## Sources

- [[Cove/docs/archive/originals/transcriptions/bylaws-full|2012 Bylaws — Verbatim]]
- [[Cove/docs/archive/originals/transcriptions/2009-Restated-Declaration-Text|2009 Restated Declaration — Verbatim]]
- [[Cove/docs/archive/originals/governance/2026-03-21-CoAC-Annual-Meeting-Minutes|2026-03-21 AGM Minutes]]
- `Cove/docs/archive/originals/governance/Bylaws_Modernization_Package.docx` — in-progress modernization draft (2026-03-26)
- [Cove/CLAUDE.md](../../Cove/CLAUDE.md) — platform compliance table (AB 805, AB 502, AB 2159, AB 2460, AB 130, SB 900)
- California Civil Code §§4000–6150 (Davis-Stirling)
- California Corporations Code §§7110 et seq. (Nonprofit Mutual Benefit Corporations)
