---
date: 2026-04-22
type: wiki
tags: [growdirect, timelog, token-analysis, resource-consumption, sprint-2]
sources:
  - docs/_archive/ip-vault/timelogs/2026/02-February/daily/2026-02-20_token_analysis.md
last-compiled: 2026-04-22
needs-review: 2026-05-06
---

**Wiki:** [[Brain/Home|Home]]

# Token Consumption Analysis — February 20, 2026

**Logged by:** Eva (Program Manager)
**Classification:** Contemporaneous resource consumption record
**Source Data:** Session transcript `1139612b` (JSONL with embedded usage telemetry)

## Executive Summary

Canary's heaviest single-day token consumption: **7 context windows burned** across a sustained Sprint 2 implementation push. Total estimated API cost **~$282** across **813 API calls**. 25 deliverables, 85 new tests, LP coverage 32% → 85%.

**Key finding:** 92.4% of input tokens were cache reads (cheap), not fresh context creation. The system architecture (CLAUDE.md as persistent context, continuation sessions preserving state) is working efficiently. The expensive part isn't the work — it's the context reload on each continuation.

## Token Budget — Aggregate

| Category | Tokens | Est. Cost | % of Total Cost |
|---|---|---|---|
| Input (new) | 36,319 | $0.54 | 0.2% |
| Cache creation | 6,723,071 | $126.06 | 44.7% |
| Cache read | 81,675,653 | $153.14 | 54.3% |
| Output | 6,731 | $0.50 | 0.2% |
| **TOTAL** | **88,441,774** | **~$282** | **100%** |

## Cost Breakdown by Channel

| Channel | API Calls | Est. Cost | % |
|---|---|---|---|
| Main conversation (Opus 4) | 511 | $211.26 | 74.9% |
| Subagents — IP scrub (8 agents, mostly Haiku) | 302 | $70.76 | 25.1% |

## Token Allocation by Deliverable

### Tier 1 — Heavy Token Consumers (code generation + testing)

| Deliverable | Agent | Est. Tokens | Est. Cost |
|---|---|---|---|
| 10 Chirp detection rules (`chirp.py`) | Jeremy | ~18M | ~$55 |
| 6 parse helpers (`square_client.py`) | Jeremy | ~12M | ~$38 |
| 6 table DDL (`models.py`) | Jeremy | ~8M | ~$25 |
| 49 Chirp rule tests | Jeremy | ~8M | ~$25 |
| 23 parse helper tests | Jeremy | ~5M | ~$16 |
| Ingestion layer + 13 tests | Jeremy | ~5M | ~$16 |
| **Subtotal — Code Generation** | | **~56M** | **~$175** |

### Tier 2 — Document Generation & Analysis

| Deliverable | Agent | Est. Cost |
|---|---|---|
| CRDM Gap Analysis | Eva | ~$12 |
| Tom T-3 Schema Review + Brief | Tom | ~$15 |
| Jeremy Implementation Brief | Jeremy | ~$9 |
| Attack Plan v1.2 | Eva | ~$6 |
| **Subtotal — Documents** | | **~$42** |

### Tier 3 — IP Scrub (Subagents)

| Deliverable | Est. Cost |
|---|---|
| Vendor name scrub (8 parallel agents) | ~$71 |

## Efficiency Metrics

| Metric | Value |
|---|---|
| Cost per deliverable | ~$11.28 (25 deliverables / $282) |
| Cost per test written | ~$2.05 (85 tests / ~$175) |
| Cost per Chirp rule coded+tested | ~$8.00 |
| Cost per table DDL | ~$4.17 |
| Cache efficiency | 92.4% — excellent, context reuse working |

## Where Tokens Were Wasted

1. **Context Continuations (~30% of cache creation cost).** Each of 6 continuations required re-establishing context (~80K tokens of CLAUDE.md, CRDM, project state). Single largest efficiency loss.
2. **IP Scrub Subagents ($71 for text replacement).** 8 parallel Haiku agents scrubbing vendor names — a simple Python script could do it in seconds for <$0.01. Reserve subagents for judgment-intensive work.
3. **"Keep going" Continuations (P9, P10, P11, P16).** Four phases with "keep going" — each required context re-read.

**Estimated recoverable savings:** ~$120 (43% of day).

## Forward-Looking Budget Framework

Per-sprint token budget (extrapolated from Feb 20 actuals):

| Activity | Est. Cost / 2-Week Sprint |
|---|---|
| Code generation (features) | $180–240 |
| Test writing | $45–60 |
| Document generation | $30–45 |
| Code review + debugging | $15–30 |
| Planning + coordination | $9–15 |
| **Sprint total** | **$280–$390** |

## Recommendations

1. Build `scripts/token_report.py` — automate JSONL parsing, run daily, output markdown for timelog.
2. Add token budget to sprint planning — propose $400/sprint for Sprint 2.
3. Reserve subagents for judgment work — don't use Haiku for text replacement.
4. Minimize continuation sessions — each costs ~$20 in cache re-creation.
5. Track cost-per-deliverable as a KPI — baseline $11.28.

## Related

- [[Brain/projects/GrowDirect|GrowDirect MOC]]
- [[Brain/wiki/growdirect-working-papers|Working Papers Structure]]
- [[Brain/wiki/growdirect-timelog-week-feb16-24|Weekly Roll-Up: Feb 16–24]]

## Sources

- `docs/_archive/ip-vault/timelogs/2026/02-February/daily/2026-02-20_token_analysis.md`
