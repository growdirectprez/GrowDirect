# Canary Protocol — Next-Session Kickoff Prompt

**Author:** ALX · Date: 2026-05-02 (for execution next session)
**Companion:** `2026-05-03-canary-gcp-blinking-multi-track-kickoff.md` (the full plan this prompt routes to)

---

## What this is

A copy-paste prompt for the next deep code session. Designed for state-mode autonomous execution with subagent dispatch in parallel where dependencies permit. The full multi-wave plan lives in the companion file — this prompt is the entry point that loads it and sets working norms.

## Usage

1. Open a new Claude Code session in `/Users/gclyle/GrowDirect`
2. Paste the **prompt** section below into the first message
3. Let it run autonomously; respond only to the explicit ESCALATE triggers

The prompt is self-contained: it routes to the full plan, loads the relevant memories, sets working norms, and defines escalation triggers. Bias toward action; reserve interrupts for the genuine unknowns listed under ESCALATE.

---

## The prompt

```
You are running the Canary Protocol GCP-API-Blinking MVP push.

Read these in this exact order, then start:

1. /Users/gclyle/GrowDirect/CLAUDE.md — platform rules (working dir context)
2. /Users/gclyle/GrowDirect/docs/superpowers/plans/2026-05-03-canary-gcp-blinking-multi-track-kickoff.md — your full plan; treat it as the spec
3. /Users/gclyle/GrowDirect/docs/superpowers/plans/2026-05-02-canary-protocol-phase1-execution-plan.md — predecessor plan; supersedes priority order but inherits dispatch inventory
4. The most recent comment on Linear GRO-739 — strategic reorder context
5. Run memory_recall("project_canary_is_customer_of_protocol") + memory_recall("project_gcp_commitment_locked") + memory_recall("feedback_just_commit_no_three_card_monte") + memory_recall("feedback_working_documents_not_pitch_decks")

MISSION (one sentence): end this session with api.canary.growdirect.io deployed on GCP, accepting signed webhooks from outside the laptop, staging events into Cloud SQL — with DPA + breach runbook drafted as working documents.

EXECUTION:
- Wave 1: file the new Phase 1.J dispatch under GRO-739, then dispatch 5 subagents in parallel (briefs are in §1.1 through §1.5 of the plan). Use git worktrees so they don't step on each other.
- Wave 2: review subagent commits, sequence integration.
- Wave 3: per-track commits with full test runs; ship dispatches to Done.
- Wave 4: execute the Phase 1.J runbook; light up api.canary.growdirect.io; smoke-test from outside the laptop.

WORKING NORMS (encoded from saved feedback memories — non-negotiable):
- No three-card monte. When the next step is obvious, just do it. Don't ceremoniously surface trivial decisions.
- Working documents not pitch decks. Any docs produced are working-grade — tables, references, named owners, no marketing copy.
- Files are for agents. Concise, actionable, machine-readable. External-facing leave-behinds keep human polish.
- Patent claims (Application 63/991,596) are the architectural spine. No silent drift.
- No internal agent identity names externally. The .jeffe namespace IS external; ALX/Owl/etc. are NOT.
- Memory bus reseed after any Brain/wiki/ change.
- Per-dispatch comments on pickup AND completion (commit SHA + DoD verification).

PRE-FLIGHT before spawning anything (~5 min): git status, docker ps for postgres+valkey, gh auth status, gcloud auth list. If gcloud isn't authenticated or the Docker stack is down, stop and tell me. If git status shows surprise uncommitted work in CanaryGo/, stop and tell me.

ESCALATE to me only on:
- gcloud auth or wrong project
- DNS / Cloudflare API access needed
- Cost estimate > $200/mo for the MVP
- Patent-claim drift that needs adjudication
- Counsel-sign-off-required legal wording

Everything else: ship it, log it, move. Bias toward action and reporting what's done over what's perfect.

Begin with the pre-flight, then Wave 1.0.
```

---

## Why this shape

- **Self-contained** — works cold, no prior conversation context required
- **Files are the spec** — the meaty plan lives in the companion markdown file; the prompt routes the next session there
- **Working norms upfront** — the `feedback_*` memories get loaded explicitly so the next session doesn't re-learn them by trial and error
- **Wave structure visible** — the next session knows the shape immediately
- **Escalation triggers explicit** — the founder doesn't get pinged for things that aren't worth pinging for, but does get pinged for the genuinely-need-input moments
- **One clear "begin" instruction** — pre-flight, then Wave 1.0

## Expected outputs

If the plan executes well: 5 dispatches shipped (GRO-687/693/694/748 + new Phase 1.J), `api.canary.growdirect.io` live, Cloud SQL receiving real evidence rows. Even at 70% execution that's a Phase-1-MVP-shipped session.

## When to spawn this

Whenever the founder is ready to commit a full focused block (~6-8 hours) to pushing the GCP-blinking MVP. Don't fragment across short sessions — the wave structure assumes contiguous work time so subagents can run in parallel without coordination overhead from interleaved interrupts.
