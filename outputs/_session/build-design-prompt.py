#!/usr/bin/env python3
"""
Build the Claude.ai design-mode prompt — a paste-ready markdown file that,
when pasted into a fresh Claude.ai conversation, instructs Claude to render
the wave deliverable as a designed single-site artifact.

Output: outputs/wave-deliverable-claude-design-prompt.md
"""

from pathlib import Path

OUTPUTS = Path("/sessions/lucid-peaceful-tesla/mnt/GrowDirect/outputs")

def read_md(path: str) -> str:
    full = OUTPUTS / path
    if not full.exists():
        return f"*[Source not found: {path}]*"
    text = full.read_text()
    # Strip YAML frontmatter
    if text.startswith("---"):
        end = text.find("---", 3)
        if end >= 0:
            text = text[end+3:].lstrip()
    return text

# ---------------------------------------------------------------------------
# Top-level brief
# ---------------------------------------------------------------------------

BRIEF = """
# Design brief — single-site HTML artifact (Wave session deliverable, 2026-05-03)

You are designing a single-site HTML artifact that renders a report-style
deliverable for a venture-formation proposal. The deliverable consolidates
twelve source artifacts into one navigable web page that can be opened in
a browser, shared as a URL, printed cleanly, or embedded in an email.

The intended reader is the founder's principal counterparty — Tim — plus
adjacent reviewers (compliance-architecture lead candidates, Wyoming counsel
prospects, capital-allocator investors, UW academic contacts). The reader's
posture is *operator skim first, then deep dive on the sections that warrant
it.* The artifact must reward both reads.

This is a substantive document, not a marketing site. Operator language.
No SaaS-marketing copy. No theater. The visual design should feel like a
boutique-firm investor memo crossed with a 1963 nonprofit charter — confident,
spare, lineage-anchored, slightly editorial.

## Output format

A single self-contained HTML artifact. Use shadcn/ui + Tailwind via React,
or pure HTML + CSS — your call. Constraints:

- One file or one artifact bundle
- No external dependencies that won't load in a static-hosted environment
  (Cloudflare Pages, GCS bucket, Vercel) other than CDN-loaded React/Tailwind
  if you go the React route
- Loads fast on a slow connection (no heavy media; lazy-load any future
  imagery)
- Print-friendly (the founder may PDF this for offline review)
- Accessible (semantic HTML; sufficient color contrast; keyboard navigable)
- Responsive (mobile renders cleanly without sacrificing the desktop
  navigation experience)
- Sticky sidebar nav on desktop; collapsible drawer or sticky top bar on
  mobile
- Active-section highlighting in the nav as the user scrolls
- Block-height anchor placeholder in the cover and footer
  (`Anchored to BTC block height: TBD`)

## Design parameters

**Color palette — Ocean Gradient with Cream accent.**

| Token | Hex | Where it lives |
| --- | --- | --- |
| `navy` | `#21295C` | Cover background; section headers; primary text on dark |
| `deep` | `#065A82` | Accent links; secondary header text; chart primary |
| `teal` | `#1C7293` | Italic accents; section eyebrows; pull quotes |
| `cream` | `#ECE2D0` | Light text on navy; cover accents |
| `sand` | `#F5F1E8` | Code blocks; alternate row backgrounds; soft callouts |
| `white` | `#FFFFFF` | Primary background |
| `charcoal` | `#36454F` | Body text |

The dominant 60-70% should be white background with charcoal body text.
Navy is the deep accent — used for the cover, section headers, and the
sidebar. Cream/sand provide warmth in callouts and code blocks.

**Typography.**

- Headings: Georgia (or "Iowan Old Style" / "Times New Roman" fallback) —
  serif, slightly editorial, weight bold
- Body: system sans (`-apple-system, BlinkMacSystemFont, "Segoe UI",
  Calibri, Roboto, sans-serif`) — clean, readable
- Code / monospace data: SF Mono / Menlo / Consolas — for hashes,
  block heights, txids
- Body size: 16px; line-height 1.55
- Headline scale: 36px (section h1) → 28px (h2) → 22px (h3) → 18px (h4)
- Cover headline: 64-72px serif bold

**Layout.**

- Two-column layout on desktop: 280px sidebar nav (sticky, full-height,
  navy background) + main content column (max-width ~760px, centered,
  generous margins)
- Mobile: collapsible nav (drawer or top bar); main content full-width
  with 24px horizontal padding
- 64px vertical padding above and below each section; 32px horizontal
  inside section
- Border-bottom 1px on each section for visual rhythm; remove on the last

**Visual motifs.**

Pick ONE distinctive element and repeat it consistently:

- *Option A:* Small accent rule (4px wide, cream-on-navy or teal-on-white)
  on the left margin of cover and section headers
- *Option B:* Eyebrow text (12px, uppercase, letter-spaced, teal) above
  every section title
- *Option C:* Pull-quote treatment for the lineage statements with serif
  italic + teal left border

I recommend Option B (eyebrows). Avoid full-width colored bars across the
top of every section — that reads as AI-generated.

**No.**

- No accent lines under titles (AI-slop signature)
- No decorative full-width colored bars/header strips
- No cream/beige page backgrounds (use white)
- No emoji decoration in headers
- No SaaS-marketing-copy language anywhere
- No "best-in-class," "industry-leading," "comprehensive solution"
- No historical-lineage citation paragraphs ("this comes from the 1929 X" /
  "Article VI Section 3 of the 1949 Y") — the structural patterns are what
  matter; the citation density loses the reader

## Voice rules (non-negotiable)

These are the rules the source content was written under. Preserve them in
any visual treatment, captioning, or summary you add:

1. **Form follows function.** Lead with what the substrate does for the
   reader. Performative historical citations get cut. Bitcoin's Section 3
   (Timestamp Server) is the substrate's actual technical foundation and
   stays as a one-line technical reference; everything else lineage-flavored
   should be expressed structurally rather than historically.
2. **Anti-extraction is structural.** No HR. No shared services. No
   PE-style mechanisms. The substrate handles the function. State this as
   architecture, not as values.
3. **Roles, not names.** Compliance-architecture lead / third principal /
   Domain principal / Ops principal / Governance principal. Tim and Bart
   appear by name only where the relationship requires it.
4. **Bart-respect.** No surfer-drift puns. No DriftPOS-as-legacy-being-
   replaced framing. Peer treatment.
5. **Operator-readable.** Would a non-technical reader understand the claim
   on a single read? If not, rewrite. Plain numbers, plain consequences,
   plain mechanisms.
6. **King Harbor / Redondo Beach / pier.** Location anchor in cover and
   footer (low key — operational detail, not a banner).
7. **eljeffe Hash and Seal Protocol.** Formal substrate name. Use formally
   where the formal name is right; plainer language for non-technical
   audiences.
8. **Compliance-by-architecture.** Load-bearing claim. The substrate
   produces audit-defensible evidence by construction. Don't oversell;
   don't undersell.
9. **Block-height anchor.** Any artifact that benefits from on-chain
   provenance carries one. The cover and footer reference it; the actual
   block height is filled in at publication.
10. **What this protects.** Customer data sovereignty / contributor
    permanent-stake / operator un-cullability are the three concrete
    protections. State them; don't dress them as values.

## Structure — sections in nav order

The artifact has 13 sections grouped into 6 categories. Render the sidebar
nav with category labels (small caps, opacity 0.6) and section links beneath.

| # | Section ID | Title | Category | Notes |
| --- | --- | --- | --- | --- |
| 1 | `cover` | Cover | (no category — first thing) | Dark cover; navy bg; large serif headline; eyebrow date; tagline; meta line |
| 2 | `foundation` | Foundation synthesis | Overview | Wave session corpus inventory + voice rules + cross-reference map |
| 3 | `position` | A5 — Position paper for eljeffe.io/position | External-facing | Public-facing single-page document — hero treatment for the lineage section |
| 4 | `investor` | F1-F2 — Investor brief | External-facing | Capital-allocator extension; VeriSign analogy table; Metcalfe valuation table |
| 5 | `memo` | D5a — Memo to principals (retail vertical) | Principal-facing proposal | The primary proposal; "Tell me where I'm wrong" energy |
| 6 | `deck` | D5b — Shore Club retail-vertical deck | Principal-facing proposal | Slide-content rendered as inline sections |
| 7 | `tim-prep` | B1 — Tim conversation prep package | Principal-facing proposal | Conversation agenda + open-decisions list; THIS IS THE COLLATION |
| 8 | `bylaws-skill` | C1 — namespace-bylaws skill | Substrate skill | Index/reference of the bylaws skill structure |
| 9 | `compliance-role` | B4 — Compliance-architecture role scope | Engagement scopes | Role definition + scope of work + comp structure |
| 10 | `wyoming` | A1 — Wyoming counsel engagement scope | Engagement scopes | Counsel selection criteria + Phase 1/2 engagement structure |
| 11 | `dns` | A4 — DNS / publication scope | Engagement scopes | DNS + minimal-site + block-height anchor mechanic |
| 12 | `uw` | G1 — UW engagement scope | Engagement scopes | Outreach email template + 30-min call agenda |
| 13 | `close` | Session close — artifacts produced, decisions, next steps | Session close | Reconciliation list + next-session priorities + founder review pass |

## Visual treatment by section type

- **Cover.** Dark (navy) background, full viewport height (or 80vh).
  Large serif headline. Eyebrow with date. Subtitle in serif. Tag line in
  italic. Meta line at bottom with location anchor + block-height
  placeholder.
- **External-facing sections** (`position`, `investor`). Slightly more
  visual emphasis on the lineage paragraphs and the "what we're asking" /
  "investor sentence" pull quotes. Tables get the navy header treatment.
- **Principal-facing sections** (`memo`, `deck`, `tim-prep`). Standard
  body treatment. The memo's "Tell me where I'm wrong" closing line
  gets pull-quote emphasis. The deck section can use a subtle slide-divider
  pattern between the 12 slide blocks (small numbered eyebrow per slide).
- **Substrate skill section** (`bylaws-skill`). Reference / index treatment.
  Tighter typography. The file-list table is the primary content.
- **Engagement scopes** (`compliance-role`, `wyoming`, `dns`, `uw`).
  Standard body treatment with strong section headers and clear table
  treatments for engagement structures, deliverables timelines, etc.
- **Session close** (`close`). The artifact-table is the hero element.
  Reconciliation list and next-session priorities below.

## Content payload

The full content of each section follows. Render each as the section's body
with the markdown converted to HTML/JSX. Preserve all tables, code blocks,
italic and bold treatments, and cross-references.

Where you see a cross-reference like `#position` or `outputs/dispatches/...md`,
render those as functional anchor links (within the artifact) or as styled
code (for external file paths the reader would need to look up separately).

---

"""

# ---------------------------------------------------------------------------
# Section content — same payload as build-deliverable.py
# ---------------------------------------------------------------------------

SECTIONS = [
    ("foundation", "Foundation synthesis", "_session/foundation-synthesis.md", "overview"),
    ("position", "A5 — Position paper for eljeffe.io/position", "position-paper-eljeffe-io.md", "external"),
    ("investor", "F1-F2 — Investor brief", "investor-brief-eljeffe-io.md", "external"),
    ("memo", "D5a — Memo to principals (retail vertical)", "memo-to-principals-retail-vertical.md", "proposal"),
    ("deck", "D5b — Shore Club retail-vertical deck", None, "proposal"),
    ("tim-prep", "B1 — Tim conversation prep package", None, "proposal"),
    ("bylaws-skill", "C1 — namespace-bylaws skill", None, "substrate"),
    ("addendum", "Addendum — what the substrate adds next", None, "addendum"),
    ("compliance-role", "B4 — Compliance-architecture role scope", "dispatches/B4-compliance-architecture-role.md", "engagement"),
    ("wyoming", "A1 — Wyoming counsel engagement scope", "dispatches/A1-wyoming-counsel-scope.md", "engagement"),
    ("dns", "A4 — DNS / publication scope", "dispatches/A4-dns-publication-scope.md", "engagement"),
    ("uw", "G1 — UW engagement scope", "dispatches/G1-uw-engagement-scope.md", "engagement"),
    ("close", "Session close — artifacts produced, decisions, next steps", None, "close"),
]

# Inline content (mirrors build-deliverable.py)
INLINE = {
    "addendum": """
# Addendum — what the substrate adds next

Forward design for the formation-documents skill. The bylaws skill ships now with what's already operationally needed for Phase A. The addendum specifies the architectural extensions — three new or revised articles, three drafting-discipline additions, four open questions — that the formation-documents skill operationalizes in the next wave. Full design notes live at `outputs/addendum-substrate-port-and-officer-architecture.md`.

## Architectural decisions (10)

**1. Three port classes — Member, Council, Audit.** Same physical mechanism (an MCP service plugged into a port) routes to three different financial and constitutional rails. Member ports L402-gated, packets-served compensation. Council ports treasury-paid (oversight is not metered). Audit ports for external compliance entities (regulators, security firms) holding no ordinal but with defined inspection rights.

**2. Introduction-accountability-revocation contract.** Every entity plugging into a port emits a port declaration with identity / provenance commitment / intent stream / revocation conformance. Three revocation tiers: Pause / Revoke / Quarantine.

**3. Packets-served equity model — formalized via Article XI.** L402 micropayments wrap every Member Port. Three principles must hold: acceptance signal (packets accepted as useful constitute the equity ledger entry), packet-type definitions (platform-wide), retroactive unwinding (quarantine revokes accepted status; equity unwinds).

**4. Annexation Article (XVI) — substrate-namespace relationship.** Two valid models, namespace electing at constitution: lease (operationally independent namespace) or subdivision-with-root-operating-company (substrate retains active operational presence). Article enumerates must-inherit articles, permitted variation, term and renewal, reversion conditions, modification thresholds.

**5. Officer Ordinal class — held by namespace contract address.** New ordinal class held by the namespace's smart contract address rather than by individuals. Operated by named delegates (human, agentic, or hybrid). Membership coextensive with the role. Solves the agentic-officer constitutional standing problem cleanly.

**6. Bridged-accountability — officers serving substrate-and-namespace simultaneously.** Officer operates two officer ordinals (substrate-level and namespace-level). Accountable to namespace board for operational performance, to substrate bylaws for structural conformance, with standing in both layers to escalate breach. Structural safeguard against rogue subDAOs.

**7. Agentic Secretary — canonical bridged-officer instance.** The Secretary role implemented agentically: maintains on-chain ledger continuously, issues conclusive-evidence certificates downstream consumers can rely on, handles delinquency notices and lien recording, generates periodic disclosures. Bounded function maps cleanly to deterministic agentic operation.

**8. Reversion-on-material-breach — added to Article VIII.** Strongest enforcement mechanism. Defines material breach (treasury raid, alignment-check sabotage, identity fraud, malicious port publication, willful substrate-level violation), establishes adjudication procedure (Council Port-class review independent of breaching member, Board vote at structural-amendment threshold, founder consent / lineage-weighted ratification per phase), high invocation threshold so the clause is a backstop.

**9. Voided-but-preserved documentary discipline.** When a clause becomes unenforceable: preserve verbatim in the historical record, mark visibly void, inscribe override rationale, cite override authority, do not erase. Amendment never overwrites; it inscribes prior state and override rationale on chain.

**10. External-validation council loop — active operational pattern.** External review continuous, executed via Audit Ports. Findings route through triage by operator-of-record (external-validation language to bank / real finding to action / context-blind suggestion to discount), inscribe both finding and triage decision, multi-reviewer reconciliation via port-declaration schema, acceptance loop auditable over time.

## Drafting order recommended

XVI (load-bearing — lease-vs-subdivision election determines structural posture) → V (Officers, including officer-ordinal class and bridged-accountability) → XV (Service Ports, building on the officer infrastructure from V) → VIII (reversion clause) → XI extension (packets-served equity formalization) → XIV extension or new XVII (voided-but-preserved drafting discipline).

Each article in the substrate's two-layer style (cultural clause + technical clause + cross-references). Each passes through the alignment checks per Article XIV before ratification.

## Open questions

| # | Question | Default lean |
| --- | --- | --- |
| Q1 | Lease vs subdivision — substrate-default or namespace-choice? | Mandatory election at constitution |
| Q2 | Operator-of-record liability for Council Ports — namespace indemnifies from treasury, or operators bear individual risk? | Open |
| Q3 | Bridged-officer revocation when substrate and namespace disagree — which authority prevails? | Substrate (with explicit precedence rules per officer role) |
| Q4 | Audit Port admission threshold — voluntary path and required path likely both need specification | Both paths specified |

## Why this matters for the wave

Three of the wave's open decisions are materially affected: the third principal candidate decision (open decision #1 — bridged-officer model changes the role definition), the open-source vs proprietary line (open decision #4 — Service Ports schema is a candidate for open-source publication), and Heal's role (open decision #5 — principal-tier vs Council Port advisory changes constitutional standing and compensation rail).

These addendum-driven implications surface as Tim's calibration on the original 8 open decisions, not as new asks.
""",

    "deck": """
# Shore Club retail-vertical deck — content

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
""",

    "tim-prep": """
# B1 — Tim conversation prep package

**Status:** Ready for the Tim conversation. This single-site HTML *is* the
collation. Tim opens this URL (or the file), reads top-to-bottom or jumps
via the navigation, and arrives at the conversation with the same context
the founder has.

**Format note:** Per the deliverable directive, the package is the
single-site HTML wrapping every relevant artifact rather than a separate
collation document. The four sections that matter for the Tim conversation
specifically are linked below; the rest of the HTML is supporting context.

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

## Counterparty questions — what we need from Tim to unblock the next wave

Specific items Tim's response unblocks:

- **B2 third principal outreach** — Tim's preference shape determines the
  outreach plan
- **B3 Bart partnership update** — Tim's alignment shapes what Bart hears;
  if Tim wants Bart looped in earlier, B3 accelerates
- **A1 Wyoming counsel selection** — Tim's existing Wyoming-counsel
  relationships (if any) shorten the cycle
- **F1 investor target identification** — Tim's network may include Tier-1
  (Bitcoin-native) or Tier-2 (values-aligned independent operators)
  candidates

## What success looks like at conversation close

- Tim has read the memo, position paper, and (at minimum) skimmed the deck
- Tim's stated alignment / pushback / counter-proposals on the structure
  are captured in writing
- Open decisions 1, 5, 8 have at least preliminary answers
- A specific next-checkpoint date is set
- A specific list of which Phase A dispatches kick off this week is agreed,
  with named owner per dispatch
- If the answer is "proceed": Tim approves engaging Wyoming counsel (A1)
  and Tim approves the founder beginning the third-principal outreach (B2)

If alignment is reached at conversation close, the wave moves from staging
into execution within 48 hours.

*King Harbor — Redondo Beach — pier.*
""",

    "bylaws-skill": """
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
""",

    "close": """
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
| 12 | **Wave deliverable HTML** | `outputs/wave-deliverable.html` | Shipped |
| 13 | **Claude.ai design-mode prompt** | `outputs/wave-deliverable-claude-design-prompt.md` | Shipped |

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

The 8 reference docs (01-08) absorbed from the prior-session uploads are
canonical and were not modified.

## Open-decision list updated

No new resolutions reached this wave. The 8 open decisions from the
company-formation epic Part 5 carry forward unchanged into the Tim
conversation. Tim's calibration on items 1, 5, 8 is the priority for the
conversation; items 2, 3, 4, 6, 7 can be deferred to follow-up checkpoints.

## Next-session priorities

**Month 1 finishing items (Phase A weeks 4-8):**

- B1 Tim conversation execution (this HTML supports it; conversation needs to happen)
- A1 Wyoming counsel selection and engagement
- A4 DNS configuration + position paper publication at eljeffe.io/position
- A5 → A4 inscription event (position paper hash inscribed; block-height anchor recorded; footer updated)
- G1 UW outreach (founder names specific contact)
- B4 compliance-architecture role candidate identification (per Tim's preference from B1)

**Month 2 setup (Phase A weeks 9-12):**

- B2 third principal identification + outreach (per Tim's calibration from B1)
- B3 Bart partnership update (per Tim's alignment shape from B1)
- A2 Genesis block inscription (depends on bylaws v1 ratified — C1 + Tim alignment from B1)
- A3 founder smart contract deployment (depends on A2)
- C2 eljeffe Hash and Seal Protocol formal specification (parallel through Month 3)
- F1-F2 → F3 first investor outreach + first close (target Phase A end at month 6)

## Session close

The wave is complete. Thirteen artifacts shipped — eleven content files,
the consolidated single-site HTML, and this Claude.ai design-mode prompt.
The 100-day intensive begins on Tim's go.
""",
}

# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

OUT_PATH = OUTPUTS / "wave-deliverable-claude-design-prompt.md"
parts = [BRIEF.lstrip()]

for sec_id, title, source, category in SECTIONS:
    parts.append(f"\n\n---\n\n## SECTION: `{sec_id}` — {title}\n\n")
    parts.append(f"*Category: {category}*\n\n")
    if source is not None:
        parts.append(read_md(source).strip())
    else:
        parts.append(INLINE[sec_id].strip())

parts.append("""

---

## Closing instruction

Render this as a single-site HTML artifact. Apply all design parameters and
voice rules above. Preserve every cross-reference, table, code block, and
italic/bold treatment. The reader can open this in a browser, share it, and
print it cleanly. Block-height anchor placeholder in cover and footer.

When complete, the artifact should feel like a boutique-firm investor memo
that a 60-year-old gun-store owner could open and immediately recognize as
not-the-usual-tech-pitch. Confident. Lineage-anchored. Spare. Editorial.

That's the design.

*King Harbor — Redondo Beach — pier.*
""")

OUT_PATH.write_text("".join(parts))
print(f"WROTE: {OUT_PATH}")
print(f"Size: {OUT_PATH.stat().st_size:,} bytes")
print(f"Lines: {len(OUT_PATH.read_text().splitlines()):,}")
