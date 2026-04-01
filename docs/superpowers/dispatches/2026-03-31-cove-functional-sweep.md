# Dispatch: Cove Functional Sweep

**Date:** 2026-03-31
**Priority:** High
**App:** Cove
**Spec:** `docs/superpowers/specs/2026-03-31-cove-functional-sweep-design.md`

---

## Paste this into a Cove Claude Code session

```
You are the Cove builder. Read ~/GrowDirect/CLAUDE.md then ~/GrowDirect/Cove/CLAUDE.md.

You have a 6-item sequential sweep to make Cove functional end-to-end. The full design spec is at:
~/GrowDirect/docs/superpowers/specs/2026-03-31-cove-functional-sweep-design.md

Read that spec NOW before doing anything else. It has the complete manifest, constraints, and test strategy for every item.

## Sequence (strict order — each depends on the previous)

1. GRO-387 — Seed realistic activity data (critical path — unlocks everything)
2. GRO-382 — Accessibility base layer (skip-nav, ARIA, focus-visible)
3. GRO-363 — Brand system (kill cream/ink/gold, cove-blue everywhere)
4. GRO-380 — Mobile responsive sidebar (Alpine.js toggle, slide-over)
5. GRO-384 — Empty states (contextual per blueprint, role-gated CTAs)
6. GRO-385 — Login UX + kill landing page (redirect / to /auth/login)

## Rules

- Run the full factory pipeline for EACH item: preflight → research → blueprint → TDD → assembly → verify → QA → ship → close
- One GRO at a time. Finish and ship before starting the next.
- Read the spec item before starting each GRO — it has exact details.
- seed.py is a protected file. Verify changes carefully.
- Ballot table has NO member_id. EVER. Envelopes link them.
- PostCSS build must succeed after CSS changes: npm run build
- All tests pass before moving to next item.

## Key constraints from spec

- Seed data must be idempotent (check before inserting)
- Accessibility goes into base.html before brand/responsive touch templates
- Brand sweep: ~69 HTML files, ~734 occurrences — mechanical but large. Grep-verify zero remaining cream-/ink-/bluff-/gold-/shore- after.
- Mobile sidebar: Alpine.js already loaded, no new deps. Close on Escape + nav click.
- Empty states: CTA buttons only for users with correct role (board for proposals/elections/meetings)
- Login: 302 redirect (not 301). Privacy and terms must remain accessible without auth.

## Start

Begin with GRO-387 (seed data). Run preflight. Go.
```
