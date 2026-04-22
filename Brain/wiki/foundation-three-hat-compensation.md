---
type: wiki
tags: [foundation, cove, governance, compensation, three-hat, advisory-synthesis]
created: 2026-04-19
sources: [Brain/raw/processed/advisor-memos/2026-04-19-comprehensive-review.md]
status: draft
last-compiled: 2026-04-19
needs-review: 2026-05-03
---

# Foundation Three-Hat Compensation Model

The Abalone Cove Foundation (California 501(c)(3), forming) will operate inside a three-entity structure. One human wearing three hats creates compensation risk if the hats blur. This card defines the boundaries, the allocation rules, and what can legally flow from which entity.

This is a distilled working position from a 2026-04-19 advisor memo. Final terms require review by separate 501(c)(3) counsel before any compensation begins.

## The Three Hats

| Hat | Entity | Work | Pay? |
|-----|--------|------|------|
| **Community of Abalone Cove** (formerly WPBCA) | California Nonprofit Mutual Benefit Corporation (HOA) | Board service, member outreach, third-director recruitment, enforcing existing CC&Rs | Volunteer. Reimbursed expenses only unless the Board formally adopts director fees per the 2012 Bylaws (drafted under the legacy WPBCA name). |
| **Foundation** | Abalone Cove Foundation (California 501(c)(3), forming) | Research, Library of Evidence, editorial sites (cove.org, abalonecove.org), inter-HOA research/convening partnership (may route through CHOA), grant writing, 501(c)(3) compliance, procedural support for §V §5 processes | Paid as officer/director, subject to disinterested-director approval and contemporaneous time logs. |
| **LLC (existing CA LLC, needs rescuing)** | The founder's existing California LLC | Commercial software R&D: Canary, governance-engine product, platform infra, Angel, ownpv, ARC/Seacove. Anything that could be sold, licensed, or commercialized. | Paid through the LLC on whatever basis the LLC uses (distributions, salary, draws). Keep entirely separate from Foundation books. |

See [[foundation-llc-rescue-status]] for the current state of the LLC and the actions needed to bring it back into good standing — compensation from that entity presumes it is in good standing.

## Why The Boundaries Matter

Three doctrines govern the separation:

**Private inurement (IRC § 501(c)(3)).** A 501(c)(3) cannot have its net earnings inure to the benefit of a private individual. Paying the founder anything beyond reasonable compensation for actual services performed for the Foundation's exempt purpose risks loss of exempt status.

**Private benefit (Reg. § 1.501(c)(3)-1(d)(1)(ii)).** Even reasonable compensation can be problematic if the Foundation's activities disproportionately benefit the founder or the founder's for-profit LLC. The Foundation must exist to serve the public charitable purpose, not to subsidize the LLC's product development.

**Duty of care + conflict rules (Corp. Code § 5231, § 5233).** Director compensation and self-dealing transactions are reviewed by disinterested directors. The founder cannot vote on their own compensation or on contracts between the Foundation and their LLC.

Breach of any of these can trigger: IRS audit, loss of 501(c)(3) status, intermediate sanctions (excise tax on excess benefit transactions), or AG enforcement action in California. Member lawsuits are possible under Davis-Stirling if Community of Abalone Cove funds or governance interests get entangled.

## File-Path Allocation Rules

Time is logged per session. When a session touches files belonging to different hats, allocation is by file path, split proportionally by lines-changed across touched files. See [[foundation-time-logging-policy]] for the mechanics; this card defines the rules.

**LLC (commercial R&D) — paid through the LLC, not the Foundation:**

- `Canary/**` — loss prevention SaaS (commercial product)
- `Cove/cove/**` — the governance-engine application code (commercial product to sell/license to HOAs)
- `Cove/cove/angel/**`, `Angel/**` — real-estate intelligence platform
- `services/**`, `devops/**`, `content-engine/**`, `.claude/skills/**` (shared platform) — platform infrastructure serving commercial apps
- `Seacove/**` — SketchUp pipeline (product exploration)
- `~/ownpalosverdes/**` — marketing site for the real-estate business
- `docs/sdds/**`, `docs/superpowers/specs/**` (when the spec is for a commercial product) — R&D documentation

**Foundation (501(c)(3)) — reasonable compensation for actual services:**

- `Brain/wiki/cove-*.md` research articles (Declaration 100, PVPLC partnership, CSUDH field guide, LRPMP, Zone 2 geotech, Coastal Specific Plan, Colyear, etc.) — Library of Evidence
- `Brain/wiki/foundation-*.md` — Foundation legal framework and governance knowledge
- `Brain/projects/Cove.md` when editing the Foundation / Community of Abalone Cove revival threads (not the commercial-app threads)
- `Cove/docs/2026-04-18-abalone-cove-foundation-design.md` and related Foundation design specs
- `abalonecove.org` and `cove.org` editorial site content (not the governance-engine app)
- Grant writing, position letters, 1023-EZ narrative, bylaws drafting — anywhere these live

**Community of Abalone Cove (volunteer, unpaid) — logged, not paid:**

- Member outreach, director recruitment, board meeting prep
- Any communication with current Community of Abalone Cove directors, members, or the third-director search
- CC&R enforcement activities (not research — *enforcement*)

When the path isn't clear, err toward the non-Foundation hat. An hour wrongly charged to the LLC or logged as volunteer is recoverable. An hour wrongly charged to the Foundation can compound into a private-benefit finding.

## Reasonable Compensation

Year 1 target (from the advisor memo, pending counsel validation):

- Hourly rate: $50–$75/hr for Foundation-specific work
- Annual cap: $25k–$60k total from the Foundation
- Starting posture: part-time (10–20 hours/week) until Foundation has stable funding and comparable-compensation data

Comparables come from similar-size California historic-preservation or civic-education 501(c)(3)s. The disinterested directors must review comparable data before approving the rate, document the review in board minutes, and re-approve annually.

The LLC side has no Foundation-imposed cap — it is governed by whatever the LLC operating agreement and tax strategy dictate. Keep the books separate.

## What The Foundation Must Never Pay For

- Community of Abalone Cove governance work (board service, member outreach, director recruitment) — that is mutual-benefit volunteer labor, and any payment would commingle entities.
- Commercial software development — even when the deliverable looks useful to the Foundation (e.g., the deferred Governance Engine). If the code is also marketable, it is LLC R&D.
- Hours already billed to the LLC, or vice versa. Double-billing is the fastest way to lose exempt status.
- Anything without a contemporaneous time log or (for backfilled Feb–Apr hours) a reconstructed log clearly marked as such per [[foundation-time-logging-policy]].

## R&D Carve-Out: Why Canary Counts As LLC, Not Foundation

Canary and the platform tooling built through W08–W16 look, on the surface, like generic software work. They are. They are R&D for the commercial product line the LLC sells. The governance engine planned for deferred Epic 3 of the Foundation spec is a *product of the LLC*, which the Foundation may later license on arm's-length terms — it is not Foundation-built charitable infrastructure.

This matters because:

1. The Foundation cannot fund R&D for the LLC's commercial product. That is private benefit.
2. The LLC building a tool it later licenses to the Foundation (or to CHOA, or to other HOAs) is fine, as long as the license terms are arm's-length and approved by disinterested Foundation directors.
3. The approximately 1,200+ commits across Canary, Cove app code, Platform, ownpv, and ARC since Feb 2026 are LLC R&D hours. They should be logged to the LLC hat on reconstruction, not to the Foundation.

See [[foundation-ca-formation]] for why the LLC and the 501(c)(3) stay structurally separate, and [[foundation-bylaws]] for the conflict-of-interest language that governs any future LLC↔Foundation licensing.

## Arm's-Length Licensing (Deferred, LLC → Foundation / HOAs)

If and when the LLC licenses software to the Foundation or to other HOAs (CHOA members, Community of Abalone Cove, other peninsula HOAs):

- Disinterested Foundation directors approve the license terms
- Terms are documented in writing, compared against market rates
- Founder recuses from the Foundation-side vote
- License agreement is an exhibit to board minutes
- Annual review by the Foundation board

This is the path the advisor memo describes for CHOA adoption of the governance engine: the *product* comes from the LLC; the *Foundation* facilitates procedural/educational support for HOAs that use it. Two entities, two revenue streams, one set of clean books each.

## Gaps the Advisor Flagged (Must Be Closed)

A 2026-04-19 advisor review of this card concluded it is a strong starting framework but does not fully satisfy IRS Form 990, California AG Registry, or duty-of-care standards on its own. The following must happen before any Foundation compensation is paid:

- **Formal board adoption** — this wiki is an internal working note. It must be converted into a board-adopted "Compensation and Conflict-of-Interest Policy" (or attached to the bylaws), approved by disinterested directors (you recuse), and recorded in minutes.
- **Comparable-compensation data** — the board must obtain and document comparable-salary data (e.g., executive directors of similar-size California historic-preservation or civic 501(c)(3)s with budgets under $250k). The approval resolution must state the data relied upon and conclude the rate is reasonable.
- **Annual re-approval** — compensation gets reviewed and re-approved annually with updated comparables and updated logs.
- **Annual conflict-disclosure statements** — all directors sign annual conflict statements disclosing any LLC, Community of Abalone Cove, or other relevant roles.
- **Written disclosure of the founder's LLC + Community of Abalone Cove board roles** — included in the conflict policy and disclosed at the first board meeting.
- **Form 990 readiness** — compensation to officers/directors reported on Part VII; Schedule J if >$100k; related-party transactions disclosed.
- **Record retention** — Foundation logs + board minutes retained for at least the IRS statute of limitations (3–6 years) plus any litigation hold.

## What To Do Before Any Compensation Begins

1. Form the Foundation as a California Nonprofit Public Benefit Corporation — see [[foundation-ca-formation]]
2. Adopt standalone Foundation bylaws with a strong conflict-of-interest policy — see [[foundation-bylaws]]
3. Engage separate 501(c)(3) counsel (not Community of Abalone Cove counsel)
4. Confirm the LLC is in good standing — see [[foundation-llc-rescue-status]]
5. Stand up the time-logging system using system-generated CICD + email logs — see [[foundation-time-logging-policy]]
6. Disinterested directors adopt the Compensation and Conflict-of-Interest Policy with comparable data
7. Board resolution approving the rate, scope, and founding-period ratification, recorded in minutes
8. First paycheck only after steps 1–7 are complete

## Founding-Period Ratification (Q1 2026)

Work performed before the Foundation is legally formed is "pre-formation organizational work." It can be ratified at the first organizational board meeting if the standard sequence is followed: Articles filed → EIN issued → first board meeting → disinterested directors review logs + summary → adopt compensation policy → ratify pre-formation services.

Founding-period guidance (advisor, pending counsel validation):
- Range: $50–$75/hr
- Q1 total: conservative ($8k–$15k unless comparable data supports higher)
- Payment as one-time founding stipend OR hourly rate, documented as compensation for services rendered to the Foundation's exempt purposes

Protective bylaws language to include:

> "The Board may approve reasonable compensation for services performed by a director or officer during the pre-incorporation and organizational phase, provided that (i) a summary of tasks and supporting logs are presented, (ii) the compensation is reviewed and approved by disinterested directors, and (iii) the amount is determined to be reasonable based on the nature and scope of the work performed for the Corporation's exempt purposes."

## Related

- [[foundation-legal-framework]] — MOC for the Foundation legal structure
- [[foundation-ca-formation]] — Why California, not Wyoming; the formation process
- [[foundation-bylaws]] — What the bylaws must contain
- [[foundation-time-logging-policy]] — Contemporaneous + reconstructed logging rules
- [[foundation-llc-rescue-status]] — Status of the existing CA LLC
- [[foundation-blockchain-proof-layer]] — How the governance engine fits as a product, not a Foundation-built tool
- [[foundation-crypto-donations]] — Separate non-cash gift rules
