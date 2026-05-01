---
classification: internal
type: audit-report
date: 2026-04-25
companion-sdd: docs/sdds/canary/ncr-counterpoint-retail-spine-integration.md
companion-dispatch: Brain/dispatches/2026-04-25-tsp-crdm-counterpoint-flow.md
phase: 0a
status: draft-1
---

# Audit — Square Coupling in the Canary App Layer (NCR Counterpoint Phase 0a)

## 1. Executive summary

**Coupling intensity: MEDIUM-HIGH.** The Canary app layer was built as a Square-only pipeline and the assumption shows up at three depths: file/function names, model column names, and behavioral contracts. The footprint is broad — 143 Python files reference the string "square" in some form, ~50 distinct `square_*` columns exist across `app` and `sales` schemas, and core runtime predicates (HMAC validation, idempotency, ID resolution, schema-drift fingerprinting, stateless Chirp rules) all assume push-based webhook semantics with Square's payload shape.

**Dominant pattern of coupling:** every entity table in the `app` schema carries a `square_<entity>_id` natural-key column that is also the upsert lookup key, and every Chirp rule that crosses sales→app boundaries does its own `square_id → UUID` resolver lookup. The platform already has the bones of a generalized model — `source_systems`, `external_identities`, `merchant_sources`, the `MerchantSource.source_code` FK, and the source-agnostic `enrich_payload(source, ...)` and `normalize_payload(source, ...)` functions — but the actual lookup paths bypass those bridges and read `square_*` columns directly.

**Rough work order to generalize.** (1) Lock the abstractions that already exist (validators, enrichers, source registration) by registering a `counterpoint` source code; (2) introduce a poll-mode ingress siblng to `webhooks_tsp.py` that produces the same 9-field stream message; (3) generalize the `square_<entity>_id` upsert path so the resolver reads from `external_identities` instead of the column; (4) keep the `square_*` columns where they are (they're harmless when `external_identities` becomes the canonical lookup) and add `counterpoint_*` siblings or `source_native_id` only when a column does double-duty as a forensic field; (5) leave Square-specific files (`validators/square.py`, `enrichers/square.py`, `parsers/square_*.py`) untouched as the proof case and add `counterpoint` peers.

## 2. Coupling inventory

### Layer 1 — String / identifier hardcoding (cosmetic)

| File:lines | What it does | What couples it to Square | Proposed generalization | Severity | Effort |
|---|---|---|---|---|---|
| `canary/blueprints/webhooks_tsp.py:33` | `REGISTERED_SOURCES = {"square"}` — set of valid `<source>` path params | Hard set of 1 entry | Read from `source_systems` table on app boot or extend set to `{"square", "counterpoint"}` once the Counterpoint validator exists. | LOW | XS |
| `canary/blueprints/webhooks_tsp.py:36-43` | `SOURCE_VALIDATORS` and `SOURCE_SIGNATURE_HEADERS` — single-entry dicts mapping source code → validator module / header | Only `"square"` registered | Add `"counterpoint": counterpoint_validator` entry. The dict abstraction is already correct. | LOW | XS |
| `canary/blueprints/webhooks_tsp.py:167` | `if not parse_failed and source == "square":` — gates the inline stateless Chirp evaluator | Hardcoded source check | Replace with `if route.stateless` and let `webhook_dispatch` route by source+event_type. | MED | S |
| `canary/blueprints/webhooks_tsp.py:253-261` | `ready` probe calls `square_validator.get_signature_key()` and `get_notification_url()` | Readiness gate hard-bound to Square config | Iterate `SOURCE_VALIDATORS.items()` and call a uniform `validator.health_check()` interface. | LOW | S |
| `canary/services/webhook_dispatch.py:53-403` | `EVENT_ROUTES` dict — 70+ entries, every parser path is `square_<thing>_parser:parse_<thing>` | All parser dotted-paths hardcoded | Wrap into a `SOURCE_DISPATCH = {"square": EVENT_ROUTES, "counterpoint": COUNTERPOINT_ROUTES}` map; `resolve_route` takes (source, event_type). | MED | M |
| `canary/services/webhook_dispatch.py:412-446` | `PREFIX_ROUTES` dict — Square event-name prefixes (`payment.`, `refund.`, `loyalty.`, etc.) | Square taxonomy baked in | Move under per-source dispatch table. Counterpoint will have its own taxonomy (Documents, Items, Customers, etc.). | MED | S |
| `canary/services/webhook_dispatch.py:457` | `import_parser` hardcoded module prefix `canary.services.parsers.{module_name}` | Implicitly assumes a flat parser dir of Square modules | Either pass the full module path through `EventRoute.parser` or scope by source: `canary.services.parsers.{source}.{module_name}`. | LOW | S |
| `canary/services/tsp/enrichers/__init__.py:22-24` | `_SOURCE_ENRICHERS = {"square": "..."}` — single-entry dispatch | Same shape as validators — already source-agnostic but only Square wired | Add `"counterpoint": "canary.services.tsp.enrichers.counterpoint"` once the polling adapter writes to the same stream. The interface is already right. | LOW | XS |
| `canary/services/parsers/` — 17 files prefixed `square_` | One parser module per Square event family | Filename + module-level docstrings + every function name | Leave the existing 17 files alone (proof case). Add a `counterpoint/` subdirectory or `counterpoint_*.py` peers. | LOW | XL (parser surface, not refactor) |
| `canary/services/config_service.py:41-50, 89` | Config registry hardcodes 10 `SQUARE_*` env keys under `'square'` namespace | Square-only env contract | Add a `'counterpoint'` namespace with `COUNTERPOINT_API_BASE_URL`, `COUNTERPOINT_BASIC_USER`, `COUNTERPOINT_API_KEY`, etc. The dict structure already supports namespaces. | LOW | S |
| `canary/services/condor/intelligence.py:80-84` | SDK version-tracking dict — knows about Square SDK | Source-aware version intelligence | Extend to include Counterpoint REST API version detection (`DB_CTL.DB_VER`). | LOW | XS |
| `canary/services/scenario_runner.py:413` | Test scenario builder mints `square_shift_id=f"SQ_SHIFT_SCN_..."` | Synthetic Square ID format | Out of scope per the audit charter (test/scenario layer); flag for completeness. | LOW | XS |
| `canary/services/payload_factory.py:204, 213` | Payload factory mints `receipt_url=https://squareup.com/...` and `square_product=SQUARE_POS` | Synthetic data is Square-shaped | Tag synthetic payloads with `_source` so factory can branch. Lab/test concern but the factory is referenced by ops_console. | LOW | S |
| `canary/blueprints/square_oauth_wired.py` (entire file) | Square OAuth blueprint — OAuth flow, sandbox bootstrap, factory-reset, source registration via `MerchantSource.source_code == "square"` | Square OAuth endpoint contract | Stays as-is. Counterpoint authn is Basic + APIKey, not OAuth — needs a *different* blueprint, e.g., `counterpoint_connect_wired.py`. The MerchantSource hooks already use a `source_code` parameter — generalize the helper functions (`_register_square_source`) into `_register_source(merchant_id, source_code, session)`. | LOW | M |
| `canary/blueprints/square_explorer_wired.py` (entire file) | Square API capability explorer / dev tool | Explicitly Square API explorer | Stays Square-only; Counterpoint has its own discovery surface (the OpenAPI + endpoint spine map). Add a peer `counterpoint_explorer_wired.py` later if useful. | LOW | – |
| `canary/services/square_capability_explorer.py`, `square_oauth.py`, `square_sandbox_seeder.py` | Source-specific service helpers | Square-only by design | Stay Square-only. Build sibling `counterpoint_*` modules. | LOW | – |
| `canary/services/scenario_fire.py:643, 653, 672, 689, 731, 783` | Scenario-fire helper imports `_get_square_client` and calls Square sandbox | Lab/scenario layer is Square-coupled | Out of audit scope (tests/lab); flag for parity once Counterpoint sandbox exists. | LOW | – |
| `templates/auth/join.html`, `connect.html`, `welcome.html`, `settings.html`, `team.html`, `app/owl.html`, `ops/test_lab.html` | UI strings: "Connect with Square", "from Square", `square_env`, `btn-square` CSS class, "Pulling your data from Square…" | Square branding/strings in UI copy | These templates serve the Square onboarding flow. Build a parallel set of Counterpoint-onboarding templates rather than refactoring these. UI copy references on dashboards/tables ("from Square", "Square employee ID") need a label-overrides or per-source UI layer. | LOW | M |

### Layer 2 — Model-layer Square assumptions (structural)

The dominant pattern: every entity table that came from a Square webhook has a `square_<entity>_id: Mapped[str]` column that doubles as the upsert key and as the FK target for sibling tables.

| Table / file | Square-shaped columns | What couples it to Square | Proposed generalization | Severity | Effort |
|---|---|---|---|---|---|
| `app/employees.py:35,82` | `square_employee_id` + `idx_employees_merchant_square_id` | Lookup key for upsert; resolver target across the whole codebase (chirp engine, alerts, dashboards) | KEEP column for forensic source-of-truth; switch the upsert/resolver path to read `external_identities` (already exists per GRO-267). Add `counterpoint_employee_id` only if Counterpoint employees are sourced (per Counterpoint SDD §6.12, Module L is parked — Counterpoint doesn't expose employees). | HIGH | L |
| `app/locations.py:35,91` | `square_location_id` + index | Same as employees — used by Chirp resolver, dashboards, employee_links FK | Same: keep column, route resolution through `external_identities`. Counterpoint Stores will land in this table as a separate source. | HIGH | L |
| `app/customers.py:36,67` | `square_customer_id` + index | Upsert key, customer-tier resolution | Same pattern: `external_identities`-mediated. Counterpoint customer pull (Module C) is straightforward to layer on. | MED | M |
| `app/products.py:35,72` | `square_item_id` + index | Catalog identifier; joined by Owl Search registry | Same. Counterpoint Item* endpoints map cleanly. | MED | M |
| `app/gift_cards.py:39,84,90` | `square_gift_card_id`, `square_created_at`, index | Upsert key + Square-side timestamp | Same. `square_created_at` represents source-side creation time → rename to `source_created_at` in a future cleanup pass, but this is cosmetic. | LOW | S |
| `app/transfer_orders.py:36,78,82,88` | `square_transfer_order_id`, `square_created_at`, `square_updated_at`, index | Upsert key + source timestamps | Same. Counterpoint maps to Document* with transfer DOC_TYP. | MED | M |
| `app/subscriptions.py:37,106,112` | `square_subscription_id`, `square_created_at`, index | Upsert key | Same. Counterpoint has no subscription endpoint surface — column stays Square-only. | LOW | S |
| `app/bank_accounts.py:35,104` | `square_bank_account_id` + index | Upsert key | Same. Counterpoint has no bank-account API. | LOW | XS |
| `app/oauth.py:27,64` (table `square_oauth_tokens`) | TABLE NAME literally encodes Square; `SquareOAuthToken` class | Square OAuth-shaped (access_token / refresh_token / scopes) — Counterpoint uses Basic + APIKey, fundamentally different | KEEP. Counterpoint credentials need a *different* table — e.g., `counterpoint_credentials` storing encrypted (basic_user, basic_password, api_key, base_url, company_alias). One row per (merchant, company). Don't shoehorn into `square_oauth_tokens`. | MED | M |
| `sales/transactions.py:140` | `square_product` column (POS / INVOICES / VIRTUAL_TERMINAL / ONLINE_STORE) | Square-specific product family | Rename to `source_channel` or leave + add per-source siblings. Counterpoint's analog is the `source_name` field on Documents. Owl Search registry references this column at `registry.py:318`. | MED | S |
| `sales/transactions.py:43,47` | `external_id` doc says "Square payment_id or refund_id" + `order_id` doc says "Square order_id" | Field semantics tied to Square IDs | Keep column names; update doc strings to "source-system payment_id / order_id" and have the parsers populate consistently. | LOW | XS |
| `sales/transactions.py:57` | `source_type` defaults to "WEBHOOK" — values = WEBHOOK / POLLING / BATCH | Already source-agnostic per type, but `source` system itself isn't tracked here | Add `source_code` column (FK to source_systems.code) to record which integration produced the row. The current model can't distinguish a Square txn from a Counterpoint txn in `sales`. | HIGH | M |
| `sales/disputes.py:38,78` | `square_dispute_id` + repr | Upsert key | Counterpoint has no dispute endpoint — keep Square-only. | LOW | XS |
| `sales/timecards.py:39` | `square_timecard_id` | Upsert key | Counterpoint has no timecard endpoint (Module L parked). Keep Square-only. | LOW | XS |
| `sales/gift_cards.py:36` | `square_activity_id` (gift-card activity log) | Upsert key | Counterpoint maps to GiftCard* document/transaction surface. | LOW | S |
| `sales/terminal.py:39,111,115,153,221,225` | `square_checkout_id`, `square_refund_id`, `square_created_at`, `square_updated_at` (×2) | Upsert keys + Square timestamps | Counterpoint has no Terminal endpoint. Keep Square-only. | LOW | XS |
| `sales/payouts.py:37,69` | `square_payout_id` + repr | Upsert key | Counterpoint has no payout endpoint. Keep Square-only. | LOW | XS |
| `sales/cash_drawers.py:39` | `square_shift_id` | Upsert key | Counterpoint has no cash-drawer-shift endpoint. Keep Square-only. | LOW | XS |
| `sales/invoices.py:55,172,193` | `square_invoice_id`, `raw_square_object` (JSONB blob) + repr | Upsert key + literal Square JSON object stored | Counterpoint invoices live in Documents; rename `raw_square_object` to `raw_source_object` in a future pass. | MED | S |
| `sales/devices.py:36,50,112,133` | `square_device_id`, `raw_square_object`, indexes | Upsert key + raw Square payload | Counterpoint Devices map via Store_Station / Device_Config. Same generalization as invoices. | MED | S |
| `sales/loyalty.py:22,31,66,94` | `square_loyalty_id`, `square_event_id`, indexes | Upsert keys | Counterpoint loyalty embedded in Customer record (per SDD Q4). Keep Square-only. | LOW | XS |
| `sales/inventory.py:37` | `square_adjustment_id` | Upsert key | Counterpoint Inventory_ByLocation has its own identifier model. | MED | S |
| `metrics/dimensions.py:113,176` | `DimLocation.square_location_id` + `DimEmployee.square_employee_id` | Star-schema dim tables keyed by Square IDs | Same fix as `app/` tables: route through `external_identities`. Affects `services/metrics/dim_loader.py` and `services/chart_queries.py:129-209`. | MED | M |
| `app/external_identities.py:21` | `ENTITY_TYPES = ("employee", "location", "device", "product", "customer")` | Hard tuple; CHECK constraint `ck_ext_id_entity_type` | Add `"item_category"`, `"vendor"`, `"transfer_order"`, `"document"` (for Counterpoint Documents that map across `Things`/`Events`). Requires migration. | MED | S |
| `app/source_systems.py:39` | Doc string suggests `'square', 'clover', 'toast'` | Reference table is correctly source-agnostic; just needs `'counterpoint'` row | Insert `('counterpoint', 'NCR Counterpoint', 'pos', true, ...)` row. | LOW | XS |
| `app/merchant_sources.py:43-48` | `source_code` FK is correct; `external_merchant_id` doc says "Square merchant_id" | Correct source-agnostic shape; just needs Counterpoint row | Counterpoint's analog: `<company-alias>` (per SDD §3). Update doc; add per-source `metadata_json` schema. | LOW | XS |

### Layer 3 — Behavioral assumptions (deepest)

These are the architecture-level decisions where the system was built around Square's contract. Generalizing requires design choices, not just renames.

| File / function | What couples it to Square | Proposed generalization | Severity | Effort |
|---|---|---|---|---|
| `webhooks_tsp.py:48-215` — `receive_webhook(source)` | The entire ingress is **push-based webhook**. Counterpoint is **poll-based REST** — there is no inbound HTTP, no HMAC header, no "return 200 to client" contract. | Build a sibling `services/tsp/poll/counterpoint_poller.py` that runs on a cron/Celery interval, fetches via `/Documents`, `/Customers`, `/Items` etc., and writes to the **same** `canary:events` Valkey stream with the same 9-field message contract. The four downstream consumers (sub1-sub4) reuse unchanged. | HIGH | L |
| `webhooks_tsp.py:107-109` — `event_hash = SHA-256(raw_bytes)` BEFORE JSON parse | Hash is anchored to "exact bytes the client sent" — Counterpoint pulls have no client-sent bytes; we pull, hash our own request bytes (vendor lock-in to a representation we chose) | Hash the **canonicalized JSON** of the response we received from Counterpoint (sorted keys, fixed encoding). Document this as a deliberate "pull-mode hash anchor" decision in the SDD — the evidence guarantee shifts from "what Square sent" to "what we received and stored verbatim". | HIGH | M |
| `webhooks_tsp.py:140` — idempotency key `(source, source_event_id)` derived from Square's `event_id` field | Counterpoint Documents have `DOC_NO` + `DOC_TYP` + workgroup; there's no analog to Square's `event_id` for non-Document entities | Per-source idempotency-key derivation function, e.g., `compute_idempotency_key(source, payload, event_type)`. For Counterpoint: `f"{company}:{doc_typ}:{doc_no}"` for Documents; primary key for Customers/Items. | HIGH | M |
| `webhooks_tsp.py:118-126` — merchant resolution: `_app.query(Merchant).filter_by(source_merchant_id=merchant_id)` | Assumes 1 merchant = 1 source merchant_id (Square's flat model). Counterpoint has **multi-company per tenant** (`<company-alias>.<username>`). | Resolve `(merchant_id, company_alias) → internal merchant UUID` for Counterpoint. May require splitting Merchant into `Tenant` + `MerchantCompany`, or adding a `company_alias` column on `merchant_sources.metadata_json` and resolving via that. | HIGH | L |
| `services/tsp/validators/square.py` (entire file) | HMAC-SHA256 over `notification_url + body` keyed with subscription key — Square's exact spec | Counterpoint has no HMAC. Build `services/tsp/validators/counterpoint.py` that validates (Basic Auth realm + APIKey header presence) on the **outbound** poll, plus a TLS pin if customer host requires it. The "validator" abstraction is currently 1:1 with HMAC; widen the interface to "is this exchange authentic". | LOW (separate file) | M |
| `services/chirp/rule_engine.py:67-116, 1556-1603` — `_resolve_square_ids`, `_resolve_employee_id`, `_resolve_location_id` | The Chirp engine reads `Employee.square_employee_id` / `Location.square_location_id` as the resolver join keys. Bypasses `external_identities`. | Replace with `external_identities`-mediated lookup: `resolve(merchant_id, entity_type, source_code, external_id) → uuid`. Cache shape is identical. After change, both Square and Counterpoint employees resolve uniformly. | HIGH | M |
| `services/tsp/consumers/sub2_parse.py:66-198` — `_lookup_primary_employee`, `_sync_employee_locations`, `_upsert_employee` | Hardcoded `Employee.square_employee_id` lookups for primary-employee assignment + location sync | Same `external_identities` mediation. Sub2's `_upsert_*` family (employee, customer, location, gift_card, card_profile, subscription, transfer_order, bank_account) is structurally identical — six identical implementations differing only in `square_<entity>_id` column name. Refactor into a single `upsert_via_external_id(session, model_cls, parsed, source_code, entity_type)`. | HIGH | L |
| `services/tsp/consumers/sub2_parse.py:678-845` — `_build_models` | Branches on `event_type.startswith("payment.")`, `"refund."`, `"order."` — Square taxonomy | Pass the route's `crdm_model` and a `model_builder` callable through the `EventRoute`. Each source's dispatch table provides its own builder for "payment-equivalent → Transaction enrichment", etc. | MED | M |
| `services/tsp/consumers/sub2_parse.py:482-499, 502-663` — `PAYMENT_ENRICHMENT_FIELDS`, `_enrich_from_payment` | Square-specific bidirectional enrichment: an order webhook arrives with header info, a payment webhook arrives later with card details, both write to the same Transaction row. Counterpoint Documents come in **whole** (header + lines + payments + tenders all in one PS_DOC_HDR + 11 nested arrays). | Counterpoint won't need this enrichment dance. The `_build_models` dispatch for `source="counterpoint"` parses one Document → one Transaction + children atomically. The Square enrichment path stays untouched. | – | – |
| `services/tsp/consumers/sub2_parse.py:1113-1165` — `_check_schema_fingerprint` | Computes SHA-256 of sorted top-level field names of the **payload**. Square's payload shape is flat-ish at root (`type`, `event_id`, `merchant_id`, `data`, `created_at`). Counterpoint Documents have a nested PS_DOC_HDR + arrays — top-level keys are different and a "drift" alert would fire spuriously on every Counterpoint event. | Source-aware fingerprinting: include `source` in the fingerprint key, and let the field-extraction strategy be source-specific (root keys for Square; full schema-walk for Counterpoint). `SchemaFingerprint` model needs a `source` column. | MED | M |
| `services/chirp/stateless_engine.py:51-69` — Tier 1 rules `_check_after_hours`, `_check_high_value_refund`, `_check_square_delay_hold`, `_check_partial_auth`, `_check_no_sale` | C-009 (`SQUARE_DELAY_HOLD`) reads `delay_action`/`delay_duration` — Square-specific risk-hold mechanism with no Counterpoint analog. C-011 (`NO_SALE_DETECTED`) reads `transaction_type=="NO_SALE"` from `capabilities` — Square-specific. C-010 reads `approved_amount_cents` (Square partial-auth signal). | C-009/C-010/C-011 stay **Square-only** rules (gated on `source_code == "square"`). Add new Counterpoint-specific Tier 1 rules: voided-tender patterns, employee-discount via PayCodes, transfer-immediately-after-create, etc. (per SDD §6.5 Module Q open question). | MED | M |
| `services/chirp/rule_engine.py:25-32` — `_AUTO_CASE_RULES = {"C-009", ...}` | Includes C-009 (Square-specific delay hold) | Add Counterpoint-specific auto-case rules to the set; rule IDs are already source-tagged. | LOW | XS |
| `services/parsers/square_payment_parser.py:79-84` | Hardcodes Square Payment status enum: `COMPLETED`, `APPROVED`, `CANCELED` | Counterpoint Document status uses different codes (`IS_DOC_COMMITTED`, `IS_OFFLINE`, etc. — per SDD Q15 partial). Each parser is source-bound — leave Square parsers untouched, build Counterpoint parsers with their own status mapping. | – | – |
| `services/identity/external_id_resolver.py` (referenced from sub2_parse.py:131-138) | The bridge already exists and takes `source_code` as a parameter — register_external_id is correctly source-agnostic | Confirmed already-correct. The fix above (Layer 3 chirp/sub2 refactor) reuses this. | – | – |
| `services/raas/payload_normalizer.py:20-64` | `normalize_payload(payload, merchant_uuid, source)` is **already source-agnostic** by design. Currently called only with `source="square"` from sub2_parse. | Confirmed already-correct. Counterpoint payloads route through it unchanged. | – | – |
| `services/tsp/enrichers/__init__.py` + `services/tsp/enrichers/square.py` | Source-agnostic dispatch + per-source module — already correctly factored | Add `enrichers/counterpoint.py` if Counterpoint pulls need post-hoc API enrichment (likely no — pulls already retrieve full Documents). | LOW | XS |

## 3. High-blast-radius items

The five places that will eat the most engineering time if not handled deliberately:

1. **The `square_<entity>_id` resolver pattern** (HIGH × 8 tables × 4+ call sites). Every entity table in `app/` has the same shape: `square_<thing>_id` natural key, an upsert function that filters on it, and at least one resolver in Chirp / dashboards / dim_loader / sub2_parse that joins on it. Generalizing this means adding an `external_identities`-mediated indirection across ~12 modules. It pays for itself once Counterpoint lands but the change touches `chirp/rule_engine.py` (3 sites), `tsp/consumers/sub2_parse.py` (8 upsert functions), `services/dashboard_queries.py` (2 sites), `services/chart_queries.py` (4 sites), `services/metrics/dim_loader.py` (4 sites), `blueprints/views_wired.py` (5+ sites), and `blueprints/webhooks_tsp.py:392` (location resolver for stateless Chirp).

2. **Push vs. pull ingress contract** (HIGH × architectural). `webhooks_tsp.py` is a webhook handler — it receives, validates HMAC, returns 200 to a remote caller. Counterpoint inverts this: Canary is the caller. The right play is to leave `webhooks_tsp.py` untouched (Square's working ingress) and build a sibling `services/tsp/poll/counterpoint_poller.py` that publishes to the same `canary:events` stream with the same 9-field message. The four consumers (sub1-sub4) need zero changes. But: the **idempotency derivation** (`source_event_id`), the **hash anchor** (raw bytes vs canonical JSON), and the **merchant resolution** (single Square merchant_id vs Counterpoint multi-company) all need source-aware logic at the publish boundary. That's three deep changes in close proximity.

3. **Schema-drift fingerprinting `_check_schema_fingerprint`** (MED-HIGH × 1 file but global). Currently fingerprints the sorted top-level field names of the payload. Counterpoint Documents have a fundamentally different payload shape (PS_DOC_HDR + 11 nested arrays vs. Square's `type`/`event_id`/`merchant_id`/`data` flat root). Without a `source` column on `SchemaFingerprint`, every Counterpoint event will look like "schema drift" and pollute the dashboard. Requires migration.

4. **Stateless Chirp evaluator gated on `source == "square"`** (MED × deep). `webhooks_tsp.py:167` runs Tier 1 rules inline only when source is Square. Three of the five Tier 1 rules (C-009 SQUARE_DELAY_HOLD, C-010 PARTIAL_AUTHORIZATION, C-011 NO_SALE_DETECTED) are Square-payload-specific. Generalizing here means moving the `source == "square"` gate to per-rule (each rule declares which sources it applies to), which is a small refactor but touches the rule definitions and the per-source threshold registry.

5. **`square_oauth_tokens` table + `SquareOAuthService`** (MED × isolated). Square's OAuth tokens (access_token / refresh_token / scopes) don't fit Counterpoint's auth model (Basic + APIKey). The cleanest path is a separate `counterpoint_credentials` table and a `CounterpointAuthService`. The risk is teams later trying to "reuse" `square_oauth_tokens` for Counterpoint and shoehorning the schema. Add an explicit ADR + a `source_oauth_tokens.source_code = 'square'` CHECK constraint to prevent that.

## 4. Schema audit summary

### `app` schema — what is Square-shaped

| Table | Square-shaped column | Recommended treatment |
|---|---|---|
| `employees` | `square_employee_id` (NN, indexed) | KEEP. Stays as Square's source-of-truth ID. Add Counterpoint employees to `external_identities` if/when Module L source identified — Counterpoint REST does not expose employees. |
| `locations` | `square_location_id` (NN, indexed) | KEEP. Counterpoint Stores land here as separate rows; resolution via `external_identities`. |
| `customers` | `square_customer_id` (NN, indexed) | KEEP. Counterpoint customers land in same table; mediate via `external_identities`. |
| `products` | `square_item_id` (NN, indexed) | KEEP. Counterpoint Items same pattern. |
| `gift_cards` | `square_gift_card_id`, `square_created_at` | KEEP. Counterpoint gift cards via Document_GfcActivity. Rename `square_created_at` → `source_created_at` cosmetic later. |
| `transfer_orders` | `square_transfer_order_id`, `square_created_at`, `square_updated_at` | KEEP. Counterpoint transfers via Document with transfer DOC_TYP. |
| `subscriptions` | `square_subscription_id`, `square_created_at` | Square-only forever — Counterpoint has no subscription endpoint. |
| `bank_accounts` | `square_bank_account_id` | Square-only forever — no Counterpoint analog. |
| `square_oauth_tokens` (table) | Whole table is Square-shaped | KEEP. Build separate `counterpoint_credentials` table for Basic+APIKey storage. |
| `external_identities.entity_type` CHECK | `('employee','location','device','product','customer')` | EXTEND to add `item_category`, `vendor`, `transfer_order`, `document` for Counterpoint. |
| `source_systems` | reference table | INSERT `'counterpoint'` row. |
| `merchant_sources.source_code` | FK to `source_systems.code` | Already correct shape. Just add Counterpoint registrations. |
| `webhook_events.event_id` | docstring "Square event_id" | Generalize docstring. Counterpoint has no equivalent — unique key per pulled event. |
| `schema_fingerprints` | global, no `source` column | ADD `source: Mapped[str]` column. Source-aware fingerprinting. |
| `schema_drift_alerts` | same | Add `source` column for source-aware drift. |

### `sales` schema — what is Square-shaped

| Table | Square-shaped column | Recommended treatment |
|---|---|---|
| `transactions` | `square_product` (POS / INVOICES / VIRTUAL_TERMINAL / ONLINE_STORE), `external_id` doc, `order_id` doc, no `source_code` column | ADD `source_code` column (FK to `source_systems.code`). Rename `square_product` → `source_channel` later or leave + map Counterpoint values. The `source_type` enum (WEBHOOK/POLLING/BATCH) is fine but doesn't capture *which* source. |
| `disputes` | `square_dispute_id` | Square-only — no Counterpoint analog. |
| `timecards` | `square_timecard_id` | Square-only — Module L parked. |
| `gift_cards` (sales — gift card activity) | `square_activity_id` | KEEP, rename to `source_activity_id` long-term. |
| `terminal` (TerminalCheckout, TerminalRefund) | `square_checkout_id`, `square_refund_id`, `square_created_at` ×2, `square_updated_at` ×2 | Square-only — Counterpoint has no Terminal API. |
| `payouts` | `square_payout_id` | Square-only — no Counterpoint analog. |
| `cash_drawers` | `square_shift_id` | Square-only — no Counterpoint cash-drawer API. |
| `invoices` | `square_invoice_id`, `raw_square_object` (JSONB) | KEEP. Rename `raw_square_object` → `raw_source_object` or move to per-source JSONB. Counterpoint invoices come via Document. |
| `devices` | `square_device_id`, `raw_square_object` (JSONB) | KEEP. Same generalization. Counterpoint via Store_Station / Device_Config. |
| `loyalty` (LoyaltyAccount, LoyaltyEvent) | `square_loyalty_id`, `square_event_id` | Square-only — Counterpoint loyalty embedded in Customer record. |
| `inventory` | `square_adjustment_id` | KEEP. Counterpoint Inventory_ByLocation has its own ID. |
| `ingestion_log` | docstring "Square event_id or batch reference" | Already source-agnostic. Update doc. |

### `metrics` schema — what is Square-shaped

| Table | Square-shaped column | Recommended treatment |
|---|---|---|
| `dim_locations` | `square_location_id` | Same as `app.locations` — route through `external_identities`. |
| `dim_employees` | `square_employee_id` | Same. |

### Generalization shape — recommended

For columns that are upsert keys (`app.employees.square_employee_id`, `app.locations.square_location_id`, etc.):

- **KEEP the column** — it's a concrete forensic record and no harm staying.
- **Stop using it as the resolver path** — every read should go through `external_identities` (already implemented for writes per GRO-267, but reads bypass it).
- **Don't add `counterpoint_*` siblings** unless a column does double duty as a Square-specific forensic field (e.g., `raw_square_object` JSONB). For those, rename to `raw_source_object` over time.
- **Add `source_code` to `sales.transactions`** — currently the table can't tell a Square-sourced txn from a Counterpoint-sourced one. This is a gap.
- **Add `source` to `schema_fingerprints` + `schema_drift_alerts`** — source-aware drift detection is required to avoid false positives.

## 5. Behavioral assumptions register

Layer 3 findings, called out for architecture decisions before code.

1. **Push vs pull ingress.** TSP-01's HTTP-200 contract assumes a remote client that retries. Counterpoint pulls have no such client — when our poll fails, we retry. Decision: keep `webhooks_tsp.py` untouched, sibling `services/tsp/poll/counterpoint_poller.py` writes to the same Valkey stream, both feed the same four consumers. **Decision required:** what's the polling cadence per endpoint class? Documents = real-time-ish (60s?), Items = nightly, Customers = hourly?

2. **Hash anchor semantics.** Square's evidence chain anchors to "exact bytes Square sent". Counterpoint's anchor must be "exact bytes we received and stored". Hash the raw HTTP response body (Counterpoint API returns JSON), not a re-serialization. **Decision required:** is canonical JSON (sorted keys) acceptable, or do we hash the raw response bytes verbatim? Forensic admissibility differs.

3. **Idempotency key derivation.** Square has a globally-unique `event_id` per webhook. Counterpoint Documents have `(company, doc_typ, doc_no)`; Customers have `(company, customer_id)`; Items have `(company, item_id)`. **Decision required:** unify under `compute_idempotency_key(source, payload, event_type) -> str` — but Counterpoint pulls aren't "events", they're "snapshots of resources at time T". Do we generate an event from each pulled resource (potentially billions of duplicates), or only when state changes (requires diffing against last-seen state)?

4. **Multi-tenant assumption.** Square: 1 merchant = 1 OAuth token = 1 source_merchant_id. Counterpoint: 1 customer can have N companies, each with its own creds. **Decision required:** does "merchant" remain the unit, with a 1:N relationship to `counterpoint_company` rows? Or does the data model gain a `tenant → merchants → companies` layer? The current `Merchant.source_merchant_id UNIQUE` constraint is incompatible with multi-company-per-tenant.

5. **Schema-drift detection.** `_check_schema_fingerprint` works on top-level field names; Counterpoint payloads have a different shape and would pollute the drift table. **Decision required:** source-aware fingerprint algorithm (root keys for Square, full schema-walk for Counterpoint), and a migration to add `source` to `schema_fingerprints`.

6. **Stateless Chirp rule applicability.** C-009/C-010/C-011 are Square-payload-specific. **Decision required:** add `applicable_sources: set[str]` to each rule definition; gate `evaluate_stateless` on it. Counterpoint will need its own Tier 1 rule set (Module Q SDD §6.5 open question).

7. **Auto-Fox-case rule set.** `_AUTO_CASE_RULES` includes C-009 (Square-specific). When Counterpoint rules ship, decide which auto-create cases — likely a per-source whitelist.

## 6. Proposed Phase 0b scope (generalization work)

Ordered by dependency. Each step is a separate Linear issue.

1. **Register Counterpoint as a source.** Insert row into `source_systems` with `code='counterpoint'`. Extend `app.external_identities.ENTITY_TYPES` + CHECK constraint with new entity types. Add `source` column to `schema_fingerprints` + `schema_drift_alerts`. *(Effort: S; touches 3 migrations.)*

2. **Generalize merchant + auth.** Add `counterpoint_credentials` table (encrypted Basic + APIKey + base_url + company_alias). Build `CounterpointAuthService` (parallel to `SquareOAuthService`). Decide multi-company-per-tenant model — likely add `company_alias` to `merchant_sources.metadata_json` initially. *(Effort: M.)*

3. **Generalize the resolver layer.** Replace `Employee.square_employee_id` direct queries in `chirp/rule_engine.py:67-116, 1556-1603` and `tsp/consumers/sub2_parse.py:66-92, 199-285` with `external_identities`-mediated lookups. The `_id_cache` shape stays the same. Verify Square test suite still green. *(Effort: L; touches Chirp, dashboard_queries, chart_queries, metrics/dim_loader.)*

4. **Add `source_code` to `sales.transactions`.** Migration + backfill (existing Square rows get `source_code='square'`). Update parsers and `_build_models` to set it. *(Effort: M.)*

5. **Generalize the dispatch table.** Wrap `EVENT_ROUTES` + `PREFIX_ROUTES` into a per-source dict: `SOURCE_DISPATCH["square"] = {...}`. `resolve_route` takes (source, event_type). Build `SOURCE_DISPATCH["counterpoint"]` map for Counterpoint endpoint families. *(Effort: M.)*

6. **Generalize the stateless Chirp gate.** Replace `if source == "square":` in `webhooks_tsp.py:167` with a per-rule `applicable_sources` filter. *(Effort: S.)*

7. **Build the Counterpoint poller as a sibling ingress.** New `services/tsp/poll/counterpoint_poller.py` running on Celery / cron. Polls `/Documents`, `/Customers`, `/Items` per the SDD's MCP tool surface. Publishes to the same `canary:events` stream with the 9-field contract. Idempotency key derivation per source. *(Effort: XL; this is the bulk of Phase 1.)*

8. **Build Counterpoint validators + enrichers + parsers.** `validators/counterpoint.py`, `enrichers/counterpoint.py` (likely a no-op), `parsers/counterpoint_*.py` (Document, Customer, Item, etc.). Each is a sibling to its Square counterpart — *zero changes to Square parsers*. *(Effort: XL.)*

9. **Source-aware schema-drift detection.** Update `_check_schema_fingerprint` to accept `source` and route to source-specific field-extraction. Migrate existing Square fingerprints to `source='square'`. *(Effort: S.)*

## 7. What stays untouched

These pieces are intentionally Square-coupled and should remain so. They are the proof case.

- **`canary/services/tsp/validators/square.py`** — Square's HMAC-SHA256-over-(URL+body) is Square's spec; Counterpoint has its own validator file.
- **`canary/services/tsp/enrichers/square.py`** — Square Orders API enrichment for notification-only webhooks; Counterpoint pulls return full Documents and don't need this.
- **`canary/services/parsers/square_*.py`** (17 files) — every Square parser stays; Counterpoint parsers are siblings.
- **`canary/services/square_oauth.py`, `square_capability_explorer.py`, `square_sandbox_seeder.py`** — Square-specific service helpers; Counterpoint gets siblings.
- **`canary/blueprints/square_oauth_wired.py`, `square_explorer_wired.py`** — Square OAuth/explorer endpoints; Counterpoint gets a different blueprint (`counterpoint_connect_wired.py`).
- **`app.square_oauth_tokens` table** — Square OAuth-shaped; Counterpoint gets its own credentials table.
- **`canary/blueprints/webhooks_tsp.py`** as the *Square ingress* — keep this file Square-coupled; Counterpoint pulls live in a parallel `services/tsp/poll/` module that publishes to the same Valkey stream. The four consumers (sub1-sub4) are intentionally source-agnostic and should stay that way.
- **Square-only Chirp rules** — C-009 SQUARE_DELAY_HOLD, C-010 PARTIAL_AUTHORIZATION, C-011 NO_SALE_DETECTED — these read Square-specific fields and stay gated on `source == "square"` via `applicable_sources`.
- **Square-shaped table columns on Square-only domains** — `disputes.square_dispute_id`, `timecards.square_timecard_id`, `terminal.square_checkout_id`, `payouts.square_payout_id`, `cash_drawers.square_shift_id`, `loyalty.square_loyalty_id`, `subscriptions.square_subscription_id`, `bank_accounts.square_bank_account_id` — these tables map to Square endpoint families that have no Counterpoint analog. Stay Square-only.
- **`templates/auth/join.html`, `connect.html`, `welcome.html`** — Square OAuth onboarding flow; Counterpoint gets a parallel set of templates.
- **`scenarios`, `payload_factory`, `scenario_fire`, `scenario_runner`, `square_sandbox_seeder`** — test/lab tooling that uses Square sandbox by design. Out of audit scope; flagged for parity once a Counterpoint sandbox lands.

## 8. Coverage note

- **Out of audit scope (per charter):** `Canary/tests/`, `Canary/docs/`, migration history files (only current `canary/models/` state inspected), the GrowDirect platform repo outside `Canary/`.
- **Templates:** searched `templates/` (singular, repo root) — `canary/templates/` does not exist as a directory; the project's actual template dir is at `Canary/templates/`. ~70 Square hits in templates, all UI strings or Jinja conditionals on `square_env`. Cataloged at the family level (auth/, app/, ops/) rather than line-by-line because they are LOW severity and recommended approach is parallel template set, not refactor.
- **Static / JS:** searched `canary/static/` for `square` — no JS files reference Square. The `templates/app/owl.html` JS comment at line 305 (`/* GRO-237: UUID first, Square ID fallback */`) is the only Square-aware client code.
- **Models inspected fully:** all 31 files under `canary/models/{app,sales,metrics}/`. The 4 files under `canary/models/fox/` were not exhaustively read — Fox case-management is a layer above CRDM and references entity UUIDs, so it inherits whatever resolver model the rest of the system uses. Spot-checked `models/fox/` and confirmed no `square_*` columns there.
- **Service files inspected fully:** `services/webhook_dispatch.py`, `services/tsp/validators/square.py`, `services/tsp/enrichers/square.py`, `services/tsp/enrichers/__init__.py`, `services/tsp/stream_publisher.py`, `services/tsp/consumers/sub2_parse.py`, `services/chirp/rule_engine.py` (lines 1-200 + 1540-1620), `services/chirp/stateless_engine.py`, `services/raas/payload_normalizer.py`, `services/config_service.py:41-90`. Spot-checked: `services/condor/intelligence.py`, `services/identity/tools.py`, `services/dashboard_queries.py`, `services/chart_queries.py`, `services/metrics/dim_loader.py`, `services/scenario_fire.py`.
- **Skipped at the file-line level:** `services/parsers/square_*.py` (17 files) — these are by-design source-bound and stay that way; counted at the file level. `services/owl/search/registry.py:318,345,529` — three Square-shaped column references in the Owl search registry; flagged in Layer 2 with `square_product` and `square_item_id`.
- **Migration history:** intentionally not audited per charter. The model files reflect current state.
- **Ambiguous / needs founder clarification:**
  - Multi-company-per-tenant data model — split `Merchant` or use `MerchantSource.metadata_json`? (Per Counterpoint SDD §7.6.)
  - Hash-anchor semantics for pull mode — canonicalized JSON or raw response bytes? Forensic implications differ.
  - Idempotency for Counterpoint snapshot pulls — diff-based change detection vs. emit-event-per-pull? Volume implications.
