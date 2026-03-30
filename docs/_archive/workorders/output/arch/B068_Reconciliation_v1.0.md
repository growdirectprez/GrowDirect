---
type: spec
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# B-068 Token Registry Reconciliation
## Lane D (Vocabulary Schema) vs. Lane B (Token Registry)

**Work Order:** B-068 (final step)
**Date:** February 28, 2026
**Author:** Tom (Systems Architect)
**Reviewed files:**
- Tom Lane D: `Canary_IP/Markdown/Specs/B068_VocabularySchema_v1.0.md`
- Condor Lane B: `_ALX/WorkOrders/output/Condor/B068_TokenRegistry_v1.0.md`
- Locale Pack: `_ALX/WorkOrders/output/Triangulation/LocalePacks/en-US.json`
- Vocabulary Pack: `_ALX/WorkOrders/output/Triangulation/VocabularyPacks/default_vocabulary.json`
- Vocabulary Template: `_ALX/WorkOrders/output/Triangulation/VocabularyPacks/vocabulary_template.json`

---

## Result: GAPS FOUND (1 functional, 1 documentation)

---

## Check 1: Schema Alignment

**ALIGNED.**

The `merchant_vocabulary` table accommodates all 32 vocabulary-overridable tokens from Condor's registry. The schema is token-agnostic by design — `token_key VARCHAR(128)` with a format constraint (`^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*){2,5}$`) accepts any 3-to-6-segment dot-separated key. All 32 Condor tokens are 3-segment keys (e.g., `employee.label.singular`) and pass the constraint. Column types, the unique composite index on `(merchant_id, locale, token_key)`, and the `display_value VARCHAR(255)` constraint are all sufficient.

## Check 2: Token Naming

**ALIGNED.**

Every one of Condor's 32 overridable token keys follows the `module.element.variant` pattern that Tom's regex constraint enforces. Verified all 32:

- 15 entity pairs (singular + plural): `employee`, `location`, `cash_drawer`, `transaction`, `void`, `refund`, `case`, `chirp`, `shift`, `tender`, `store`, `drawer`, `discount`, `exchange`, `investigation` — all 30 keys pass.
- 2 singular-only tokens: `variance.label.singular`, `shrink.label.singular` — both pass.

Non-overridable tokens (146) also fit the regex if ever inserted — the longest keys (e.g., `process.open_store.step2.validation.zero_warning` at 5 segments) are within the 6-segment maximum.

## Check 3: Resolution Chain

**ALIGNED.**

The session prompt specifies: `merchant_vocabulary` DB → Locale Pack JSON → `en-US.json`.

Tom's `VocabularyResolver` implements:
1. Valkey cache (populated from `merchant_vocabulary` DB) — merchant + locale
2. Merchant en-US fallback (if requested locale differs)
3. Locale pack JSON (in-memory, loaded at startup)
4. `en-US.json` hardcoded fallback

This matches the required chain. The Valkey cache layer is an optimization on top of the DB tier, not a separate resolution tier — on cache miss, the DB is the source of truth.

Condor's Lane C notes reference "Vocabulary Pack → Locale Pack → en-US default" as the backend resolution order. This aligns: the "Vocabulary Pack" in Condor's terminology is the DB-stored merchant overrides (Tom's `merchant_vocabulary` table), the "Locale Pack" is the in-memory JSON, and "en-US default" is the hardcoded fallback. The naming differs but the chain is identical.

## Check 4: Missing Tokens

**ALIGNED.**

Tom's schema is token-agnostic — it does not enumerate specific token keys. The `merchant_vocabulary` table stores any token key that passes the format constraint. Condor's 32 overridable tokens all pass. No tokens exist in Tom's schema that Condor didn't register (the schema doesn't pre-populate). No tokens in Condor's registry are excluded by Tom's constraints.

Tom's session prompt baseline listed 16 tokens (8 entity pairs). Condor's final registry has 32 (15 entity pairs + 2 singular-only). The schema handles all 32 without modification.

## Check 5: JSON Pack Structure

**GAP FOUND.**

### The Gap

Tom's `VocabularyResolver` treats the locale pack as a **flat dictionary** keyed by dot-notation token keys:

```python
pack = self.locale_packs.get(locale, {})
if token_key in pack:
    return pack[token_key]
```

This expects: `pack["employee.label.singular"] = "Employee"`

Condor's JSON packs use **nested object structure**:

```json
{
  "employee": {
    "label": {
      "singular": "Employee"
    }
  }
}
```

There is no top-level key `"employee.label.singular"` in the JSON. The resolver will return `None` for every locale pack lookup, falling through to the `en-US.json` fallback (which has the same nesting problem), and ultimately returning the raw token key string as a diagnostic.

### Recommended Fix

Add a startup-time flattener that converts nested JSON into flat dot-notation keys when locale packs are loaded. This is a one-time transform at application init — no runtime cost.

```python
def flatten_locale_pack(nested: dict, prefix: str = "") -> dict:
    """Convert nested JSON structure to flat dot-notation keys.

    {"employee": {"label": {"singular": "Employee"}}}
    → {"employee.label.singular": "Employee"}
    """
    flat = {}
    for key, value in nested.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            flat.update(flatten_locale_pack(value, full_key))
        else:
            flat[full_key] = value
    return flat
```

The `VocabularyResolver.__init__` would call this on each locale pack:

```python
self.locale_packs = {
    locale: flatten_locale_pack(pack_json["tokens"])
    for locale, pack_json in raw_locale_packs.items()
}
```

**Owner:** Jeremy (implementation). This is a ~10-line utility function added to the vocabulary service module. No schema change. No DDL. No migration.

**Severity:** Medium. Without this fix, the resolver silently degrades — it serves raw token keys instead of display strings whenever the DB has no override. The degradation is visible (the UI would show `employee.label.singular` instead of "Employee") but not catastrophic. Fix before any Settings UI work in Sprint 7.

---

## Documentation Note: Scale Assessment Numbers

Tom's scale assessment in Section 6 references "16 (8 pairs: singular + plural)" vocabulary-overridable tokens. Condor's final registry has **32** (15 entity pairs + 2 singular-only). This doesn't affect the schema — the table is token-agnostic — but the Phase 1/2/3 row count projections should be doubled:

| Phase | Tom's estimate | Corrected |
|---|---|---|
| Phase 1 max rows | 16 | 32 |
| Phase 2 max rows | 15,000 | 30,000 |
| Phase 3 max rows | 10,000,000 | 20,000,000 |

At 20M theoretical max rows the table still fits comfortably in PostgreSQL with the composite index. No architectural impact. Tom should update the scale assessment table in `B068_VocabularySchema_v1.0.md` to reflect 32 tokens.

---

## Sign-Off

**B-068 Foundation Layer: GAPS — 1 functional (JSON flattener), 1 documentation (scale numbers)**

Both gaps are minor and do not block Sprint 6. The functional gap (JSON flattener) must be resolved before Sprint 7 vocabulary editor work. The documentation gap is a correction to Tom's own spec.

All five B-068 lanes are delivered. The schema aligns with the token registry. The partition architecture (Lane A), vocabulary schema (Lane D), token registry (Lane B), and locale/vocabulary JSON packs (Lane C) form a coherent foundation.

---

*Tom | B-068 Reconciliation | February 28, 2026*
*"One row per merchant per token. The schema holds. The JSON needs a flattener."*
