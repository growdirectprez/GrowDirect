---
type: spec
domain: canary
status: active
created: 2026-03-19
updated: 2026-03-19
---
# B-068-D: Merchant Vocabulary DB Schema

**One row per merchant per token. No global vocabulary state. Ever.**

**Version:** 1.0
**Date:** February 28, 2026
**Author:** Tom (Systems Architect)
**Work Order:** B-068, Lane D
**Classification:** Internal — Architecture Specification
**Status:** Draft — pending Jim QA review

---

## 1. `merchant_vocabulary` DDL

### Table Definition

```sql
CREATE TABLE merchant_vocabulary (
    id              VARCHAR(36)     NOT NULL DEFAULT gen_random_uuid()::text,
    merchant_id     VARCHAR(36)     NOT NULL,
    token_key       VARCHAR(128)    NOT NULL,
    locale          VARCHAR(10)     NOT NULL DEFAULT 'en-US',
    display_value   VARCHAR(255)    NOT NULL,
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT now(),
    created_by      VARCHAR(36),
    modified_by     VARCHAR(36),

    CONSTRAINT pk_merchant_vocabulary PRIMARY KEY (id),
    CONSTRAINT fk_mv_merchant FOREIGN KEY (merchant_id)
        REFERENCES merchants(merchant_id) ON DELETE CASCADE,
    CONSTRAINT chk_mv_token_key_format
        CHECK (token_key ~ '^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*){2,5}$'),
    CONSTRAINT chk_mv_locale_format
        CHECK (locale ~ '^[a-z]{2}(-[A-Z]{2})?$'),
    CONSTRAINT chk_mv_display_value_length
        CHECK (char_length(display_value) BETWEEN 1 AND 255),
    CONSTRAINT chk_mv_display_value_printable
        CHECK (display_value !~ '[\x00-\x1F\x7F]')
);
```

### Indexes

```sql
-- Primary lookup: hot read path. Every API response resolving a vocabulary
-- token hits this index. Must be O(1).
CREATE UNIQUE INDEX uix_mv_merchant_locale_token
    ON merchant_vocabulary (merchant_id, locale, token_key);

-- Reverse lookup: "show me all overrides for this merchant" (Settings UI).
-- Covered by the unique index above (merchant_id is the leading column).

-- Token-level query: "which merchants override this token?" (admin/analytics).
CREATE INDEX idx_mv_token_key
    ON merchant_vocabulary (token_key);
```

### Design Notes

- **UUID primary key** (`id VARCHAR(36)`) — consistent with all CRDM tables. The unique composite index on `(merchant_id, locale, token_key)` is the operational key; `id` exists for ORM compatibility and audit trail foreign keys.
- **FK targets `merchants.merchant_id`**, not `merchants.id` — aligns with CRDM convention where `merchant_id` is the tenant isolation key throughout the schema.
- **ON DELETE CASCADE** — when a merchant is removed, their vocabulary overrides are removed with them. No orphaned rows. Same isolation principle as the partition: the merchant boundary is the cleanup boundary.
- **`token_key` format constraint** — enforces the `module.screen.element.variant` naming convention from Condor's registry. Minimum 3 segments (e.g., `employee.label.singular`), maximum 6 segments. Lowercase alphanumeric plus underscore within segments, dot-separated.
- **`locale` format constraint** — BCP 47 language tags. Supports both `en` (language only) and `en-US` (language + region). Does not support script subtags or extensions — these are unnecessary for the current locale pack scope.
- **`display_value` constraints** — non-empty, max 255 characters, no control characters. Allows Unicode (accented characters, CJK, etc.) — required for `es-MX`, future `zh-CN`, etc.
- **Sparse by design** — most merchants override nothing. A merchant with zero overrides has zero rows. The table only stores exceptions to the defaults.

---

## 2. `merchants` Table Additions

### New Columns

```sql
ALTER TABLE merchants
    ADD COLUMN locale              VARCHAR(10)  NOT NULL DEFAULT 'en-US',
    ADD COLUMN vocabulary_enabled  BOOLEAN      NOT NULL DEFAULT true;
```

| Column | Type | Default | Purpose |
|---|---|---|---|
| `locale` | `VARCHAR(10)` | `en-US` | Merchant's default locale. Drives which locale pack JSON loads at session start. BCP 47. |
| `vocabulary_enabled` | `BOOLEAN` | `true` | Toggle vocabulary resolution per merchant without deleting override rows. When `false`, resolution skips the DB lookup entirely — returns locale pack defaults. |

### Relationship to `merchant_settings.language`

The existing `merchant_settings.language` column (`VARCHAR(10)`, default `en-US`) was a placeholder for i18n configuration. The new `merchants.locale` column supersedes it for vocabulary resolution purposes. The distinction:

- `merchants.locale` — **core identity**. Determines which locale pack loads. Used by the vocabulary resolution function. Lives on the merchant record because it defines the merchant's linguistic context.
- `merchant_settings.language` — **UI preference**. Can remain for any UI-only formatting needs (date/time display, number formatting) that don't involve vocabulary resolution. No migration needed — both can coexist.

### Alembic Migration Pattern

```python
"""Add locale and vocabulary_enabled to merchants table.

Revision ID: 005_add_merchant_locale
Revises: 004_hash_chain_triggers
"""
from alembic import op
import sqlalchemy as sa

revision = '005_add_merchant_locale'
down_revision = '004_hash_chain_triggers'

def upgrade():
    op.add_column('merchants',
        sa.Column('locale', sa.String(10), nullable=False, server_default='en-US'))
    op.add_column('merchants',
        sa.Column('vocabulary_enabled', sa.Boolean(), nullable=False, server_default='true'))

def downgrade():
    op.drop_column('merchants', 'vocabulary_enabled')
    op.drop_column('merchants', 'locale')
```

---

## 3. Resolution Function

### Decision: Option B — Application-Layer Service

**Chosen.** The resolution function lives in the Python application layer, not as a PostgreSQL function.

### Justification

| Criterion | Option A (PG function) | Option B (App layer) |
|---|---|---|
| Cache layer | None at DB level. Every call = DB round trip on the hot read path. | Valkey cache per merchant per locale. Sub-millisecond on cache hit. |
| Cache invalidation | No cache to invalidate — but no cache means every API response pays the lookup cost. | Bust one Valkey key on PUT/DELETE. Next read rebuilds from DB. Propagation: instant (next request). |
| Locale pack fallback | PG function returns NULL, caller handles JSON fallback anyway — split logic across two layers. | Single function handles all three tiers. Resolution logic lives in one place. |
| Testability | Requires PG connection for unit tests. | Pure Python — mockable, testable without DB. |
| Deployment | DDL migration for any logic change. | Python deploy. No schema migration for logic changes. |
| Observability | PG function calls are opaque to application tracing. | Full visibility in application metrics, logging, tracing. |

The only argument for Option A is reduced network hops when the cache is cold. But the cold-cache case is rare (first request after a merchant logs in or after cache bust), and even then the indexed lookup is sub-millisecond. The warm-cache case is the common case, and Option B wins there decisively.

### Resolution Logic

```python
class VocabularyResolver:
    """Three-level vocabulary resolution with Valkey caching.

    Resolution order:
        1. Valkey cache (merchant + locale) — sub-ms
        2. merchant_vocabulary table (DB lookup) — indexed, sub-ms
        3. Locale pack JSON (in-memory) — always resolves
        4. en-US.json fallback — hardcoded, never fails
    """

    CACHE_TTL_SECONDS = 3600  # 1 hour. Busted on write, not on expiry.
    CACHE_KEY_PREFIX = "vocab"

    def __init__(self, db_session, valkey_client, locale_packs: dict):
        self.db = db_session
        self.cache = valkey_client
        self.locale_packs = locale_packs  # {"en-US": {...}, "es-MX": {...}}

    def resolve(self, merchant_id: str, token_key: str, locale: str = "en-US") -> str:
        """Resolve a single token key to its display string.

        Returns the most specific match:
            merchant override (exact locale) >
            merchant override (en-US fallback) >
            locale pack >
            en-US default
        """
        # 1. Check Valkey cache for merchant's full vocabulary map
        overrides = self._get_cached_overrides(merchant_id, locale)

        if overrides is not None:
            if token_key in overrides:
                return overrides[token_key]
        else:
            # Cache miss — load from DB, populate cache
            overrides = self._load_overrides_from_db(merchant_id, locale)
            self._set_cached_overrides(merchant_id, locale, overrides)
            if token_key in overrides:
                return overrides[token_key]

        # 2. If locale != en-US, try en-US overrides as merchant-level fallback
        if locale != "en-US":
            en_overrides = self._get_or_load_overrides(merchant_id, "en-US")
            if token_key in en_overrides:
                return en_overrides[token_key]

        # 3. Locale pack JSON (loaded at startup, in-memory)
        pack = self.locale_packs.get(locale, {})
        if token_key in pack:
            return pack[token_key]

        # 4. en-US fallback (always resolves)
        return self.locale_packs["en-US"].get(token_key, token_key)
        # Final fallback: return the token key itself as a visible diagnostic.

    def invalidate(self, merchant_id: str, locale: str = None):
        """Bust cache on vocabulary write (PUT or DELETE).

        If locale is None, bust all locales for this merchant.
        """
        if locale:
            self.cache.delete(self._cache_key(merchant_id, locale))
        else:
            # Pattern delete: vocab:{merchant_id}:*
            pattern = f"{self.CACHE_KEY_PREFIX}:{merchant_id}:*"
            keys = self.cache.keys(pattern)
            if keys:
                self.cache.delete(*keys)

    def resolve_batch(self, merchant_id: str, token_keys: list, locale: str = "en-US") -> dict:
        """Resolve multiple token keys in one call. Used by API response builder."""
        return {key: self.resolve(merchant_id, key, locale) for key in token_keys}

    # --- Internal methods ---

    def _cache_key(self, merchant_id: str, locale: str) -> str:
        return f"{self.CACHE_KEY_PREFIX}:{merchant_id}:{locale}"

    def _get_cached_overrides(self, merchant_id: str, locale: str) -> dict | None:
        raw = self.cache.get(self._cache_key(merchant_id, locale))
        if raw is None:
            return None
        return json.loads(raw)

    def _set_cached_overrides(self, merchant_id: str, locale: str, overrides: dict):
        self.cache.set(
            self._cache_key(merchant_id, locale),
            json.dumps(overrides),
            ex=self.CACHE_TTL_SECONDS
        )

    def _load_overrides_from_db(self, merchant_id: str, locale: str) -> dict:
        """Load all overrides for a merchant + locale into a flat dict."""
        rows = self.db.query(MerchantVocabulary).filter(
            MerchantVocabulary.merchant_id == merchant_id,
            MerchantVocabulary.locale == locale
        ).all()
        return {row.token_key: row.display_value for row in rows}

    def _get_or_load_overrides(self, merchant_id: str, locale: str) -> dict:
        overrides = self._get_cached_overrides(merchant_id, locale)
        if overrides is None:
            overrides = self._load_overrides_from_db(merchant_id, locale)
            self._set_cached_overrides(merchant_id, locale, overrides)
        return overrides
```

### Cache Invalidation Design

| Event | Action | Propagation Time |
|---|---|---|
| Merchant PUTs a vocabulary override | `invalidate(merchant_id, locale)` — bust that locale's cache | Next request (< 1ms to bust, sub-ms to rebuild) |
| Merchant DELETEs a vocabulary override | Same as PUT | Same |
| Merchant changes locale in settings | `invalidate(merchant_id)` — bust all locales | Same |
| `vocabulary_enabled` toggled to `false` | No cache bust needed — resolver checks the flag before cache lookup | Instant |
| Locale pack JSON updated (deploy) | Application restart reloads JSON packs. Valkey cache TTL expires (1h max). No explicit bust needed — JSON packs are deploy-time artifacts, not runtime-mutable. | Up to 1 hour (or immediate on restart) |

**Cache shape:** One Valkey key per merchant per locale. Value is a JSON-serialized dict of `{token_key: display_value}`. For a merchant with 16 overrides across 2 locales, that's 2 Valkey keys, each holding a small JSON map.

**Cache miss cost:** One indexed DB query returning all overrides for that merchant + locale. With the `uix_mv_merchant_locale_token` index, this is an index range scan bounded by `merchant_id` + `locale` — sub-millisecond for any realistic override count.

**Why not cache individual tokens?** A merchant's override set is small (typically 0–30 keys). Loading the entire set per locale into one cache entry means a single cache miss populates all tokens. Individual token caching would mean N cache misses on first load instead of 1.

---

## 4. Cache Invalidation Design

Covered in Section 3 above. Summary:

```
Write path (PUT/DELETE vocabulary override):
    → DB write (INSERT/UPDATE/DELETE on merchant_vocabulary)
    → Valkey cache bust: DELETE vocab:{merchant_id}:{locale}
    → Next read: cache miss → DB reload → cache repopulate

Read path (API response building):
    → Check merchants.vocabulary_enabled
    → If false: skip DB/cache, go straight to locale pack
    → If true: Valkey GET vocab:{merchant_id}:{locale}
        → Hit: resolve from cached map
        → Miss: DB load → cache set → resolve from loaded map
    → Fallback: locale pack → en-US.json → token_key literal
```

No background refresh. No pub/sub. No eventual consistency window. The cache is busted synchronously on the write path. The next read rebuilds it. Maximum staleness window: zero — there is no window where a stale value can be served after a successful write.

---

## 5. Settings UI Data Contract

### Endpoints

#### GET `/api/vocabulary/{merchant_id}`

Returns all active overrides for a merchant, grouped by locale.

**Response: 200 OK**

```json
{
    "merchant_id": "MLE55GCYANCYT",
    "locale": "en-US",
    "vocabulary_enabled": true,
    "overrides": [
        {
            "token_key": "employee.label.singular",
            "locale": "en-US",
            "display_value": "Barista",
            "updated_at": "2026-02-28T14:30:00Z"
        },
        {
            "token_key": "employee.label.plural",
            "locale": "en-US",
            "display_value": "Baristas",
            "updated_at": "2026-02-28T14:30:00Z"
        }
    ],
    "defaults": [
        {
            "token_key": "employee.label.singular",
            "default_value": "Employee",
            "overridable": true
        },
        {
            "token_key": "employee.label.plural",
            "default_value": "Employees",
            "overridable": true
        }
    ]
}
```

**Notes:**
- `overrides` — only rows that exist in `merchant_vocabulary`. Empty array if merchant has no overrides.
- `defaults` — the full set of vocabulary-overridable tokens from Condor's registry, each with its current default value from the locale pack. This gives the Settings UI the full token list to render the editor, with current overrides pre-filled.
- The `overridable` flag comes from Condor's token registry — not all tokens are exposed to the merchant in the Settings UI, even though the resolution function handles any token key.

#### PUT `/api/vocabulary/{merchant_id}/{token_key}`

Sets or updates a single vocabulary override.

**Request body:**

```json
{
    "locale": "en-US",
    "display_value": "Barista"
}
```

**Response: 200 OK**

```json
{
    "token_key": "employee.label.singular",
    "locale": "en-US",
    "display_value": "Barista",
    "previous_value": "Employee",
    "updated_at": "2026-02-28T14:30:00Z"
}
```

**Side effect:** Busts Valkey cache key `vocab:{merchant_id}:{locale}`.

**Validation rules:**
| Field | Rule |
|---|---|
| `token_key` (URL param) | Must match `^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*){2,5}$`. Must be in Condor's overridable token registry. |
| `locale` | Must match `^[a-z]{2}(-[A-Z]{2})?$`. Must be a locale for which a pack exists. |
| `display_value` | 1–255 characters. No control characters (`[\x00-\x1F\x7F]`). No leading/trailing whitespace (trimmed on input). |
| `merchant_id` (URL param) | Must match an active merchant. Caller must have settings-write permission for this merchant. |

**Error responses:**
- `400` — validation failure (bad token_key format, display_value too long, etc.)
- `403` — caller lacks settings-write permission for this merchant
- `404` — merchant not found or token_key not in overridable registry
- `409` — concurrent write detected (optimistic locking via `updated_at` if needed — Phase 2)

#### DELETE `/api/vocabulary/{merchant_id}/{token_key}`

Reverts a single override to the default.

**Query parameter:** `locale` (optional, defaults to merchant's default locale).

**Response: 200 OK**

```json
{
    "token_key": "employee.label.singular",
    "locale": "en-US",
    "reverted_to": "Employee",
    "deleted_at": "2026-02-28T14:35:00Z"
}
```

**Side effect:** Busts Valkey cache key `vocab:{merchant_id}:{locale}`.

**Note:** This is a hard delete, not a soft delete. The override row is removed from `merchant_vocabulary`. The token reverts to locale pack resolution. There is no "history" of previous overrides — if a merchant wants to restore a previous custom value, they re-enter it. The audit trail lives in application logs, not in the table itself.

---

## 6. Scale Assessment

### Key Space

| Dimension | Current | Phase 2 (100 merchants) | Phase 3 (10,000 merchants) |
|---|---|---|---|
| Vocabulary-overridable tokens | 16 (8 pairs: singular + plural) | ~50 (Condor registry expansion) | ~100 (third-party apps add tokens) |
| Locales per merchant | 1 (en-US only for Phase 1) | 2–3 (en-US, es-MX, en-AU) | 5–10 |
| Merchants | 1 (GrowDirect Lab) | 100 | 10,000 |
| **Max rows (all merchants, all tokens, all locales)** | **16** | **15,000** | **10,000,000** |

### Realistic Row Count

The table is sparse. Most merchants override 0–5 tokens. Realistic utilization:

| Phase | Merchants | Avg overrides/merchant | Avg locales/merchant | Realistic rows |
|---|---|---|---|---|
| Phase 1 | 1 | 16 | 1 | 16 |
| Phase 2 | 100 | 5 | 1.2 | 600 |
| Phase 3 | 10,000 | 8 | 1.5 | 120,000 |

At 120,000 rows with the composite unique index, this table fits entirely in PostgreSQL's shared buffer cache on any reasonable deployment. No partitioning needed on this table. No sharding needed. The index scan for a single merchant's overrides returns in microseconds.

### Valkey Cache Footprint

Each Valkey key holds one JSON map per merchant per locale. Typical override map: 8 key-value pairs, ~500 bytes serialized.

| Phase | Cache keys | Total memory |
|---|---|---|
| Phase 1 | 1 | < 1 KB |
| Phase 2 | 120 | ~60 KB |
| Phase 3 | 15,000 | ~7.5 MB |

Negligible. Even at 10,000 merchants the vocabulary cache uses less memory than a single Valkey stream.

---

## 7. Architectural Rationale

### Why This Table Exists

The `merchant_vocabulary` table is the database expression of per-merchant linguistic isolation — the same principle that produces per-merchant hash chains at the Bitcoin layer and per-merchant partitions at the Postgres layer.

In Section 3.3 of the Unified Architecture Thesis, the vocabulary pack is defined as the mechanism that makes the "any app" claim literal. A coffee shop's employee is a "Barista." A cannabis dispensary's employee is a "Budtender." These are not cosmetic differences — they determine whether the application fits the merchant's cognitive model of their own business.

This table implements that principle as a relational structure. One row per merchant per token per locale. No global vocabulary state. A merchant's overrides are scoped to their `merchant_id`, isolated by the same key that scopes their partition and their hash chain. When a merchant is deleted, their vocabulary overrides cascade-delete with them. When a merchant's vocabulary is queried, the index range scan is bounded by their `merchant_id` — no other merchant's data is touched, examined, or risked.

The resolution fallback chain — merchant override, locale pack, en-US default — means the table is additive. A merchant with zero overrides pays zero storage cost and receives zero behavioral change. The system works identically with an empty table as it does with a million rows. Configuration, not code. That is the design contract.

A new engineer looking at this table should understand: this is not "settings storage." This is per-merchant isolation expressed at the presentation layer. Same principle, different layer. The partition isolates their data. The hash chain isolates their evidence. The vocabulary table isolates their language. One merchant, one boundary, everywhere.

---

*Tom | B-068-D | February 28, 2026*
*"The partition isolates their data. The hash chain isolates their evidence. The vocabulary table isolates their language."*
