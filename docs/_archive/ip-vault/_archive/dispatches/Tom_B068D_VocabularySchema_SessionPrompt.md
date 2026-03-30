---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Tom — B-068-D: Merchant Vocabulary DB Schema
## Session Prompt

**Work Order:** B-068, Lane D
**Date:** February 28, 2026
**From:** ALX
**Priority:** 🟡 HIGH — Required before Sprint 7 vocabulary editor. Runs parallel with Lane A.

---

## Read This First

```
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/PhD/
  GrowDirect_UnifiedArchitectureThesis_v1.0.md
```

Sections **3.2 and 3.3 together**. Read them as one argument.

Section 3.2 is the partition. Section 3.3 is the vocabulary pack. They are the same
decision expressed at different layers. The `merchant_vocabulary` table you are
designing is the database expression of Section 3.3 — one row per merchant per token
per locale, no global vocabulary state, same isolation principle as the partition.

---

## What the Vocabulary System Does

The presentation layer resolves display strings through a three-level fallback chain:

```
1. merchant_vocabulary  (DB lookup — merchant-specific overrides)
        ↓ miss
2. Locale pack JSON     (loaded at startup — language defaults)
        ↓ miss
3. en-US.json           (hardcoded fallback — always resolves)
```

The API returns both the token key and the resolved string in every response.
The frontend renders what it receives. No string logic in the frontend.
No hardcoded labels anywhere in the Blueprint.

A merchant who calls their employees "Baristas" sets one row in `merchant_vocabulary`.
On their next API call, every screen that renders `{{employee.label.plural}}` shows
"Baristas" instead of "Employees." Zero rebuild. Zero deploy. Configuration, not code.

---

## What You Are Designing

### Table: `merchant_vocabulary`

One row per merchant per token key per locale. Sparse — most merchants override
nothing. The table only stores exceptions to the defaults.

Columns you must define:
- `merchant_id` — foreign key to `merchants.id`
- `token_key` — the token identifier (e.g., `employee.label.singular`)
- `locale` — BCP 47 language tag (e.g., `en-US`, `es-MX`)
- `display_value` — the merchant's custom string
- Standard audit fields: `created_at`, `updated_at`, `created_by`

Index requirement: lookup must be O(1) on `(merchant_id, locale, token_key)`.
This is a hot read path — every API response that contains a resolved string
queries this index.

### Schema Additions to `merchants`

Two new columns:
1. `locale` — the merchant's default locale (BCP 47). Drives which locale pack loads.
   Default: `en-US`. Example values: `en-US`, `es-MX`, `en-AU`.
2. `vocabulary_enabled` — boolean flag. Allows vocabulary resolution to be toggled
   per merchant without deleting their override rows. Default: `true`.

### Resolution Function

Design the resolution function. You have two options:

**Option A — PostgreSQL function**
```sql
CREATE FUNCTION resolve_token(
  p_merchant_id VARCHAR,
  p_token_key   VARCHAR,
  p_locale      VARCHAR DEFAULT 'en-US'
) RETURNS VARCHAR AS $$
  -- 1. Check merchant_vocabulary for merchant + locale + key
  -- 2. Check merchant_vocabulary for merchant + en-US + key (locale fallback)
  -- 3. Return NULL (caller falls back to JSON locale pack)
$$ LANGUAGE plpgsql;
```

**Option B — Application-layer service**
A Python service method that:
1. Checks the DB (cached per merchant session)
2. Falls back to the locale pack JSON loaded at startup
3. Falls back to en-US JSON

**Your call.** Make it. Justify it. Consider: where does cache invalidation live?
If a merchant updates a vocabulary override, how quickly does it propagate?

### Settings UI Data Model

The Sprint 7 vocabulary editor (Art's Config page) needs to read and write this
table. Define the data contract:
- GET `/api/vocabulary/{merchant_id}` — returns all active overrides
- PUT `/api/vocabulary/{merchant_id}/{token_key}` — sets one override
- DELETE `/api/vocabulary/{merchant_id}/{token_key}` — reverts to default

What does the response shape look like? What validation rules apply to
`display_value` (max length, prohibited characters)?

---

## Coordination with Condor (Lane B)

Condor is building the token registry in parallel. You do not need their output
to design this schema — the table structure is independent of the specific token
keys. What you need from Condor's registry:

1. The complete list of vocabulary-overridable token keys (so you can verify your
   index handles the full key space)
2. The naming convention (`module.screen.element.variant`) so your schema and
   their registry use identical key format

If you need to start before Condor delivers, use these confirmed vocabulary-overridable
tokens as your baseline:

```
employee.label.singular      employee.label.plural
location.label.singular      location.label.plural
cash_drawer.label.singular   cash_drawer.label.plural
transaction.label.singular   transaction.label.plural
void.label.singular          void.label.plural
refund.label.singular        refund.label.plural
case.label.singular          case.label.plural
chirp.label.singular         chirp.label.plural   (resolves to "Alert" in default)
```

The schema must handle any token key — vocabulary-overridable or not — since the
resolution function is generic. Condor's registry just tells us which keys
the Settings UI exposes to the merchant.

---

## Output

```
Canary_IP/Markdown/Specs/B068_VocabularySchema_v1.0.md
```

Structure:
1. `merchant_vocabulary` DDL — complete with indexes and constraints
2. `merchants` table additions — `locale` and `vocabulary_enabled` columns + Alembic migration pattern
3. Resolution function — chosen option with full pseudocode or SQL
4. Cache invalidation design
5. Settings UI data contract (API shape + validation rules)
6. Scale assessment (token key space × merchant count × locale count)
7. One paragraph: how this table is the database expression of per-merchant isolation
   (same principle as the partition — write it so a new engineer understands why this
   table exists, not just what it does)

---

## Coordination

**Runs parallel with Lane A.** No dependency between A and D.

**Condor's Lane B token registry** is useful but not blocking. Start without it.
Reconcile key naming when Condor delivers.

**Gates:**
- Art: vocabulary editor UI (Sprint 7 Config page) — reads your API contract
- Condor: Lane C (JSON files) — your locale field naming must match their JSON structure

---

*ALX | B-068-D | February 28, 2026*
*"One row per merchant per token. No global vocabulary state. Ever."*
