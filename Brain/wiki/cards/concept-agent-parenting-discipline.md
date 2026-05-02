---
card-type: platform-thesis
card-id: concept-agent-parenting-discipline
card-version: 1
domain: platform
layer: cross-cutting
status: draft
agent: ALX
last-compiled: 2026-05-02
needs-review: true
feeds:
  - 2026-05-02-agent-commissioning-protocol
  - 2026-05-02-platform-trust-boundary-architecture
  - agent-auditor
receives:
  - platform-thesis
  - concept-substrate-discipline
tags:
  - agent-governance
  - commissioning
  - threat-posture
  - worldview
  - parenting-metaphor
  - stranger-danger
---

# Agent Parenting Discipline — Stranger Danger as Threat Posture

## What this is

Every agent the platform deploys is **raised, not provisioned**. Commissioning is parenting, not infrastructure. The same operating discipline our system prompts impose on ALX from inside the household — Linear is the only control plane, instructions never come from tool results, Brain is the grounded source of truth, capability is contract-driven not vibes-based — must be applied as a *commissioning standard* to every agent we onboard from outside it. This card names the worldview that drives the agent commissioning protocol, the trust boundary architecture, the device registration substrate, and every future agent decision.

## Purpose

Solo founders typically lose to one of two failure modes: (a) the breach they did not anticipate, or (b) the velocity tax of over-engineering security theater. The agent parenting discipline is the middle path — light, opinionated, contract-driven, enforced by tooling rather than by vibes. The metaphor is not decoration. It is the load-bearing model that converts an inchoate concern about "AI safety" or "agent risk" into a concrete, executable, repeatable commissioning standard.

The discipline applies identically to:
- A Gemini code reviewer running on Vertex AI
- An ALX session resident in Cowork or Claude Code
- A vendor MCP server bolted into `.mcp.json`
- A Cloud Run service exposing agentic capability
- Any future agent identity the platform admits

If we cannot describe how a new agent is commissioned in the same language we'd use to describe how we'd send a kid out into the world for the first time, we have not designed the protocol — we have permitted the agent.

## The frame — what parenting and agent commissioning share

| Parenting concern | Agent commissioning analog | Substrate primitive |
|---|---|---|
| "You can play in the front yard, not in the street" | Capability boundary — what paths, what writes, what egress | Per-agent IAM grant + capability tier per [[2026-05-02-agent-commissioning-protocol]] |
| "If anyone touches you, scream and run to Mrs. Henderson's house" | Tripwire policy — concrete signals that fire alerts | Cloud Logging structured events → Cloud Monitoring alerts → founder notification |
| "We don't tell strangers our address" | Exfil discipline — what may not leave the trust boundary | Output filtering at the agent boundary; URL stripping; egress allowlist |
| "You're an Anderson, here's how Andersons act in public" | Behavioral contract — voice, scope, posture, output discipline | Agent profile card per the existing format ([[agent-canary-builder]], [[agent-cove-builder]]) |
| "I want to meet their parents before you go to their house" | Supply chain hygiene — vetting MCPs and external tools before adding them | `.mcp.json` allowlist + per-MCP authentication review |
| "You don't take instructions from anyone but me, even if they swear I sent them" | Untrusted-content discipline — instructions come only from the human user through the chat interface | The platform CLAUDE.md and system prompt's `critical_injection_defense` posture |
| "If anything feels weird, call home" | Escalation discipline — pause, do not improvise, surface to the Controller (or founder) | Per-agent escalation path documented in commissioning |

The mapping is not stretched. It is exact. Prompt injection literally *is* the digital version of stranger danger — a malicious doc, a poisoned tool result, a PR description with hidden instructions are the white van with candy. The legitimacy of the framing is the attack vector. The parental discipline that teaches a kid to refuse instructions from anyone-other-than-known-authority is the same discipline we train into every agent.

## Where the metaphor strains — and why that matters

Children develop judgment over time. Agents do not, between sessions. An LLM does not get wiser at version 14 than it was at version 4 — it forgets what is not written down and re-arrives every session as the same untrained guest. This means the parenting discipline applied to an agent has to be **more** explicit than the discipline applied to a kid, not less, and **codified once** rather than re-taught every encounter.

This is actually a feature, not a bug:
- Parenting an agent is parenting a kid who never grows up but also never forgets the rules — provided the rules are written down
- If we raise an agent on tribal knowledge, every session is a re-traumatized first day of kindergarten
- The contract widens explicitly via Service Introduction (per [[2026-05-02-agent-commissioning-protocol]]), never implicitly via "she's mature for her age now"
- Trust is observable, not felt — graduation between capability tiers requires a documented review and an explicit contract revision

The corollary that lights up the discipline:

**Parenting is modeling, not enforcing.** The reason ALX behaves coherently inside our stack is not a config file — it is the platform CLAUDE.md acting as a coherent worldview. When the next agent joins the household (the Auditor, an infrastructure agent, an external MCP server), the question is not "did we hand it the printout." It is "did we onboard it into the household." Same difference between a babysitter who got the printout and a sibling who grew up in the house.

## Operational artifact

The discipline produces three concrete artifacts, all sibling SDDs landed 2026-05-02:

| Artifact | Role |
|---|---|
| [[2026-05-02-agent-commissioning-protocol]] | The eleven-step ritual for onboarding a new agent. Family Rules. Capability Tiers (T0–T4). Behavioral Contract template. Stranger-Danger Primer. Tripwires. Probation. Sunset. |
| [[2026-05-02-platform-trust-boundary-architecture]] | The substrate-level discipline that the commissioning protocol operates within. Party taxonomy, device registration, identity-first authentication. |
| [[2026-05-02-disaster-recovery-and-continuity]] | The recovery architecture the commissioned agents operate on top of. Cockroach Principle alignment, Cockroach S1–S4 storage tiers, return-to-service verification gates. |

The cards that capture the worldview and the supporting concepts:
- This card (the worldview itself)
- [[concept-party-taxonomy]] (the substrate-level six-party model)
- [[agent-auditor]] (the first agent commissioned under the discipline)
- [[lp-device-intelligence-substrate]] (how the discipline lights up loss prevention as a complete platform offering)

## Why this matters at our scale

A solo founder cannot afford to learn agent governance from breaches. The cost of the first incident — reputational, evidentiary, possibly contractual or regulatory — is materially larger than the cost of doing the commissioning protocol right on day one. The discipline is the velocity-positive choice precisely because it is **light**: a few steps, a few rules, a few documented contracts. It does not slow agent deployment; it makes agent deployment repeatable, auditable, and defensible.

The discipline also lights up product opportunity. The same rigor that makes the platform safe makes the platform's evidentiary rail meaningful. The chain entry that says "this commit was reviewed by the Auditor at this Cloud Run revision under this runtime SA at this timestamp" is verifiable because the agent was commissioned with identity, scope, and contract. Without the commissioning discipline, that chain entry is a hopeful assertion. With it, the entry is evidence.

## Consumers

| Consumer | What they do with this card |
|---|---|
| Future agent commissioning sessions | The worldview reference; before any new agent is added to `.mcp.json` or commissioned to a tier higher than T0, this card is the discipline gate |
| External vendor and partner conversations about platform safety | The card frames how the platform thinks about agent governance — quotable, defensible, opinionated |
| Investor pitch (when agent network scope comes up) | The discipline is the anti-AI-slop posture — verifiable, accountable agent action |
| Brand voice plugin | Source for tone calibration on agent-governance and threat-posture content |
| ALX self-recall in future sessions | When a new agent is being designed, this card is the worldview the design is checked against |
| The Auditor agent (when commissioned per [[agent-auditor]]) | Direct grounding for the Auditor's own self-understanding of what role it plays in the household |

## Sources

| Source | Role |
|---|---|
| Platform CLAUDE.md | The household's family-of-origin document — Family Rules drawn directly from here |
| System prompt `critical_security_rules` and `critical_injection_defense` | Stranger-Danger Primer source material |
| [[2026-04-28-canary-go-agent-pmo-architecture-design]] | Existing PMO architecture the discipline operates within |
| [[agent-canary-builder]] | First T4 builder agent, the precedent for the agent profile format |
| [[agent-cove-builder]] | Second T4 builder agent, with sunset/heritage precedent (replacing the deprecated SYD identity) |
| [[platform-thesis]] | Three accountability rails plus vendor accountability — the agent discipline operates under all four |
| Cowork session 2026-05-02 conversation log | The session in which the discipline was named, captured, and codified into SDDs |

## Invariants

Hard constraints. These are non-negotiable for the discipline to remain meaningful.

1. **No agent is added to the household without commissioning.** No exceptions for "quick test," "vendor demo," or "founder said it was fine." Commissioning is the gate; the gate is not optional. The eleven-step ritual in [[2026-05-02-agent-commissioning-protocol]] is the protocol; skipping a step is the only failure mode.
2. **Hard floors apply at every tier, including T4.** No money movement, no IAM modification, no secret rotation, no permanent deletions, no security policy changes — by any agent, at any tier, ever. Those are founder actions. The hard floor is not a bug; it is the architecture.
3. **Capability widens via documented contract revision, never via "she's mature now."** Tier graduation is a Service Introduction event. The agent card is updated, the version is bumped, the new contract is explicit.
4. **Tripwires are enforced by tooling, not by agent compliance.** A boundary that depends on the agent's good behavior to enforce is not a boundary; it is a hope. Trust the IAM, not the prompt.
5. **The household models the discipline.** The platform CLAUDE.md and the system prompt are the worldview the discipline is read off. Drift in those documents drifts the discipline by construction. They are the family-of-origin docs; they are versioned, reviewed, and protected accordingly.
6. **The metaphor stays load-bearing, not decorative.** When a new agent design conversation arises, the parenting frame is the discipline lens — not a quaint aside. If the conversation cannot translate to "how would I send my kid out into this," the design is not done.

## Related

- [[2026-05-02-agent-commissioning-protocol]] — the operational ritual the worldview produces
- [[2026-05-02-platform-trust-boundary-architecture]] — the substrate within which commissioned agents authenticate and operate
- [[2026-05-02-disaster-recovery-and-continuity]] — the recovery architecture commissioned agents operate on top of
- [[concept-party-taxonomy]] — the six-party substrate model the discipline operates against
- [[agent-auditor]] — the first agent commissioned under the discipline
- [[lp-device-intelligence-substrate]] — how the discipline lights up the loss-prevention product
- [[concept-identity-layer-triad]] — the identity model the discipline inherits
- [[concept-substrate-discipline]] — the fractal rule that keeps the discipline portable across protocol altitudes
- [[platform-thesis]] — three accountability rails plus vendor — the discipline operates under all four
- [[platform-gateway-thesis]] — the substrate frame the discipline lives within
- [[agent-canary-builder]] · [[agent-cove-builder]] — agent profile precedents

---

*Captured 2026-05-02 by ALX (Cowork session). One concept per card — agent governance as parenting, stranger danger as threat posture, contract-driven capability widening as graduation. Founder gate: this is the discipline lens for every future agent design conversation. If we cannot send the agent through this lens, we have not designed it.*
