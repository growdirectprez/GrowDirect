---
id: sdd-pos-adapter
title: Canary — POSAdapter Substrate (Multi-POS Architecture)
status: draft-1
version: 0.1.0
date: 2026-04-26
author: GrowDirect Engineering
linear: GRO-TBD
companion-sdds:
  - docs/sdds/canary/ncr-counterpoint-tsp-adapter.md
  - docs/sdds/canary/ncr-counterpoint-store-station-adapter.md
  - Canary/docs/sdds/v2/tsp.md
  - Canary/docs/sdds/v2/identity.md
implements-cycle: 7 (Substrate scaffold per 2026-04-25-canary-for-rapidpos-delivery-spec.md)
---

# Canary — POSAdapter Substrate (Multi-POS Architecture)

## 1. Purpose

Canary's Square integration was designed as a singleton. The Counterpoint
engagement requires a second POS source without rewriting the platform.
This SDD specifies the substrate that makes Canary genuinely multi-POS:

- `POSAdapter` abstract base class
- `CanonicalEvent` dataclass (provider-agnostic event)
- Adapter registry and provider resolution
- `pos_tenant_credentials` table (credential storage + lifecycle)
- `source_systems` catalog table
- Activation ordering (reference data before transactions)
- Contract test requirements

**What this document does NOT cover:** adapter-specific parsing logic
(covered in per-adapter SDDs: `ncr-counterpoint-tsp-adapter.md`, etc.),
Square-specific OAuth flow (covered in `identity.md`), or Chirp rule
dispatch (covered in `ncr-counterpoint-module-q-chirp-wiring.md`).

## 2. Architecture context

```
                  Webhook ingress            Poll loop
                  (Square today)        (Counterpoint today)
                        │                       │
                        ▼                       ▼
              ┌─────────────────┐   ┌─────────────────────┐
              │ webhook_dispatch │   │ poll_consumer.py     │
              │ (source-keyed)  │   │ (per-tenant cron)    │
              └────────┬────────┘   └──────────┬──────────┘
                       │                       │
                       ▼                       ▼
              CanonicalEvent ──────────────────────────────▶
                                     │
                                     ▼
                           canary:events (Valkey stream)
                                     │
                       ┌────────┬────┴────┬──────────┐
                       ▼        ▼         ▼          ▼
                    Sub1     Sub2      Sub3       Sub4
                  (seal)   (parse)  (Merkle)  (detect)
```

From Sub1 onward, no component knows whether the CanonicalEvent came from
a Square webhook or a Counterpoint poll. The adapter layer is the seam.

## 3. Core data structures

### 3.1 CanonicalEvent

```python
# canary/services/pos/base.py

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class CanonicalEvent:
    """
    Provider-agnostic event flowing from an adapter into the TSP pipeline.

    Immutable once created. The `payload` dict carries the parsed,
    source-specific data; it is NOT the raw provider payload (that lives
    in the Sub1 evidence record). Payload shape varies by event_type and
    is documented in the per-adapter SDDs.
    """
    provider: str          # "square" | "counterpoint" | future
    event_type: str        # "transaction.created" | "customer.upserted" | ...
    tenant_id: str         # Canary merchant UUID (string)
    occurred_at: datetime  # Business event time (NOT ingestion time)
    external_id: str       # Provider's native ID for this event/entity
    payload: dict[str, Any] = field(default_factory=dict)

    # Optional: company alias for multi-company providers (Counterpoint)
    company_alias: str | None = None

    def __post_init__(self) -> None:
        if not self.provider:
            raise ValueError("provider required")
        if not self.event_type:
            raise ValueError("event_type required")
        if not self.tenant_id:
            raise ValueError("tenant_id required")
```

### 3.2 Fixture

```python
@dataclass(frozen=True)
class Fixture:
    """
    Seed data batch for a freshly connected tenant.
    Used by `POSAdapter.seed_data()` to populate reference tables
    (stores, items, customers) before transaction sync begins.
    """
    entity_type: str       # "store" | "item" | "customer" | "category" | ...
    rows: list[dict[str, Any]]
    source: str            # provider code
    tenant_id: str
    company_alias: str | None = None
```

### 3.3 PollResult

```python
@dataclass
class PollResult:
    """
    Result of one poll() invocation for one entity type.
    Includes the events emitted and the new watermark to persist.
    """
    entity_type: str
    events: list[CanonicalEvent]
    new_watermark: datetime | None  # None = no update (no events returned)
    pages_fetched: int = 0
    error: Exception | None = None

    @property
    def success(self) -> bool:
        return self.error is None
```

## 4. POSAdapter ABC

```python
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Iterator, Type


class POSAdapter(ABC):
    """
    Abstract base class for all POS source adapters.

    Implementations:
      SquareAdapter    — webhook-only (empty poll_intervals)
      CounterpointAdapter — poll-only (empty webhook_event_types)

    An adapter may implement both surfaces (e.g., a future POS that
    offers webhooks for transactions but requires polling for catalog).

    The provider class attribute uniquely identifies the adapter in
    the registry. It must match the source_code in `source_systems`
    and `external_identities`.
    """
    provider: str  # "square" | "counterpoint" | ... (class-level constant)

    # ── Webhook surface ──────────────────────────────────────────────────

    @abstractmethod
    def webhook_event_types(self) -> frozenset[str]:
        """
        Event type strings this adapter accepts on webhook ingress.
        Return frozenset() for poll-only adapters.
        """
        ...

    @abstractmethod
    def parse_webhook(self, raw_event: dict) -> CanonicalEvent | None:
        """
        Convert a raw webhook payload to a CanonicalEvent.
        Return None to discard (unsupported event type, test ping, etc.).
        Raise ValueError for malformed payloads that should dead-letter.
        """
        ...

    # ── Poll surface ─────────────────────────────────────────────────────

    @abstractmethod
    def poll_intervals(self) -> dict[str, timedelta]:
        """
        Per-entity-type polling cadence.
        Return {} for webhook-only adapters.

        Keys are entity_type strings matching poll_watermarks.entity_type.
        Example:
          {
            "transaction":     timedelta(minutes=1),
            "customer":        timedelta(hours=1),
            "item":            timedelta(hours=24),
            "store":           timedelta(hours=24),
            "item_categories": timedelta(hours=24),
          }
        """
        ...

    @abstractmethod
    def poll(
        self,
        tenant_id: str,
        entity_type: str,
        since: datetime,
        credentials: dict,
        company_alias: str | None = None,
    ) -> PollResult:
        """
        Pull events for one entity_type since the watermark.
        Returns a PollResult with all CanonicalEvents and the new watermark.

        `credentials` is the decrypted credential dict for this tenant.
        `company_alias` is the Counterpoint company alias (None for Square).

        Must be idempotent: calling poll() twice with the same `since`
        produces the same events (or a superset — never a loss).
        """
        ...

    # ── Common ───────────────────────────────────────────────────────────

    @abstractmethod
    def auth_flow_class(self) -> Type:
        """
        Returns the class that manages credential collection and
        connection testing for this adapter.
        Square: SquareOAuthFlow
        Counterpoint: CounterpointBasicAuthFlow
        """
        ...

    @abstractmethod
    def seed_data(
        self,
        tenant_id: str,
        credentials: dict,
        company_alias: str | None = None,
    ) -> Iterator[Fixture]:
        """
        Yields Fixture batches for reference-data seeding at install time.
        Called once per tenant activation, in activation-ordering sequence.
        """
        ...

    @abstractmethod
    def test_connection(
        self,
        credentials: dict,
        company_alias: str | None = None,
    ) -> bool:
        """
        Verify credentials are valid and the API is reachable.
        Called during onboarding before writing to pos_tenant_credentials.
        Raise ConnectionError with a user-visible message on failure.
        """
        ...
```

## 5. Adapter registry

```python
# canary/services/pos/registry.py

from canary.services.pos.base import POSAdapter

_REGISTRY: dict[str, type[POSAdapter]] = {}


def register_adapter(adapter_class: type[POSAdapter]) -> type[POSAdapter]:
    """Decorator. Usage: @register_adapter above class definition."""
    provider = adapter_class.provider
    if not provider:
        raise ValueError(f"{adapter_class.__name__} must define provider")
    if provider in _REGISTRY:
        raise ValueError(f"Adapter already registered for provider '{provider}'")
    _REGISTRY[provider] = adapter_class
    return adapter_class


def get_adapter(provider: str) -> type[POSAdapter]:
    """Returns adapter class for a provider. Raises KeyError if not registered."""
    if provider not in _REGISTRY:
        raise KeyError(
            f"No adapter registered for provider '{provider}'. "
            f"Registered: {list(_REGISTRY)}"
        )
    return _REGISTRY[provider]


def providers() -> list[str]:
    """All registered provider codes."""
    return list(_REGISTRY.keys())
```

### Registration pattern

```python
# canary/services/pos/square/adapter.py
from canary.services.pos.registry import register_adapter
from canary.services.pos.base import POSAdapter

@register_adapter
class SquareAdapter(POSAdapter):
    provider = "square"
    def webhook_event_types(self) -> frozenset[str]: ...
    def poll_intervals(self) -> dict: return {}   # webhook-only
    ...

# canary/services/pos/counterpoint/adapter.py
@register_adapter
class CounterpointAdapter(POSAdapter):
    provider = "counterpoint"
    def webhook_event_types(self) -> frozenset[str]: return frozenset()  # poll-only
    def poll_intervals(self) -> dict: ...
    ...
```

Registry is loaded in `canary/__init__.py` via explicit imports of adapter
modules. No auto-discovery magic — adapter registration must be intentional.

## 6. source_systems catalog table

Provider metadata table. One row per registered adapter, seeded by Alembic
migration. The `source_code` here is the FK target for `external_identities.source_code`.

```sql
CREATE TABLE app.source_systems (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_code     TEXT NOT NULL UNIQUE,       -- 'square' | 'counterpoint'
    display_name    TEXT NOT NULL,              -- 'Square' | 'NCR Counterpoint'
    adapter_class   TEXT NOT NULL,              -- Python dotted path (documentation)
    supports_webhook BOOLEAN NOT NULL DEFAULT FALSE,
    supports_poll   BOOLEAN NOT NULL DEFAULT FALSE,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Seed data
INSERT INTO app.source_systems (source_code, display_name, adapter_class, supports_webhook, supports_poll)
VALUES
    ('square',       'Square',           'canary.services.pos.square.adapter.SquareAdapter',        TRUE,  FALSE),
    ('counterpoint', 'NCR Counterpoint', 'canary.services.pos.counterpoint.adapter.CounterpointAdapter', FALSE, TRUE)
ON CONFLICT (source_code) DO NOTHING;
```

## 7. pos_tenant_credentials table

Stores encrypted connection credentials for each merchant's POS source.
One row per `(merchant_id, source_code, company_alias)`. For Square,
credentials are OAuth tokens; for Counterpoint, they are Basic Auth +
API key + host configuration.

```sql
CREATE TABLE app.pos_tenant_credentials (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id     UUID NOT NULL REFERENCES app.merchants(id),
    source_code     TEXT NOT NULL REFERENCES app.source_systems(source_code),
    company_alias   TEXT,           -- NULL for Square; required for Counterpoint
                                    -- A merchant may have multiple CP companies

    -- Encrypted credential blob (AES-256 at rest via Flask-Talisman + key service)
    -- Shape varies by provider; documented in per-adapter auth SDDs
    credentials_enc BYTEA NOT NULL,

    -- Lifecycle
    status          TEXT NOT NULL DEFAULT 'active',
                    -- active | credential_error | suspended | disconnected
    status_reason   TEXT,           -- human-readable on non-active transitions
    last_tested_at  TIMESTAMPTZ,    -- last successful test_connection() call
    last_polled_at  TIMESTAMPTZ,    -- last successful poll() completion
    error_count     INTEGER NOT NULL DEFAULT 0,
    last_error_at   TIMESTAMPTZ,
    last_error_msg  TEXT,

    -- Canary metadata
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),

    UNIQUE (merchant_id, source_code, company_alias)
);

CREATE INDEX idx_pos_creds_merchant_source
    ON app.pos_tenant_credentials (merchant_id, source_code);

CREATE INDEX idx_pos_creds_active_source
    ON app.pos_tenant_credentials (source_code, status)
    WHERE status = 'active';
```

### Credential shapes per provider

**Square** (stored in `credentials_enc` as JSON):

```json
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer",
  "expires_at": "2026-07-01T00:00:00Z",
  "merchant_id_square": "MLXXXXXXXXX"
}
```

**Counterpoint** (stored in `credentials_enc` as JSON):

```json
{
  "host": "https://pos.retailerstore.com:81",
  "username": "MGMT",
  "password": "...",
  "api_key": "...",
  "company_alias": "MAINCO",
  "verify_ssl": true
}
```

`company_alias` in the credential JSON is redundant with the column — kept
in the blob for completeness and to allow the adapter to be self-contained.

### Credential encryption

Credentials are encrypted with AES-256-GCM using a key derived from the
application's `SECRET_KEY` + a per-row salt. The credential service:

```python
# canary/services/pos/credential_service.py

class CredentialService:
    def store(self, merchant_id, source_code, company_alias, credentials: dict) -> str:
        """Encrypt and persist credentials. Returns credential row ID."""

    def load(self, merchant_id, source_code, company_alias) -> dict:
        """Load and decrypt credentials. Raises CredentialNotFound if absent."""

    def rotate(self, credential_id, new_credentials: dict) -> None:
        """Replace encrypted blob without changing the row ID."""

    def invalidate(self, credential_id, reason: str) -> None:
        """Set status=credential_error. Halts polling for this source."""
```

Credentials are never logged. `credentials_enc` column is excluded from
all SQL query result sets that feed logging or audit tables.

## 8. Merchant source status lifecycle

```
                ┌─────────────────┐
                │    (onboarding) │
                │  test_connection│
                └────────┬────────┘
                         │ success
                         ▼
                    ┌──────────┐
                    │  active  │◀──────────────────┐
                    └────┬─────┘                   │
                         │ poll error               │ credential rotated
                         ▼                          │ + test_connection ok
               ┌──────────────────┐                │
               │ credential_error │────────────────┘
               └──────────────────┘
                         │
                         │ operator disconnects
                         ▼
                   ┌────────────┐
                   │ disconnected│
                   └────────────┘
```

The poll consumer checks `pos_tenant_credentials.status` before each poll
cycle. `credential_error` halts polling and sends a notification to the
merchant's primary user. Re-activation requires calling `test_connection()`
with new credentials.

Error escalation:
- `error_count >= 3` in a 1-hour window → status transitions to
  `credential_error`
- `error_count >= 1` for 401/403 responses → immediate `credential_error`
  (no grace period for auth failures)

## 9. Poll consumer loop

The poll consumer (`canary/services/pos/poll_consumer.py`) runs as a
background process, iterating over all active poll-capable tenant credentials:

```python
# Pseudocode — actual implementation in Cycle 7

async def run_poll_consumer():
    while True:
        active_sources = db.query(PosTenantCredentials).filter_by(
            status="active",
        ).join(
            SourceSystem,
            (SourceSystem.source_code == PosTenantCredentials.source_code)
            & (SourceSystem.supports_poll == True),
        ).all()

        for cred in active_sources:
            adapter = get_adapter(cred.source_code)()
            intervals = adapter.poll_intervals()

            for entity_type, interval in intervals.items():
                watermark = get_watermark(cred.merchant_id, cred.source_code,
                                          cred.company_alias, entity_type)
                if watermark.last_polled_at + interval > now():
                    continue  # not due yet

                credentials = credential_service.load(
                    cred.merchant_id, cred.source_code, cred.company_alias
                )
                result = adapter.poll(
                    tenant_id=cred.merchant_id,
                    entity_type=entity_type,
                    since=watermark.last_event_ts or epoch,
                    credentials=credentials,
                    company_alias=cred.company_alias,
                )

                if result.success:
                    for event in result.events:
                        publish_to_stream(event)
                    advance_watermark(watermark, result.new_watermark)
                    cred.error_count = 0
                else:
                    handle_poll_error(cred, result.error)

        sleep(POLL_CONSUMER_TICK_SECONDS)  # default 30s
```

The 30-second tick is the outer loop frequency; actual poll frequency
per entity is governed by `poll_intervals()` + watermark state.

## 10. webhook_dispatch source-keying

The existing `webhook_dispatch.py` uses a flat `event_type → handler` dict.
The multi-POS refactor (Cycle 7, L3B-01) replaces it with a compound
`(provider, event_type) → handler` dispatch:

```python
# canary/services/webhook_dispatch.py (after refactor)

EVENT_PARSERS: dict[tuple[str, str], Callable] = {}

def register_webhook_handlers():
    """Called at app startup. Iterates registered adapters and builds dispatch table."""
    for provider_code in providers():
        adapter = get_adapter(provider_code)()
        for event_type in adapter.webhook_event_types():
            key = (provider_code, event_type)
            EVENT_PARSERS[key] = adapter.parse_webhook

def dispatch_webhook(request, provider: str) -> CanonicalEvent | None:
    """Route a raw webhook request to the correct adapter parser."""
    raw = request.get_json()
    event_type = extract_event_type(raw, provider)
    key = (provider, event_type)
    parser = EVENT_PARSERS.get(key)
    if parser is None:
        return None  # unknown event type for this provider
    return parser(raw)
```

Square webhooks continue routing through `provider = "square"` (derived
from the webhook endpoint URL path or signature key lookup). This is a
non-breaking refactor — Square behavior is unchanged.

## 11. Contract test requirements

`tests/contracts/test_pos_adapter.py` parameterizes over all registered
adapters and verifies the ABC contract:

```python
import pytest
from canary.services.pos.registry import providers, get_adapter

@pytest.fixture(params=providers())
def adapter(request):
    return get_adapter(request.param)()

def test_provider_set(adapter):
    assert isinstance(adapter.provider, str) and adapter.provider

def test_webhook_event_types_type(adapter):
    result = adapter.webhook_event_types()
    assert isinstance(result, frozenset)

def test_poll_intervals_type(adapter):
    result = adapter.poll_intervals()
    assert isinstance(result, dict)
    for k, v in result.items():
        assert isinstance(k, str)
        assert isinstance(v, timedelta)

def test_poll_only_or_webhook_only_or_both(adapter):
    has_webhooks = bool(adapter.webhook_event_types())
    has_polling   = bool(adapter.poll_intervals())
    assert has_webhooks or has_polling, (
        f"Adapter '{adapter.provider}' has neither webhook nor poll surface"
    )

def test_auth_flow_class(adapter):
    cls = adapter.auth_flow_class()
    assert isinstance(cls, type)

def test_no_event_type_overlap_across_providers():
    """Two providers cannot register the same (provider, event_type) pair."""
    seen = set()
    for provider_code in providers():
        a = get_adapter(provider_code)()
        for et in a.webhook_event_types():
            key = (provider_code, et)
            assert key not in seen
            seen.add(key)
```

The suite runs green with zero registered adapters (vacuously). It begins
failing as adapters are registered without full conformance. This is the
intended behavior — it enforces the contract incrementally during Cycle 7.

## 12. File structure (Cycle 7 target)

```
Canary/canary/services/pos/
├── __init__.py               # imports adapter modules to trigger registration
├── base.py                   # CanonicalEvent, Fixture, PollResult, POSAdapter ABC
├── registry.py               # register_adapter(), get_adapter(), providers()
├── poll_consumer.py          # poll loop; reads pos_tenant_credentials
├── credential_service.py     # encrypt/decrypt credential blobs
│
├── square/
│   ├── __init__.py
│   ├── adapter.py            # SquareAdapter (registered)
│   ├── oauth.py              # moved from services/square_oauth.py
│   └── parsers/              # moved from services/parsers/square_*.py (16 files)
│       └── ...
│
└── counterpoint/
    ├── __init__.py
    ├── adapter.py            # CounterpointAdapter (registered)
    ├── auth.py               # CounterpointBasicAuthFlow
    ├── client.py             # HTTP client (Basic Auth + APIKey headers)
    └── parsers/
        ├── document.py       # parse_cp_transaction, parse_cp_return, ...
        ├── customer.py       # parse_cp_customer
        ├── item.py           # parse_cp_item, parse_cp_item_categories
        └── store.py          # parse_cp_store, parse_cp_station
```

**Square refactor is a rename, not a rewrite.** All 16 Square parser files
move to their new home; their import paths change, but function signatures
and behavior are unchanged. Tests are updated to import from new paths.

## 13. New tables summary — Alembic migration checklist

| Table | Schema | Action | Notes |
|---|---|---|---|
| `source_systems` | app | CREATE + seed | Provider catalog; FK for external_identities |
| `pos_tenant_credentials` | app | CREATE | Encrypted creds + lifecycle |
| `external_identities.source_code` FK | app | FK to source_systems | Enforce provider validity |

## 14. Acceptance criteria

**AC-POS-01 — Registry:** After startup, `providers()` returns at least
`["square", "counterpoint"]`. `get_adapter("unknown")` raises `KeyError`.

**AC-POS-02 — Contract tests:** The full `tests/contracts/test_pos_adapter.py`
suite passes with both Square and Counterpoint registered.

**AC-POS-03 — Square non-regression:** After the file-move refactor,
all existing Square integration tests pass without modification to test
logic. Square webhook dispatch produces identical CanonicalEvents as
before the refactor.

**AC-POS-04 — Credential storage:** `CredentialService.store()` encrypts
credentials such that `credentials_enc` in the DB contains no plaintext
passwords or API keys. `CredentialService.load()` round-trips correctly.

**AC-POS-05 — Poll consumer cadence:** For a Counterpoint tenant with
`poll_intervals = {"transaction": timedelta(minutes=1)}`, the poll loop
invokes `poll()` at approximately 1-minute intervals. Jitter within ±10s
is acceptable.

**AC-POS-06 — Credential error halt:** Three consecutive failed poll()
calls (simulated with a bad API key) transition `pos_tenant_credentials.status`
to `credential_error`. Subsequent poll loop iterations skip this credential.
A notification event is emitted.

**AC-POS-07 — Multi-company:** A single merchant with two Counterpoint
company aliases (e.g., `MAINCO` + `REGIONCO`) has two rows in
`pos_tenant_credentials`. The poll consumer polls each independently with
the correct alias passed to `poll()`. Events from both companies reach
the `canary:events` stream with distinct `company_alias` values.

## 15. Open questions

| ID | Question | Impact |
|---|---|---|
| POS-OQ-01 | Square OAuth token is per-merchant (global); Counterpoint credentials are per-`(merchant, company_alias)`. Should `pos_tenant_credentials` store one row for Square (no company_alias) or enforce `company_alias = NULL` constraint for Square? Current design: `UNIQUE (merchant_id, source_code, company_alias)` with `company_alias = NULL` for Square — this works with PostgreSQL's NULL-distinct semantics. Verify this doesn't create index conflicts. | Schema constraint correctness |
| POS-OQ-02 | Credential encryption key management. Current design uses `SECRET_KEY` derivation. Should this use a separate CMK (customer master key) per merchant, stored in AWS KMS or similar? Adds operational complexity but isolates key compromise scope. | Security posture decision |
| POS-OQ-03 | Poll consumer deployment model. Run as a separate Flask-CLI command (`flask pos poll`), a Celery beat task, or a Thread spawned at app startup? Recommendation: Flask-CLI command run by a separate Gunicorn worker with `--timeout 300`. Confirm with ops. | Deployment architecture |
| POS-OQ-04 | On-demand poll trigger (cache-miss items, cache-miss stores). Cache-miss events are published to `canary:events` by the TSP parsers. The poll consumer needs a fast-path for on-demand fetches that bypasses the 1-minute cadence. Design: dedicated `canary:poll_demand` stream that the poll consumer drains before sleeping. | Cache-miss latency |

---

## Related

- `docs/sdds/canary/ncr-counterpoint-tsp-adapter.md` — Document adapter; uses POSAdapter poll surface
- `docs/sdds/canary/ncr-counterpoint-customer-adapter.md` — Customer adapter; poll surface
- `docs/sdds/canary/ncr-counterpoint-item-catalog-adapter.md` — Item adapter; poll surface
- `docs/sdds/canary/ncr-counterpoint-store-station-adapter.md` — Store adapter; poll surface + activation ordering
- `Canary/docs/sdds/v2/tsp.md` — TSP consumer architecture; CanonicalEvent consumer side
- `Canary/docs/sdds/v2/identity.md` — Square OAuth; SquareOAuthFlow reference
- `docs/superpowers/plans/2026-04-25-canary-for-rapidpos-delivery-spec.md` — Appendix A: original POSAdapter sketch
