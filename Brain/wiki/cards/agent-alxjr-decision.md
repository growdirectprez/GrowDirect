---
card-type: role-binding
card-id: agent-alxjr-decision
card-version: 1
domain: platform
layer: cross-cutting
status: open-question
agent: ALX
tags: [alxjr, mini, dispatch, dev-workstation, gcp, decision-pending]
last-compiled: 2026-05-01
needs-review: true
---

# ALXjr — identity decision

After GRO-700 Phase 1 (mini wipe), the Mac mini becomes a dev workstation. The current "ALXjr" identity exists because the mini was a server with its own Docker stack, its own memory bus, and its own dispatch queue. None of those things will exist on the mini after Phase 1. **The ALXjr identity needs a decision: sunset or thin-client.**

## Status: open question — founder decision pending

This card flags the decision; it does not make it.

## The two paths

### Option A — Sunset ALXjr

Mini becomes a dev workstation; Claude Code running on the mini IS the canonical ALX, just with a smaller screen. No separate identity. Linear dispatches lose the `Agent/ALXjr` label entirely; everything dispatched to the mini is dispatched to ALX.

**Pros:**
- Simplest. One agent identity, one memory, one set of dispatches.
- Matches the GRO-700 strategic shift (mini = dev workstation, not server).
- Removes the `Mini Docker Gate` rule from CLAUDE.md once Phase 5 lands.
- No card content debt — `ALXjr` references in `feedback_mini_docker_gate.md`, `project_alx_alxjr_naming.md`, and `feedback_church_state_sessions.md` get retired or rewritten as historical notes.

**Cons:**
- Loses the church/state distinction the mini-as-state-machine convention provided. State-mode dispatch on the laptop becomes the only way to differentiate "this is delivery, not exploration."
- The dispatch protocol's `Target/mini` label semantics shift — it just means "this should be done on a particular machine," not "this is for a different agent."

### Option B — Thin-client ALXjr

ALXjr survives as a distinct agent identity that runs from the mini terminal but authenticates to Cloud Run / Cloud SQL / Vertex AI exactly like ALX on the laptop. The mini is no longer a server, but ALXjr is the "Claude Code running on the mini" identity, distinct from ALX (laptop).

**Pros:**
- Preserves the church/state convention as a behavioral discipline (laptop = church, mini = state).
- Keeps existing dispatch routing (`Target/mini`, `Agent/ALXjr`) without rewrites.
- Memory-bus content on `feedback_mini_docker_gate` stays valid (with Docker gate replaced by "Cloud SQL connectivity gate").

**Cons:**
- ALX and ALXjr authenticate to the same Cloud Run / Cloud SQL / Vertex AI services with the same credentials and produce the same outputs. Two identities for cosmetically different invocations of the same agent.
- The "blind ALXjr" failure mode (Docker down, memory bus unreachable) just transforms into a different failure mode (Cloud SQL Auth Proxy down) — the discipline doesn't get simpler.

## Recommendation

**Sunset (Option A).** The ALXjr identity exists because the mini was a server. After Phase 1 it isn't. The church/state discipline can survive as a session-mode label (`/church` and `/state` skills) without needing a separate agent identity to enforce it. The simpler model wins.

If sunset:
1. Rewrite or delete the following memory files:
   - `feedback_mini_docker_gate.md` → replace with Phase 5 transition note
   - `project_alx_alxjr_naming.md` → mark deprecated
   - `feedback_church_state_sessions.md` → keep, but reframe as session-mode discipline (not agent-identity)
2. Strip ALXjr from `CLAUDE.md`: remove "Mini Hard Rule" section entirely once Phase 5 lands; keep church/state discipline in place
3. Linear dispatch protocol: drop the `Agent/ALXjr` label; keep `Target/mini` (or `Target/cloud-workstations`)
4. Update `gcp-foundation-runbook.md` and `Brain/wiki/agent-card-format.md` references accordingly

## Acceptance — this card closes when

- Founder picks A or B
- The chosen path is captured in CLAUDE.md
- Memory files are reconciled (deletions or rewrites)
- This card's status moves from `open-question` to `approved` with the decision recorded

## Related

- [[platform-alx-vsm]] — ALX canonical agent (post-decision, also covers the mini)
- [[agent-canary-builder]] · [[agent-cove-builder]] — peer builder identities (unaffected by this decision)
- GRO-700 v2 — the dispatch driving the substrate change
- [[gcp-foundation-runbook]] — the substrate ALX runs on, regardless of A or B
