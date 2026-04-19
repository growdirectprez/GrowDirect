---
type: wiki
tags: [wpbca, cove, governance, compliance, payments, davis-stirling, advisory-synthesis]
created: 2026-04-19
sources: [Cove/docs/advisor-memos/2026-04-19-comprehensive-review.md]
status: draft
---

# Community of Abalone Cove (formerly WPBCA) — Payments Platform and Assessment Collection

Community of Abalone Cove (formerly West Portuguese Bend Community Association; "WPBCA" remains in historical references and legacy counsel communication) needs a modern, low-friction assessment collection system that satisfies Davis-Stirling requirements, protects the board from fiduciary exposure, and is accessible to all 81 lots regardless of tech sophistication. This card captures the working position on how to do that.

This is a distilled working position from a 2026-04-19 advisor memo (advisor transcripts preserved verbatim under `Cove/docs/advisor-memos/` and use the legacy WPBCA name). Adoption requires a functioning three-director Community of Abalone Cove board and is gated on the third-director recruitment — see the Blockers section.

## The Target Experience

The friction problem the board wants to solve: mailbox-dropped index cards with a QR code that a member scans to pay their assessment. One tap, done. No mailed check, no lost statements, no late-pay guilt spiral.

The constraint: this has to work without putting the HOA's treasury, insurance, or director liability at risk. The QR code must lead to a fiat payment page, not a crypto wallet, and funds must settle in the WPBCA's EIN-tied business bank account — not a Lightning wallet, not a Strike wallet, not a crypto custody service.

## The Compliant Architecture

Three layers:

**Layer 1 — Primary HOA-specific payment platform (required).**

Platforms purpose-built for California common-interest developments:

- AppFolio
- CINC Systems
- Buildium (RealPage)
- TenantCloud (smaller HOAs)
- HOA Express / Spectrum Association Management tools

For an 81-lot community, pricing is typically $1–$3 per unit per month or a flat monthly fee.

What these platforms provide:

- Built-in Davis-Stirling compliance: automatic proper-notice generation, lien tracking, payment histories that satisfy member inspection rights (Civ. Code § 5200), and clear audit trails
- Resident portal + shareable payment links + QR code generation
- Multiple rails: ACH (recurring or one-time), credit/debit cards, e-check, sometimes Apple Pay/Google Pay
- Accounting integration with direct reconciliation to the HOA bank account
- Insurance/banking familiarity — D&O and fidelity carriers recognize them
- Automation: late notices, delinquency tracking, reminders

**Layer 2 — Optional supplemental ACH rail (Strike or similar).**

Strike can be one of the ACH rails inside the HOA platform if fees are attractive. Funds still settle into the same EIN-tied business bank account. Strike is not the primary treasury; it is a processor.

What Strike cannot be:

- The primary business banking account (not a regulated depository; no FDIC; not equivalent to BofA or Chase business checking despite offering ACH)
- The destination for held funds (funds must flow through to the EIN-tied bank account)
- A Lightning / crypto payment rail for assessments (volatility, accessibility, insurance, custody problems — see [[wpbca-investment-policy]])

**Layer 3 — Traditional fallback (always available).**

Paper check and in-person payment must remain available. Davis-Stirling requires uniform, accessible collection practice. A tech-forward system that disadvantages members without phones or internet would draw equity challenges.

## What This Does Not Change

The Community of Abalone Cove business bank account is the source of truth. It must be:

- In the HOA's exact current legal name: **Community of Abalone Cove** (previously titled under the legacy name "West Portuguese Bend Community Association"; confirm the bank's records reflect the renamed entity)
- Tied to the HOA's EIN
- At a reputable bank (BofA, Chase, or a credit union familiar with HOAs)
- FDIC-insured
- The destination for every payment rail

Separate Investment Policy Statement governs what the treasury holds — see [[wpbca-investment-policy]]. Short answer: stable, liquid, insured instruments only. Not Bitcoin. Not Lightning sats. Not community tokens.

## Why Not Lightning or Community Tokens for Assessments

The board may be tempted by the low-fee, fast-settlement appeal of Lightning or a community-token rail. This doesn't work for HOA assessments. The short version:

- **Fiduciary duty** (Corp. Code § 7231, Civ. Code § 5800) holds directors to a prudent-person / trust-like standard, not the business-judgment rule that protects for-profit directors. Even if GAAP moves to mark-to-market for Bitcoin, that is an accounting rule — it does not override fiduciary duty.
- **Davis-Stirling collection rules** (Civ. Code §§ 5650–5740) require uniform, transparent, auditable practice. Crypto rails are pseudonymous by default and require extra work to map to specific lots.
- **D&O insurance + fidelity bonds** frequently exclude crypto-related losses. Running assessments through crypto rails can void or reduce coverage.
- **Accessibility** — not every homeowner has crypto knowledge or wallets. The board cannot impose an unauthorized technology requirement.
- **Regulatory exposure** — material crypto volume could draw DFPI attention (money-transmission analysis).

Crypto has a legitimate place in the broader structure — just not here. Route it through personal holdings or the Abalone Cove Foundation gift-acceptance policy, not the HOA treasury. See [[foundation-crypto-donations]].

## Implementation Steps (When Board Is Functional)

1. **Confirm HOA business checking account status** — exact legal name, EIN, active, properly titled. If the account has lapsed or the titling is off, fix that first.
2. **Research and demo 2–3 platforms** — AppFolio, CINC, and Buildium are the main candidates. Ask each about:
   - QR code / shareable payment link generation
   - ACH recurring authorization
   - Integration with the current bank account
   - Reporting formats for board meetings and member inspections
   - Cost for an 81-unit HOA
   - Member onboarding experience (the part that determines whether the index-card QR drop actually works)
3. **Draft the WPBCA Payment Policy** — one-page board-adoptable document that:
   - Authorizes the chosen platform
   - Requires all funds to flow into the HOA's primary bank account
   - Discloses options to all members (ACH, card, e-check, paper check)
   - Specifies late-fee, returned-payment, and dispute handling
   - Confirms traditional payment methods remain available
4. **Confirm D&O and fidelity coverage** — disclose the platform choice to the carrier; confirm no new exclusions
5. **Pilot with 3–5 volunteer households** — test the QR card → payment → reconciliation flow end-to-end
6. **Board resolution** — disinterested, functional three-director board adopts the policy. Record in minutes.
7. **Full rollout** — mailbox index-card drop with the QR code, portal URL, and fallback instructions for paper payment

## Blockers

**Third-director recruitment is a hard prerequisite.** A two-director board cannot adopt a binding payment policy under the WPBCA 2012 Bylaws (quorum and voting requirements). Every step in the implementation list above assumes a functional board. See [[wpbca-third-director-recruitment]] for the parallel track.

**Bank account status verification.** Before any platform evaluation, confirm the current WPBCA business checking account is properly titled, active, and tied to the HOA's EIN. An orphaned or mis-titled account blocks platform integration.

## Open Decisions

These need to be answered before the Payment Policy can be finalized:

- Which HOA-specific platform (after demos)? AppFolio vs. CINC vs. Buildium vs. other.
- Strike ACH as a supplemental rail, or stick with the platform's native ACH only?
- QR-code-on-index-card distribution: monthly, quarterly, or annually with stickers for updates?
- Fallback paper-check handling: addressed to WPBCA at what mailing address?
- Late-fee structure inside the platform (must match what the 2009 Declaration / 2012 Bylaws authorize).
- Who is the primary board point-of-contact with the platform vendor? (Treasurer, typically.)

## Related

- [[wpbca-compliance-framework]] — MOC for WPBCA mutual-benefit operational governance
- [[wpbca-investment-policy]] — Treasury composition rules (why not Bitcoin, why insured low-risk assets)
- [[wpbca-third-director-recruitment]] — The blocker that gates every board action
- [[wpbca-ocean-path-easement]] — Sensitive private governance matter (separate track)
- [[foundation-crypto-donations]] — Where crypto exposure does belong (at the Foundation, not the HOA)
- [[foundation-legal-framework]] — MOC for the Foundation 501(c)(3) side of the structure
