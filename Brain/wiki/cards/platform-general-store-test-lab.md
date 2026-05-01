---
card-type: platform-thesis
card-id: platform-general-store-test-lab
card-version: 1
domain: platform
layer: front-end
status: approved
agent: ALX
tags: [general-store, test-lab, front-end-requirements, murdochs, recon, module-s, episerver, constructor-io, bopis, map-pricing, dual-keyed-item-master]
last-compiled: 2026-04-29
needs-review: false
---

## What this is

The Murdoch's site reconnaissance (commit `e2a5578`, 2026-04-29) is the front-end requirements baseline for the **General Store** — Canary's reference storefront / test lab. The recon is no longer just evidence for Module S; it is the canonical specification for what a Counterpoint-backed specialty retailer storefront must do, observable in production at a 47-store, 40,774-URL chain.

## Why this matters

Front-end requirements, until now, have been derived from architecture documents and vendor positioning. The Murdoch's recon replaces inference with observation. Every behavior the General Store must support is something a real Counterpoint-backed retailer has already shipped to customers — at scale, in production, today. The recon is the ground truth; the General Store is the agent-native rebuild.

## The General Store

The General Store is Canary's internal reference storefront — the test lab where front-end behaviors are exercised, regressions are caught, and the agent-native experience is demonstrated. It is what we point a partner to when they ask "show me what this looks like for a customer." It is also what Module S (Storefront), Module D (Inventory), and Module P (Pricing) must collectively render correctly.

## Front-end requirements derived from the Murdoch's recon

| Behavior | Observed at Murdoch's | General Store implication |
|---|---|---|
| 4-tier merchandise hierarchy | Sitemap depth 6 (4 levels of categorization before SKU slug) | Hierarchy navigation, breadcrumbs, and PLP filters all support 4 tiers minimum |
| Dual-keyed item master visible to customer | PDP prints `SKU # 9390357` and `MPN # 190424` side-by-side; GA4 ships `idFOGR_190424` | PDP component renders both identifiers; manufacturer code is first-class |
| Two-fulfillment-path UI | Every PDP exposes SHIP IT and Find in a Murdoch's store as parallel paths | Cart and PDP support delivery + BOPIS as peer paths, not delivery-default with BOPIS-fallback |
| MAP-gated pricing | ~9% of catalog (358 SKUs) hides price; `clickToViewPriceCuratedProduct` global controls reveal | Price component supports gated state, click-to-reveal interaction, MAP rule attached to SKU at render time |
| Manufacturer prefix taxonomy in image paths | Image URLs encode `f-manu/fogr/`, `r-manu/rega/`, etc. | Asset path convention uses derivable manufacturer master; no per-asset metadata lookup at render |
| Search/recs as separate vendor surface | Constructor.io fires `ac.cnstrc.com/v2/behavioral_action/*` on every PLP interaction | Search/recs is a swappable substrate; the General Store renders a search interface, not a search vendor |
| Lifecycle/email beacon on every PDP | Listrak activity beacon fires on every product view | Front-end emits structured product-view events; lifecycle vendor is downstream |
| Heavy seasonal-seed catalog | Botanical Interests + Renee's Garden = 28.5% of L&G catalog | Seasonal merchandising patterns are first-class; PLP supports time-window-bound listings |
| Orphan SKU paths (sitemap drift) | 4 PDPs sit at `/products/` instead of nested category path | Routing tolerates flat product URLs alongside nested category paths |
| Anti-bot at request layer | BrandLock beacon every page | Front-end coexists with anti-bot middleware without breaking server-rendered fallback |
| 10+ tracking pipelines | GA4, Bing UET, FB Pixel, Pinterest, TheTradeDesk, Quantcast, DoubleClick, Microsoft Clarity, Application Insights, Google Merchant Center | Tag manager / event bus pattern, not per-vendor inline integration |
| Server-rendered .NET CMS | Episerver/Optimizely | Counterpart on Canary side is server-rendered Go; SPA-only is wrong for this market |

## What the General Store is NOT

- Not a clone of Murdoch's. The recon is requirements, not visual reference.
- Not a Murdoch's pitch deck artifact. It is an internal test lab and reference; the Murdoch's-specific framing stays in `Brain/raw/inbox/murdochs/` and the proof case.
- Not the production Canary storefront. The General Store exercises the platform's front-end primitives; production deployments customize on top of the same primitives.

## Test lab usage

Every front-end behavior in the recon becomes a regression target in the General Store:

1. Render a 4-tier hierarchy and verify breadcrumbs/PLP filters resolve at every depth
2. Render a dual-keyed PDP and verify SKU + MPN are both queryable
3. Toggle a SKU into MAP-gated state and verify the click-to-reveal renders correctly
4. Render a SHIP IT + BOPIS PDP and verify both paths reach the cart
5. Inject 4 orphan SKUs at `/products/<slug>/` and verify routing
6. Fire a product-view and verify the event bus delivers to all configured downstream sinks

These are the test cases the recon underwrites. Each failure surfaces a Module S, Module D, or Module P specification gap.

## Open follow-ups (from the recon manifest)

- BOPIS inventory-by-store XHR contract — highest-priority gap (request/response shape, refresh cadence, qty granularity)
- Reviews vendor — wired but unobserved; need a high-review SKU page-load capture
- MAP pricing trigger — what conditions cause a SKU to gate price?
- Per-store amenities and hours — separate per-store crawl needed
- Counterpoint endpoint cross-walk — every observed shape mapped to its REST API equivalent

These follow-ups are the General Store's outstanding requirements gaps.

## Related

- [[Brain/wiki/murdochs-ranch-home-supply-proof-case|Murdoch's — Proof Case]]
- [[Brain/wiki/counterpoint-market-gtm-proposal|Counterpoint Market GTM Proposal]]
- [[Brain/wiki/cards/icp-murdochs-reference|Murdoch's ICP Reference Card]]
- `Brain/raw/inbox/murdochs/_manifest.md` — recon manifest (commit `e2a5578`)
- `Brain/raw/inbox/murdochs/site-map/feature-inventory.md` — full stack/feature breakdown
- `Brain/raw/inbox/murdochs/site-map/gateway-architecture.md` — slip-in plan with diagrams

## Sources

- Murdoch's catalog & site map recon (commit `e2a5578`, 2026-04-29) — 40,774 URLs, 4,021 PDPs, 47 stores, full stack/feature inventory
