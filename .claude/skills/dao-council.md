---
name: dao-council
description: >
  DAO governance council — spawns 5 independent delegates with distinct legal/technical
  mandates to stress-test claims, positions, and architectural decisions. Each delegate
  argues independently, then all responses are anonymized and peer-reviewed. A chairman
  synthesizes the final verdict with per-claim confidence ratings. Use when evaluating
  legal positions (Lot H, covenant enforcement, Davis-Stirling compliance), architecture
  decisions, or any high-stakes question where being wrong is expensive. Trigger phrases:
  "council this", "run the council", "stress-test this", "DAO review", "governance council".
---

# DAO Governance Council

A deliberation skill that spawns 5 independent delegates to adversarially evaluate
a position, then runs anonymous peer review and synthesizes a governance-grade verdict.

Based on Karpathy's LLM Council method: multiple independent perspectives + anonymous
peer review catches blind spots that no single analysis surfaces.

## When to Use

- Evaluating legal positions before the board acts on them
- Stress-testing covenant enforcement theories
- Reviewing architectural decisions with expensive failure modes
- Any claim where agreeable AI is dangerous

## How It Works

### Phase 1: Context Gathering

Before spawning delegates, gather all relevant source material. The council is only
as good as the evidence each delegate receives.

For legal positions, gather:
- The position document itself (the claims being evaluated)
- Referenced recorded instruments, case law citations
- Relevant bylaws sections (`cove/governance/wpbca-bylaws-config.json`)
- Parcel data from `land_divisions` if relevant
- Any archived documents from the vault

**Lot H / WPBCA / Peninsula positions:** ALWAYS start by reading
`Cove/docs/council/LOT-H-CONTEXT-BRIEF.md` — this is the canonical
evidence packet covering all recorded instruments, entity history,
data architecture, assessed values, open research threads, and
geospatial state. Every delegate receives this brief identically
as their factual foundation. If the brief doesn't cover a fact
the position claims, the delegate must flag it as unverified.

For technical decisions, gather:
- The design document or spec
- Relevant existing code
- Platform standards from CLAUDE.md
- Prior art (check memory bus, docs/decisions/)

Read all source material and prepare a **context brief** — a factual summary of
the evidence (not the claims) that each delegate receives identically.

### Phase 2: Delegate Dispatch

Spawn all 5 delegates in parallel using the Agent tool. Each delegate receives:

1. The context brief (identical for all)
2. The position/claims being evaluated
3. Their specific mandate (below)
4. Instructions to produce a structured response

**Critical: delegates must NOT see each other's responses.** Each runs independently
in its own agent. This prevents groupthink.

#### The Five Delegates

Configure delegates based on the domain. Choose the appropriate roster:

**Legal Roster** (covenant enforcement, Davis-Stirling, governance positions):

| Delegate | Mandate |
|----------|---------|
| **Title Examiner** | Read only the recorded instruments and chain of title. Verify every factual claim about what the documents say. Flag any claim that reads the instruments more favorably than a neutral title officer would. Do not make policy arguments. |
| **Opposing Counsel** | You represent the party who wants this position to fail. Find every attack vector: laches, changed conditions, standing defects, procedural gaps, statutory preemption, merger with zoning. Your job is to write the opposition brief. |
| **Statutory Specialist** | Focus on current California statutory law. Does each claim hold under the current Civil Code (post-AB 805 recodification)? Check every code section cited. Flag outdated references. Identify any statutory change that affects the argument. |
| **Regulatory Advisor** | Look at this from the land use and housing law side. Housing Accountability Act, Builder's Remedy, Housing Element compliance, CEQA. What regulatory moves could undermine the private covenant position? What's the interaction between public zoning and private restrictions? |
| **Strategic Operator** | You are the only non-legal voice. Assess: Can this community actually execute this position? What does litigation cost? What happens if asserting the broad theory provokes a declaratory judgment that resolves covenants against you? What's the sequencing risk? What does the community gain vs. what it risks? |

**Technical Roster** (architecture, system design, code review):

| Delegate | Mandate |
|----------|---------|
| **Correctness Auditor** | Verify the technical claims are factually correct. Check code paths, data models, API contracts. Flag anything that doesn't match the actual codebase. |
| **Failure Analyst** | Assume this will break. How? What are the failure modes — data corruption, race conditions, security gaps, scale limits? What's the blast radius of each failure? |
| **Standards Reviewer** | Check against platform standards (CLAUDE.md, tech stack conventions). Does this follow existing patterns or create new ones? If new, is there a good reason? |
| **Integration Tester** | How does this interact with everything else? Other blueprints, other services, the database, the frontend. Where are the seams that could tear? |
| **Operator** | Can you actually ship, deploy, and maintain this? What's the migration path? What breaks for existing users? What's the rollback plan? |

**Treasury Roster** (capital deployment, trading strategies, treasury operations):

| Delegate | Mandate |
|----------|---------|
| **Risk Officer** | Evaluate every claim through capital preservation and downside scenarios. What is the maximum loss? Are stated win rates credible? Is the risk budget appropriate? What happens when multiple correlated strategies fail simultaneously? Does the kill switch actually work in a flash crash? Find the holes in the risk framework. |
| **Market Analyst** | Verify market opportunity claims are factually accurate. Are win rates survivorship bias? What does actual data say about returns? How many competing bots exist? What's the realistic opportunity at the proposed capital level? Search for current market data before rendering judgment. |
| **Regulatory Counsel** | Assess legal and regulatory exposure. Can the entity legally operate this activity? What are CFTC, SEC, FinCEN implications? Does entity structure (DUNA) provide actual regulatory cover or just formation cover? What's the liability chain if capital is lost? Does governance create fiduciary duties that conflict with automated trading? |
| **Platform Architect** | Does this fit the GrowDirect platform or is it being forced into the wrong mold? Does the tech stack work for this use case? What are the real-time, uptime, and latency requirements? Should this be a different kind of service? Where does the AI agent loop run? |
| **Strategic Operator** | The only non-technical, non-legal voice. Can the team actually execute this given current workload? What's the opportunity cost against primary revenue apps? Is the absolute dollar upside worth the engineering investment? What's the sequencing risk? What happens to investor perception? |

#### Delegate Prompt Template

Each delegate agent receives this prompt structure:

```
You are a delegate on a governance council. Your mandate: {mandate}

You are evaluating the following position:
---
{position_document}
---

Supporting evidence:
---
{context_brief}
---

Respond with:

## Assessment
For each major claim in the position, state:
- **Claim:** [restate the claim]
- **Rating:** STRONG | CONTESTED | SPECULATIVE | UNFOUNDED
- **Reasoning:** [your analysis from your mandate's perspective]
- **Key risk:** [the single biggest vulnerability in this claim]

## Overall Position
- **Strongest element:** [which claim is best supported]
- **Weakest element:** [which claim is most vulnerable]
- **What everyone will miss:** [the thing that's not in the document but should be]

Be direct. Do not hedge. Your job is to find problems, not validate the position.
```

### Phase 3: Anonymous Peer Review

After all 5 delegates return, anonymize their responses:

1. Strip delegate names — label them Response A through E
2. Shuffle the mapping (A is not necessarily Delegate 1)
3. Compile all 5 responses into a single review document

Spawn 5 NEW reviewer agents (or reuse with fresh context). Each reviewer receives
ALL anonymized responses and answers:

```
You are reviewing 5 independent analyses of a governance position.

The anonymized responses are below. You do not know which perspective produced which.

{all_five_responses_anonymized}

Answer these questions:

1. **Strongest response:** Which response (A-E) is most rigorous and why?
2. **Biggest blind spot:** Which response has the most critical gap?
3. **Consensus claims:** Which claims do all 5 agree on? (These are likely solid.)
4. **Contested claims:** Where do they disagree? (These need more work.)
5. **What all five missed:** What question or risk does NONE of them address?

Question 5 is the most important. Take your time with it.
```

### Phase 4: Chairman Synthesis

After peer review completes, synthesize everything into the final verdict.
This can be done inline (no separate agent needed).

Read all delegate responses + all peer reviews and produce:

```markdown
# DAO Council Verdict: {topic}

**Date:** {date}
**Delegates:** {roster_type} (5 independent, anonymized peer review)
**Source:** {position_document_path}

## Claim-by-Claim Assessment

| # | Claim | Confidence | Consensus | Key Risk |
|---|-------|------------|-----------|----------|
| 1 | ... | STRONG/CONTESTED/SPECULATIVE | 5-0 / 4-1 / 3-2 | ... |

## Strongest Ground
{what the council agrees is most defensible}

## Most Vulnerable Ground
{what the council agrees is weakest — this is where opponents will attack}

## Blind Spot Report
{what the peer review caught that no individual delegate saw}

## Strategic Recommendation
{what to do with this position — act, refine, shelve, or sequence}

## Dissenting Views
{any delegate that reached a fundamentally different conclusion — include their reasoning}

## Full Transcript
{link to markdown file with all delegate responses and peer reviews}
```

### Phase 5: Output

Save two files:

1. **Verdict (HTML):** A scannable visual report saved to the workspace.
   Use a clean single-file HTML with inline CSS. Include the claim table,
   confidence ratings with color coding (green/yellow/red), and collapsible
   sections for the full reasoning.

2. **Transcript (Markdown):** The complete record — all delegate responses,
   all peer reviews, the synthesis. Saved alongside the verdict for audit.

File naming: `dao-council-{topic-slug}-{date}.html` and `.md`

Save to: `docs/council/` in the relevant app repo (e.g., `Cove/docs/council/`).

## Running the Council

When triggered, follow this sequence:

1. **Identify the position** — read the document being evaluated
2. **Gather context** — pull all referenced source material
3. **Select roster** — legal or technical based on the domain
4. **Spawn 5 delegates** in parallel (Agent tool, all in one message)
5. **Wait for all to complete**
6. **Anonymize and shuffle** responses
7. **Spawn 5 peer reviewers** in parallel
8. **Wait for all to complete**
9. **Synthesize** the chairman verdict
10. **Save** HTML verdict + markdown transcript

The whole process runs in one session. No external services needed.

## Example Invocation

```
council this: evaluate the legal position in lot-h-legal-position.md —
are the covenant enforcement claims well-reasoned? Use the legal roster.
```
