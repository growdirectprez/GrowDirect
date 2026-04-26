# Canary for RapidPOS — Delivery Spec

**Status:** Draft v1 (2026-04-25). Author: Cowork session, grounded in GRO-558, GRO-560, the L3B audit (`docs/superpowers/specs/2026-04-25-mini-self-review.md` § Lens B), the Counterpoint API corpus (`Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/`), and the existing SDD (`docs/sdds/canary/ncr-counterpoint-retail-spine-integration.md`).
**Scope:** Get Canary running on a non-Square POS as a peer of Square — multi-cycle delivery plan. Not just the substrate; the full path to a live tenant.
**Linear epic:** GRO-558.
**Decision gate:** GRO-560 (NCR product-line ADR — Aloha vs Counterpoint vs Voyix). Spec assumes Counterpoint. If the ADR picks Aloha or Voyix, the directory names and parser shape change but the substrate contract does not.

## Governing thesis

Canary is structurally Square-shaped. Making it multi-POS is not a parallel rewrite, it is a **substrate decoupling pass** — extract the abstractions, refactor Square into a peer of itself, then onboard the second flavor against the same contract. The second flavor is harder than Square in two ways the substrate must accommodate: it is **poll-only** (Counterpoint has no webhooks) and it is **document-centric** rather than payment-centric (Counterpoint sales are Documents with Lines/Payments — Square is Payments with embedded line items). The substrate ABC must support both shapes, or we are back to a parallel rewrite.

## End-state definition

A specialty SMB retailer running NCR Counterpoint installs Canary, supplies their Counterpoint API base URL + company alias + service-account credentials + API key, and within minutes sees:

- Live transactions flowing into the EJ Spine
- Chirp scoring against the merchant's data — without Square code paths firing
- Owl answering natural-language questions about the retailer's sales
- Fox case management when chirps fire
- Dashboard rendering with the merchant's terminals, employees, products

Operational invariants:

- `POS_PROVIDER` is a tenant attribute, read once during request handling
- Adding a third POS provider requires no edits to `webhook_dispatch.py`, `chirp/rule_engine.py`, `tsp/consumers/`, or any model
- Square tenants continue running unchanged through every refactor (zero-downtime, zero behavior change)
- A new provider passes the same contract test suite Square does, or it does not ship

## The substrate problem (recap from L3B audit)

| Finding | What's wrong | Where (file) |
|---|---|---|
| L3B-01 | `webhook_dispatch.py` keys parsers by event type alone — no provider in the key | `canary/services/webhook_dispatch.py` |
| L3B-02 | TSP `sub2_parse` calls Square parsers directly — no dispatch by `source_code` | `canary/services/tsp/consumers/sub2_parse.py` |
| L3B-03 | Chirp rule engine has `_resolve_square_ids` — Square-specific lookup | `canary/services/chirp/rule_engine.py` |
| L3B-04 | Chirp lab + merchant simulator use Square-shaped fixtures | `canary/services/health_check/chirp_lab.py`, `canary/services/health_check/merchant_simulator.py` |
| L3B-05 | (Open — confirm scope) | TBD |
| L3B-06 | (Open — confirm scope) | TBD |
| L3B-07 | `transactions` table carries raw `square_*_id` columns | `canary/models/sales/transactions.py` |
| L3B-08 | `terminal` table carries raw `square_*_id` columns | `canary/models/sales/terminal.py` |
| L3B-09 | (Open — confirm scope) | TBD |
| L3B-10 | (Open — confirm scope) | TBD |

L3B-05/06/09/10 are listed in GRO-558 but not enumerated above — first task in cycle 7 is to read the audit and fill these rows. The substrate plan must address all ten findings or we ship a half-decoupled system.

## Counterpoint architectural reality

| Dimension | Square | Counterpoint |
|---|---|---|
| Inbound model | Webhook (event push) | Polling REST (we pull) |
| Auth | OAuth2 + per-merchant access token | HTTP Basic (`<CompanyAlias>.<UserName>:password`) + API Key header per request |
| Tenancy | One merchant = one Square account | One API server can host multiple Counterpoint companies; tenant key is `<CompanyAlias>` |
| Transaction shape | `Payment` with embedded `order_line_items` | `Document` (type=ticket/invoice) with `Document_Lines` + `Document_Payments` joined |
| Refunds | Webhook event (`refund.created`) | Negative-amount Document, polled |
| Caching | n/a — webhooks fire on change | 24-hour server-side cache; `ServerCache: no-cache` to bust |
| Date format | Unix epoch | ISO8601 |
| Typical merchant | 1–50 employees, single location | 5–500 employees, often multi-location, on-prem or hybrid hosting |
| Module overlap | T/R/N/Q (today) | T/R/N/Q + naturally extends to **D** (distribution/transfers), **C** (commercial/items), **J** (forecast/PO), **P** (pricing/promo) |

The poll-only constraint is the architectural pivot. The current `webhook_dispatch.py`-as-entry-point assumption is wrong as soon as you ship the second adapter. The substrate must accept either an adapter that emits CanonicalEvents from webhooks (Square) or an adapter that emits CanonicalEvents from a poll loop (Counterpoint), and from the perspective of the TSP, CRDM, Chirp, and Owl, these are indistinguishable.

The module-overlap row is the pleasant surprise: a Counterpoint adapter can light up four spine modules that Square cannot (D, C, J, P). The Counterpoint engagement is therefore an **opportunity to mature the spine itself**, not just a "second POS." Worth keeping in scope as a stretch — see Cycle 10 § Module Expansion.

## Delivery roadmap — four cycles

| Cycle | Window | Theme | Acceptance |
|---|---|---|---|
| **7** | Apr 30 – May 7 | Substrate scaffold + Square refactor | `POS_PROVIDER` knob; ABC + registry; contract tests; Square refactored into `pos/square/`; webhook dispatch provider-keyed; `_resolve_square_ids` gone; Counterpoint adapter directory exists with auth + Document parser stubs passing the same contract tests as Square |
| **8** | May 7 – May 14 | Model cutover + Counterpoint poll loop | `square_*_id` columns dropped from `transactions` + `terminal`, replaced by `external_identities`; back-compat shim for in-flight Square tenants; Counterpoint poll consumer running against sandbox; first Document → CanonicalEvent → CRDM round-trip |
| **9** | May 14 – May 21 | Onboarding + first live tenant | Tenant install flow for Counterpoint (credential collection, base URL, API key, connection test, seed fetch); Chirp rules firing on Counterpoint data; Owl + dashboard rendering Counterpoint tenant; smoke test — full TSP → CRDM → Chirp without Square code paths firing |
| **10** | May 21 – May 28 | Production readiness + spine expansion | `docs/runbooks/add-a-pos-provider.md`; SDD updates; monitoring + alerting for poll loop health; rate-limit + cache-control discipline; **stretch:** light up D/C/J/P spine modules from the Counterpoint Item/Inventory/PO/Pricing endpoints |

Four cycles ≈ 28 calendar days. Compression to three cycles is plausible if Cycle 8 model cutover slips into Cycle 9 (low-risk because it's invisible to tenants while back-compat shim is in place); compression to two cycles is unrealistic.

## Cycle 7 — detailed scope

**Sprint goal:** Square is one of N. Substrate ABC + registry + contract tests + Square refactor + Counterpoint scaffold all land green.

### Sub-issues (proposed under GRO-558)

| Seq | Title | Scope | File:line | Acceptance |
|---|---|---|---|---|
| 7.0 | NCR product-line ADR (GRO-560) | Pick the second flavor | `Canary-Retail-Brain/case-studies/canary-ncr-product-line-decision.md` | ADR file landed; `Brain/wiki/canary-architecture-decisions-index.md` updated |
| 7.1 | L3B audit completion sweep | Read `docs/superpowers/specs/2026-04-25-mini-self-review.md` Lens B; fill in L3B-05/06/09/10 in GRO-558 | audit doc | GRO-558 description updated with all 10 findings + file:line |
| 7.2 | Substrate scaffold | `canary/services/pos/__init__.py`, `pos/base.py` (POSAdapter ABC + CanonicalEvent dataclass + Fixture dataclass), `pos/registry.py` (single dict, `register_adapter()`, `get_adapter(provider)`), `pos/config.py` (`POS_PROVIDER` reader, single source) | new dir | ABC defined with webhook + poll surface; registry empty; config reads from env + tenant attribute |
| 7.3 | Contract test suite | `tests/contracts/test_pos_adapter.py` parameterized over `registry.providers()`; tests: ABC compliance, fixture loadability, webhook event-type uniqueness, poll-interval validity, auth-flow class instantiability | new test | Suite runs green with zero providers (vacuous); designed to fail when Square + Counterpoint registered without conformance |
| 7.4 | Square refactor — file moves (no behavior change) | Move `services/parsers/square_*.py` (16 files) → `services/pos/square/parsers/`; move `services/square_oauth.py` → `services/pos/square/oauth.py`; create `services/pos/square/adapter.py` registering Square as `POSAdapter` instance | 16 file moves + new adapter wrapper | Square tenants continue running; existing tests pass; contract suite green for Square |
| 7.5 | Webhook dispatch refactor (L3B-01) | `services/webhook_dispatch.py` — replace `EVENT_TYPE_PARSERS: dict[str, callable]` with `(provider, event_type) → callable` keyed registry; provider derived from request signature or URL path | `canary/services/webhook_dispatch.py` | Square webhooks still route correctly; Counterpoint adapter could register its (zero) webhook event types without conflict |
| 7.6 | TSP source-code dispatch (L3B-02) | `services/tsp/consumers/sub2_parse.py` — dispatch via the existing `source_code` field; remove hardcoded Square calls | `canary/services/tsp/consumers/sub2_parse.py` | Same Square behavior, but the dispatch function is provider-agnostic |
| 7.7 | Chirp ID resolution (L3B-03) | `services/chirp/rule_engine.py` — replace `_resolve_square_ids` with `_resolve_external_ids` against the `external_identities` table | `canary/services/chirp/rule_engine.py` | All 29 chirp rules pass against Square data; rule engine is provider-agnostic |
| 7.8 | Chirp lab + simulator abstraction (L3B-04) | `services/health_check/chirp_lab.py`, `services/health_check/merchant_simulator.py` — fixtures keyed by canonical event schema, not Square shape | two files | Lab passes for Square; lab fails-loud for an unregistered provider |
| 7.9 | Counterpoint adapter scaffold | `canary/services/pos/counterpoint/{__init__.py, adapter.py, auth.py, openapi_client.py, parsers/document.py, parsers/customer.py, parsers/item.py}`. `auth.py` implements Basic + API key header injection per `Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/Basics/Requests.md`. Parsers are stubs that pass the contract tests but produce empty CanonicalEvents | new dir | Counterpoint registered in adapter registry; contract test suite green; `POS_PROVIDER=counterpoint` with empty data does not crash |
| 7.10 | CLAUDE.md sync (GRO-556) | Auth section, file layout, mini steady-state | `CLAUDE.md` | Ride-along; demo-readiness |

### Cycle 7 risks

The audit findings L3B-05/06/09/10 are not yet enumerated; if any of them touches a model or service we did not plan for, sequence 7.1 will slip into 7.4–7.8. Bundle 7.1 into Day 1 to surface the surprise early.

The 16-file Square parser move (7.4) is mechanically large — it touches imports across `tsp/`, `chirp/`, `webhook_dispatch.py`, `health_check/`, possibly UI templates. Use `git mv`, do it in a single commit per parser, run the test suite after each. If imports drift across more than three other directories, split 7.4 into 7.4a (parsers) and 7.4b (oauth) to avoid one giant PR.

### Out of scope for Cycle 7

Models cutover (L3B-07/08) deferred to Cycle 8. Counterpoint poll loop deferred to Cycle 8. Counterpoint live data deferred to Cycle 9. Documentation (runbook + SDD update) folded into the relevant cycle's PR descriptions, not a standalone task.

## Cycle 8 — Model cutover + Counterpoint poll loop

**Sprint goal:** Models are provider-agnostic. Counterpoint sandbox data flows through the substrate end-to-end (TSP → CRDM → Chirp), even if no live tenant exists yet.

### Sub-issues (proposed)

| Seq | Title | Scope |
|---|---|---|
| 8.1 | Models migration — drop `square_*_id`, link via `external_identities` | Alembic migration; `canary/models/sales/transactions.py`, `canary/models/sales/terminal.py`. Back-compat shim: properties on the models that read from `external_identities` and continue to expose `square_payment_id` etc. for any caller not yet refactored. Three-phase: add columns, dual-write, drop columns. |
| 8.2 | Caller refactor — eliminate direct `square_*_id` reads | Sweep all `.square_*_id` references across `canary/`; replace with `external_identities` lookups. Likely 30–60 sites. |
| 8.3 | Counterpoint poll consumer | New TSP consumer: `tsp/consumers/poll_counterpoint.py`. Reads `pos_tenant_credentials` table for active Counterpoint tenants, polls Documents/Customers/Items per their adapter's `poll_intervals()`, publishes CanonicalEvents to `canary:events`. Watermark per (tenant, entity) to support `since` filtering. |
| 8.4 | Counterpoint Document parser — production | Map Document + Document_Lines + Document_Payments + Document_Note + Document_Contact → CanonicalEvent for transaction. Cover invoice, ticket, return Document types. |
| 8.5 | Counterpoint Customer + Item parsers | Customer → CanonicalEvent for customer create/update. Item → CanonicalEvent for product (light up C-commercial spine module). |
| 8.6 | Sandbox round-trip test | `tests/integration/test_counterpoint_round_trip.py` — fixture Counterpoint sandbox responses, run through poll consumer, assert CRDM rows + chirp scoring. |
| 8.7 | Polling discipline | Rate-limit awareness, exponential backoff on 429, `ServerCache: no-cache` only when fresh data demanded, watermark-driven incremental polls. |

### Cycle 8 risks

Caller refactor (8.2) sweep size is unknown until we grep — could be 30 sites, could be 200. Time-box at 2 days; if not done, ship the back-compat shim long-term and call the cutover "phased."

Counterpoint sandbox availability — confirmed via `Brain/wiki/ncr-counterpoint-sandbox-setup-checklist.md` exists, but does the founder/team have credentials? If not, 8.3+ block on getting them. Surface this in Cycle 7 retro.

## Cycle 9 — Onboarding + first live tenant

**Sprint goal:** A real Counterpoint merchant can install Canary, connect, and see their data. End-to-end smoke test passes with Square code paths confirmed not firing.

### Sub-issues (proposed)

| Seq | Title | Scope |
|---|---|---|
| 9.1 | Per-tenant POS_PROVIDER selection | Tenant-level config: `tenants.pos_provider` column, set at install. Substrate reads it, not env. |
| 9.2 | Counterpoint onboarding UI | New install path alongside Square OAuth. Form: API base URL, company alias, service-account user, password, API key. Connection test button. On success, fetch seed (stores, stations, items, customers) and confirm tenant ready. |
| 9.3 | Credentials vault | Store per-tenant Counterpoint credentials encrypted in `pos_tenant_credentials`. Rotation interface. |
| 9.4 | Chirp rules pass on Counterpoint data | Validate all 29 chirp rules fire correctly on Counterpoint Document shape. Patch any that broke during the model cutover. |
| 9.5 | Owl + dashboard tenant-aware | Owl prompts and dashboard tiles render correctly for `pos_provider=counterpoint`. No `square_*` field references in templates. |
| 9.6 | Production smoke test | Pick a target merchant (Solex worked example? a beta partner?). Run the install flow, watch one transaction flow end-to-end, verify zero Square code paths fire (audit log + grep). |
| 9.7 | Cutover playbook | What to do if Counterpoint goes wrong — rollback, support runbook, escalation. |

### Cycle 9 risks

The first live tenant is a partnership conversation, not just engineering. Cycle 7's GRO-560 ADR should name the target merchant or merchant profile so the engineering side has someone real to test against. Without a target, 9.6 has nothing to smoke.

Counterpoint deployment models — some installs are on-prem with no public IP. The Canary backend may not be able to reach the Counterpoint API server. If so, polling is impossible without a customer-side agent (or a tunnel). Surface this constraint in 9.2 design; may push the first live tenant to a hosted-Counterpoint customer.

## Cycle 10 — Production readiness + spine expansion

**Sprint goal:** Onboarding the third POS provider is a documented exercise, not a research project. Stretch: the Counterpoint adapter lights up new spine modules.

### Sub-issues (proposed)

| Seq | Title | Scope |
|---|---|---|
| 10.1 | `docs/runbooks/add-a-pos-provider.md` | Step-by-step: ABC implementation, registry registration, contract test pass, model wiring, onboarding UI, credential storage, smoke test. The next provider takes weeks not months. |
| 10.2 | SDD update | Refresh `docs/sdds/canary/ncr-counterpoint-retail-spine-integration.md` with as-built; add `docs/sdds/canary/pos-adapter-substrate.md` describing the contract |
| 10.3 | Poll loop monitoring | Health check per tenant (last-successful-poll timestamps), alerting when a tenant goes silent, dashboard for ops |
| 10.4 | Rate-limit + cache discipline audit | Confirm we don't hammer the Counterpoint API server during peak hours. Per-tenant poll budgets. |
| 10.5 | **Stretch — Distribution module (D)** | Counterpoint has Inventory_ByLocation + Items_ByLocation + transfer-style endpoints. Light up the D module from this data. |
| 10.6 | **Stretch — Commercial module (C)** | Counterpoint Items + ItemCategories + ItemSerial — full product/category hierarchy. Square has none of this; Counterpoint adapter teaches Canary about products. |
| 10.7 | **Stretch — Forecast/PO module (J)** | Counterpoint has VendorItem + Document type=PO. Light up the J module from polled PO data. |
| 10.8 | **Stretch — Pricing module (P)** | Counterpoint pricing endpoints (need to confirm in API) — promo + price overrides. |

### Cycle 10 risks

Stretch items are the spine maturing; if they slip, no harm. But J and P specifically are Counterpoint-native data Canary has never had — flagging them as "stretch" risks losing the differentiator. Recommend treating 10.5 + 10.6 as committed and 10.7 + 10.8 as stretch.

## Open questions to resolve in Cycle 7

1. **GRO-560 outcome.** Counterpoint vs Aloha vs Voyix vs CounterPro. Spec assumes Counterpoint; if Aloha (restaurant), the Document model differs (orders + modifiers + courses), and the merchant profile target shifts to restaurants — Q-loss-prevention rules need restaurant-specific tuning.
2. **L3B-05/06/09/10 scope.** Read the audit; fill in. Without these, the substrate refactor is incomplete.
3. **Counterpoint sandbox access.** Do we have credentials? If not, who do we ask?
4. **Target first live tenant.** Specialty retail SMB on Counterpoint — name the merchant or the profile in the GRO-560 ADR. Without a target, Cycle 9 smoke test has no aim.
5. **Webhook vs poll architectural commitment.** Confirm via Counterpoint API docs that there is truly no webhook surface — the API corpus we have suggests poll-only, but a managed-Counterpoint cloud offering may have a webhook bus we haven't found.
6. **On-prem reachability.** Customers running Counterpoint on local infrastructure — can the Canary backend reach them? If not, the polling architecture needs a customer-side agent. This constrains 9.2 onboarding design.
7. **Credential rotation cadence.** Counterpoint passwords change. How often? Who rotates? What's the failure mode when they don't?

## Risks worth pricing in

The L3B audit names ten findings but explicitly enumerates only six in GRO-558. The other four are unknowns; budget Cycle 7 day 1 for a complete read.

The Counterpoint adapter has more parsing surface than Square because Counterpoint exposes more entity types (Items, Inventory, Vendors, POs). Cycle 8's "production parsers" task could be 5 parsers or 15. Spike before sizing.

The model cutover (8.1, 8.2) touches every callsite that reads `transaction.square_payment_id` or `terminal.square_device_id`. The back-compat shim makes this safer but adds permanent surface area to the models. Decide explicitly whether the shim is temporary (delete after one quarter) or permanent (forever-stable contract for legacy callers). Recommend temporary, with deletion ticketed for Cycle 14.

The first live Counterpoint tenant is a partnership relationship, not just a technical install. Cycle 9 should pull the founder into a conversation about merchant acquisition early — engineering throughput stalls without a real target.

## Appendix A — POSAdapter contract sketch

```python
# canary/services/pos/base.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Iterator

@dataclass(frozen=True)
class CanonicalEvent:
    """Provider-agnostic event that flows through TSP → CRDM → Chirp."""
    provider: str                 # "square", "counterpoint", ...
    event_type: str               # "transaction.created", "customer.updated", ...
    tenant_id: str
    occurred_at: datetime
    external_id: str              # provider's ID — stored in external_identities
    payload: dict                 # canonical-shape payload, not provider-shape

@dataclass(frozen=True)
class Fixture:
    """Seed data for a fresh tenant — items, employees, locations."""
    entity_type: str
    rows: list[dict]

class POSAdapter(ABC):
    provider: str  # class-level identifier — "square", "counterpoint"

    # --- Webhook surface (Square, Aloha if it has webhooks) ---
    @abstractmethod
    def webhook_event_types(self) -> set[str]:
        """Event types this adapter accepts on webhook ingress. Empty set = poll-only."""
        ...

    @abstractmethod
    def parse_webhook(self, raw_event: dict) -> CanonicalEvent | None:
        """Convert a raw webhook payload into a CanonicalEvent. None = ignore."""
        ...

    # --- Polling surface (Counterpoint, any future poll adapter) ---
    @abstractmethod
    def poll_intervals(self) -> dict[str, timedelta]:
        """Per-entity-type polling cadence. Empty dict = webhook-only."""
        ...

    @abstractmethod
    def poll(self, tenant_id: str, entity_type: str, since: datetime) -> Iterator[CanonicalEvent]:
        """Pull events for one entity type since the watermark."""
        ...

    # --- Common ---
    @abstractmethod
    def auth_flow_class(self) -> type:
        """The class that handles credential collection + connection test."""
        ...

    @abstractmethod
    def seed_data(self, tenant_id: str) -> Iterator[Fixture]:
        """Initial data fetched at install time (stores, employees, products)."""
        ...
```

An adapter can implement webhook-only (Square: empty `poll_intervals`), poll-only (Counterpoint: empty `webhook_event_types`), or both. The TSP doesn't care; it just receives CanonicalEvents.

## Appendix B — Counterpoint → CanonicalEvent mapping (preview)

| Counterpoint entity | Endpoint | Canonical event type | Spine module |
|---|---|---|---|
| Document (type=ticket, paid) | `GET /Document` | `transaction.created` | T |
| Document (type=ticket, void) | `GET /Document` (filter) | `transaction.voided` | T, Q |
| Document (negative ticket) | `GET /Document` | `refund.created` | T, Q |
| Document_Lines | `GET /Document` (joined) | (embedded in transaction.created) | T |
| Document_Payments | `GET /Document` (joined) | (embedded in transaction.created) | T |
| Customer | `GET /Customers` | `customer.created` / `customer.updated` | R |
| Customer_Address, Customer_Card, Customer_Note | `GET /Customer/{id}` | `customer.attribute_updated` | R |
| Store, Store_Station | `GET /Stores`, `GET /Store/{id}/Station` | `terminal.registered` | N |
| Item, ItemCategories, ItemSerial | `GET /Items`, `GET /Item/{id}` | `product.created`, `product.serialized` | C |
| Inventory_ByLocation | `GET /Inventory/ByLocation` | `inventory.snapshot` | D |
| User, UserRoles | `GET /Users`, `GET /User/{id}/Roles` | `employee.registered` | (no current spine module — future) |
| GiftCard, GiftCardCode | `GET /GiftCards` | `gift_card.activity` | T, Q |
| Document (type=PO) | `GET /Document` (filter) | `purchase_order.created` | J |
| TaxCodes, PayCodes | `GET /TaxCodes`, `GET /PayCodes` | (config — seed_data, not events) | F |

Any mapping marked "future" or "config" is intentionally out of scope until the spine module is live. The Cycle 8 production parser scope covers Document + Customer + Item + Store/Station + User. The rest comes in Cycle 10 stretch or a later expansion.

## Appendix C — Files that already exist (do not recreate)

- `docs/sdds/canary/ncr-counterpoint-retail-spine-integration.md` — primary SDD
- `docs/sdds/canary/ncr-counterpoint-square-coupling-audit.md` — coupling audit
- `docs/sdds/canary/ncr-counterpoint-openapi.yaml` — derived OpenAPI spec
- `Brain/wiki/ncr-counterpoint-api-reference.md`
- `Brain/wiki/ncr-counterpoint-connection-runbook.md`
- `Brain/wiki/ncr-counterpoint-document-model.md`
- `Brain/wiki/ncr-counterpoint-endpoint-spine-map.md`
- `Brain/wiki/ncr-counterpoint-phase-0-context-brief.md`
- `Brain/wiki/ncr-counterpoint-rapid-pos-relationship.md`
- `Brain/wiki/ncr-counterpoint-sandbox-setup-checklist.md`

Each will get an "as-built" pass in Cycle 10's documentation update. Until then, treat them as design intent, not as-implemented reality.
