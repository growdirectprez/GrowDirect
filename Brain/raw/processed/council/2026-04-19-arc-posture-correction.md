# ARC Posture — Correction

**Author:** Condor
**Date:** 2026-04-19
**Status:** Supersedes the overreach in the prior ARC Protocol Sketch.
**Extracted to:** `Brain/wiki/cove-arc-posture.md`

---

Earlier today I drafted an "ARC Protocol" with a publisher-side Manifest and
an applicant-side Twin. That sketch was too grand. Jeffe corrected it. This
memo captures the corrected posture.

## The correction

The city handles permitting. Rancho Palos Verdes Planning Department is the
legal permitting authority. They set the standard. They run the process.
They approve or deny. That is not the ARC's job and should never become the
ARC's job.

The HOA ARC at WPBCA is not a review body in any meaningful sense. It does
not publish design standards. It does not evaluate submissions. It does not
gate-keep.

The ARC's role is smaller and quieter:

1. Help members who want to remodel follow the city's process correctly —
   so they don't freelance, skip steps, or end up with stop-work orders.
2. Track what's happening in the neighborhood — who's filing, what's in
   flight, what the scope is.
3. Answer neighbors factually when they ask — "yes, permitted; yes,
   proceeding through RPV; here's the schedule; here's the scope."

That's it. Concierge plus transparency layer. Not reviewer.

## Why this is the right shape

Abalone Cove is 65+ years old. The original owners are turning over. New
owners arrive with more money and bigger plans. Teardowns, additions, view
disputes, construction-impact complaints — the pressure curve is rising.

In that environment, an ARC that tries to impose design judgment becomes the
target of every dispute. An ARC that quietly documents "this is happening,
it's permitted, here's the record" dissolves most friction without any
authority. The neighbors' question is rarely "is the design good?" — it's
"is this legitimate and how long will the disruption last?"

The restraint is the feature. Not much has happened through the ARC
historically. That is the point. Keep it that way, but make it useful during
turnover.

## What this means for the tool and the demo

Nothing about the plugin or pipeline changes mechanically. What changes is
the *framing* of what comes out of it.

- Not "validate against ARC Manifest." Instead "validate against RPV's
  published checklist," which is what the city actually cares about.
- Not "Readiness Report for ARC approval." Instead "Readiness Report for
  the member's own confidence that their city filing is complete."
- Not "ARC publishes the standard." Instead "ARC helps the member reach
  the city's standard, then documents what's happening so the community can
  see it."
- The permit twin stays useful — but its job is documentation for
  transparency, not compliance against a local manifest.

## Revised demo posture

Jeffe is WPBCA ARC chairman. The demo is not "I built a tool that publishes
our review standard." The demo is:

> I helped myself walk through the city's remodel process properly. I
> documented what I have, what I'm filing, and where I am in the city's
> process. If any of you want the same help on your own remodel, here's the
> playbook. When your neighbors ask what's going on, I can tell them — not
> because I approved anything, but because we kept a real record.

Same pipeline. Same artifacts. Different message. Smaller, calmer, harder
to argue with.

## What to retire

- The "ARC Manifest" concept as applied to WPBCA. (The concept may still
  be valid for cities that *do* set standards — e.g., Palos Verdes Estates
  ARC is a different animal — but it is not the WPBCA move.)
- Any framing that positions the ARC as an adversary to coerce or route
  around. The ARC at WPBCA is not the problem. Rising turnover pressure is.
  The tool is here to make the turnover quieter, not to reform the body.

## What to keep

- The permit twin — still useful as the durable record of a house across
  permit cycles.
- The pipeline — still the mechanism that turns messy owner assets into a
  clean city submittal.
- The skill pack — still the distribution format for "help a member walk
  through RPV's process."
- The Seacove-as-case-study approach — still the right way to demonstrate
  without preaching.

## The one-line posture

> The city approves remodels. The ARC helps members get through the city's
> process cleanly and keeps the community factually informed. That is enough.
