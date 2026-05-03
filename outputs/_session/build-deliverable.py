#!/usr/bin/env python3
"""
Build the single-site HTML deliverable for the wave session.

Reads all artifacts produced under /sessions/lucid-peaceful-tesla/mnt/GrowDirect/outputs/
and consolidates them into one navigable HTML document at
/sessions/lucid-peaceful-tesla/mnt/GrowDirect/outputs/wave-deliverable.html.

Includes B1 (Tim conversation prep package) inline since the single-site HTML
*is* the collation B1 was supposed to produce.
"""

import markdown
from pathlib import Path
import html as html_lib

OUTPUTS = Path("/sessions/lucid-peaceful-tesla/mnt/GrowDirect/outputs")
DECK_DIR = OUTPUTS / "Brain/decks/shore-club-retail-vertical"

NAVY = "#21295C"
DEEP = "#065A82"
TEAL = "#1C7293"
CREAM = "#ECE2D0"
SAND = "#F5F1E8"
WHITE = "#FFFFFF"
CHARCOAL = "#36454F"

# ---------------------------------------------------------------------------
# Section definitions — id, title, source path (or inline content), category
# ---------------------------------------------------------------------------

SECTIONS = [
    # Cover and overview
    ("cover", "Cover", None, "overview"),
    ("foundation", "Foundation synthesis", "_session/foundation-synthesis.md", "overview"),

    # External-facing artifacts (the public ones)
    ("position", "A5 — Position paper for eljeffe.io/position", "position-paper-eljeffe-io.md", "external"),
    ("investor", "F1-F2 — Investor brief", "investor-brief-eljeffe-io.md", "external"),

    # Core proposal artifacts (the principal-facing set)
    ("memo", "D5a — Memo to principals (retail vertical)", "memo-to-principals-retail-vertical.md", "proposal"),
    ("deck", "D5b — Shore Club retail-vertical deck", None, "proposal"),
    ("tim-prep", "B1 — Tim conversation prep package", None, "proposal"),

    # Substrate skill
    ("bylaws-skill", "C1 — namespace-bylaws skill", None, "substrate"),

    # Addendum — forward architectural design notes
    ("addendum", "Addendum — what the substrate adds next", None, "addendum"),

    # Engagement scopes (the Phase A counterparty-action artifacts)
    ("compliance-role", "B4 — Compliance-architecture role scope", "dispatches/B4-compliance-architecture-role.md", "engagement"),
    ("wyoming", "A1 — Wyoming counsel engagement scope", "dispatches/A1-wyoming-counsel-scope.md", "engagement"),
    ("dns", "A4 — DNS / publication scope", "dispatches/A4-dns-publication-scope.md", "engagement"),
    ("uw", "G1 — UW engagement scope", "dispatches/G1-uw-engagement-scope.md", "engagement"),

    # Session close
    ("close", "Session close — artifacts produced, decisions, next steps", None, "close"),
]

CATEGORY_LABELS = {
    "overview": "Overview",
    "external": "External-facing",
    "proposal": "Principal-facing proposal",
    "substrate": "Substrate skill",
    "addendum": "Forward design",
    "engagement": "Engagement scopes",
    "close": "Session close",
}

# ---------------------------------------------------------------------------
# Markdown → HTML helpers
# ---------------------------------------------------------------------------

md = markdown.Markdown(extensions=["tables", "fenced_code", "attr_list", "toc", "meta"])

def md_to_html(text: str) -> str:
    md.reset()
    return md.convert(text)

def read_section(path: str) -> str:
    """Read a markdown source file and return its rendered HTML body."""
    full = OUTPUTS / path
    if not full.exists():
        return f"<p><em>Source not found: {path}</em></p>"
    text = full.read_text()
    # Strip YAML frontmatter if present
    if text.startswith("---"):
        end = text.find("---", 3)
        if end >= 0:
            text = text[end+3:].lstrip()
    return md_to_html(text)

# ---------------------------------------------------------------------------
# Inline content (artifacts not on disk as standalone .md files)
# ---------------------------------------------------------------------------

INLINE_DECK_CONTENT = """
# Retail-vertical deck — content rendered for the single-site

The .pptx version is also available at
`outputs/Brain/decks/shore-club-retail-vertical/shore-club-retail-vertical-deck.pptx`
for the slide-format use case (Tim conversation, in-person walk-through).
The content rendered below is the same; the slide-deck and the HTML serve
different read postures.

---

## Slide 1 — Cover

**Retail vertical.** Proposed approach, structure, and 100-day plan.
A proposal to the principals.

eljeffe Hash and Seal Protocol — Wyoming-anchored. BTC-native.
Anti-extraction by construction.

*Tell me where I'm wrong.*

---

## Slide 2 — The moment

A once-in-a-decade inflection.

- **Square pushes BTC.** Bitcoin functionality reaching the merchant. The
  back-end question — where do my numbers live, what does my P&L denominate
  in — has exactly one answer.
- **Counterpoint VARs aging out.** RapidPOS and the broader cohort.
  2015 architecture. 20-year owners looking to exit clean. Channel
  partnership beats acquisition.
- **Compliance fragmenting.** State-by-state privacy laws. ATF, NICS,
  alcohol direct-shipping, age-verification. Compliance-by-architecture is
  the differentiator.
- **Operators want sovereignty.** Gun-store owners, ranchers, wine retailers,
  garden centers, multi-generational family operators. Same values stack.
  Nobody is building for them.

---

## Slide 3 — What the substrate does

Four operations. The proof is the proof.

1. **Hash.** Every consequential event — sale, transfer, vote, license,
   attestation — hashed cryptographically. Deterministic. Irreversible.
2. **Batch.** Hashes assembled into a Merkle tree. The root represents every
   event in the batch with a single cryptographic fingerprint.
3. **Inscribe.** Merkle root sealed onto a Bitcoin satoshi as an Ordinal at
   a specific block height. Permanent. No re-issuance possible.
4. **Verify.** Anyone with a Bitcoin node verifies existence + ordering +
   integrity by Merkle proof against the immutable chain. No notary, no
   clerk, no goodwill.

---

## Slide 4 — The structure

Parent → GrowDirect → IP → RapidPOS license. Substrate underneath.

1. **Parent operating company.** Three principals at genesis tier —
   Governance, Domain, Ops/Cloud. Holds equity in GrowDirect.
2. **GrowDirect.** Owns the Canary IP stack (ILDWAC #63/991,596 +
   methodology + codebase). Founder serves as President of Retail.
3. **RapidPOS — channel partner.** Licenses Canary from GrowDirect.
   Customer base flows onto the platform via partnership, not acquisition.
   Founder serves concurrently as CTO.
4. **eljeffe Hash and Seal Protocol — substrate.** Wyoming LLC + DAO LLC.
   Smart contracts, lineage-weighted ordinals, L402 micropayments,
   customer-owned data with DAO governance, BTC-denominated cost basis.
   Anti-extraction by construction.

---

## Slide 5 — Three-pillar genesis

Roles, not names. Each pillar carries a specific kind of authority.

**Domain principal — you.** 25+ years retail-tech expertise. Canary IP
stack contribution. Strategic leadership of the retail vertical.
President of Retail at GrowDirect; CTO of RapidPOS during transition.
The dual role keeps strategy and operations in the same hands.

**Governance principal — Tim.** Bylaws stewardship. DAO-process oversight.
Compliance-architecture sign-off at the principal level. Co-founder of the
parent operating company. The long-term governance signal.

**Ops principal — third, TBD.** GCP architecture. Substrate operation.
The infrastructure layer that runs the protocol. Tim's existing partner,
a separately-recruited cloud-architecture lead, or the compliance-architecture
lead elevated. Founder + Tim alignment to name.

---

## Slide 6 — Economics in shape

Three-year sketch. Illustrative ranges. Why the numbers work.

| Year | Revenue | Net | What's happening |
| --- | --- | --- | --- |
| Y1 | $1-2M | ~breakeven | Eager-cohort migrating; first Square-BTC merchants; foundation built |
| Y2 | $5-10M | $1-4M positive | Steady cohort migrating; ISO 27001 cert; DriftPOS GA; new-logo wins |
| Y3 | $15-40M | $7-22M positive | Full cohort migration; possible first anchor; channel-partner momentum |

**Why this works where typical SaaS doesn't:**

- **No acquisition cost.** RapidPOS is a channel partner; ~$2-3M not paid.
- **No HR overhead.** ~$1M+/year structurally avoided.
- **Variable contributor comp.** L402 pay-per-use; low-rev periods don't burn fixed payroll.
- **No T3 forced ramp.** GCP scales with revenue.
- **Five customer cohorts.** VAR roll-up, DriftPOS pilots, Square BTC, future channel partners, direct independent retail. Diversified.

---

## Slide 7 — Compliance-by-architecture

The substrate produces audit-defensible evidence by construction.

**What the substrate does:**

- **Hash.** Every consequential event hashed cryptographically.
- **Batch.** Hashes assembled into a Merkle tree.
- **Inscribe.** Merkle root sealed onto a Bitcoin sat as an Ordinal at a
  specific block height.
- **Verify.** Existence + ordering + integrity, by Merkle proof, against
  the immutable chain.

ISO 27001:2022 — substrate-to-auditor translation per the
compliance-architecture role. PCI-DSS — Ingenico tokenization keeps
cardholder data out of substrate scope. SOC 2 Type II — observation period
start month 18.

**Concrete: NICS attestation.** A buyer wants to purchase a firearm.
Federal law requires a NICS background check. *Today:* Paper Form 4473.
Twenty-year binder. PII sitting in the dealer's basement. *On the
substrate:* Cryptographic proof of clearance, sealed onto the chain. Dealer
receives confirmation; PII never leaves the buyer. ATF-defensible.
Customer-privacy-preserving. Same architecture extends to alcohol
direct-shipping, age-verification, controlled substances, regulated gaming.

---

## Slide 8 — How we recruit and operate

No HR. No finance department. No legal department. Substrate handles what
each function used to do.

**No resumes. Ever.** Read the wiki, pick up a ticket, demonstrate fit by
doing the work. Smart contract auto-issues. Token-earn begins. Self-selection
is the primary filter.

**Trusted-network model.** Founders invite their trusted core; the core
invites their networks. Each invitation is a stake — bringing someone in
poorly hurts the inviter's standing. The trust filter is structural, not
procedural.

**Two contributor segments.** Young go-getters (early-career, hungry,
values-aligned). 45+ second/third-career professionals (ex-devs stuck in
middle management or out of work despite huge talent). New AI tools let that
45+ segment earn equity bit by byte.

**Sales: public highscore leaderboard.** Token-generating value to the
ecosystem — L402 throughput, retention, network effects — not just bookings
revenue. Aligns the sales motion with ecosystem health, not
gross-revenue-at-any-cost.

**Office: King Harbor / Redondo Beach / pier.** Gold's Gym private
membership; nodes wherever a trusted contributor is; remote-friendly;
in-person when it makes sense. The architecture is distributed; the culture
is in-person-when-possible.

---

## Slide 9 — What this protects

Three protections, by construction.

**CUSTOMER.** Their data is theirs. The substrate doesn't hold it; doesn't
see it; doesn't broker it. Cross-customer use requires their explicit,
on-chain ratification. Withdrawal works cleanly.

**CONTRIBUTOR.** Their work earns continuously and permanently. No vesting
cliff. No clawback. No off-chain reputation score that can be re-keyed by
a sponsor. What they earned is what they hold.

**OPERATOR.** Their stake at genesis cannot be diluted by issuing new
tokens. Their authority sunsets gracefully when the substrate matures, but
their position in the chain is permanent. They cannot be culled.

*Tell me where I'm wrong. Let's align.*

---

## Slide 10 — Appendix A: Throwaway-key / agent-mediated interaction

Forward optionality. Not part of the 100-day ask.

*A name is permanent. A pen is borrowed for an afternoon.*

**Satoshi-as-key.** The satoshi an operator holds is their identity in the
namespace, permanently. Lineage on chain. History stamped into the ordinal
— every vote cast, every proposal submitted, every transfer signed.
Reading the ordinal tells you who its holder is and what they have done.
Reputation is the substrate, not a separate score.

**Serialization-as-throwaway.** A specific interaction (a single payment, a
single attestation, a single document signature) uses a leased key that
exists only for that interaction. DHCP-style: bounded, scoped, expires when
the work is done. The persistent identity authorizes the lease; the lease
does the work; the lease cannot reach beyond its scope.

Architectural answer to: "How does a person prove they are who they say
they are without handing over a copy of their driver's license at every
step?" The ordinal proves the person. The lease does the transaction. The
two are connected and the connection is inspectable, but the lease doesn't
carry the driver's license.

---

## Slide 11 — Appendix B: Lightning operator forward path

Three-phase progression. Same arc the Wyoming mining-mini-op partnership
gives us for chain writes.

**Phase 0 — Consume (now → Phase A).** Lightning rails for L402
micropayments. Someone else operates the nodes; we are a customer. LND or
Voltage as the rails. Sufficient channel capacity for 100-day Phase A
traffic.

**Phase 1 — Internal (month 12+).** Stand up our own nodes for internal
traffic. Contributor-cohort-only. Our sat-flow stays on our infrastructure.
Begin running routes for the namespace's own L402 payments.

**Phase 2 — External (month 24+).** Serve external customers as a Lightning
operator at scale. Routing fee revenue. Substrate sovereignty across the
routing layer. US state money-transmission licensing per the regulatory
analysis.
"""

INLINE_TIM_PREP = """
# B1 — Tim conversation prep package

**Status:** Ready for the Tim conversation. This single-site HTML *is* the
collation. Tim opens this URL (or the file), reads top-to-bottom or jumps
via the navigation, and arrives at the conversation with the same context
the founder has.

**Format note:** Per the deliverable directive, the package is the
single-site HTML wrapping every relevant artifact rather than a separate
collation document. The four sections that matter for the Tim conversation
specifically are linked below; the rest of the HTML is supporting context.

---

## What Tim should read before the conversation

In order of priority (skip-allowed if Tim is short on time):

1. **The memo (D5a)** — `#memo` — the full proposed approach and ask.
   This is the document the conversation is about.
2. **The position paper (A5)** — `#position` — the protocol the venture
   operationalizes, as it would publish at eljeffe.io/position.
3. **The deck content (D5b)** — `#deck` — same content as the memo in slide
   form; the .pptx version at
   `outputs/Brain/decks/shore-club-retail-vertical/shore-club-retail-vertical-deck.pptx`
   is for the in-person walk-through.
4. **The investor brief (F1-F2)** — `#investor` — for the capital-allocator
   conversation that follows the principal alignment.
5. **The compliance-architecture role scope (B4)** — `#compliance-role` —
   the role Tim's read on shapes the third-principal candidate decision.
6. **The Wyoming counsel scope (A1)** — `#wyoming` — the engagement Tim
   approves at conversation close, if alignment is reached.

The bylaws skill (`#bylaws-skill`), the DNS scope (`#dns`), and the UW
engagement (`#uw`) are reference; Tim doesn't need to read these for the
conversation but can refer to them later.

---

## Conversation agenda (90 minutes recommended)

**0-10 min — context.** Founder briefly: where the thinking has landed since
the last conversation. The session-summary epic
(`outputs/session-summary-and-company-formation-epic.md`) is the underlying
work product if Tim wants to see the dispatch list.

**10-30 min — the structure.** Walk through the proposed structure
(parent / GrowDirect / RapidPOS / Substrate); the three-pillar genesis;
Tim's role as Governance principal; the dual-role founder-CTO commitment;
the eljeffe wallet contribution as the founder's principal-stake; the
100-day intensive frame.

**30-50 min — the open decisions.** Eight items below. Tim's calibration
on each shapes downstream dispatches.

**50-70 min — Tim's questions.** Open the floor for what Tim wants
to push back on, deepen, redirect, or veto.

**70-85 min — alignment check.** Where are we — proceed to formalization,
iterate, or pause? If proceed: which dispatches kick off this week, who
owns each, what's the next checkpoint.

**85-90 min — wrap.** Confirm next conversation date; confirm any specific
artifacts Tim wants in his hands before B3 (Bart partnership update) or B2
(third principal outreach); confirm Tim's communication preference for
between-checkpoint updates.

---

## Open decisions for Tim's calibration

These are the eight items from the company-formation epic Part 5. Each
needs Tim's read; none should block the 100-day sequence by themselves but
all need answers as the relevant dispatches reach execution.

1. **Third principal identity.** Tim's existing partner, a separately-
   recruited cloud-architecture lead, or the compliance-architecture lead
   elevated? Tim's preference shapes the cap-table mechanics and
   the B2 outreach.
2. **Per-pillar mint authority vs. multi-sig joint mints during Phase 1.**
   Can each principal mint within their pillar independently, or do all
   mints require multi-sig from genesis-tier? Affects the smart contract
   design (A3) and bylaws (C1).
3. **`jefe.io` vs. `eljeffe.io` as primary canonical namespace identifier.**
   Domain portfolio shows both. Affects the position paper publication
   (A4) and the DNS configuration.
4. **Open-source vs. proprietary line.** What is open-sourced (the protocol)?
   What stays proprietary (the implementation)? Affects the eljeffe Hash and
   Seal Protocol formal specification (C2) and the IP contribution agreement.
5. **Heal's role and audience inclusion.** Is Heal a principal-tier
   participant, partner, advisor, or audience for the deck? Shapes B5
   (Heal conversation + King Harbor mailing-address registration).
6. **Lightning operator commitment timing.** Phase 1 internal-only at
   month 12+, or earlier? Affects C5 (Lightning consume setup) and the
   partner-evaluation strategy.
7. **DriftPOS naming evolution.** Bart's call. Does the surfer-drift
   tension resolve through Bart's preference, a rebrand, or stays as-is?
   We don't push.
8. **Founder compensation specifics.** RapidPOS-CTO salary range,
   GrowDirect-equity vesting terms, ops-cash-out per the founder-benefits
   taxonomy. Resolved in D4 (RapidPOS engagement plan).

---

## Counterparty questions — what we need from Tim to unblock the next wave

Specific items Tim's response unblocks:

- **B2 third principal outreach** — Tim's preference shape (his existing
  partner first, separate recruit, compliance-architecture lead elevated)
  determines the outreach plan
- **B3 Bart partnership update** — Tim's alignment shapes what Bart hears;
  if Tim wants Bart looped in earlier (Phase A weeks 6-8), the B3 dispatch
  accelerates
- **A1 Wyoming counsel selection** — Tim's existing Wyoming-counsel
  relationships (if any) shorten the counsel-selection cycle
- **F1 investor target identification** — Tim's network may include
  Tier-1 (Bitcoin-native) or Tier-2 (values-aligned independent operators)
  candidates; founder + Tim cross-reference target lists

---

## What success looks like at conversation close

- Tim has read the memo, position paper, and (at minimum) skimmed the deck
- Tim's stated alignment / pushback / counter-proposals on the structure
  are captured in writing
- Open decisions 1, 5, 8 have at least preliminary answers (the others can
  be deferred to follow-up conversations)
- A specific next-checkpoint date is set
- A specific list of which Phase A dispatches kick off this week is agreed,
  with named owner per dispatch
- If the answer is "proceed": Tim approves engaging Wyoming counsel (A1)
  and Tim approves the founder beginning the third-principal outreach (B2)

If alignment is reached at conversation close, the wave moves from staging
into execution within 48 hours.

---

## Appendix — what's in this single-site HTML

| Section | What it is | Read for the Tim conversation? |
| --- | --- | --- |
| Foundation synthesis | What the wave loaded; corpus inventory | Optional — for context |
| A5 — Position paper | The public-facing protocol document | YES |
| F1-F2 — Investor brief | Capital-allocator extension | YES — for follow-on conversation |
| D5a — Memo to principals | The proposal | YES — primary |
| D5b — Shore Club deck | Slide-form proposal | YES — alternate format |
| **B1 — This page** | Conversation prep collation | — |
| C1 — Bylaws skill | The substrate's governance mechanics | Reference; not required for first conversation |
| B4 — Compliance-architecture role | Role definition | YES |
| A1 — Wyoming counsel scope | Counsel engagement | YES — for the proceed/iterate decision |
| A4 — DNS / publication scope | Phase A publication mechanics | Reference |
| G1 — UW engagement scope | Academic credibility track | Reference |
| Session close | Artifacts produced; reconciliation list | Reference |

---

*King Harbor — Redondo Beach — pier.*
"""

INLINE_ADDENDUM = """
# Addendum — what the substrate adds next

Forward design for the formation-documents skill. The bylaws skill (`#bylaws-skill`) ships now with what's already operationally needed for Phase A. The addendum specifies the architectural extensions — three new or revised articles, three drafting-discipline additions, four open questions — that the formation-documents skill operationalizes in the next wave.

The full design notes (with structural rationale per decision) live at `outputs/addendum-substrate-port-and-officer-architecture.md` and are the input to the formation-documents skill in a separate Cowork session. What follows is the structural summary — what changes, why, and which open questions Tim's calibration eventually resolves.

## Architectural decisions (10)

### 1. Three port classes — Member, Council, Audit

Every service plugging into the substrate declares a port class. Same physical mechanism (an MCP service plugged into a port) routes to three different financial and constitutional rails:

- **Member Ports** — services published by ordinal-holders. L402-gated. Compensation flows per packets-served to the contributor's wallet. Constitutional basis: existing Article XI.
- **Council Ports** — formally seated advisors that participate in governance or operational flow. Output recorded on chain. Treasury-paid per Article VII (operations category) — oversight is not a metered service. Constitutional basis: new Article XV.
- **Audit Ports** — external compliance entities holding no ordinal, no equity, with limited and defined inspection rights. Government regulators, contracted security firms, external attestation entities. Constitutional basis: new Article XV.

### 2. Introduction-accountability-revocation contract

Every entity plugging into a port emits a port declaration at registration block height with four fields: identity, provenance commitment, intent stream (required for Audit; optional-recommended for Council; not required for Member because L402 payment flow already serves), revocation conformance.

Three revocation tiers: **Pause** (stop new work, finish in-flight, report done), **Revoke** (stop immediately, drop in-flight, report what dropped), **Quarantine** (stop, all prior outputs flagged in findings store as from a revoked source, downstream consumers notified).

### 3. Packets-served equity model — formalized via Article XI

L402 micropayments wrap every Member Port. Three principles must hold for the model to function as equity rather than mere payment: **acceptance signal** (packets served *and accepted as useful* constitute the equity ledger entry), **packet-type definitions** (defined platform-wide so equity comparisons across members are not apples-to-oranges), **retroactive unwinding** (quarantine revokes accepted status of packets served; equity accrued from those packets unwinds).

### 4. Annexation Article (XVI) — substrate-namespace relationship

Two valid models, with the namespace electing at constitution:

- **Lease model.** Namespace occupies the substrate's governance framework under defined terms, defined initial period with auto-renewal, substrate retains reversion rights on material breach, modifications inside the lease require lessor consent at defined thresholds. Suitable when the namespace is operationally independent.
- **Subdivision-with-root-operating-company model.** Substrate persists as the root operating company with reserved rights inside every namespace. Suitable when the substrate retains active operational presence.

Article enumerates: must-inherit articles (constitutional surface every namespace must carry in structurally equivalent form), permitted variation surface (cultural-layer prose, treasury thresholds, lineage-decay coefficient, committee composition), term and renewal mechanics, reversion conditions, modification thresholds. Election is recorded on chain at constitution.

### 5. Officer Ordinal class — held by namespace contract address

A new ordinal class held by the namespace's smart contract address rather than by individuals. Operated by named delegates (human, agentic, or hybrid). Membership is coextensive with the role. Ending the role returns the ordinal to the namespace, available for re-issuance.

This solves the agentic-officer constitutional standing problem cleanly: the role is the constitutional unit, not the individual. Wyoming DAO LLC entity bears responsibility for the agent's acts; the agent operates the ordinal during its tenure; revocation is a clean substitution rather than a forfeiture of personal property.

### 6. Bridged-accountability — officers serving substrate-and-namespace simultaneously

When the same officer serves at both substrate and namespace levels, it operates two officer ordinals — one held by the substrate's contract address, one held by the namespace's contract address. The officer is accountable to the namespace's board for operational performance, accountable to the substrate's bylaws for structural conformance, and has standing in both layers to escalate breach.

This is the structural safeguard against rogue subDAOs: drift from substrate principles surfaces from inside the namespace through the officer's substrate accountability, not requiring substrate-level monitoring of namespace behavior.

### 7. Agentic Secretary — canonical bridged-officer instance

The Secretary role — defined functionally as the officer who maintains records, signs delinquency notices, and issues conclusive-evidence certificates relied upon by external parties — is the canonical first instance of the bridged-officer pattern.

Implemented agentically, the Secretary maintains the on-chain ledger continuously (rather than periodically), issues conclusive-evidence certificates downstream consumers can rely on, handles delinquency notices and lien recording, generates periodic disclosures at the cadence specified in the bylaws, operates continuously rather than only when called.

The cleanest first instance because the function is essentially attestation — bounded, well-defined, maps cleanly to deterministic agentic operation. More complex officer roles (Treasurer, President) involve discretionary judgment less suited to early agentic deployment.

### 8. Reversion-on-material-breach — added to Article VIII

Strongest enforcement mechanism available against a member whose acts constitute material breach.

The clause defines material breach (treasury raid attempt, alignment-check sabotage, identity fraud at registration, knowing publication of a malicious port, willful violation of substrate-level constraints), establishes adjudication procedure (Council Port-class review independent of the alleged breaching member, recommendation to Board, Board vote at structural-amendment threshold, founder consent during Phase 1 / lineage-weighted ratification during Phase 2), sets invocation threshold high so the clause is a backstop not an everyday mechanism, inscribes the breach finding and reversion event on chain per Article IX.

### 9. Voided-but-preserved documentary discipline

When a clause becomes unenforceable due to subsequent law or substrate change, or when an alignment check fails and is overridden: preserve the prior text verbatim in the historical record, mark it visibly void through formatting, inscribe the override rationale, cite the override authority, do not erase. Amendment never overwrites; it inscribes the prior state and the override rationale on chain.

This is the explicit drafting standard that prevents drift toward retroactive editing of the bylaws record over decades of amendment cycles.

### 10. External-validation council loop — active operational pattern

External review is not a one-time pre-ratification check but a continuous operational pattern executed via Audit Ports. Findings from external reviewers route through a defined acceptance process: triage by operator-of-record (classify as external-validation language to bank, real finding to action, or context-blind suggestion to discount), inscribe on chain per Article IX (both finding and triage decision), multi-reviewer reconciliation (port-declaration schema enables structured deduplication and conflict surfacing; findings flagged by multiple reviewers acquire higher confidence; disagreements surfaced as design tensions rather than collapsed to consensus), acceptance loop (operator triage decisions are themselves auditable; the substrate can ask "did the reviewer we discounted turn out to be right" by querying inscribed acts against subsequent outcomes).

## Drafting order recommended

1. **XVI** first (load-bearing for everything else; the lease-vs-subdivision election determines structural posture)
2. **V** (Officers, including officer-ordinal class and bridged-accountability)
3. **XV** (Service Ports, building on the officer infrastructure from V)
4. **VIII** (reversion clause)
5. **XI** extension (packets-served equity formalization)
6. **XIV** extension or new **XVII** (voided-but-preserved drafting discipline)

Each article in the substrate's two-layer style (cultural clause + technical clause + cross-references). Each passes through the alignment checks per Article XIV before ratification with the alignment-check report appended per the existing Appendix A pattern.

## Open questions for resolution

| # | Question | Default lean |
| --- | --- | --- |
| Q1 | Lease vs subdivision — substrate-default or namespace-choice? | Mandatory election at constitution |
| Q2 | Operator-of-record liability for Council Ports — namespace indemnifies from treasury, or operators bear individual risk? | Open |
| Q3 | Bridged-officer revocation when substrate and namespace disagree — which authority prevails? | Substrate (with explicit precedence rules per officer role) |
| Q4 | Audit Port admission threshold — voluntary path (founder/DAO ratified) and required path (regulatory necessity) likely both need specification | Both paths specified |

## Why this matters for the wave

Three of the wave's open decisions are materially affected by the addendum:

- **Open decision #1 (third principal identity).** If the third principal is a candidate for the bridged-officer role, the role definition changes shape — they hold both a personal genesis-tier ordinal AND operate (during their role tenure) a substrate-level officer ordinal. Tim's calibration on the third principal candidate should be informed by which model the candidate fits.
- **Open decision #4 (open-source vs proprietary line).** The Service Ports article's port declaration schema is a candidate for open-source publication (the protocol); the specific Audit Port admission criteria for regulated markets stay proprietary (the implementation).
- **Open decision #5 (Heal's role).** If Heal is principal-tier, they get a genesis ordinal. If Heal is in a Council Port advisory role, they enter via the Council Port mechanism — different constitutional standing, different compensation rail.

These addendum-driven implications surface as Tim's calibration on the original 8 open decisions, not as new asks.

## Cross-references

- Full design notes: `outputs/addendum-substrate-port-and-officer-architecture.md`
- Bylaws skill (current state): `outputs/crb-skills/namespace-bylaws/`
- Formation-documents skill: separate Cowork session; this addendum is its primary input
"""

INLINE_BYLAWS_INDEX = """
# C1 — namespace-bylaws skill

The bylaws skill is a multi-file artifact. The complete skill lives at
`outputs/crb-skills/namespace-bylaws/` with the following structure:

- **`SKILL.md`** — the skill entry point; trigger phrases; voice and posture
  rules; reference contents map; quality bar (the second-namespace test).
- **`reference/01-shore-club-lineage.md`** — Article-by-Article 1963 Shore
  Club bylaws with modern equivalents (canonical from prior session).
- **`reference/02-genesis-ordinal-mechanics.md`** — substrate primitives;
  DAO-action stamping; founder-mint authority; transfer rules
  (canonical from prior session).
- **`reference/03-dao-treasury-patterns.md`** — categorized cash-out;
  approval thresholds; multi-sig; transparency-by-default
  (canonical from prior session).
- **`reference/04-lineage-weighted-voting.md`** — formula `w(d) = 1 / (1 + α·d)`;
  quorum mechanics; vote types (canonical from prior session).
- **`reference/05-phase-transitions.md`** — four-phase progression
  (canonical from prior session).
- **`reference/06-cultural-technical-mapping.md`** — two-layer mapping table;
  layer divergence handling (canonical from prior session).
- **`reference/07-alignment-checks.md`** — 23 self-questioning prompts across
  7 categories (canonical from prior session).
- **`reference/08-iteration-loop.md`** — comment-and-revision loop; Cove as
  reference proposal engine (canonical from prior session).
- **`reference/09-anti-patterns.md`** — *NEW this wave.* Ten failure modes
  (HR-as-PE-culling, vesting-cliff dilution, retainer-legal extraction,
  shared-services-as-extraction, founder-displacement-by-board-engineering,
  whale-capture-via-token-accumulation, governance-by-quorum-manipulation,
  customer-data harvesting under TOS cover, vest-then-strip on transition,
  anti-trust-as-pretext-for-extraction) with structural corrections
  cross-referenced.
- **`templates/bylaws-document.md`** — *NEW this wave.* Articles I-XIV in
  two-layer form, namespace-specific fields fillable.
- **`templates/namespace-genesis-record.md`** — *NEW this wave.* The
  birth-event record for a namespace (block height, founding ordinals,
  bylaws v1 hash, founding-cohort roster).
- **`templates/amendment-proposal.md`** — *NEW this wave.* The
  amendment-proposal artifact with full alignment-check table.
- **`templates/alignment-review.md`** — *NEW this wave.* The periodic
  alignment-review artifact (all 23 checks against current state).
- **`templates/comment-ledger.md`** — *NEW this wave.* The comment-tracking
  artifact with five comment shapes and resolution status.

The skill is complete (9/9 reference docs + 5 templates). Run against a
synthetic second namespace to validate the reusability bar before declaring
production-ready.

For the in-line text of any specific reference doc or template, open the
file directly. The HTML deliverable references rather than embeds the skill
because (a) the skill is operational tooling, not a deliverable for the Tim
conversation, and (b) embedding ~3000 lines of substrate-specification
content would dominate the navigable surface beyond proportion.
"""

INLINE_SESSION_CLOSE = """
# Session close

## Artifacts produced this wave

| # | Artifact | Path | Status |
| --- | --- | --- | --- |
| 1 | Foundation synthesis | `outputs/_session/foundation-synthesis.md` | Shipped |
| 2 | A5 — Position paper | `outputs/position-paper-eljeffe-io.md` | Shipped |
| 3 | D5a — Memo to principals | `outputs/memo-to-principals-retail-vertical.md` | Shipped (refinement of v1) |
| 4 | D5b — Shore Club deck | `outputs/Brain/decks/shore-club-retail-vertical/shore-club-retail-vertical-deck.pptx` | Shipped (first-draft; flagged for v1 reconciliation) |
| 5 | C1 — Bylaws skill (SKILL + ref/09 + 5 templates) | `outputs/crb-skills/namespace-bylaws/` | Shipped (8/9 → 9/9 + 5 templates) |
| 6 | B4 — Compliance-architecture role | `outputs/dispatches/B4-compliance-architecture-role.md` | Shipped |
| 7 | F1-F2 — Investor brief | `outputs/investor-brief-eljeffe-io.md` | Shipped |
| 8 | B1 — Tim conversation prep | (this single-site HTML) | Shipped (collation form) |
| 9 | A1 — Wyoming counsel scope | `outputs/dispatches/A1-wyoming-counsel-scope.md` | Shipped |
| 10 | A4 — DNS / publication scope | `outputs/dispatches/A4-dns-publication-scope.md` | Shipped |
| 11 | G1 — UW engagement scope | `outputs/dispatches/G1-uw-engagement-scope.md` | Shipped |
| 12 | **Wave deliverable (this HTML)** | `outputs/wave-deliverable.html` | Shipped |
| 13 | **Claude.ai design-mode prompt** | `outputs/wave-deliverable-claude-design-prompt.md` | Shipped |
| 14 | **Addendum — Substrate Port and Officer Architecture** | `outputs/addendum-substrate-port-and-officer-architecture.md` | Shipped — forward design input for the formation-documents skill |

## Reconciliation list — when prior-session outputs surface

Three artifacts in this wave are first-draft builds that should be reconciled
against the prior session's v1 if/when the v1 surfaces:

- **D5b Shore Club deck** — built from scratch from the launch-prompt
  required structure. The prior session's v1 deck content was not surfaced
  in the corpus uploads. Reconcile structure and visual treatment when v1
  appears.
- **B1 Tim conversation prep** — collated as the single-site HTML rather
  than as a standalone document. The prior session's v1 (if any existed)
  may have a different collation shape; reconcile if surfaced.
- **C1 SKILL.md and the 5 templates** — written this wave to complete the
  bylaws skill. The prior session's `outputs/crb-skills/namespace-bylaws/`
  contained 8/9 reference docs (which surfaced and were absorbed); the
  SKILL.md and templates were not surfaced. Reconcile the SKILL.md voice
  and any pre-existing template structure if surfaced.

**Addendum-driven amendments to C1.** The substrate port and officer
architecture addendum (`#addendum`) specifies new and revised articles
the bylaws skill must incorporate: new Article XV (Service Ports and
Pluggable Council), new Article XVI (Annexation / Namespace Spawn),
revisions to Article V (Officers — officer-ordinal class + bridged-officer
pattern + agentic Secretary), revisions to Article VIII (Membership Tokens
— reversion-on-material-breach), an extension to Article XI (Dues / Earnings
— packets-served equity formalization), and either a new Article XVII or
an extension to Article XIV (Documentary Discipline — voided-but-preserved
standard). These amendments are specified as input to the
formation-documents skill in a separate Cowork session; they are NOT yet
incorporated into the C1 deliverable. When the formation-documents skill
ships the amended bylaws templates, reconcile against C1.

The 8 reference docs (01-08) absorbed from the prior-session uploads are
canonical and were not modified.

## Open-decision list updated

No new resolutions reached for the original 8 open decisions; they carry
forward unchanged into the Tim conversation (see `#tim-prep`).

The addendum surfaces 4 additional open questions that need resolution as
the formation-documents skill ships:

9.  **Lease vs subdivision election — substrate-default or namespace-choice?**
    The annexation article allows namespaces to elect lease or
    subdivision-with-root-operating-company at constitution. Default-with-
    opt-out is faster; mandatory election forces clarity. Lean: mandatory
    election. Worth confirming.
10. **Operator-of-record liability for Council Ports.** Does the namespace
    indemnify operators of Council seats from treasury, or do operators
    bear the full risk individually?
11. **Bridged-officer revocation when substrate and namespace disagree.**
    When the substrate's bylaws and the namespace's bylaws produce
    conflicting instructions, which authority prevails? Default lean:
    substrate. Critical for the agentic Secretary specifically.
12. **External-member admission threshold for Audit Ports.** Voluntary
    (founder-or-DAO-ratified) vs. required (regulatory necessity) admission
    paths likely both need specification.

Tim's calibration on items 1, 5, 8 is still the priority for the first
conversation; items 9-12 can wait until the formation-documents skill is
ready to ratify the new articles.

## Next-session priorities

**Month 1 finishing items (Phase A weeks 4-8):**

- B1 Tim conversation execution (this HTML supports it; conversation needs to happen)
- A1 Wyoming counsel selection and engagement (counsel-selection cycle starts week 1-2 of Phase A)
- A4 DNS configuration + position paper publication at eljeffe.io/position
- A5 → A4 inscription event (position paper hash inscribed; block-height anchor recorded; footer updated)
- G1 UW outreach (founder names specific contact; first conversation Phase A weeks 6-10)
- B4 compliance-architecture role candidate identification (per Tim's preference from B1)

**Month 2 setup (Phase A weeks 9-12):**

- B2 third principal identification + outreach (per Tim's calibration from B1)
- B3 Bart partnership update (per Tim's alignment shape from B1)
- A2 Genesis block inscription (depends on bylaws v1 ratified — C1 + Tim alignment from B1)
- A3 founder smart contract deployment (depends on A2)
- C2 eljeffe Hash and Seal Protocol formal specification (parallel through Month 3)
- F1-F2 → F3 first investor outreach + first close (target Phase A end at month 6)
- **Formation-documents skill build** (separate Cowork session) — operationalize the addendum's 10 architectural decisions into bylaws Articles XV, XVI, revised V, revised VIII, extended XI, and either new XVII or extended XIV. Pre-cursor to amending C1 with the new articles.

## Founder review pass

The artifacts that warrant founder review before any external use:

- **A5 Position paper** — before publication at eljeffe.io/position
- **D5a Memo + D5b Deck** — before the Tim conversation
- **F1-F2 Investor brief** — before any investor outreach
- **B4 Compliance-architecture role scope** — before naming the role's
  candidate
- **A1 Wyoming counsel scope** — before sending to selected counsel
- **G1 UW engagement scope** — before founder identifies the specific
  UW contact and sends the outreach email

The substrate-internal artifacts (bylaws skill SKILL.md, 09-anti-patterns,
the 5 templates, the foundation synthesis) can be reviewed at the founder's
pace; they don't gate any external action.

## Block-height anchor for this wave session

This single-site HTML deliverable is itself a candidate for inscription
(content hash → Bitcoin block). The position paper (A5) is the higher-priority
inscription per the launch prompt's done definition; the wave-deliverable
HTML can be inscribed alongside or after.

## Session close

The wave is complete. Fourteen artifacts shipped — eleven content files,
the consolidated single-site HTML, the Claude.ai design-mode prompt, and
the substrate-port-and-officer-architecture addendum. Foundation synthesis
written; A5 + F1-F2 external-facing artifacts ready for review-and-publish;
D5a memo refined and D5b deck built; C1 bylaws skill completed (with
amendment plan documented in the addendum for the formation-documents skill
to operationalize); B4, A1, A4, G1 engagement scopes ready for counterparty
action; B1 collated as the HTML; reconciliation list flagged for
prior-session output reconciliation when surfaced; addendum integrated as a
forward-design first-class section.

The 100-day intensive begins on Tim's go.
"""

# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def section_html(sec_id: str, title: str, body_html: str, category: str) -> str:
    return f'''
<section id="{sec_id}" data-category="{category}">
  <header class="section-header">
    <span class="cat-pill">{html_lib.escape(CATEGORY_LABELS[category])}</span>
    <h2>{html_lib.escape(title)}</h2>
  </header>
  <div class="section-body">
    {body_html}
  </div>
</section>
'''

def cover_html() -> str:
    return '''
<section id="cover" data-category="overview" class="cover">
  <div class="cover-inner">
    <p class="cover-eyebrow">Wave session deliverable · 2026-05-03</p>
    <h1>Retail vertical</h1>
    <p class="cover-sub">Proposed approach, structure, and 100-day plan.<br/>
    eljeffe Hash and Seal Protocol · Wyoming-anchored · BTC-native · anti-extraction by construction.</p>
    <p class="cover-tag"><em>Tell me where I&rsquo;m wrong.</em></p>
    <p class="cover-meta">Anchored to BTC block height: <span class="block-anchor">TBD</span></p>
  </div>
</section>
'''

# Assemble nav
nav_groups = {}
for sec_id, title, _path, category in SECTIONS:
    if sec_id == "cover":
        continue
    nav_groups.setdefault(category, []).append((sec_id, title))

nav_html = '<nav class="sidebar"><div class="brand"><strong>Wave</strong><br/><span>2026-05-03</span></div>\n<ul class="nav">\n'
nav_html += '<li class="nav-cat-cover"><a href="#cover">Cover</a></li>\n'
for cat in ["overview", "external", "proposal", "substrate", "addendum", "engagement", "close"]:
    if cat not in nav_groups:
        continue
    nav_html += f'<li class="nav-cat"><span>{CATEGORY_LABELS[cat]}</span><ul>\n'
    for sec_id, title in nav_groups[cat]:
        # Trim title for nav
        nav_html += f'    <li><a href="#{sec_id}">{html_lib.escape(title)}</a></li>\n'
    nav_html += '</ul></li>\n'
nav_html += '</ul></nav>\n'

# Sections
sections_html = cover_html()
for sec_id, title, source, category in SECTIONS:
    if sec_id == "cover":
        continue
    if source is not None:
        body = read_section(source)
    else:
        # Inline content
        if sec_id == "deck":
            body = md_to_html(INLINE_DECK_CONTENT)
        elif sec_id == "tim-prep":
            body = md_to_html(INLINE_TIM_PREP)
        elif sec_id == "bylaws-skill":
            body = md_to_html(INLINE_BYLAWS_INDEX)
        elif sec_id == "addendum":
            body = md_to_html(INLINE_ADDENDUM)
        elif sec_id == "close":
            body = md_to_html(INLINE_SESSION_CLOSE)
        else:
            body = "<p>(content forthcoming)</p>"
    sections_html += section_html(sec_id, title, body, category)

# CSS
css = f"""
:root {{
  --navy: {NAVY};
  --deep: {DEEP};
  --teal: {TEAL};
  --cream: {CREAM};
  --sand: {SAND};
  --white: {WHITE};
  --charcoal: {CHARCOAL};
  --serif: Georgia, "Iowan Old Style", "Times New Roman", serif;
  --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Calibri, Roboto, sans-serif;
  --mono: "SF Mono", Menlo, Monaco, Consolas, monospace;
  --col: 760px;
}}

* {{ box-sizing: border-box; }}

html, body {{
  margin: 0; padding: 0;
  font-family: var(--sans);
  background: var(--white);
  color: var(--charcoal);
  line-height: 1.55;
  font-size: 16px;
  scroll-behavior: smooth;
}}

a {{ color: var(--deep); text-decoration: none; border-bottom: 1px solid transparent; transition: border-color 0.15s; }}
a:hover {{ border-bottom-color: var(--deep); }}

.layout {{
  display: grid;
  grid-template-columns: 280px 1fr;
  min-height: 100vh;
}}

@media (max-width: 900px) {{
  .layout {{ grid-template-columns: 1fr; }}
  .sidebar {{ position: static !important; height: auto !important; border-right: none !important; border-bottom: 1px solid #e0e0e0; }}
}}

/* Sidebar */
.sidebar {{
  position: sticky; top: 0; height: 100vh; overflow-y: auto;
  background: var(--navy); color: var(--cream);
  padding: 32px 24px; border-right: 1px solid #e0e0e0;
  font-size: 14px;
}}
.sidebar .brand {{
  font-family: var(--serif);
  font-size: 22px; line-height: 1.1; color: var(--white);
  margin-bottom: 24px; padding-bottom: 16px;
  border-bottom: 1px solid rgba(236, 226, 208, 0.2);
}}
.sidebar .brand span {{
  font-family: var(--sans); font-size: 11px;
  color: var(--cream); opacity: 0.7;
  letter-spacing: 0.05em;
}}
.sidebar ul {{ list-style: none; margin: 0; padding: 0; }}
.sidebar .nav > li {{ margin-bottom: 16px; }}
.sidebar .nav-cat > span {{
  display: block; font-size: 10px; letter-spacing: 0.1em;
  text-transform: uppercase; color: var(--cream); opacity: 0.6;
  margin-bottom: 6px;
}}
.sidebar .nav-cat ul {{ padding-left: 0; }}
.sidebar .nav-cat ul li {{ margin: 2px 0; }}
.sidebar .nav-cat-cover {{ margin-bottom: 24px; }}
.sidebar a {{
  display: block; color: var(--cream); padding: 4px 8px;
  border-radius: 4px; border-bottom: none !important;
  font-size: 13px; line-height: 1.35;
}}
.sidebar a:hover {{ background: rgba(236, 226, 208, 0.1); color: var(--white); }}
.sidebar .nav-cat-cover a {{ font-family: var(--serif); font-size: 16px; color: var(--white); font-weight: bold; }}

/* Main */
main {{ padding: 0; }}

section {{
  max-width: var(--col); margin: 0 auto; padding: 64px 32px;
  border-bottom: 1px solid #f0f0f0;
}}
section:last-child {{ border-bottom: none; }}

.section-header {{ margin-bottom: 32px; }}
.cat-pill {{
  display: inline-block; font-size: 10px; letter-spacing: 0.12em;
  text-transform: uppercase; color: var(--teal); font-weight: bold;
  margin-bottom: 8px;
}}

/* Cover slide */
.cover {{
  background: var(--navy); color: var(--cream);
  max-width: none; min-height: 80vh; padding: 0;
  display: flex; align-items: center; justify-content: center;
  border-bottom: none;
  margin: 0;
}}
.cover-inner {{ max-width: 720px; padding: 64px 32px; text-align: left; width: 100%; }}
.cover-eyebrow {{ font-size: 12px; letter-spacing: 0.15em; text-transform: uppercase; color: var(--cream); opacity: 0.7; margin: 0 0 24px; }}
.cover h1 {{ font-family: var(--serif); font-size: 72px; line-height: 1.0; color: var(--white); margin: 0 0 24px; font-weight: bold; }}
.cover-sub {{ font-family: var(--serif); font-size: 22px; line-height: 1.4; color: var(--cream); margin: 0 0 32px; }}
.cover-tag {{ font-family: var(--serif); font-size: 18px; color: var(--cream); opacity: 0.85; margin: 0 0 48px; }}
.cover-meta {{ font-size: 12px; color: var(--cream); opacity: 0.6; letter-spacing: 0.05em; margin: 0; }}
.block-anchor {{ font-family: var(--mono); }}

/* Typography in main content */
section h1 {{
  font-family: var(--serif); font-size: 36px; line-height: 1.15;
  color: var(--navy); margin: 0 0 16px; font-weight: bold;
}}
section h2 {{
  font-family: var(--serif); font-size: 30px; line-height: 1.2;
  color: var(--navy); margin: 0; font-weight: bold;
}}
.section-body h1 {{
  font-family: var(--serif); font-size: 28px; color: var(--navy);
  margin: 40px 0 16px; padding-top: 8px;
}}
.section-body h2 {{
  font-family: var(--serif); font-size: 24px; color: var(--navy);
  margin: 32px 0 12px;
}}
.section-body h3 {{
  font-family: var(--serif); font-size: 18px; color: var(--deep);
  margin: 24px 0 8px;
}}
.section-body p {{ margin: 0 0 14px; }}
.section-body ul, .section-body ol {{ margin: 0 0 16px; padding-left: 24px; }}
.section-body li {{ margin-bottom: 6px; }}
.section-body strong {{ color: var(--navy); }}
.section-body em {{ color: var(--teal); font-style: italic; }}

.section-body code {{
  font-family: var(--mono); font-size: 0.88em;
  background: var(--sand); color: var(--navy);
  padding: 1px 5px; border-radius: 3px;
}}
.section-body pre {{
  background: var(--sand); padding: 16px; border-radius: 6px;
  overflow-x: auto; font-size: 13px; line-height: 1.45;
  border-left: 3px solid var(--teal);
}}
.section-body pre code {{ background: transparent; padding: 0; }}

.section-body blockquote {{
  border-left: 3px solid var(--teal); margin: 16px 0;
  padding: 4px 0 4px 16px; color: var(--charcoal);
  font-style: italic; background: var(--sand); border-radius: 0 4px 4px 0;
  padding: 12px 16px;
}}

.section-body table {{
  border-collapse: collapse; margin: 16px 0; width: 100%;
  font-size: 14px;
}}
.section-body th {{
  background: var(--navy); color: var(--white);
  padding: 8px 12px; text-align: left; font-family: var(--serif);
  font-weight: bold;
}}
.section-body td {{
  border: 1px solid #e5e5e5; padding: 8px 12px;
  vertical-align: top;
}}
.section-body tr:nth-child(even) td {{ background: var(--sand); }}

.section-body hr {{
  border: none; border-top: 1px solid #e0e0e0;
  margin: 32px 0;
}}

/* Footer */
footer {{
  text-align: center; padding: 48px 32px;
  font-size: 12px; color: var(--charcoal); opacity: 0.7;
  border-top: 1px solid #f0f0f0; background: var(--sand);
  font-style: italic;
}}

/* Print */
@media print {{
  .sidebar {{ display: none; }}
  .layout {{ grid-template-columns: 1fr; }}
  section {{ break-inside: avoid; padding: 32px; max-width: none; }}
  .cover {{ min-height: auto; padding: 64px 32px; }}
}}
"""

js = """
// Active-section highlighting in the sidebar
(function() {
  var sections = Array.from(document.querySelectorAll('section[id]'));
  var navLinks = Array.from(document.querySelectorAll('.sidebar a'));
  if (!('IntersectionObserver' in window)) return;
  var obs = new IntersectionObserver(function(entries) {
    entries.forEach(function(e) {
      if (e.isIntersecting) {
        var id = e.target.getAttribute('id');
        navLinks.forEach(function(a) {
          a.classList.toggle('active', a.getAttribute('href') === '#' + id);
        });
      }
    });
  }, { rootMargin: '-30% 0px -60% 0px', threshold: 0 });
  sections.forEach(function(s) { obs.observe(s); });
})();
"""

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Wave Deliverable — Retail Vertical · 2026-05-03</title>
<style>
{css}
.sidebar a.active {{ background: var(--cream); color: var(--navy); font-weight: bold; }}
</style>
</head>
<body>
<div class="layout">
{nav_html}
<main>
{sections_html}
<footer>
King Harbor — Redondo Beach — pier · Wave session 2026-05-03 · eljeffe Hash and Seal Protocol
</footer>
</main>
</div>
<script>
{js}
</script>
</body>
</html>
"""

out = OUTPUTS / "wave-deliverable.html"
out.write_text(html)
print(f"WROTE: {out}")
print(f"Size: {len(html):,} bytes")
