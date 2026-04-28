# GRO-626 + GRO-627: ARTS POSLOG Alignment & TransactionFact Scoring Substrate

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Align the Python sales schema to ARTS POSLOG fields (multi-POS coexistence) and add the TransactionFact pre-computed scoring table for Chirp detection.

**Architecture:** GRO-626 adds nullable ARTS columns to existing sales tables + a new `transaction_taxes` table. GRO-627 adds a `transaction_facts` table and a fact builder service triggered at T.CLOSE. Both are additive — no existing columns change, no data migration, UUID PKs preserved.

**Tech Stack:** Python 3.12, SQLAlchemy 2.0 (Mapped[] syntax), Alembic, PostgreSQL 17, pytest

**Linear:** GRO-626 (Urgent) → GRO-627 (High) → unblocks GRO-618

---

## File Map

### GRO-626 — ARTS POSLOG Alignment

| Action | File | Responsibility |
|--------|------|----------------|
| Modify | `Canary/canary/models/sales/transactions.py` | Add 8 ARTS columns to Transaction + composite index |
| Modify | `Canary/canary/models/sales/line_items.py` | Add 7 ARTS columns to TransactionLineItem |
| Modify | `Canary/canary/models/sales/tenders.py` | Add `canonical_tender_type` column |
| Create | `Canary/canary/models/sales/transaction_taxes.py` | New TransactionTax model (per-jurisdiction) |
| Modify | `Canary/canary/models/sales/__init__.py` | Export TransactionTax |
| Modify | `Canary/canary/services/parsers/square_payment_parser.py` | Populate new ARTS fields on parse |
| Create | `Canary/canary/migrations/versions/gro626_arts_poslog_alignment.py` | Alembic migration |
| Create | `Canary/tests/unit/test_arts_alignment.py` | Unit tests for ARTS field parsing |
| Create | `Canary/tests/integration/test_arts_schema.py` | Integration tests for new columns + table |
| Modify | `Canary/tests/integration/conftest.py` | Import TransactionTax for create_all() |

### GRO-627 — TransactionFact Scoring Substrate

| Action | File | Responsibility |
|--------|------|----------------|
| Create | `Canary/canary/models/sales/transaction_facts.py` | TransactionFact model |
| Modify | `Canary/canary/models/sales/__init__.py` | Export TransactionFact |
| Create | `Canary/canary/services/fact_builder.py` | FactBuilderService |
| Create | `Canary/canary/migrations/versions/gro627_transaction_fact_table.py` | Alembic migration |
| Create | `Canary/tests/unit/test_fact_builder.py` | Unit tests for fact computation |
| Create | `Canary/tests/integration/test_transaction_facts.py` | Integration tests for persistence |
| Modify | `Canary/tests/integration/conftest.py` | Import TransactionFact for create_all() |

---

## Chunk 1: GRO-626 Models

### Task 1: Add ARTS columns to Transaction model

**Files:**
- Modify: `Canary/canary/models/sales/transactions.py:1-231`
- Test: `Canary/tests/integration/test_arts_schema.py`

- [ ] **Step 1: Write the failing integration test for new Transaction ARTS columns**

Create `Canary/tests/integration/test_arts_schema.py`:

```python
"""Integration tests for GRO-626 ARTS POSLOG schema alignment."""
import pytest
from datetime import datetime, date, timezone
from canary.models.base import SalesBase, generate_uuid
from canary.models.sales.transactions import Transaction

pytestmark = [pytest.mark.postgres, pytest.mark.integration]


class TestTransactionARTSColumns:
    """Verify ARTS columns exist and accept values."""

    def test_transaction_arts_fields_nullable(self, sales_session):
        """Existing transactions without ARTS fields should work (all nullable)."""
        txn = Transaction(
            id=generate_uuid(),
            merchant_id=generate_uuid(),
            external_id="sq_pay_001",
            source_type="WEBHOOK",
            location_id=generate_uuid(),
            transaction_type="SALE",
            transaction_date=datetime.now(timezone.utc),
            amount_cents=1500,
            currency="USD",
        )
        sales_session.add(txn)
        sales_session.flush()

        result = sales_session.get(Transaction, txn.id)
        assert result.source_system is None
        assert result.business_day_date is None
        assert result.workstation_id is None
        assert result.sequence_number is None
        assert result.begin_datetime is None
        assert result.end_datetime is None
        assert result.operator_id is None
        assert result.transaction_status is None

    def test_transaction_arts_fields_populated(self, sales_session):
        """Transaction with all ARTS fields populated."""
        now = datetime.now(timezone.utc)
        txn = Transaction(
            id=generate_uuid(),
            merchant_id=generate_uuid(),
            external_id="ncr_tkt_001",
            source_type="POLLING",
            location_id=generate_uuid(),
            transaction_type="SALE",
            transaction_date=now,
            amount_cents=2500,
            currency="USD",
            source_system="NCR_COUNTERPOINT",
            business_day_date=date(2026, 4, 27),
            workstation_id="REG-01",
            sequence_number=42,
            begin_datetime=now,
            end_datetime=now,
            operator_id="EMP-005",
            transaction_status="COMPLETE",
        )
        sales_session.add(txn)
        sales_session.flush()

        result = sales_session.get(Transaction, txn.id)
        assert result.source_system == "NCR_COUNTERPOINT"
        assert result.business_day_date == date(2026, 4, 27)
        assert result.workstation_id == "REG-01"
        assert result.sequence_number == 42
        assert result.operator_id == "EMP-005"
        assert result.transaction_status == "COMPLETE"
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_arts_schema.py -v -x 2>&1 | head -30
```

Expected: FAIL — `source_system` attribute does not exist on Transaction.

- [ ] **Step 3: Add ARTS columns to Transaction model**

Edit `Canary/canary/models/sales/transactions.py`. Add these columns after `cancel_context` (around line 56) and before `transaction_date`:

```python
    # --- ARTS POSLOG canonical identity (GRO-626) ---
    source_system: Mapped[Optional[str]] = mapped_column(
        String(32), nullable=True,
        doc="ARTS source system: SQUARE|NCR_COUNTERPOINT|CLOVER|SHOPIFY_POS|LIGHTSPEED"
    )
    business_day_date: Mapped[Optional[date]] = mapped_column(
        nullable=True, index=True,
        doc="ARTS BusinessDayDate — fiscal date, may differ from transaction_date for 24h stores"
    )
    workstation_id: Mapped[Optional[str]] = mapped_column(
        nullable=True, index=True,
        doc="ARTS WorkstationID — register/terminal canonical ID"
    )
    sequence_number: Mapped[Optional[int]] = mapped_column(
        nullable=True,
        doc="ARTS SequenceNumber — per-workstation, per-business-day counter"
    )
    begin_datetime: Mapped[Optional[datetime]] = mapped_column(
        nullable=True,
        doc="ARTS BeginDateTime — when cashier started the transaction"
    )
    end_datetime: Mapped[Optional[datetime]] = mapped_column(
        nullable=True,
        doc="ARTS EndDateTime — when transaction completed (CLOSE timestamp)"
    )
    operator_id: Mapped[Optional[str]] = mapped_column(
        nullable=True, index=True,
        doc="ARTS OperatorID — employee who opened the transaction (may differ from employee_id)"
    )
    transaction_status: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True,
        doc="ARTS TransactionStatus: COMPLETE|VOIDED|SUSPENDED|POST_VOIDED"
    )
```

Also add `date` to the datetime import: `from datetime import date, datetime`

Add the ARTS composite index to `__table_args__`:

```python
    Index(
        "ix_transactions_arts_key",
        "merchant_id", "source_system", "workstation_id",
        "business_day_date", "sequence_number",
    ),
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_arts_schema.py::TestTransactionARTSColumns -v -x
```

Expected: PASS (both tests green).

- [ ] **Step 5: Commit**

```bash
cd ~/GrowDirect/Canary && git add canary/models/sales/transactions.py tests/integration/test_arts_schema.py
git commit -m "feat(sales): add ARTS POSLOG columns to Transaction model (GRO-626 CS1)"
```

---

### Task 2: Add ARTS columns to TransactionLineItem model

**Files:**
- Modify: `Canary/canary/models/sales/line_items.py:1-90`
- Test: `Canary/tests/integration/test_arts_schema.py` (append)

- [ ] **Step 1: Write the failing test for line item ARTS columns**

Append to `Canary/tests/integration/test_arts_schema.py`:

```python
from canary.models.sales.line_items import TransactionLineItem
from decimal import Decimal


class TestLineItemARTSColumns:
    """Verify ARTS columns on TransactionLineItem."""

    def _make_transaction(self, sales_session):
        txn = Transaction(
            id=generate_uuid(),
            merchant_id=generate_uuid(),
            external_id=generate_uuid(),
            source_type="WEBHOOK",
            location_id=generate_uuid(),
            transaction_type="SALE",
            transaction_date=datetime.now(timezone.utc),
            amount_cents=1000,
            currency="USD",
        )
        sales_session.add(txn)
        sales_session.flush()
        return txn

    def test_line_item_arts_fields_nullable(self, sales_session):
        """Existing line items without ARTS fields should work."""
        txn = self._make_transaction(sales_session)
        li = TransactionLineItem(
            id=generate_uuid(),
            merchant_id=txn.merchant_id,
            transaction_id=txn.id,
            quantity=Decimal("1.0"),
            base_price_cents=500,
            gross_sales_cents=500,
            item_type="ITEM",
        )
        sales_session.add(li)
        sales_session.flush()

        result = sales_session.get(TransactionLineItem, li.id)
        assert result.line_sequence_number is None
        assert result.article_id is None
        assert result.uom is None
        assert result.line_type is None
        assert result.regular_unit_price_cents is None
        assert result.actual_unit_price_cents is None
        assert result.price_override_reason is None

    def test_line_item_arts_fields_populated(self, sales_session):
        """Line item with ARTS fields populated (NCR source)."""
        txn = self._make_transaction(sales_session)
        li = TransactionLineItem(
            id=generate_uuid(),
            merchant_id=txn.merchant_id,
            transaction_id=txn.id,
            quantity=Decimal("2.5"),
            base_price_cents=399,
            gross_sales_cents=998,
            item_type="ITEM",
            line_sequence_number=1,
            article_id="00012345678905",
            uom="LB",
            line_type="SALE",
            regular_unit_price_cents=499,
            actual_unit_price_cents=399,
            price_override_reason="MANAGER_MARKDOWN",
        )
        sales_session.add(li)
        sales_session.flush()

        result = sales_session.get(TransactionLineItem, li.id)
        assert result.line_sequence_number == 1
        assert result.article_id == "00012345678905"
        assert result.uom == "LB"
        assert result.line_type == "SALE"
        assert result.regular_unit_price_cents == 499
        assert result.actual_unit_price_cents == 399
        assert result.price_override_reason == "MANAGER_MARKDOWN"
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_arts_schema.py::TestLineItemARTSColumns -v -x 2>&1 | head -20
```

Expected: FAIL — `line_sequence_number` attribute does not exist.

- [ ] **Step 3: Add ARTS columns to TransactionLineItem model**

Edit `Canary/canary/models/sales/line_items.py`. Add after `return_reason` (around line 78), before `created_at`:

```python
    # --- ARTS POSLOG fields (GRO-626 CS2) ---
    line_sequence_number: Mapped[Optional[int]] = mapped_column(
        nullable=True,
        doc="ARTS RetailTransactionLineItem SequenceNumber"
    )
    article_id: Mapped[Optional[str]] = mapped_column(
        nullable=True, index=True,
        doc="ARTS canonical article identifier — UPC/GTIN/EAN (source-agnostic)"
    )
    uom: Mapped[Optional[str]] = mapped_column(
        String(16), nullable=True,
        doc="ARTS UnitOfMeasureCode — EACH|OZ|LB|KG|FT|M|PALLET"
    )
    line_type: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True,
        doc="ARTS line type: SALE|RETURN|VOID_LINE|EXCHANGE"
    )
    regular_unit_price_cents: Mapped[Optional[int]] = mapped_column(
        nullable=True,
        doc="ARTS RegularSalesUnitPrice — shelf price before override"
    )
    actual_unit_price_cents: Mapped[Optional[int]] = mapped_column(
        nullable=True,
        doc="ARTS ActualSalesUnitPrice — what was actually charged per unit"
    )
    price_override_reason: Mapped[Optional[str]] = mapped_column(
        nullable=True,
        doc="ARTS RetailPriceModifierReasonCode — LP signal for price overrides"
    )
```

Also add `String` to the sqlalchemy import if not already present.

- [ ] **Step 4: Run test to verify it passes**

```bash
cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_arts_schema.py::TestLineItemARTSColumns -v -x
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
cd ~/GrowDirect/Canary && git add canary/models/sales/line_items.py tests/integration/test_arts_schema.py
git commit -m "feat(sales): add ARTS POSLOG columns to TransactionLineItem (GRO-626 CS2)"
```

---

### Task 3: Add canonical_tender_type to TransactionTender

**Files:**
- Modify: `Canary/canary/models/sales/tenders.py:1-72`
- Test: `Canary/tests/integration/test_arts_schema.py` (append)

- [ ] **Step 1: Write the failing test**

Append to `Canary/tests/integration/test_arts_schema.py`:

```python
from canary.models.sales.tenders import TransactionTender


class TestTenderARTSColumns:
    """Verify canonical_tender_type on TransactionTender."""

    def _make_transaction(self, sales_session):
        txn = Transaction(
            id=generate_uuid(),
            merchant_id=generate_uuid(),
            external_id=generate_uuid(),
            source_type="WEBHOOK",
            location_id=generate_uuid(),
            transaction_type="SALE",
            transaction_date=datetime.now(timezone.utc),
            amount_cents=1000,
            currency="USD",
        )
        sales_session.add(txn)
        sales_session.flush()
        return txn

    def test_tender_canonical_type_nullable(self, sales_session):
        """Existing tenders without canonical type should work."""
        txn = self._make_transaction(sales_session)
        tender = TransactionTender(
            id=generate_uuid(),
            merchant_id=txn.merchant_id,
            transaction_id=txn.id,
            tender_type="CARD",
            amount_cents=1000,
        )
        sales_session.add(tender)
        sales_session.flush()
        result = sales_session.get(TransactionTender, tender.id)
        assert result.canonical_tender_type is None

    def test_tender_canonical_type_populated(self, sales_session):
        """Tender with ARTS canonical type."""
        txn = self._make_transaction(sales_session)
        tender = TransactionTender(
            id=generate_uuid(),
            merchant_id=txn.merchant_id,
            transaction_id=txn.id,
            tender_type="SQUARE_GIFT_CARD",
            amount_cents=500,
            canonical_tender_type="STORE_CREDIT",
        )
        sales_session.add(tender)
        sales_session.flush()
        result = sales_session.get(TransactionTender, tender.id)
        assert result.canonical_tender_type == "STORE_CREDIT"
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_arts_schema.py::TestTenderARTSColumns -v -x 2>&1 | head -20
```

Expected: FAIL — `canonical_tender_type` does not exist.

- [ ] **Step 3: Add canonical_tender_type to TransactionTender**

Edit `Canary/canary/models/sales/tenders.py`. Add after `team_member_id` (around line 58), before `created_at`:

```python
    # --- ARTS POSLOG (GRO-626 CS3) ---
    canonical_tender_type: Mapped[Optional[str]] = mapped_column(
        String(32), nullable=True,
        doc="ARTS canonical tender type — normalized from source-specific tender_type by EJ Spine parser"
    )
```

Add `String` to the sqlalchemy import if not already present.

- [ ] **Step 4: Run test to verify it passes**

```bash
cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_arts_schema.py::TestTenderARTSColumns -v -x
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
cd ~/GrowDirect/Canary && git add canary/models/sales/tenders.py tests/integration/test_arts_schema.py
git commit -m "feat(sales): add canonical_tender_type to TransactionTender (GRO-626 CS3)"
```

---

### Task 4: Create TransactionTax model

**Files:**
- Create: `Canary/canary/models/sales/transaction_taxes.py`
- Modify: `Canary/canary/models/sales/__init__.py`
- Test: `Canary/tests/integration/test_arts_schema.py` (append)

- [ ] **Step 1: Write the failing test for TransactionTax**

Append to `Canary/tests/integration/test_arts_schema.py`:

```python
from canary.models.sales.transaction_taxes import TransactionTax


class TestTransactionTax:
    """Verify TransactionTax table creation and FK relationships."""

    def _make_transaction_with_line(self, sales_session):
        txn = Transaction(
            id=generate_uuid(),
            merchant_id=generate_uuid(),
            external_id=generate_uuid(),
            source_type="WEBHOOK",
            location_id=generate_uuid(),
            transaction_type="SALE",
            transaction_date=datetime.now(timezone.utc),
            amount_cents=2000,
            currency="USD",
        )
        sales_session.add(txn)
        sales_session.flush()
        li = TransactionLineItem(
            id=generate_uuid(),
            merchant_id=txn.merchant_id,
            transaction_id=txn.id,
            quantity=Decimal("1.0"),
            base_price_cents=2000,
            gross_sales_cents=2000,
            item_type="ITEM",
        )
        sales_session.add(li)
        sales_session.flush()
        return txn, li

    def test_transaction_level_tax(self, sales_session):
        """Tax at transaction level (line_item_id is null)."""
        txn, _ = self._make_transaction_with_line(sales_session)
        tax = TransactionTax(
            id=generate_uuid(),
            merchant_id=txn.merchant_id,
            transaction_id=txn.id,
            line_item_id=None,
            jurisdiction_code="06-037",
            jurisdiction_level="COUNTY",
            tax_category="GENERAL",
            taxable_amount_cents=2000,
            tax_rate=Decimal("0.082500"),
            tax_amount_cents=165,
            is_exempt=False,
            source_system="SQUARE",
        )
        sales_session.add(tax)
        sales_session.flush()

        result = sales_session.get(TransactionTax, tax.id)
        assert result.jurisdiction_code == "06-037"
        assert result.jurisdiction_level == "COUNTY"
        assert result.taxable_amount_cents == 2000
        assert result.tax_amount_cents == 165
        assert result.is_exempt is False
        assert result.line_item_id is None

    def test_line_level_tax(self, sales_session):
        """Tax at line item level with FK."""
        txn, li = self._make_transaction_with_line(sales_session)
        tax = TransactionTax(
            id=generate_uuid(),
            merchant_id=txn.merchant_id,
            transaction_id=txn.id,
            line_item_id=li.id,
            jurisdiction_code="06-037-001",
            jurisdiction_level="CITY",
            tax_category="GENERAL",
            taxable_amount_cents=2000,
            tax_rate=Decimal("0.009500"),
            tax_amount_cents=19,
            is_exempt=False,
            source_system="NCR_COUNTERPOINT",
        )
        sales_session.add(tax)
        sales_session.flush()

        result = sales_session.get(TransactionTax, tax.id)
        assert result.line_item_id == li.id
        assert result.source_system == "NCR_COUNTERPOINT"

    def test_exempt_tax_record(self, sales_session):
        """EBT/SNAP exempt tax record."""
        txn, li = self._make_transaction_with_line(sales_session)
        tax = TransactionTax(
            id=generate_uuid(),
            merchant_id=txn.merchant_id,
            transaction_id=txn.id,
            line_item_id=li.id,
            jurisdiction_level="STATE",
            tax_category="FOOD_GROCERY",
            taxable_amount_cents=0,
            tax_rate=Decimal("0.000000"),
            tax_amount_cents=0,
            is_exempt=True,
        )
        sales_session.add(tax)
        sales_session.flush()

        result = sales_session.get(TransactionTax, tax.id)
        assert result.is_exempt is True
        assert result.tax_amount_cents == 0
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_arts_schema.py::TestTransactionTax -v -x 2>&1 | head -20
```

Expected: FAIL — `transaction_taxes` module does not exist.

- [ ] **Step 3: Create TransactionTax model**

Create `Canary/canary/models/sales/transaction_taxes.py`:

```python
"""
Per-jurisdiction tax breakdown — APPEND-ONLY.

ARTS POSLOG carries tax at line level with jurisdiction attribution.
The existing LineItemTax table stores Square-aggregated tax; this table
stores the ARTS-canonical per-jurisdiction breakdown for multi-POS and
multi-jurisdiction support.

GRO-626 Change Set 4.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import ForeignKey, Index, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from canary.models.base import SalesBase, generate_uuid


class TransactionTax(SalesBase):
    __tablename__ = "transaction_taxes"

    id: Mapped[str] = mapped_column(primary_key=True, default=generate_uuid)
    merchant_id: Mapped[str] = mapped_column(nullable=False, index=True)
    transaction_id: Mapped[str] = mapped_column(
        ForeignKey("transactions.id", name="fk_tx_tax_transaction"),
        nullable=False,
    )
    line_item_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey("transaction_line_items.id", name="fk_tx_tax_line"),
        nullable=True,
        doc="FK to line item — null if tax applies at transaction level",
    )
    jurisdiction_code: Mapped[Optional[str]] = mapped_column(
        nullable=True,
        doc="Tax jurisdiction code (FIPS or ISO subdivision)",
    )
    jurisdiction_level: Mapped[Optional[str]] = mapped_column(
        String(20), nullable=True,
        doc="FEDERAL|STATE|COUNTY|CITY|SPECIAL_DISTRICT",
    )
    tax_category: Mapped[Optional[str]] = mapped_column(
        String(32), nullable=True,
        doc="ARTS TaxGroupRuleID equivalent — GENERAL|FOOD_GROCERY|CLOTHING|etc.",
    )
    taxable_amount_cents: Mapped[int] = mapped_column(
        nullable=False, doc="Amount subject to this tax",
    )
    tax_rate: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(8, 6), nullable=True, doc="Applied rate e.g. 0.082500",
    )
    tax_amount_cents: Mapped[int] = mapped_column(
        nullable=False, doc="Tax amount collected",
    )
    is_exempt: Mapped[bool] = mapped_column(
        default=False,
        doc="True if item was exempt (EBT/SNAP, tax holiday, etc.)",
    )
    source_system: Mapped[Optional[str]] = mapped_column(
        String(32), nullable=True,
        doc="Source POS system that provided this tax data",
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default="now()", nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default="now()", nullable=False,
    )

    __table_args__ = (
        Index("ix_tx_tax_merchant_transaction", "merchant_id", "transaction_id"),
        Index("ix_tx_tax_merchant_jurisdiction", "merchant_id", "jurisdiction_level"),
    )
```

- [ ] **Step 4: Export TransactionTax from __init__.py**

Edit `Canary/canary/models/sales/__init__.py`. Add import and export:

```python
from canary.models.sales.transaction_taxes import TransactionTax
```

Add `TransactionTax` to the exports (after the existing `LineItemTax` import line).

- [ ] **Step 4b: Add TransactionTax import to integration conftest**

Edit `Canary/tests/integration/conftest.py`. Add after the existing `LineItemTax` import (around line 75):

```python
from canary.models.sales.transaction_taxes import TransactionTax  # noqa: F401
```

Without this, `SalesBase.metadata.create_all()` won't know about the new table and integration tests will fail with "relation does not exist."

- [ ] **Step 5: Run test to verify it passes**

```bash
cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_arts_schema.py::TestTransactionTax -v -x
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
cd ~/GrowDirect/Canary && git add canary/models/sales/transaction_taxes.py canary/models/sales/__init__.py tests/integration/test_arts_schema.py
git commit -m "feat(sales): add TransactionTax per-jurisdiction model (GRO-626 CS4)"
```

---

## Chunk 2: GRO-626 Parser & Migration

### Task 5: Update Square payment parser to populate ARTS fields

**Files:**
- Modify: `Canary/canary/services/parsers/square_payment_parser.py`
- Test: `Canary/tests/unit/test_arts_alignment.py`

- [ ] **Step 1: Write the failing unit test**

Create `Canary/tests/unit/test_arts_alignment.py`:

```python
"""Unit tests for ARTS field population in Square parser (GRO-626 CS5)."""
import pytest
from canary.services.parsers.square_payment_parser import parse_payment

pytestmark = [pytest.mark.unit, pytest.mark.square]

SQUARE_PAYMENT_PAYLOAD = {
    "data": {
        "type": "payment",
        "id": "evt_123",
        "object": {
            "payment": {
                "id": "pay_abc123",
                "order_id": "ord_xyz",
                "location_id": "loc_001",
                "amount_money": {"amount": 1500, "currency": "USD"},
                "total_money": {"amount": 1500, "currency": "USD"},
                "status": "COMPLETED",
                "source_type": "CARD",
                "card_details": {
                    "card": {
                        "card_brand": "VISA",
                        "last_4": "1234",
                        "fingerprint": "fp_abc",
                    },
                    "entry_method": "CHIP",
                    "status": "CAPTURED",
                    "cvv_status": "CVV_ACCEPTED",
                    "avs_status": "AVS_ACCEPTED",
                },
                "created_at": "2026-04-27T10:30:00Z",
                "updated_at": "2026-04-27T10:30:05Z",
                "employee_id": "emp_001",
                "device_id": "dev_001",
                "receipt_number": "R001",
                "capabilities": ["AUTOCOMPLETE"],
            }
        },
    }
}


class TestSquareARTSFields:
    """Verify Square parser populates ARTS fields."""

    def test_source_system_is_square(self):
        result = parse_payment(SQUARE_PAYMENT_PAYLOAD)
        assert result["source_system"] == "SQUARE"

    def test_business_day_date_derived(self):
        result = parse_payment(SQUARE_PAYMENT_PAYLOAD)
        assert result["business_day_date"] is not None
        # Should be the date portion of created_at
        assert str(result["business_day_date"]) == "2026-04-27"

    def test_workstation_id_from_device(self):
        result = parse_payment(SQUARE_PAYMENT_PAYLOAD)
        assert result["workstation_id"] == "dev_001"

    def test_operator_id_from_employee(self):
        result = parse_payment(SQUARE_PAYMENT_PAYLOAD)
        assert result["operator_id"] == "emp_001"

    def test_transaction_status_complete(self):
        result = parse_payment(SQUARE_PAYMENT_PAYLOAD)
        assert result["transaction_status"] == "COMPLETE"

    def test_transaction_status_voided(self):
        payload = {
            "data": {
                "type": "payment",
                "id": "evt_456",
                "object": {
                    "payment": {
                        "id": "pay_void",
                        "location_id": "loc_001",
                        "amount_money": {"amount": 500, "currency": "USD"},
                        "total_money": {"amount": 500, "currency": "USD"},
                        "status": "CANCELED",
                        "source_type": "CARD",
                        "created_at": "2026-04-27T11:00:00Z",
                        "capabilities": [],
                    }
                },
            }
        }
        result = parse_payment(payload)
        assert result["transaction_status"] == "VOIDED"

    def test_missing_device_yields_none_workstation(self):
        payload = {
            "data": {
                "type": "payment",
                "id": "evt_789",
                "object": {
                    "payment": {
                        "id": "pay_nodev",
                        "location_id": "loc_001",
                        "amount_money": {"amount": 100, "currency": "USD"},
                        "total_money": {"amount": 100, "currency": "USD"},
                        "status": "COMPLETED",
                        "source_type": "CARD",
                        "created_at": "2026-04-27T12:00:00Z",
                        "capabilities": [],
                    }
                },
            }
        }
        result = parse_payment(payload)
        assert result["workstation_id"] is None
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd ~/GrowDirect/Canary && python3 -m pytest tests/unit/test_arts_alignment.py -v -x 2>&1 | head -20
```

Expected: FAIL — `source_system` key not in result dict.

- [ ] **Step 3: Update parse_payment to populate ARTS fields**

Edit `Canary/canary/services/parsers/square_payment_parser.py`. At the top, add `from datetime import date as date_type` if needed.

In the `parse_payment` function, after the existing field extraction and before the `return` statement, add:

```python
    # ARTS POSLOG canonical fields (GRO-626 CS5)
    result["source_system"] = "SQUARE"

    # business_day_date: date portion of created_at
    created_str = payment.get("created_at", "")
    if created_str:
        try:
            result["business_day_date"] = datetime.fromisoformat(
                created_str.replace("Z", "+00:00")
            ).date()
        except (ValueError, AttributeError):
            result["business_day_date"] = None
    else:
        result["business_day_date"] = None

    # workstation_id: Square device_id is the canonical workstation
    result["workstation_id"] = payment.get("device_id")

    # operator_id: same as employee_id for Square
    result["operator_id"] = payment.get("employee_id")

    # transaction_status: derive from transaction_type
    txn_type = result.get("transaction_type", "")
    if txn_type in ("VOID", "POST_VOID"):
        result["transaction_status"] = "VOIDED"
    else:
        result["transaction_status"] = "COMPLETE"
```

Note: `datetime` should already be imported in this file. If the parser uses a different datetime parsing pattern, follow the existing convention.

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd ~/GrowDirect/Canary && python3 -m pytest tests/unit/test_arts_alignment.py -v -x
```

Expected: PASS (all 7 tests).

- [ ] **Step 5: Run existing parser tests for regression**

```bash
cd ~/GrowDirect/Canary && python3 -m pytest tests/unit/test_square_parsers.py -v 2>&1 | tail -10
```

Expected: All existing tests still pass.

- [ ] **Step 6: Commit**

```bash
cd ~/GrowDirect/Canary && git add canary/services/parsers/square_payment_parser.py tests/unit/test_arts_alignment.py
git commit -m "feat(parsers): populate ARTS fields in Square payment parser (GRO-626 CS5)"
```

---

### Task 6: Write Alembic migration for GRO-626

**Files:**
- Create: `Canary/canary/migrations/versions/gro626_arts_poslog_alignment.py`

- [ ] **Step 1: Generate migration stub**

```bash
cd ~/GrowDirect/Canary && alembic revision -m "gro626_arts_poslog_alignment" 2>&1 | tail -5
```

Note the generated file path.

- [ ] **Step 2: Write migration content**

Edit the generated migration file. **Preserve the auto-generated `revision`, `down_revision`, `branch_labels`, and `depends_on` variables from the stub.** Replace only the docstring, imports, `upgrade()`, and `downgrade()` functions:

```python
"""GRO-626: ARTS POSLOG alignment — additive schema changes.

Adds ARTS canonical columns to transactions, transaction_line_items,
transaction_tenders. Creates transaction_taxes table.
"""
from alembic import op
import sqlalchemy as sa

# revision, down_revision, etc. — KEEP FROM GENERATED STUB

def upgrade() -> None:
    # CS1: Transaction ARTS columns
    op.add_column("transactions", sa.Column("source_system", sa.String(32), nullable=True), schema="sales")
    op.add_column("transactions", sa.Column("business_day_date", sa.Date(), nullable=True), schema="sales")
    op.add_column("transactions", sa.Column("workstation_id", sa.String(length=255), nullable=True), schema="sales")
    op.add_column("transactions", sa.Column("sequence_number", sa.Integer(), nullable=True), schema="sales")
    op.add_column("transactions", sa.Column("begin_datetime", sa.DateTime(), nullable=True), schema="sales")
    op.add_column("transactions", sa.Column("end_datetime", sa.DateTime(), nullable=True), schema="sales")
    op.add_column("transactions", sa.Column("operator_id", sa.String(length=255), nullable=True), schema="sales")
    op.add_column("transactions", sa.Column("transaction_status", sa.String(20), nullable=True), schema="sales")

    op.create_index(
        "ix_transactions_business_day_date", "transactions",
        ["merchant_id", "business_day_date"], schema="sales",
    )
    op.create_index(
        "ix_transactions_workstation", "transactions",
        ["merchant_id", "workstation_id"], schema="sales",
    )
    op.create_index(
        "ix_transactions_operator", "transactions",
        ["merchant_id", "operator_id"], schema="sales",
    )
    op.create_index(
        "ix_transactions_arts_key", "transactions",
        ["merchant_id", "source_system", "workstation_id", "business_day_date", "sequence_number"],
        schema="sales",
    )

    # CS2: TransactionLineItem ARTS columns
    op.add_column("transaction_line_items", sa.Column("line_sequence_number", sa.Integer(), nullable=True), schema="sales")
    op.add_column("transaction_line_items", sa.Column("article_id", sa.String(length=255), nullable=True), schema="sales")
    op.add_column("transaction_line_items", sa.Column("uom", sa.String(16), nullable=True), schema="sales")
    op.add_column("transaction_line_items", sa.Column("line_type", sa.String(20), nullable=True), schema="sales")
    op.add_column("transaction_line_items", sa.Column("regular_unit_price_cents", sa.Integer(), nullable=True), schema="sales")
    op.add_column("transaction_line_items", sa.Column("actual_unit_price_cents", sa.Integer(), nullable=True), schema="sales")
    op.add_column("transaction_line_items", sa.Column("price_override_reason", sa.String(length=255), nullable=True), schema="sales")

    op.create_index(
        "ix_lineitem_article", "transaction_line_items",
        ["merchant_id", "article_id"], schema="sales",
    )

    # CS3: TransactionTender canonical type
    op.add_column("transaction_tenders", sa.Column("canonical_tender_type", sa.String(32), nullable=True), schema="sales")

    # CS4: TransactionTax table
    op.create_table(
        "transaction_taxes",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("merchant_id", sa.String(), nullable=False),
        sa.Column("transaction_id", sa.String(), sa.ForeignKey("sales.transactions.id", name="fk_tx_tax_transaction"), nullable=False),
        sa.Column("line_item_id", sa.String(), sa.ForeignKey("sales.transaction_line_items.id", name="fk_tx_tax_line"), nullable=True),
        sa.Column("jurisdiction_code", sa.String(), nullable=True),
        sa.Column("jurisdiction_level", sa.String(20), nullable=True),
        sa.Column("tax_category", sa.String(32), nullable=True),
        sa.Column("taxable_amount_cents", sa.Integer(), nullable=False),
        sa.Column("tax_rate", sa.Numeric(8, 6), nullable=True),
        sa.Column("tax_amount_cents", sa.Integer(), nullable=False),
        sa.Column("is_exempt", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("source_system", sa.String(32), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        schema="sales",
    )
    op.create_index("ix_tx_tax_merchant", "transaction_taxes", ["merchant_id"], schema="sales")
    op.create_index("ix_tx_tax_merchant_transaction", "transaction_taxes", ["merchant_id", "transaction_id"], schema="sales")
    op.create_index("ix_tx_tax_merchant_jurisdiction", "transaction_taxes", ["merchant_id", "jurisdiction_level"], schema="sales")


def downgrade() -> None:
    # CS4
    op.drop_table("transaction_taxes", schema="sales")

    # CS3
    op.drop_column("transaction_tenders", "canonical_tender_type", schema="sales")

    # CS2
    op.drop_index("ix_lineitem_article", "transaction_line_items", schema="sales")
    op.drop_column("transaction_line_items", "price_override_reason", schema="sales")
    op.drop_column("transaction_line_items", "actual_unit_price_cents", schema="sales")
    op.drop_column("transaction_line_items", "regular_unit_price_cents", schema="sales")
    op.drop_column("transaction_line_items", "line_type", schema="sales")
    op.drop_column("transaction_line_items", "uom", schema="sales")
    op.drop_column("transaction_line_items", "article_id", schema="sales")
    op.drop_column("transaction_line_items", "line_sequence_number", schema="sales")

    # CS1
    op.drop_index("ix_transactions_arts_key", "transactions", schema="sales")
    op.drop_index("ix_transactions_operator", "transactions", schema="sales")
    op.drop_index("ix_transactions_workstation", "transactions", schema="sales")
    op.drop_index("ix_transactions_business_day_date", "transactions", schema="sales")
    op.drop_column("transactions", "transaction_status", schema="sales")
    op.drop_column("transactions", "operator_id", schema="sales")
    op.drop_column("transactions", "end_datetime", schema="sales")
    op.drop_column("transactions", "begin_datetime", schema="sales")
    op.drop_column("transactions", "sequence_number", schema="sales")
    op.drop_column("transactions", "workstation_id", schema="sales")
    op.drop_column("transactions", "business_day_date", schema="sales")
    op.drop_column("transactions", "source_system", schema="sales")
```

- [ ] **Step 3: Run migration against dev database**

```bash
cd ~/GrowDirect/Canary && alembic upgrade head 2>&1
```

Expected: Migration applies cleanly.

- [ ] **Step 4: Verify migration against test database**

```bash
cd ~/GrowDirect/Canary && DATABASE_URL=postgresql://growdirect:growdirect_dev@localhost:5432/canary_test alembic upgrade head 2>&1
```

Expected: Clean upgrade.

- [ ] **Step 5: Run full integration test suite to confirm no regression**

```bash
cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_arts_schema.py -v
```

Expected: All tests in test_arts_schema.py pass.

- [ ] **Step 6: Run existing test suite for regression**

```bash
cd ~/GrowDirect/Canary && python3 -m pytest tests/ -x --timeout=60 2>&1 | tail -20
```

Expected: No regressions.

- [ ] **Step 7: Commit**

```bash
cd ~/GrowDirect/Canary && git add canary/migrations/versions/gro626_*.py
git commit -m "migrate: GRO-626 ARTS POSLOG alignment (columns + transaction_taxes table)"
```

---

## Chunk 3: GRO-627 TransactionFact Model & Builder

### Task 7: Create TransactionFact model

**Files:**
- Create: `Canary/canary/models/sales/transaction_facts.py`
- Modify: `Canary/canary/models/sales/__init__.py`
- Test: `Canary/tests/integration/test_transaction_facts.py`

- [ ] **Step 1: Write the failing integration test**

Create `Canary/tests/integration/test_transaction_facts.py`:

```python
"""Integration tests for TransactionFact model (GRO-627)."""
import pytest
from datetime import date, datetime, timezone
from decimal import Decimal
from canary.models.base import SalesBase, generate_uuid
from canary.models.sales.transactions import Transaction
from canary.models.sales.transaction_facts import TransactionFact

pytestmark = [pytest.mark.postgres, pytest.mark.integration]


def _make_transaction(sales_session, **overrides):
    defaults = dict(
        id=generate_uuid(),
        merchant_id=generate_uuid(),
        external_id=generate_uuid(),
        source_type="WEBHOOK",
        location_id=generate_uuid(),
        transaction_type="SALE",
        transaction_date=datetime.now(timezone.utc),
        amount_cents=5000,
        currency="USD",
        source_system="SQUARE",
        business_day_date=date(2026, 4, 27),
    )
    defaults.update(overrides)
    txn = Transaction(**defaults)
    sales_session.add(txn)
    sales_session.flush()
    return txn


class TestTransactionFactPersistence:
    """Verify TransactionFact table and constraints."""

    def test_fact_row_created(self, sales_session):
        txn = _make_transaction(sales_session)
        fact = TransactionFact(
            id=generate_uuid(),
            transaction_id=txn.id,
            merchant_id=txn.merchant_id,
            location_id=txn.location_id,
            employee_id=None,
            operator_id=None,
            business_day_date=date(2026, 4, 27),
            computed_at=datetime.now(timezone.utc),
            line_count=3,
            unique_sku_count=2,
            basket_size=5,
            line_void_count=0,
            line_void_rate=Decimal("0.0000"),
            post_sale_void_flag=False,
            coupon_count=0,
            discount_count=1,
            manual_price_override_count=0,
            discount_amount_cents=200,
            manual_override_amount_cents=0,
            discount_rate=Decimal("0.0400"),
            gross_amount_cents=5000,
            net_amount_cents=4800,
            tax_amount_cents=396,
            refund_amount_cents=0,
            tender_count=1,
            split_tender_flag=False,
            cash_tender_amount_cents=0,
            gift_card_tender_amount_cents=0,
            return_line_count=0,
            refund_without_linked_sale_flag=False,
            avg_unit_price_cents=1600,
            max_unit_price_cents=2500,
            high_value_item_count=0,
            transaction_duration_seconds=None,
            is_after_hours=False,
            age_restricted_item_count=0,
            age_verification_performed=False,
        )
        sales_session.add(fact)
        sales_session.flush()

        result = sales_session.get(TransactionFact, fact.id)
        assert result.transaction_id == txn.id
        assert result.line_count == 3
        assert result.discount_rate == Decimal("0.0400")
        assert result.chirp_score is None
        assert result.chirp_rules_bitmap is None
        assert result.scored_at is None

    def test_unique_constraint_on_transaction_id(self, sales_session):
        """Only one fact row per transaction."""
        txn = _make_transaction(sales_session)
        fact1 = TransactionFact(
            id=generate_uuid(),
            transaction_id=txn.id,
            merchant_id=txn.merchant_id,
            location_id=txn.location_id,
            business_day_date=date(2026, 4, 27),
            computed_at=datetime.now(timezone.utc),
            line_count=1, unique_sku_count=1, basket_size=1,
            line_void_count=0, line_void_rate=Decimal("0"),
            post_sale_void_flag=False,
            coupon_count=0, discount_count=0,
            manual_price_override_count=0,
            discount_amount_cents=0, manual_override_amount_cents=0,
            discount_rate=Decimal("0"),
            gross_amount_cents=1000, net_amount_cents=1000,
            tax_amount_cents=0, refund_amount_cents=0,
            tender_count=1, split_tender_flag=False,
            cash_tender_amount_cents=0,
            gift_card_tender_amount_cents=0,
            return_line_count=0,
            refund_without_linked_sale_flag=False,
            avg_unit_price_cents=1000, max_unit_price_cents=1000,
            high_value_item_count=0,
            is_after_hours=False,
            age_restricted_item_count=0,
            age_verification_performed=False,
        )
        sales_session.add(fact1)
        sales_session.flush()

        from sqlalchemy.exc import IntegrityError
        fact2 = TransactionFact(
            id=generate_uuid(),
            transaction_id=txn.id,  # same transaction
            merchant_id=txn.merchant_id,
            location_id=txn.location_id,
            business_day_date=date(2026, 4, 27),
            computed_at=datetime.now(timezone.utc),
            line_count=1, unique_sku_count=1, basket_size=1,
            line_void_count=0, line_void_rate=Decimal("0"),
            post_sale_void_flag=False,
            coupon_count=0, discount_count=0,
            manual_price_override_count=0,
            discount_amount_cents=0, manual_override_amount_cents=0,
            discount_rate=Decimal("0"),
            gross_amount_cents=1000, net_amount_cents=1000,
            tax_amount_cents=0, refund_amount_cents=0,
            tender_count=1, split_tender_flag=False,
            cash_tender_amount_cents=0,
            gift_card_tender_amount_cents=0,
            return_line_count=0,
            refund_without_linked_sale_flag=False,
            avg_unit_price_cents=1000, max_unit_price_cents=1000,
            high_value_item_count=0,
            is_after_hours=False,
            age_restricted_item_count=0,
            age_verification_performed=False,
        )
        sales_session.add(fact2)
        with pytest.raises(IntegrityError):
            sales_session.flush()

    def test_chirp_second_pass_update(self, sales_session):
        """Chirp fields can be updated after initial insert."""
        txn = _make_transaction(sales_session)
        fact = TransactionFact(
            id=generate_uuid(),
            transaction_id=txn.id,
            merchant_id=txn.merchant_id,
            location_id=txn.location_id,
            business_day_date=date(2026, 4, 27),
            computed_at=datetime.now(timezone.utc),
            line_count=1, unique_sku_count=1, basket_size=1,
            line_void_count=0, line_void_rate=Decimal("0"),
            post_sale_void_flag=False,
            coupon_count=0, discount_count=0,
            manual_price_override_count=0,
            discount_amount_cents=0, manual_override_amount_cents=0,
            discount_rate=Decimal("0"),
            gross_amount_cents=1000, net_amount_cents=1000,
            tax_amount_cents=0, refund_amount_cents=0,
            tender_count=1, split_tender_flag=False,
            cash_tender_amount_cents=0,
            gift_card_tender_amount_cents=0,
            return_line_count=0,
            refund_without_linked_sale_flag=False,
            avg_unit_price_cents=1000, max_unit_price_cents=1000,
            high_value_item_count=0,
            is_after_hours=False,
            age_restricted_item_count=0,
            age_verification_performed=False,
        )
        sales_session.add(fact)
        sales_session.flush()

        # Second-pass: chirp scoring
        fact.chirp_score = Decimal("7.50")
        fact.active_chirp_count = 2
        fact.chirp_rules_bitmap = (1 << 3) | (1 << 7)  # rules 3 and 7 fired
        fact.scored_at = datetime.now(timezone.utc)
        sales_session.flush()

        result = sales_session.get(TransactionFact, fact.id)
        assert result.chirp_score == Decimal("7.50")
        assert result.active_chirp_count == 2
        assert result.chirp_rules_bitmap & (1 << 3) != 0  # rule 3 fired
        assert result.chirp_rules_bitmap & (1 << 7) != 0  # rule 7 fired
        assert result.chirp_rules_bitmap & (1 << 5) == 0  # rule 5 did not fire
        assert result.scored_at is not None
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_transaction_facts.py -v -x 2>&1 | head -20
```

Expected: FAIL — `transaction_facts` module does not exist.

- [ ] **Step 3: Create TransactionFact model**

Create `Canary/canary/models/sales/transaction_facts.py`:

```python
"""
Pre-computed header-level scoring row — one per closed transaction.

Written by the fact builder service at T.CLOSE. Chirp fields filled
in a second pass by the detection engine. Immutable after initial
write except for chirp columns.

GRO-627.
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    BigInteger, ForeignKey, Index, Numeric, String, UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from canary.models.base import SalesBase, generate_uuid


class TransactionFact(SalesBase):
    __tablename__ = "transaction_facts"

    # --- identity / partition ---
    id: Mapped[str] = mapped_column(primary_key=True, default=generate_uuid)
    transaction_id: Mapped[str] = mapped_column(
        ForeignKey("transactions.id", name="fk_txfact_transaction"),
        nullable=False,
    )
    merchant_id: Mapped[str] = mapped_column(nullable=False)
    location_id: Mapped[str] = mapped_column(nullable=False)
    employee_id: Mapped[Optional[str]] = mapped_column(nullable=True)
    operator_id: Mapped[Optional[str]] = mapped_column(
        nullable=True, doc="ARTS operator — may differ from employee on supervised register",
    )
    business_day_date: Mapped[date] = mapped_column(nullable=False)
    computed_at: Mapped[datetime] = mapped_column(nullable=False)

    # --- basket composition ---
    line_count: Mapped[int] = mapped_column(nullable=False, doc="Total non-void lines")
    unique_sku_count: Mapped[int] = mapped_column(nullable=False)
    basket_size: Mapped[int] = mapped_column(nullable=False, doc="Sum of line quantities")

    # --- void / cancellation signals ---
    line_void_count: Mapped[int] = mapped_column(nullable=False)
    line_void_rate: Mapped[Decimal] = mapped_column(
        Numeric(5, 4), nullable=False,
        doc="line_void_count / (line_count + line_void_count) — stored, never divide at query time",
    )
    post_sale_void_flag: Mapped[bool] = mapped_column(nullable=False)

    # --- discount / coupon signals ---
    coupon_count: Mapped[int] = mapped_column(nullable=False)
    discount_count: Mapped[int] = mapped_column(nullable=False)
    manual_price_override_count: Mapped[int] = mapped_column(nullable=False)
    discount_amount_cents: Mapped[int] = mapped_column(nullable=False)
    manual_override_amount_cents: Mapped[int] = mapped_column(nullable=False)
    discount_rate: Mapped[Decimal] = mapped_column(
        Numeric(5, 4), nullable=False,
        doc="discount_amount / gross_amount — stored, never divide at query time",
    )

    # --- amounts ---
    gross_amount_cents: Mapped[int] = mapped_column(nullable=False)
    net_amount_cents: Mapped[int] = mapped_column(nullable=False)
    tax_amount_cents: Mapped[int] = mapped_column(nullable=False)
    refund_amount_cents: Mapped[int] = mapped_column(nullable=False)

    # --- tender signals ---
    tender_count: Mapped[int] = mapped_column(nullable=False)
    split_tender_flag: Mapped[bool] = mapped_column(nullable=False)
    cash_tender_amount_cents: Mapped[int] = mapped_column(nullable=False)
    gift_card_tender_amount_cents: Mapped[int] = mapped_column(nullable=False)

    # --- return signals ---
    return_line_count: Mapped[int] = mapped_column(nullable=False)
    refund_without_linked_sale_flag: Mapped[bool] = mapped_column(nullable=False)

    # --- pricing signals ---
    avg_unit_price_cents: Mapped[int] = mapped_column(nullable=False)
    max_unit_price_cents: Mapped[int] = mapped_column(nullable=False)
    high_value_item_count: Mapped[int] = mapped_column(nullable=False)

    # --- timing / behavioral ---
    transaction_duration_seconds: Mapped[Optional[int]] = mapped_column(
        nullable=True, doc="end_datetime - begin_datetime; null if ARTS fields not populated",
    )
    is_after_hours: Mapped[bool] = mapped_column(nullable=False)

    # --- compliance ---
    age_restricted_item_count: Mapped[int] = mapped_column(nullable=False)
    age_verification_performed: Mapped[bool] = mapped_column(nullable=False)

    # --- chirp output (second-pass write by detection engine) ---
    chirp_score: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(5, 2), nullable=True, doc="Nil until detection engine runs",
    )
    active_chirp_count: Mapped[Optional[int]] = mapped_column(nullable=True)
    chirp_rules_bitmap: Mapped[Optional[int]] = mapped_column(
        BigInteger, nullable=True,
        doc="Bit N = rule N fired; != 0 means any alert; no join needed for bulk scan",
    )
    scored_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    # --- timestamps ---
    created_at: Mapped[datetime] = mapped_column(
        server_default="now()", nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default="now()", nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("transaction_id", name="uq_txfact_transaction"),
        Index("ix_txfact_merchant_bday", "merchant_id", "business_day_date"),
        Index("ix_txfact_merchant_employee_bday", "merchant_id", "employee_id", "business_day_date"),
        Index("ix_txfact_merchant_location_bday", "merchant_id", "location_id", "business_day_date"),
        Index(
            "ix_txfact_chirp_bitmap", "merchant_id", "chirp_rules_bitmap",
            postgresql_where="chirp_rules_bitmap IS NOT NULL AND chirp_rules_bitmap != 0",
        ),
        Index(
            "ix_txfact_pending_scoring", "merchant_id", "scored_at",
            postgresql_where="scored_at IS NULL",
        ),
    )
```

- [ ] **Step 4: Export TransactionFact from __init__.py**

Edit `Canary/canary/models/sales/__init__.py`. Add:

```python
from canary.models.sales.transaction_facts import TransactionFact
```

- [ ] **Step 4b: Add TransactionFact import to integration conftest**

Edit `Canary/tests/integration/conftest.py`. Add after the TransactionTax import:

```python
from canary.models.sales.transaction_facts import TransactionFact  # noqa: F401
```

- [ ] **Step 5: Run test to verify it passes**

```bash
cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_transaction_facts.py -v -x
```

Expected: PASS (all 3 tests).

- [ ] **Step 6: Commit**

```bash
cd ~/GrowDirect/Canary && git add canary/models/sales/transaction_facts.py canary/models/sales/__init__.py tests/integration/test_transaction_facts.py
git commit -m "feat(sales): add TransactionFact scoring substrate model (GRO-627 CS1)"
```

---

### Task 8: Create FactBuilderService

**Files:**
- Create: `Canary/canary/services/fact_builder.py`
- Test: `Canary/tests/unit/test_fact_builder.py`

- [ ] **Step 1: Write failing unit tests for fact computation**

Create `Canary/tests/unit/test_fact_builder.py`:

```python
"""Unit tests for FactBuilderService — pure computation, no DB (GRO-627 CS2)."""
import pytest
from datetime import date, datetime, timezone
from decimal import Decimal

from canary.services.fact_builder import FactBuilderService

pytestmark = [pytest.mark.unit]


def _txn(**overrides):
    """Minimal transaction dict matching model attributes."""
    defaults = dict(
        id="txn-001",
        merchant_id="m-001",
        location_id="loc-001",
        employee_id="emp-001",
        operator_id="emp-001",
        transaction_type="SALE",
        transaction_date=datetime(2026, 4, 27, 14, 30, 0, tzinfo=timezone.utc),
        business_day_date=date(2026, 4, 27),
        amount_cents=5000,
        tax_amount_cents=412,
        discount_amount_cents=200,
        begin_datetime=datetime(2026, 4, 27, 14, 28, 0, tzinfo=timezone.utc),
        end_datetime=datetime(2026, 4, 27, 14, 30, 0, tzinfo=timezone.utc),
    )
    defaults.update(overrides)
    return defaults


def _line(item_type="ITEM", is_voided=False, quantity="1.0",
          base_price_cents=1000, gross_sales_cents=1000,
          total_discount_cents=0, catalog_object_id="sku-001",
          line_type=None, price_override_reason=None, return_reason=None):
    return dict(
        item_type=item_type,
        is_voided=is_voided,
        quantity=Decimal(quantity),
        base_price_cents=base_price_cents,
        gross_sales_cents=gross_sales_cents,
        total_discount_cents=total_discount_cents,
        catalog_object_id=catalog_object_id,
        line_type=line_type,
        price_override_reason=price_override_reason,
        return_reason=return_reason,
    )


def _tender(tender_type="CARD", amount_cents=5000):
    return dict(tender_type=tender_type, amount_cents=amount_cents)


class TestBasketComposition:
    def test_line_count_excludes_voids(self):
        lines = [_line(), _line(), _line(is_voided=True)]
        result = FactBuilderService.compute(
            _txn(), lines, [_tender()], business_hours=None,
        )
        assert result["line_count"] == 2

    def test_unique_sku_count(self):
        lines = [
            _line(catalog_object_id="a"),
            _line(catalog_object_id="a"),
            _line(catalog_object_id="b"),
        ]
        result = FactBuilderService.compute(
            _txn(), lines, [_tender()], business_hours=None,
        )
        assert result["unique_sku_count"] == 2

    def test_basket_size_is_sum_of_quantities(self):
        lines = [_line(quantity="2.0"), _line(quantity="3.0")]
        result = FactBuilderService.compute(
            _txn(), lines, [_tender()], business_hours=None,
        )
        assert result["basket_size"] == 5


class TestVoidSignals:
    def test_void_count_and_rate(self):
        lines = [_line(), _line(is_voided=True)]
        result = FactBuilderService.compute(
            _txn(), lines, [_tender()], business_hours=None,
        )
        assert result["line_void_count"] == 1
        # 1 / (1 + 1) = 0.5
        assert result["line_void_rate"] == Decimal("0.5000")

    def test_zero_voids(self):
        lines = [_line(), _line()]
        result = FactBuilderService.compute(
            _txn(), lines, [_tender()], business_hours=None,
        )
        assert result["line_void_count"] == 0
        assert result["line_void_rate"] == Decimal("0.0000")


class TestDiscountSignals:
    def test_discount_count(self):
        lines = [
            _line(total_discount_cents=100),
            _line(total_discount_cents=0),
            _line(total_discount_cents=50),
        ]
        result = FactBuilderService.compute(
            _txn(discount_amount_cents=150), lines, [_tender()], business_hours=None,
        )
        assert result["discount_count"] == 2

    def test_manual_price_override_count(self):
        lines = [
            _line(price_override_reason="MANAGER_MARKDOWN"),
            _line(price_override_reason=None),
        ]
        result = FactBuilderService.compute(
            _txn(), lines, [_tender()], business_hours=None,
        )
        assert result["manual_price_override_count"] == 1

    def test_discount_rate_stored(self):
        result = FactBuilderService.compute(
            _txn(amount_cents=10000, discount_amount_cents=500),
            [_line(gross_sales_cents=10000)],
            [_tender(amount_cents=9500)],
            business_hours=None,
        )
        # 500 / 10000 = 0.05
        assert result["discount_rate"] == Decimal("0.0500")


class TestTenderSignals:
    def test_split_tender(self):
        tenders = [_tender("CASH", 2000), _tender("CARD", 3000)]
        result = FactBuilderService.compute(
            _txn(), [_line()], tenders, business_hours=None,
        )
        assert result["tender_count"] == 2
        assert result["split_tender_flag"] is True

    def test_cash_tender_amount(self):
        tenders = [_tender("CASH", 2000), _tender("CARD", 3000)]
        result = FactBuilderService.compute(
            _txn(), [_line()], tenders, business_hours=None,
        )
        assert result["cash_tender_amount_cents"] == 2000

    def test_gift_card_amount(self):
        tenders = [_tender("SQUARE_GIFT_CARD", 1000), _tender("CARD", 4000)]
        result = FactBuilderService.compute(
            _txn(), [_line()], tenders, business_hours=None,
        )
        assert result["gift_card_tender_amount_cents"] == 1000


class TestReturnSignals:
    def test_return_line_count(self):
        lines = [
            _line(line_type="SALE"),
            _line(line_type="RETURN", return_reason="DEFECTIVE"),
        ]
        result = FactBuilderService.compute(
            _txn(), lines, [_tender()], business_hours=None,
        )
        assert result["return_line_count"] == 1


class TestTimingSignals:
    def test_duration_computed(self):
        result = FactBuilderService.compute(
            _txn(
                begin_datetime=datetime(2026, 4, 27, 14, 28, 0, tzinfo=timezone.utc),
                end_datetime=datetime(2026, 4, 27, 14, 30, 30, tzinfo=timezone.utc),
            ),
            [_line()], [_tender()], business_hours=None,
        )
        assert result["transaction_duration_seconds"] == 150

    def test_duration_null_without_arts_times(self):
        result = FactBuilderService.compute(
            _txn(begin_datetime=None, end_datetime=None),
            [_line()], [_tender()], business_hours=None,
        )
        assert result["transaction_duration_seconds"] is None

    def test_after_hours_detection(self):
        # business_hours: {"open": "09:00", "close": "21:00"}
        result = FactBuilderService.compute(
            _txn(transaction_date=datetime(2026, 4, 27, 22, 30, 0, tzinfo=timezone.utc)),
            [_line()], [_tender()],
            business_hours={"open": "09:00", "close": "21:00"},
        )
        assert result["is_after_hours"] is True

    def test_during_hours(self):
        result = FactBuilderService.compute(
            _txn(transaction_date=datetime(2026, 4, 27, 14, 30, 0, tzinfo=timezone.utc)),
            [_line()], [_tender()],
            business_hours={"open": "09:00", "close": "21:00"},
        )
        assert result["is_after_hours"] is False

    def test_no_business_hours_assumes_not_after_hours(self):
        result = FactBuilderService.compute(
            _txn(), [_line()], [_tender()], business_hours=None,
        )
        assert result["is_after_hours"] is False
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd ~/GrowDirect/Canary && python3 -m pytest tests/unit/test_fact_builder.py -v -x 2>&1 | head -20
```

Expected: FAIL — `canary.services.fact_builder` does not exist.

- [ ] **Step 3: Implement FactBuilderService**

Create `Canary/canary/services/fact_builder.py`:

```python
"""
FactBuilderService — computes TransactionFact fields from transaction data.

Pure computation: takes dicts (or model attributes), returns a dict of fact
fields ready for TransactionFact insertion. No DB access in compute().

GRO-627 CS2.
"""
from datetime import datetime, time, timezone
from decimal import Decimal, ROUND_HALF_UP


class FactBuilderService:

    CASH_TENDER_TYPES = {"CASH"}
    GIFT_CARD_TENDER_TYPES = {"SQUARE_GIFT_CARD", "GIFT_CARD", "STORE_CREDIT"}
    RETURN_LINE_TYPES = {"RETURN", "RETURN_CUSTOMER"}

    @staticmethod
    def compute(
        txn: dict,
        lines: list[dict],
        tenders: list[dict],
        business_hours: dict | None,
    ) -> dict:
        """Compute all fact fields from transaction data.

        Args:
            txn: Transaction attributes dict.
            lines: List of line item attribute dicts.
            tenders: List of tender attribute dicts.
            business_hours: {"open": "HH:MM", "close": "HH:MM"} or None.

        Returns:
            Dict of TransactionFact fields (excluding id, created_at, updated_at,
            and chirp second-pass fields).
        """
        # --- Partition lines ---
        active_lines = [l for l in lines if not l.get("is_voided", False)]
        void_lines = [l for l in lines if l.get("is_voided", False)]

        # --- Basket composition ---
        line_count = len(active_lines)
        unique_skus = {l.get("catalog_object_id") or l.get("article_id")
                       for l in active_lines}
        unique_skus.discard(None)
        unique_sku_count = len(unique_skus)
        basket_size = int(sum(Decimal(str(l.get("quantity", 0))) for l in active_lines))

        # --- Void signals ---
        line_void_count = len(void_lines)
        total_for_rate = line_count + line_void_count
        line_void_rate = (
            Decimal(line_void_count) / Decimal(total_for_rate)
            if total_for_rate > 0 else Decimal("0")
        ).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)

        post_sale_void_flag = txn.get("transaction_type") in ("VOID", "POST_VOID")

        # --- Discount / coupon signals ---
        discount_count = sum(
            1 for l in active_lines if l.get("total_discount_cents", 0) > 0
        )
        manual_price_override_count = sum(
            1 for l in active_lines if l.get("price_override_reason")
        )
        coupon_count = 0  # requires discount type data; populated when available
        discount_amount_cents = txn.get("discount_amount_cents", 0)
        manual_override_amount_cents = sum(
            l.get("total_discount_cents", 0) for l in active_lines
            if l.get("price_override_reason")
        )

        gross_amount_cents = sum(
            l.get("gross_sales_cents", 0) for l in active_lines
        ) or txn.get("amount_cents", 0)

        discount_rate = (
            Decimal(discount_amount_cents) / Decimal(gross_amount_cents)
            if gross_amount_cents > 0 else Decimal("0")
        ).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)

        # --- Amounts ---
        net_amount_cents = txn.get("amount_cents", 0)
        tax_amount_cents = txn.get("tax_amount_cents", 0)
        refund_amount_cents = (
            abs(net_amount_cents) if txn.get("transaction_type") == "RETURN" else 0
        )

        # --- Tender signals ---
        tender_count = len(tenders)
        split_tender_flag = tender_count > 1
        cash_tender_amount_cents = sum(
            t.get("amount_cents", 0) for t in tenders
            if t.get("tender_type") in FactBuilderService.CASH_TENDER_TYPES
        )
        gift_card_tender_amount_cents = sum(
            t.get("amount_cents", 0) for t in tenders
            if t.get("tender_type") in FactBuilderService.GIFT_CARD_TENDER_TYPES
        )

        # --- Return signals ---
        return_line_count = sum(
            1 for l in active_lines
            if l.get("line_type") in FactBuilderService.RETURN_LINE_TYPES
            or l.get("return_reason") is not None
        )
        refund_without_linked_sale_flag = (
            txn.get("transaction_type") == "RETURN"
            # No linked original — would require RefundLink check in DB layer
        )

        # --- Pricing signals ---
        unit_prices = [l.get("base_price_cents", 0) for l in active_lines]
        avg_unit_price_cents = (
            sum(unit_prices) // len(unit_prices) if unit_prices else 0
        )
        max_unit_price_cents = max(unit_prices) if unit_prices else 0
        high_value_item_count = 0  # requires merchant threshold config; set in DB layer

        # --- Timing / behavioral ---
        begin_dt = txn.get("begin_datetime")
        end_dt = txn.get("end_datetime")
        if begin_dt and end_dt:
            transaction_duration_seconds = int((end_dt - begin_dt).total_seconds())
        else:
            transaction_duration_seconds = None

        is_after_hours = False
        if business_hours:
            txn_time = txn.get("transaction_date")
            if txn_time and hasattr(txn_time, "hour"):
                open_parts = business_hours.get("open", "00:00").split(":")
                close_parts = business_hours.get("close", "23:59").split(":")
                open_time = time(int(open_parts[0]), int(open_parts[1]))
                close_time = time(int(close_parts[0]), int(close_parts[1]))
                txn_time_only = txn_time.time() if hasattr(txn_time, "time") else time(txn_time.hour, txn_time.minute)
                is_after_hours = txn_time_only < open_time or txn_time_only >= close_time

        # --- Compliance ---
        age_restricted_item_count = 0  # requires item catalog lookup; set in DB layer
        age_verification_performed = False  # requires compliance event; set in DB layer

        return {
            "transaction_id": txn["id"],
            "merchant_id": txn["merchant_id"],
            "location_id": txn["location_id"],
            "employee_id": txn.get("employee_id"),
            "operator_id": txn.get("operator_id"),
            "business_day_date": txn.get("business_day_date"),
            "computed_at": datetime.now(timezone.utc),
            "line_count": line_count,
            "unique_sku_count": unique_sku_count,
            "basket_size": basket_size,
            "line_void_count": line_void_count,
            "line_void_rate": line_void_rate,
            "post_sale_void_flag": post_sale_void_flag,
            "coupon_count": coupon_count,
            "discount_count": discount_count,
            "manual_price_override_count": manual_price_override_count,
            "discount_amount_cents": discount_amount_cents,
            "manual_override_amount_cents": manual_override_amount_cents,
            "discount_rate": discount_rate,
            "gross_amount_cents": gross_amount_cents,
            "net_amount_cents": net_amount_cents,
            "tax_amount_cents": tax_amount_cents,
            "refund_amount_cents": refund_amount_cents,
            "tender_count": tender_count,
            "split_tender_flag": split_tender_flag,
            "cash_tender_amount_cents": cash_tender_amount_cents,
            "gift_card_tender_amount_cents": gift_card_tender_amount_cents,
            "return_line_count": return_line_count,
            "refund_without_linked_sale_flag": refund_without_linked_sale_flag,
            "avg_unit_price_cents": avg_unit_price_cents,
            "max_unit_price_cents": max_unit_price_cents,
            "high_value_item_count": high_value_item_count,
            "transaction_duration_seconds": transaction_duration_seconds,
            "is_after_hours": is_after_hours,
            "age_restricted_item_count": age_restricted_item_count,
            "age_verification_performed": age_verification_performed,
        }
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd ~/GrowDirect/Canary && python3 -m pytest tests/unit/test_fact_builder.py -v
```

Expected: All tests PASS.

- [ ] **Step 5: Commit**

```bash
cd ~/GrowDirect/Canary && git add canary/services/fact_builder.py tests/unit/test_fact_builder.py
git commit -m "feat(services): add FactBuilderService for TransactionFact computation (GRO-627 CS2)"
```

---

### Task 9: Write Alembic migration for GRO-627

**Files:**
- Create: `Canary/canary/migrations/versions/gro627_transaction_fact_table.py`

- [ ] **Step 1: Generate migration stub**

```bash
cd ~/GrowDirect/Canary && alembic revision -m "gro627_transaction_fact_table" 2>&1 | tail -5
```

- [ ] **Step 2: Write migration content**

**Preserve the auto-generated `revision`, `down_revision`, `branch_labels`, and `depends_on` variables from the stub.** Replace only the docstring, imports, `upgrade()`, and `downgrade()`:

```python
"""GRO-627: TransactionFact scoring substrate.

Creates sales.transaction_facts — one row per closed transaction,
pre-computed scoring fields for Chirp detection.
"""
from alembic import op
import sqlalchemy as sa

# revision, down_revision, etc. — KEEP FROM GENERATED STUB

def upgrade() -> None:
    op.create_table(
        "transaction_facts",
        # identity
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("transaction_id", sa.String(),
                  sa.ForeignKey("sales.transactions.id", name="fk_txfact_transaction"),
                  nullable=False),
        sa.Column("merchant_id", sa.String(), nullable=False),
        sa.Column("location_id", sa.String(), nullable=False),
        sa.Column("employee_id", sa.String(), nullable=True),
        sa.Column("operator_id", sa.String(), nullable=True),
        sa.Column("business_day_date", sa.Date(), nullable=False),
        sa.Column("computed_at", sa.DateTime(), nullable=False),
        # basket
        sa.Column("line_count", sa.Integer(), nullable=False),
        sa.Column("unique_sku_count", sa.Integer(), nullable=False),
        sa.Column("basket_size", sa.Integer(), nullable=False),
        # void
        sa.Column("line_void_count", sa.Integer(), nullable=False),
        sa.Column("line_void_rate", sa.Numeric(5, 4), nullable=False),
        sa.Column("post_sale_void_flag", sa.Boolean(), nullable=False),
        # discount
        sa.Column("coupon_count", sa.Integer(), nullable=False),
        sa.Column("discount_count", sa.Integer(), nullable=False),
        sa.Column("manual_price_override_count", sa.Integer(), nullable=False),
        sa.Column("discount_amount_cents", sa.Integer(), nullable=False),
        sa.Column("manual_override_amount_cents", sa.Integer(), nullable=False),
        sa.Column("discount_rate", sa.Numeric(5, 4), nullable=False),
        # amounts
        sa.Column("gross_amount_cents", sa.Integer(), nullable=False),
        sa.Column("net_amount_cents", sa.Integer(), nullable=False),
        sa.Column("tax_amount_cents", sa.Integer(), nullable=False),
        sa.Column("refund_amount_cents", sa.Integer(), nullable=False),
        # tender
        sa.Column("tender_count", sa.Integer(), nullable=False),
        sa.Column("split_tender_flag", sa.Boolean(), nullable=False),
        sa.Column("cash_tender_amount_cents", sa.Integer(), nullable=False),
        sa.Column("gift_card_tender_amount_cents", sa.Integer(), nullable=False),
        # return
        sa.Column("return_line_count", sa.Integer(), nullable=False),
        sa.Column("refund_without_linked_sale_flag", sa.Boolean(), nullable=False),
        # pricing
        sa.Column("avg_unit_price_cents", sa.Integer(), nullable=False),
        sa.Column("max_unit_price_cents", sa.Integer(), nullable=False),
        sa.Column("high_value_item_count", sa.Integer(), nullable=False),
        # timing
        sa.Column("transaction_duration_seconds", sa.Integer(), nullable=True),
        sa.Column("is_after_hours", sa.Boolean(), nullable=False),
        # compliance
        sa.Column("age_restricted_item_count", sa.Integer(), nullable=False),
        sa.Column("age_verification_performed", sa.Boolean(), nullable=False),
        # chirp (second-pass)
        sa.Column("chirp_score", sa.Numeric(5, 2), nullable=True),
        sa.Column("active_chirp_count", sa.Integer(), nullable=True),
        sa.Column("chirp_rules_bitmap", sa.BigInteger(), nullable=True),
        sa.Column("scored_at", sa.DateTime(), nullable=True),
        # timestamps
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        # constraints
        sa.UniqueConstraint("transaction_id", name="uq_txfact_transaction"),
        schema="sales",
    )

    op.create_index("ix_txfact_merchant_bday", "transaction_facts",
                    ["merchant_id", "business_day_date"], schema="sales")
    op.create_index("ix_txfact_merchant_employee_bday", "transaction_facts",
                    ["merchant_id", "employee_id", "business_day_date"], schema="sales")
    op.create_index("ix_txfact_merchant_location_bday", "transaction_facts",
                    ["merchant_id", "location_id", "business_day_date"], schema="sales")

    # Partial indexes for Chirp detection query performance
    op.execute("""
        CREATE INDEX ix_txfact_chirp_bitmap ON sales.transaction_facts (merchant_id, chirp_rules_bitmap)
        WHERE chirp_rules_bitmap IS NOT NULL AND chirp_rules_bitmap != 0
    """)
    op.execute("""
        CREATE INDEX ix_txfact_pending_scoring ON sales.transaction_facts (merchant_id, scored_at)
        WHERE scored_at IS NULL
    """)


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS sales.ix_txfact_pending_scoring")
    op.execute("DROP INDEX IF EXISTS sales.ix_txfact_chirp_bitmap")
    op.drop_table("transaction_facts", schema="sales")
```

- [ ] **Step 3: Run migration**

```bash
cd ~/GrowDirect/Canary && alembic upgrade head 2>&1
```

Expected: Clean upgrade.

- [ ] **Step 4: Run full test suite**

```bash
cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_transaction_facts.py tests/integration/test_arts_schema.py tests/unit/test_fact_builder.py tests/unit/test_arts_alignment.py -v
```

Expected: All tests pass.

- [ ] **Step 5: Commit**

```bash
cd ~/GrowDirect/Canary && git add canary/migrations/versions/gro627_*.py
git commit -m "migrate: GRO-627 transaction_facts table"
```

---

## Chunk 4: Final Verification & Linear Update

### Task 10: Full regression + Linear comments

- [ ] **Step 1: Run full test suite**

```bash
cd ~/GrowDirect/Canary && python3 -m pytest tests/ -x --timeout=120 -q 2>&1 | tail -20
```

Expected: All tests pass, no regressions.

- [ ] **Step 2: Verify migration state**

```bash
cd ~/GrowDirect/Canary && alembic current 2>&1
cd ~/GrowDirect/Canary && alembic check 2>&1
```

Expected: Head revision, no pending migrations.

- [ ] **Step 3: Comment on GRO-626 in Linear**

Comment with:
- Changed files list
- Migration ID
- Confirmation that `alembic upgrade head` ran clean
- Note: data backfill (source_system='SQUARE', business_day_date from transaction_date) is a separate dispatch

- [ ] **Step 4: Comment on GRO-627 in Linear**

Comment with:
- Created files list
- Migration ID
- Note: Chirp rule refactoring (CS3 from GRO-627) is a separate dispatch — fact builder is ready, detection engine wiring is next
- Confirm GRO-618 is unblocked

- [ ] **Step 5: Update Linear issue statuses**

Set GRO-626 status → Done.
Set GRO-627 status → Done.
