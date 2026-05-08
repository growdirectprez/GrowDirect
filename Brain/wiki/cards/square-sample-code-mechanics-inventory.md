---
last-compiled: 2026-05-08
needs-review: false
type: reference
status: active
tags: [square, sample-code, oauth, catalog, webhook, csv, scan, mechanics, inventory, accelerator, canary-go]
created: 2026-05-08
gro: GRO-881
sources:
  - https://github.com/square/connect-api-examples
  - https://developer.squareup.com/reference/square/catalog-api/batch-upsert-catalog-objects
  - https://developer.squareup.com/docs/webhooks/step3validate
  - https://developer.squareup.com/docs/build-basics/general-considerations/handling-errors
  - https://squareup.com/help/us/en/article/6172-import-item-library-troubleshooting
---

# Square Sample-Code Mechanics Inventory

A reference list of Square sample-code patterns Canary can lift directly into the item-setup build (and adjacent surfaces). **Mechanics only** — the parts of seller-facing UX where merchant complexity doesn't differentiate. Patterns specific to Square's data model that would mis-shape Canary's catalog (variations, single UOM, flat categories) are called out as anti-patterns at the bottom.

This card unblocks the build dispatch downstream of [GRO-877](https://linear.app/growdirect/issue/GRO-877) (item-setup screens). Sequenced after [GRO-880](https://linear.app/growdirect/issue/GRO-880) (Counterpoint catalog data-model audit) so the lift recommendations land against a schema with known altitude.

> **Verification status:** repo paths and language ports are based on the published `square/connect-api-examples` master-branch structure as of 2026-05-08. Specific line numbers within sample files are NOT pinned to commit SHAs in this card — the verification pass when this card is consumed by the build dispatch should run a `git clone` of the repo at a specific SHA, walk the cited paths, and replace `[verify]` markers with line ranges. The patterns themselves (algorithms, request shapes, error envelopes) are confirmed against Square's developer docs and stable across the v2 API surface.

---

## Hard scope distinction (load-bearing)

Square samples are useful for **upstream POS-adjacent mechanics** — the parts where Square sellers and Counterpoint sellers face the same engineering problem:

- OAuth flow + state + token refresh + revoke recovery
- Webhook signature verification (HMAC over signing-key + URL + raw body)
- Idempotency-key generation + reattempt semantics
- Batch upsert orchestration with intra-batch placeholder IDs
- CSV bulk-upload validation rules (Excel auto-conversion, encoding, required columns, tax header format)
- Camera barcode scanning UX (the WebSDK and seller-app patterns are widely-mirrored)

Square samples are **NOT** useful for above-the-POS retail-operations differentiation. The Counterpoint audit ([GRO-880](https://linear.app/growdirect/issue/GRO-880)) established that Counterpoint's REST surface is below back-office altitude; Square's data model is below Counterpoint's REST altitude. Anti-patterns at the bottom of this card enumerate which Square sample paths surface those limitations and should NOT be lifted.

---

## Recon Target 1 — `connect-api-examples/v2` catalog patterns

### Repo locations

The repository's v2 sample tree lives at:

```
github.com/square/connect-api-examples/
└── connect-examples/
    └── v2/
        ├── java_catalog/                  ← Java; catalog operations (lift target)
        ├── node_catalog_subscription/     ← Node.js; subscriptions over catalog
        ├── node_orders-payments/          ← Node.js; line-item composition (idempotency reference)
        └── (10 other language/topic combos for payments)
```

Language distribution for the repo as a whole: JavaScript 31.5%, Java 20.8%, TypeScript 8.2%, Ruby 7.0%, plus C# / PHP / Python.

### Pattern: Catalog Batch Upsert with placeholder IDs

**Source:** `connect-api-examples/connect-examples/v2/java_catalog/` `[verify]` — primary; mirror the request-shape construction logic.
**Language(s):** Java (primary sample); the API shape is language-agnostic.
**What it does:** Upserts up to 10K catalog objects in a single atomic request, with intra-batch cross-references via `#`-prefixed placeholder IDs. Server returns `id_mappings[]` translating placeholders to server-assigned UUIDs.
**Why we want it:** Flow B (supplier CSV import) is a batch-upsert problem at heart. The Square pattern handles intra-batch cross-references (e.g., create `CatalogItem#ABC` AND its `CatalogItemVariation` with `item_id: "#ABC"` in the same call) — the same pattern Canary needs for inserting a parent item + its barcodes + its vendor link in a single tx.
**Lift form:** Pattern, not code. Adapt the placeholder-ID convention to Canary's INSERT chain in the catalog-import store. The `#`-prefix encoding is reusable verbatim — mark client-supplied placeholder IDs with `#` and the store's `Insert` method substitutes server-assigned UUIDs at commit time, returning a `id_mappings` array.
**Caveat:** Square's hard limits (10 batches × 1000 objects = 10K) are the right ballpark for Canary too. A single supplier CSV uploading 5K rows fits in one batch; 50K rows requires chunking. Document the chunk size in Flow B's spec.

**Real shape (from `developer.squareup.com/reference/square/catalog-api/batch-upsert-catalog-objects`):**

```
POST /v2/catalog/batch-upsert
{
  "idempotency_key": "<uuid>",        // 1-128 chars; reattempt-safe
  "batches": [
    {
      "objects": [
        {
          "type": "ITEM",
          "id": "#ABC",                // # = client placeholder
          "item_data": {
            "name": "...",
            "variations": [
              { "type": "ITEM_VARIATION", "id": "#ABC-V1",
                "item_variation_data": { "item_id": "#ABC", ... } }
            ]
          }
        }
      ]
    }
    // ... up to 10 batches
  ]
}

Response:
{
  "objects": [...],                    // server-assigned IDs
  "id_mappings": [                     // placeholder → real
    { "client_object_id": "#ABC", "object_id": "<server-uuid>" },
    ...
  ],
  "updated_at": "...",
  "errors": [...]
}
```

### Pattern: Idempotency-key reattempt safety

**Source:** Recurring pattern across `node_orders-payments`, `java_catalog`, `python_payment` `[verify]`.
**What it does:** Every state-mutating call accepts an `idempotency_key` (caller-generated UUID). Reattempting with the same key is safe — Square deduplicates server-side and returns the original result.
**Why we want it:** Flow B's per-row INSERT path needs this for crash-recovery. If the gateway dies after writing rows 1-30 of 47, the resume path retries 31-47 with the same idempotency keys — rows 1-30 short-circuit (already-written), rows 31-47 commit cleanly. **This is the design ratchet for the "import_jobs status='COMMITTING' → resume" flow** in `canary-item-setup-screen-decomp.md` Flow B5.
**Lift form:** Convention. Generate one idempotency key per row at preview time (B3); persist on the import_jobs row; resume path pulls them and replays.
**Caveat:** Square doesn't document the idempotency window explicitly (forum guidance: "indefinite for catalog operations; 24h for payments"). Canary should keep its own idempotency-key→outcome map per import_jobs row rather than rely on an external window.

### Pattern: Square API Error Envelope

**Source:** `developer.squareup.com/docs/build-basics/general-considerations/handling-errors` — the wire-level shape.
**What it does:** Every error response carries:

```json
{
  "errors": [
    {
      "category": "INVALID_REQUEST_ERROR",   // high-level classification
      "code": "VALUE_TOO_LONG",              // specific identifier
      "detail": "Item name exceeds 255 char limit", // optional human description
      "field": "objects[3].item_data.name"   // optional pointer
    }
  ]
}
```

**Why we want it:** The `category` + `code` + `detail` + `field` shape is what Flow B's row-level validation should emit. The Counterpoint REST envelope in `IM_ITEM` has a single `ErrorCode` field (per the OpenAPI spec at line 191, `ErrorCode` schema); Square's structured envelope is materially better for client-side recovery UX.
**Lift form:** Adopt as Canary's import-error envelope verbatim. Adapter normalizes Counterpoint REST `ErrorCode` into this richer shape with synthesized category/code where Counterpoint emits opaque error strings.
**Caveat:** Square's full `ErrorCategory` enum is at `developer.squareup.com/reference/square/objects/ErrorCategory` — `[verify]` for the full set. Canary should pick a subset that matches its actual error population, not adopt every category Square has (many are payment-specific).

### Pattern: Webhook Signature Verification (HMAC over key + URL + body)

**Source:** `developer.squareup.com/docs/webhooks/step3validate`. SDK utilities at `WebhooksHelper` in Square's Node, Python, C#, Go, Java, PHP, and Ruby SDKs.
**What it does:** Square signs every webhook with HMAC-SHA-256 over `signing_key + notification_url + raw_request_body`. Header: `x-square-hmacsha256-signature`. Constant-time compare required.
**Why we want it:** Canary's webhook adapter (`internal/protocol/webhook/`) already does HMAC-SHA-256 signature verification per the protocol-layer hardening that shipped in Sprint 2 (T-D). The Square pattern's wrinkle worth lifting: **the URL is part of the signature payload**. Most webhook signers omit this — Square includes it specifically so a captured signature can't be replayed against a different endpoint. Worth adopting on Canary's webhook surface for the same reason.
**Lift form:** Confirm Canary's existing `internal/protocol/webhook/` includes the URL in the HMAC payload (audit follow-up). If not, add it.
**Caveat:** The "raw body" rule is load-bearing — the body MUST be hashed before any JSON parsing/re-serialization (which would change whitespace and break the signature). Square's docs explicitly warn: `{"hello":"world"}` (no whitespace, exact representation as wire). Canary should enforce the same.

### Pattern: OAuth state + scope-narrowed token

**Source:** `connect-api-examples/connect-examples/oauth/{java,node,php,python,python-aws-chalice,ruby}/` `[verify]` — 6 language ports.
**What it does:** Standard OAuth 2.0 authorization-code flow with state parameter for CSRF defense. Scopes are requested explicitly (per-permission); Square exposes account-level vs location-level scope distinctions via the `OAuthPermissions.md` reference doc in the repo root.
**Why we want it:** `internal/squareauth/` already implements this for the Square OAuth flow. The polish pieces worth lifting:
- **State parameter pattern** — short-lived, single-use, bound to session
- **Refresh-token rotation** — reuse-detection pattern (similar to T-1's `refreshfamily` we shipped, but Square applies it to OAuth tokens, not application JWTs)
- **Deauthorize flow** — `POST /oauth2/revoke` cleanly revokes and forces re-consent on next reconnect

**Lift form:** Reference; current `internal/squareauth/` is roughly aligned. The `python-aws-chalice` sample is the cleanest reference because it separates OAuth from app logic — useful for Canary's planned identity service split (T-1).
**Caveat:** Square's OAuth supports PKCE for first-party mobile clients but the sample-code repo does NOT consistently demonstrate PKCE — most samples are server-side flow only. If Canary ever needs a mobile-native OAuth flow (Android POS app), PKCE is required and the Square samples won't be the reference; use the IETF RFC 7636 reference instead.

---

## Recon Target 2 — Camera barcode scanning

### Reality check

Square's seller mobile app does barcode scanning, but the implementation is in their internal iOS/Android codebases — **NOT in the open-source `connect-api-examples` repo**. Square's Web SDK is payment-focused; it does NOT include a barcode-scanning component.

The pattern lift therefore comes from **library-level, not Square-specific**:

- **`BarcodeDetector` Web API** (Chrome/Edge/Android Chrome) — native browser camera scanning, no library needed
- **ZXing-JS** (`@zxing/browser`) — Safari + cross-browser fallback
- **html5-qrcode** — wraps both above with a clean React/vanilla component
- **Quagga2** — JavaScript-only fallback for older browsers

**Why this still belongs in this card:** the dispatch listed Square Web SDK as a recon target. The honest answer — "Square doesn't have this; lift from BarcodeDetector + ZXing directly" — is the load-bearing finding. Don't waste time hunting through Square's repos for a scanning pattern that isn't there.

### Pattern: BarcodeDetector with ZXing fallback

**Source:** Not Square. Use:
- MDN Web Docs `BarcodeDetector` API for the native path
- `@zxing/browser` npm package, MIT-licensed, ~150KB minified

**What it does:** Camera permission prompt → live decode → callback with format + value.

**Why we want it:** Flow A1 (scan entry) is the surface. The recommended UX:

```
1. on Mount: navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
   → camera permission prompt
   → on grant: render live video element + BarcodeDetector overlay
   → on deny: show ring-scanner pairing helper + manual entry field
2. BarcodeDetector + scanFromVideoDevice() polls @ 10fps
3. On decode: vibrate(50ms), audio click, re-render the scanned barcode
4. Confirm screen with "Looks right? [Continue]" or "Scan again [Retry]"
```

**Lift form:** Implementation pattern, not Square code. Reference the MDN BarcodeDetector docs; for the polyfill use `@zxing/browser`. **Important:** BarcodeDetector is Chromium-only; Safari needs ZXing fallback. Canary's surface needs both paths.

**Caveat:** Camera scanning quality degrades materially in low light. Real Bluetooth ring scanners (Socket Mobile, Zebra) are the ops-grade solution; the camera path is fine for casual on-floor setup but won't survive a high-volume receiving session. Canary's UX should make ring-scanner pairing a one-click pattern, not a "go into settings" workflow.

### Pattern: Bluetooth ring scanner pairing (HID profile)

**Source:** Not Square. Pattern lifted from `socketmobile/capture-android` and similar vendor SDKs.

**What it does:** Bluetooth ring scanners (Socket S700, Zebra RS5100) advertise as HID keyboards by default — they "type" the scanned barcode into whatever input field has focus. No special pairing; the device auto-connects after a Bluetooth pairing.

**Why we want it:** Floor associates can scan into the manual-entry field on C1 (or Flow A's "Or type" fallback) without any app integration. The only wrinkle: HID-mode scanners send a literal RETURN keystroke after each barcode, so the input field needs to capture-and-clear on RETURN, not submit-the-form on RETURN.

**Lift form:** Convention. JS event handler:

```js
input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    e.preventDefault();   // do NOT submit the form
    onBarcode(input.value);
    input.value = '';
  }
});
```

**Caveat:** SDK-mode scanners (Socket Mobile's "Capture" SDK, Zebra DataWedge) offer richer behaviors (battery status, bidirectional config) but require app-level integration. Day-one is HID; SDK is Phase 3 if Canary ever ships a native mobile app.

---

## Recon Target 3 — CSV bulk catalog upload

### Square's CSV import troubleshooting page (the gold mine)

**Source:** `squareup.com/help/us/en/article/6172-import-item-library-troubleshooting`

**Why we want it:** Square has battle-tested its CSV import against millions of merchants over a decade. The error class taxonomy that page enumerates IS the error class taxonomy Flow B3's row-level validation should mirror. Lifting it saves Canary from re-discovering each gotcha through field reports.

### Confirmed gotchas to bake into Flow B3

| # | Gotcha | What happens | Defense |
|---|---|---|---|
| 1 | **SKU in scientific notation** (e.g., `2.68435E+17`) | Excel auto-converts long numeric SKUs the moment the file is opened. Re-saving the .xlsx loses precision. | Canary detects scientific-notation pattern in SKU column; warns "Looks like Excel mangled this — show me how to fix"; offers a "Reformat as text" path that re-pastes the SKU as a string. |
| 2 | **Leading-zero loss in barcodes** | UPC-A starts with a numeric leading zero (e.g., `012345678905`). Excel strips the leading zero unless the column is explicitly text-formatted. | Detect length-12 numeric SKU/barcode columns where row count drops below 12 — flag rows; offer reformat-and-retry. |
| 3 | **Commas in description fields** | CSV-without-quoted-strings breaks the row layout the moment a field contains a `,`. | Recommend XLSX over CSV (XLSX is delimiter-safe by construction). If CSV is mandated, require RFC 4180 quoted strings; reject naive comma-separated. |
| 4 | **Wrong file format** | Square accepts only .xlsx and .csv — not .xls, .xlsm, .numbers. | Mime-type detection on B2; reject non-supported with a one-line "Save as XLSX or CSV" instruction. |
| 5 | **Tax column header format** | Square requires `Tax - Sales (7%)` exactly — percent in parens — for the tax rate to bind. | Adopt a similar canonical header convention; document in the supplier-CSV template generator on B1. |
| 6 | **Per-location Enabled column** | Multi-location merchants need an Enabled-{Location Name} column for each location, not a single status column. | Match the convention; auto-generate columns for each tenant location when the operator downloads the per-tenant template. |
| 7 | **Required vs optional columns** | Square requires Item Name + Variation Name + Description + SKU; the rest are optional. | Canary's required set is similar (description / SKU / supplier / cost / price / case_pack per Flow C1). Match the column-naming convention so a CSV that imports cleanly into Square also imports into Canary with minimal mapping. |
| 8 | **UTF-8 BOM** | Excel's CSV export prefixes UTF-8 BOM bytes (`EF BB BF`) on the first line; many parsers treat the BOM as part of the first column header. | Strip BOM during B2 parse; flag warn-only if detected. |
| 9 | **Multi-byte truncation** | Some platforms truncate descriptions silently at byte boundaries that fall mid-codepoint, producing mojibake. | Length-validate by codepoint count, not byte count. Postgres `text` is fine; the truncation comes from upstream tools. |

**Lift form:** Adopt all 9 verbatim into Flow B3's per-row validation rules. Each becomes a canary-side error code (e.g., `sku_scientific_notation`, `barcode_leading_zero_lost`, `unquoted_comma`, `unsupported_file_format`, `tax_header_malformed`, `missing_location_columns`, `bom_in_first_line`, `multibyte_truncation`).

**Caveat:** Square's UI surfaces these as inline notifications mid-upload. Canary's Flow B3 design (per `canary-item-setup-screen-decomp.md`) groups them into a "needs attention" row list — which is more compact for the operator but loses the per-cell precision. Worth considering an "expand row" affordance on B3 that shows Square-style per-cell highlighting on demand.

---

## Recon Target 4 — Receipt rendering

**Status: defer.** Not on Canary's near-term roadmap. The dispatch flagged this as lower priority; the Counterpoint long-arc card (`project_canary_replaces_counterpoint_long_arc.md`) puts receipt rendering at Phase 4 of the 5-7 year POS-replacement arc.

When this becomes relevant:
- Square's iOS / Android Reader SDKs document ESC/POS thermal printer command sequences for the supported star/epson/zebra printers
- HTML email-receipt templates live in the seller dashboard's printable format
- The receipts API at `developer.squareup.com/reference/square/orders-api` returns a `receipt_url` string — Square hosts the receipt page

**Recommendation when receipts become Canary scope:** open a separate dispatch; cross-reference Square's documented ESC/POS commands but use a maintained Go library (`mugli/escpos` or `bbqshellgun/escpos`) rather than copying byte sequences from Square's docs. The byte sequences vary by printer manufacturer; the library handles the dispatch.

---

## Recon Target 5 — OAuth + deauthorize polish

### Pattern: Reconnect-after-revoke recovery

**Source:** `connect-api-examples/connect-examples/oauth/python/` `[verify]` — clearest of the language ports for the recovery flow.

**What it does:** When a Square user revokes Canary's OAuth from the Square seller dashboard, Canary's stored tokens become invalid — but Canary doesn't know until the next API call returns 401. The Square-recommended pattern:

1. Catch 401 with `category=AUTHENTICATION_ERROR` on any API call.
2. Mark the merchant's OAuth credentials as `status=revoked` in the local store.
3. Surface a banner on the merchant's next page load: "Your Square connection was revoked. [Reconnect]"
4. Reconnect button kicks off a fresh OAuth flow, re-binds tokens, clears the banner.

**Why we want it:** `internal/squareauth/` today does the OAuth dance but doesn't have the revoke-recovery banner. Square users WILL revoke and reconnect over a year; without the recovery surface, they'll see "data not loading" without diagnostic context.

**Lift form:** Convention. Add a `revoke_detected_at` column on the `pos_tenant_credentials` row; set it on 401 from the Square adapter; Flow A's scan path checks it and surfaces the banner.

**Caveat:** Square's OAuth tokens have a 30-day refresh window. If a merchant doesn't connect for >30 days, the refresh token also expires — same surface treatment (banner + reconnect), different cause. The `detail` field on the 401 distinguishes them.

### Pattern: Partial-permission scope handling

**Source:** `connect-api-examples/connect-examples/oauth/OAuthPermissions.md` `[verify]`.

**What it does:** When the OAuth flow asks for N scopes and the user grants M (M < N), the response has reduced permissions. Square's pattern: detect on first API call, prompt user to re-grant the missing scope.

**Why we want it:** A Square merchant who declines `MERCHANT_PROFILE_READ` will still grant `ITEMS_READ` — Canary should fall back to a degraded-mode UX (no merchant name in the dashboard header) rather than refuse to operate.

**Lift form:** Convention. Adapter checks the granted-scopes claim on token; Canary's UI conditionally renders surfaces based on which scopes are present.

**Caveat:** Counterpoint's auth model doesn't have this concept (single API key per company). The partial-scope path is Square-specific and won't apply to RapidPOS sellers.

---

## Anti-patterns — what NOT to lift from Square

These show up in Square's sample code and would mis-shape Canary's catalog if adopted. **Each is sourced to a specific sample file so the build dispatch can avoid the trap.**

| # | Anti-pattern | Where in Square's samples | Why NOT lift |
|---|---|---|---|
| 1 | **Single-dimension `CatalogItemVariation`** — Square's variations support 1 axis per item (size OR color OR flavor) | `connect-api-examples/connect-examples/v2/java_catalog/` `[verify]` example uses single-axis variation throughout | Counterpoint operators run 3D grids (Size × Color × Style for apparel; Length × Material × Edge for lumber) — see [GRO-880 audit](#counterpoint-catalog-data-model-audit). Square's one-axis assumption mis-shapes the model. |
| 2 | **Single UOM** — Square has one `unit_type` per item; no purchasing/selling/inventory split | Universal across `java_catalog`, `node_catalog_subscription` | Counterpoint REST exposes STK_UNIT + PREF_UNIT (and back-office has Stocking + Alternate + Associated). Square's single-UOM mental model loses receiving conversions. |
| 3 | **Flat `Category`** — Square has one-level categories | `java_catalog` `[verify]` | Counterpoint REST exposes Category + Subcategory (2-level). Canary's `product_categories.parent_id` already supports the hierarchy; Square's flat assumption would regress. |
| 4 | **One price per item** — Square's `CatalogItem.variations[].item_variation_data.price_money` is single-valued | Universal | Counterpoint has 10-layer pricing precedence (per `Brain/wiki/cards/counterpoint-catalog-data-model-audit.md` §Pricing). Even GRO-880's "observe-don't-replicate" recommendation needs more than a single-price field. |
| 5 | **`InventoryAdjustment` as a counter, not a positions ledger** | `developer.squareup.com/reference/square/inventory-api` | Canary's inventory thesis is a positions ledger with movement events. Square's adjust-by-delta API doesn't compose into the audit-ready ledger Canary needs. |
| 6 | **Modifier Lists conflated with Variations** | `node_catalog_subscription/` `[verify]` mixes both | Square distinguishes Modifiers (per-line add-ons like "+ extra cheese") from Variations (separate SKUs). Counterpoint represents both as separate ITEM_NO records. Canary should follow Counterpoint here, not Square. |
| 7 | **Tax classes as catalog objects** | `developer.squareup.com/reference/square/catalog-api/upsert-catalog-object` (CatalogTax type) | Canary's `tax_class TEXT` column is a string lookup into a separate `pricing.tax_classes` table — better separation. Square treats taxes as catalog objects with their own UUIDs and lifecycle, which couples tax-config to catalog-bulk-upsert atomicity. Don't follow that. |
| 8 | **Square's `present_at_all_locations` boolean** | `java_catalog` | Counterpoint authorization is the 4-dimension model (item eligibility / regulatory zone / planogram listing / operational blocks per `retail-item-authorization.md`). The boolean flag is too crude. |

---

## Lift sequencing — which patterns into which Canary screens

| Square pattern | Canary screen / flow | Priority |
|---|---|---|
| Catalog Batch Upsert with placeholder IDs | Flow B5 (per-row commit; `id_mappings[]` returned to client for cross-reference resolution) | P0 |
| Idempotency-key reattempt safety | Flow B (per-row crash recovery on `import_jobs.status='COMMITTING'`) | P0 |
| Square API Error Envelope | Flow B3 (row-level validation reporting); Counterpoint adapter normalization | P0 |
| Webhook URL-in-signature defense | `internal/protocol/webhook/` audit follow-up | P1 |
| OAuth state + scope-narrowed token | `internal/squareauth/` already aligned; spot-fix gaps | P1 |
| Reconnect-after-revoke recovery banner | Flow A and dashboard chrome | P1 |
| Partial-permission scope handling | Square-specific; degraded-mode UI | P2 |
| BarcodeDetector + ZXing | Flow A1 scan entry (via npm packages, not Square code) | P0 |
| Bluetooth ring scanner HID convention | Flow A1 scan entry + C1 manual fallback | P0 |
| CSV gotchas (all 9) | Flow B3 row-level validation rules | P0 |

---

## Verification pass (the unfinished work)

When this card is consumed by the build dispatch, the following pinning is needed:

1. **`git clone github.com/square/connect-api-examples` at a specific commit SHA** — record the SHA in this card's frontmatter.
2. **Walk the cited sample files** (`java_catalog/CatalogApiSample.java`, `node_orders-payments/server.js`, `oauth/python/oauth.py` etc.) and replace `[verify]` markers with line ranges for the specific patterns called out.
3. **Confirm the `OAuthPermissions.md` content** in the OAuth examples directory matches the partial-permission pattern documented above.
4. **Cross-check the SDK `WebhooksHelper` source** for the URL-in-signature handling; confirm the implementation hashes URL + body, not body only.
5. **Pin the Square error-handling docs SHA** by archiving the page content at the verification timestamp (Square updates docs in-place; URLs alone don't preserve historical content).

After the verification pass, this card moves from `[verify]`-marked to fully-pinned. The patterns themselves are stable; the line numbers are what need anchoring.

---

## See also

- [[canary-item-setup-screen-decomp]] — the screens these patterns flow into (Flow A scan, Flow B import, OAuth-revoke banner)
- [[counterpoint-catalog-data-model-audit]] — what NOT to lift, with Counterpoint-side justification
- [[canary-item-master-and-catalog]] — parent retail-substrate card; build-priority context
- [[canary-mobile-task-ux-flows]] — mobile UX precedent; ring-scanner HID convention applies
- `CanaryGo/internal/squareauth/` — existing OAuth implementation to refine with revoke-recovery banner
- `CanaryGo/internal/adapters/square/` — adapter to refine with Square-error-envelope normalization
- `CanaryGo/internal/protocol/webhook/` — webhook signature path to audit for URL-in-signature defense
- GRO-881 — this card's source dispatch
- GRO-880 — the Counterpoint audit that established what NOT to lift altitudes
