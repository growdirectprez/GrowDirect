---
name: session-synthesis
description: |
  Synthesize AI chat transcripts into structured session documents. Use whenever
  Jeffe shares a Grok link, AI chat URL, or raw brainstorm transcript that needs
  to be processed into the team's standard session format. Triggers on any
  grok.com URL, AI chat transcript, "synthesize this session", "brainstorm",
  "parse this chat".
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Session Synthesis — BrainStorm

## What This Skill Does

Jeffe regularly brainstorms with Grok and other AI tools, producing raw transcripts
full of strategic decisions, technical directions, action items, and quotable moments.
This skill transforms those raw transcripts into structured session documents the
team relies on for coordination.

## Workflow

### Step 1: Get the Source Content

Input is typically a Grok share link or raw text.

**Primary method — Chrome browser tools (preferred):**
1. Check Chrome is connected via `tabs_context_mcp`
2. Navigate to URL, wait for load
3. Use `get_page_text` to extract conversation

**Fallback — WebFetch** (only if Chrome unavailable):
```
WebFetch(url=<url>, prompt="Extract the complete conversation transcript.")
```

**Last resort:** Ask the user to paste the transcript directly.

### Step 2: Read Project Context

Load current project state for accurate team routing:
1. Read `CLAUDE.md` — current status, team table
2. Read strategy docs — to understand scope boundaries

### Step 3: Extract and Organize

Parse the transcript and identify:

- **Strategic Threads** — major topics discussed, each becomes a numbered section
- **Verbatim Quotes** — exact words on strategy, vision, direction
- **Technical Details** — API endpoints, architecture decisions, configs
- **Action Items** — concrete tasks with owners
- **Design Decisions** — confirmed architectural or strategic choices
- **Scope Implications** — does anything expand or conflict with current scope?

### Step 4: Write the Synthesis Document

Create at: `~/GrowDirect/IP/Sessions/<descriptive_name>_<YYYY-MM-DD>.md`

#### Document Structure

```markdown
# [Descriptive Title]
**Date:** [Date]
**Version:** 1.0
**Logged by:** [Agent name]
**Source:** [Description + URL if available]
**Classification:** Internal / Strategic
**Status:** Synthesized — routed to team

---

## Executive Summary
[2-4 sentences: what was covered, why it matters]

---

## Verbatim Strategic Quotes
> *"Quote 1"*
> *"Quote 2"*

---

## Thread 1 — [Thread Title]
**Route to: [Team member names]**

### Context
[What was discussed and why]

### Technical Details
[Specific technical content]

### Key Decisions
[What was decided or confirmed]

### Action Items
- [ ] **Name** — Task description

---

## Priority Stack

| Priority | Thread | Who | What |
|---|---|---|---|
| P1 | [Thread name] | [Names] | [One-line summary] |
| P2 | [Thread name] | [Names] | [One-line summary] |

---

## Key Design Decisions Confirmed
1. **[Decision]** — [Brief explanation]

---

## Scope Implications
[Does this change MVP boundary? If no: "No scope changes identified."]

---

## Where to Pick Up
- **[Name]**: [Specific next step]

---
*GrowDirect | Confidential*
*Synthesized: [Date] | [Logged by]*
```

### Step 5: Confirm with User

Present the synthesis and ask if they want it appended to CLAUDE.md as a session log entry.

## Quality Checks

1. Every thread has at least one action item with a named owner
2. Quotes are verbatim — don't paraphrase
3. Technical details are specific enough to act on
4. No virtual team member names leak into external-facing outputs
