---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Session Prompt: Condor — Triangulation Blueprint Lead Author

**Date:** February 25, 2026
**Dispatched by:** ALX
**Work Order:** `_ALX/WorkOrders/WORKORDER_Triangulation_VibeFrontend.md`

---

## Context

Jeffe has directed a parallel track to Sprint 5: produce a Generic Frontend Blueprint that can be fed into an open-source vibe coding platform (Bolt.diy) to rapidly generate a working prototype of the Canary merchant app. You are the lead author.

This is a triangulation effort. Four agents contribute: you (sanitization + assembly), Tom (retail process validation), PhD (IP boundary + research depth), and Art (visual specification). You produce the single Markdown deliverable.

## Your Mission

1. **Read all 8 input documents** listed in the work order (Art wireframe, Art self-critique, Jim 2C brief, Jim wizard mapping, Jess Functional Guide, Jess Technical Guide, PhD Alignment Brief, Brand Guide).

2. **Produce the Generic Frontend Blueprint v1.0** following the exact structure in the work order (Sections 1-7). This is a sanitized, buildable specification that an AI tool can read and generate a working React prototype from.

3. **Apply your sanitization rules strictly:**
   - No CRDM details (table names, columns, triggers, hash chains)
   - No detection algorithm internals (rule names, thresholds)
   - No company names (GrowDirect, Canary → "the platform")
   - No team member names
   - No Lightning/Dome architecture
   - No PhD thesis content
   - Descriptive placeholders, not [REDACTED] tags

4. **Functional completeness is your quality bar.** After sanitization, the blueprint must still be buildable. If Bolt.diy can't generate a working prototype from your output, you've over-redacted. Test yourself: "Could someone with no Canary knowledge build this?"

5. **Produce a diff report** showing what was redacted from each source document.

## Key Files

- Work order: `_ALX/WorkOrders/WORKORDER_Triangulation_VibeFrontend.md`
- Output location: `_ALX/WorkOrders/output/Triangulation/Canary_Generic_Frontend_Blueprint_v1.0.md`
- Diff report: `_ALX/WorkOrders/output/Triangulation/Condor_Sanitization_Diff_v1.0.md`

## Dependencies

- Art reviews Sections 2 + 3.1 for visual fidelity (Wed)
- Tom reviews full blueprint for retail accuracy + API shapes (Thu AM)
- PhD reviews full blueprint for IP safety (Thu AM)
- You incorporate their feedback and produce final version (Thu PM)

## Standing Instructions

- Log references to Reference Library
- File timelog on session close
- Use brand template for any .docx output (this deliverable is Markdown)

---

*Dispatched by ALX — February 25, 2026*
