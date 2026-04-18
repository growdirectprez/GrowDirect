---
type: spec
domain: canary
status: active
created: 2026-03-19
updated: 2026-03-19
---
# Multi-POS Translation Layer Architecture

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]

**Version:** 1.0
**Date:** February 17, 2026
**Author:** Tom (Systems Architect)
**Purpose:** Define Canary's vendor-agnostic POS integration strategy using ARTS POSlog 6.0 as canonical schema with translation layer for proprietary formats

---

## Executive Summary

**The Strategy:**
- **ARTS POSlog 6.0 = Canonical Internal Schema** (our "truth" - industry-standard, future-proof)
- **Vendor-Specific Parsers** translate proprietary formats (Square JSON, Shopify JSON, Micros XML, etc.) → ARTS schema
- **Canary analytics/Fox operate on ARTS schema only** - vendor-agnostic

**Why This Matters:**
- ✅ **Industry credibility:** "ARTS POSlog 6.0 compliant" unlocks enterprise RFPs
- ✅ **Flexibility:** Can ingest any POS system (add parser, not rewrite schema)
- ✅ **Future-proof:** New POS = new parser (50-200 lines), not database migration
- ✅ **Defensible architecture:** ARTS is NRF-endorsed standard, not "made-up schema"

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     POS SYSTEMS (Data Sources)                  │
├─────────────────────────────────────────────────────────────────┤
│  Square JSON    Shopify JSON    Clover JSON    Toast JSON       │
│  Micros XML     NCR Aloha CSV   Dutchie JSON   Cova JSON       │
│  Lightspeed     Revel           Vend            SpotOn          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              TRANSLATION LAYER (Vendor Parsers)                 │
├─────────────────────────────────────────────────────────────────┤
│  SquareParser()      ShopifyParser()     CloverParser()         │
│  ToastParser()       MicrosParser()      NCRParser()           │
│  DutchieParser()     CovaParser()        [... +20 more]        │
│                                                                 │
│  Each parser implements: parse_to_arts_transaction()            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│            CANONICAL SCHEMA (ARTS POSlog 6.0)                   │
├─────────────────────────────────────────────────────────────────┤
│  POSLogTransaction (header)                                     │
│    ├── RetailTransaction                                        │
│    │   ├── LineItem[]                                          │
│    │   ├── Total[]                                             │
│    │   ├── Customer                                            │
│    │   ├── LoyaltyAccount                                      │
│    │   └── Associate[]                                         │
│    └── Metadata (source_system, raw_data_jsonb)                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│         CANARY ANALYTICS & FOX (Vendor-Agnostic)                │
├─────────────────────────────────────────────────────────────────┤
│  Fraud Detection Queries (SQL on ARTS schema)                  │
│  Fox Case Management (ARTS entity references)                  │
│  Owl Analytics Dashboards (ARTS-compliant metrics)             │
│  Goose BTC Payments (ARTS transaction signing)                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Principle: ARTS as "Rosetta Stone"

**ARTS POSlog 6.0 is the universal language of retail transactions.**

Every vendor's proprietary format maps to ARTS entities:
- Square `payment` → ARTS `RetailTransaction`
- Shopify `order` → ARTS `RetailTransaction`
- Micros `check` → ARTS `RetailTransaction`
- Dutchie `receipt` → ARTS `RetailTransaction`

**Once translated to ARTS:**
- Fox case management references ARTS `transaction_id`, `operator_id`, `line_item_sequence`
- Fraud queries join ARTS `transactions`, `line_items`, `tenders`
- Owl dashboards aggregate ARTS `transaction_totals`, `tax`, `discounts`
- Export to partners uses ARTS XML (industry-standard)

---

## Translation Layer: Vendor Parser Interface

### Base Parser Contract

Every vendor parser implements this interface:

```python
from abc import ABC, abstractmethod
from typing import Dict, Any
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass
class ARTSTransaction:
    """Canonical ARTS POSlog 6.0 Transaction"""
    # POSLogTransaction level
    transaction_id: str
    source_system: str  # 'square', 'shopify', 'micros', etc.
    cancel_flag: bool
    training_mode_flag: bool
    offline_flag: bool
    retail_store_id: str
    workstation_id: str
    till_id: str | None
    sequence_number: int
    business_day_date: datetime.date
    begin_datetime: datetime
    end_datetime: datetime
    operator_id: str | None
    currency_code: str

    # RetailTransaction level
    poslog_version: str = "6.0"
    transaction_type_code: str  # 'Sale', 'Return', etc.
    transaction_status: str  # 'COMPLETED', 'CANCELLED', 'SUSPENDED'
    outside_sales_flag: bool = False
    split_check_flag: bool = False
    special_order_number: str | None = None
    receipt_datetime: datetime | None = None
    item_count: int | None = None

    # Nested structures
    line_items: list[Dict[str, Any]]
    totals: list[Dict[str, Any]]
    tenders: list[Dict[str, Any]]
    customer: Dict[str, Any] | None = None
    loyalty_account: Dict[str, Any] | None = None
    associates: list[Dict[str, Any]] = None

    # Fraud detection fields (extended ARTS)
    device_id: str | None = None
    device_name: str | None = None
    employee_id: str | None = None
    card_brand: str | None = None
    card_last_4: str | None = None
    card_entry_method: str | None = None
    card_fingerprint: str | None = None
    cvv_status: str | None = None
    avs_status: str | None = None
    risk_level: str | None = None

    # Metadata
    raw_data: Dict[str, Any]  # Original vendor payload (JSONB)
    parsed_at: datetime
    parser_version: str


class POSParser(ABC):
    """Base class for all POS system parsers"""

    @abstractmethod
    def parse_to_arts_transaction(self, raw_payload: Dict[str, Any]) -> ARTSTransaction:
        """
        Parse vendor-specific transaction format to ARTS POSlog 6.0 schema.

        Args:
            raw_payload: Vendor's native transaction format (JSON/XML as dict)

        Returns:
            ARTSTransaction with all fields mapped to ARTS standard

        Raises:
            ParserError: If required fields missing or format invalid
        """
        pass

    @abstractmethod
    def validate_payload(self, raw_payload: Dict[str, Any]) -> bool:
        """Validate vendor payload structure before parsing"""
        pass

    def get_parser_version(self) -> str:
        """Return parser version for audit trail"""
        return "1.0.0"

    def get_source_system(self) -> str:
        """Return source system identifier"""
        return self.__class__.__name__.replace("Parser", "").lower()
```

---

## Vendor-Specific Parsers

### 1. Square Parser (Current - MVP)

**Input:** Square Payment webhook (JSON)
**Key Mappings:**
```python
class SquareParser(POSParser):
    def parse_to_arts_transaction(self, payment: Dict) -> ARTSTransaction:
        return ARTSTransaction(
            # POSLogTransaction
            transaction_id=payment['id'],
            source_system='square',
            cancel_flag=(payment['status'] == 'CANCELED'),
            training_mode_flag=False,  # Square doesn't have training mode
            offline_flag=False,
            retail_store_id=payment['location_id'],
            workstation_id=payment.get('device_details', {}).get('device_id'),
            till_id=None,  # Square doesn't expose till_id
            sequence_number=self._generate_sequence(payment),
            business_day_date=parse_date(payment['created_at']),
            begin_datetime=parse_datetime(payment['created_at']),
            end_datetime=parse_datetime(payment['updated_at']),
            operator_id=payment.get('employee_id'),
            currency_code=payment['amount_money']['currency'],

            # RetailTransaction
            transaction_type_code='Sale' if payment['amount_money']['amount'] > 0 else 'Return',
            transaction_status=self._map_square_status(payment['status']),
            special_order_number=payment.get('order_id'),
            receipt_datetime=parse_datetime(payment['updated_at']),
            item_count=self._count_line_items(payment),

            # Fraud fields (from Square)
            device_id=payment.get('device_details', {}).get('device_id'),
            device_name=payment.get('device_details', {}).get('device_name'),
            employee_id=payment.get('employee_id'),
            card_brand=payment.get('card_details', {}).get('card', {}).get('card_brand'),
            card_last_4=payment.get('card_details', {}).get('card', {}).get('last_4'),
            card_entry_method=payment.get('card_details', {}).get('entry_method'),
            card_fingerprint=payment.get('card_details', {}).get('card', {}).get('fingerprint'),
            cvv_status=payment.get('card_details', {}).get('cvv_status'),
            avs_status=payment.get('card_details', {}).get('avs_status'),
            risk_level=payment.get('risk_evaluation', {}).get('risk_level'),

            # Line items (fetch from order if available)
            line_items=self._parse_line_items(payment),
            totals=self._parse_totals(payment),
            tenders=self._parse_tenders(payment),
            customer=self._parse_customer(payment),

            # Metadata
            raw_data=payment,
            parsed_at=datetime.utcnow(),
            parser_version=self.get_parser_version()
        )
```

**Status:** ✅ Already implemented (v1), upgrade to v2 with full ARTS mapping in Sprint 1

---

### 2. Shopify Parser (E-commerce - High Priority)

**Input:** Shopify Order webhook (JSON)
**Key Differences from Square:**
- Shopify has `line_items[]` array natively (Square requires Order API call)
- Customer info is richer (email, phone, address)
- No `device_id` (online orders)
- Shipping/fulfillment data

**Mapping Strategy:**
```python
class ShopifyParser(POSParser):
    def parse_to_arts_transaction(self, order: Dict) -> ARTSTransaction:
        return ARTSTransaction(
            transaction_id=str(order['id']),
            source_system='shopify',
            cancel_flag=(order.get('cancelled_at') is not None),
            training_mode_flag=False,
            offline_flag=False,
            retail_store_id=order.get('location_id', 'online'),
            workstation_id='shopify-web',  # Online order
            till_id=None,
            sequence_number=order['order_number'],
            business_day_date=parse_date(order['created_at']),
            begin_datetime=parse_datetime(order['created_at']),
            end_datetime=parse_datetime(order.get('updated_at', order['created_at'])),
            operator_id=None,  # No employee for online orders
            currency_code=order['currency'],

            transaction_type_code='Sale',
            transaction_status='COMPLETED' if order['financial_status'] == 'paid' else 'SUSPENDED',
            outside_sales_flag=True,  # E-commerce = outside sales
            item_count=sum(item['quantity'] for item in order['line_items']),

            # Line items (native in Shopify)
            line_items=self._parse_shopify_line_items(order['line_items']),
            totals=self._parse_shopify_totals(order),
            tenders=self._parse_shopify_payments(order['payment_details']),
            customer=self._parse_shopify_customer(order.get('customer')),

            # No fraud fields (online, no card details exposed)
            device_id=None,
            card_entry_method='ECOMMERCE',

            raw_data=order,
            parsed_at=datetime.utcnow(),
            parser_version=self.get_parser_version()
        )
```

**Priority:** HIGH - E-commerce is huge market for Canary (online fraud, return abuse)

---

### 3. Oracle Micros (Simphony) Parser (Enterprise Restaurant - High Priority)

**Input:** Micros XML or proprietary format
**Key Differences:**
- XML format (not JSON)
- Table service data (covers, guests, courses)
- Split checks, guest checks
- Server/bartender tracking
- Kitchen timing data

**Mapping Strategy:**
```python
class MicrosParser(POSParser):
    def parse_to_arts_transaction(self, check: Dict) -> ARTSTransaction:
        """
        Micros 'check' = ARTS 'transaction'
        Note: Micros XML → parse to dict first
        """
        return ARTSTransaction(
            transaction_id=check['CheckNum'],
            source_system='micros',
            cancel_flag=(check['CheckStatus'] == 'Void'),
            training_mode_flag=(check.get('TrainingMode') == '1'),
            offline_flag=False,
            retail_store_id=check['RVCNum'],  # Revenue Center
            workstation_id=check['WorkstationNum'],
            till_id=check.get('EmpNum'),  # Employee = till in Micros
            sequence_number=int(check['CheckNum']),
            business_day_date=parse_date(check['BusinessDate']),
            begin_datetime=parse_datetime(check['CheckOpenTime']),
            end_datetime=parse_datetime(check['CheckCloseTime']),
            operator_id=check['EmpNum'],
            currency_code='USD',  # Micros often doesn't include currency

            transaction_type_code='Sale',
            transaction_status='COMPLETED' if check['CheckStatus'] == 'Closed' else 'SUSPENDED',
            split_check_flag=(check.get('SplitCheckFlag') == '1'),
            item_count=len(check.get('DetailLines', [])),

            # Hospitality-specific
            line_items=self._parse_micros_detail_lines(check['DetailLines']),
            totals=self._parse_micros_totals(check['Totals']),
            tenders=self._parse_micros_tenders(check['Tenders']),

            # Micros-specific extensions (store in raw_data)
            raw_data={
                **check,
                'TableNum': check.get('TableNum'),
                'GuestCount': check.get('GuestCount'),
                'ServerName': check.get('ServerName')
            },
            parsed_at=datetime.utcnow(),
            parser_version=self.get_parser_version()
        )
```

**Priority:** HIGH - Enterprise restaurant market, high fraud risk (comps, voids, employee meals)

---

### 4. NCR Aloha Parser (Restaurant - Medium Priority)

**Input:** Aloha XML/CSV export
**Similar to Micros but different field names**

**Priority:** MEDIUM - Competing with Micros in restaurant space

---

### 5. Clover Parser (SMB Retail - High Priority)

**Input:** Clover Order JSON (very similar to Square)
**Key Differences:**
- `lineItems` array structure different from Square
- Clover has native inventory tracking
- Employee management built-in

**Priority:** HIGH - Direct Square competitor, easy to port existing customers

---

### 6. Toast Parser (Restaurant - High Priority)

**Input:** Toast Order JSON
**Key Differences:**
- Table service focus
- Kitchen routing data
- Tip/gratuity tracking
- Delivery integration

**Priority:** HIGH - Major restaurant POS, high fraud risk

---

### 7. Lightspeed Parser (Retail/Restaurant - Medium Priority)

**Input:** Lightspeed Sale JSON
**Priority:** MEDIUM - Popular in Canada/EU

---

### 8. Cannabis POS Parsers (Dutchie, Cova, Flowhub, Treez)

**Input:** Cannabis-specific JSON with METRC fields
**Key Differences:**
- `metrc_package_uid` on every line item
- Customer purchase limits
- ID verification data
- Potency (THC/CBD mg)

**Mapping Strategy:**
```python
class DutchieParser(POSParser):
    def parse_to_arts_transaction(self, receipt: Dict) -> ARTSTransaction:
        arts_txn = ARTSTransaction(
            transaction_id=receipt['id'],
            source_system='dutchie',
            retail_store_id=receipt['facility_id'],
            # ... standard ARTS fields ...

            # Cannabis extensions (store in raw_data)
            raw_data={
                **receipt,
                'metrc_packages': receipt.get('metrc_packages', []),
                'customer_type': receipt.get('customer_type'),  # 'recreational' or 'medical'
                'id_verified': receipt.get('id_verified'),
                'purchase_limits': receipt.get('purchase_limits')
            }
        )

        # Add cannabis-specific line item fields
        for item in arts_txn.line_items:
            item['metrc_package_uid'] = receipt_item.get('metrc_package_uid')
            item['thc_mg'] = receipt_item.get('thc_mg')
            item['cbd_mg'] = receipt_item.get('cbd_mg')

        return arts_txn
```

**Priority:** HIGH - Cannabis vertical (per Risk Dictionary)

---

## Parser Registry & Auto-Detection

```python
class ParserRegistry:
    """Central registry of all vendor parsers"""

    _parsers = {
        'square': SquareParser(),
        'shopify': ShopifyParser(),
        'micros': MicrosParser(),
        'ncr': NCRParser(),
        'clover': CloverParser(),
        'toast': ToastParser(),
        'dutchie': DutchieParser(),
        'cova': CovaParser(),
        'flowhub': FlowhubParser(),
        # ... register all parsers
    }

    @classmethod
    def get_parser(cls, source_system: str) -> POSParser:
        """Get parser for a given source system"""
        if source_system not in cls._parsers:
            raise ValueError(f"No parser registered for '{source_system}'")
        return cls._parsers[source_system]

    @classmethod
    def auto_detect_parser(cls, raw_payload: Dict) -> POSParser:
        """Auto-detect source system from payload structure"""
        # Check for vendor-specific signatures
        if 'payment' in raw_payload and 'location_id' in raw_payload:
            return cls.get_parser('square')
        elif 'order' in raw_payload and 'line_items' in raw_payload:
            return cls.get_parser('shopify')
        elif 'CheckNum' in raw_payload and 'RVCNum' in raw_payload:
            return cls.get_parser('micros')
        # ... more detection logic
        else:
            raise ValueError("Could not auto-detect source system")
```

---

## Ingestion Pipeline

```python
class TransactionIngestionService:
    """Service to ingest vendor transactions and persist to Canary DB"""

    def ingest_transaction(self, source_system: str, raw_payload: Dict) -> int:
        """
        Ingest a transaction from any POS system.

        Returns: Canary transaction_id
        """
        # 1. Get appropriate parser
        parser = ParserRegistry.get_parser(source_system)

        # 2. Validate payload
        if not parser.validate_payload(raw_payload):
            raise ValidationError(f"Invalid {source_system} payload")

        # 3. Parse to ARTS schema
        arts_txn = parser.parse_to_arts_transaction(raw_payload)

        # 4. Persist to DB (ARTS-compliant schema)
        txn_id = self._persist_arts_transaction(arts_txn)

        # 5. Trigger fraud detection
        self._run_fraud_detection(txn_id)

        return txn_id

    def _persist_arts_transaction(self, arts_txn: ARTSTransaction) -> int:
        """Persist ARTS transaction to canary_app.transactions table"""
        sql = """
        INSERT INTO transactions (
            external_id, source_system, cancel_flag, training_mode_flag,
            retail_store_id, workstation_id, operator_id, currency_code,
            transaction_type_code, transaction_status, begin_datetime,
            end_datetime, device_id, card_fingerprint, cvv_status,
            avs_status, risk_level, raw_data, created_at
        ) VALUES (
            %(transaction_id)s, %(source_system)s, %(cancel_flag)s,
            %(training_mode_flag)s, %(retail_store_id)s, %(workstation_id)s,
            %(operator_id)s, %(currency_code)s, %(transaction_type_code)s,
            %(transaction_status)s, %(begin_datetime)s, %(end_datetime)s,
            %(device_id)s, %(card_fingerprint)s, %(cvv_status)s,
            %(avs_status)s, %(risk_level)s, %(raw_data)s, NOW()
        )
        RETURNING id
        """

        result = db.execute(sql, arts_txn.__dict__)
        return result['id']
```

---

## Priority: Parser Development Roadmap

### Sprint 1-2: Foundation (Current)
- ✅ **SquareParser v1** (already exists)
- 🔄 **SquareParser v2** (upgrade to full ARTS compliance - 22+ fields)
- ✅ **ParserRegistry** (base classes, auto-detection)

### Sprint 3-4: SMB Retail (Next 2 months)
- **ShopifyParser** (e-commerce fraud detection)
- **CloverParser** (Square alternative)
- **LightspeedParser** (retail)

### Sprint 5-6: Enterprise Restaurant (Months 3-4)
- **MicrosParser** (Oracle Simphony)
- **ToastParser** (cloud restaurant)
- **NCRParser** (Aloha)

### Sprint 7-8: Cannabis Vertical (Months 5-6)
- **DutchieParser**
- **CovaParser**
- **FlowhubParser**
- **TreezParser**

### Sprint 9+: Long Tail (Months 6+)
- Revel, SpotOn, Vend, Heartland, etc. (on-demand based on customer needs)

---

## Benefits of This Architecture

### 1. Industry Credibility
- **"ARTS POSlog 6.0 Compliant"** on marketing materials
- RFPs with ARTS requirements: ✅ Canary qualifies
- NRF/RILA conference credibility

### 2. Future-Proof
- New POS integration = 50-200 lines of parser code (not database migration)
- Internal analytics/Fox never change (always query ARTS schema)
- Can add ARTS XML export for partner integrations (ALTO, Verisae, etc.)

### 3. Vendor-Agnostic
- Customer switches from Square → Clover? Same Canary queries work.
- Multi-location client with mixed POS? Unified analytics.

### 4. Regulatory Defense
- Cannabis: "Our system follows ARTS retail standards + METRC extensions"
- Enterprise audits: "ARTS-compliant data model per NRF specification"

### 5. Developer Experience
- New engineer onboards once: learn ARTS schema
- Fraud query library (SQL) works across all POS systems
- Fox case management: vendor-agnostic references

---

## Open Questions / Next Steps

### Questions for Jeffe:
1. **Priority POS systems?** Beyond Square, which should we tackle first? (Shopify? Micros? Cannabis?)
2. **Enterprise sales focus?** If targeting restaurants, Micros/Toast = high priority. If SMB retail, Shopify/Clover.
3. **Cannabis timing?** When do we want to launch cannabis vertical? (Determines Dutchie/Cova parser priority)

### Technical Tasks:
1. Finalize ARTS schema in PostgreSQL (migrate from current 10-field `transactions` to full ARTS)
2. Build `POSParser` base class + `ParserRegistry`
3. Upgrade `SquareParser` to v2 (22+ fields)
4. Write unit tests for parser contract
5. Design parser versioning strategy (for breaking changes)

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-17 | Tom | Initial multi-POS translation layer architecture |

---

**Status:** ✅ Architecture defined. Ready for Sprint 1 implementation (SquareParser v2 + base classes).

**Next Action:** Jeremy to implement `POSParser` base class, Tom to finalize ARTS PostgreSQL schema.
