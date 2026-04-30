# Murdoch's Storefront — Feature Inventory

Cross-cutting capabilities observed during the 2026-04-29 reconnaissance. Each entry: what we see, what stack drives it (with evidence-confidence), and what request shape we observed.

## Search & faceting

**Vendor: Constructor.io** — confirmed, high confidence.

Every facet element on `/products/lawn-garden/` carries a `cio-*` class prefix: `cio-filters`, `cio-filter-group`, `cio-filter-multiple-option`, `cio-filter-option-name`, `cio-filter-option-count`. The Constructor.io React SDK renders the entire faceted browse experience client-side, hydrating an SSR shell. On PDP load we directly captured `POST ac.cnstrc.com/v2/behavioral_action/item_detail_load` with API key `key_eN0Z5gklJfTKN3qm`. The runtime endpoint pattern is `ac.cnstrc.com/v2/behavioral_action/{action}`.

Implication: Murdoch's catalog is *indexed* by Constructor.io. The catalog feed flowing into Constructor.io is a critical integration point — currently presumably served from Murdoch's Episerver/PIM layer.

## Geolocation & store selector

**Vendor: in-house, SSR-injected.** No XHR.

The store list on `/stores/` is delivered as a JavaScript object literal in an inline `<script>` block: `var svmObj = {stores: [...47 stores...], stateGroups: [...]}`. Full address, phone, lat/lng, and `comingSoon` flag for every store. Plus a `chooseAStoreServerSideViewModel` global with `selectedStoreNumber`, `murdochsRegionDistanceThreshold: 300` (miles), and `freeInStoreComingSoon`.

Geolocation calculation runs client-side via the `GeoLocationCalculator` global. Map view uses Google Maps JS (`maps.googleapis.com/maps-api-v3/...`).

## Inventory by store

**Status: not captured this session.** UI workflow confirmed.

PDP shows a "Find in a Murdoch's store" link that opens a dialog with a ZIP/city search field (`txtFindQuery`, form `searchAddressForm`, first field name `cityOrZipCode`). Clicking the search button closed the dialog without surfacing the inventory XHR in our network monitor — likely intercepted by a service worker, or fired before the monitor's window opened, or used a fetch the extension can't intercept on certain page types. This is the highest-value first-party endpoint we did not capture and should be the priority for a follow-up session.

## Fulfillment options

**Two-path model confirmed.** PDP visible UI shows:

- **"SHIP IT"** primary CTA (with "Deliver to Address" sub-label) — direct ship-to-home flow
- **"Find in a Murdoch's store"** secondary link — BOPIS / in-store check flow

Two distinct fulfillment paths, exposed at the SKU level on every PDP.

## Recommendations

**Vendor: Constructor.io.** Same SDK as search/PLP. Behavioral tracking on PDP fires `item_detail_load` action which feeds their recs engine. Recommendation rendering (e.g., "You might also like") was not directly observed — likely a separate `cio-*`-classed widget below the fold.

## Reviews & UGC

**Status: wired but not observed firing.** PDP visible UI shows "(0)" star rating + "Write a review" link. No review-platform XHR captured on the sample PDP (which has 0 reviews). Likely vendor: BazaarVoice or PowerReviews — confirm by inspecting a PDP that has reviews loaded (not in our sample).

## Cart persistence

**Status: not observed.** Did not exercise add-to-cart per dispatch constraints (no auth flows, no checkout). Cart persistence model (anonymous cookie vs logged-in token) unconfirmed.

## Loyalty / rewards

**Visible: "Rewards" link in utility nav** pointing to `/services/rewards/`. Sticky promotional CTA on PDP "Get 10% Off*" is a Listrak personalization rule, not the rewards program itself. Rewards mechanics not investigated.

## Email / lifecycle marketing

**Vendor: Listrak.** High confidence. Three personalization rule files fetched from `t.lt02.net/pf/805b69a5-e16a-4c23-9124-3c6fa5cc4274/<rule-uuid>.json` on PDP load, plus an activity beacon to `webcontent-activity.listrak.com/Activity/<token>`. The "Get 10% Off*" floating CTA is a Listrak browse-abandonment / first-visit acquisition rule.

## Live chat

**Vendor: 3CX.** Surfaced via a script load `downloads-global.3cx.com/downloads/livechatandtalk/v1/callus.js` (visible in BrandLock's payload report). 3CX is a small/mid-market PBX + chat platform — uncommon choice for a $XXM retailer; suggests a deliberate cost-conscious or legacy decision.

## Bot detection / anti-fraud

**Vendor: BrandLock.** Beacons fire on every observed page to `portal.brandlock.io/?hit=<encoded_payload>` carrying a 90+ feature vector (timing, interaction patterns, device fingerprint), session/visit IDs, and `web_id: 475`. Aimed at scraper deflection and account-takeover protection.

## Consent management

**Vendor: CookieYes.** Tenant ID `c9fc9914f81130b0a384697bd278a742`. Consent banner JS, audit table, IP-based geo decision (`directory.cookieyes.com/api/v1/ip`), translations, and consent log are all CookieYes-served. CCPA "Do Not Share My Personal Information" link visible bottom-left.

## Asset CDN / image optimization

**Vendors: Yottaa (full-page perf optimization) + their own globalassets path.** Yottaa is referenced in robots.txt (`/yottaa.service.worker.js`) — full-page optimization vendor. Image URLs follow pattern `/globalassets/hlr-system/product/hard-goods/manufacturer/{f-manu-prefix}/{vendor-code}/products/{slug}.png`. The `f-manu/fogr/` segment is a manufacturer code namespace — `fogr` = "Fogr" brand prefix, matching the `FOGR_190424` MPN we saw in GA4. Their PIM/asset taxonomy is keyed on manufacturer.

## Tracking & analytics

Heavy. Every page fires:

- **GA4** (G-GY9KCXQ44W) with enhanced ecommerce
- **Google Merchant Center conversion** (MC-16RCRTRCFN)
- **Bing UET** (4049525)
- **Facebook Pixel** (715694765179509)
- **Pinterest tag**
- **TheTradeDesk** (insight.adsrvr.org/track/realtimeconversion)
- **Quantcast** (p-h0Uy1gWhZj5Eq)
- **DoubleClick floodlight** + Google rmkt + 1p-user-list
- **Microsoft Clarity** (session replay/heatmaps)
- **Application Insights** (Microsoft Azure server-side telemetry)

That's 10+ tracking pipelines simultaneously — aggressive martech stack typical of mid-market retail running heavy paid acquisition.

## Internal Murdoch's-built service (anomaly)

**Host: `mbzaubiphz.us-west-2.awsapprunner.com`** — anonymous AWS App Runner hostname, single observed endpoint `/events/{hash}`, POST with 503 response. This is the *only* first-party-shaped Murdoch's API surface we captured. Could be:

- Behavioral telemetry sink (likely)
- Loyalty/rewards events
- Internal experimentation tool

Worth chasing in follow-up. It's the lone non-vendor first-party endpoint surfaced.

## Pricing — MAP enforcement signal

Window global `clickToViewPriceCuratedProduct` on PLP suggests **MAP pricing** (Minimum Advertised Price): some SKUs from price-controlled brands hide their price behind a click-to-reveal interaction to comply with vendor MAP policies. Logic and trigger conditions unobserved but the global's existence is unambiguous evidence the pattern is in their model.

## Item master — dual-keyed (the big one)

The PDP visible UI prints both:

- **SKU # 9390357** (POS SKU, matches JSON-LD `offers[].sku`)
- **MPN # 190424** (Manufacturer Part Number)

GA4 enhanced ecommerce ships `pr1=idFOGR_190424` — vendor code `FOGR` + MPN `190424`. Image asset path includes `f-manu/fogr/`. Three independent surfaces (visible UI, analytics payload, asset taxonomy) confirm a dual-keyed item master where the manufacturer code and the POS SKU are both first-class identifiers. This maps directly to Counterpoint's `IM_ITEM.ITEM_VEND_NO` field — Murdoch's already operates this pattern in production.
