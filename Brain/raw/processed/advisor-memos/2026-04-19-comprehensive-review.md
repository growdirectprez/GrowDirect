---
type: advisor-memo
date: 2026-04-19
advisor: external (not WPBCA counsel, not Foundation counsel)
subject: Comprehensive review — compensation wiki, system-generated logs, Q1 founding weeks, founder narrative, BTC treasury, HOA payment platforms
scope: Foundation (501c3) + WPBCA (mutual-benefit) + personal founder context
status: archived, distilled into Brain/wiki/foundation-* and wpbca-* cards
supersedes: [2026-04-19-hoa-payments.md — that memo is a subset of this broader exchange]
---

# Advisor Memo — Comprehensive Review (2026-04-19)

**Not legal advice.** External advisor synthesis preserved verbatim for the record. Final positions require separate 501(c)(3) counsel (Foundation) and/or HOA counsel (WPBCA) review before adoption.

The working positions distilled from this memo are in the Foundation legal framework and WPBCA compliance framework cards. This file is archived for traceability.

## Exchanges Covered

1. **Review of `foundation-three-hat-compensation.md`** — advisor's assessment of whether the wiki satisfies reporting
2. **System-generated CICD + email logs** — user correction that logs are not reconstructed, they are automated from pipeline; advisor response on what still needs to be added
3. **Q1 2026 founding weeks compensation** — advisor confirming pre-formation work can be ratified at first board meeting
4. **Founder narrative and personal context** — 3rd-generation Californian, moved back 2003, public schools, age 55, BTC mining in 2014 on Raspberry Pi, sliding house as largest asset, SS gap-filling, wife's boom-bust real estate income
5. **Ocean path easement sensitivity** — Tract 14649 lots with lot lines beyond mean high tide; Hollister Ranch / Bixby parallel; advisor guidance to treat as PRIVATE WPBCA governance matter, Foundation does neutral documentation only
6. **Bitcoin as HOA treasury** — advisor says no; fiduciary duty under Corp. Code § 7231 + Civ. Code § 5800; volatility + D&O insurance exclusions + Davis-Stirling collection rules
7. **GAAP mark-to-market rebuttal** — user pushed that public companies are exploring BTC treasuries; advisor distinguished: HOAs held to prudent-person / trust-like standard, accounting changes don't override fiduciary duty
8. **Community tokens + QR-code cards** — advisor says no for assessments; fiduciary, accessibility, insurance issues
9. **Lightning wallet as business banking account** — advisor says no; cannot replace EIN-tied insured depository account
10. **Strike ACH as supplemental rail** — acceptable if routed into EIN-tied business bank account; not primary treasury
11. **HOA-specific payment platforms** — advisor recommends AppFolio, CINC, Buildium, TenantCloud, HOA Express as primary system with optional Strike ACH rail

## Distilled Working Positions

### On the `foundation-three-hat-compensation` wiki

Advisor's assessment: "a strong starting framework, but does not yet fully satisfy reporting and compliance requirements on its own."

Strengths acknowledged:
- Three-entity separation + file-path allocation rules
- Legal doctrines correctly identified (private inurement, private benefit, Corp. Code § 5231/5233)
- Conservative Year 1 compensation targets ($25k–$60k, $50–$75/hr)
- Disinterested-director approval + board minutes required
- Double-billing and WPBCA work correctly flagged as non-payable

Gaps that must be addressed before any compensation begins:
- **Formal board adoption** — wiki is internal note; must be presented to disinterested directors, approved by resolution, recorded in minutes, incorporated into bylaws or standalone policy
- **Contemporaneous logging rules** — must be explicit about what contemporaneous means and the retention period (3–6 years IRS SOL + litigation hold)
- **Reasonable-compensation determination** — board must obtain and document comparable data (salary surveys for exec directors of similar-size CA historic-preservation 501(c)(3)s), document review in minutes, re-approve annually
- **Conflict-of-interest procedures** — written disclosure, recusal, annual signed conflict statements by all directors
- **Arm's-length licensing language** — if LLC ever licenses to Foundation or other HOAs
- **Form 990 + RRF-1 reporting readiness** — Part VII, Schedule J if >$100k, related-party transactions disclosure

### On system-generated CICD + email logs (user correction)

User's position: "we are not reconstructing them we are compiling them from logs that we systematic logs from our CICD pipeline everything including emails are tracked through logs does constituent reconstruction seems much more accurate than notes of any kind or any human in the loop at the time its all system generated"

Advisor's response: "It is a strong starting point and materially better than manual notes alone, but it does not yet fully satisfy compliance requirements on its own."

What automated logs do well:
- Objectivity and verifiability (git commit history, file paths, timestamps, email metadata)
- Granularity (file-path allocation rules)
- Contemporaneous nature (logs created at moment of action)
- Audit trail (exportable raw logs)

What's still needed:
- **Explicit allocation to exempt purpose** — file-path rules must be reviewed and approved by the board, not just applied silently
- **Disinterested director oversight** — logs must be summarized (not raw) for board review + approval
- **Reasonable compensation determination** — still requires comparable-data + rate review
- **Record retention** — 3–6 year IRS SOL + litigation hold
- **Short cover memo** — turns raw logs into defensible evidence by stating the allocation rules applied

### On Q1 2026 founding-weeks compensation

"Founding weeks are a legitimate period of work for a new 501(c)(3). Many small nonprofits compensate their founder/executive director for organizational setup (drafting governing documents, filing with the Secretary of State and IRS, building initial programs, recruiting the board, etc.). However, because this is the highest-risk period for private inurement and private benefit challenges, the process must be more formal, not less."

Standard sequence:
1. File Articles of Incorporation first (creates legal entity)
2. Obtain EIN + hold first organizational board meeting (adopt bylaws, elect officers, approve conflict-of-interest policy, adopt compensation policy, ratify pre-formation actions)
3. Approve compensation for founding-period work at that first meeting, based on logs and summary

Founding-period guidance:
- Conservative range: $50–$75/hr
- Keep Q1 total modest (e.g., $8k–$15k) unless comparable data supports higher
- Payment as one-time founding stipend or hourly, documented as compensation for services
- Protective bylaws language: "The Board may approve reasonable compensation for services performed by a director or officer during the pre-incorporation and organizational phase, provided that (i) a summary of tasks and supporting logs are presented, (ii) the compensation is reviewed and approved by disinterested directors, and (iii) the amount is determined to be reasonable based on the nature and scope of the work performed for the Corporation's exempt purposes."

### On the sensitive ocean path easement

User's framing: "we have the same situation sort of. some of the lots in tract 14649 have lot lines that are beyond the mean high tide line, they like it that way, it is exceedingly rare, in terms of assets valuable, it makes a k shaped economy right inside our own [HOA]"

Advisor's guidance: "Treat the easement as a private governance matter best handled through WPBCA board processes and inter-HOA coordination. The Foundation's role should be limited to neutral, factual research and documentation (e.g., publishing the 1949 Declaration of Easements and related chain-of-title history) without advocating for or against specific lot owners' positions. Keep any strategic discussion about the easement within WPBCA or closed inter-HOA channels. The Foundation's public output (cove.org) should remain educational and restrained."

Rationale:
- Public advocacy could invite external pressure (Coastal Commission staff, media, activist groups) — Hollister Ranch parallel
- Could create internal member conflict between lots with and without the easement
- Foundation's mission is documentation, not litigation-adjacent advocacy
- Individual lot-level issues (e.g., 0 Clipper grading risk to your walls) belong with individual owners or WPBCA, not the Foundation

### On Bitcoin as HOA treasury

Advisor: "Do not hold Bitcoin in the WPBCA treasury."

Reasons:
- Fiduciary duty violation risk (Corp. Code § 7231, Civ. Code § 5800 — prudent-person standard, not business-judgment rule)
- Davis-Stirling collection rules (Civ. Code §§ 5650–5740) require uniform, transparent, auditable practice
- Custody and security (private keys, multi-sig, cold storage) is catastrophic-loss territory for a volunteer board
- Accounting (basis tracking, FMV on receipt, disposition gains/losses, Form 1120-H or 990) adds administrative burden
- D&O insurance and fidelity bonds often exclude crypto-related losses — directors personally exposed
- Member equity — not every homeowner has crypto knowledge or wallets
- External pressure — crypto-holding HOA becomes a visible target

On the GAAP mark-to-market rebuttal: "Accounting Treatment Does Not Override Fiduciary Duty. Even if GAAP eventually moves to full mark-to-market for Bitcoin (reducing impairment-only accounting), that is an accounting rule, not a safe harbor for fiduciary duty."

Where crypto exposure CAN live:
- Personal holdings (user's own accounts)
- Foundation 501(c)(3) — can accept crypto donations via gift-acceptance policy with mandatory prompt USD conversion
- LLC — commercial Bitcoin-related treasury strategy or Lightning work

### On Lightning wallet as primary HOA banking

Advisor: "A California HOA cannot realistically or compliantly use a Lightning wallet (or any crypto payment rail) as its primary business banking / assessment collection account in place of a traditional EIN-linked business bank account."

Reasons (beyond those above):
- Lightning wallet is not a bank account — no FDIC, no BSA/AML, no regulated depository status
- Not equivalent to Bank of America business account for legal purposes
- Channel management, liquidity, settlement complexity is ongoing administrative burden for volunteer board

### On Strike ACH as supplemental rail

Advisor: "Strike can be used as one payment rail for ACH collection, but it cannot replace the HOA's primary EIN-linked business bank account."

Acceptable because:
- ACH is fiat banking rail (Nacha rules, USD settlement in linked bank account)
- Common practice via banks, Stripe, PayPal, HOA-specific platforms
- Lower fees than wires or card processing

Required guardrails:
- HOA must designate a primary business checking account in the HOA's exact legal name and EIN
- Strike links to and pushes ACH into that account
- Board adopts a formal Payment Policy
- Record-keeping via Strike reports reconciled to bank account
- Confirm D&O/fidelity carrier does not exclude fintech processors

### On HOA-specific payment platforms (recommended)

Advisor: "Using a dedicated HOA-specific payment platform is the safest, most compliant, and most practical choice for WPBCA."

Platforms named: AppFolio, CINC Systems, Buildium (RealPage), TenantCloud, HOA Express / Spectrum.

Pricing for 81-lot: often $1–$3/unit/month or flat monthly fee.

Capabilities that matter:
- Built-in Davis-Stirling compliance (notices, lien tracking, inspection-ready records)
- Resident portal + QR codes / payment links for mailbox index-card drops
- ACH, credit/debit, e-check, sometimes Apple Pay/Google Pay
- Accounting integration + reconciliation
- Insurance/banking friendliness (familiar to D&O/fidelity carriers)
- Automation (late notices, delinquency tracking)

Recommended hybrid:
- Primary: HOA-specific platform (portal + automation)
- Optional rail: Strike or similar ACH processor routed into same HOA bank account
- Fallback: paper checks + in-person for members who prefer

## Proposed Next-Step Drafts (Advisor Offered)

- Compensation + Conflict-of-Interest Policy (formal, board-adoptable)
- Time Allocation and Compensation Approval Policy (incorporating CICD/email logging methodology)
- Board resolution language for first organizational meeting (including ratification of Q1 pre-formation work)
- Founding Period Time Summary template
- WPBCA Payment Policy (HOA-specific platform + Strike ACH)
- WPBCA Investment Policy Statement (limiting treasury to low-risk liquid insured assets)
- Foundation Gift Acceptance Policy (covering cryptocurrency with mandatory conversion)
- Meeting agenda template for first organizational board meeting

These drafts are pending: (a) confirmation of three initial Foundation directors, (b) separate 501(c)(3) counsel engagement for review before adoption.
