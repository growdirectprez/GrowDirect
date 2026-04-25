---
type: dispatch
status: pickup-saturday-am
date: 2026-04-25
target: claude-code-session (Saturday morning resume)
priority: high
deadline: deliverables to Tim by Sunday evening
tags: [monday-call, bart, tim, prep, sparring-partner]
---

# Dispatch — Monday 1pm PST Call Prep (Saturday AM Pickup)

Friday session ended after birthing ALX (Alejandro Castillo) and
landing the Welcome Journey package in CATz. Resume Saturday
morning to produce the three Monday-call prep docs.

## The call

**When.** Monday 2026-04-27, 1pm PST.

**Cast.**

- **Geoff (founder)** — pitching.
- **Tim** — close friend, ex-IBM Fresh & Easy Commercial Business
  Lead, call organizer, GTM-partner-aligned. Offgrid 4pm Friday
  through Monday morning. Materials must be in his inbox by Sunday
  evening so he reads them Monday morning before the call.
- **Bart** — third person, unmet by Geoff. Ex-Accenture / IBM /
  Gartner / Starbucks. Manager-not-doer / big-thinker type. NCR +
  RAPID contract exposure from the Arthur-Andersen / PW-MH era.
  Framework-fluent, pattern-matches fast, will probe gaps.

## The framing (Tim's words, taken seriously)

> "My goal is to convince Bart we've got something. Use him as the
> opportunity to build it out and harden the approach/solution. In
> the process, we identify other targets to land client #2
> (scaled) and get this rolling."

This means Monday is **not** a closing call. It's a sparring-
partner-recruitment call. Goal: land Bart as the first serious
external scrutiny that hardens the offering for client #2. Bart's
pedigree makes him receptive to that framing if presented honestly;
he'd reject a sales pitch from a stranger.

Pitch-register implication: soft, not aggressive. Concrete claims +
acknowledged gaps + invitation to push back. The 25-year arc story
(PwC/Monday → IBM BCS → today's CATz productization) is the
opener; the live Canary-on-Solex demo is the proof; the welcome-
journey prompt is the leave-behind for asynchronous round-2.

## What's already in the can (today's session)

All four repos in committed state. Resume by reading these files
first to refresh context:

- `~/CATz/` (5 commits, 32 markdown files including the welcome-
  journey package and ALX bio)
- `~/Canary-Retail-Brain/` (4 commits, including Stream 4 Solex
  worked-example anchoring)
- `~/GrowDirect/Canary/` (cleanup + security + sibling cross-refs;
  latest commit `aa3ed23`)
- `~/GrowDirect/` main (4 dispatches committed; latest `25dd02a`)

The Welcome Journey package (`CATz/welcome-journey/`) has the
onboarding prompt + dispatch template + synthesis template ready
to deploy. ALX exists as a named persona at `CATz/bios/alx.md` and
`CATz/method/roles/alx.md`.

## Three docs to write Saturday morning

Time estimate: ~2 hours total. Produce in order; commit each to
the GrowDirect repo.

### 1. `Brain/raw/inbox/tim-prebrief-2026-04-27.md` (internal)

Tim's pre-call reading. ~15-min read for him Monday morning.
Friendly register; assumes Tim's prior context.

Sections:
- One paragraph: what's been built since Tim last saw progress
- 25-year arc compressed (IBM BCS lineage Tim will recognize)
- Three-move CIO leave-behind wedge as pitch frame
- Suggested 45-min call shape (open / arc / demo / Bart reaction /
  leave-behind)
- Bart-likely-objections + Geoff's honest answers
- Suggested intro language Tim can use verbatim or improvise

### 2. `CATz/welcome-journey/companion-onepager.md` (external)

Bart-facing 1-pager. Externally clean. Reusable across future
partners — first artifact of a partner-pre-read library.

Sections:
- GrowDirect at a glance (4 sentences)
- Three-move wedge (one paragraph each: certified / productized /
  proven)
- Three links to CATz Home, Canary-Retail-Brain `platform/overview`,
  CATz `proof-cases/canary-self-diagnostic`
- One-sentence acknowledgment line referencing NOTICE.md

### 3. `Brain/raw/inbox/monday-call-script.md` (internal — Geoff's eyes only)

Geoff's call script + objection bank.

Sections:
- 45-min flow with timing
- Live demo checklist (Solex emitting → Canary observing → Chirp/
  Fox detecting). What to show; what to skip.
- Bart-specific objection bank pattern-matched to his Accenture /
  IBM / Gartner / Starbucks / NCR-RAPID background
- Lines that must land (especially the IBM BCS / IBM GS integration-
  failure diagnosis as the architectural rationale for CATz)
- Lines to avoid (no hype; no overclaiming; no reading from deck)

## Two gates before writing — answer these Saturday morning

These determine pitch register and whether the 1-pager has live URLs.

### Gate 1 — Call goal

- **A.** "Land Bart as sparring partner; harden the offering through
  his scrutiny; surface client #2 from there." Soft register,
  invite-pushback frame. (Recommended — matches Tim's words.)
- **B.** "Convince Bart to commit as paying client #1." Sharper
  register, closer-energy.

### Gate 2 — GitHub URLs in the 1-pager

- **A.** Attach URLs as they'll exist after Phase 7 (`github.com/
  growdirect-llc/...`). Requires user to stand up the
  `growdirect-llc` org and push the three repos before Sunday
  evening. Live links Bart can click. (Recommended.)
- **B.** Skip URLs; Bart sees content live during the call only.
  Simpler if `growdirect-llc` org doesn't get stood up; loses the
  "leave-behind he can read at his pace" property.

If gate 2 = A, also produce: Phase 7 push sequence (CATz + CRB +
Canary all to `growdirect-llc`, rename + transfer Canary to
`canary-retail`). Time estimate: 30 min once the org exists.

## Saturday morning resume checklist

Read these files first to recover state:

- This dispatch (you're reading it)
- `dispatches/2026-04-24-cto-readiness-ship-handoff.md` (the 8
  decisions captured Friday)
- `CATz/welcome-journey/onboarding-prompt.md` (the IP-laden artifact
  the Monday demo proves out)
- `CATz/proof-cases/canary-self-diagnostic.md` (the substantive
  pitch the call hits)

Then answer the two gates and produce the three docs.

## Sunday-evening checkpoint

By Sunday evening, the following must be true:

- [ ] Three docs written and reviewed by Geoff
- [ ] Tim has the prebrief + 1-pager in his inbox (so it's there
      Monday morning when he gets back from the mountains)
- [ ] If gate 2 = A: `growdirect-llc` org exists, three repos pushed,
      Canary renamed + transferred to `canary-retail`
- [ ] Demo path tested locally (Canary running, Solex emitting,
      Chirp/Fox detecting)

## Deferred — handle Monday afternoon (post-call)

- Send Bart the welcome-journey prompt as the leave-behind artifact
- Ingest synthesis into memory bus when Bart returns it
- Update `Brain/projects/<bart-slug>.md` with the engagement chain

## Related

- `dispatches/2026-04-24-cto-readiness-ship-handoff.md` — broader
  ship sequence and the 8 captured decisions
- `dispatches/dispatch-platform-brand-consolidation-2026-04.md` —
  the platform reframe + four-layer threat posture + Stream 4 Solex
  anchoring
- `dispatches/2026-04-24-cio-leave-behind-wedge.md` — the CIO
  positioning wedge that Monday's call demonstrates
- `CATz/bios/alx.md` — ALX persona, the named entity that operates
  the welcome journey
- `CATz/welcome-journey/onboarding-prompt.md` — the prompt itself
