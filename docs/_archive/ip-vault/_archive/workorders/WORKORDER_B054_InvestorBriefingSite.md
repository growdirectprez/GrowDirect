---
type: workorder
domain: business
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Work Order: B-054 — Investor Briefing Site (Password-Protected)
*Issued by: ALX | February 27, 2026 | Approved by: Jeffe*
*Classification: MAXIMUM CONFIDENTIAL*
*Routes to: Jess (primary build), PhD (section copy), Syd (legal review), Art (landing page link)*

---

## Directive

Jeffe directive (Feb 27): Build an expanded investor briefing site based on `growdirect_investor_1.html`. Single self-contained HTML. Password-protected. Incorporates B-053 compliance slide content, PhD briefs, and curated content from Work Order output files. This is THE investor package.

**Architecture:**
- **Public face:** `growdirect.io` landing page (already in git: `_ALX/WorkOrders/output/Art/growdirect-site/index.html`) — stays as-is
- **Gate:** "Learn More" button on landing page → navigates to password-protected investor briefing
- **Private:** Expanded `growdirect_investor_1.html` — the full package behind the password

**North Star:** This site must reduce investor cognitive load. One page. One password. The full story. No PDF attachments, no "let me send you the deck" — this IS the deck.

---

## Source Template

**File:** `/mnt/uploads/growdirect_investor_1.html`
**Password:** `eljeffe2026` (client-side JS gate — Syd to advise if this needs upgrading)

### Current Sections (keep all — expand where noted)
1. **Gate** — Password entry (keep as-is, Syd reviews password strength)
2. **01 — The Problem** — "The Record Is Broken" (3 cards: Polling Gaps, Mutable Records, Trust Required)
3. **02 — The Solution** — "Capture. Seal. Inscribe." (3 steps + 6-node pipeline + 4 moat cards)
4. **03 — The Economy** — Closed loop SVG diagram + 4 ownership tiers
5. **04 — The Market** — Beachhead stats + competitive comparison
6. **05 — The Vision** — 6 use cases (universal protocol)
7. **06 — What's Built** — Metrics + checklist + protection cards + closing

### New Sections to Add

**Section 2.5 (after Solution, before Economy):**
### 02b — Compliance by Construction
*Source: B-053 work order output (PhD brief + Syd-approved language)*

Content:
- The argument: El Jeffe eliminates the attack surface that compliance standards were designed to protect
- Hash PII before inscription — SHA-256 one-way function — no PII on chain
- Comparison table: Traditional Compliance vs. El Jeffe (from B-053 work order)
- Key line: whichever version Syd approves (Option A or Option B from B-053)
- Design: use the same card/grid layout as existing sections. Signal Yellow for El Jeffe column.

**Section 3.5 (after Economy, before Market):**
### 03b — The Investment Thesis
*Source: PhD briefs — curated and condensed*

Sub-sections (each as a card or expandable block):

1. **Block Space as Write Access** — From `PhD_Layer5_BlockSpaceMoat_Thesis.md`
   - Key insight: "Mining does not produce coins. Mining produces write access to the most permanent ledger ever created."
   - Fee window argument: current inscription costs ~200 sats, window closing post-halving
   - Why the position is unreplicable

2. **The Genesis Pool** — From `PhD_Layer5_GenesisPool_CapitalThesis.md`
   - Founder commitment: 10M satoshis from personal F2Pool mining reward (0.1 BTC)
   - Option A/B/C comparison: sell, hold, or inscribe (inscribe wins)
   - "Every inscription generates validation revenue indefinitely"

3. **The VeriSign Parallel** — From `PhD_VeriSign_Analogy_InvestorBrief.md`
   - Structural comparison: VeriSign claimed trust root of the internet in 1995, GrowDirect claims trust root of commercial truth in 2026
   - The table: VeriSign dimensions vs. El Jeffe dimensions
   - "Whoever establishes the canonical trust layer for a new category of commerce — before the market understands the category — owns the tollbooth permanently."

4. **Vertical Integration** — From `PhD_Layer5_VerticalIntegration_Thesis.md`
   - Mine → Mint → License → Validate → Reinvest cycle

**Section 6.5 (end, before closing):**
### 07 — Protection
*Source: Syd IP Strategy + patent filing*

- Patent Pending: Provisional 63/991,596, filed Feb 26, 2026
- 9 claims, 6 embodiments
- Trade secret + copyright + trademark protection layers (high-level, no specifics)
- "The IP is the combination" — brief version of Syd's framing
- NOTE: Syd must review every word of this section. Nothing about protection layers goes live without legal sign-off.

---

## Design Specifications

### Preserve from Template
- Dark theme (#080808 base)
- Bitcoin orange (#F7931A) + gold (#FBBF24) accent palette
- Fonts: Bebas Neue (headers), DM Sans (body), DM Serif Display (quotes), Space Mono (mono/labels)
- Animated SVG closed-loop economy diagram
- Film grain texture overlay
- Fade-in scroll animations
- Responsive mobile layout
- Password gate (client-side JS)
- Single self-contained HTML file — all CSS/JS/SVG inline

### New Design Elements
- Compliance comparison table: use same card styling, Signal Yellow (#FBBF24) for El Jeffe column, institutional gray (#5a5a5a) for traditional column
- Investment thesis cards: same card grid as existing sections, with expandable/collapsible content for longer PhD content
- VeriSign comparison table: same table styling as the competitive comparison in Market section
- Protection section: understated, monospace, "Patent Pending" in gold, rest in muted tones — confidence, not salesmanship
- Navigation: update sticky nav to include new sections

---

## Content Sources — Full File Paths

### PhD Briefs (condensed into investor-facing copy by PhD)
| Source | Output File | Section |
|---|---|---|
| Block Space Moat | `_ALX/WorkOrders/output/PhD/PhD_Layer5_BlockSpaceMoat_Thesis.md` | 03b — Investment Thesis |
| Genesis Pool | `_ALX/WorkOrders/output/PhD/PhD_Layer5_GenesisPool_CapitalThesis.md` | 03b — Investment Thesis |
| VeriSign Analogy | `_ALX/WorkOrders/output/PhD/PhD_VeriSign_Analogy_InvestorBrief.md` | 03b — Investment Thesis |
| Vertical Integration | `_ALX/WorkOrders/output/PhD/PhD_Layer5_VerticalIntegration_Thesis.md` | 03b — Investment Thesis |
| Trust Collapse | `_ALX/WorkOrders/output/PhD/PhD_Layer5_TrustCollapsisThesis.md` | 03b — Investment Thesis (optional — include if space allows) |
| Patent Schematic | `_ALX/WorkOrders/output/PhD/PhD_StagedImmutability_PatentSchematic_v1.0.md` | 02 — Solution (reference for pipeline visual accuracy) |
| Volume Analysis | `_ALX/WorkOrders/output/PhD/PhD_StagedImmutability_VolumeAnalysis_v1.0.md` | 04 — Market (reference for scale numbers) |

### B-053 Content (feeds Section 02b)
| Source | Output File | Section |
|---|---|---|
| Compliance argument | `_ALX/WorkOrders/WORKORDER_B053_ComplianceSlide.md` | 02b — Compliance by Construction |
| PhD theoretical brief | TBD — PhD delivers `PhD_B053_ComplianceByConstruction_Brief.md` | 02b — Compliance by Construction |
| Syd legal memo | TBD — Syd delivers approved language | 02b — Compliance by Construction |

### Syd Content (feeds Section 07)
| Source | Output File | Section |
|---|---|---|
| IP Protection Strategy | `_ALX/WorkOrders/output/Syd/Syd_IP_Protection_Strategy_v1.0.md` | 07 — Protection (high-level only) |
| Patent Assessment | `_ALX/WorkOrders/output/Syd/Syd_PatentAssessment_StagedImmutability_v1.0.md` | 07 — Protection |

---

## Agent Routing

### Jess — Primary Builder (HTML)
**Deliverable:** `growdirect_investor_v2.0.html` — single self-contained file

1. Start from `growdirect_investor_1.html` template
2. Preserve ALL existing design: colors, fonts, animations, SVG, grain texture, password gate
3. Add new sections in order specified above (02b, 03b, 07)
4. Condense PhD content into investor-facing copy (PhD provides raw, Jess edits for voice)
5. Update navigation to include all sections
6. Test password gate still works
7. Ensure mobile responsive
8. Output to: `_ALX/WorkOrders/output/Jess/growdirect_investor_v2.0.html`

**Voice guidance:** Match the existing site's tone. Confident. Sparse. Let the architecture speak. No hype words — the mechanism IS the pitch. Bebas Neue for section titles. DM Sans for body. Space Mono for technical callouts.

### PhD — Section Copy
**Deliverable:** Investor-facing condensed versions of 4 briefs + B-053 compliance brief

1. Deliver B-053 compliance brief first (feeds Syd review and Jess Section 02b)
2. Condense each of the 4 investment thesis briefs into ~150-200 word investor-facing summaries
3. Preserve the key lines / pull quotes that anchor each argument
4. Remove all internal references, agent names, file paths, classification markings
5. Output: `PhD_B054_InvestorSiteCopy_v1.0.md` with clearly labeled sections

### Syd — Legal Review (TWO deliverables)
**Deliverable 1: B-053 legal memo** (already in B-053 work order — sequential gate still applies)
- Review compliance language, approve Option A or B, deliver memo

**Deliverable 2: B-054 full site legal review**
- Review ALL text on the expanded investor site before it goes live
- Flag any claim that creates legal exposure
- Confirm patent pending language is accurate
- Confirm no trade secrets are exposed
- Confirm protection section does not overpromise
- **Password gate review:** Is client-side JS sufficient, or do we need server-side auth?
- Special attention: PhD briefs contain MAXIMUM CONFIDENTIAL content — what can go behind a password gate vs. what should never leave the building?
- Output: `Syd_B054_InvestorSite_LegalReview.md`

### Art — Landing Page Link
**Deliverable:** Updated `growdirect-site/index.html` with "Learn More" button pointing to investor briefing

1. The current landing page has a "Learn More" CTA (`.btn-secondary`)
2. Update href to point to the password-protected investor briefing URL
3. This is a 1-line change — Art confirms the link destination with Jeffe
4. Do NOT change any other content on the landing page

---

## Dependencies

```
B-053 PhD brief      ──→  B-054 Section 02b content
B-053 Syd legal memo ──→  B-054 Section 02b approved language
PhD condensed briefs ──→  Jess builds Section 03b
Syd full site review ──→  Site goes to ANY investor (absolute gate)
B-032 (Square accts)  ──  No dependency (investor site is independent of dev track)
```

---

## Timeline

| Step | Agent | Dependency | Target |
|---|---|---|---|
| 1. PhD B-053 compliance brief | PhD | None | ASAP |
| 2. PhD condensed investor copy (4 briefs) | PhD | None (parallel with step 1) | ASAP |
| 3. Syd B-053 legal memo | Syd | Step 1 | After PhD brief |
| 4. Jess builds expanded site v2.0 | Jess | Steps 1, 2, 3 | After Syd memo |
| 5. Syd full site legal review | Syd | Step 4 | Before ANY external use |
| 6. Art updates landing page link | Art | Step 5 (URL confirmed) | After site approved |

**Hard gate: Nothing goes to an investor before Syd signs off on the complete site.**

---

## IP Exposure Concern (SAME-DAY ACTION)

Jeffe is concerned about IP exposed on the public GrowDirect web. Separate from this work order, Syd is dispatched for a same-day IP exposure audit:

**See:** `_ALX/WorkOrders/DISPATCH_Syd_IPExposureAudit.md`

This audit determines what comes down, what stays, and what Jeffe tells the attorney.

---

*ALX | Chief of Staff | February 27, 2026*
*This deliverable is gated: PhD delivers copy → Syd reviews → Jess builds → Syd signs off → Art links*
