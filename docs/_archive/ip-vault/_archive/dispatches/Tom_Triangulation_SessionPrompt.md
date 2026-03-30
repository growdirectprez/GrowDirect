---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Session Prompt: Tom — Triangulation Blueprint Retail Validator

**Date:** February 25, 2026
**Dispatched by:** ALX
**Work Order:** `_ALX/WorkOrders/WORKORDER_Triangulation_VibeFrontend.md`

---

## Context

Jeffe has directed a parallel track: produce a Generic Frontend Blueprint that an open-source vibe coding tool (Bolt.diy) can use to generate a working prototype of the Canary merchant app. Condor is the lead author (sanitization). Your role is **retail process validation**.

## Your Mission

1. **Read the work order** at `_ALX/WorkOrders/WORKORDER_Triangulation_VibeFrontend.md`.

2. **Wait for Condor's first draft** (expected Wed Feb 26 EOD) at `_ALX/WorkOrders/output/Triangulation/Canary_Generic_Frontend_Blueprint_v1.0.md`.

3. **Review the full blueprint against your principles:**
   - Does the navigation flow map to real retail operations? (Process first, technology second.)
   - Do the wizard steps match what a merchant actually does? (Prototype with the small retailer — coffee shop owner, 200 SKUs, one Square terminal, no IT department.)
   - Are the data shapes in Section 5 complete and correct? If the frontend asks for data, does the shape make sense for what a POS system would produce?
   - Is the seed data in Section 7 realistic for a specialty coffee chain?
   - Does the API contract describe everything the frontend needs, and nothing it doesn't?

4. **Provide corrections** directly as comments or a review document. Condor incorporates them Thursday PM.

5. **Jointly evaluate Bolt.diy vs. Dyad** with PhD. You assess from a "does this work for a small retailer" angle. PhD assesses from an IP safety angle. Produce a 1-paragraph recommendation for inclusion in the blueprint.

## Key Questions to Answer

- Can a coffee shop owner with no technical background navigate the screens described in this blueprint?
- Are there any retail processes missing from the wizard flows?
- Do the error states cover what actually goes wrong in a store?
- Is the seed data realistic enough that a merchant would recognize it as "their kind of business"?

## Key Files

- Work order: `_ALX/WorkOrders/WORKORDER_Triangulation_VibeFrontend.md`
- Condor's draft: `_ALX/WorkOrders/output/Triangulation/Canary_Generic_Frontend_Blueprint_v1.0.md` (available Wed EOD)
- Your review output: `_ALX/WorkOrders/output/Triangulation/Tom_Review_Notes.md`

## Standing Instructions

- Log references to Reference Library
- File timelog on session close
- Use brand template for any .docx output

---

*Dispatched by ALX — February 25, 2026*
