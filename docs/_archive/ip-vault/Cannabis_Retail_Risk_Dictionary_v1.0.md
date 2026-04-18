---
type: research
domain: canary
status: active
created: 2026-03-19
updated: 2026-03-19
---

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]

# Cannabis Retail Risk Dictionary & Integration Spec
**Version:** 1.0
**Date:** February 17, 2026
**Author:** Tom (Systems Architect)
**Purpose:** Vertical-specific risk dictionary for cannabis dispensaries - domain knowledge, fraud patterns, POS integration requirements, and onboarding questionnaire

---

## Executive Summary

This document provides **vertical intelligence** for Canary LP to serve cannabis dispensaries as a loss prevention layer. Unlike general retail, cannabis has:
- **Regulatory compliance** (METRC/BioTrack seed-to-sale tracking)
- **Cash-heavy operations** (limited banking access)
- **High-value inventory** (premium flower, concentrates)
- **Purchase limits** (state-mandated per-customer tracking)
- **Unique fraud vectors** (employee diversion, package splitting, ghost sales)

**Strategic Positioning:** Canary LP integrates with **existing cannabis POS** (Dutchie, Cova, Flowhub, Treez) as a loss prevention layer - we don't replace the POS, we detect fraud/shrinkage in their transaction feeds.

---

## 1. Cannabis Retail Business Model

### 1.1 Operating Environment

**Regulatory Framework:**
- **METRC (Metric Tracking System):** Mandatory seed-to-sale tracking in 20+ states (CA, CO, MI, etc.)
- **BioTrack:** Alternative track-and-trace in some states (NM, IL, etc.)
- **State-specific rules:** Purchase limits, ID verification, product testing, packaging requirements

**Key Compliance Requirements:**
- Every cannabis product has a **METRC Package UID** (barcode/RFID tag)
- All sales must be reported to state system (real-time or daily batch)
- Purchase limits enforced: e.g., CA = 28.5g flower/day, 8g concentrate, 80,000mg edibles
- Patient vs. recreational limits (medical gets higher limits)
- Age verification (21+ recreational, 18+ medical with card)

**Financial Constraints:**
- **280E tax code:** No business deductions except cost of goods
- **Limited banking:** Many dispensaries are cash-heavy (some use compliant processors like POSaBIT, PayQwick)
- **High shrinkage risk:** Cash + high-value product = major LP challenge

### 1.2 Cannabis Product Taxonomy

Different from general retail - products classified by:
- **Category:** Flower, pre-rolls, vapes, concentrates, edibles, topicals, accessories
- **Potency:** THC/CBD content (mg or %)
- **Weight/Count:** UOM varies by category (grams for flower, mg for edibles, units for pre-rolls)
- **Batch/Lot:** Traceability for recalls

**Example Product Structure:**
```json
{
  "metrc_package_uid": "1A4B2C3D4E5F6789",
  "sku": "FLOWER-BLUE-DREAM-1G",
  "name": "Blue Dream Flower - 1g",
  "category": "flower",
  "subcategory": "indica-dominant-hybrid",
  "brand": "West Coast Growers",
  "thc_percent": 20.5,
  "cbd_percent": 0.3,
  "weight_grams": 1.0,
  "price": 15.00,
  "cost": 6.00,
  "batch_number": "WCG-2024-001",
  "test_date": "2024-01-15",
  "harvest_date": "2024-01-10"
}
```

### 1.3 Sales Channels

- **In-store (retail counter):** Budtender-assisted sales
- **Online (pickup/delivery):** Menu websites (integrated with POS)
- **Curbside:** Order online, pickup without entering store
- **Delivery:** Must verify ID at doorstep, limited to local jurisdiction

---

## 2. Cannabis-Specific Fraud & Loss Patterns

### 2.1 Employee Theft & Diversion (HIGH RISK)

**Pattern:** Budtenders steal high-margin products or "sell" to friends without ringing up.

**Detection Signals:**
- **Ghost sales:** METRC package marked "sold" but no corresponding POS transaction
- **Off-hours activity:** Sales logged outside business hours
- **Employee discount abuse:** Excessive discounts applied by single budtender
- **Package split manipulation:** Break 3.5g package into (1g + 2.5g), sell 1g off-books
- **Return fraud:** Fake returns for products never sold
- **Tender mismatch:** Cash tendered < total (budtender pockets difference)

**Canary Detection Queries:**
```sql
-- Ghost sales: METRC sold packages with no POS match
SELECT m.package_uid, m.sold_datetime, m.budtender_id
FROM metrc_sales m
LEFT JOIN pos_transactions p ON m.receipt_number = p.receipt_id
WHERE p.receipt_id IS NULL
  AND m.sold_datetime > NOW() - INTERVAL '7 days';

-- Employee discount abuse: Single budtender >10% of discounts
SELECT employee_id, COUNT(*) as discount_count, SUM(discount_amount) as total_discounts
FROM pos_transactions
WHERE discount_amount > 0
  AND created_at > NOW() - INTERVAL '30 days'
GROUP BY employee_id
HAVING SUM(discount_amount) > (SELECT AVG(total) * 0.1 FROM pos_transactions WHERE discount_amount > 0);

-- Package split before sale (requires METRC package history)
SELECT parent_package_uid, COUNT(child_package_uid) as splits
FROM metrc_package_splits
WHERE split_datetime BETWEEN '08:00' AND '09:00'  -- Before store opens
GROUP BY parent_package_uid
HAVING COUNT(child_package_uid) > 3;  -- Excessive splitting
```

### 2.2 Customer Fraud

**Pattern:** Customers exceed purchase limits, use fake IDs, or collude with budtenders.

**Detection Signals:**
- **Multi-visit limit evasion:** Same customer ID scanning multiple times same day
- **Shared payment method:** Different customers using same card (straw buyers)
- **Fake ID:** Age doesn't match DOB on driver license scan
- **Card testing:** Small purchases with multiple cards (stolen card validation)

**Canary Detection Queries:**
```sql
-- Customer exceeding daily purchase limits (across visits)
SELECT customer_id, business_day_date,
       SUM(flower_grams) as total_flower,
       SUM(concentrate_grams) as total_concentrate
FROM pos_transactions
WHERE business_day_date = CURRENT_DATE
GROUP BY customer_id, business_day_date
HAVING SUM(flower_grams) > 28.5  -- CA limit
    OR SUM(concentrate_grams) > 8;

-- Card sharing: Same card, different customers
SELECT card_fingerprint, COUNT(DISTINCT customer_id) as unique_customers
FROM pos_transactions
WHERE card_fingerprint IS NOT NULL
  AND created_at > NOW() - INTERVAL '7 days'
GROUP BY card_fingerprint
HAVING COUNT(DISTINCT customer_id) > 3;
```

### 2.3 Inventory Shrinkage (METRC Discrepancies)

**Pattern:** Physical inventory doesn't match METRC system (theft, waste not logged, or data entry errors).

**Detection Signals:**
- **METRC vs. POS mismatch:** Packages marked sold in METRC but not in POS
- **Negative inventory:** POS shows more sold than METRC packages received
- **Waste not logged:** Products destroyed but not marked as waste in METRC
- **Cycle count discrepancies:** Physical count < system count

**Canary Detection:**
- Daily reconciliation: `metrc_packages.quantity_on_hand` vs. `pos_inventory.current_stock`
- Alert on >5% variance per product category
- Flag locations with chronic discrepancies (>10 alerts/month)

### 2.4 Point-of-Sale Manipulation

**Pattern:** Budtenders manipulate transactions to pocket cash or undercharge friends.

**Detection Signals:**
- **Void/cancel abuse:** Excessive voids by single budtender
- **Price override:** Manual price entry instead of scanning (undercharge)
- **Tender swap:** Ring up as cash, accept card (pocket difference)
- **No-sale opens:** Excessive cash drawer opens with no transaction

**Canary Detection Queries:**
```sql
-- Void abuse: Budtender >5 voids/day
SELECT employee_id, DATE(created_at) as date, COUNT(*) as void_count
FROM pos_transactions
WHERE status = 'VOIDED'
GROUP BY employee_id, DATE(created_at)
HAVING COUNT(*) > 5;

-- Price overrides: Manual pricing instead of barcode scan
SELECT employee_id, COUNT(*) as manual_price_count
FROM pos_line_items
WHERE entry_method = 'MANUAL'
  AND created_at > NOW() - INTERVAL '7 days'
GROUP BY employee_id
HAVING COUNT(*) > 20;
```

### 2.5 Cash Handling (HIGH RISK - Cash-Heavy Operations)

**Pattern:** Till shortages, skimming, or fake bills.

**Detection Signals:**
- **Till variance:** Expected cash vs. counted cash >$50 variance
- **Short change scams:** Customer claims incorrect change (budtender error or fraud)
- **Counterfeit bills:** Fake $20s, $50s, $100s (especially common in cannabis)
- **Drop variance:** Safe drops don't match expected amounts

**Canary Detection:**
- Track till variance by employee (flag >3 variances/month)
- Correlate large bills with transaction amounts (flag $100 bill for $15 purchase)

---

## 3. Cannabis POS Data Structure (Integration Requirements)

### 3.1 Core Transaction Schema (Extended Shopify-Style + Cannabis Fields)

Cannabis POS systems (Dutchie, Cova, Flowhub) use JSON transaction formats similar to Shopify but with METRC extensions:

```json
{
  "transaction_id": "uuid",
  "source": "pos",  // or "online", "delivery"
  "created_at": "2026-02-16T16:00:00Z",
  "location_id": "store-001",
  "location_name": "Green Valley Dispensary",
  "metrc_facility_license": "C11-0000001-LIC",

  "staff": {
    "id": "emp-123",
    "name": "Jane Doe",
    "metrc_user_key": "API-KEY-ABC123"  // METRC requires per-employee keys
  },

  "customer": {
    "id": "cust-456",
    "id_verified": true,
    "id_type": "driver_license",
    "dob": "1990-01-01",
    "customer_type": "recreational",  // or "medical"
    "purchase_limit_remaining": {
      "flower_grams": 28.5,
      "concentrate_grams": 8.0,
      "edibles_mg": 80000
    }
  },

  "items": [
    {
      "metrc_package_uid": "1A4B2C3D4E5F6789",
      "sku": "FLOWER-BLUE-DREAM-1G",
      "name": "Blue Dream Flower - 1g",
      "category": "flower",
      "quantity": 1,
      "unit_price": 15.00,
      "discount": 0,
      "subtotal": 15.00,
      "tax": 1.35,
      "total": 16.35,
      "potency": {
        "thc_percent": 20.5,
        "thc_mg": 205,
        "cbd_percent": 0.3
      },
      "batch": {
        "number": "WCG-2024-001",
        "harvest_date": "2024-01-10",
        "test_date": "2024-01-15"
      }
    }
  ],

  "totals": {
    "subtotal": 15.00,
    "discount": 0.00,
    "tax": 1.35,
    "excise_tax": 0.45,  // Cannabis-specific excise tax
    "sales_tax": 0.90,
    "grand_total": 16.35
  },

  "payment": {
    "tender_type": "cash",  // or "debit", "lightning" (rare)
    "amount_tendered": 20.00,
    "change": 3.65,
    "processor": null  // or "POSaBIT", "PayQwick"
  },

  "metrc_compliance": {
    "receipt_number": "REC-456",
    "synced_to_metrc": true,
    "metrc_sync_datetime": "2026-02-16T16:02:00Z",
    "packages_marked_sold": ["1A4B2C3D4E5F6789"]
  },

  "status": "completed",  // or "voided", "returned"
  "void_reason": null,
  "notes": null
}
```

### 3.2 Key Fields for Canary Integration

| Field | Purpose for LP | Priority |
|-------|----------------|----------|
| `metrc_package_uid` | Match POS sales to METRC packages (detect ghost sales) | **CRITICAL** |
| `staff.id` / `staff.metrc_user_key` | Employee fraud correlation | **CRITICAL** |
| `customer.id_verified` | Fake ID detection | **HIGH** |
| `customer.purchase_limit_remaining` | Limit evasion detection | **HIGH** |
| `items[].category` | Product-level shrinkage analysis | **MEDIUM** |
| `items[].potency.thc_mg` | High-value product theft tracking | **MEDIUM** |
| `payment.tender_type` | Cash handling anomalies | **HIGH** |
| `metrc_compliance.synced_to_metrc` | METRC discrepancy detection | **CRITICAL** |
| `status` (void/return) | Void abuse, return fraud | **HIGH** |

### 3.3 METRC Integration (For Canary LP)

Canary doesn't need to **push** to METRC (that's the POS's job), but we **pull** from METRC for reconciliation:

**METRC API Endpoints (Read-Only for Canary):**
- `GET /packages/v1/active` - All active packages in inventory
- `GET /sales/v1/receipts` - All sales receipts (for cross-check with POS)
- `GET /packages/v1/{id}` - Package details (including quantity sold)

**Canary Use Case:**
```python
# Daily reconciliation query
metrc_sales = metrc_client.get_receipts(facility_license, date=today)
pos_sales = db.query("SELECT * FROM pos_transactions WHERE business_day_date = %s", today)

# Find ghost sales: In METRC but not POS
metrc_receipt_ids = {s['ReceiptNumber'] for s in metrc_sales}
pos_receipt_ids = {s['receipt_id'] for s in pos_sales}
ghost_sales = metrc_receipt_ids - pos_receipt_ids

if ghost_sales:
    alert_fox_case(
        case_type="GHOST_SALE",
        severity="HIGH",
        description=f"{len(ghost_sales)} METRC sales missing from POS",
        evidence=ghost_sales
    )
```

---

## 4. Cannabis Dispensary Onboarding Questionnaire

**Purpose:** Capture client-specific risk factors, business model, and metadata to configure Canary's risk dictionary.

### 4.1 Business Profile

**Location & Licensing:**
- How many locations? (single vs. multi-store)
- State(s) of operation? (determines METRC vs. BioTrack)
- Facility license number(s)? (for METRC integration)
- Recreational, medical, or both?

**Sales Channels:**
- In-store retail? (yes/no)
- Online ordering? (pickup/delivery)
- Delivery radius? (for driver fraud monitoring)

**Operating Hours:**
- Store hours per location? (for after-hours detection)
- 24/7 operations? (some delivery-only)

### 4.2 POS System & Data Access

**Current POS:**
- Which POS? (Dutchie, Cova, Flowhub, Treez, other)
- API access available? (yes/no)
- API credentials: Who provides? (IT manager, POS vendor)
- Data format: JSON, XML, CSV export?
- Real-time webhooks or batch export? (daily/hourly)

**METRC Integration:**
- Do you sync METRC in real-time or daily batch?
- Who manages METRC integration? (POS vendor, in-house, third-party)
- METRC API keys: Per-employee or shared?
- Historical METRC data available? (last 90 days)

### 4.3 Team Structure

**Roles:**
- How many budtenders per location?
- How many managers/supervisors?
- Delivery drivers? (if applicable)
- Shift structure: Overlapping or solo shifts? (lone budtender = higher risk)

**Access Control:**
- Do budtenders have POS admin access? (should be NO)
- Who can process voids/returns? (managers only?)
- Who can apply discounts? (limit % by role?)

### 4.4 Known Risk Factors

**Past Incidents:**
- Have you experienced employee theft? (If yes: what happened?)
- Inventory shrinkage rate? (industry avg = 2-5%)
- METRC compliance issues? (state audits, fines)
- Cash handling problems? (till shortages, counterfeit bills)

**High-Risk Products:**
- Which products have highest margins? (usually concentrates, vapes)
- Which products are most stolen? (often pre-rolls, small edibles)
- Do you sell high-potency (>30% THC) products? (theft risk)

**Known Vulnerabilities:**
- Cash-only operations? (banking access?)
- Solo shifts? (no oversight = high risk)
- After-hours access? (cleaning crew, deliveries)

### 4.5 Compliance & Policies

**Company Policies:**
- Employee discount policy? (%, restrictions)
- Return/exchange policy? (timeframe, manager approval)
- Void/cancel policy? (who can void, max $ without approval)
- Till variance tolerance? (over/short acceptable range)

**Audit Trail:**
- Security cameras at registers? (yes/no)
- How long retained? (30/60/90 days)
- Cash drop frequency? (every $500? EOD only?)
- Inventory cycle count frequency? (weekly, monthly)

### 4.6 Canary Configuration Preferences

**Alert Thresholds:**
- Void count trigger: ___ voids/day by single budtender
- Discount threshold: ___% discount requires alert
- Till variance: $___+ over/short triggers alert
- METRC discrepancy: ___% variance acceptable

**Reporting Cadence:**
- Daily loss prevention summary? (yes/no)
- Weekly shrinkage report? (yes/no)
- Real-time alerts to: (email/SMS/Slack)

**Priority Concerns:**
- Rank your top 3 concerns: (employee theft, inventory shrinkage, cash handling, customer fraud, compliance violations)

---

## 5. Canary LP for Cannabis: Feature Set

### 5.1 Core Fraud Detection (Day 1)

- **Ghost sale detection:** METRC-to-POS reconciliation
- **Employee discount abuse:** Per-budtender discount % tracking
- **Void/cancel abuse:** Per-budtender void frequency
- **Till variance tracking:** Expected vs. actual cash per shift
- **After-hours activity:** Transactions outside business hours

### 5.2 Advanced Analytics (Phase 2)

- **Purchase limit evasion:** Multi-visit same-day tracking
- **Card sharing detection:** Same card fingerprint, different customers
- **Inventory shrinkage trends:** Category-level variance over time
- **High-risk product theft:** Premium concentrate/vape loss analysis
- **Shift-based anomaly detection:** Per-shift sales velocity vs. inventory usage

### 5.3 Compliance Support (Phase 3)

- **METRC audit prep:** Generate reconciliation reports (POS vs. METRC)
- **Package traceability:** Batch/lot tracking for recalls
- **ID verification audit trail:** Customer age verification logs
- **Tax calculation validation:** Verify excise + sales tax accuracy

### 5.4 Integrations (Phase 4)

- **POS APIs:** Dutchie, Cova, Flowhub, Treez (pull transaction data)
- **METRC API:** Read-only access (pull packages, receipts)
- **Security cameras:** CCTV timestamp correlation (via Fox module)
- **Accounting:** QuickBooks export (shrinkage, till variance)

---

## 6. Competitive Intel: Cannabis LP Landscape

**Existing Players:**
- **METRC itself:** Compliance tracking only, no LP features
- **POS vendors (Dutchie, Cova):** Basic inventory reporting, no LP focus
- **General LP tools (Verisae, ALTO):** Don't understand cannabis-specific patterns

**Canary's Advantage:**
- **Cannabis-native risk dictionary** (this doc)
- **METRC reconciliation** (ghost sale detection)
- **Multi-POS support** (not locked to one vendor)
- **Fox case management** (evidence chain for employee theft)
- **Bitcoin-native security** (optional Lightning for dispensary staff auth)

---

## 7. Implementation Roadmap

### Phase 1: Single-Location Pilot (4-6 weeks)
- Integrate with 1 POS (Dutchie or Cova)
- Ingest 90 days historical transaction data
- Configure 5 core fraud queries (ghost sales, void abuse, discount abuse, till variance, after-hours)
- Deploy Fox case management for incident tracking
- Weekly LP report to dispensary owner

### Phase 2: METRC Reconciliation (4-6 weeks)
- METRC API integration (read-only)
- Daily POS-to-METRC reconciliation job
- Ghost sale alerting
- Inventory shrinkage dashboard

### Phase 3: Multi-Location Scale (8 weeks)
- Support 5+ locations for same client
- Cross-location anomaly detection (employee moves between stores)
- Regional shrinkage benchmarking

### Phase 4: Multi-POS Expansion (12 weeks)
- Add Cova, Flowhub, Treez integrations
- Canonical cannabis transaction schema (ARTS-inspired)
- Vendor-agnostic LP platform

---

## 8. Pricing Model for Cannabis Vertical

**Recommended Pricing:**
- **Base:** $500-$1,000/month per location
- **METRC reconciliation:** +$200/month (compliance add-on)
- **Fox case management:** +$100/month (incident tracking)
- **Multi-location discount:** 10% off for 3+ locations

**Why Cannabis Pays More:**
- Higher shrinkage rates (2-5% vs. 1-2% general retail)
- Regulatory risk (METRC compliance failures = license suspension)
- Cash-heavy operations (higher internal theft risk)
- Product margins justify LP investment (30-50% margins)

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-17 | Tom | Initial cannabis vertical risk dictionary |

---

**Status:** ✅ Cannabis domain knowledge captured. Ready for pilot client onboarding.

**Next Action:** Identify 1 pilot dispensary (single-location, Dutchie/Cova POS, METRC state) for MVP integration.
