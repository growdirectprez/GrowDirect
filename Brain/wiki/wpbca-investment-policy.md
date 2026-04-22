---
type: wiki
tags: [wpbca, cove, governance, treasury, investment, davis-stirling, bitcoin, advisory-synthesis]
created: 2026-04-19
sources: [Brain/raw/processed/advisor-memos/2026-04-19-comprehensive-review.md]
status: draft
last-compiled: 2026-04-19
needs-review: 2026-05-03
---

# Community of Abalone Cove (formerly WPBCA) — Investment Policy Statement

Community of Abalone Cove (formerly WPBCA) operating and reserve funds must be held in stable, liquid, insured instruments — not Bitcoin, not Lightning sats, not community tokens, not any volatile asset. This card captures the working position on treasury composition. Adoption requires a functional three-director board; see [[wpbca-third-director-recruitment]].

Distilled working position from a 2026-04-19 advisor memo. HOA counsel review required before adoption.

## The Short Answer

Do not hold Bitcoin (or any volatile crypto asset) in the WPBCA treasury.

Even though Bitcoin is maturing and GAAP is moving toward mark-to-market accounting, HOAs are held to a different standard than for-profit corporations. Corp. Code § 7231 and Civ. Code § 5800 apply a prudent-person / trust-like standard. Accounting changes do not override fiduciary duty.

## Why the Corporate-Treasury Analogy Does Not Apply

Some public companies, Lightning wallet developers, and newer Bitcoin treasury companies are moving material portions of corporate treasury into BTC. Valid for them. Not valid for WPBCA:

| For-Profit Corporation | California HOA |
|-----------------------|----------------|
| Directors owe duties to shareholders who knowingly accept volatility | Directors owe duties to members who expect stability for essential maintenance, insurance, reserves |
| Business judgment rule provides broad protection | Prudent-person standard is closer to a trust or conservatorship standard |
| Purpose is to innovate / grow / take calculated risk | Purpose is to maintain roads, roofs, drainage, insurance, and enforce CC&Rs |
| Shareholders can exit by selling | Members are bound by deed restrictions; cannot exit without selling the property |
| Accounting rule changes are a meaningful signal | Accounting rule changes are just accounting — fiduciary standard is a separate body of law |

A 50% BTC drawdown at a public company is a bad quarter. A 50% BTC drawdown at WPBCA — already operating with 2 of 5 director seats filled and underfunded at <$20/month dues — is potentially an existential event for the association.

## What the Treasury Should Hold

- Money market funds (insured, liquid)
- Short-term U.S. Treasuries (low risk, liquid)
- Insured certificates of deposit (CDs) within FDIC limits
- Checking accounts at reputable banks, tied to WPBCA's EIN
- Nothing that requires private-key management, custody providers, or specialized custodians

## What the Treasury Must Not Hold

- Bitcoin or any cryptocurrency (spot holdings)
- Lightning Network sats (even temporary settlement balances from supplemental Strike ACH — see [[wpbca-payments-platform]])
- Community tokens or any tokenized governance instrument
- Volatile equity positions
- Uninsured or illiquid assets
- Any asset that D&O / fidelity insurance carriers exclude from coverage

## Governing Law

**California Corporations Code § 7231** — Duty of Care:

> "A director shall perform the duties of a director... in good faith, in a manner such director believes to be in the best interests of the corporation and with such care, including reasonable inquiry, as an ordinarily prudent person in a like position would use under similar circumstances."

**California Civil Code § 5800** — Davis-Stirling liability limitation for volunteer directors:

Protection applies only if the director acts in good faith, within authority, and not intentionally or with gross negligence. A BTC-laden treasury that crashes has a hard time surviving the "ordinarily prudent person" inquiry.

**Civil Code §§ 5510 et seq.** — Reserve funding and investment. Boards must maintain adequate reserves for major repairs/replacements and invest those funds prudently.

## Why Lightning Is Not a Bank Account

Even with the temptation to use a Lightning wallet as the EIN-tied business banking account — low fees, fast settlement, 24/7 — it does not satisfy the legal requirements:

- Not a regulated depository; no FDIC insurance
- Not equivalent to a BofA or Chase business checking account despite offering payment functionality
- Channel liquidity management, settlement complexity, and custody of private keys all add operational burden for a volunteer board
- D&O and fidelity insurance carriers often exclude crypto-related losses
- Davis-Stirling expects uniform, transparent, auditable collection practice — Lightning payments are pseudonymous by default

See [[wpbca-payments-platform]] for the compliant way to reduce collection friction (HOA-specific platforms + optional Strike ACH as a supplemental rail into a traditional EIN-tied bank account).

## Where Crypto Exposure Does Belong

- **Personal holdings** — individual members can hold BTC personally. Many do.
- **Abalone Cove Foundation** — can accept crypto donations with mandatory USD conversion per [[foundation-crypto-donations]]
- **LLC** — commercial software work including any Bitcoin-related treasury strategy or Lightning-related licensing (the founder's existing CA LLC, see [[foundation-llc-rescue-status]])

The structure is designed so that crypto has a place in the founder's life without being in the HOA treasury.

## Operational Policy (For Board Adoption)

The WPBCA board adopts (in a formal Investment Policy Statement) rules like:

- All HOA funds held in insured, liquid, stable USD instruments
- Any deviation requires written board resolution, professional fiduciary advice (not crypto-promoter advice), and full member transparency
- Annual review of the IPS by the full board
- Treasurer reports treasury composition at each regular board meeting
- Any material deviation from this policy triggers mandatory member notice

## Blockers

Adoption requires a quorum-capable board. Currently impossible with only 2 of 5 director seats filled. See [[wpbca-third-director-recruitment]]. Until then, this card is a draft working position — the current two directors can informally agree to follow it as a posture but cannot formally adopt.

## Open Decisions

- Specific IPS language (draft pending HOA counsel)
- Bank selection for the EIN-tied operating account (BofA, Chase, a CA-focused credit union, or a bank experienced with HOAs)
- Reserve fund split (how much at the bank vs. in Treasuries vs. money market funds)
- Treasurer / board point-of-contact for treasury decisions
- Whether to coordinate with other peninsula HOAs on shared banking or brokerage relationships (inter-HOA efficiency play, not governance delegation)

## Related

- [[wpbca-compliance-framework]] — MOC
- [[wpbca-payments-platform]] — Compliant collection system (payment friction ≠ treasury composition)
- [[wpbca-third-director-recruitment]] — Blocker on adopting any binding policy
- [[foundation-crypto-donations]] — Where crypto donations can legitimately be received (Foundation, not HOA)
- [[foundation-llc-rescue-status]] — Where crypto-related commercial work belongs
