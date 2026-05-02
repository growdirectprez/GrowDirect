---
card-type: infra-capability
card-id: infra-dns-topology
card-version: 1
domain: platform
layer: infra
status: draft
last-compiled: 2026-05-03
needs-review: true
agent: ALX
feeds:
  - platform-gateway-thesis
  - website-canary-launch
  - canary-go-deployment
receives:
  - platform-gateway-thesis
  - concept-substrate-discipline
  - mission-main-street
tags:
  - dns
  - domain-topology
  - eljeffe-io
  - growdirect-io
  - canary-api
  - tenant-subdomain
  - substrate-discipline
  - cloudflare
  - apache-2
---

# DNS / Domain Topology — Substrate Discipline at the URL Layer

## What this is

The domain architecture for GrowDirect — four domains, three concerns, one substrate-discipline rule. The protocol lives at one root because it is a namespace; consumers live at peer subdomains under it because they are tenants. Same fractal rule that governs the substrate spec ([[concept-substrate-discipline]]) applied at the DNS layer.

## Purpose

Every URL the founder gives a partner, integrator, or Square reviewer is a small architectural statement. If integrators paste `canary.growdirect.io/api` into their code, the URL says *Canary is a GrowDirect product surface — when the contract changes, ask GrowDirect.* If they paste `canary.api.eljeffe.io`, the URL says *Canary is one tenant of a published protocol — when the contract changes, the protocol changes for everyone.* The first reading sells lock-in; the second reading sells substrate access. The platform's mission ([[mission-main-street]]) requires the second reading. The DNS topology is one of the architectural surfaces that has to carry it.

## Structure — four domains

| Domain | Carries | Role | Status (2026-05-03) |
|---|---|---|---|
| **`growdirect.io`** | Company surface — portfolio, mission, investor, contact, hiring | Corporate identity. Not the protocol. Not a product. The **Mission layer** (Layer 1 of the brand stack). | Owned · live |
| **`eljeffe.io`** | Protocol surface — TSP / .jeffe namespace / ARTS spec / Apache 2.0 LICENSE / reference implementation | The substrate's home. Apache 2.0 publication lives here. The **Open protocol layer** (Layer 2 of the brand stack). | Owned · DNS posture not yet captured (see related GRO) |
| **`api.eljeffe.io`** | The protocol's API surface | Tenant subdomains hang off this. Wildcard cert covers the tree. Where the **Canary operation** (Layer 3) is reached. | To configure |
| **`{tenant}.api.eljeffe.io`** | One consumer's projection of the protocol API | First tenant: `canary.api.eljeffe.io`. Future peers: `cove.api.eljeffe.io`, `angel.api.eljeffe.io`, partner-tenant subdomains (`rapidpos.api.eljeffe.io`, etc.). The **Proof case layer** (Layer 4) and **Future verticals layer** (Layer 5). | First tenant locked: `canary.api.eljeffe.io` |

Subdomains read right-to-left in *decreasing* scope, so `canary.api.eljeffe.io` literally reads "Canary's slice of the eljeffe.io API." The URL itself encodes substrate discipline. When a partner shop wants to consume the substrate, they get `partner-name.api.eljeffe.io` at the same altitude — equal footing, no `/partners/canary/` path-prefix that buries them under Canary. Open-protocol commitment becomes visible in DNS, not just in copy.

## Why this ordering (and not the alternatives)

| Pattern | Reads as | Architectural signal |
|---|---|---|
| **`canary.api.eljeffe.io` (chosen)** | "Canary's slice of the eljeffe.io API" | Substrate-disciplined. URL says protocol is bigger than any one tenant. |
| `api.canary.eljeffe.io` | "the API of canary on eljeffe" | Positions canary as a brand-product on the eljeffe protocol — closer, but still implies Canary owns the API. |
| `api.canary.io` | Standalone brand surface | Hides the substrate entirely. Sells lock-in. Contradicts the open-protocol commitment ([[platform-gateway-thesis]]). |
| `canary.growdirect.io/api` | Path-prefixed under company surface | Conflates company-marketing and protocol-API concerns. Contradicts substrate discipline at the DNS layer. |

The chosen pattern is the only one of the four that survives substrate-discipline review. The rest leak company-or-product policy into the protocol surface.

## Tradeoff — brand visibility

**Real friction worth naming.** When a Canary integrator pastes `canary.api.eljeffe.io` into their integration code, they read "eljeffe.io" not "canary.com" or "growdirect.io." Two readings:

- **Embraced:** the integrator immediately understands Canary is on a protocol they could implement themselves. The open-protocol pitch landing in the DNS bar.
- **Friction:** a less-savvy developer wonders "wait, why am I hitting eljeffe.io?" and emails support.

The mitigation is documentation, not domain re-architecture. Don't move the URL to hide the substrate; that contradicts the mission. Solve the friction with a one-paragraph "why eljeffe.io" callout in the API docs and on the canary.growdirect.io product page.

## Operational implications

| Concern | Decision | Notes |
|---|---|---|
| DNS hosting | Confirm `eljeffe.io` is on Cloudflare; if not, decide whether to migrate or run split-horizon | See related GRO |
| TLS cert for tenants | Wildcard on `*.api.eljeffe.io` via Let's Encrypt DNS-01 challenge | Cloudflare's DNS API makes DNS-01 trivial; ~10 minutes once we can manage records |
| Repo split for protocol | Eventually `github.com/growdirectprez/eljeffe` carries the spec + LICENSE + reference impl | Apache 2.0 publication ([[platform-gateway-thesis]] v3) makes that repo the canonical artifact. Not blocking website v1.0. |
| Routing for `canary.api.eljeffe.io` | One Canary Go service backing the subdomain via Cloud Run / GKE / equivalent; substrate code is shared, tenant subdomain is a routing concern | See `docs/sdds/go-handoff/` |
| MCP for ongoing DNS management | Cloudflare GraphQL or DNS Analytics MCP install reserved; not in registry today; install path is `developers.cloudflare.com/agents/model-context-protocol/` | Path-of-least-resistance until install: dashboard or curl with Zone:Read API token |
| Email | `*@growdirect.io` already operational; no email under `eljeffe.io` for now (protocol root, not a contact surface) | Defer until a partner asks |

## Consumers

| Consumer | What they do with this card |
|---|---|
| Website build (v1.0) | `/gateway` page hero references `eljeffe.io` as the published-protocol home; `canary.growdirect.io` product page references `canary.api.eljeffe.io` as the integration endpoint |
| Canary Go deployment SDD | Tenant routing for `canary.api.eljeffe.io`; substrate vs tenant separation in the deployment topology |
| Partner conversations (Bart, Square, future Counterpoint VARs) | Equal-footing subdomain pattern is the architectural answer to "what would my shop's surface look like?" |
| LICENSE file work (next session) | Apache 2.0 publication lives at `eljeffe.io` repo root; this card sets the URL where the spec is canonical |
| Future tenants (cove, angel, partner shops) | Pattern is `{tenant}.api.eljeffe.io` — peer-level, not nested |

## Sources

| Source | Role |
|---|---|
| `Brain/wiki/cards/platform-gateway-thesis.md` | Five-layer brand stack that this DNS topology projects onto |
| `Brain/wiki/cards/concept-substrate-discipline.md` | The fractal rule applied at the DNS layer |
| `Brain/wiki/cards/mission-main-street.md` | Civic mission that requires substrate-disciplined URLs |
| `docs/_archive/ip-vault/strategy/GrowDirect_Manifesto_v1.1.md` §V.9 | .jeffe namespace as identity layer — the architectural origin of `eljeffe.io` as the protocol root |
| Cowork session 2026-05-03 | Founder's articulation of the topology + Apache 2.0 license decision (committed in chain `8297df3`) |
| Cloudflare developer-platform MCP probe (this session) | Account inventory: 1 Worker (`abalonecove-chat`), 2 KV namespaces, no R2; no Canary or growdirect.io infra on Cloudflare today |

## Invariants

1. **Protocol root and corporate root are separate domains.** `eljeffe.io` carries the protocol; `growdirect.io` carries the company. Never collapse them.
2. **Tenant subdomains are peer-level under `api.eljeffe.io`.** No path-prefix nesting (`api.eljeffe.io/canary/...`), no Canary-favoring (`canary.api.eljeffe.io` and `partner.api.eljeffe.io` sit at the same altitude).
3. **The protocol surface does not know which tenant is calling at the URL level.** Tenant scope is a routing concern carried by the subdomain; the underlying substrate code is shared. (Substrate discipline: substrate carries data and intersections; tenant identity is a meaning-layer concern.)
4. **No tenant subdomain is added without a corresponding substrate consumer record.** The DNS record is the visible signal; the underlying tenant-of-the-protocol contract is the architectural commitment.
5. **License posture follows the protocol root.** Apache 2.0 LICENSE lives at the `eljeffe.io` repo root and on each published spec file. It does not need to repeat at every tenant subdomain — the tenant inherits the license posture from the protocol it consumes.
6. **Capability language only on public-facing DNS-adjacent copy.** Same invariant as the gateway thesis ([[platform-gateway-thesis]] invariant #6) — public copy that talks about the URLs uses *protocol*, *substrate*, *open spec*, *tenant*, not Bitcoin/L402/satoshi terminology.

## Open questions (track via related GRO)

| # | Question | Resolution path |
|---|---|---|
| OQ-1 | Is `eljeffe.io` on Cloudflare DNS, or at a different registrar? | Dashboard check or Cloudflare DNS MCP install |
| OQ-2 | Wildcard cert provisioning path: Cloudflare-issued vs Let's Encrypt DNS-01 vs a tenant-per-cert pattern? | DevOps decision once DNS posture is captured |
| OQ-3 | Repo split for `eljeffe.io` published spec — when, and what stays in the GrowDirect repo vs splits out? | Next-session build planning; not blocking website v1.0 |
| OQ-4 | Cloudflare DNS / Zone management MCP — install Cloudflare's GraphQL server, or wait for the registry to surface a DNS-capable connector? | Cost/benefit; install if DNS work becomes recurring |

## Related

- [[platform-gateway-thesis|Platform Gateway Thesis]] — five-layer brand stack this DNS topology projects onto
- [[concept-substrate-discipline|Substrate Discipline]] — the fractal rule applied here
- [[mission-main-street|Mission · Main Street]] — civic mission requiring substrate-disciplined URLs
- [[concept-decision-substrate|Decision Substrate]] — runtime calls vs session threads (the API surface this DNS topology fronts)
- [[concept-identity-layer-triad|Identity Layer Triad]] — health · voting · spend across the same DNS topology
- [[infra-blockchain-evidence-anchor|Blockchain Evidence Anchor]] — evidentiary rail substrate (architecture-only language; surfaced at `eljeffe.io` as spec, at `*.api.eljeffe.io` as runtime endpoint)

---

*Captured 2026-05-03 by ALX (substrate captures session, end-of-session). Founder confirmed `eljeffe.io` ownership; DNS posture (which records exist, which registrar) not captured this session — see related GRO for the follow-up. Card supersedes any prior implicit topology decisions; future DNS additions ladder onto this card.*
