---
name: canary-review
description: |
  Code review for Canary. Use after completing tasks, implementing features,
  or before merging. Reviews against Factory Process compliance, data integrity,
  and infrastructure standards. Replaces superpowers:requesting-code-review.
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
---

# Canary Review — Code Review

## Overview

Dispatch a review subagent or self-review to catch issues before they compound.

**Core principle:** Review early, review often.

**Announce at start:** "I'm using canary-review to review this work."

## When to Request Review

**Mandatory:** After each task in subagent execution, after completing a feature, before merge.
**Optional:** When stuck, before refactoring, after fixing complex bugs.

## Review Checklist

### Factory Process Compliance
- Was there a Blueprint (plan)?
- Were Parts manufactured test-first?
- Does the commit history show RED -> GREEN -> REFACTOR?
- Is there a GRO issue referenced in commits?

### Data Integrity
- Does this touch canary_sales schema? INSERT-only preserved? Hash chain intact?
- Does this touch detection rules? False positive / false negative risk?

### Infrastructure Integrity
- New dependencies: open license, production-grade, no rebuild risk?
- New environment variables added to `.env.example`?
- New Docker services or port bindings?

### Pipeline Compliance
- Merchant-first isolation maintained?
- Data that should flow to gLog actually flows there?
- UUID used as primary identifier (not Square's external_id)?
- TSP pipeline: data flows end-to-end?

### Code Quality
- SQLAlchemy 2.0 `Mapped[]` syntax?
- Imports verified against actual codebase?
- No `_v2`, `_new`, or `_backup` file variants?
- `python3` used, not `python`?

### Test Quality
- Every new function has a test?
- Mocks only for external services?
- Pytest markers assigned per `pytest.ini`?
- Smoke tests still green?

## Red Flags in Code

| Pattern | Problem |
|---------|---------|
| `UPDATE`/`DELETE` on canary_sales | Violates immutability |
| `from canary.models import Base` | Legacy pattern |
| Hard-coded Square merchant ID | Should use UUID |
| `import sqlite3` | SQLite banned |
| File named `*_v2.py` | Edit the original |

---

*Canary Review v1.0 — Code Review*
*Replaces: superpowers:requesting-code-review*
