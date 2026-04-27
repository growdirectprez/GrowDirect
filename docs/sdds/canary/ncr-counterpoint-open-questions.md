---
id: sdd-cp-oq
title: NCR Counterpoint — Open Questions Register
status: living
version: 0.2.0
date: 2026-04-26
author: GrowDirect Engineering
linear: GRO-TBD
resolution-targets:
  - bart-call-2026-04-27
  - sandbox
  - deferred-phase-2
---

# NCR Counterpoint — Open Questions Register

Consolidated from all Counterpoint SDD drafts. Triaged by resolution target
for the Monday 2026-04-27 call with Bart McCleskey (Rapid Garden POS).

Questions that require sandbox access are blocked until lab/test credentials
are available. Questions marked "deferred" are out of scope for Phase 1.

---

## Priority: Bart Call (2026-04-27)

These questions require Bart's direct input — either topology knowledge,
product configuration know-how, or business-rule context. No sandbox access needed.

| ID | SDD | Question | Why it matters |
|---|---|---|---|
| O-OQ-03 | Onboarding | Cloud connectivity: does the Counterpoint REST endpoint require a VPN, tunnel, or on-prem agent? If it's behind a NAT, Canary cloud can't reach `server_host` directly. | Changes the entire deployment topology — may require a local agent binary rather than direct cloud polling. Critical before any onboarding UI is built. |
| O-OQ-01 | Onboarding | Installer UX: does the field rep use a Canary admin panel or a tenant-facing wizard? | Determines the auth model and who sees the credential entry form. |
| O-OQ-02 | Onboarding | Phase B entity scale: how large are customer rosters and item catalogs in a typical Rapid POS garden center deployment? 5K/10K or 50K+? | Drives task timeout settings and ETA display in the wizard. |
| O-OQ-05 | Onboarding | Vertical profiles: besides `garden_center`, which other verticals should be in scope at launch (hardware, florist, nursery-supply)? | Each vertical needs its own allow-list profile seeded at activation. |
| F-OQ-02 | PayCode | Garden center cash-vendor payments use CASH pay code. `Q-IS-02` allow-list classifies `DOC_TYP=RECVR + CASH tender` as legitimate — but does this apply to any CASH tender on a RECVR doc, or only specific `PAY_COD` values? Some stores configure separate vendor-payment pay codes. | Changes Q-IS-02 allow-list precision — the rule may need to match on PAY_COD string, not just canonical_type. |
| D-OQ-02 | Inventory | Write-off transactions: does a live-goods write-off generate a `PS_DOC` with a specific `DOC_TYP` (e.g., `ADJUST`), or is it a direct `IM_INV` update with no document? | If no document, inventory delta is the only signal — no corroborating transaction evidence. Changes Q-IS rule design significantly. |
| D-OQ-04 | Inventory | Snapshot frequency: are there rate limits or pagination requirements on `GET /InventoryLocations` for typical Rapid POS garden-center server hardware? | Hourly inventory polls may be too aggressive for an on-prem server. |
| A-OQ-01 | Auth | Per-user API permission levels: does the API user account need special permissions, or does the standard CP user work? | Test account must match production permission level — else sandbox passes but production fails. |
| A-OQ-02 | Auth | HTTP vs HTTPS: do any Rapid POS deployments run SSL on the Counterpoint REST endpoint? | Determines whether the client needs certificate validation / self-signed bypass. |
| S-OQ-02 | Store/Station | `PS_STR` pagination: does `GET /Stores` support pagination, or does it return all stores in one response? | If paginated, the store sync loop must handle cursor pagination. |
| S-OQ-03 | Store/Station | Station configuration sync interval: `PS_STA` changes rarely in production. Is daily sync too frequent, causing unnecessary load? | Tune poll interval for station config. |
| S-OQ-05 | Store/Station | `MIN_PFT_PCT` calibration: what values are typical in Rapid POS garden center configs (e.g., 15–25%)? Is this field consistently populated? | C-1501 `BELOW_CATEGORY_MARGIN` needs a real baseline, not a hardcoded default. |

---

## Priority: Sandbox Access

These require a live Counterpoint API to inspect. Blocked until test credentials
are available (expected from Bart after Monday call).

| ID | SDD | Question | Why it matters |
|---|---|---|---|
| F-OQ-01 | PayCode | Full `PAY_TYP` value space: sample data shows C, K, E, A, G, V, S, F. Are there production values not in this set (particularly garden center configs)? | `PAY_TYP_TO_CANONICAL` mapping completeness — unknown values fall through to `"other"`. |
| F-OQ-03 | PayCode | Foreign currency tenders (`IS_FOREIGN = True`): present in any US garden center deployment? | If not, `canonical_type = 'foreign'` is dead code for Phase 1. |
| D-OQ-01 | Inventory | `GET /InventoryLocations` without `Loc` filter: does the endpoint support bulk (all locations), or must you filter per-store? | If bulk is supported, per-store loop collapses to one call. |
| D-OQ-03 | Inventory | `QTY_ON_HND` for bulk/weighed items: are fractional quantities accurate for items like bulk soil or fertilizer sold by weight? | Shrinkage threshold calibration for weighed items. |
| T-OQ-01 | TSP | `PS_DOC_AUDIT_LOG` availability: is the audit log endpoint available in the Rapid POS sandbox? The field is present in CP documentation but may not be exposed in all server versions. | C-1401 `DOC_EDIT_AFTER_PAYMENT` requires audit log data. If unavailable, the rule cannot fire. |
| T-OQ-03 | TSP | `DOC_TYP` exhaustive list: sample documents show `SALE`, `RECVR`, `TRNSF`, `QUOTE`. Are there other `DOC_TYP` values in garden center deployments (LAYAWAY, ORDER, WORK_ORDER)? | DOC_TYP routing table completeness in the TSP adapter. |
| T-OQ-05 | TSP | Tax line structure: does `PS_DOC_TAX` include a tax code / jurisdiction field, or just a single tax_amt per document? | `transaction_taxes` schema completeness — may need a tax_code column if multiple rates appear. |
| R-OQ-01 | Customer | `CATEG_COD` taxonomy: what category codes are in use in a typical garden center deployment? | `cp_tier_definitions` seeding — the "Gold / Silver / Bronze" hierarchy assumed in the SDD may not match actual field values. |
| R-OQ-03 | Customer | Customer merge history: does Counterpoint track customer merges? If a `CUST_NO` is retired and redirected to another, the `external_identities` bridge will have stale FK mappings. | `cp_customer_profiles` UPSERT on merge scenarios. |
| A-OQ-03 | Auth | APIKey scope: is the APIKey a server-wide static key or per-user? | Credential model — one field vs. two, rotation scope. |
| A-OQ-04 | Auth | `GET /APIVersion` permission level: does this endpoint require admin-level auth, or does any valid CP API user reach it? | Connection-test reliability — if admin-only, a non-admin installer credential will fail the test incorrectly. |

---

## Priority: Deferred (Phase 2 or Later)

Out of scope for Phase 1. Logged here so they don't get lost.

| ID | SDD | Question | Reason for deferral |
|---|---|---|---|
| T-OQ-06 | TSP | Counterpoint Gift Card reconciliation: `PAY_TYP = G/V` tenders — does the Counterpoint server expose a gift card balance API? | Gift card fraud is Phase 2 scope. |
| T-OQ-07 | TSP | Loyalty point manipulation: `PS_DOC_LIN.LIN_TYP = LOYDSC` for loyalty discounts. Can a cashier apply an arbitrary loyalty discount without supervisor override? | Loyalty rule family is Phase 2. |
| R-OQ-04 | Customer | GDPR/CCPA deletion requests: if a customer requests data deletion, which `cp_*` fields must be purged vs. retained for financial audit? | Compliance / legal review needed. No US client has triggered this yet. |
| I-OQ-01 | Item Catalog | Bill-of-materials items: does Counterpoint expose BOM components in the `IM_ITEM` response? Garden centers occasionally build kits (potting soil + pot + plant). | Mix-and-match margin rule (Q-MM) is partially specified but BOM structure is unknown. |
| S-OQ-04 | Store/Station | Multi-company support: can a single Rapid POS deployment serve multiple `company_alias` values on one server (e.g., parent company + subsidiary)? | Multi-company within one merchant is an edge case; not in Phase 1 scope. |
| L-OQ-01 | (unwritten) | Labor module (Module L): the Counterpoint REST API has no labor/timecard endpoint. Is labor data in a separate system (e.g., Rapid POS time-clock module)? | Module L is Phase 6+ per the canonical Canary roadmap. Placeholder here for the gap. |

---

## Resolved

Questions that were open in earlier drafts and have since been answered.

| ID | SDD | Question | Resolution |
|---|---|---|---|
| R-OQ-02 | Customer, Store | Walk-in / anonymous customer sentinel: what is the value of the walk-in customer number? | Resolved by Store SDD: read `PS_STR_CFG_PS.WALK_IN_CUST_NO` per store. Default "CASH" if field absent. Do not hardcode. |
| S-OQ-01 | Store | Store discovery without `GET /Stores` list: how are stores enumerated on first sync? | Resolved by Store SDD: seed `cp_known_store_ids` from onboarding input; discovery cache-miss from `STR_ID` on Document parse. |

---

## How to Use This Register

1. **Before the Bart call:** print or share the "Priority: Bart Call" section.
   Each row is a standalone question — no SDD context needed to ask it.

2. **After sandbox access:** work through the "Priority: Sandbox" section
   systematically. Update the SDD open-question tables as each resolves.
   Mark resolved questions in the "Resolved" table above with a one-line
   summary.

3. **Updating SDDs:** when a question resolves, update the source SDD's
   `## Open Questions` table (change the row to a note or remove it), then
   move the question here into the Resolved section.

4. **Filing GRO issues:** each unresolved "Bart Call" question that requires
   a code change after resolution should become a GRO issue before
   implementation begins.
