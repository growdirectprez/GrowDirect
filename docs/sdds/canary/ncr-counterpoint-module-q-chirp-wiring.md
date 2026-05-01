---
id: sdd-cp-module-q-chirp
title: NCR Counterpoint — Module Q Chirp Rule Wiring
status: draft-1
version: 0.1.0
date: 2026-04-26
author: GrowDirect Engineering
linear: GRO-TBD
companion-sdds:
  - docs/sdds/canary/ncr-counterpoint-tsp-adapter.md
  - docs/sdds/canary/ncr-counterpoint-customer-adapter.md
  - docs/sdds/canary/ncr-counterpoint-item-catalog-adapter.md
  - Canary/docs/sdds/v2/data-model.md
source-wiki:
  - Brain/wiki/canary-module-q-counterpoint-rule-catalog.md
---

# NCR Counterpoint — Module Q Chirp Rule Wiring

## 1. Purpose

The wiki article `Brain/wiki/canary-module-q-counterpoint-rule-catalog.md`
defines the full Counterpoint LP rule catalog (30+ rules across 12 families).
This SDD is its engineering complement: it specifies how those rules enter
Chirp's live detection stack — the `DetectionRule` catalog entries, new rule
categories, substrate table joins, `rule_definitions.py` extension pattern,
and deployment phasing.

The wiki defines WHAT to detect. This document specifies HOW it runs.

## 2. New Chirp rule categories (additions to `DetectionRule.category`)

The existing category enum in `app.detection_rules`:

```
payment | cash_drawer | order | timecard | void | inventory | gift_card |
loyalty | composite | dispute | invoice
```

New categories added for Counterpoint substrate:

```
discount_markdown  — discount/markdown abuse (Q-DM series)
audit_trail        — Document audit log anomalies (Q-AT series)
margin_erosion     — below-cost / below-category-margin sales (Q-ME series)
inventory_shrink   — receiver/transfer/write-off anomalies (Q-IS series)
tax_compliance     — multi-authority tax + exempt-customer abuse (Q-TC series)
customer_tier      — tier assignment and pricing tier abuse (Q-CT series)
mix_and_match      — mix-match exploitation (Q-MM series)
compliance         — regulatory / restricted-item (Q-COMP series)
commercial_b2b     — B2B credit and AR anomalies (Q-C series)
```

The existing `void` and `cash_drawer` categories absorb the Counterpoint
void/return and drawer/session rule families (Q-VR and Q-DS map to existing
categories to avoid schema proliferation).

## 3. Rule ID scheme

Counterpoint rules use 4-digit C-codes to distinguish them from Square
rules (3-digit or letter-prefix):

| Wiki family | Chirp category | C-code range |
|---|---|---|
| Q-DM (Discount/Markdown) | discount_markdown | C-1001 to C-1099 |
| Q-VR (Void/Return) | void | C-1101 to C-1199 (extends existing void) |
| Q-TM (Tender Mix) | payment | C-1201 to C-1299 (extends existing payment) |
| Q-DS (Drawer/Session) | cash_drawer | C-1301 to C-1399 (extends existing) |
| Q-AT (Audit Trail) | audit_trail | C-1401 to C-1499 |
| Q-ME (Margin Erosion) | margin_erosion | C-1501 to C-1599 |
| Q-IS (Inventory/Shrink) | inventory_shrink | C-1601 to C-1699 |
| Q-TC (Tax/Compliance) | tax_compliance | C-1701 to C-1799 |
| Q-CT (Customer Tier) | customer_tier | C-1801 to C-1899 |
| Q-MM (Mix and Match) | mix_and_match | C-1901 to C-1999 |
| Q-COMP (Compliance) | compliance | C-2001 to C-2099 |
| Q-C (Commercial B2B) | commercial_b2b | C-2101 to C-2199 |

## 4. Priority rules — Phase 1 deployment (Cycle 9)

Not all rules deploy on day one. Phase 1 (Cycle 9) ships the rules that
have the highest signal-to-noise ratio and lowest calibration burden.

**Phase 1 rules (ship at go-live):**

| C-ID | Wiki ID | Name | Severity | Category |
|---|---|---|---|---|
| C-1001 | Q-DM-01 | DISCOUNT_CAP_EXCEEDED | medium | discount_markdown |
| C-1003 | Q-DM-03 | BELOW_COST_SALE | high | discount_markdown |
| C-1101 | Q-VR-01 | VOID_WITHOUT_ORIGINAL | high | void |
| C-1102 | Q-VR-02 | RETURN_WITHOUT_ORIGINAL | high | void |
| C-1103 | Q-VR-03 | SAME_EMPLOYEE_VOID_CLUSTER | medium | void |
| C-1401 | Q-AT-01 | DOC_EDIT_AFTER_PAYMENT | medium | audit_trail |
| C-1501 | Q-ME-01 | BELOW_CATEGORY_MARGIN | low | margin_erosion |
| C-1502 | Q-ME-02 | FREE_ITEM_OVERRIDE | medium | margin_erosion |
| C-2001 | Q-COMP | RESTRICTED_ITEM_NO_OVERRIDE | critical | compliance |

**Phase 2 rules (after 30-day calibration window):**

| C-ID | Wiki ID | Name | Severity | Category |
|---|---|---|---|---|
| C-1002 | Q-DM-02 | MARKDOWN_AND_BUY | high | discount_markdown |
| C-1201 | Q-TM-01 | CASH_ONLY_REGISTER | low | payment |
| C-1202 | Q-TM-02 | TENDER_SWAP | high | payment |
| C-1301 | Q-DS-01 | DRAWER_SESSION_SHRINKAGE | low | cash_drawer |
| C-1302 | Q-DS-02 | POST_CLOSE_ACTIVITY | medium | cash_drawer |
| C-1402 | Q-AT-02 | CROSS_STATION_DOCUMENT | medium | audit_trail |
| C-1601 | Q-IS-01 | RECEIVER_PO_DISCREPANCY | low | inventory_shrink |
| C-1701 | Q-TC-01 | MULTI_AUTH_TAX_MISMATCH | medium | tax_compliance |
| C-1801 | Q-CT-01 | WHOLESALE_ON_RETAIL_PATTERN | low | customer_tier |
| C-1802 | Q-CT-02 | TIER_REASSIGNMENT_PRE_PURCHASE | high | customer_tier |
| C-1901 | Q-MM-01 | MIX_MATCH_BELOW_COST | medium | mix_and_match |
| C-2101 | Q-M-01 | AT_LIMIT_ACCOUNT_TRANSACTING | medium | commercial_b2b |
| C-2103 | Q-M-03 | AR_PAST_DUE_THRESHOLD | medium | commercial_b2b |

**Informational-only rules (never alert; analytics/trend only):**

| C-ID | Wiki ID | Name | Category |
|---|---|---|---|
| C-1602 | Q-IS-02 | CASH_VENDOR_RECEIVE_CLASSIFY | inventory_shrink |
| C-1604 | Q-IS-04 | LIVE_GOODS_WRITEOFF_TRACKING | inventory_shrink |

## 5. rule_definitions.py extension pattern

The Counterpoint rules extend `Canary/canary/services/chirp/rule_definitions.py`
using the same `RuleSpec` dataclass pattern as the Square rules.

```python
# In rule_definitions.py, after the existing rule sections:

# --- Counterpoint: Discount/Markdown rules (C-1001 to C-1099) ---
RuleSpec(
    rule_id="C-1001", name="DISCOUNT_CAP_EXCEEDED",
    category="discount_markdown", severity="medium",
    description=(
        "Per-line discount exceeds store MAX_DISC_AMT or MAX_DISC_PCT "
        "without manager override. Source: PS_DOC_LIN.HAS_PRC_OVRD, "
        "PS_STR_CFG_PS.MAX_DISC_AMT/PCT."
    ),
    default_threshold=json.dumps({
        "multiplier_of_max": 1.0,
        "require_manager_override": True,
    }),
),
RuleSpec(
    rule_id="C-1003", name="BELOW_COST_SALE",
    category="discount_markdown", severity="high",
    description=(
        "Transaction line sold below last cost via price override. "
        "Source: PS_DOC_LIN.EXT_PRC < IM_ITEM.LST_COST, "
        "PS_DOC_LIN.HAS_PRC_OVRD = 'Y'."
    ),
    default_threshold=json.dumps({
        "cost_basis": "LST_COST",
        "loss_threshold_dollars": 50.0,
    }),
),
# --- Counterpoint: Void/Return (C-1101 to C-1199) ---
RuleSpec(
    rule_id="C-1101", name="VOID_WITHOUT_ORIGINAL",
    category="void", severity="high",
    description=(
        "Void document with no linked original ticket in "
        "PS_DOC_HDR_ORIG_DOC. Indicates unlinked void workflow."
    ),
    default_threshold=json.dumps({
        "tolerance_minutes": 0,
        "require_reason_code": True,
    }),
),
RuleSpec(
    rule_id="C-1102", name="RETURN_WITHOUT_ORIGINAL",
    category="void", severity="high",
    description=(
        "Return lines (LIN_TYP=R) with no original-doc reference "
        "and no receipt-lookup in audit trail."
    ),
    default_threshold=json.dumps({
        "customer_known_required": True,
    }),
),
# --- Counterpoint: Margin Erosion (C-1501 to C-1599) ---
RuleSpec(
    rule_id="C-1501", name="BELOW_CATEGORY_MARGIN",
    category="margin_erosion", severity="low",
    description=(
        "Transaction lines whose (price-cost)/price < category MIN_PFT_PCT. "
        "Source: IM_CATEG_COD.MIN_PFT_PCT, PS_DOC_LIN.EXT_PRC, EXT_COST."
    ),
    default_threshold=json.dumps({
        "aggregation_window_days": 7,
        "volume_threshold_dollars": 1000.0,
    }),
),
RuleSpec(
    rule_id="C-1502", name="FREE_ITEM_OVERRIDE",
    category="margin_erosion", severity="medium",
    description="Items priced to $0 via manual override (HAS_PRC_OVRD=Y, EXT_PRC=0).",
    default_threshold=json.dumps({
        "count_per_employee_per_session": 3,
    }),
),
# --- Counterpoint: Compliance (C-2001 to C-2099) ---
RuleSpec(
    rule_id="C-2001", name="RESTRICTED_ITEM_NO_OVERRIDE",
    category="compliance", severity="critical",
    description=(
        "Restricted item (prop_65, epa_pesticide, epa_herbicide, "
        "restricted_chemical, age_restricted) sold without the "
        "'restricted_items_authorized' override on the Document."
    ),
    default_threshold=json.dumps({
        "flag_set": ["prop_65", "epa_pesticide", "epa_herbicide",
                     "restricted_chemical", "age_restricted"],
        "required_override_code": "restricted_items_authorized",
        "evidence_retention_days": 2555,
    }),
),
```

The full list of rules follows the same pattern. All rules are inactive-by-default
(`is_active=False`) when first seeded for Counterpoint merchants — operators
promote them through the dry-run → observation → active lifecycle
(see §7 Deployment phasing).

## 6. Substrate join map

Each rule requires a specific join path through the CRDM tables. This is the
engineering-critical section: wrong joins → false rules, missed detections.

### Discount/margin rules (C-1001, C-1003, C-1501, C-1502)

```sql
-- Base join for discount/margin rules
SELECT
    t.id               AS transaction_id,
    t.merchant_id,
    t.store_id         AS str_id,
    t.employee_id      AS usr_id,
    t.occurred_at,
    li.id              AS line_item_id,
    li.catalog_object_id AS item_no,
    li.base_price_cents / 100.0 AS ext_prc,
    li.total_discount_cents / 100.0 AS disc_amt,
    li.is_voided,
    -- Item catalog
    ci.lst_cost,
    ci.prc_1           AS reg_prc,
    ci.is_discntbl,
    ci.prompt_for_prc,
    ci.categ_cod,
    -- Category margin targets
    cat.min_pft_pct,
    cat.trgt_pft_pct,
    -- Store thresholds (from Store adapter — Phase 2)
    -- sto.max_disc_pct,
    -- sto.max_disc_amt,
    -- Audit substrate
    t.source_code
FROM sales.transactions t
JOIN sales.transaction_line_items li ON li.transaction_id = t.id
LEFT JOIN app.external_identities ei
    ON ei.merchant_id = t.merchant_id
   AND ei.source_code = 'counterpoint'
   AND ei.entity_type = 'product'
   AND ei.external_id = li.catalog_object_id
LEFT JOIN app.cp_item_catalog ci
    ON ci.id = ei.entity_id::uuid
LEFT JOIN app.cp_item_categories cat
    ON cat.merchant_id = ci.merchant_id
   AND cat.categ_cod   = ci.categ_cod
WHERE t.merchant_id = :merchant_id
  AND t.source_code  = 'counterpoint'
  AND t.occurred_at  >= :window_start;
```

### Void/return rules (C-1101, C-1102)

```sql
-- Void transactions with no original-doc reference
SELECT
    t.id               AS transaction_id,
    t.merchant_id,
    t.store_id,
    t.employee_id,
    t.occurred_at,
    t.transaction_type,
    dr.original_doc_id  -- NULL = no original linked
FROM sales.transactions t
LEFT JOIN sales.document_original_refs dr
    ON dr.transaction_id = t.id
WHERE t.merchant_id    = :merchant_id
  AND t.source_code    = 'counterpoint'
  AND t.transaction_type IN ('void', 'return')
  AND dr.original_doc_id IS NULL
  AND t.occurred_at   >= :window_start;
```

### Audit trail rules (C-1401)

```sql
-- Documents edited after payment was recorded (IS_DOC_COMMITTED=Y)
SELECT
    al.transaction_id,
    al.log_seq_no,
    al.logged_at,
    al.user_id,
    al.activity,
    al.log_entry,
    t.is_committed
FROM sales.transaction_audit_log al
JOIN sales.transactions t ON t.id = al.transaction_id
WHERE t.merchant_id = :merchant_id
  AND t.is_committed = TRUE
  AND al.logged_at > t.occurred_at  -- edited after transaction close
  AND t.occurred_at >= :window_start;
```

### Margin erosion (C-1501, C-1502)

Margin erosion rules use the base discount/margin join (§6 first query).
The C-1501 filter: `(ext_prc - lst_cost) / NULLIF(ext_prc, 0) < min_pft_pct / 100`.
The C-1502 filter: `ext_prc = 0 AND disc_amt > 0`.

### Compliance (C-2001)

The restricted item flag must be stored somewhere Chirp can read. Two options:
1. A `cp_item_catalog.restricted_flags` JSONB column (preferred — inline with item)
2. A separate `cp_item_restricted_flags` table (more normalized)

**Recommendation:** JSONB column on `cp_item_catalog`:

```sql
ALTER TABLE app.cp_item_catalog
ADD COLUMN restricted_flags JSONB DEFAULT '[]'::jsonb;

CREATE INDEX idx_cp_item_restricted ON app.cp_item_catalog
    USING GIN (restricted_flags)
    WHERE restricted_flags != '[]'::jsonb;
```

This column is populated during onboarding via a Rapid POS / Bart-assisted
config step: the operator tags items with their applicable restriction flags
through Canary's onboarding UI (or via a bulk import from the customer's
existing compliance mapping). Counterpoint does not natively carry these flags
in its API surface.

The `document_original_refs` audit log provides the override evidence:
if a Document has an audit entry with `ACTIV = 'restricted_items_authorized'`,
the sale is compliant.

```sql
SELECT
    t.id, t.merchant_id, t.store_id, t.employee_id, t.occurred_at,
    li.catalog_object_id AS item_no,
    ci.restricted_flags,
    bool_or(al.activity = 'restricted_items_authorized') AS has_override
FROM sales.transactions t
JOIN sales.transaction_line_items li ON li.transaction_id = t.id
LEFT JOIN app.external_identities ei
    ON ei.merchant_id = t.merchant_id AND ei.source_code = 'counterpoint'
   AND ei.entity_type = 'product' AND ei.external_id = li.catalog_object_id
LEFT JOIN app.cp_item_catalog ci ON ci.id = ei.entity_id::uuid
LEFT JOIN sales.transaction_audit_log al ON al.transaction_id = t.id
WHERE t.merchant_id = :merchant_id
  AND t.source_code = 'counterpoint'
  AND ci.restricted_flags != '[]'::jsonb
GROUP BY t.id, t.merchant_id, t.store_id, t.employee_id, t.occurred_at,
         li.catalog_object_id, ci.restricted_flags
HAVING NOT bool_or(al.activity = 'restricted_items_authorized');
```

## 7. Garden-center allow-list entries — seed data

On first Counterpoint merchant activation, the following allow-list entries
are seeded into `app.merchant_rule_configs` with `allow_list` JSON:

```python
GARDEN_CENTER_ALLOW_LISTS = {
    "C-1601": {  # RECEIVER_PO_DISCREPANCY
        "cash_vendor_payment": True,
        "route_to_queue": "ad_hoc_vendor_review",
    },
    "C-1604": {  # LIVE_GOODS_WRITEOFF_TRACKING
        "mode": "informational",
        "seasonal_baselines": {
            "PERENNIAL": {"spring": 0.08, "summer": 0.15, "fall": 0.12},
            "ANNUAL": {"spring": 0.05, "summer": 0.20, "fall": 0.35},
            "TROPICAL": {"summer": 0.10},
        },
    },
    "C-1901": {  # MIX_MATCH_BELOW_COST
        "compute_bundle_margin": True,
        "bundle_negative_threshold_dollars": 50.0,
    },
    "C-2001": {  # RESTRICTED_ITEM_NO_OVERRIDE
        "activated_flags": [],  # populated during onboarding by store state
        "evidence_retention_days": 2555,
    },
}
```

The vertical template is `garden_center`. Additional vertical templates
(`wine_spirits`, `gun_range`, `feed_tack`) follow the same pattern with
different allow-list defaults.

## 8. `merchant_rule_configs` schema — Counterpoint additions

The existing `MerchantRuleConfig` model needs two additive columns to
support Counterpoint-source rules:

```python
# Additive migration on app.merchant_rule_configs
source_code: Mapped[Optional[str]] = mapped_column(
    String(50), nullable=True,
    doc="If set, this config applies only when the alert source matches. "
        "None = all sources. 'counterpoint' = Counterpoint-only config."
)
is_dry_run: Mapped[bool] = mapped_column(
    Boolean, default=False, server_default="false", nullable=False,
    doc="If True, rule evaluates but does not write to alerts table."
)
```

The `is_dry_run` flag implements the observation window in deployment phasing
(§9). Rules begin in dry_run mode; operators promote them to live via the
`tune_rule_threshold()` MCP tool.

## 9. Deployment phasing (per-merchant)

Following the wiki's phasing model, translated to Canary's data model:

| Day | `is_dry_run` | `is_active` | Alert behavior |
|---|---|---|---|
| Day 0 (activation) | `True` | `True` | Evaluates, no alerts written |
| Day 1–7 (observation) | `False` for Phase 1 rules; `True` for Phase 2 | `True` | Phase 1 alerts fire; Phase 2 dry-run |
| Day 8–30 (calibration) | Operator-controlled per rule | `True` | Operator promotes Phase 2 rules rule-by-rule |
| Day 30+ (steady state) | `False` for all active rules | Per-rule | Full production |

The activation flow runs in `CounterpointMerchantActivationService.seed_rule_configs()`,
called when a merchant's Counterpoint source is first connected.

## 10. Chirp detection trigger points

Counterpoint rules fire in two modes:

**Transaction-time (real-time):** Sub4 (detect consumer) evaluates rules
on each `canary:events` stream event. Rules that evaluate on a single
transaction (C-1101 void-without-original, C-2001 restricted-item,
C-1502 free-item) fire within the same pipeline pass.

**Batch window (async):** Rules that require aggregate context
(C-1001 discount-cap, C-1003 below-cost, C-1501 below-category-margin,
C-1802 tier-reassignment-pre-purchase) run on a scheduled batch job:
`ChirpBatchDetector.run_aggregate_rules(merchant_id, window_start)`.
Batch cadence: 15-minute intervals during business hours, 4-hour otherwise.
The batch detector reads from PostgreSQL (not the Valkey stream).

This split is the same pattern as existing Square rules — Sub4 handles
single-event rules, the batch job handles multi-event/aggregate rules.

## 11. New table summary — Alembic migration checklist

| Object | Schema | Action | Notes |
|---|---|---|---|
| `cp_item_catalog.restricted_flags` | app | ADD COLUMN (JSONB) | Compliance rule substrate |
| `merchant_rule_configs.source_code` | app | ADD COLUMN (nullable text) | Source-scoped configs |
| `merchant_rule_configs.is_dry_run` | app | ADD COLUMN (bool, default False) | Dry-run mode |
| `detection_rules` new category values | app | Seed data migration | New category strings |
| New Counterpoint rules (C-1001+) | app | Seed data migration | Via seed_rules service |

## 12. Acceptance criteria

**AC-Q-01 — Seed categories:** After running the Counterpoint rule seed
migration, `app.detection_rules` contains the new category values:
`discount_markdown`, `audit_trail`, `margin_erosion`, `inventory_shrink`,
`tax_compliance`, `customer_tier`, `mix_and_match`, `compliance`,
`commercial_b2b`.

**AC-Q-02 — Phase 1 seed:** After merchant Counterpoint activation,
`app.merchant_rule_configs` contains Phase 1 rules with `is_dry_run=True`
(day-0 state). All C-1001 through C-2001 Phase 1 rules are present.

**AC-Q-03 — Below-cost detection:** For a test transaction with a line item
where `base_price_cents` < `cp_item_catalog.lst_cost × 100`, C-1003
fires an alert within the Sub4 pipeline cycle. Alert has correct
`transaction_id`, `merchant_id`, `rule_id=C-1003`, and `severity=high`.

**AC-Q-04 — Void-without-original:** For a test void Document with no
entry in `sales.document_original_refs`, C-1101 fires within Sub4.

**AC-Q-05 — Restricted item:** For a transaction line referencing an item
with `restricted_flags = ["prop_65"]` and no matching audit-log override,
C-2001 fires with `severity=critical`. For the same transaction with
`activity = 'restricted_items_authorized'` in the audit log, C-2001 does
NOT fire.

**AC-Q-06 — Dry-run mode:** With `is_dry_run=True` on C-1003 for a test
merchant, a below-cost transaction causes the rule to EVALUATE (visible
in batch detector output log) but NOT write to `app.alerts`. After setting
`is_dry_run=False`, the same transaction class writes an alert.

**AC-Q-07 — Garden-center allow-list:** For a cash-vendor receiver Document
(DOC_TYP=RECVR, payment via CASH pay code), C-1601 routes to
`ad_hoc_vendor_review` queue rather than the fraud alert queue.

## 13. Open questions

| ID | Question | Impact |
|---|---|---|
| Q-OQ-01 | Counterpoint `ACTIV` code vocabulary for audit log entries. The restricted-item override fires on `ACTIV = 'restricted_items_authorized'` — but actual Counterpoint audit log ACTIV values are undocumented in the API spec. What are the real strings? Confirm in sandbox. | C-2001 correctness |
| Q-OQ-02 | Does the existing `app.merchant_rule_configs` model support the additive `source_code` and `is_dry_run` columns without breaking existing Square configs? Verify that `source_code = NULL` semantics are backward-compatible with Square rule evaluations. | Migration safety |
| Q-OQ-03 | Restricted-item flag population workflow: how does a garden center operator tag items in Canary? Options: (a) import from customer's existing compliance list; (b) category-level flag in onboarding config; (c) manual item-by-item tagging. The SDD assumes (c) as default; Bart call may clarify preference. | C-2001 onboarding flow |
| Q-OQ-04 | Drawer reconciliation data: `Q-DS-01` (drawer shrinkage) requires drawer count at close vs. expected. Does Counterpoint expose this via audit log ACTIV codes, or via a separate `DrawerReconciliation` endpoint not yet identified? | C-1301 implementability |
| Q-OQ-05 | `Q-DM-02` (markdown-and-buy) requires comparing item price changes to subsequent purchases by the same employee. Item price changes are tracked in `cp_item_catalog.lst_maint_dt` + `rs_utc_dt` deltas. But `ps_doc_lin.HAS_PRC_OVRD` only tells us the ticket used an override, not whether the item CATALOG price was changed. Is there a separate audit trail for catalog price changes? | C-1002 implementability |

---

## Related

- `Brain/wiki/canary-module-q-counterpoint-rule-catalog.md` — Full rule definitions (this SDD's source)
- `docs/sdds/canary/ncr-counterpoint-tsp-adapter.md` — `sales.transaction_audit_log` DDL (Q-AT substrate)
- `docs/sdds/canary/ncr-counterpoint-item-catalog-adapter.md` — `cp_item_catalog` DDL (margin/discount substrate)
- `docs/sdds/canary/ncr-counterpoint-customer-adapter.md` — `cp_customer_profiles` DDL (tier/AR substrate)
- `Brain/wiki/garden-center-operating-reality.md` — Vertical allow-list justification
- `Canary/canary/services/chirp/rule_definitions.py` — Existing Chirp rule seeding (extend, don't replace)
