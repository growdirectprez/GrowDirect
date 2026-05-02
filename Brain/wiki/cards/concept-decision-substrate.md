---
card-type: platform-thesis
card-id: concept-decision-substrate
card-version: 1
domain: platform
layer: cross-cutting
status: draft
last-compiled: 2026-05-03
needs-review: true
agent: ALX
feeds:
  - platform-gateway-thesis
  - website-canary-launch
  - square-partnership
  - vertical-smb-health-hypothesis
receives:
  - platform-gateway-thesis
  - concept-substrate-discipline
tags:
  - decision-substrate
  - runtime
  - session-thread
  - ai-architecture
  - continuity
  - square-partnership
  - main-street
---

# The Decision Substrate — Runtime Calls, Not Session Threads

## What this is

The architectural claim that ties the Square partnership opportunity, the AI-as-team accelerator pack, and the Main Street mission together: **the platform is a runtime that calls agents on contract events, not a chatbot that operators open in sessions.** The substrate carries the operator's durable record of how this specific business decides things; the agents are stateless callers; the operator gets continuity for free.

## Purpose

Every "AI for retail" pitch in 2025–2026 is session-shaped. The operator opens a chat. Asks a question. Gets an answer. Closes the chat. Tomorrow they open another chat. Cold start. The platform never accumulates memory of how this specific store decides things; the operator never accumulates leverage from the platform's prior runs. The platform's data model lives inside the chat thread. Close the thread, lose the substrate.

This is the wrong shape for retail operations. Retail decisions are continuous, multi-actor, context-heavy, and expensive to re-derive from scratch. A receiving discrepancy that fires today connects to a vendor scorecard event from last quarter, an OTB commitment from last month, a supplier conversation from yesterday. The session-shaped agent has none of that context unless the operator manually re-states it every time — which they won't, because they're running a store.

The decision-substrate frame inverts the architecture: **the substrate's data model is the durable layer; the agents are stateless callers; the runtime invokes them when contract events fire.** A receipt arrives → POSLOG record → namespace identity attached → field-capture maps fields → contract event fires → relevant agent function runs → result writes back to substrate. The operator never opened a chat. The agent never started cold. The substrate carried the continuity.

## The technical-meets-business claim

The technical claim is architectural: **runtime calls, not session threads.** The business claim is the consequence: **operators get the eight-specialist team they could never afford** ([[mission-main-street]]) without managing eight chat threads, because the substrate carries the context the agents need.

The claim lands at three altitudes simultaneously, which is why it ties so many strategic conversations together:

| Altitude | What it sounds like | Why it lands |
|---|---|---|
| **Square partnership** | "We're the missing operations + decision substrate above the till — runtime, not sessions, accumulating against POSLOG." | Square's marketplace has no decision-continuity layer. The till is the till; everything above the till is missing. We are the substrate for what happens above the till. |
| **AI-as-team / accelerator pack** | "The accelerator pack is the analyst, architect, dev, delivery, support, training, change, CSM the retailer never hired — runtime functions over their substrate, not chat sessions they have to remember to open." | The session-shaped competitors burn the operator's attention. The runtime-shaped substrate gives the operator their attention back. |
| **Main Street mission** | "Operator agency means the substrate is the operator's; the agents are interchangeable; the leave-behind is the substrate, not the agents." | The session model traps operators in the vendor's chat surface. The runtime model puts the durable record in the operator's substrate, where they can swap agents, run their own, or fork the protocol. |

## Why session-shaped fails for retail

Three structural failures of the session model in this domain:

1. **Cold start tax.** Every conversation reconstructs the operator's context from scratch. Multi-hat operators don't have time to brief an agent every morning; the agent that needs briefing is worse than no agent.
2. **Context loss on close.** The session thread holds the analytical work; closing the thread loses the work. Operators need the *substrate* to hold the analytical context, not the chat surface.
3. **Vendor-locked memory.** Session memory lives on the vendor's servers. The operator can't fork it, audit it, or take it with them. This is incompatible with the open-protocol commitment ([[mission-main-street]]).

The runtime-shaped alternative fixes all three by placing the durable state in the substrate the operator owns and treating agents as callers — replaceable, auditable, and answerable to the substrate's contract.

## How it shows up architecturally

The runtime-call model has concrete architectural consequences that distinguish it from the session-shaped competition:

- **POSLOG is the event spine.** Every contract event (receipt, vendor short-ship, OTB commit request, evidence anchor request, scorecard tick) fires a runtime call. The agent network listens; agents are subscribers, not chat counterparties.
- **Namespace identity attaches to records, not to sessions.** A receipt knows what merchant it belongs to without an operator authenticating. The substrate carries identity.
- **Field-capture is the agent's input contract.** Agents read field-captured records, not free-text descriptions. This is what makes them stateless and replaceable — the contract is the substrate, not the prompt.
- **The MCP tool surface is for the runtime, not for the human.** Agents call MCP tools because the runtime fired them; the operator never types into MCP. The operator interacts with the substrate (the Brain, the dashboards, the alerts); the runtime mediates.
- **Evidence anchor on every meaningful event.** The cryptographic provenance lives in the substrate, not in a session log. (Implementation: hash-chained provenance via L2 anchoring — architecture-only language.)
- **Vendor accountability rail rides the same shape.** Cloud-bill SLA assertions are runtime calls against telemetry, not dashboard reviews. See [[platform-thesis]] Rail 4.

## Consumers

| Consumer | What they do with this card |
|---|---|
| Website `/gateway` copy | The substrate page articulates runtime-vs-session as the architectural difference; this card is the source |
| Square partnership conversation | "We are Square's missing operations + decision substrate" lands because of this card's claim |
| Partner deck (Tim Mooney recap) | The "AI as accelerator pack" slide rests on the runtime-call frame |
| Investor follow-on conversations | When asked "how are you different from the AI-for-retail companies", this is the answer |
| Future agent designers | When designing a new accelerator-pack capability, the rule is *runtime call, not session thread* — this card is the specification |
| Architectural reviews | Any proposed feature that requires a long-lived session thread fails this card; redesign required |

## Sources

| Source | Role |
|---|---|
| `Brain/wiki/cards/platform-gateway-thesis.md` | The thesis this concept ladders into |
| `Brain/wiki/cards/platform-thesis.md` | Four accountability rails — all of them runtime-shaped, not session-shaped |
| `docs/sdds/go-handoff/go-module-layout.md` | Module spine — every module is a runtime function over POSLOG |
| Founder's working memory | The articulation captured during the substrate captures session, 2026-05-02/03 |

## Invariants

1. **Substrate is durable; agents are stateless.** The operator's record of how their business decides things lives in the substrate. Agents that hold state across calls are violating this card.
2. **Runtime invokes; operator is invoked.** The runtime fires the agent on a contract event. The operator does not have to remember to ask. The operator is alerted (or not), based on what the substrate says is decision-worthy.
3. **No long-lived session threads in the agent surface.** A chat-style session is acceptable as a UI affordance only if the substrate holds the durable record and the session is just a view onto it. Treat the session as a window; close it, the substrate persists.
4. **Agents are replaceable.** Because the contract is the substrate (not the prompt), any agent that conforms to the field-capture input and writes back the contract output can replace any other. This is the architectural consequence of the open-protocol commitment ([[mission-main-street]]).

## Related

- [[platform-gateway-thesis|Platform Gateway Thesis]] — the thesis this concept ladders into
- [[concept-substrate-discipline|Substrate Discipline]] — the fractal rule that keeps decision-making out of the substrate
- [[mission-main-street|Mission · Main Street]] — the civic frame that requires substrate ownership
- [[platform-thesis|Platform Thesis]] — four accountability rails as runtime calls
- [[concept-identity-layer-triad|Identity Layer Triad]] — the same runtime model carrying health, voting, and spend across verticals

---

*Captured 2026-05-03 by ALX (substrate captures session). One concept per card — runtime calls, not session threads. Founder gate: confirm the runtime-vs-session articulation lands as the technical core of the Square partnership pitch before the conversation runs.*
