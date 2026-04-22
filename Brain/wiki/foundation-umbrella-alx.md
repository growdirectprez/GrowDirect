---
type: wiki
tags: [foundation, cove, alx, orchestration, architecture, parking, deferred]
created: 2026-04-19
sources: [user message 2026-04-19]
status: parking
last-compiled: 2026-04-19
needs-review: 2026-05-03
---

# Foundation — Umbrella ALX (Parking)

Parking card for a structural idea that emerged in conversation but is not yet fully designed: **ALX as the orchestration layer across the three entities (Foundation, LLC, Community of Abalone Cove)**.

The founder said: "personal stuff in there too takes ok its founder narrative we are figuring out a whole umbrella ALX."

This card holds the thread so it doesn't get lost. The design comes later, once the three entities are stable and the three-hat time-logging pipeline is working.

## What ALX Is Today

ALX is the platform-level agent architecture already in the repo:

- Platform service skeleton under `services/` and referenced from Linear project "Platform" (`ab4d168d-a7ae-4526-8fd6-8fa1bc7c971d`)
- Feeds agent context to builders (Canary builder, Cove builder) and coordinates cross-app work
- Runs in the shared GrowDirect Docker infrastructure
- Tools for memory, domain context, session start
- Per Cove/CLAUDE.md: "Founder: Jeffe (CEO — talks to ALX, not directly to builders)"

ALX already is the founder-facing orchestration layer for software development. The question this card holds is whether it extends to orchestrating the three-entity operational structure.

## What "Umbrella ALX" Could Mean

Possibilities, in rough order of scope:

### 1. Time-logging orchestration (smallest scope)

ALX becomes the thing that:
- Ingests git + Linear + Brain + email logs
- Applies the file-path allocation rules from [[foundation-three-hat-compensation]]
- Emits the monthly summaries for board review
- Flags sessions where the hat allocation is ambiguous or mixed

This is the natural extension of the existing project-timelog skill and directly serves the Foundation's compensation compliance requirements. See [[foundation-time-logging-policy]].

### 2. Cross-entity context broker (medium scope)

ALX holds context for each hat separately and can answer "what Foundation work has been done this month?" "what's the Community of Abalone Cove third-director recruitment status?" "what's the LLC rescue status?" — without mixing state across entities.

- Foundation context: Brain wiki articles, cove.org content, advisor memos, 1023-EZ status
- Community of Abalone Cove context: board roster, bylaws-as-config, payment-platform selection, third-director recruitment
- LLC context: commercial product status, licensing pipeline, rescue checklist

This is harder than (1) because it requires entity-scoped memory, but it's doable with the existing MCP + memory-bus architecture.

### 3. Governance orchestration (largest scope)

ALX runs agentic workflows tied to specific governance events:
- When a Community of Abalone Cove board meeting is scheduled, ALX prepares the agenda from open issues
- When a Foundation board meeting is scheduled, ALX generates the compensation summary
- When a §V §5 reactivation is called, ALX coordinates the hybrid blockchain-proof process
- When a Foundation grant is submitted, ALX assembles the supporting evidence from the Library of Evidence

This is Epic-3-adjacent. Don't design it yet.

## Why This Is Parked

Premature design of the umbrella would:
- Lock in entity boundaries that haven't been established yet
- Over-couple Foundation, Community of Abalone Cove, and LLC operations
- Create a system with no real users (the entities don't exist yet)
- Distract from the actual Q1 priorities (form the Foundation, restore Community of Abalone Cove quorum, rescue the LLC)

Parking it here ensures the idea doesn't get lost while the foundational work happens.

## Trigger for Revisiting

Revisit this card when:
- The Foundation is formed, bylaws adopted, and the first compensation cycle has run
- Community of Abalone Cove quorum is restored and the first payment-platform contract is in place
- The LLC is in good standing
- The project-timelog skill extension has been running for 3–6 months and the operational pain points are known

At that point, scope (1) above is the most obvious first cut. Scopes (2) and (3) follow the actual needs.

## Related

- [[foundation-legal-framework]] — MOC
- [[foundation-time-logging-policy]] — The pipeline that would be the first "umbrella ALX" use case
- [[foundation-three-hat-compensation]] — The entity separation the umbrella must respect
- [[wpbca-compliance-framework]] — The Community of Abalone Cove side of the orchestration
- [[foundation-founders-narrative]] — Founder's own language ("umbrella ALX") is preserved in the narrative
- Linear project "Platform" — Where ALX work already lives
