---
date: 2026-04-10
type: wiki
tags: [canary, chirp, detection, alerts, loss-prevention, rules]
sources: [Canary/canary/services/chirp/rule_definitions.py, Canary/docs/atlas/decision/]
last-compiled: 2026-04-10
needs-review: 2026-04-24
---

# Canary Detection Engine

## Summary

Chirp is Canary's real-time loss prevention rule engine. It evaluates Square merchant transactions against 29 detection rules across 8 categories and 3 execution tiers. Rules fire based on configurable thresholds that can be overridden per merchant. Violations produce alerts that enter a lifecycle managed by the Alerts service and can escalate into Fox cases.

## The Three-Tier Architecture

Rules are classified by the data they need to evaluate:

**Tier 1 — Stateless** (payload only). These rules fire from a single webhook payload with zero lookups. They are the fastest and cheapest to evaluate. Examples: C-004 (after-hours transaction, just checks the timestamp), C-007 (high-value refund, checks amount), C-009 (Square delay hold, checks delay_action field), C-502 (post-void, checks transaction_type).

**Tier 2 — Lightweight** (Valkey counters). These rules maintain sliding-window counters in Valkey. They need to see patterns across multiple events but don't require database queries. Examples: C-002 (excessive refund rate, tracks per-employee refund ratio), C-005 (card velocity, tracks card fingerprint frequency), C-803 (cross-location loyalty velocity, tracks location sets in Valkey).

**Tier 3 — Full** (database required). These rules need historical data from PostgreSQL — shift reconciliation, order aggregates, timecard cross-references. They are the most powerful but most expensive. Examples: C-001 (rapid refund, needs original sale lookup), C-301 (off-clock transaction, needs timecard data), C-204 (untendered order, needs order+payment cross-reference).

## Rule Catalog (29 Rules, 8 Categories)

**Payment** (11 rules, C-001 to C-011): The core loss prevention rules. Cover refund abuse, structuring patterns (round amounts, split tenders), card velocity, manual entry spikes, and Square-computed signals (delay holds, partial authorizations, no-sale events).

**Cash Drawer** (4 rules, C-101 to C-104): No-sale drawer opens, cash variance, paid-out anomalies, and after-hours drawer access. C-104 (after-hours drawer) is rated critical — a cash drawer opening outside business hours is a strong theft signal.

**Order** (4 rules, C-201 to C-204): Sweethearting detection — excessive discounts, line item void rates, unapproved discounts on high-value items, and untendered orders (orders with no payment that drift open).

**Timecard** (3 rules, C-301 to C-303): Cross-reference transactions against employee time records. Ghost employee detection (off-clock transactions), break-time transactions, and wrong-location transactions. All rated high or critical.

**Void** (2 rules, C-501 to C-502): High void rates per shift and post-void detection. Post-voids (COMPLETED → CANCELED after a delay) are always flagged as critical because they are the most common concealment technique in retail theft.

**Gift Card** (2 rules, C-601 to C-602): Load velocity (multiple loads in a short window = laundering signal) and drain detection (full redemption immediately after load).

**Loyalty** (4 rules, C-801 to C-804): Rapid point accumulation, bulk redemption, cross-location velocity, and enrollment fraud (mass enrollments by a single employee).

**Composite** (1 rule, C-901): SRA (Shrink Risk Assessment) threshold breach — a batch-computed metric that fires when estimated shrink exceeds a percentage of net sales. This is the only period-level rule.

## Severity Distribution

5 critical rules: C-009 (Square delay hold), C-104 (after-hours drawer), C-204 (untendered order), C-301 (off-clock transaction), C-502 (post-void), C-602 (gift card drain). These always warrant immediate investigation.

16 high-severity rules form the bulk of daily detection. 8 medium-severity rules are pattern indicators that contribute to risk scores but may not individually warrant alerts at default thresholds.

## Threshold System

Every rule has default thresholds defined in `RULE_CATALOG`. Merchants can override any threshold via `MerchantRuleConfig`, which is cached in Valkey with database fallback. The `ThresholdManager` resolves the effective threshold for each rule-merchant pair: merchant override → Valkey cache → database → catalog default.

Individual rules can also be disabled per merchant via the `disabled_rules` set.

## Alert Pipeline

When a rule fires, Chirp produces an alert dict containing the rule ID, severity, merchant context, transaction reference, and threshold details. These flow into `write_alerts_to_session()` which batches them into the alert lifecycle:

Created → Acknowledged → Escalated → Resolved

The Alerts service scores each alert for business impact (dollar exposure, pattern frequency, employee risk profile). Fox monitors alert clusters — when related alerts accumulate beyond a threshold, Fox escalates them into a formal case with an evidence chain.

## Related

- [[Brain/wiki/canary-alerts-guide|Canary Alerts Guide]] — Merchant-facing plain-English counterpart to this architecture doc; covers every rule in plain language plus tuning, throttling, and onboarding sequence
- [[Brain/wiki/canary-architecture|Canary Architecture]] — System overview and service mesh
- [[Brain/wiki/canary-data-model|Canary Data Model]] — Schema details including alert and case tables
- [[Brain/projects/Canary|Canary MOC]] — Links to all atlas decision diagrams (D-01 through D-04)

## Sources

- `Canary/canary/services/chirp/rule_definitions.py` — Complete rule catalog (29 rules, frozen dataclasses)
- `Canary/docs/atlas/decision/fig-d01-chirp-rule-evaluation.md` — Full evaluation flowchart
- `Canary/docs/atlas/decision/fig-d02-risk-score-classification.md` — Risk scoring
- `Canary/docs/atlas/decision/fig-d03-fox-case-escalation.md` — Case escalation logic
- `Canary/docs/atlas/decision/fig-d04-alert-severity-matrix.md` — Severity classification
- `Canary/docs/atlas/lifecycle/fig-l02-alert-lifecycle.md` — Alert state machine
