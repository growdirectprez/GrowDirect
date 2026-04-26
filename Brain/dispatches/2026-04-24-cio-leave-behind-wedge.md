---
type: dispatch
status: ready-to-paste
target: Linear (team GRO)
author: Geoffrey C. Lyle
date: 2026-04-24
source_of_truth: Brain/wiki/cio-leave-behind-wedge.md
related:
  - Brain/wiki/cio-leave-behind-wedge.md
  - plugins/consulting/README.md
  - Personal-CIO-Playbook-v1.docx
  - dispatches/2026-04-24-consulting-skills.md
---

# Dispatch — CIO Leave-Behind Wedge (positioning)

**Why this exists.** The CIO positioning crystallized in a session with
Claude on 2026-04-24. The wedge is: *consulting leaves behind a deck; we
leave behind a plugin, a SaaS instance, and the CIO.* The three-move
frame — certified method (2003) · productized plugin (2026) · proof case
on ourselves (Canary) — becomes the spine of every future positioning
asset, internal and external. The offer is engagement + plugin + SaaS
tenant + embedded CIO, one invoice.

**Canonical source:** [[Brain/wiki/cio-leave-behind-wedge|CIO Leave-Behind Wedge]].
All downstream assets pull from that card. If that card changes, the
downstream assets propagate.

---

## Parent initiative

**Title:** CIO Leave-Behind Wedge — positioning propagation

**Description:**
The canonical positioning card at `Brain/wiki/cio-leave-behind-wedge.md`
is the source of truth for GrowDirect's CIO / Chief AI Officer
positioning. Four downstream assets need to pull from it to stay aligned:

1. Plugin README "why" section (consulting plugin)
2. Personal CIO Playbook v2 — new section "The Wedge"
3. Board-ready pitch packet (Part 3 of the CIO positioning system)
4. LinkedIn long-form — public positioning piece

This initiative covers the four propagation issues. It does not touch
the canonical card itself — that stays stable until a real engagement
or market signal forces revision.

**Labels:** `positioning`, `cio`, `go-to-market`, `canonical-source`
**Milestone:** CIO positioning v2 — ready to pitch
**Target:** Q2 2026

---

## Issue 1 — Plugin README "why" section

**Title:** Update `plugins/consulting/README.md` with positioning "why"

**Labels:** `positioning`, `plugin`, `docs`
**Priority:** Medium
**Estimate:** 1 pt
**Owner (proposed):** Jess (documentation)

**Description:**
Add a "Why this plugin exists" section to the top of
`plugins/consulting/README.md` pulling from
`Brain/wiki/cio-leave-behind-wedge.md`. Section should be 3–4 short
paragraphs covering:

- The three moves (certified / productized / proven)
- The offer: engagement + plugin + SaaS + embedded CIO
- The Big 4 wedge (Zora / ChatPwC / EY.ai / KymChat / AI Refinery are
  selling the concept; this plugin ships the artifact)

**Acceptance:**
- README "why" section renders the three-move frame
- Cross-links to `Brain/wiki/cio-leave-behind-wedge.md`
- Plugin version bumps to 0.1.1 in `plugin.json`
- Diff reviewed against canonical card for drift

---

## Issue 2 — Personal CIO Playbook v2, section "The Wedge"

**Title:** Add "The Wedge" section to Personal CIO Playbook v2

**Labels:** `positioning`, `cio`, `content`
**Priority:** High
**Estimate:** 2 pts
**Owner (proposed):** Geoffrey + Claude (Cowork session)

**Description:**
Build a v2 of Personal-CIO-Playbook (current v1 at
`Personal-CIO-Playbook-v1.docx`) that adds a new section titled "The
Wedge" positioned between the existing identity/credential sections
and the 90-day plan.

"The Wedge" section reproduces the three-move frame from
`cio-leave-behind-wedge.md` in playbook voice:

- Methodology (IBM 2003 certification + Clarks/Morrisons portfolio)
- Productized (consulting plugin — reference the plugin README)
- Proven (GrowDirect / Canary as the operating proof case)

Closes with the offer statement and the Big 4 contrast. Produces
Personal-CIO-Playbook-v2.docx in the workspace folder.

**Acceptance:**
- v2 docx produced with new section in correct position
- "I am offering myself as the leave-behind" appears as a section
  callout / pull-quote
- Big 4 competitor named-product list matches the canonical card
- Companion to v1 (v1 stays available as the pre-wedge version)

---

## Issue 3 — Board-ready pitch packet

**Title:** Build board-ready pitch packet (Part 3 of CIO system)

**Labels:** `positioning`, `cio`, `pitch`, `pptx`
**Priority:** Medium
**Estimate:** 3 pts
**Owner (proposed):** Geoffrey + Claude + `anthropic-skills:pptx`

**Description:**
Build the board-ready pitch packet that was originally scoped as Part 3
of the three-part CIO positioning system (Parts 1 and 2 were Personal
Playbook and Public positioning). Packet is a pptx deck in the IBM BCS
deliverable style the consulting plugin produces — numbered navigator
ribbon, evidence traceability, prize sizing — but applied to the pitch
itself:

- Slide 1–3: the wedge (three moves) rendered as a pitch
- Slide 4–6: the offer (engagement + plugin + SaaS + CIO) with
  deliverables, pricing frame, term
- Slide 7–9: the proof case (GrowDirect / Canary as live-fire demo;
  screenshots from the running tenant)
- Slide 10–12: the Big 4 competitive comparison (side-by-side like the
  Morrisons options section)
- Slide 13: recommendation — for the board audience, the recommendation
  is "retain"
- Slide 14–15: appendix — consulting plugin screenshots, methodology
  wiki links, certification lineage

**Acceptance:**
- pptx packet renders in both PowerPoint and Keynote
- Eats its own dog food: uses the consulting plugin's visual language
- Pulls from `cio-leave-behind-wedge.md` for all positioning text
- Stored in workspace folder as `GrowDirect-CIO-Pitch-Packet-v1.pptx`

---

## Issue 4 — LinkedIn long-form

**Title:** Write LinkedIn long-form: "I'm Productizing What the Big 4 Is Pitching"

**Labels:** `positioning`, `content`, `public`, `linkedin`
**Priority:** Medium (timing-dependent)
**Estimate:** 2 pts
**Owner (proposed):** Geoffrey + Claude + `brand-voice:enforce-voice` + `marketing:draft-content`

**Description:**
Public-facing long-form LinkedIn piece that adapts the canonical
positioning card for the "I might be right" register (the voice Geoffrey
chose for public positioning in an earlier session). Target length:
900–1,400 words. Structure:

- Hook: the Big 4 products by name (Zora / ChatPwC / EY.ai / KymChat /
  AI Refinery) and what they're all selling
- Pivot: what they can't ship yet
- The three moves in first person (certified 2003 · productized 2026 ·
  proven on ourselves)
- The leave-behind reframe, with "I am offering myself as the
  leave-behind" as the anchor quote
- Close: an invitation, not a pitch — what a real engagement starts
  from (single call, plugin demo on real data, proposal within a week)

**Acceptance:**
- Draft passes `brand-voice:enforce-voice` check against GrowDirect's
  voice guidelines if they exist; else uses Geoffrey's Brain voice
  ("I might be right" register)
- Does not paraphrase the canonical card — extends it for public
  register
- Cross-posted to Brain at
  `Brain/wiki/public/2026-linkedin-big4-wedge.md` with frontmatter for
  eventual republication
- Timing: hold for publication until the consulting plugin has at
  least one external demo-ready run

**Dependencies:**
- Depends on Issue 1 (plugin README) being complete so the LinkedIn
  piece can link to a stable README
- Depends on Issue 3 only if the LinkedIn piece references board
  materials (optional)

---

## Notes for the Linear-user (Geoffrey)

1. Paste the parent initiative first.
2. Issues 1 and 2 are independent and can run in parallel.
3. Issue 3 (pitch packet) depends on Issue 2 (playbook v2) for voice
   consistency.
4. Issue 4 (LinkedIn) is timing-dependent — it is a spearhead that
   should fire once the wedge is fully armed (plugin README live,
   Canary tenant demo-ready). Do not publish prematurely.
5. When Linear MCP reconnects, I can post directly as
   `mcp__a018de2b-*__save_issue` calls. For now this is
   dispatch-ready copy.

---

## Canonical source — single edit point

If market feedback or a real engagement changes the positioning, the
only edit that matters is to
[[Brain/wiki/cio-leave-behind-wedge|cio-leave-behind-wedge.md]]. After
editing, re-run propagation through the four issues above (or whichever
assets have been built by then) with a structural diff against the
updated card. This dispatch stays as the record of the propagation
protocol.
