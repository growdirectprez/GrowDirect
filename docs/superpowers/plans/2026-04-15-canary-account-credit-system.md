# Canary Account Management + Credit System Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a sat-denominated credit system with tunable gas fees, macaroon-based L402 gating, and Strike Lightning API integration for Canary merchants.

**Architecture:** Five new SQLAlchemy models in `app` schema, a `services/goose/` directory with Strike client, macaroon service, wallet service, gas meter, and L402 middleware. One new Flask blueprint (`goose_api`) on `/goose`. Hooks into existing Square OAuth onboarding. New dependency: `pymacaroons`.

**Tech Stack:** Python 3.12, Flask, SQLAlchemy 2.0 (`Mapped[]`), PostgreSQL 17 (`app` schema), Alembic, `pymacaroons`, Strike REST API, `canary/utils/crypto.py` (AES-256-GCM).

**Spec:** `docs/superpowers/specs/2026-04-15-canary-account-credit-system-design.md`

---

## Chunk 1: Data Models + Migration

### Task 1: MerchantWallet Model

**Files:**
- Create: `Canary/canary/models/app/merchant_wallet.py`
- Modify: `Canary/canary/models/app/__init__.py`
- Test: `Canary/tests/integration/test_goose_models.py`

- [ ] **Step 1: Write the failing test**

Create `Canary/tests/integration/test_goose_models.py`:

```python
"""Integration tests — Goose account/credit models.

Validates merchant_wallets, wallet_transactions, gas_schedule,
macaroon_tokens, and strike_invoices tables.
"""

import pytest
from sqlalchemy.exc import IntegrityError

from canary.models.app.merchant_wallet import MerchantWallet

pytestmark = pytest.mark.postgres


class TestMerchantWallet:
    """MerchantWallet model — custodial credit wallet per merchant."""

    def test_create_wallet_for_merchant(self, app_session, test_merchant):
        wallet = MerchantWallet(
            merchant_id=test_merchant.id,
            balance_sats=0,
            lifetime_funded_sats=0,
            lifetime_spent_sats=0,
            warning_threshold_sats=20000,
            hard_floor_sats=0,
            status="active",
            funded_by="treasury",
        )
        app_session.add(wallet)
        app_session.flush()

        assert wallet.id is not None
        assert wallet.balance_sats == 0
        assert wallet.status == "active"
        assert wallet.merchant_id == test_merchant.id

    def test_wallet_unique_per_merchant(self, app_session, test_merchant):
        w1 = MerchantWallet(
            merchant_id=test_merchant.id,
            balance_sats=0,
            lifetime_funded_sats=0,
            lifetime_spent_sats=0,
            status="active",
            funded_by="treasury",
        )
        app_session.add(w1)
        app_session.flush()

        w2 = MerchantWallet(
            merchant_id=test_merchant.id,
            balance_sats=0,
            lifetime_funded_sats=0,
            lifetime_spent_sats=0,
            status="active",
            funded_by="treasury",
        )
        app_session.add(w2)
        with pytest.raises(IntegrityError):
            app_session.flush()

    def test_wallet_rejects_bogus_merchant_id(self, app_session):
        wallet = MerchantWallet(
            merchant_id="nonexistent-uuid-0000",
            balance_sats=0,
            lifetime_funded_sats=0,
            lifetime_spent_sats=0,
            status="active",
            funded_by="treasury",
        )
        app_session.add(wallet)
        with pytest.raises(IntegrityError):
            app_session.flush()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_goose_models.py::TestMerchantWallet -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'canary.models.app.merchant_wallet'`

- [ ] **Step 3: Write the MerchantWallet model**

Create `Canary/canary/models/app/merchant_wallet.py`:

```python
"""
Goose credit wallet — custodial sat balance per merchant.

merchant_wallets:  One wallet per merchant, tracks credit balance in sats.
"""

from typing import Optional

from sqlalchemy import String, BigInteger, Boolean, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column

from canary.models.base import AppBase, AuditMixin, generate_uuid


class MerchantWallet(AppBase, AuditMixin):
    """
    Custodial credit wallet per merchant. Balance denominated in satoshis.
    GrowDirect holds the keys — this is Wallet 1 (promotional credits).

    One wallet per merchant. FK to app.merchants.id.
    """
    __tablename__ = "merchant_wallets"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid,
        nullable=False,
    )
    merchant_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("merchants.id"),
        nullable=False,
        unique=True,
        index=True,
        comment="FK to merchants.id — one wallet per merchant",
    )
    balance_sats: Mapped[int] = mapped_column(
        BigInteger,
        default=0,
        server_default="0",
        nullable=False,
        comment="Current credit balance in satoshis. Can go negative (grace).",
    )
    lifetime_funded_sats: Mapped[int] = mapped_column(
        BigInteger,
        default=0,
        server_default="0",
        nullable=False,
    )
    lifetime_spent_sats: Mapped[int] = mapped_column(
        BigInteger,
        default=0,
        server_default="0",
        nullable=False,
    )
    warning_threshold_sats: Mapped[int] = mapped_column(
        BigInteger,
        default=20000,
        server_default="20000",
        nullable=False,
        comment="Alert merchant when balance drops below this sat amount.",
    )
    hard_floor_sats: Mapped[int] = mapped_column(
        BigInteger,
        default=0,
        server_default="0",
        nullable=False,
        comment="Below this, premium features gate (Fox, Owl, etc.).",
    )
    status: Mapped[str] = mapped_column(
        String(30),
        default="active",
        server_default="active",
        nullable=False,
        index=True,
        comment="active | warning | depleted | suspended",
    )
    funded_by: Mapped[str] = mapped_column(
        String(30),
        default="treasury",
        server_default="treasury",
        nullable=False,
        comment="treasury | self | mixed — who funded this wallet",
    )

    __table_args__ = (
        Index("idx_merchant_wallets_merchant_id", "merchant_id"),
        Index("idx_merchant_wallets_status", "status"),
    )
```

- [ ] **Step 4: Add to models `__init__.py`**

Add import line to `Canary/canary/models/app/__init__.py`:

```python
from canary.models.app.merchant_wallet import MerchantWallet
```

And add `"MerchantWallet"` to `__all__`.

- [ ] **Step 5: Run test to verify it passes**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_goose_models.py::TestMerchantWallet -v`
Expected: 3 PASSED

- [ ] **Step 6: Commit**

```bash
git add canary/models/app/merchant_wallet.py canary/models/app/__init__.py tests/integration/test_goose_models.py
git commit -m "feat(goose): add MerchantWallet model with integration tests"
```

---

### Task 2: WalletTransaction Model

**Files:**
- Create: `Canary/canary/models/app/wallet_transaction.py`
- Modify: `Canary/canary/models/app/__init__.py`
- Modify: `Canary/tests/integration/test_goose_models.py`

- [ ] **Step 1: Write the failing test**

Append to `Canary/tests/integration/test_goose_models.py`:

```python
from canary.models.app.wallet_transaction import WalletTransaction


class TestWalletTransaction:
    """WalletTransaction — immutable credit/debit ledger."""

    def test_create_credit_transaction(self, app_session, test_merchant):
        wallet = MerchantWallet(
            merchant_id=test_merchant.id,
            balance_sats=0,
            lifetime_funded_sats=0,
            lifetime_spent_sats=0,
            status="active",
            funded_by="treasury",
        )
        app_session.add(wallet)
        app_session.flush()

        tx = WalletTransaction(
            wallet_id=wallet.id,
            merchant_id=test_merchant.id,
            tx_type="credit",
            source="treasury_fund",
            operation_type=None,
            amount_sats=100000,
            balance_after_sats=100000,
            reference_id=None,
            reference_type=None,
            note="Initial treasury funding",
        )
        app_session.add(tx)
        app_session.flush()

        assert tx.id is not None
        assert tx.tx_type == "credit"
        assert tx.amount_sats == 100000
        assert tx.balance_after_sats == 100000

    def test_create_debit_transaction(self, app_session, test_merchant):
        wallet = MerchantWallet(
            merchant_id=test_merchant.id,
            balance_sats=100000,
            lifetime_funded_sats=100000,
            lifetime_spent_sats=0,
            status="active",
            funded_by="treasury",
        )
        app_session.add(wallet)
        app_session.flush()

        tx = WalletTransaction(
            wallet_id=wallet.id,
            merchant_id=test_merchant.id,
            tx_type="debit",
            source="gas_fee",
            operation_type="tsp.transaction.ingested",
            amount_sats=1,
            balance_after_sats=99999,
        )
        app_session.add(tx)
        app_session.flush()

        assert tx.operation_type == "tsp.transaction.ingested"
        assert tx.amount_sats == 1

    def test_transaction_rejects_bogus_wallet_id(self, app_session, test_merchant):
        tx = WalletTransaction(
            wallet_id="nonexistent-wallet-uuid",
            merchant_id=test_merchant.id,
            tx_type="credit",
            source="treasury_fund",
            amount_sats=100000,
            balance_after_sats=100000,
        )
        app_session.add(tx)
        with pytest.raises(IntegrityError):
            app_session.flush()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_goose_models.py::TestWalletTransaction -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Write the WalletTransaction model**

Create `Canary/canary/models/app/wallet_transaction.py`:

```python
"""
Goose wallet transaction ledger — INSERT-ONLY.

wallet_transactions:  Every credit and debit against a merchant wallet.
                      Immutable audit trail. Never UPDATE or DELETE.
"""

from typing import Optional

from sqlalchemy import String, BigInteger, Text, ForeignKey, Index, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from canary.models.base import AppBase, generate_uuid


class WalletTransaction(AppBase):
    """
    Immutable ledger entry. Every credit/debit to a merchant wallet.
    INSERT-ONLY — no updates, no deletes. This is the financial audit trail.

    Does NOT use AuditMixin because updated_at/created_by/modified_by
    are not meaningful for append-only records. Has its own created_at
    and updated_at (set once, never modified) for platform compliance.
    """
    __tablename__ = "wallet_transactions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid,
        nullable=False,
    )
    wallet_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("merchant_wallets.id"),
        nullable=False,
        index=True,
        comment="FK to merchant_wallets.id",
    )
    merchant_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("merchants.id"),
        nullable=False,
        index=True,
        comment="Denormalized for query speed — FK to merchants.id",
    )
    tx_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        comment="credit | debit",
    )
    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Credits: treasury_fund, strike_payment, manual_credit, promo. Debits: gas_fee",
    )
    operation_type: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="Null for credits. For debits: matches gas_schedule.operation_key",
    )
    amount_sats: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        comment="Always positive. Direction determined by tx_type.",
    )
    balance_after_sats: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        comment="Running balance after this transaction",
    )
    reference_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        nullable=True,
        comment="FK to triggering record (alert, transaction, case, invoice)",
    )
    reference_type: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="chirp_alert | tsp_transaction | fox_case | owl_query | strike_invoice",
    )
    strike_invoice_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="Null unless this is a Strike payment credit",
    )
    note: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    created_at: Mapped["datetime"] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped["datetime"] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Set once at insert. Never modified. Present for platform compliance.",
    )

    __table_args__ = (
        Index("idx_wallet_tx_wallet_created", "wallet_id", "created_at"),
        Index("idx_wallet_tx_merchant_created", "merchant_id", "created_at"),
        Index("idx_wallet_tx_reference", "reference_id", "reference_type"),
    )
```

Add `from datetime import datetime` at the top of the file.

- [ ] **Step 4: Add to models `__init__.py`**

Add import and `__all__` entry for `WalletTransaction`.

- [ ] **Step 5: Run test to verify it passes**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_goose_models.py::TestWalletTransaction -v`
Expected: 3 PASSED

- [ ] **Step 6: Commit**

```bash
git add canary/models/app/wallet_transaction.py canary/models/app/__init__.py tests/integration/test_goose_models.py
git commit -m "feat(goose): add WalletTransaction model (INSERT-ONLY ledger)"
```

---

### Task 3: GasSchedule Model

**Files:**
- Create: `Canary/canary/models/app/gas_schedule.py`
- Modify: `Canary/canary/models/app/__init__.py`
- Modify: `Canary/tests/integration/test_goose_models.py`

- [ ] **Step 1: Write the failing test**

Append to test file:

```python
from canary.models.app.gas_schedule import GasSchedule


class TestGasSchedule:
    """GasSchedule — tunable pricing per operation type."""

    def test_create_gas_schedule_entry(self, app_session):
        entry = GasSchedule(
            operation_key="tsp.transaction.ingested",
            category="transaction",
            description="Per transaction through TSP pipeline",
            cost_sats=1,
            is_active=True,
        )
        app_session.add(entry)
        app_session.flush()

        assert entry.id is not None
        assert entry.cost_sats == 1
        assert entry.is_active is True

    def test_operation_key_unique(self, app_session):
        e1 = GasSchedule(
            operation_key="test.duplicate.key",
            category="transaction",
            description="First",
            cost_sats=1,
            is_active=True,
        )
        app_session.add(e1)
        app_session.flush()

        e2 = GasSchedule(
            operation_key="test.duplicate.key",
            category="transaction",
            description="Second",
            cost_sats=2,
            is_active=True,
        )
        app_session.add(e2)
        with pytest.raises(IntegrityError):
            app_session.flush()

    def test_tier_overrides_jsonb(self, app_session):
        entry = GasSchedule(
            operation_key="test.tier.override",
            category="compute",
            description="Test with tier overrides",
            cost_sats=100,
            is_active=True,
            tier_overrides={"starter": 100, "pro": 50, "enterprise": 0},
        )
        app_session.add(entry)
        app_session.flush()

        assert entry.tier_overrides["enterprise"] == 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_goose_models.py::TestGasSchedule -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Write the GasSchedule model**

Create `Canary/canary/models/app/gas_schedule.py`:

```python
"""
Goose gas schedule — tunable sat pricing per operation type.

gas_schedule:  Each metered operation has a configurable cost in sats.
               Adjustable without code changes via admin API.
"""

from typing import Optional

from sqlalchemy import String, BigInteger, Boolean, Text, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from canary.models.base import AppBase, AuditMixin, generate_uuid


class GasSchedule(AppBase, AuditMixin):
    """
    Tunable pricing table. Each operation type has a sat cost.
    operation_key is the unique identifier (e.g. 'tsp.transaction.ingested').
    cost_sats = 0 means the operation is free.
    """
    __tablename__ = "gas_schedule"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid,
        nullable=False,
    )
    operation_key: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
        comment="Unique key, e.g. tsp.transaction.ingested, chirp.alert.fired",
    )
    category: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        comment="transaction | detection | compute",
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    cost_sats: Mapped[int] = mapped_column(
        BigInteger,
        default=0,
        server_default="0",
        nullable=False,
        comment="Cost in satoshis. 0 = free.",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default="true",
        nullable=False,
        comment="Can disable metering on specific operations",
    )
    tier_overrides: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        comment='Per-tier pricing overrides. e.g. {"starter": 1, "pro": 0}',
    )

    __table_args__ = (
        Index("idx_gas_schedule_category", "category"),
    )
```

- [ ] **Step 4: Add to models `__init__.py`**

Add import and `__all__` entry for `GasSchedule`.

- [ ] **Step 5: Run test to verify it passes**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_goose_models.py::TestGasSchedule -v`
Expected: 3 PASSED

- [ ] **Step 6: Commit**

```bash
git add canary/models/app/gas_schedule.py canary/models/app/__init__.py tests/integration/test_goose_models.py
git commit -m "feat(goose): add GasSchedule model with tunable sat pricing"
```

---

### Task 4: MacaroonToken Model

**Files:**
- Create: `Canary/canary/models/app/macaroon_token.py`
- Modify: `Canary/canary/models/app/__init__.py`
- Modify: `Canary/tests/integration/test_goose_models.py`

- [ ] **Step 1: Write the failing test**

Append to test file:

```python
from datetime import datetime, timedelta, timezone
from canary.models.app.macaroon_token import MacaroonToken


class TestMacaroonToken:
    """MacaroonToken — tracks minted macaroons (metadata, not the secret)."""

    def test_create_macaroon_token(self, app_session, test_merchant):
        now = datetime.now(timezone.utc)
        token = MacaroonToken(
            merchant_id=test_merchant.id,
            macaroon_hash="sha256:abc123def456",
            caveats={"merchant_id": test_merchant.id, "tier": "free", "expires_at": str(now + timedelta(days=30))},
            status="active",
            minted_at=now,
            expires_at=now + timedelta(days=30),
        )
        app_session.add(token)
        app_session.flush()

        assert token.id is not None
        assert token.status == "active"
        assert token.caveats["tier"] == "free"

    def test_macaroon_rejects_bogus_merchant(self, app_session):
        now = datetime.now(timezone.utc)
        token = MacaroonToken(
            merchant_id="nonexistent-uuid-0000",
            macaroon_hash="sha256:bogus",
            caveats={},
            status="active",
            minted_at=now,
            expires_at=now + timedelta(days=30),
        )
        app_session.add(token)
        with pytest.raises(IntegrityError):
            app_session.flush()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_goose_models.py::TestMacaroonToken -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Write the MacaroonToken model**

Create `Canary/canary/models/app/macaroon_token.py`:

```python
"""
Goose macaroon token registry — tracks minted L402 tokens.

macaroon_tokens:  Metadata about minted macaroons. NOT the token itself.
                  The actual macaroon bytes are never stored server-side.
"""

from typing import Optional
from datetime import datetime

from sqlalchemy import String, ForeignKey, Index, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from canary.models.base import AppBase, generate_uuid


class MacaroonToken(AppBase):
    """
    Tracks minted macaroon tokens. Stores metadata (hash, caveats, status),
    NOT the token bytes. The macaroon_hash is SHA-256 of the serialized
    macaroon for lookup/revocation purposes.

    Status: active | exhausted | expired | revoked
    """
    __tablename__ = "macaroon_tokens"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid,
        nullable=False,
    )
    merchant_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("merchants.id"),
        nullable=False,
        index=True,
        comment="FK to merchants.id — who this token was minted for",
    )
    macaroon_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        comment="SHA-256 of macaroon bytes — for lookup, not the secret",
    )
    caveats: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        comment="Snapshot of caveats at mint time",
    )
    status: Mapped[str] = mapped_column(
        String(30),
        default="active",
        server_default="active",
        nullable=False,
        index=True,
        comment="active | exhausted | expired | revoked",
    )
    minted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        comment="From the expires_at caveat",
    )
    revoked_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    replaced_by: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("macaroon_tokens.id"),
        nullable=True,
        comment="Points to the replacement token",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    __table_args__ = (
        Index("idx_macaroon_tokens_merchant_status", "merchant_id", "status"),
    )
```

- [ ] **Step 4: Add to models `__init__.py`**

Add import and `__all__` entry for `MacaroonToken`.

- [ ] **Step 5: Run test to verify it passes**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_goose_models.py::TestMacaroonToken -v`
Expected: 2 PASSED

- [ ] **Step 6: Commit**

```bash
git add canary/models/app/macaroon_token.py canary/models/app/__init__.py tests/integration/test_goose_models.py
git commit -m "feat(goose): add MacaroonToken model for L402 token registry"
```

---

### Task 5: StrikeInvoice Model

**Files:**
- Create: `Canary/canary/models/app/strike_invoice.py`
- Modify: `Canary/canary/models/app/__init__.py`
- Modify: `Canary/tests/integration/test_goose_models.py`

- [ ] **Step 1: Write the failing test**

Append to test file:

```python
from canary.models.app.strike_invoice import StrikeInvoice


class TestStrikeInvoice:
    """StrikeInvoice — Lightning invoices for credit refills."""

    def test_create_strike_invoice(self, app_session, test_merchant):
        wallet = MerchantWallet(
            merchant_id=test_merchant.id,
            balance_sats=0,
            lifetime_funded_sats=0,
            lifetime_spent_sats=0,
            status="active",
            funded_by="treasury",
        )
        app_session.add(wallet)
        app_session.flush()

        invoice = StrikeInvoice(
            merchant_id=test_merchant.id,
            wallet_id=wallet.id,
            strike_invoice_id="inv_abc123",
            amount_usd=10.00,
            amount_sats=10000,
            conversion_rate=100000.00000000,
            bolt11_enc="GCM:encrypted_bolt11_data",
            payment_hash_enc="GCM:encrypted_payment_hash",
            state="pending",
        )
        app_session.add(invoice)
        app_session.flush()

        assert invoice.id is not None
        assert invoice.state == "pending"
        assert invoice.amount_sats == 10000

    def test_strike_invoice_id_unique(self, app_session, test_merchant):
        wallet = MerchantWallet(
            merchant_id=test_merchant.id,
            balance_sats=0,
            lifetime_funded_sats=0,
            lifetime_spent_sats=0,
            status="active",
            funded_by="treasury",
        )
        app_session.add(wallet)
        app_session.flush()

        inv1 = StrikeInvoice(
            merchant_id=test_merchant.id,
            wallet_id=wallet.id,
            strike_invoice_id="inv_dedup_test",
            amount_usd=10.00,
            amount_sats=10000,
            conversion_rate=100000.00000000,
            state="pending",
        )
        app_session.add(inv1)
        app_session.flush()

        inv2 = StrikeInvoice(
            merchant_id=test_merchant.id,
            wallet_id=wallet.id,
            strike_invoice_id="inv_dedup_test",
            amount_usd=20.00,
            amount_sats=20000,
            conversion_rate=100000.00000000,
            state="pending",
        )
        app_session.add(inv2)
        with pytest.raises(IntegrityError):
            app_session.flush()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_goose_models.py::TestStrikeInvoice -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Write the StrikeInvoice model**

Create `Canary/canary/models/app/strike_invoice.py`:

```python
"""
Goose Strike invoice tracking — Lightning invoices for credit refills.

strike_invoices:  Tracks every Strike Lightning invoice created for
                  merchant wallet top-ups. Encrypted fields for bolt11
                  and payment_hash (AES-256-GCM via canary/utils/crypto.py).
"""

from typing import Optional
from datetime import datetime
from decimal import Decimal

from sqlalchemy import String, BigInteger, Numeric, Text, ForeignKey, Index, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from canary.models.base import AppBase, generate_uuid


class StrikeInvoice(AppBase):
    """
    Strike Lightning invoice for merchant wallet top-up.

    bolt11_enc and payment_hash_enc are stored encrypted (AES-256-GCM).
    preimage_enc is populated on settlement (proof of payment).

    strike_invoice_id is the idempotency key — webhook dedup uses this.
    """
    __tablename__ = "strike_invoices"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=generate_uuid,
        nullable=False,
    )
    merchant_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("merchants.id"),
        nullable=False,
        index=True,
    )
    wallet_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("merchant_wallets.id"),
        nullable=False,
        index=True,
    )
    strike_invoice_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        comment="Strike's invoice identifier — idempotency key for webhook dedup",
    )
    amount_usd: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )
    amount_sats: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )
    conversion_rate: Mapped[Decimal] = mapped_column(
        Numeric(18, 8),
        nullable=False,
        comment="USD/BTC rate at invoice creation time",
    )
    bolt11_enc: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Lightning BOLT11 invoice string. Encrypted at rest (AES-256-GCM).",
    )
    payment_hash_enc: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="Lightning payment hash. Encrypted at rest.",
    )
    preimage_enc: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="Lightning preimage (proof of payment). Populated on settlement. Encrypted.",
    )
    state: Mapped[str] = mapped_column(
        String(30),
        default="pending",
        server_default="pending",
        nullable=False,
        index=True,
        comment="pending | paid | expired | canceled",
    )
    paid_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    __table_args__ = (
        Index("idx_strike_invoices_merchant_state", "merchant_id", "state"),
        Index("idx_strike_invoices_wallet", "wallet_id"),
    )
```

- [ ] **Step 4: Add to models `__init__.py`**

Add import and `__all__` entry for `StrikeInvoice`.

- [ ] **Step 5: Run test to verify it passes**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_goose_models.py::TestStrikeInvoice -v`
Expected: 2 PASSED

- [ ] **Step 6: Commit**

```bash
git add canary/models/app/strike_invoice.py canary/models/app/__init__.py tests/integration/test_goose_models.py
git commit -m "feat(goose): add StrikeInvoice model with encrypted fields"
```

---

### Task 6: Alembic Migration

**Files:**
- Create: `Canary/canary/migrations/versions/xxxx_goose_account_credit_system.py`

**Important:** The actual revision hash will be auto-generated by Alembic. The implementing agent should run `alembic revision --autogenerate` after all 5 models are in place, review the output, and apply.

- [ ] **Step 1: Generate the migration**

```bash
cd ~/GrowDirect/Canary
python3 -m alembic revision --autogenerate -m "goose account credit system — 5 tables"
```

- [ ] **Step 2: Review the generated migration**

Verify it creates these tables in the `app` schema:
- `merchant_wallets`
- `wallet_transactions`
- `gas_schedule`
- `macaroon_tokens`
- `strike_invoices`

Verify all indexes, FKs, and constraints are present. Check `schema='app'` on every `op.*` call.

- [ ] **Step 3: Run the migration**

```bash
cd ~/GrowDirect/Canary
python3 -m alembic upgrade head
```

Expected: Migration applies cleanly. All 5 tables created.

- [ ] **Step 4: Verify tables exist**

```bash
docker exec growdirect_postgres psql -U canary -d canary -c "
  SELECT tablename FROM pg_tables
  WHERE schemaname = 'app'
  AND tablename IN ('merchant_wallets', 'wallet_transactions', 'gas_schedule', 'macaroon_tokens', 'strike_invoices')
  ORDER BY tablename;"
```

Expected: 5 rows returned.

- [ ] **Step 5: Commit**

```bash
git add canary/migrations/versions/
git commit -m "feat(goose): alembic migration for 5 credit system tables"
```

---

### Task 7: Seed Gas Schedule

**Files:**
- Create: `Canary/canary/services/goose/__init__.py`
- Create: `Canary/canary/services/goose/seed.py`
- Test: `Canary/tests/integration/test_goose_models.py` (add seed test)

- [ ] **Step 1: Write the failing test**

Append to test file:

```python
from canary.services.goose.seed import seed_gas_schedule


class TestGasScheduleSeed:
    """Verify gas schedule seeding."""

    def test_seed_creates_entries(self, app_session):
        count = seed_gas_schedule(app_session)
        assert count == 11  # 11 operation types from spec

        entries = app_session.query(GasSchedule).all()
        assert len(entries) == 11

        # Gold list alerts must be free
        gold = app_session.query(GasSchedule).filter_by(
            operation_key="chirp.gold_list.fired"
        ).first()
        assert gold is not None
        assert gold.cost_sats == 0

    def test_seed_is_idempotent(self, app_session):
        seed_gas_schedule(app_session)
        seed_gas_schedule(app_session)

        entries = app_session.query(GasSchedule).all()
        assert len(entries) == 11  # No duplicates
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_goose_models.py::TestGasScheduleSeed -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Write the seed module**

Create `Canary/canary/services/goose/__init__.py`:

```python
"""Goose — account management, credit system, L402 gating."""
```

Create `Canary/canary/services/goose/seed.py`:

```python
"""
Seed the gas_schedule table with initial operation pricing.

Idempotent — safe to run multiple times. Uses operation_key
as the dedup key. Does not update existing entries (preserves
admin-tuned values).
"""

import logging

from canary.models.app.gas_schedule import GasSchedule

logger = logging.getLogger(__name__)

# Initial gas schedule — placeholder values, tune from real usage data.
# Gold list alerts are FREE (cost_sats=0) — they are the sales hook.
INITIAL_GAS_SCHEDULE = [
    ("tsp.transaction.ingested", "transaction", 1, "Per transaction through TSP pipeline"),
    ("tsp.transaction.batch", "transaction", 10, "Per webhook batch processed"),
    ("chirp.alert.fired", "detection", 5, "Per Chirp rule hit surfaced as alert"),
    ("chirp.gold_list.fired", "detection", 0, "Gold list alerts — always FREE"),
    ("fox.case.created", "compute", 100, "Fox case creation"),
    ("fox.evidence.attached", "compute", 50, "Evidence attachment to case"),
    ("owl.query.basic", "compute", 25, "Owl basic search"),
    ("owl.query.deep", "compute", 250, "Owl deep analysis"),
    ("owl.health_check", "compute", 500, "Weekly health check report"),
    ("vault.recall", "compute", 10, "Memory recall from vault"),
    ("receipt.proof", "compute", 50, "TSP receipt verification proof"),
]


def seed_gas_schedule(session) -> int:
    """Seed gas_schedule with initial entries. Returns count of new entries created."""
    created = 0
    for op_key, category, cost, description in INITIAL_GAS_SCHEDULE:
        existing = session.query(GasSchedule).filter_by(operation_key=op_key).first()
        if existing is None:
            entry = GasSchedule(
                operation_key=op_key,
                category=category,
                cost_sats=cost,
                description=description,
                is_active=True,
            )
            session.add(entry)
            created += 1

    if created > 0:
        session.flush()
        logger.info("Gas schedule seeded: %d new entries", created)

    return created
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_goose_models.py::TestGasScheduleSeed -v`
Expected: 2 PASSED

- [ ] **Step 5: Commit**

```bash
git add canary/services/goose/ tests/integration/test_goose_models.py
git commit -m "feat(goose): gas schedule seed with 11 initial operation types"
```

---

## Chunk 2: Core Services (Wallet, Gas Meter, Macaroon)

### Task 8: WalletService — Credit/Debit Operations

**Files:**
- Create: `Canary/canary/services/goose/wallet_service.py`
- Create: `Canary/tests/integration/test_goose_wallet_service.py`

- [ ] **Step 1: Write the failing test**

Create `Canary/tests/integration/test_goose_wallet_service.py`:

```python
"""Integration tests — WalletService credit/debit operations."""

import pytest

from canary.models.app.merchant_wallet import MerchantWallet
from canary.services.goose.wallet_service import WalletService

pytestmark = pytest.mark.postgres


class TestWalletServiceCredit:
    """WalletService.credit() — add sats to wallet."""

    def test_credit_increases_balance(self, app_session, test_merchant):
        wallet = MerchantWallet(
            merchant_id=test_merchant.id,
            balance_sats=0,
            lifetime_funded_sats=0,
            lifetime_spent_sats=0,
            status="active",
            funded_by="treasury",
        )
        app_session.add(wallet)
        app_session.flush()

        svc = WalletService(app_session)
        tx = svc.credit(
            wallet_id=wallet.id,
            merchant_id=test_merchant.id,
            amount_sats=100000,
            source="treasury_fund",
            note="Initial funding",
        )

        assert tx.amount_sats == 100000
        assert tx.balance_after_sats == 100000
        assert tx.tx_type == "credit"
        assert wallet.balance_sats == 100000
        assert wallet.lifetime_funded_sats == 100000


class TestWalletServiceDebit:
    """WalletService.debit() — subtract sats from wallet."""

    def test_debit_decreases_balance(self, app_session, test_merchant):
        wallet = MerchantWallet(
            merchant_id=test_merchant.id,
            balance_sats=100000,
            lifetime_funded_sats=100000,
            lifetime_spent_sats=0,
            status="active",
            funded_by="treasury",
        )
        app_session.add(wallet)
        app_session.flush()

        svc = WalletService(app_session)
        tx = svc.debit(
            wallet_id=wallet.id,
            merchant_id=test_merchant.id,
            amount_sats=100,
            operation_type="fox.case.created",
            reference_id=None,
            reference_type=None,
        )

        assert tx.amount_sats == 100
        assert tx.balance_after_sats == 99900
        assert wallet.balance_sats == 99900
        assert wallet.lifetime_spent_sats == 100

    def test_debit_sets_warning_status(self, app_session, test_merchant):
        wallet = MerchantWallet(
            merchant_id=test_merchant.id,
            balance_sats=20001,
            lifetime_funded_sats=100000,
            lifetime_spent_sats=79999,
            warning_threshold_sats=20000,
            status="active",
            funded_by="treasury",
        )
        app_session.add(wallet)
        app_session.flush()

        svc = WalletService(app_session)
        svc.debit(
            wallet_id=wallet.id,
            merchant_id=test_merchant.id,
            amount_sats=2,
            operation_type="tsp.transaction.ingested",
        )

        assert wallet.status == "warning"
        assert wallet.balance_sats == 19999

    def test_debit_sets_depleted_status(self, app_session, test_merchant):
        wallet = MerchantWallet(
            merchant_id=test_merchant.id,
            balance_sats=1,
            lifetime_funded_sats=100000,
            lifetime_spent_sats=99999,
            hard_floor_sats=0,
            status="warning",
            funded_by="treasury",
        )
        app_session.add(wallet)
        app_session.flush()

        svc = WalletService(app_session)
        svc.debit(
            wallet_id=wallet.id,
            merchant_id=test_merchant.id,
            amount_sats=1,
            operation_type="tsp.transaction.ingested",
        )

        assert wallet.status == "depleted"
        assert wallet.balance_sats == 0


class TestWalletServiceInsufficientFunds:
    """WalletService.check_balance() — returns False when insufficient."""

    def test_check_balance_returns_false_when_depleted(self, app_session, test_merchant):
        wallet = MerchantWallet(
            merchant_id=test_merchant.id,
            balance_sats=0,
            lifetime_funded_sats=100000,
            lifetime_spent_sats=100000,
            hard_floor_sats=0,
            status="depleted",
            funded_by="treasury",
        )
        app_session.add(wallet)
        app_session.flush()

        svc = WalletService(app_session)
        assert svc.check_balance(wallet.id, 100) is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_goose_wallet_service.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Write WalletService**

Create `Canary/canary/services/goose/wallet_service.py`:

```python
"""
WalletService — credit/debit operations on merchant wallets.

All balance mutations go through this service. Every operation creates
an immutable WalletTransaction record and updates the wallet balance.
"""

import logging
from typing import Optional

from canary.models.app.merchant_wallet import MerchantWallet
from canary.models.app.wallet_transaction import WalletTransaction

logger = logging.getLogger(__name__)


class WalletService:
    """Credit/debit operations on merchant wallets."""

    def __init__(self, session):
        self._session = session

    def get_wallet(self, merchant_id: str) -> Optional[MerchantWallet]:
        """Get wallet by merchant_id. Returns None if not found."""
        return self._session.query(MerchantWallet).filter_by(
            merchant_id=merchant_id
        ).first()

    def check_balance(self, wallet_id: str, required_sats: int) -> bool:
        """Check if wallet has sufficient balance for an operation."""
        wallet = self._session.query(MerchantWallet).filter_by(id=wallet_id).first()
        if wallet is None:
            return False
        return wallet.balance_sats >= required_sats

    def credit(
        self,
        wallet_id: str,
        merchant_id: str,
        amount_sats: int,
        source: str,
        note: Optional[str] = None,
        strike_invoice_id: Optional[str] = None,
        reference_id: Optional[str] = None,
        reference_type: Optional[str] = None,
    ) -> WalletTransaction:
        """Add sats to a wallet. Returns the ledger entry."""
        wallet = self._session.query(MerchantWallet).filter_by(id=wallet_id).one()

        wallet.balance_sats += amount_sats
        wallet.lifetime_funded_sats += amount_sats

        # Update funded_by tracking
        if source == "treasury_fund" and wallet.funded_by == "self":
            wallet.funded_by = "mixed"
        elif source in ("strike_payment", "manual_credit") and wallet.funded_by == "treasury":
            wallet.funded_by = "mixed"

        # Reset status based on new balance
        if wallet.balance_sats > wallet.warning_threshold_sats:
            wallet.status = "active"
        elif wallet.balance_sats > wallet.hard_floor_sats:
            wallet.status = "warning"

        tx = WalletTransaction(
            wallet_id=wallet_id,
            merchant_id=merchant_id,
            tx_type="credit",
            source=source,
            operation_type=None,
            amount_sats=amount_sats,
            balance_after_sats=wallet.balance_sats,
            reference_id=reference_id,
            reference_type=reference_type,
            strike_invoice_id=strike_invoice_id,
            note=note,
        )
        self._session.add(tx)
        self._session.flush()

        logger.info(
            "Wallet %s credited %d sats (source=%s, balance=%d)",
            wallet_id, amount_sats, source, wallet.balance_sats,
        )
        return tx

    def debit(
        self,
        wallet_id: str,
        merchant_id: str,
        amount_sats: int,
        operation_type: str,
        reference_id: Optional[str] = None,
        reference_type: Optional[str] = None,
    ) -> WalletTransaction:
        """Subtract sats from a wallet. Returns the ledger entry.

        Does NOT check balance — caller is responsible for gating.
        This allows grace period (negative balance).
        """
        wallet = self._session.query(MerchantWallet).filter_by(id=wallet_id).one()

        wallet.balance_sats -= amount_sats
        wallet.lifetime_spent_sats += amount_sats

        # Update wallet status based on new balance
        if wallet.balance_sats <= wallet.hard_floor_sats:
            wallet.status = "depleted"
        elif wallet.balance_sats < wallet.warning_threshold_sats:
            wallet.status = "warning"

        tx = WalletTransaction(
            wallet_id=wallet_id,
            merchant_id=merchant_id,
            tx_type="debit",
            source="gas_fee",
            operation_type=operation_type,
            amount_sats=amount_sats,
            balance_after_sats=wallet.balance_sats,
            reference_id=reference_id,
            reference_type=reference_type,
        )
        self._session.add(tx)
        self._session.flush()

        logger.info(
            "Wallet %s debited %d sats (op=%s, balance=%d, status=%s)",
            wallet_id, amount_sats, operation_type, wallet.balance_sats, wallet.status,
        )
        return tx
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_goose_wallet_service.py -v`
Expected: 5 PASSED

- [ ] **Step 5: Commit**

```bash
git add canary/services/goose/wallet_service.py tests/integration/test_goose_wallet_service.py
git commit -m "feat(goose): WalletService with credit/debit/balance operations"
```

---

### Task 9: GasMeter — Gas Schedule Lookup + Debit Orchestration

**Files:**
- Create: `Canary/canary/services/goose/gas_meter.py`
- Create: `Canary/tests/integration/test_goose_gas_meter.py`

- [ ] **Step 1: Write the failing test**

Create `Canary/tests/integration/test_goose_gas_meter.py`:

```python
"""Integration tests — GasMeter gas schedule lookup and metering."""

import pytest

from canary.models.app.merchant_wallet import MerchantWallet
from canary.models.app.gas_schedule import GasSchedule
from canary.services.goose.gas_meter import GasMeter

pytestmark = pytest.mark.postgres


class TestGasMeterLookup:
    """GasMeter.get_cost() — look up operation cost from gas_schedule."""

    def test_get_cost_returns_sats(self, app_session):
        entry = GasSchedule(
            operation_key="test.meter.lookup",
            category="compute",
            description="Test entry",
            cost_sats=42,
            is_active=True,
        )
        app_session.add(entry)
        app_session.flush()

        meter = GasMeter(app_session)
        cost = meter.get_cost("test.meter.lookup")
        assert cost == 42

    def test_get_cost_returns_zero_for_free_ops(self, app_session):
        entry = GasSchedule(
            operation_key="test.meter.free",
            category="detection",
            description="Free operation",
            cost_sats=0,
            is_active=True,
        )
        app_session.add(entry)
        app_session.flush()

        meter = GasMeter(app_session)
        assert meter.get_cost("test.meter.free") == 0

    def test_get_cost_returns_zero_for_inactive(self, app_session):
        entry = GasSchedule(
            operation_key="test.meter.inactive",
            category="compute",
            description="Inactive operation",
            cost_sats=100,
            is_active=False,
        )
        app_session.add(entry)
        app_session.flush()

        meter = GasMeter(app_session)
        assert meter.get_cost("test.meter.inactive") == 0

    def test_get_cost_returns_zero_for_unknown_key(self, app_session):
        meter = GasMeter(app_session)
        assert meter.get_cost("nonexistent.operation") == 0


class TestGasMeterCharge:
    """GasMeter.charge() — lookup + debit in one call."""

    def test_charge_debits_wallet(self, app_session, test_merchant):
        entry = GasSchedule(
            operation_key="test.meter.charge",
            category="compute",
            description="Test charge",
            cost_sats=50,
            is_active=True,
        )
        app_session.add(entry)
        app_session.flush()

        wallet = MerchantWallet(
            merchant_id=test_merchant.id,
            balance_sats=1000,
            lifetime_funded_sats=1000,
            lifetime_spent_sats=0,
            status="active",
            funded_by="treasury",
        )
        app_session.add(wallet)
        app_session.flush()

        meter = GasMeter(app_session)
        result = meter.charge(
            merchant_id=test_merchant.id,
            operation_key="test.meter.charge",
        )

        assert result.charged is True
        assert result.cost_sats == 50
        assert wallet.balance_sats == 950

    def test_charge_skips_free_operations(self, app_session, test_merchant):
        entry = GasSchedule(
            operation_key="test.meter.free.charge",
            category="detection",
            description="Free",
            cost_sats=0,
            is_active=True,
        )
        app_session.add(entry)
        app_session.flush()

        wallet = MerchantWallet(
            merchant_id=test_merchant.id,
            balance_sats=1000,
            lifetime_funded_sats=1000,
            lifetime_spent_sats=0,
            status="active",
            funded_by="treasury",
        )
        app_session.add(wallet)
        app_session.flush()

        meter = GasMeter(app_session)
        result = meter.charge(
            merchant_id=test_merchant.id,
            operation_key="test.meter.free.charge",
        )

        assert result.charged is False
        assert result.cost_sats == 0
        assert wallet.balance_sats == 1000  # Unchanged

    def test_charge_returns_insufficient_when_depleted(self, app_session, test_merchant):
        entry = GasSchedule(
            operation_key="test.meter.insufficient",
            category="compute",
            description="Expensive",
            cost_sats=500,
            is_active=True,
        )
        app_session.add(entry)
        app_session.flush()

        wallet = MerchantWallet(
            merchant_id=test_merchant.id,
            balance_sats=100,
            lifetime_funded_sats=100,
            lifetime_spent_sats=0,
            hard_floor_sats=0,
            status="active",
            funded_by="treasury",
        )
        app_session.add(wallet)
        app_session.flush()

        meter = GasMeter(app_session)
        result = meter.charge(
            merchant_id=test_merchant.id,
            operation_key="test.meter.insufficient",
        )

        assert result.charged is False
        assert result.insufficient is True
        assert result.cost_sats == 500
        assert wallet.balance_sats == 100  # Unchanged
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_goose_gas_meter.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Write GasMeter**

Create `Canary/canary/services/goose/gas_meter.py`:

```python
"""
GasMeter — gas schedule lookup and debit orchestration.

Looks up the sat cost for an operation from gas_schedule,
checks wallet balance, and debits if sufficient.
"""

import logging
from dataclasses import dataclass
from typing import Optional

from canary.models.app.gas_schedule import GasSchedule
from canary.models.app.merchant_wallet import MerchantWallet
from canary.services.goose.wallet_service import WalletService

logger = logging.getLogger(__name__)


@dataclass
class ChargeResult:
    """Result of a gas charge attempt."""
    charged: bool
    cost_sats: int
    insufficient: bool = False
    wallet_status: Optional[str] = None


class GasMeter:
    """Gas schedule lookup and metered debit orchestration."""

    def __init__(self, session):
        self._session = session
        self._wallet_svc = WalletService(session)

    def get_cost(self, operation_key: str, tier: Optional[str] = None) -> int:
        """Look up the sat cost for an operation. Returns 0 if not found or inactive."""
        entry = self._session.query(GasSchedule).filter_by(
            operation_key=operation_key
        ).first()

        if entry is None or not entry.is_active:
            return 0

        # Check tier override
        if tier and entry.tier_overrides and tier in entry.tier_overrides:
            return entry.tier_overrides[tier]

        return entry.cost_sats

    def charge(
        self,
        merchant_id: str,
        operation_key: str,
        reference_id: Optional[str] = None,
        reference_type: Optional[str] = None,
        tier: Optional[str] = None,
    ) -> ChargeResult:
        """Look up cost, check balance, debit if sufficient.

        Returns ChargeResult with charged=True if debited, or
        insufficient=True if balance too low.
        """
        cost = self.get_cost(operation_key, tier=tier)

        # Free operations — no debit needed
        if cost == 0:
            return ChargeResult(charged=False, cost_sats=0)

        wallet = self._wallet_svc.get_wallet(merchant_id)
        if wallet is None:
            logger.warning("No wallet for merchant %s, skipping charge", merchant_id)
            return ChargeResult(charged=False, cost_sats=cost, insufficient=True)

        # Check balance
        if wallet.balance_sats < cost:
            return ChargeResult(
                charged=False,
                cost_sats=cost,
                insufficient=True,
                wallet_status=wallet.status,
            )

        # Debit
        self._wallet_svc.debit(
            wallet_id=wallet.id,
            merchant_id=merchant_id,
            amount_sats=cost,
            operation_type=operation_key,
            reference_id=reference_id,
            reference_type=reference_type,
        )

        return ChargeResult(
            charged=True,
            cost_sats=cost,
            wallet_status=wallet.status,
        )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_goose_gas_meter.py -v`
Expected: 7 PASSED

- [ ] **Step 5: Commit**

```bash
git add canary/services/goose/gas_meter.py tests/integration/test_goose_gas_meter.py
git commit -m "feat(goose): GasMeter with schedule lookup and charge orchestration"
```

---

### Task 10: MacaroonService — Mint, Verify, Revoke

**Files:**
- Create: `Canary/canary/services/goose/macaroon_service.py`
- Create: `Canary/tests/integration/test_goose_macaroon_service.py`

**Dependency:** `pymacaroons` must be installed first.

- [ ] **Step 1: Flag dependency — get approval to add `pymacaroons`**

Check if it's already in requirements: `grep pymacaroons ~/GrowDirect/Canary/requirements.txt`

If not present, tell the user: "Need to add `pymacaroons` to requirements.txt and rebuild the Docker image." Get approval before proceeding.

- [ ] **Step 2: Add `pymacaroons` to requirements.txt and rebuild**

```bash
echo "pymacaroons>=0.13.0" >> ~/GrowDirect/Canary/requirements.txt
cd ~/GrowDirect/Canary/devops && docker compose build flask
```

- [ ] **Step 3: Write the failing test**

Create `Canary/tests/integration/test_goose_macaroon_service.py`:

```python
"""Integration tests — MacaroonService mint, verify, revoke."""

import os
import pytest
from datetime import datetime, timedelta, timezone

from canary.services.goose.macaroon_service import MacaroonService

pytestmark = pytest.mark.postgres

# Test root key — never use in production
TEST_ROOT_KEY = "test-macaroon-root-key-32bytes!"


class TestMacaroonMint:
    """MacaroonService.mint() — create a new macaroon for a merchant."""

    def test_mint_returns_serialized_macaroon(self, app_session, test_merchant):
        svc = MacaroonService(app_session, root_key=TEST_ROOT_KEY)
        macaroon_bytes, token_record = svc.mint(
            merchant_id=test_merchant.id,
            tier="free",
            ttl_days=30,
        )

        assert macaroon_bytes is not None
        assert len(macaroon_bytes) > 0
        assert token_record.status == "active"
        assert token_record.merchant_id == test_merchant.id
        assert "merchant_id" in token_record.caveats

    def test_mint_creates_db_record(self, app_session, test_merchant):
        svc = MacaroonService(app_session, root_key=TEST_ROOT_KEY)
        _, token_record = svc.mint(
            merchant_id=test_merchant.id,
            tier="free",
            ttl_days=30,
        )

        from canary.models.app.macaroon_token import MacaroonToken
        found = app_session.query(MacaroonToken).filter_by(id=token_record.id).first()
        assert found is not None
        assert found.status == "active"


class TestMacaroonVerify:
    """MacaroonService.verify() — validate a macaroon and extract caveats."""

    def test_verify_valid_macaroon(self, app_session, test_merchant):
        svc = MacaroonService(app_session, root_key=TEST_ROOT_KEY)
        macaroon_bytes, _ = svc.mint(
            merchant_id=test_merchant.id,
            tier="free",
            ttl_days=30,
        )

        result = svc.verify(macaroon_bytes)
        assert result.valid is True
        assert result.merchant_id == test_merchant.id
        assert result.tier == "free"

    def test_verify_rejects_tampered_macaroon(self, app_session, test_merchant):
        svc = MacaroonService(app_session, root_key=TEST_ROOT_KEY)
        macaroon_bytes, _ = svc.mint(
            merchant_id=test_merchant.id,
            tier="free",
            ttl_days=30,
        )

        # Tamper with the macaroon
        tampered = macaroon_bytes[:-4] + b"XXXX"
        result = svc.verify(tampered)
        assert result.valid is False

    def test_verify_rejects_wrong_root_key(self, app_session, test_merchant):
        svc = MacaroonService(app_session, root_key=TEST_ROOT_KEY)
        macaroon_bytes, _ = svc.mint(
            merchant_id=test_merchant.id,
            tier="free",
            ttl_days=30,
        )

        wrong_svc = MacaroonService(app_session, root_key="wrong-key-wrong-key-32bytesXXXX")
        result = wrong_svc.verify(macaroon_bytes)
        assert result.valid is False


class TestMacaroonRevoke:
    """MacaroonService.revoke() — invalidate a macaroon by ID."""

    def test_revoke_sets_status(self, app_session, test_merchant):
        svc = MacaroonService(app_session, root_key=TEST_ROOT_KEY)
        _, token_record = svc.mint(
            merchant_id=test_merchant.id,
            tier="free",
            ttl_days=30,
        )

        svc.revoke(token_record.id)
        assert token_record.status == "revoked"
        assert token_record.revoked_at is not None
```

- [ ] **Step 4: Run test to verify it fails**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_goose_macaroon_service.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 5: Write MacaroonService**

Create `Canary/canary/services/goose/macaroon_service.py`:

```python
"""
MacaroonService — mint, verify, and revoke L402 macaroon tokens.

Macaroons are cryptographic authorization tokens with chainable caveats.
Each caveat restricts the token's scope (merchant_id, tier, expiry).
Caveats can only restrict, never expand.
"""

import hashlib
import logging
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple

from pymacaroons import Macaroon, Verifier
from pymacaroons.exceptions import MacaroonInvalidSignatureException

from canary.models.app.macaroon_token import MacaroonToken

logger = logging.getLogger(__name__)


@dataclass
class VerifyResult:
    """Result of macaroon verification."""
    valid: bool
    merchant_id: Optional[str] = None
    tier: Optional[str] = None
    expires_at: Optional[datetime] = None
    error: Optional[str] = None


class MacaroonService:
    """Mint, verify, and revoke L402 macaroon tokens."""

    def __init__(self, session, root_key: Optional[str] = None):
        self._session = session
        self._root_key = root_key or os.getenv("GOOSE_MACAROON_ROOT_KEY", "")

    def mint(
        self,
        merchant_id: str,
        tier: str = "free",
        ttl_days: int = 30,
        endpoints: Optional[str] = None,
    ) -> Tuple[bytes, MacaroonToken]:
        """Mint a new macaroon for a merchant. Returns (serialized_bytes, db_record)."""
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(days=ttl_days)

        # Create the macaroon with caveats
        m = Macaroon(
            location="canary",
            identifier=merchant_id,
            key=self._root_key,
        )
        m.add_first_party_caveat(f"merchant_id = {merchant_id}")
        m.add_first_party_caveat(f"tier = {tier}")
        m.add_first_party_caveat(f"expires_at = {expires_at.isoformat()}")
        if endpoints:
            m.add_first_party_caveat(f"endpoints = {endpoints}")

        serialized = m.serialize()
        macaroon_bytes = serialized.encode("utf-8") if isinstance(serialized, str) else serialized
        macaroon_hash = hashlib.sha256(macaroon_bytes).hexdigest()

        # Record in DB
        caveats = {
            "merchant_id": merchant_id,
            "tier": tier,
            "expires_at": expires_at.isoformat(),
        }
        if endpoints:
            caveats["endpoints"] = endpoints

        token_record = MacaroonToken(
            merchant_id=merchant_id,
            macaroon_hash=macaroon_hash,
            caveats=caveats,
            status="active",
            minted_at=now,
            expires_at=expires_at,
        )
        self._session.add(token_record)
        self._session.flush()

        logger.info("Minted macaroon for merchant %s (tier=%s, ttl=%dd)", merchant_id, tier, ttl_days)
        return macaroon_bytes, token_record

    def verify(self, macaroon_bytes: bytes) -> VerifyResult:
        """Verify a macaroon's signature and extract caveats."""
        try:
            serialized = macaroon_bytes.decode("utf-8") if isinstance(macaroon_bytes, bytes) else macaroon_bytes
            m = Macaroon.deserialize(serialized)

            v = Verifier()
            # Satisfy caveats by accepting any value (signature check is the gate)
            v.satisfy_general(lambda caveat: True)
            verified = v.verify(m, self._root_key)

            if not verified:
                return VerifyResult(valid=False, error="Signature verification failed")

            # Extract caveats
            caveats = {}
            for caveat in m.caveats:
                parts = caveat.caveat_id.split(" = ", 1)
                if len(parts) == 2:
                    caveats[parts[0].strip()] = parts[1].strip()

            # Check expiry
            expires_at_str = caveats.get("expires_at")
            if expires_at_str:
                expires_at = datetime.fromisoformat(expires_at_str)
                if datetime.now(timezone.utc) > expires_at:
                    return VerifyResult(valid=False, error="Token expired")
            else:
                expires_at = None

            # Check revocation status in DB
            macaroon_hash = hashlib.sha256(macaroon_bytes).hexdigest()
            token_record = self._session.query(MacaroonToken).filter_by(
                macaroon_hash=macaroon_hash
            ).first()
            if token_record and token_record.status == "revoked":
                return VerifyResult(valid=False, error="Token revoked")

            return VerifyResult(
                valid=True,
                merchant_id=caveats.get("merchant_id"),
                tier=caveats.get("tier"),
                expires_at=expires_at,
            )

        except MacaroonInvalidSignatureException:
            return VerifyResult(valid=False, error="Invalid signature")
        except Exception as e:
            logger.warning("Macaroon verification failed: %s", e)
            return VerifyResult(valid=False, error=str(e))

    def revoke(self, token_id: str) -> None:
        """Revoke a macaroon by its DB record ID."""
        token = self._session.query(MacaroonToken).filter_by(id=token_id).one()
        token.status = "revoked"
        token.revoked_at = datetime.now(timezone.utc)
        self._session.flush()
        logger.info("Revoked macaroon %s", token_id)
```

- [ ] **Step 6: Run test to verify it passes**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_goose_macaroon_service.py -v`
Expected: 6 PASSED

- [ ] **Step 7: Commit**

```bash
git add canary/services/goose/macaroon_service.py tests/integration/test_goose_macaroon_service.py requirements.txt
git commit -m "feat(goose): MacaroonService with mint/verify/revoke + pymacaroons dep"
```

---

## Chunk 3: Strike Client, Onboarding, Blueprint, Config

### Task 11: StrikeClient — Strike API Wrapper

**Files:**
- Create: `Canary/canary/services/goose/strike_client.py`
- Create: `Canary/tests/unit/test_goose_strike_client.py`

This service wraps the Strike REST API. Unit tests use mocked HTTP responses (no real API calls in CI).

- [ ] **Step 1: Write the failing test**

Create `Canary/tests/unit/test_goose_strike_client.py`:

```python
"""Unit tests — StrikeClient API wrapper (mocked HTTP)."""

import pytest
from unittest.mock import patch, MagicMock

from canary.services.goose.strike_client import StrikeClient


class TestStrikeClientInvoice:
    """StrikeClient.create_invoice() — create a Lightning invoice."""

    @patch("canary.services.goose.strike_client.requests")
    def test_create_invoice_returns_invoice_data(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "invoiceId": "inv_abc123",
            "amount": {"amount": "10.00", "currency": "USD"},
            "state": "UNPAID",
            "paymentHash": "hash_abc",
            "description": "Canary credit top-up",
        }
        mock_requests.post.return_value = mock_response

        client = StrikeClient(api_key="test-key", api_url="https://api.strike.me/v1")
        result = client.create_invoice(amount_usd=10.00, description="Canary credit top-up")

        assert result["invoiceId"] == "inv_abc123"
        assert result["state"] == "UNPAID"

    @patch("canary.services.goose.strike_client.requests")
    def test_create_invoice_raises_on_error(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_response.raise_for_status.side_effect = Exception("400 Bad Request")
        mock_requests.post.return_value = mock_response

        client = StrikeClient(api_key="test-key", api_url="https://api.strike.me/v1")
        with pytest.raises(Exception):
            client.create_invoice(amount_usd=10.00, description="test")


class TestStrikeClientQuote:
    """StrikeClient.get_quote() — get BTC/USD conversion quote."""

    @patch("canary.services.goose.strike_client.requests")
    def test_get_quote_returns_rate(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "quoteId": "quote_123",
            "sourceAmount": {"amount": "10.00", "currency": "USD"},
            "targetAmount": {"amount": "0.00010000", "currency": "BTC"},
            "conversionRate": {"amount": "100000.00", "currency": "BTCUSD"},
        }
        mock_requests.post.return_value = mock_response

        client = StrikeClient(api_key="test-key", api_url="https://api.strike.me/v1")
        result = client.get_quote(amount_usd=10.00)

        assert result["quoteId"] == "quote_123"


class TestStrikeWebhookVerify:
    """StrikeClient.verify_webhook() — HMAC signature verification."""

    def test_verify_webhook_valid_signature(self):
        import hmac
        import hashlib

        secret = "webhook-secret-123"
        body = b'{"invoiceId": "inv_abc123", "state": "PAID"}'
        signature = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()

        client = StrikeClient(api_key="test-key", webhook_secret=secret)
        assert client.verify_webhook(body, signature) is True

    def test_verify_webhook_invalid_signature(self):
        client = StrikeClient(api_key="test-key", webhook_secret="secret")
        assert client.verify_webhook(b"body", "invalid-sig") is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/unit/test_goose_strike_client.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Write StrikeClient**

Create `Canary/canary/services/goose/strike_client.py`:

```python
"""
StrikeClient — Strike REST API wrapper.

Handles invoice creation, quote generation, webhook verification,
and account balance queries. All HTTP calls go through this client.
"""

import hashlib
import hmac
import logging
import os
from typing import Optional

import requests

logger = logging.getLogger(__name__)

STRIKE_API_URL_DEFAULT = "https://api.strike.me/v1"


class StrikeClient:
    """Strike API client for Lightning invoice and payment operations."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        webhook_secret: Optional[str] = None,
    ):
        self._api_key = api_key or os.getenv("STRIKE_API_KEY", "")
        self._api_url = api_url or os.getenv("STRIKE_API_URL", STRIKE_API_URL_DEFAULT)
        self._webhook_secret = webhook_secret or os.getenv("GOOSE_WEBHOOK_SECRET", "")

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def create_invoice(self, amount_usd: float, description: str = "Canary credit top-up") -> dict:
        """Create a Strike invoice for the given USD amount.

        Returns the invoice data including invoiceId, paymentHash, and state.
        Raises on HTTP error.
        """
        payload = {
            "correlationId": None,
            "description": description,
            "amount": {
                "amount": f"{amount_usd:.2f}",
                "currency": "USD",
            },
        }
        resp = requests.post(
            f"{self._api_url}/invoices",
            json=payload,
            headers=self._headers(),
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()

    def get_invoice(self, invoice_id: str) -> dict:
        """Get invoice status by Strike invoice ID."""
        resp = requests.get(
            f"{self._api_url}/invoices/{invoice_id}",
            headers=self._headers(),
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()

    def get_quote(self, amount_usd: float) -> dict:
        """Get a BTC/USD conversion quote for the given amount."""
        payload = {
            "sourceAmount": {
                "amount": f"{amount_usd:.2f}",
                "currency": "USD",
            },
            "targetCurrency": "BTC",
        }
        resp = requests.post(
            f"{self._api_url}/rates/tick",
            json=payload,
            headers=self._headers(),
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()

    def get_balance(self) -> dict:
        """Get Strike account balance."""
        resp = requests.get(
            f"{self._api_url}/balances",
            headers=self._headers(),
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()

    def verify_webhook(self, body: bytes, signature: str) -> bool:
        """Verify Strike webhook HMAC-SHA256 signature."""
        if not self._webhook_secret:
            logger.warning("No webhook secret configured — rejecting webhook")
            return False
        expected = hmac.new(
            self._webhook_secret.encode(),
            body,
            hashlib.sha256,
        ).hexdigest()
        return hmac.compare_digest(expected, signature)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/unit/test_goose_strike_client.py -v`
Expected: 4 PASSED

- [ ] **Step 5: Commit**

```bash
git add canary/services/goose/strike_client.py tests/unit/test_goose_strike_client.py
git commit -m "feat(goose): StrikeClient API wrapper with webhook verification"
```

---

### Task 12: GooseOnboardingService — Wallet Provisioning at OAuth

**Files:**
- Create: `Canary/canary/services/goose/onboarding.py`
- Create: `Canary/tests/integration/test_goose_onboarding.py`

- [ ] **Step 1: Write the failing test**

Create `Canary/tests/integration/test_goose_onboarding.py`:

```python
"""Integration tests — GooseOnboardingService merchant provisioning."""

import pytest

from canary.models.app.merchant_wallet import MerchantWallet
from canary.models.app.macaroon_token import MacaroonToken
from canary.models.app.wallet_transaction import WalletTransaction
from canary.services.goose.onboarding import GooseOnboardingService

pytestmark = pytest.mark.postgres

TEST_ROOT_KEY = "test-macaroon-root-key-32bytes!"


class TestGooseOnboarding:
    """GooseOnboardingService.provision_merchant() — full onboarding."""

    def test_provision_creates_wallet(self, app_session, test_merchant):
        svc = GooseOnboardingService(
            app_session,
            macaroon_root_key=TEST_ROOT_KEY,
            initial_funding_sats=100000,
        )
        result = svc.provision_merchant(test_merchant.id)

        assert result.wallet is not None
        assert result.wallet.balance_sats == 100000
        assert result.wallet.status == "active"
        assert result.wallet.funded_by == "treasury"

    def test_provision_creates_macaroon(self, app_session, test_merchant):
        svc = GooseOnboardingService(
            app_session,
            macaroon_root_key=TEST_ROOT_KEY,
            initial_funding_sats=100000,
        )
        result = svc.provision_merchant(test_merchant.id)

        assert result.macaroon_bytes is not None
        assert result.token_record is not None
        assert result.token_record.status == "active"

    def test_provision_creates_funding_transaction(self, app_session, test_merchant):
        svc = GooseOnboardingService(
            app_session,
            macaroon_root_key=TEST_ROOT_KEY,
            initial_funding_sats=100000,
        )
        result = svc.provision_merchant(test_merchant.id)

        txs = app_session.query(WalletTransaction).filter_by(
            wallet_id=result.wallet.id
        ).all()
        assert len(txs) == 1
        assert txs[0].tx_type == "credit"
        assert txs[0].source == "treasury_fund"
        assert txs[0].amount_sats == 100000

    def test_provision_is_idempotent(self, app_session, test_merchant):
        svc = GooseOnboardingService(
            app_session,
            macaroon_root_key=TEST_ROOT_KEY,
            initial_funding_sats=100000,
        )
        result1 = svc.provision_merchant(test_merchant.id)
        result2 = svc.provision_merchant(test_merchant.id)

        # Second call returns existing wallet, does not create duplicate
        assert result1.wallet.id == result2.wallet.id

        wallets = app_session.query(MerchantWallet).filter_by(
            merchant_id=test_merchant.id
        ).all()
        assert len(wallets) == 1
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_goose_onboarding.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Write GooseOnboardingService**

Create `Canary/canary/services/goose/onboarding.py`:

```python
"""
GooseOnboardingService — merchant wallet provisioning at OAuth.

Called after Square OAuth callback assigns a merchant UUID.
Creates wallet, mints macaroon, funds from treasury.
"""

import logging
import os
from dataclasses import dataclass
from typing import Optional

from canary.models.app.merchant_wallet import MerchantWallet
from canary.models.app.macaroon_token import MacaroonToken
from canary.services.goose.wallet_service import WalletService
from canary.services.goose.macaroon_service import MacaroonService

logger = logging.getLogger(__name__)


@dataclass
class ProvisionResult:
    """Result of merchant provisioning."""
    wallet: MerchantWallet
    macaroon_bytes: Optional[bytes]
    token_record: Optional[MacaroonToken]
    already_existed: bool = False


class GooseOnboardingService:
    """Provisions merchant wallets and macaroons at onboarding."""

    def __init__(
        self,
        session,
        macaroon_root_key: Optional[str] = None,
        initial_funding_sats: Optional[int] = None,
    ):
        self._session = session
        self._root_key = macaroon_root_key or os.getenv("GOOSE_MACAROON_ROOT_KEY", "")
        self._initial_funding = initial_funding_sats or int(
            os.getenv("GOOSE_INITIAL_FUNDING_SATS", "100000")
        )
        self._wallet_svc = WalletService(session)
        self._macaroon_svc = MacaroonService(session, root_key=self._root_key)

    def provision_merchant(self, merchant_id: str, tier: str = "free") -> ProvisionResult:
        """Create wallet, mint macaroon, fund from treasury.

        Idempotent — if wallet exists, returns existing. Does not double-fund.
        """
        # Check for existing wallet
        existing = self._wallet_svc.get_wallet(merchant_id)
        if existing is not None:
            logger.info("Wallet already exists for merchant %s, skipping provision", merchant_id)
            return ProvisionResult(
                wallet=existing,
                macaroon_bytes=None,
                token_record=None,
                already_existed=True,
            )

        # 1. Create wallet
        wallet = MerchantWallet(
            merchant_id=merchant_id,
            balance_sats=0,
            lifetime_funded_sats=0,
            lifetime_spent_sats=0,
            warning_threshold_sats=20000,
            hard_floor_sats=0,
            status="active",
            funded_by="treasury",
        )
        self._session.add(wallet)
        self._session.flush()

        # 2. Mint macaroon
        macaroon_bytes, token_record = self._macaroon_svc.mint(
            merchant_id=merchant_id,
            tier=tier,
            ttl_days=30,
        )

        # 3. Fund from treasury
        self._wallet_svc.credit(
            wallet_id=wallet.id,
            merchant_id=merchant_id,
            amount_sats=self._initial_funding,
            source="treasury_fund",
            note="Initial treasury funding at onboarding",
        )

        logger.info(
            "Provisioned merchant %s: wallet=%s, funded=%d sats",
            merchant_id, wallet.id, self._initial_funding,
        )

        return ProvisionResult(
            wallet=wallet,
            macaroon_bytes=macaroon_bytes,
            token_record=token_record,
        )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_goose_onboarding.py -v`
Expected: 4 PASSED

- [ ] **Step 5: Commit**

```bash
git add canary/services/goose/onboarding.py tests/integration/test_goose_onboarding.py
git commit -m "feat(goose): GooseOnboardingService — provision wallet + macaroon at OAuth"
```

---

### Task 13: TreasuryService — Treasury Funding + Balance Management

**Files:**
- Create: `Canary/canary/services/goose/treasury.py`
- Create: `Canary/tests/integration/test_goose_treasury.py`

- [ ] **Step 1: Write the failing test**

Create `Canary/tests/integration/test_goose_treasury.py`:

```python
"""Integration tests — TreasuryService funding and balance management."""

import pytest

from canary.models.app.merchant_wallet import MerchantWallet
from canary.models.app.wallet_transaction import WalletTransaction
from canary.services.goose.treasury import TreasuryService

pytestmark = pytest.mark.postgres

TEST_ROOT_KEY = "test-macaroon-root-key-32bytes!"


class TestTreasuryFundMerchant:
    """TreasuryService.fund_merchant() — fund wallet from GrowDirect treasury."""

    def test_fund_merchant_credits_wallet(self, app_session, test_merchant):
        wallet = MerchantWallet(
            merchant_id=test_merchant.id,
            balance_sats=0,
            lifetime_funded_sats=0,
            lifetime_spent_sats=0,
            status="active",
            funded_by="treasury",
        )
        app_session.add(wallet)
        app_session.flush()

        svc = TreasuryService(app_session)
        tx = svc.fund_merchant(
            merchant_id=test_merchant.id,
            amount_sats=100000,
        )

        assert tx.amount_sats == 100000
        assert tx.source == "treasury_fund"
        assert wallet.balance_sats == 100000


class TestTreasurySummary:
    """TreasuryService.get_treasury_summary() — outflow report."""

    def test_summary_includes_total_funded(self, app_session, test_merchant):
        wallet = MerchantWallet(
            merchant_id=test_merchant.id,
            balance_sats=0,
            lifetime_funded_sats=0,
            lifetime_spent_sats=0,
            status="active",
            funded_by="treasury",
        )
        app_session.add(wallet)
        app_session.flush()

        svc = TreasuryService(app_session)
        svc.fund_merchant(merchant_id=test_merchant.id, amount_sats=100000)

        summary = svc.get_treasury_summary()
        assert summary["total_funded_sats"] >= 100000
        assert summary["funded_merchant_count"] >= 1
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_goose_treasury.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Write TreasuryService**

Create `Canary/canary/services/goose/treasury.py`:

```python
"""
TreasuryService — GrowDirect treasury funding and balance management.

Manages treasury operations: funding merchant wallets, tracking
outflows, and enforcing the emergency balance floor.
"""

import logging
import os
from typing import Optional

from sqlalchemy import func

from canary.models.app.merchant_wallet import MerchantWallet
from canary.models.app.wallet_transaction import WalletTransaction
from canary.services.goose.wallet_service import WalletService

logger = logging.getLogger(__name__)


class TreasuryService:
    """GrowDirect treasury operations — fund merchants, track outflows."""

    def __init__(self, session):
        self._session = session
        self._wallet_svc = WalletService(session)
        self._emergency_reserve_usd = int(
            os.getenv("GOOSE_EMERGENCY_RESERVE_USD", "500")
        )

    def fund_merchant(
        self,
        merchant_id: str,
        amount_sats: int,
        note: Optional[str] = None,
    ) -> WalletTransaction:
        """Fund a merchant wallet from GrowDirect treasury.

        Returns the credit transaction record.
        """
        wallet = self._wallet_svc.get_wallet(merchant_id)
        if wallet is None:
            raise ValueError(f"No wallet found for merchant {merchant_id}")

        tx = self._wallet_svc.credit(
            wallet_id=wallet.id,
            merchant_id=merchant_id,
            amount_sats=amount_sats,
            source="treasury_fund",
            note=note or f"Treasury funding: {amount_sats} sats",
        )

        logger.info(
            "Treasury funded merchant %s: %d sats (new balance: %d)",
            merchant_id, amount_sats, wallet.balance_sats,
        )
        return tx

    def get_treasury_summary(self) -> dict:
        """Get treasury outflow summary across all merchants."""
        total_funded = self._session.query(
            func.coalesce(func.sum(WalletTransaction.amount_sats), 0)
        ).filter(
            WalletTransaction.tx_type == "credit",
            WalletTransaction.source == "treasury_fund",
        ).scalar()

        funded_count = self._session.query(
            func.count(func.distinct(WalletTransaction.merchant_id))
        ).filter(
            WalletTransaction.tx_type == "credit",
            WalletTransaction.source == "treasury_fund",
        ).scalar()

        total_self_funded = self._session.query(
            func.coalesce(func.sum(WalletTransaction.amount_sats), 0)
        ).filter(
            WalletTransaction.tx_type == "credit",
            WalletTransaction.source == "strike_payment",
        ).scalar()

        return {
            "total_funded_sats": int(total_funded),
            "total_self_funded_sats": int(total_self_funded),
            "funded_merchant_count": int(funded_count),
            "emergency_reserve_usd": self._emergency_reserve_usd,
        }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_goose_treasury.py -v`
Expected: 2 PASSED

- [ ] **Step 5: Commit**

```bash
git add canary/services/goose/treasury.py tests/integration/test_goose_treasury.py
git commit -m "feat(goose): TreasuryService with merchant funding and outflow tracking"
```

---

### Task 14: Goose Blueprint — `/goose` Routes (all 11 routes)

**Files:**
- Create: `Canary/canary/blueprints/goose_api.py`
- Modify: `Canary/wsgi.py` (add to BLUEPRINT_SPECS — requires `critical-file-guardian` skill)

- [ ] **Step 1: Write the blueprint**

Create `Canary/canary/blueprints/goose_api.py`:

```python
"""
Goose API blueprint — account management, wallet, gas schedule.

Routes:
  GET  /goose/wallet                    — Merchant wallet balance + recent txs
  POST /goose/wallet/topup              — Create Strike invoice for refill
  GET  /goose/wallet/topup/<invoice_id> — Check payment status
  POST /goose/webhook/strike            — Handle Strike webhook
  GET  /goose/gas-schedule              — Current gas prices
  GET  /goose/health                    — Service health check
  POST /goose/admin/fund                — Admin: fund merchant wallet
  PUT  /goose/admin/gas-schedule        — Admin: update gas pricing
  GET  /goose/admin/treasury            — Admin: treasury overview
  GET  /goose/admin/wallets             — Admin: all wallets overview
  POST /goose/admin/revoke/<id>         — Admin: revoke macaroon
"""

import logging

from flask import Blueprint, jsonify, request, g
from flask_login import login_required, current_user

from canary.extensions import limiter
from canary.utils.auth import role_required

logger = logging.getLogger(__name__)

goose_bp = Blueprint("goose", __name__)


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

@goose_bp.route("/health", methods=["GET"])
@limiter.exempt
def health():
    """GET /goose/health — service liveness + Strike API reachability."""
    return jsonify({
        "status": "healthy",
        "service": "goose",
        "strike_configured": bool(__import__("os").getenv("STRIKE_API_KEY")),
    }), 200


# ---------------------------------------------------------------------------
# Merchant — Wallet
# ---------------------------------------------------------------------------

@goose_bp.route("/wallet", methods=["GET"])
@login_required
def wallet_balance():
    """GET /goose/wallet — merchant's wallet balance + recent transactions."""
    from canary.db.session_factory import get_session
    from canary.services.goose.wallet_service import WalletService
    from canary.models.app.wallet_transaction import WalletTransaction

    merchant_id = g.get("merchant_id")
    if not merchant_id:
        return jsonify({"error": "Not authenticated"}), 401

    session = get_session()
    svc = WalletService(session)
    wallet = svc.get_wallet(merchant_id)

    if wallet is None:
        return jsonify({"error": "No wallet found"}), 404

    recent_txs = session.query(WalletTransaction).filter_by(
        wallet_id=wallet.id
    ).order_by(WalletTransaction.created_at.desc()).limit(20).all()

    return jsonify({
        "wallet_id": wallet.id,
        "balance_sats": wallet.balance_sats,
        "lifetime_funded_sats": wallet.lifetime_funded_sats,
        "lifetime_spent_sats": wallet.lifetime_spent_sats,
        "status": wallet.status,
        "funded_by": wallet.funded_by,
        "recent_transactions": [
            {
                "id": tx.id,
                "tx_type": tx.tx_type,
                "source": tx.source,
                "operation_type": tx.operation_type,
                "amount_sats": tx.amount_sats,
                "balance_after_sats": tx.balance_after_sats,
                "created_at": tx.created_at.isoformat() if tx.created_at else None,
            }
            for tx in recent_txs
        ],
    }), 200


# ---------------------------------------------------------------------------
# Merchant — Top-up
# ---------------------------------------------------------------------------

@goose_bp.route("/wallet/topup", methods=["POST"])
@login_required
@limiter.limit("10/minute")
def wallet_topup():
    """POST /goose/wallet/topup — create Strike invoice for credit refill."""
    from canary.db.session_factory import get_session
    from canary.services.goose.wallet_service import WalletService
    from canary.services.goose.strike_client import StrikeClient
    from canary.models.app.strike_invoice import StrikeInvoice
    from canary.utils.crypto import encrypt_token

    merchant_id = g.get("merchant_id")
    if not merchant_id:
        return jsonify({"error": "Not authenticated"}), 401

    data = request.get_json(silent=True) or {}
    amount_usd = data.get("amount_usd", 10.00)

    session = get_session()
    svc = WalletService(session)
    wallet = svc.get_wallet(merchant_id)
    if wallet is None:
        return jsonify({"error": "No wallet found"}), 404

    try:
        strike = StrikeClient()
        invoice_data = strike.create_invoice(
            amount_usd=float(amount_usd),
            description=f"Canary credit top-up for {merchant_id}",
        )

        # Calculate sats from quote (simplified — in production use Strike quote API)
        amount_sats = int(float(amount_usd) * 100)  # Placeholder conversion

        invoice = StrikeInvoice(
            merchant_id=merchant_id,
            wallet_id=wallet.id,
            strike_invoice_id=invoice_data["invoiceId"],
            amount_usd=amount_usd,
            amount_sats=amount_sats,
            conversion_rate=0,  # Populated from Strike quote
            bolt11_enc=encrypt_token(invoice_data.get("lnInvoice", "")),
            payment_hash_enc=encrypt_token(invoice_data.get("paymentHash", "")),
            state="pending",
        )
        session.add(invoice)
        session.commit()

        return jsonify({
            "invoice_id": invoice.id,
            "strike_invoice_id": invoice_data["invoiceId"],
            "amount_usd": float(amount_usd),
            "amount_sats": amount_sats,
            "state": "pending",
        }), 201

    except Exception as e:
        logger.error("Failed to create Strike invoice: %s", e)
        session.rollback()
        return jsonify({"error": "Failed to create invoice"}), 500


# ---------------------------------------------------------------------------
# Webhook — Strike
# ---------------------------------------------------------------------------

@goose_bp.route("/webhook/strike", methods=["POST"])
@limiter.limit("100/minute")
def webhook_strike():
    """POST /goose/webhook/strike — handle Strike invoice.updated events."""
    from canary.db.session_factory import get_session
    from canary.services.goose.strike_client import StrikeClient
    from canary.services.goose.wallet_service import WalletService
    from canary.models.app.strike_invoice import StrikeInvoice
    from canary.utils.crypto import encrypt_token
    from datetime import datetime, timezone

    body = request.get_data()
    signature = request.headers.get("X-Strike-Signature", "")

    strike = StrikeClient()
    if not strike.verify_webhook(body, signature):
        logger.warning("Invalid Strike webhook signature")
        return jsonify({"error": "Invalid signature"}), 401

    data = request.get_json(silent=True) or {}
    strike_invoice_id = data.get("invoiceId")
    state = data.get("state", "").upper()

    if not strike_invoice_id:
        return jsonify({"error": "Missing invoiceId"}), 400

    session = get_session()

    # Idempotency check
    invoice = session.query(StrikeInvoice).filter_by(
        strike_invoice_id=strike_invoice_id
    ).first()

    if invoice is None:
        logger.warning("Webhook for unknown invoice: %s", strike_invoice_id)
        return jsonify({"status": "ignored"}), 200

    if invoice.state == "paid":
        # Already processed — idempotent
        return jsonify({"status": "already_processed"}), 200

    if state == "PAID":
        invoice.state = "paid"
        invoice.paid_at = datetime.now(timezone.utc)
        if data.get("preimage"):
            invoice.preimage_enc = encrypt_token(data["preimage"])

        # Credit the wallet
        svc = WalletService(session)
        svc.credit(
            wallet_id=invoice.wallet_id,
            merchant_id=invoice.merchant_id,
            amount_sats=invoice.amount_sats,
            source="strike_payment",
            strike_invoice_id=strike_invoice_id,
            note=f"Strike payment {strike_invoice_id}",
        )
        session.commit()
        logger.info("Invoice %s paid — credited %d sats", strike_invoice_id, invoice.amount_sats)

    return jsonify({"status": "processed"}), 200


# ---------------------------------------------------------------------------
# Public — Gas Schedule
# ---------------------------------------------------------------------------

@goose_bp.route("/wallet/topup/<invoice_id>", methods=["GET"])
@login_required
def wallet_topup_status(invoice_id):
    """GET /goose/wallet/topup/<invoice_id> — check payment status + QR."""
    from canary.db.session_factory import get_session
    from canary.models.app.strike_invoice import StrikeInvoice

    merchant_id = g.get("merchant_id")
    if not merchant_id:
        return jsonify({"error": "Not authenticated"}), 401

    session = get_session()
    invoice = session.query(StrikeInvoice).filter_by(
        id=invoice_id, merchant_id=merchant_id
    ).first()

    if invoice is None:
        return jsonify({"error": "Invoice not found"}), 404

    return jsonify({
        "invoice_id": invoice.id,
        "strike_invoice_id": invoice.strike_invoice_id,
        "amount_usd": float(invoice.amount_usd),
        "amount_sats": invoice.amount_sats,
        "state": invoice.state,
        "paid_at": invoice.paid_at.isoformat() if invoice.paid_at else None,
        "expires_at": invoice.expires_at.isoformat() if invoice.expires_at else None,
    }), 200


@goose_bp.route("/gas-schedule", methods=["GET"])
@login_required
def gas_schedule():
    """GET /goose/gas-schedule — current gas prices (transparency)."""
    from canary.db.session_factory import get_session
    from canary.models.app.gas_schedule import GasSchedule

    session = get_session()
    entries = session.query(GasSchedule).filter_by(
        is_active=True
    ).order_by(GasSchedule.category, GasSchedule.operation_key).all()

    return jsonify({
        "gas_schedule": [
            {
                "operation_key": e.operation_key,
                "category": e.category,
                "description": e.description,
                "cost_sats": e.cost_sats,
            }
            for e in entries
        ],
    }), 200


# ---------------------------------------------------------------------------
# Admin — Fund, Gas Schedule, Treasury, Wallets, Revoke
# ---------------------------------------------------------------------------

@goose_bp.route("/admin/fund", methods=["POST"])
@login_required
@role_required("admin")
def admin_fund():
    """POST /goose/admin/fund — manually fund a merchant wallet from treasury."""
    from canary.db.session_factory import get_session
    from canary.services.goose.wallet_service import WalletService

    data = request.get_json(silent=True) or {}
    merchant_id = data.get("merchant_id")
    amount_sats = data.get("amount_sats", 100000)

    if not merchant_id:
        return jsonify({"error": "merchant_id required"}), 400

    session = get_session()
    svc = WalletService(session)
    wallet = svc.get_wallet(merchant_id)
    if wallet is None:
        return jsonify({"error": "No wallet found for merchant"}), 404

    tx = svc.credit(
        wallet_id=wallet.id,
        merchant_id=merchant_id,
        amount_sats=int(amount_sats),
        source="manual_credit",
        note=f"Admin manual funding: {amount_sats} sats",
    )
    session.commit()

    return jsonify({
        "wallet_id": wallet.id,
        "credited_sats": int(amount_sats),
        "new_balance_sats": wallet.balance_sats,
        "transaction_id": tx.id,
    }), 200


@goose_bp.route("/admin/gas-schedule", methods=["PUT"])
@login_required
@role_required("admin")
def admin_update_gas_schedule():
    """PUT /goose/admin/gas-schedule — update gas schedule pricing."""
    from canary.db.session_factory import get_session
    from canary.models.app.gas_schedule import GasSchedule

    data = request.get_json(silent=True) or {}
    operation_key = data.get("operation_key")
    cost_sats = data.get("cost_sats")

    if not operation_key or cost_sats is None:
        return jsonify({"error": "operation_key and cost_sats required"}), 400

    session = get_session()
    entry = session.query(GasSchedule).filter_by(operation_key=operation_key).first()
    if entry is None:
        return jsonify({"error": f"Unknown operation: {operation_key}"}), 404

    entry.cost_sats = int(cost_sats)
    session.commit()

    return jsonify({
        "operation_key": entry.operation_key,
        "cost_sats": entry.cost_sats,
        "updated": True,
    }), 200


@goose_bp.route("/admin/treasury", methods=["GET"])
@login_required
@role_required("admin")
def admin_treasury():
    """GET /goose/admin/treasury — treasury balance + outflow summary."""
    from canary.db.session_factory import get_session
    from canary.services.goose.treasury import TreasuryService

    session = get_session()
    svc = TreasuryService(session)
    summary = svc.get_treasury_summary()

    return jsonify(summary), 200


@goose_bp.route("/admin/wallets", methods=["GET"])
@login_required
@role_required("admin")
def admin_wallets():
    """GET /goose/admin/wallets — all merchant wallets overview."""
    from canary.db.session_factory import get_session
    from canary.models.app.merchant_wallet import MerchantWallet

    session = get_session()
    wallets = session.query(MerchantWallet).order_by(
        MerchantWallet.status, MerchantWallet.balance_sats
    ).all()

    return jsonify({
        "wallets": [
            {
                "wallet_id": w.id,
                "merchant_id": w.merchant_id,
                "balance_sats": w.balance_sats,
                "lifetime_funded_sats": w.lifetime_funded_sats,
                "lifetime_spent_sats": w.lifetime_spent_sats,
                "status": w.status,
                "funded_by": w.funded_by,
            }
            for w in wallets
        ],
        "count": len(wallets),
    }), 200


@goose_bp.route("/admin/revoke/<macaroon_id>", methods=["POST"])
@login_required
@role_required("admin")
def admin_revoke(macaroon_id):
    """POST /goose/admin/revoke/<macaroon_id> — revoke a macaroon."""
    from canary.db.session_factory import get_session
    from canary.services.goose.macaroon_service import MacaroonService

    session = get_session()
    mac_svc = MacaroonService(session)

    try:
        mac_svc.revoke(macaroon_id)
        session.commit()
        return jsonify({"revoked": True, "macaroon_id": macaroon_id}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 404
```

- [ ] **Step 2: Register blueprint in wsgi.py**

**This requires the `critical-file-guardian` skill** per Canary CLAUDE.md. Add to `BLUEPRINT_SPECS`:

```python
("canary.blueprints.goose_api", "goose_bp", "/goose", "Goose account/credit system", True),
```

`csrf_exempt=True` because the Strike webhook endpoint receives external POST requests.

- [ ] **Step 3: Add Goose config vars to config.py**

Add to `Config` base class in `Canary/canary/config.py`:

```python
# Goose — account management + credit system
STRIKE_API_KEY = os.getenv('STRIKE_API_KEY', '')
STRIKE_API_URL = os.getenv('STRIKE_API_URL', 'https://api.strike.me/v1')
GOOSE_MACAROON_ROOT_KEY = os.getenv('GOOSE_MACAROON_ROOT_KEY', '')
GOOSE_WEBHOOK_SECRET = os.getenv('GOOSE_WEBHOOK_SECRET', '')
GOOSE_INITIAL_FUNDING_SATS = int(os.getenv('GOOSE_INITIAL_FUNDING_SATS', '100000'))
GOOSE_EMERGENCY_RESERVE_USD = int(os.getenv('GOOSE_EMERGENCY_RESERVE_USD', '500'))
```

- [ ] **Step 4: Verify blueprint registers**

```bash
cd ~/GrowDirect/Canary/devops && docker compose restart flask
docker logs canary-flask 2>&1 | grep -i goose
```

Expected: `✓ /goose (Goose account/credit system)`

- [ ] **Step 5: Smoke test health endpoint**

```bash
curl -s https://localhost/goose/health | python3 -m json.tool
```

Expected: `{"status": "healthy", "service": "goose", "strike_configured": false}`

- [ ] **Step 6: Commit**

```bash
git add canary/blueprints/goose_api.py canary/config.py
git commit -m "feat(goose): goose_api blueprint with wallet, topup, webhook, admin routes"
```

---

### Task 15: Add Goose Model Imports to Integration Conftest

**Files:**
- Modify: `Canary/tests/integration/conftest.py`

The integration conftest must import all Goose models so `metadata.create_all()` creates the tables in the test database.

- [ ] **Step 1: Add imports**

Add to the model import block in `Canary/tests/integration/conftest.py`:

```python
# Goose — account management + credit system
from canary.models.app.merchant_wallet import MerchantWallet  # noqa: F401
from canary.models.app.wallet_transaction import WalletTransaction  # noqa: F401
from canary.models.app.gas_schedule import GasSchedule  # noqa: F401
from canary.models.app.macaroon_token import MacaroonToken  # noqa: F401
from canary.models.app.strike_invoice import StrikeInvoice  # noqa: F401
```

- [ ] **Step 2: Run all Goose tests to verify**

```bash
cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_goose_*.py -v
```

Expected: All tests pass.

- [ ] **Step 3: Commit**

```bash
git add tests/integration/conftest.py
git commit -m "feat(goose): add Goose model imports to integration conftest"
```

---

## Chunk 4: L402 Middleware + Integration Smoke Tests

### Task 16: L402 Middleware — `@l402_required` Decorator

**Files:**
- Create: `Canary/canary/services/goose/l402_middleware.py`
- Create: `Canary/tests/unit/test_goose_l402_middleware.py`

- [ ] **Step 1: Write the failing test**

Create `Canary/tests/unit/test_goose_l402_middleware.py`:

```python
"""Unit tests — L402 middleware decorator."""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask


class TestL402Middleware:
    """@l402_required decorator — checks macaroon before endpoint access."""

    def test_returns_402_when_no_token(self):
        from canary.services.goose.l402_middleware import l402_required

        app = Flask(__name__)

        @app.route("/test")
        @l402_required("test.operation")
        def test_route():
            return "OK", 200

        with app.test_client() as client:
            resp = client.get("/test")
            assert resp.status_code == 402

    def test_returns_401_when_invalid_token(self):
        from canary.services.goose.l402_middleware import l402_required

        app = Flask(__name__)

        @app.route("/test")
        @l402_required("test.operation")
        def test_route():
            return "OK", 200

        with app.test_client() as client:
            resp = client.get("/test", headers={
                "Cookie": "l402_token=invalid-macaroon-data"
            })
            # Invalid token should return 401 or 402
            assert resp.status_code in (401, 402)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/unit/test_goose_l402_middleware.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Write L402 middleware**

Create `Canary/canary/services/goose/l402_middleware.py`:

```python
"""
L402 middleware — @l402_required decorator for gated endpoints.

Checks for a valid macaroon token (cookie or Authorization header)
before allowing access to gated endpoints. Returns 402 Payment
Required with a Strike invoice when token is missing or invalid.
"""

import logging
from functools import wraps

from flask import request, jsonify, g, make_response

logger = logging.getLogger(__name__)


def l402_required(operation_key: str):
    """Decorator that gates an endpoint with L402 macaroon verification.

    Args:
        operation_key: The gas_schedule operation key for this endpoint.
                      Used for balance checking and gas metering.

    Usage:
        @l402_required("owl.query.deep")
        def owl_deep_analysis():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from canary.services.goose.macaroon_service import MacaroonService
            from canary.services.goose.gas_meter import GasMeter
            from canary.db.session_factory import get_session

            # 1. Check for token
            token = _extract_token(request)
            if token is None:
                return _payment_required("No L402 token provided")

            # 2. Verify macaroon
            session = get_session()
            mac_svc = MacaroonService(session)
            result = mac_svc.verify(token)

            if not result.valid:
                return _payment_required(f"Invalid token: {result.error}")

            # 3. Check gas balance
            meter = GasMeter(session)
            charge_result = meter.charge(
                merchant_id=result.merchant_id,
                operation_key=operation_key,
            )

            if charge_result.insufficient:
                return _payment_required(
                    "Insufficient credits",
                    cost_sats=charge_result.cost_sats,
                )

            # 4. Set merchant context
            g.l402_merchant_id = result.merchant_id
            g.l402_tier = result.tier

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def _extract_token(req) -> bytes | None:
    """Extract macaroon from cookie or Authorization header."""
    # Check cookie first
    cookie_token = req.cookies.get("l402_token")
    if cookie_token:
        return cookie_token.encode("utf-8") if isinstance(cookie_token, str) else cookie_token

    # Check Authorization header
    auth_header = req.headers.get("Authorization", "")
    if auth_header.startswith("L402 "):
        parts = auth_header[5:].split(":", 1)
        if parts:
            return parts[0].encode("utf-8") if isinstance(parts[0], str) else parts[0]

    return None


def _payment_required(reason: str, cost_sats: int = 0):
    """Return 402 Payment Required response."""
    response = make_response(jsonify({
        "error": "Payment Required",
        "reason": reason,
        "cost_sats": cost_sats,
        "topup_url": "/goose/wallet/topup",
    }), 402)
    return response
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/unit/test_goose_l402_middleware.py -v`
Expected: 2 PASSED

- [ ] **Step 5: Commit**

```bash
git add canary/services/goose/l402_middleware.py tests/unit/test_goose_l402_middleware.py
git commit -m "feat(goose): @l402_required middleware for gated endpoints"
```

---

### Task 17: End-to-End Smoke Test

**Files:**
- Create: `Canary/tests/integration/test_goose_e2e.py`

- [ ] **Step 1: Write the full lifecycle test**

```python
"""Integration test — full Goose lifecycle.

Onboarding → credit → gas charge → debit → balance check.
Proves the entire credit system works end-to-end.
"""

import pytest

from canary.models.app.merchant_wallet import MerchantWallet
from canary.models.app.wallet_transaction import WalletTransaction
from canary.models.app.gas_schedule import GasSchedule
from canary.services.goose.onboarding import GooseOnboardingService
from canary.services.goose.gas_meter import GasMeter
from canary.services.goose.wallet_service import WalletService
from canary.services.goose.seed import seed_gas_schedule

pytestmark = pytest.mark.postgres

TEST_ROOT_KEY = "test-macaroon-root-key-32bytes!"


class TestGooseE2E:
    """Full lifecycle: onboard → use → deplete → gate."""

    def test_full_credit_lifecycle(self, app_session, test_merchant):
        # 1. Seed gas schedule
        seed_gas_schedule(app_session)

        # 2. Onboard merchant (creates wallet, mints macaroon, funds 100k sats)
        onboard = GooseOnboardingService(
            app_session,
            macaroon_root_key=TEST_ROOT_KEY,
            initial_funding_sats=100000,
        )
        result = onboard.provision_merchant(test_merchant.id)
        wallet = result.wallet

        assert wallet.balance_sats == 100000
        assert wallet.status == "active"

        # 3. Process some transactions (1 sat each)
        meter = GasMeter(app_session)
        for _ in range(100):
            charge = meter.charge(
                merchant_id=test_merchant.id,
                operation_key="tsp.transaction.ingested",
            )
            assert charge.charged is True

        assert wallet.balance_sats == 99900

        # 4. Fire a gold list alert (FREE)
        charge = meter.charge(
            merchant_id=test_merchant.id,
            operation_key="chirp.gold_list.fired",
        )
        assert charge.charged is False  # Free, no debit
        assert wallet.balance_sats == 99900  # Unchanged

        # 5. Open a Fox case (100 sats)
        charge = meter.charge(
            merchant_id=test_merchant.id,
            operation_key="fox.case.created",
        )
        assert charge.charged is True
        assert wallet.balance_sats == 99800

        # 6. Verify transaction count in ledger
        txs = app_session.query(WalletTransaction).filter_by(
            wallet_id=wallet.id,
            tx_type="debit",
        ).all()
        assert len(txs) == 101  # 100 TSP + 1 Fox

        # 7. Verify funding transaction
        fund_tx = app_session.query(WalletTransaction).filter_by(
            wallet_id=wallet.id,
            tx_type="credit",
            source="treasury_fund",
        ).first()
        assert fund_tx is not None
        assert fund_tx.amount_sats == 100000

    def test_wallet_depletes_and_gates(self, app_session, test_merchant):
        seed_gas_schedule(app_session)

        onboard = GooseOnboardingService(
            app_session,
            macaroon_root_key=TEST_ROOT_KEY,
            initial_funding_sats=50,  # Very small funding
        )
        result = onboard.provision_merchant(test_merchant.id)
        wallet = result.wallet

        meter = GasMeter(app_session)

        # Burn through credits
        for _ in range(50):
            meter.charge(
                merchant_id=test_merchant.id,
                operation_key="tsp.transaction.ingested",
            )

        assert wallet.balance_sats == 0
        assert wallet.status == "depleted"

        # Premium operation should be gated
        charge = meter.charge(
            merchant_id=test_merchant.id,
            operation_key="fox.case.created",
        )
        assert charge.charged is False
        assert charge.insufficient is True

        # Gold list alerts still work (cost = 0)
        charge = meter.charge(
            merchant_id=test_merchant.id,
            operation_key="chirp.gold_list.fired",
        )
        assert charge.charged is False  # Free
        assert charge.insufficient is False
```

- [ ] **Step 2: Run the E2E test**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_goose_e2e.py -v`
Expected: 2 PASSED

- [ ] **Step 3: Commit**

```bash
git add tests/integration/test_goose_e2e.py
git commit -m "test(goose): end-to-end lifecycle test — onboard → charge → deplete → gate"
```

---

## Task Summary

| # | Component | Files | Tests |
|---|-----------|-------|-------|
| 1 | MerchantWallet model | 1 new, 1 modify | 3 tests |
| 2 | WalletTransaction model | 1 new, 1 modify | 3 tests |
| 3 | GasSchedule model | 1 new, 1 modify | 3 tests |
| 4 | MacaroonToken model | 1 new, 1 modify | 2 tests |
| 5 | StrikeInvoice model | 1 new, 1 modify | 2 tests |
| 6 | Alembic migration | 1 new | Verify via psql |
| 7 | Gas schedule seed | 2 new | 2 tests |
| 8 | WalletService | 1 new | 5 tests |
| 9 | GasMeter | 1 new | 7 tests |
| 10 | MacaroonService | 1 new | 6 tests |
| 11 | StrikeClient | 1 new | 4 tests |
| 12 | GooseOnboardingService | 1 new | 4 tests |
| 13 | TreasuryService | 1 new | 2 tests |
| 14 | Goose blueprint + config (all 11 routes) | 2 new, 2 modify | Smoke test |
| 15 | Integration conftest | 1 modify | Verify all pass |
| 16 | L402 middleware | 1 new | 2 tests |
| 17 | E2E smoke test | 1 new | 2 tests |

**Total:** ~22 new files, ~4 modified files, ~47 tests.
