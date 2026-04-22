---
type: wiki
tags: [foundation, cove, governance, time-logging, cicd, compensation, advisory-synthesis]
created: 2026-04-19
sources: [Brain/raw/processed/advisor-memos/2026-04-19-comprehensive-review.md]
status: draft
last-compiled: 2026-04-19
needs-review: 2026-05-03
---

# Foundation Time Logging Policy

The Foundation's time-allocation evidence is **system-generated from the CICD pipeline and email logs**. It is not reconstructed from memory or manual notes. This card defines the allocation methodology, the board review flow, and the record-retention rules.

Distilled working position from a 2026-04-19 advisor memo. Must be formally adopted by the Foundation board (with the founder recused) before any compensation is paid.

## Source of Truth

All time evidence comes from system-generated logs:

- **Git commit history** across GrowDirect/, Canary/, Cove/, Brain/, ownpalosverdes/, and any other tracked repo — timestamps + diffs + file paths
- **Linear issue activity** — GRO-* issue creation, state transitions, completions
- **Brain wiki article creation and edit timestamps** (Obsidian vault metadata)
- **Email pipeline logs** — message send/receive timestamps tied to Foundation-relevant threads (to be defined: which inboxes count; which senders/recipients flag Foundation hat)
- **Calendar logs** (if applicable) — meeting timestamps for Foundation calls

These are contemporaneous by construction — the log is created at the moment of action, not after the fact.

## Why This Beats Manual Notes

- Objective and verifiable — git hashes, Linear API audit log, file timestamps are tamper-resistant
- Granular — file-path-level precision ties each hour to a specific hat
- Auditable — exportable raw logs can be produced on request (IRS, AG, or member inspection)
- Eliminates "I worked 8 hours on X" self-reporting risk

## Allocation Methodology (File-Path Rules)

Each logged activity maps to exactly one hat based on which files were touched. The authoritative rules are in [[foundation-three-hat-compensation]]. Summary:

**Foundation hat:**
- `Brain/wiki/cove-*.md` research articles
- `Brain/wiki/foundation-*.md` legal-framework cards
- `Brain/wiki/wpbca-*.md` compliance-framework cards (when authored as neutral research, not operational direction)
- `Cove/docs/advisor-memos/*.md` (archival)
- `Cove/docs/2026-04-18-abalone-cove-foundation-design.md` and Foundation design specs
- `abalonecove.org` and `cove.org` editorial site content
- Grant writing, 1023-EZ narrative, bylaws drafting, position letters

**LLC (commercial R&D) hat:**
- `Canary/**`
- `Cove/cove/**` application code (the governance-engine product)
- `Cove/cove/angel/**`, `Angel/**`
- `services/**`, `devops/**`, `content-engine/**`
- `.claude/skills/**` (shared platform skills, not Foundation-specific)
- `Seacove/**`
- `~/ownpalosverdes/**`
- `docs/sdds/**`, `docs/superpowers/specs/**` (when the spec is for a commercial product)

**Community of Abalone Cove (formerly WPBCA) — volunteer, unpaid hat:**
- Member outreach, director recruitment, board-meeting prep
- CC&R enforcement activities
- Any work whose file path doesn't land in Foundation or LLC but directly serves Community of Abalone Cove operations

**Mixed-session splits** — when a session touches files belonging to multiple hats, allocation is proportional by lines-changed across touched files. The skill that computes this is [[foundation-umbrella-alx|ALX]] (or its successor); see the time-logging skill extension todo.

## Monthly Summary Flow

End of each month, a summary is generated from the raw logs (not raw code, not sensitive emails — aggregated categories):

```
Foundation hat — April 2026
  Research & Library of Evidence:     38.5 hours
    Key outputs: cove-declaration-100, cove-pvplc-partnership, cove-lrpmp
  Foundation formation:                22.0 hours
    Key outputs: Consolidated Design Spec v2, advisor memo review
  Editorial site (abalonecove.org):    14.5 hours
    Key outputs: timeline page, bibliography
  Total:                               75.0 hours
```

Raw logs remain available on request; the summary is what the board reviews.

## Board Review Flow

1. **Monthly (or per-cycle)**: Generate summary from logs
2. **Quarterly**: Present summary + raw log export availability to disinterested directors
3. **Board review**: Directors confirm the allocation rules were applied correctly; they do not audit individual commits unless something looks off
4. **Compensation approval**: Separate resolution approves the compensation based on the reviewed hours + comparable-compensation data (see [[foundation-three-hat-compensation]])
5. **Minutes language**: "The Board reviewed system-generated CICD and email logs and the founder's summary of services performed exclusively for the Foundation's charitable purposes and approved compensation of $X at the rate of $Y per hour as reasonable."
6. **Founder recuses** from every vote on their own compensation
7. **Annual re-approval** with updated logs and updated comparables

## What Raw Logs Look Like (Concrete Evidence)

Recent Foundation-tagged activity (2026-04-16 through 2026-04-19 window, from git):

- `spec: Abalone Cove Foundation design` (2026-04-19)
- `cove: Abalone Cove Foundation design spec + session wiki articles` (2026-04-19)
- `spec: rename WPBCA → Community of Abalone Cove; flesh out CHOA role` (2026-04-19)
- 10+ Foundation-relevant Brain wiki cards created in one burst (2026-04-19)
- `spec: Parcel 106 story, land bank economics, Vanderlip loophole` (2026-04-16)
- `spec: abalonecove.org — editorial site design` (2026-04-16)

Cross-referenced with Linear: GRO-330/331/332 (Cove setup), GRO-370 (MCP knowledge service). These git + Linear timestamps + file paths are the evidence.

## Record Retention

- Raw logs (git, Linear, Brain metadata, email indexes): retained for the IRS statute of limitations period (3–6 years) plus any active litigation hold
- Summaries and board minutes: retained per Foundation bylaws (typically 7 years or permanent)
- Export formats for potential regulator review: JSON/CSV for programmatic logs, PDF for summaries

## Q1 2026 Founding-Period Backfill

Work performed before the Foundation was legally formed (Q1 2026) is "pre-formation organizational work." The logs already exist — they are the git history since February 2026. At the first organizational board meeting, the founder presents:

1. A summary generated from the existing logs
2. The allocation methodology (this card)
3. The supporting comparable-compensation data

Disinterested directors review, determine the Foundation-specific portion, and ratify compensation for that portion only. See the founding-period section of [[foundation-three-hat-compensation]].

No manual reconstruction is required — the commit history is the record.

## Open Decisions

- Which email inbox(es) count as Foundation-relevant for the log pipeline
- Format of the monthly summary (JSON, Markdown, PDF)
- Tool for generating summaries automatically from git + Linear + Brain metadata — likely the extended project-timelog skill; see the time-logging todo
- Whether to publish high-level time summaries on cove.org for transparency

## Related

- [[foundation-three-hat-compensation]] — Allocation rules (which hat for which path)
- [[foundation-legal-framework]] — MOC
- [[foundation-bylaws]] — Adopted with the bylaws at first board meeting
- [[foundation-umbrella-alx]] — The orchestration layer that may eventually own the time-logging pipeline
