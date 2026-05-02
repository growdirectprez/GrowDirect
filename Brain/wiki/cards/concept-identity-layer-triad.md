---
card-type: platform-thesis
card-id: concept-identity-layer-triad
card-version: 1
domain: platform
layer: cross-cutting
status: draft
last-compiled: 2026-05-03
needs-review: true
agent: ALX
feeds:
  - vertical-smb-health-hypothesis
  - platform-gateway-thesis
  - growdirect-pitch-spine
receives:
  - platform-gateway-thesis
  - concept-substrate-discipline
  - concept-decision-substrate
tags:
  - identity-layer
  - triad
  - health
  - voting
  - consumer-spend
  - vertical-expansion
  - consent
  - smb
---

# The Identity Layer Triad — Health · Voting · Consumer Spend

## What this is

The three through-lines that unify SMB verticals on a single substrate: **health, voting (governance / civic participation), and consumer spend.** Every multi-hat owner-operator on Main Street touches all three. Every vertical the platform expands into projects onto this triad. The substrate carries the identity record once; consent-based projection per vertical is what differentiates the surfaces.

## Purpose

The original GrowDirect investor thesis ([[Brain/wiki/canary/investor-deck-recovery-2026-05-03]]) was multi-vertical from day one — *retail, healthcare, supply chain, legal, insurance, government* on one universal-event-notarization protocol. The current go-to-market is retail-led (Canary, Counterpoint VARs, Square SMB) for sound proof-case reasons, but the platform is not architecturally bound to retail. The identity layer triad is the through-line that makes vertical expansion an extension of the existing substrate rather than a new product.

The three legs of the triad are not arbitrary. They are the three identity domains that **every Main Street operator already participates in** as both citizen and counterparty:

1. **Consumer spend** — they sell, they buy, they receive payments, they manage open-to-buy. Already on the substrate (Canary, retail spine).
2. **Health** — they have employees, they may run a clinic, they have HIPAA-touched workflows whether they think of them that way or not. Needs the substrate (vertical-smb-health-hypothesis).
3. **Voting (governance / civic participation)** — they sit on HOA boards, run community organizations, manage member ballots, vote in regional and national elections. Cove already runs this on the substrate (HOA secret-ballot voting).

The triad is the unifying thesis. The substrate carries identity once; the verticals project consent-bounded views.

## Why these three

The triad isn't decorative. It's the minimum set that covers the operator's real life:

- **Consumer spend** is the operational engine. It is where money moves, evidence accrues, and accountability rails (operational, financial, evidentiary, vendor) earn their keep. The retail proof case anchors this leg.
- **Health** is the regulated leg. HIPAA forces every adjacent system to a higher standard of identity, audit, and consent. Building the substrate to clear HIPAA is what makes it portable to every other regulated domain (financial services, education, eldercare).
- **Voting** is the civic leg. Operator agency ([[mission-main-street]]) requires that the substrate handle governance — secret ballot, weighted voting, jurisdictional rules — because that is where collective decisions about Main Street are made. Cove's HOA voting work is the proof case.

Any vertical the platform considers in future expansion has to ladder onto at least one leg. If it doesn't, it doesn't belong on this substrate.

## Consent-based projection per vertical

The substrate carries the identity record once. The verticals do not get the full record. Each vertical projects a consent-bounded view of the identity through the field-capture / namespace layer.

The architecture:

- **Identity is a substrate-layer record.** Stable identifier, hash-anchored, namespace-resolvable. Carries no policy. (See [[concept-substrate-discipline]] for the rule.)
- **Consent is a substrate-layer contract.** A signed, evidenced authorization that specifies which projection a given counterparty is allowed to see. Lives next to identity, not inside it.
- **Projection is a vertical-module operation.** The retail module sees *spend identity* — receipts, vendor records, OTB events, scorecards. The health module sees *health identity* — patient records, claims, HIPAA-bounded interactions. The voting module sees *governance identity* — ballot eligibility, member status, voting weight. None of them sees the others' projection by default; consent is what opens cross-projection visibility.
- **Cross-projection is the operator's choice.** The operator can authorize their own retail substrate to talk to their own health substrate (e.g., a clinic owner who is also a retail operator), but the protocol does not assume that authorization. The substrate ships consent-off; the operator opts in.

This is the same identity-layer pattern that the .jeffe namespace originally introduced for retail receipt attribution (`docs/_archive/ip-vault/strategy/GrowDirect_Manifesto_v1.1.md` §V.9), generalized across the three legs. The original thesis already had the architecture; this card names the shape and locks the discipline.

## How verticals ladder onto the triad

| Vertical | Triad legs touched | Surface |
|---|---|---|
| Specialty retail (Counterpoint, RapidPOS) | Spend (primary) | Canary · accelerator pack · POSLOG |
| Square SMB merchants | Spend (primary) | Square partnership · Layer 5 brand stack |
| HOA / community governance | Voting (primary) · Spend (secondary, dues + assessments) | Cove · Davis-Stirling compliance |
| SMB Health (clinic, eldercare, dental) | Health (primary) · Spend (secondary) | [[vertical-smb-health-hypothesis]] · M365 + HIPAA tooling |
| Real estate (agent + transaction) | Spend (primary) · Health adjacent (disclosure) · Voting adjacent (HOA) | Angel — currently pinned to Cove |
| Future: education, eldercare, civic services | Voting + Health + Spend in varying mixes | Roadmap, dependent on proof cases |

The verticals are not independent products. They are projections of the same substrate — same protocol, same accountability rails, same runtime-call shape ([[concept-decision-substrate]]). What changes is which leg of the triad anchors the experience.

## Relationship to the original thesis

The original GrowDirect investor decks (`docs/_archive/ip-vault/sales/GrowDirect_Thesis_v1.0.pptx`, `Canary_Square_Opportunity.pptx`) and the Manifesto (`GrowDirect_Manifesto_v1.1.md` §VII.4) framed the multi-vertical TAM as *retail · healthcare · supply chain · legal · insurance · government* — a six-vertical list anchored in universal event notarization. The triad sharpens that list down to its load-bearing three legs:

- *Retail · supply chain · insurance* collapse into **consumer spend** — they're all the operational money-and-goods leg with different risk surfaces.
- *Healthcare* anchors **health** — it is the regulated identity leg, and it forces the highest-standards architecture.
- *Legal · government* collapse into **voting / governance** — they're the civic-participation leg, where collective decisions and accountability records live.

Six verticals → three legs. Same TAM, sharper thesis. The original "TAM is everything" claim survives; what the triad adds is the architectural through-line that makes the multi-vertical pitch land as one platform rather than six business cases. See the recovery doc ([[Brain/wiki/canary/investor-deck-recovery-2026-05-03]]) for the most-quotable original language.

## Consumers

| Consumer | What they do with this card |
|---|---|
| Investor pitch (next deck cycle) | The triad is the slide that follows the gateway thesis — same substrate, three legs, six-plus verticals projected from it |
| Square partnership conversation | Frames the Square play as the spend leg of a substrate that scales to the other two |
| SMB Health hypothesis ([[vertical-smb-health-hypothesis]]) | Direct consumer; the hypothesis depends on the triad to explain why health is the next vertical and not a different product |
| Cove project (HOA voting) | Re-frames Cove as the voting leg of the triad rather than a standalone product |
| Vertical-expansion decisions | New vertical proposals tested against the triad — if it doesn't ladder, it doesn't belong |
| Brand voice plugin | Helps the off-ramp metaphor scale beyond retail without losing voice |

## Sources

| Source | Role |
|---|---|
| `Brain/wiki/canary/investor-deck-recovery-2026-05-03.md` | Original multi-vertical thesis language and citations |
| `docs/_archive/ip-vault/sales/GrowDirect_Thesis_v1.0.pptx` | The "platform is universal" deck (retail · healthcare · supply chain · legal · insurance · government) |
| `docs/_archive/ip-vault/strategy/GrowDirect_Manifesto_v1.1.md` §V.9, §VII.4 | .jeffe namespace as identity layer; Phase 3 vertical expansion |
| `Brain/wiki/cards/platform-gateway-thesis.md` | Substrate-level frame this card extends |
| `Brain/wiki/cards/concept-substrate-discipline.md` | Fractal rule that lets identity stay in the substrate while projection lives in modules |
| `Brain/wiki/cards/concept-decision-substrate.md` | Runtime-call frame that carries the same shape across legs |
| Cove project working papers | HOA voting as the voting-leg proof case |

## Invariants

1. **Identity is substrate-layer, single record.** The platform stores one identity per operator, hash-anchored, namespace-resolvable. Per-vertical projections don't duplicate identity; they read it under consent.
2. **Consent is contract, not configuration.** The authorization to project an identity into a vertical is an evidenced contract — signed, anchored, revocable. No silent defaults that open cross-projection. The substrate ships consent-off.
3. **No vertical sees another vertical's projection without explicit operator consent.** Health module cannot read spend records. Voting module cannot read health records. The operator is the only authority that opens cross-projection.
4. **The triad is exhaustive at the level of through-lines, not verticals.** Future verticals are valid only if they ladder onto health, voting, or spend. A vertical that ladders onto none of the three is a different platform.
5. **The triad respects substrate discipline ([[concept-substrate-discipline]]).** The substrate carries identity records and consent contracts; vertical modules carry the meaning of "what this projection is for." Don't bake vertical policy into the identity record.

## Related

- [[vertical-smb-health-hypothesis|SMB Health Hypothesis]] — the next leg's first proof case
- [[platform-gateway-thesis|Platform Gateway Thesis]] — substrate frame that hosts the triad
- [[concept-substrate-discipline|Substrate Discipline]] — fractal rule that keeps the triad portable
- [[concept-decision-substrate|Decision Substrate]] — runtime-call shape that scales across legs
- [[mission-main-street|Mission · Main Street]] — civic mission that requires the voting leg
- [[growdirect-pitch-spine|GrowDirect Pitch Spine]] — investor narrative the triad re-anchors
- [[Brain/wiki/canary/investor-deck-recovery-2026-05-03|Investor Deck Recovery]] — original multi-vertical language

---

*Captured 2026-05-03 by ALX (substrate captures session). One concept per card — health · voting · consumer spend, consent-based projection, identity-as-substrate. Founder gate: confirm the triad framing before any next-cycle investor deck or Square partnership conversation locks language.*
