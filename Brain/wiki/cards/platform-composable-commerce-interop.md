---
card-type: platform-thesis
card-id: platform-composable-commerce-interop
card-version: 1
domain: platform
layer: cross-cutting
agent: ALX
status: draft
last-compiled: 2026-05-07
needs-review: 2026-06-15
tags: [composable-commerce, mach-alliance, interop, adapters, hexagonal, schemas, openapi, graphql, asyncapi, cloudevents, gs1, arts, codegen, contracts]
related: [axis-adapter, canary-go-endpoint-library, platform-stack-commitment, competitive-landscape, canary-architecture]
---

# Composable Commerce Interop Posture

## What this is

Canary's stance on the MACH Alliance / composable commerce ecosystem. Specifically: how Canary connects to commercetools, Saleor, Shopify, BigCommerce, Akeneo, Algolia, Fluent Commerce, and the next ten platforms that haven't shipped yet — without letting any of their schemas leak into Canary's domain model.

## Governing thesis

**Canary speaks composable commerce schemas at the edge; Canary's core stays ARTS.** The MACH world built schemas for D2C ecommerce; Canary's domain is the physical store and its operator. Conformance to commercetools or Saleor would be a downgrade — ARTS is the more rigorous model, and most composable schemas are subsets of it. The right posture is **adapter ports, not domain conformance**: every supported partner gets a translation layer in `internal/adapters/<partner>/`, the core domain in `internal/domain/` stays clean, and partner schemas never leak past the boundary. This is hexagonal architecture applied at the integration surface — the same pattern already governing Axis A (POS Adapter Substrate); we extend it to Axis B (Resource APIs) and Axis C (Agent Surface) for composable commerce partners.

## Why this matters now

Three forces converge on this decision:

1. **Endpoint commitments are imminent.** Canary's [[canary-go-endpoint-library|endpoint library]] already exposes a 32-service REST surface on Axis B. As partners integrate, they will arrive with composable-commerce-shaped expectations — GraphQL queries mirroring commercetools, webhook payloads in CloudEvents format, OAuth 2.0 client credentials flow. Without a posture in writing, ad-hoc decisions accrete and the domain pollutes.
2. **The MACH ecosystem is the de facto interop vocabulary** for any retail platform with a digital channel adjacent to it. Even ICP shops on NCR Counterpoint increasingly run Shopify, BigCommerce, or a headless storefront somewhere upstream. We cannot pretend that surface area away.
3. **ARTS is the moat.** Conformance pressure pushes platforms toward whichever schema is loudest. Canary's defensibility depends on staying ARTS-native at the core while being polyglot at the edge. The discipline only holds if it's encoded.

## Schema tier — what we speak, in priority order

Three tiers. Tier 1 is non-negotiable; Tier 2 is opportunistic; Tier 3 is tracked but not implemented.

| Tier | Schema | Why | Implementation cost |
|---|---|---|---|
| **1** | **commercetools API** (REST + GraphQL) | De facto MACH reference; partner expectations are shaped like this | Vendored OpenAPI + GraphQL SDL; adapter package |
| **1** | **Saleor GraphQL schema** | Open source equivalent; vocabulary reference for product/order/customer | Vendored SDL; adapter package |
| **1** | **GS1** (GTIN, GLN, SSCC, GS1 Digital Link) | Already required for retail interop; non-negotiable | Already partial; harden coverage |
| **1** | **CloudEvents 1.0 + AsyncAPI 2.x/3.x** | The async transport everyone aligns on | Adopt as outbound event envelope |
| **1** | **OAuth 2.0 / OIDC / JWT** | Service-to-service auth standard | Already present; verify coverage |
| **2** | **MACH Alliance Reference Architecture** | Thin but real OpenAPI specs; cheap alignment | Cross-reference, no separate adapter |
| **2** | **GS1 EPCIS 2.0** | Supply chain events; matters as receiving and traceability deepen | Map to existing receiving events |
| **2** | **Schema.org Product / Offer / Order** | SEO and feed exchange | Generate from product API |
| **2** | **Shopify Admin / Storefront API** | Not MACH-pure, but ICP shops have Shopify upstream more often than commercetools | Adapter package on demand |
| **3** | **Open Retail Data Model**, **OpenTrade**, **Open Commerce** | Too early to bet on | Track, don't implement |
| **3** | **OAGIS BODs** | Heavyweight; only matters if/when enterprise lane opens | Track, don't implement |

## The architectural rule — hexagonal boundary

The non-negotiable, encoded as a code-organization rule:

```
internal/
├── domain/              ← ARTS-aligned types; partner schemas FORBIDDEN here
├── adapters/
│   ├── commercetools/   ← inbound + outbound translation
│   ├── saleor/
│   ├── shopify/
│   └── <partner>/
└── ports/               ← interfaces the adapters implement
api/
├── openapi/             ← Canary's own OpenAPI (source of truth)
├── graphql/             ← Canary's own GraphQL SDL
├── asyncapi/            ← event schemas (CloudEvents envelope)
└── vendored/
    ├── commercetools/   ← partner schemas, version-pinned
    ├── saleor/
    └── <partner>/
gen/                     ← code-generated; .gitignored or CI-checked
```

Three rules enforce this:

1. **No partner type may appear in `internal/domain/`.** A `commercetoolsCustomerId` field on the customer aggregate is a bug. External IDs go in a generic `ExternalReferences` map keyed by partner name.
2. **Adapters are ports, not parts of the domain.** Translation happens in `internal/adapters/<partner>/`. A handler that reaches into a commercetools-shaped payload directly is a bug — it must go through the adapter.
3. **Generated code is consumed at the adapter, not the domain.** `oapi-codegen` output for commercetools lives next to the commercetools adapter; the domain never imports `gen/commercetools/...`.

This is the same pattern as Axis A's [[axis-adapter|POS Adapter Substrate]] — extended to outbound and partner-bidirectional surfaces.

## Go codegen toolchain — the decision

The "library" question — what we actually have on hand:

| Concern | Tool | Rationale |
|---|---|---|
| OpenAPI → Go server/client | **`oapi-codegen`** (deepmap) | Mature, broad ecosystem; `ogen` is sharper but smaller community |
| GraphQL server | **`gqlgen`** (99designs) | Schema-first; matches our "spec is source of truth" posture |
| GraphQL client (typed queries against partners) | **`genqlient`** (Khan Academy) | Typed query generation; clean against Saleor/commercetools SDLs |
| AsyncAPI / CloudEvents | **CloudEvents Go SDK** + hand-rolled AsyncAPI codegen | Codegen ecosystem still thin; SDK is solid |
| Protobuf / gRPC (internal service mesh) | **`buf`** | Lint, breaking-change detection, registry |
| Schema registry | **Buf Schema Registry** (or self-hosted Apicurio if cost matters) | Versioning + breaking-change gates |
| Contract testing | **Pact-Go** for consumer-driven contracts; **`dredd`** for OpenAPI conformance | Catch drift in CI before partners do |
| JSON Schema validation at boundaries | **`gojsonschema`** or **`jsonschema/v5`** | Boundary defense |

This is not a wishlist — it is the committed toolchain. Drift requires an explicit decision, not vibes.

## Non-negotiables — the "we always speak X" list

Independent of partner, these are baseline competencies for any Canary endpoint:

- **GS1 identifiers** (GTIN, GLN, SSCC) parse and round-trip without loss
- **OAuth 2.0 / OIDC** for inbound and outbound service auth; client credentials flow on Axis B
- **CloudEvents 1.0** envelope on every published async event
- **OpenAPI 3.1 spec** for every Resource API endpoint
- **AsyncAPI 2.x or 3.x** spec for every event publication
- **Idempotency-Key** header honored on every state-changing endpoint
- **ETag / If-Match** on every mutable resource
- **Cursor-based pagination** (`page[after]`, `page[size]`) — no offset pagination on Axis B
- **ISO 8601 UTC** for every timestamp; no local time anywhere
- **RFC 7807 Problem Details** for every error response

## What this is not

To prevent scope creep — three things this card explicitly does not commit to:

- **Becoming a commercetools-shaped commerce engine.** Canary is not a cart, not a checkout, not a storefront. We integrate; we don't impersonate.
- **Joining the MACH Alliance.** Membership is a marketing decision evaluated separately; this card is about technical posture only.
- **Building all Tier 1 adapters speculatively.** Adapters are demand-driven — first commercetools deal triggers the commercetools adapter, not the reverse. The infrastructure (codegen pipeline, vendored specs, port interfaces) is built up front; specific adapters land per integration partner.

## Anti-patterns

The trap is partner-schema leakage. Specific failure modes to refuse:

- A `customer.commercetoolsId` field added "just for now"
- A handler that pattern-matches a Saleor GraphQL response shape directly
- An event schema that carries both internal and partner fields because translation feels like overhead
- A vendored partner spec edited locally to "fix" something — vendored specs are read-only artifacts; if a partner's spec is wrong, file an upstream issue or write a translation rule
- A core domain method that takes a `*commercetools.Order` argument

If any of these ship, the card has been violated and the domain needs immediate cleanup.

## See also

- Card: [[axis-adapter]] — the inbound POS adapter substrate this generalizes
- Card: [[platform-stack-commitment]] — vendor commitment posture; codegen tools are commodity SaaS plumbing under that rubric
- Card: [[competitive-landscape]] — five-lane map; composable commerce vendors sit in Lane 1 and Lane 4
- Wiki: [[canary-go-endpoint-library]] — three-axis endpoint library this card governs the interop posture for
- Wiki: [[canary-architecture]] — overall Canary Go architecture
- External: [MACH Alliance Reference Architecture](https://machalliance.org/) · [commercetools API docs](https://docs.commercetools.com/) · [Saleor schema](https://github.com/saleor/saleor)

## Linear

GRO issue tracking the implementation of this posture: see Canary.GO project, "Establish composable commerce interop posture and adapter scaffolding."
