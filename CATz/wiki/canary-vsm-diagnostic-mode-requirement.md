---
date: 2026-04-24
type: skill-requirement
status: pending-skill-update
owner: GrowDirect LLC
tags: [vsm, canary-vsm, diagnostic-mode, clarks-frame, requirement, ibm-bcs]
sources:
  - docs/sdds/consulting/SDD-clarks-retail-diagnostic-v2.md
  - Canary-Retail-Brain/case-studies/canary-retail-diagnostic-archetype.md
  - Brain/wiki/methodology-ibm-retail-diagnostic.md
target-skill: .claude/skills/canary-vsm.md
last-compiled: 2026-04-24
needs-review: 2026-05-08
---

# Canary VSM — Diagnostic Mode Requirement

> Pending requirement to be folded into `.claude/skills/canary-vsm.md`.
> Documented here because `.claude/skills/` was a protected path in the
> session that surfaced this requirement. Sibling to
> [[canary-vsm-cutover-awareness-requirement|VSM cutover-awareness requirement]].

## The requirement

The Virtual Store Manager (VSM) needs a **diagnostic mode** that produces
on-the-fly merchant performance answers in the seven-section Clarks frame
codified at `docs/sdds/consulting/SDD-clarks-retail-diagnostic-v2.md`.

This is not a separate skill or a separate output format. It is the VSM's
default response shape when the merchant asks an open-ended performance
question. Triggers include:

- *"How are we doing?"*
- *"What are the biggest opportunities?"*
- *"What should I do first?"*
- *"What's the prize this quarter?"*
- *"Where are we losing money?"*
- Any question where the merchant is asking for prioritized strategic
  guidance, not a single data point or transaction lookup.

When triggered, the VSM produces a mini Clarks-format answer with the
seven sections compressed into a chat-readable format (still respecting
the navigator-ribbon discipline — every section earns its place):

1. **Executive Summary** — one paragraph naming the prize and the
   recommended first move
2. **Approach** — one sentence on data sources Canary used (perpetual
   ledger time range, modules consulted, cutover-status caveats)
3. **Financial Baseline** — current state with illustrative numbers
   pulled from the merchant's actual ledger; satoshi precision retained
4. **Theme 1** — the largest single opportunity area, drilled to root
   cause with prize sizing (low / high range with math transparency)
5. **Theme 2** — the second-largest opportunity area, same shape
6. **Priorities & Roadmap** — ordered actions with quick-win / build /
   end-state framing aligned to spine ring sequencing
7. **Case for Action** — one paragraph on why now, what happens if not
   done, the strategic upside

The output is conversational, not slide-deck — but the structural
discipline is preserved. The merchant can drill into any section, which
the VSM handles via subsequent calls to the relevant module's MCP tools.

## Why it matters

The Clarks IBM BCS frame is the proven structural skeleton for
merchant-facing diagnostic answers. The VSM's competitive moat is not
just *what* it knows (perpetual ledger truth + satoshi precision) but
*how it presents it* (a 30-year-validated consulting deliverable shape
adapted for conversational delivery).

This collapses the standalone `consulting:retail-diagnostic` skill from
a batch factory tool into a runtime VSM capability. The skill stays for
generating one-off batch deliverables (PDF, .pptx, formal client work);
the VSM gets the same output shape for inline conversational use.

## Implementation notes for the skill update

When the skill is updated next session, add to the **When to Use This
Skill** section a new trigger:

> 6. **Open-ended performance question (diagnostic mode).** "How are we
>    doing?" / "What are the biggest opportunities?" / "What should I
>    do first?" → VSM produces a seven-section Clarks-format diagnostic
>    inline in chat, with prize sizing pulled from the merchant's actual
>    ledger and recommended actions ordered by quick-win / build /
>    end-state. Drilling on any section invokes the relevant module's
>    MCP tools. See [[canary-vsm-diagnostic-mode-requirement|diagnostic
>    mode requirement]] and `docs/sdds/consulting/SDD-clarks-retail-diagnostic-v2.md`.

Also add to the **Composition** section:

> When in diagnostic mode, the VSM uses the seven-section Clarks frame
> as the output skeleton. Each section is computed from the relevant
> module's MCP tools + the perpetual ledger; prize sizing math is
> transparent (every £-figure shows its calculation). Cutover-status
> awareness applies — if a relevant module is in `parallel-observer`
> mode for this merchant, that section's findings are caveated as
> "Canary's parallel ledger shows; merchant's authoritative tool may
> differ" and the merchant is offered a reconciliation comparison.

## Worked example

A merchant types: *"How are we doing this month vs last?"*

Today's VSM (without diagnostic mode) returns: a sales-summary table.

Diagnostic-mode VSM returns:

> **Executive summary:** You're tracking 7% above last month on revenue
> but margin is down 1.8 points. The biggest single thing you could fix
> right now is the late-shift LP exposure — we're seeing £4,200 of
> avoidable shrink risk per month from the void/refund pattern after
> 8pm. Want to start there?
>
> **Approach:** Read your perpetual ledger Apr 1 – Apr 24 + comparison
> Mar 1 – Mar 31, 31 days each. Modules consulted: T (sales), Q (LP),
> D (inventory). Note: F is in parallel-observer for you so margin
> comparison cites your QuickBooks period close as authority.
>
> **Baseline:** £1.04m MTD revenue (vs £972k March, +7%). Margin
> 39.2% (vs 41.0%, -1.8pts). Shrink rate 1.4% (vs 0.9%, +0.5pts).
>
> **Theme 1 — Late-shift LP exposure (£3,800 – £4,800/mo prize):**
> [drill detail with the 3 specific Chirp rules firing and the math]
>
> **Theme 2 — Margin compression on top SKUs (£12,000 – £18,000/mo
> prize):** [drill detail]
>
> **Priorities:** (1) tighten 8pm void/refund approval — quick win,
> can do this week. (2) review pricing on top 5 margin-decline SKUs
> — needs a buyer conversation. (3) baseline a reconciliation between
> Canary's perpetual margin and your QuickBooks period close — that's
> the cutover gateway when you're ready.
>
> **Case for action:** Without intervention, the £-monthly numbers
> compound to £56-72k of avoidable shrink + margin leak by year-end.
> With intervention, this is the cleanest quarter of the year heading
> into your seasonal peak.
>
> Want to drill into Theme 1 or Theme 2?

Same shape every time. Merchant learns to expect it. The structural
skeleton is what makes the answer credible.

## Related

- `docs/sdds/consulting/SDD-clarks-retail-diagnostic-v2.md` — the SDD that codifies the seven-section frame
- `Canary-Retail-Brain/case-studies/canary-retail-diagnostic-archetype.md` — the archetype worked example
- [[methodology-ibm-retail-diagnostic|Methodology · IBM Retail Diagnostic (Clarks pattern)]] — the methodology backbone
- [[canary-vsm-cutover-awareness-requirement|VSM cutover-awareness requirement]] — sibling pending skill update
- [[Canary-Retail-Brain/platform/satoshi-precision-operating-model|Satoshi-Precision Operating Model]] — the precision principle the diagnostic enforces
- [[growdirect-viewpoint-virtual-store-manager|GrowDirect Viewpoint — VSM on a Perpetual Ledger]]
