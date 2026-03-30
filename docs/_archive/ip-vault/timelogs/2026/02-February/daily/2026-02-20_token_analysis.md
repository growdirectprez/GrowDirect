---
type: session
domain: canary
status: active
created: 2026-02-20
updated: 2026-03-19
---
# Token Consumption Analysis — February 20, 2026

**Logged by:** Eva (Program Manager)
**Date Filed:** 2026-02-20
**Classification:** Contemporaneous resource consumption record
**Source Data:** Session transcript `1139612b` (JSONL with embedded usage telemetry)

---

## Executive Summary

February 20 was Canary's heaviest single-day token consumption — 7 context windows burned across a sustained Sprint 2 implementation push. Total estimated API cost: **~$282** across 813 API calls. The day produced 25 deliverables, 85 new tests, and moved LP coverage from 32% → 85%.

**Key finding:** 92.4% of input tokens were cache reads (cheap), not fresh context creation. The system architecture (CLAUDE.md as persistent context, continuation sessions preserving state) is working efficiently. The expensive part isn't the work — it's the context reload on each continuation.

---

## Token Budget — Aggregate

| Category | Tokens | Est. Cost | % of Total Cost |
|----------|--------|-----------|-----------------|
| Input (new) | 36,319 | $0.54 | 0.2% |
| Cache creation | 6,723,071 | $126.06 | 44.7% |
| Cache read | 81,675,653 | $153.14 | 54.3% |
| Output | 6,731 | $0.50 | 0.2% |
| **TOTAL** | **88,441,774** | **~$282** | **100%** |

### Cost Breakdown by Channel

| Channel | API Calls | Est. Cost | % |
|---------|-----------|-----------|---|
| Main conversation (Opus 4) | 511 | $211.26 | 74.9% |
| Subagents — IP scrub (8 agents, mostly Haiku) | 302 | $70.76 | 25.1% |
| **Total** | **813** | **~$282** | **100%** |

---

## Context Window Consumption

| Metric | Value |
|--------|-------|
| Context window size (Opus 4) | 200,000 tokens |
| Continuation sessions | 6 (context ran out, session resumed) |
| Total context windows consumed | 7 |
| Effective context capacity used | ~1,400,000 tokens |
| Cache hit rate | 92.4% (reads vs. fresh creation) |

**Why 7 context windows?** Each continuation session carries forward a compressed summary of prior work, but still needs to reload CLAUDE.md (~15K tokens), CRDM spec (~20K tokens), and project context. The heavy Sprint 2 code generation (chirp.py at 1,445 lines, square_client.py parse helpers, ingestion.py, 3 test files) consumed context rapidly.

---

## Token Allocation by Deliverable (Estimated)

Mapped from session timeline phases to work product. Estimates based on phase duration, output complexity, and API call density.

### Tier 1 — Heavy Token Consumers (code generation + testing)

| Deliverable | Agent | Est. Tokens | Est. Cost | Phases |
|-------------|-------|-------------|-----------|--------|
| 10 Chirp detection rules (`chirp.py`) | Jeremy | ~18M | ~$55 | P5, P6, P9-P11 |
| 6 parse helpers (`square_client.py`) | Jeremy | ~12M | ~$38 | P5, P6, P9-P11 |
| 6 table DDL (`models.py`) | Jeremy | ~8M | ~$25 | P5-P7 |
| 49 Chirp rule tests (`test_chirp_sprint2.py`) | Jeremy | ~8M | ~$25 | P19-P20 |
| 23 parse helper tests (`test_parse_helpers_sprint2.py`) | Jeremy | ~5M | ~$16 | P19-P20 |
| Ingestion layer + 13 tests (`ingestion.py`) | Jeremy | ~5M | ~$16 | P19-P20 |
| **Subtotal — Code Generation** | | **~56M** | **~$175** | |

### Tier 2 — Document Generation & Analysis

| Deliverable | Agent | Est. Tokens | Est. Cost | Phases |
|-------------|-------|-------------|-----------|--------|
| CRDM Gap Analysis | Eva | ~4M | ~$12 | P1, P3-P4 |
| Tom T-3 Schema Review + Brief | Tom | ~5M | ~$15 | P12-P13 |
| Jeremy Implementation Brief | Jeremy | ~3M | ~$9 | P15-P16 |
| Attack Plan v1.2 (F-1/F-2/F-3) | Eva | ~2M | ~$6 | P19 |
| **Subtotal — Documents** | | **~14M** | **~$42** | |

### Tier 3 — IP Scrub (Subagents)

| Deliverable | Agent | Est. Tokens | Est. Cost | Phases |
|-------------|-------|-------------|-----------|--------|
| Vendor name scrub (8 parallel agents) | Syd directive | ~18M | ~$71 | Subagents |
| **Subtotal — IP Compliance** | | **~18M** | **~$71** | |

### Grand Total by Category

| Category | Est. Cost | % of Day |
|----------|-----------|----------|
| Code generation + testing | ~$175 | 62% |
| IP compliance scrub | ~$71 | 25% |
| Document generation | ~$42 | 15% |
| **Total** | **~$282** | **100%** |

---

## Efficiency Metrics

| Metric | Value | Benchmark |
|--------|-------|-----------|
| Cost per deliverable | ~$11.28 | 25 deliverables / $282 |
| Cost per test written | ~$2.05 | 85 tests / ~$175 |
| Cost per Chirp rule (coded + tested) | ~$8.00 | 10 rules / ~$80 |
| Cost per table DDL (coded) | ~$4.17 | 6 tables / ~$25 |
| Cost per scrubbed file | ~$8.88 | 8 files / ~$71 |
| Output tokens per API call | 8.3 | Very low — mostly tool use + reads |
| Cache efficiency | 92.4% | Excellent — context reuse working |

---

## Where Tokens Were "Wasted" (Optimization Opportunities)

### 1. Context Continuations (~30% of cache creation cost)
Each of the 6 continuations required re-establishing context (~80K tokens of CLAUDE.md, CRDM, project state). This is the single largest efficiency loss. **Mitigation:** Shorter, more focused sessions with clear deliverable boundaries.

### 2. IP Scrub Subagents ($71 for text replacement)
8 parallel Haiku agents scrubbing vendor names is expensive for what amounts to find-and-replace. **Mitigation:** A simple Python script could do this in seconds for <$0.01. Reserve subagents for judgment-intensive work.

### 3. "Keep going" Continuations (P9, P10, P11, P16)
Four phases where the user said "keep going" — each required context re-read. **Mitigation:** Batch larger work units before pausing for user input.

### Estimated Recoverable Savings

| Optimization | Est. Savings |
|--------------|-------------|
| Script-based IP scrub instead of subagents | ~$65 |
| Fewer continuation breaks (3 instead of 6) | ~$40 |
| Batch "keep going" into single phases | ~$15 |
| **Total recoverable** | **~$120 (43% of day)** |

---

## Forward-Looking Token Budget Framework

### Proposed Per-Sprint Token Budget

Based on Feb 20 actuals, extrapolated to a standard 2-week sprint:

| Activity | Est. Tokens/Sprint | Est. Cost/Sprint |
|----------|-------------------|-----------------|
| Code generation (features) | 60-80M | $180-240 |
| Test writing | 15-20M | $45-60 |
| Document generation (specs, briefs) | 10-15M | $30-45 |
| Code review + debugging | 5-10M | $15-30 |
| Planning + coordination | 3-5M | $9-15 |
| **Sprint total** | **93-130M** | **$280-$390** |

### Tracking Method (Going Forward)

1. **Session-level:** Each Cowork session generates a JSONL transcript with embedded `usage` telemetry. Token counts are per-API-call with input/output/cache breakdown.

2. **Deliverable tagging:** Eva tags each session phase with the deliverable it produced. The timelog already tracks hours→deliverables; token tracking is the parallel resource dimension.

3. **Daily roll-up:** Add a `## Token Consumption` section to the daily timelog with aggregate numbers extracted from the JSONL.

4. **Sprint retrospective:** Aggregate daily numbers into sprint-level token budget vs. actual.

### What We Can't Track (Yet)

- **Anthropic billing dashboard:** We don't have API-level billing access from within Cowork. The JSONL usage data is our best proxy.
- **Per-file token cost:** We can estimate based on session phases but can't attribute tokens to individual file edits with precision.
- **Cross-session totals:** Each Cowork session gets a new transcript. We'd need a roll-up script to aggregate across sessions.

---

## Recommendations

1. **Build a `scripts/token_report.py`** — Automate JSONL parsing. Run daily. Output markdown for the timelog. Jeremy: 30 minutes.

2. **Add token budget to sprint planning** — Eva should set a token ceiling per sprint alongside the time budget. Proposed: $400/sprint for Sprint 2.

3. **Reserve subagents for judgment work** — Don't use Haiku subagents for text replacement. Use Python scripts. Save subagents for code review, research, multi-file analysis.

4. **Minimize continuation sessions** — Each costs ~$20 in cache re-creation. Plan sessions around natural breakpoints (e.g., "write tests" = one session, "write code" = another).

5. **Track cost-per-deliverable as a KPI** — Today's $11.28/deliverable is our baseline. If it trends above $20, investigate.

---

*Token data extracted from session transcript 1139612b. Cost estimates use Claude Opus 4 API pricing ($15/MTok input, $18.75/MTok cache create, $1.875/MTok cache read, $75/MTok output). Haiku subagents use lower rates but are grouped with Opus for conservative estimation. Actual Anthropic billing may differ.*
