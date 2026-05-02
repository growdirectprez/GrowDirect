---
card-type: platform-thesis
card-id: concept-party-taxonomy
card-version: 1
domain: platform
layer: cross-cutting
status: draft
agent: ALX
last-compiled: 2026-05-02
needs-review: true
feeds:
  - 2026-05-02-platform-trust-boundary-architecture
  - 2026-05-02-agent-commissioning-protocol
  - lp-device-intelligence-substrate
  - agent-auditor
receives:
  - concept-identity-layer-triad
  - concept-substrate-discipline
  - platform-thesis
tags:
  - identity
  - parties
  - substrate
  - permissioning
  - evidentiary-rail
  - auditor
  - investigator
  - mcp-agents
---

# Party Taxonomy — Six Parties, One Substrate

## What this is

Every authenticated caller — human or machine — resolves to exactly one **party** in the substrate. The party model is the relational layer above the authentication mechanism: authentication answers *can this credential connect*; party resolution answers *who is this, in what role, with what standing*. Six party types cover the full surface of the platform, each with a distinct permission model, evidence-chain treatment, and consent-contract semantics.

The taxonomy is not arbitrary. It tracks the platform's [[platform-thesis|accountability rails]] (operational, financial, evidentiary, vendor) and lights up the substrate's permissioning architecture by saying *every party type maps onto at least one rail, and the rail determines how the substrate treats them*.

## The six parties

| Party type | Definition | Rail alignment |
|---|---|---|
| **Customer** | The merchant/operator who licenses the platform. The relational anchor every other party permissions against. | Operational + Financial |
| **Vendor** | A partner selling *into* the merchant (supplier, service provider, contracted integrator). Reads merchant data under contract, not ownership. | Vendor accountability |
| **Consumer** | An end shopper buying *from* the merchant. Lightweight identity — receipt-anchored, opt-in for deeper binding. | Financial (transactional) |
| **Auditor** | An accountant, third-party verifier, or regulator-aligned party with **standing** scope to a merchant's records. | Evidentiary |
| **Investigator** | A loss-prevention investigator, insurance investigator, or law enforcement officer with **time-bounded** authority to examine records. | Evidentiary |
| **MCP Agents** | Platform-resident or external agents per the [[2026-05-02-agent-commissioning-protocol]]. The runtime context (Cloud Run revision + runtime SA, or Cowork session + agent identity) is the device. | Cross-cutting |

## Why six and why these

The six parties are exhaustive at the level of substrate-relevant relational types. Future expansion of the platform does not require new party types unless the substrate model itself shifts. The justification by party:

**Customer** is the platform's commercial anchor. Every other party permissions against the customer's tenant. Without the customer party, there is no substrate to permission.

**Vendor** is distinct from customer because the relational direction is reversed — the vendor sells into the merchant, not the other way around. Vendor data access is read-under-contract (PO acknowledgments, shipment confirmations, vendor-scorecard data the vendor contributes), never ownership. The vendor accountability rail per [[platform-thesis]] is what gives vendor party type its substrate weight.

**Consumer** is the lightweight party — an end shopper whose identity is normally just a receipt anchor. The consumer party gets first-class substrate status because retail loss prevention, gift card fraud detection, and e-commerce fraud detection all require fingerprinting and pattern-matching at the consumer surface. Without explicit consumer party type, the substrate would conflate consumers with anonymous traffic and lose the ability to anchor consumer-side accountability cases.

**Auditor and Investigator** are the two evidentiary parties, distinguished by the fundamental difference between *standing* and *time-bounded* scope. This distinction is the single most underdeveloped concept in our prior wiki and gets its own subsection below.

**MCP Agents** is the autonomous-action axis. Per the [[concept-agent-parenting-discipline]] and the agent commissioning protocol, agents have identity, capability tier, and runtime context — they are first-class parties in the substrate, not function calls. Treating them as a party type rather than a system primitive forces the discipline that every action they take is anchored, attributed, and revocable.

## The auditor / investigator distinction

This is the distinction that does not exist anywhere else in the wiki and matters enough to warrant its own framing.

| Dimension | Auditor | Investigator |
|---|---|---|
| **Scope shape** | Standing — ongoing, contracted, expected | Time-bounded — incident-driven, authority-anchored, exceptional |
| **Authorizing instrument** | Audit engagement contract (signed by merchant) | Authority instrument — case ID, claim number, subpoena, court order, regulatory examination notice |
| **Cross-tenant** | Rare; only when audit framework grants it (regulator examining a category of merchants is the exception) | Norm under the right authority instrument; cross-tenant is what investigators do |
| **Renewal mechanism** | Per audit engagement period (annual, quarterly) | Auto-expires at the authority instrument's terminus (case closure, claim resolution, court order satisfaction) |
| **Substrate's posture toward them** | Trusted, expected, part of normal operations | Trusted under instrument, exceptional, invokes the substrate's external-authority-acknowledgment posture |
| **Evidence-chain treatment** | Every read logged (auditor presence is itself evidentiary); audit notations anchored | Every read logged with authority instrument reference; chain entries cite the authorizing document; investigator identity bound to instrument identity |

The mechanical reason this matters: auditors and investigators have *different* consent and authorization substrates, and conflating them produces either auditor-friction (treating a quarterly accountant like they need a court order every time they log in) or investigator-overreach (giving a one-off subpoena holder the standing of a registered auditor).

The product reason this matters: the Loss Prevention substrate ([[lp-device-intelligence-substrate]]) depends on the investigator party type to legitimize marketplace observation under retailer authorization. The Q3 quadrant (external resale of stolen merchandise) is built on the platform serving as an authorized investigator on behalf of the retailer for specific reported-stolen items — not as a general scraper. Without the investigator party type, that capability does not have a defensible substrate.

## Multi-party authorization

Some actions require *multiple* party identities in the same authorization envelope. Examples:

| Action | Required parties | Why |
|---|---|---|
| Vendor write to merchant data (e.g., shipment confirmation update) | Vendor identity + merchant-side consent contract | The vendor proves the action; the merchant has consented to the vendor's writes via contract |
| Cross-tenant investigator query | Investigator identity + authority instrument reference + (where framework demands) affected merchants' notification record | The investigator's authority is bounded by the instrument; the substrate verifies the instrument applies to the queried tenants |
| MCP agent escalation to founder | Agent identity + founder confirmation through chat interface | Per the commissioning protocol's escalation discipline — the agent cannot self-authorize; the founder confirms |
| Consumer cross-merchant identity binding (e.g., loyalty program shared across two merchants the consumer authorizes) | Consumer identity + merchant A consent + merchant B consent + consumer-explicit binding event | Triangulated consent; the consumer is the authority opening the cross-projection per [[concept-identity-layer-triad]] |
| Auditor cross-tenant query (regulatory examination) | Auditor identity + audit engagement contract + (where framework demands) regulatory authority reference | Standing scope plus the framework grant for cross-tenant; auditor identity is registered to the substrate as long-lived party |

Multi-party authorization is the substrate's mechanism for high-stakes operations. The chain entry carries every contributing identity; the operation is non-repudiable for each. This is the substrate primitive that makes "the merchant authorized this" or "the investigator was operating under this subpoena" verifiable evidence later.

## Rail alignment

The taxonomy maps onto the four accountability rails per [[platform-thesis]]:

| Rail | Primary parties | Why |
|---|---|---|
| **Operational** | Customer, MCP Agents | The rail of "no unknown loss" — operations, ownership, agentic execution against the operator's substrate |
| **Financial** | Customer, Vendor, Consumer | The rail of money-and-goods movement — every party that participates in a commercial transaction |
| **Evidentiary** | Auditor, Investigator (primary); all parties (secondary) | The rail of verifiable record — auditors and investigators are the parties whose work *is* the evidentiary rail; every other party contributes to the chain |
| **Vendor accountability** | Vendor (primary); Customer (secondary) | The rail of vendor cost-to-serve transparency — the vendor's actions and economics are first-class evidence the customer can verify |

The party taxonomy is what makes the rails computable. Without the taxonomy, "the evidentiary rail is the audit chain" is a slogan. With the taxonomy, the rail is "every party with auditor or investigator status produces chain entries with their identity bound to their authorizing instrument; every other party contributes events anchored under their tenant scope."

## Substrate primitives

The taxonomy is enforced by substrate-level primitives detailed in [[2026-05-02-platform-trust-boundary-architecture]]:

- **Device registration** — every device that touches the platform is registered to exactly one party at exactly one trust level
- **Authentication mechanism per party type** — Workload Identity for MCP agents; OIDC for human parties; mTLS for on-prem station devices owned by customer; HMAC for webhook senders; per-partner contracts for vendor systems
- **Tenant isolation (RLS)** — every tenant-scoped table enforces `tenant_id` at the database layer; party identity is bound to a tenant; cross-tenant access is an architectural event with explicit authority
- **Consent contracts** — per [[concept-identity-layer-triad]], the substrate-layer authorization that one party may project across into another party's data
- **Multi-party authorization envelopes** — for high-stakes operations; chain entry carries every contributing identity

## Consumers

| Consumer | What they do with this card |
|---|---|
| Substrate / database design sessions | Reference for the tenant-scoped schema and the RLS policy design — every record carries `party_id` and `party_type` |
| Future SDDs touching identity, access, or authorization | The party taxonomy is the canonical reference; new SDDs cite this card rather than re-defining parties |
| Loss-prevention substrate productization ([[lp-device-intelligence-substrate]]) | The Investigator party type is what legitimizes marketplace observation under retailer authorization |
| Compliance and legal review (HIPAA, PCI DSS, GDPR posture) | The party taxonomy is what regulators and counsel will reference for "who can see what under what authority" |
| Investor and partner conversations about platform safety | The taxonomy is the surface that explains how the platform handles auditors, investigators, and agents distinctly — defensibility against generic "AI safety" worries |
| ALX self-recall in future sessions | When designing a new feature or surface, the party taxonomy is the lens for "which parties touch this surface and what is each one's scope" |

## Sources

| Source | Role |
|---|---|
| [[2026-05-02-platform-trust-boundary-architecture]] | The originating SDD where the taxonomy was first codified |
| [[concept-identity-layer-triad]] | Substrate identity model and consent contract architecture the taxonomy operates within |
| [[platform-thesis]] | Three accountability rails plus vendor accountability — rail alignment derived from here |
| [[2026-05-02-agent-commissioning-protocol]] | Source for the MCP-agents party type's substrate primitives |
| [[lp-device-intelligence-substrate]] | First product application that depends on the auditor/investigator distinction being substrate-level |
| Cowork session 2026-05-02 conversation log | The session in which the taxonomy was named (founder insight: "register the device with a known party in our system customer vendor consumer auditor investigator amcp agents") |

## Invariants

Hard constraints. These keep the taxonomy meaningful.

1. **Every authenticated caller resolves to exactly one party type.** No mixed types, no "kind of customer kind of vendor." If a real-world entity wears multiple hats (e.g., a clinic owner who is also a retail operator), they have multiple party identities in the substrate, joined by the [[concept-identity-layer-triad|identity-layer triad]]'s consent-based projection.
2. **Auditor and Investigator are distinct party types and never conflated.** Standing scope vs time-bounded scope is the distinction; collapsing them breaks the evidentiary rail.
3. **MCP Agents is a first-class party type, not a system primitive.** Agents are treated as parties in the substrate — devices, identities, capability tiers, evidence-chain anchored actions. Treating them as anything less degrades the evidentiary rail.
4. **No facial recognition. No facial image gathering.** Per the platform's harmful-content posture and the [[lp-device-intelligence-substrate]] invariants. Party identity is commercial-relational identity, not biometric identity.
5. **The taxonomy is exhaustive at the substrate level.** New party types require substrate-level review and a new card; ad-hoc party types are not permitted in implementation.
6. **Cross-tenant access by any party type is an architectural event.** Auditors with framework grants, investigators with authority instruments, MCP agents with explicit dispatch scope. The substrate logs and anchors every cross-tenant access; nothing crosses silently.

## Related

- [[2026-05-02-platform-trust-boundary-architecture]] — the originating SDD; full per-party authentication mechanism, device registration, attestation depth ladder
- [[2026-05-02-agent-commissioning-protocol]] — the MCP Agents party type's commissioning lifecycle
- [[concept-identity-layer-triad]] — the identity model the taxonomy operates within (substrate-layer identity record + consent contracts + per-vertical projections)
- [[concept-substrate-discipline]] — fractal rule that keeps the taxonomy portable across protocol altitudes
- [[concept-agent-parenting-discipline]] — worldview that produces the substrate primitives for the MCP Agents party type
- [[lp-device-intelligence-substrate]] — first product application depending on the Investigator party type
- [[agent-auditor]] — first agent commissioned under the MCP Agents party type
- [[platform-thesis]] — three accountability rails plus vendor; rail alignment derived from here
- [[platform-gateway-thesis]] — the substrate frame the taxonomy lives within

---

*Captured 2026-05-02 by ALX (Cowork session). One concept per card — six party types, one substrate, distinct permissioning per party, evidentiary chain anchored to party identity. Founder gate: confirm the auditor/investigator distinction is correct framing before any compliance, regulatory, or legal review references this card as canonical.*
