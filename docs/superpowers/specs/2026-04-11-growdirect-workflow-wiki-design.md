---
classification: confidential
owner: GrowDirect LLC
---

# Design Spec: GrowDirect Workflow Wiki Article

**Date:** 2026-04-11
**Type:** Brain wiki article
**Output:** `Brain/wiki/growdirect-workflow.md`

## Problem

Sessions keep violating workflow rules because the operating model is scattered
across CLAUDE.md (session discipline), feedback memories (Claude Code only),
and tribal knowledge. Cowork sessions can't read feedback memories at all.
A recent session dropped a sprint plan in the repo root AND Brain inbox with
no defined reason for either location.

Brain is the only knowledge layer both agent systems can read. A wiki article
documenting the operating model makes the workflow visible to every session.

## Design — Seven Sections

### 1. What This Is (2-3 sentences)
Solo founder (Lyle) running four projects with two AI agent systems.
This article is the operating manual for how sessions work.

### 2. The Two Agent Systems
- **Claude Code** (terminal): Builds. Has `.claude/skills/` factory pipeline
  (blueprint, TDD, assembly, QA, ship). MCP access to Memory Bus + Cove
  Knowledge. No access to Linear, Gmail, Canva, Figma.
- **Cowork** (desktop): Strategizes. Has Superpowers plugin skills (brainstorming,
  presentations, spreadsheets, legal, marketing, engineering). MCP access to
  Linear, Gmail, Canva, Figma. No access to Memory Bus or Cove Knowledge.
- Key point: they don't share memory. Brain bridges them.

### 3. Knowledge Layers
The five layers table from CLAUDE.md, rewritten as knowledge (not instructions).
Which agent sees what. Why Brain is the bridge. Reference document-management
wiki for file locations.

### 4. Working Style
Distilled from feedback memories and session discipline:
- Build, don't organize. Ship something that runs.
- One deliverable per session. Scope to something committable.
- Iterate with what you have. Don't ask for better inputs.
- Verify before claiming broken. Read current state, not old reports.
- Flag dependency changes. Don't silently add packages.
- No scaffolding without a Linear issue.

### 5. Session Lifecycle
Three phases:
- **Startup:** Read project MOC. Check registry. Know what Brain already has.
- **Work:** One deliverable. Commit or revert. Route knowledge through Brain.
- **Shutdown:** Ingest knowledge, delete artifacts, rebuild registry if wiki changed.

### 6. Anti-Patterns
Specific mistakes that have burned tokens:
- Dropping files in repo root
- Hand-placing files in Brain/raw/inbox/ instead of using content engine
- Duplicating content between locations
- Creating scaffolding without a Linear issue
- Organizing instead of shipping
- Repeating stale error numbers without re-verifying

### 7. Cross-Session Handoffs
How work moves between Claude Code and Cowork:
- Brain playbooks for repeatable workflows
- What a handoff needs: what, how, where, done-looks-like
- Linear is the task system; Brain is the knowledge system; don't conflate them

## Relationships

- **Companion to:** `Brain/wiki/document-management.md` (where things go)
- **This article:** How we actually work
- **Links from:** Brain/Home.md (Platform Governance section), project MOCs
- **Sources:** CLAUDE.md, feedback memories, document-management wiki
