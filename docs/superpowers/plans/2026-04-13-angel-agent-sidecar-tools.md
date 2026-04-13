# Angel Agent Sidecar + Core Tools — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the Angel Agent sidecar container (port 8004) with 4 real estate data tools (parcel_lookup, listing_search, market_stats, listing_detail) so users can have data-backed conversations about the Palos Verdes peninsula.

**Architecture:** Raw ASGI sidecar (no web framework) with Anthropic SDK tool dispatch loop. Standalone SQLAlchemy engine for read-only DB access. Models imported from `cove.models` (Flask-SQLAlchemy). Pattern adapted from Canary QA Agent.

**Tech Stack:** Python 3.12, uvicorn, anthropic SDK, SQLAlchemy 2.0, Flask-SQLAlchemy (model metadata only), psycopg2, httpx, pytest

**Spec:** `docs/superpowers/specs/2026-04-13-angel-agent-sidecar-tools-design.md`

---

## Chunk 1: Foundation

### Task 1: Database Module

**Files:**
- Create: `Cove/cove/services/angel_agent/__init__.py`
- Create: `Cove/cove/services/angel_agent/db.py`

The sidecar needs its own SQLAlchemy engine because it runs outside Flask.
Import model metadata from `cove.extensions.db`, bind a standalone engine to it,
and provide a `get_session()` function.

- [ ] **Step 1: Create package init**

```python
# Cove/cove/services/angel_agent/__init__.py
"""Angel Agent sidecar — Claude-powered real estate assistant."""
```

- [ ] **Step 2: Write db.py**

```python
# Cove/cove/services/angel_agent/db.py
"""Standalone database access for the Angel Agent sidecar.

Creates its own SQLAlchemy engine from DATABASE_URL, independent of Flask.
Models are imported from cove.models which use Flask-SQLAlchemy's db.Model —
we bind the metadata to our standalone engine so ORM queries work.
"""

import os
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

logger = logging.getLogger(__name__)

_engine = None
_SessionLocal = None


def _init_engine():
    """Create engine and sessionmaker on first use."""
    global _engine, _SessionLocal
    if _engine is not None:
        return

    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL environment variable is required")

    _engine = create_engine(url, pool_size=5, pool_pre_ping=True)

    # Import all models so metadata knows about them
    import cove.models  # noqa: F401

    # Note: We do NOT set metadata.bind (removed in SQLAlchemy 2.0).
    # The sessionmaker(bind=_engine) is sufficient — ORM queries work
    # because the session carries the engine bind, not the metadata.

    _SessionLocal = sessionmaker(bind=_engine)
    logger.info("Angel Agent DB engine initialized: %s", url.split("@")[-1])


def get_session() -> Session:
    """Return a new DB session. Caller must close it."""
    _init_engine()
    return _SessionLocal()
```

- [ ] **Step 3: Verify imports work**

Run from Cove root (not in Docker — just checking import paths):
```bash
cd ~/GrowDirect/Cove && python3 -c "
import os; os.environ['DATABASE_URL'] = 'postgresql://growdirect:growdirect_dev@localhost:5432/cove'
from cove.services.angel_agent.db import get_session
s = get_session()
from cove.models.listing import Listing
count = s.query(Listing).count()
print(f'Listings: {count}')
s.close()
"
```
Expected: `Listings: 2368` (or similar non-zero count)

- [ ] **Step 4: Commit**

```bash
git add Cove/cove/services/angel_agent/__init__.py Cove/cove/services/angel_agent/db.py
git commit -m "feat(angel-agent): add standalone DB module for sidecar

GRO-461"
```

---

### Task 2: System Prompt

**Files:**
- Create: `Cove/cove/services/angel_agent/system_prompt.py`

Three-layer prompt: identity, knowledge context, tool instructions. Plus Fair
Housing guardrails and DRE disclosure.

- [ ] **Step 1: Write system_prompt.py**

```python
# Cove/cove/services/angel_agent/system_prompt.py
"""Three-layer system prompt for the Angel Agent."""

IDENTITY = """\
You are Angel, Angelique Lyle's AI real estate assistant for the Palos Verdes \
peninsula. Angelique is a Compass real estate agent \
(CA DRE# 01475592, 310.751.8335). You help prospective buyers and sellers \
understand the peninsula's neighborhoods, pricing, and market conditions \
using real MLS data.

You are knowledgeable, warm, and specific. You always lead with data — exact \
prices, days on market, number of transactions — never vague qualifiers like \
"great" or "desirable." When citing market data, mention the source period \
(e.g., "based on 61 closings in 2025").\
"""

# NOTE: MLS area mapping below must stay in sync with areas.py (tool resolution).
KNOWLEDGE_CONTEXT = """\
## Peninsula Geography

The Palos Verdes peninsula ("the Hill") is in the South Bay of Los Angeles \
County. It contains four cities and parts of a fifth:

- **Rancho Palos Verdes (RPV)** — largest city, broadest price range ($1.3M–$4M+)
- **Palos Verdes Estates (PVE)** — premium, fastest turnover, historic Malaga Cove
- **Rolling Hills Estates (RHE)** — equestrian community, retail hub
- **Rolling Hills (RH)** — guard-gated, equestrian mandate, ultra-premium
- **San Pedro** — most affordable peninsula-adjacent, harbor proximity

## MLS Area to Neighborhood Mapping

| MLS Area | Neighborhood | City |
|----------|-------------|------|
| 160 | Lunada Bay / Margate | PVE |
| 163 | Malaga Cove | PVE |
| 164 | Valmonte | PVE |
| 166 | Montemalaga | PVE |
| 165 | PV Drive North | RPV |
| 167 | PV Drive East | RPV |
| 170 | PV Drive South | RPV |
| 171 | Country Club | RPV |
| 173 | Los Verdes | RPV |
| 174 | La Cresta | RPV |
| 175 | Peninsula Center | RPV |
| 176 | Silver Spur | RPV |
| 177 | Eastview | RPV |
| 178 | Mira Catalina | RPV |
| 179 | South Shores | San Pedro |
| 180 | The Crest | RPV |
| 181 | West PV / Portuguese Bend | RPV |

## Market Overview

The peninsula median close price hovers around $2M with seasonal swings. \
Spring (Mar–Apr) is the fastest market (10–16 days DOM). Winter (Oct–Jan) is \
slowest (28–58 days). Volume peaks May–Jul at 50–64 closings/month. The market \
is supply-constrained — list-to-close ratios are at or above 100%.\
"""

TOOL_INSTRUCTIONS = """\
## Tools

You have access to tools that query real MLS data. Use them proactively — \
don't guess when you can look it up.

- **parcel_lookup**: Use when someone asks about a specific property by address, \
  APN, or MLS number. Returns a property card with beds/baths/sqft, pricing, and status.
- **listing_search**: Use when someone wants to browse listings — "show me homes \
  in Lunada Bay under $3M" or "what's active in RPV?" Returns up to 25 matches.
- **market_stats**: Use when someone asks about market conditions — "how's the \
  market in Valmonte?" or "what are prices doing?" Returns medians, DOM, inventory.
- **listing_detail**: Use when someone wants full detail on a specific listing \
  by MLS number. Returns everything including remarks and agent info.

Always cite specific numbers from tool results. Never fabricate data. If a tool \
returns no results, say so honestly.\
"""

FAIR_HOUSING = """\
## Fair Housing Compliance (MANDATORY)

You MUST comply with the Federal Fair Housing Act and California FEHA:

- NEVER steer based on race, color, religion, sex, national origin, familial \
  status, disability, sexual orientation, gender identity, or source of income.
- NEVER characterize a neighborhood as "safe," "dangerous," "good," "bad," \
  "family-friendly," "up-and-coming," or any demographic descriptor.
- Answer questions about schools, parks, and walkability with FACTUAL DATA ONLY \
  (test scores, park acreage, Walk Score numbers).
- If asked about neighborhood demographics, racial composition, or "what kind \
  of people live there," decline and redirect to census.gov.
- If asked whether a neighborhood is "safe," redirect to local crime statistics \
  at crimemapping.com or the RPV Sheriff's Station.

Include "CA DRE# 01475592" when discussing pricing, market conditions, or \
property recommendations.\
"""


def build_system_prompt() -> str:
    """Assemble the full system prompt from all layers."""
    return "\n\n".join([
        IDENTITY,
        KNOWLEDGE_CONTEXT,
        TOOL_INSTRUCTIONS,
        FAIR_HOUSING,
    ])
```

- [ ] **Step 2: Commit**

```bash
git add Cove/cove/services/angel_agent/system_prompt.py
git commit -m "feat(angel-agent): add 3-layer system prompt with Fair Housing guardrails

GRO-461"
```

---

### Task 3: Area Resolution Helper

**Files:**
- Create: `Cove/cove/services/angel_agent/areas.py`

Shared area alias → filter logic used by listing_search and market_stats.
Extracted to its own module to keep tools.py focused on tool handlers.

- [ ] **Step 1: Write areas.py**

```python
# Cove/cove/services/angel_agent/areas.py
"""Area name resolution for Angel Agent tools.

Maps user-friendly names and abbreviations to database values.
Used by listing_search (parcels.city / parcels.mls_area) and
market_stats (market_snapshots.area / market_snapshots.area_type).
"""

# City aliases → canonical city name (parcels.city)
CITY_ALIASES: dict[str, str] = {
    "rpv": "Rancho Palos Verdes",
    "rancho palos verdes": "Rancho Palos Verdes",
    "pve": "Palos Verdes Estates",
    "palos verdes estates": "Palos Verdes Estates",
    "rhe": "Rolling Hills Estates",
    "rolling hills estates": "Rolling Hills Estates",
    "rh": "Rolling Hills",
    "rolling hills": "Rolling Hills",
    "san pedro": "San Pedro",
}

# Neighborhood names → MLS area prefix (parcels.mls_area ILIKE 'prefix%')
NEIGHBORHOOD_ALIASES: dict[str, str] = {
    "lunada bay": "160",
    "margate": "160",
    "malaga cove": "163",
    "valmonte": "164",
    "montemalaga": "166",
    "monte malaga": "166",
    "pv drive north": "165",
    "pv dr north": "165",
    "pv drive east": "167",
    "pv dr east": "167",
    "pv drive south": "170",
    "pv dr south": "170",
    "country club": "171",
    "los verdes": "173",
    "la cresta": "174",
    "peninsula center": "175",
    "silver spur": "176",
    "eastview": "177",
    "mira catalina": "178",
    "south shores": "179",
    "the crest": "180",
    "west pv": "181",
    "portuguese bend": "181",
}

# Terms that mean "all peninsula"
PENINSULA_TERMS = {"peninsula", "pv", "palos verdes", "the hill", "all"}


def resolve_area(area: str) -> dict:
    """Resolve a user-provided area string to a filter spec.

    Returns a dict with one of:
        {"type": "peninsula"} — no area filter needed
        {"type": "city", "value": "Rancho Palos Verdes"}
        {"type": "mls_area", "value": "160"} — prefix for ILIKE
        {"type": "unknown", "value": "original input"}
    """
    normalized = area.strip().lower()

    if normalized in PENINSULA_TERMS:
        return {"type": "peninsula"}

    if normalized in CITY_ALIASES:
        return {"type": "city", "value": CITY_ALIASES[normalized]}

    if normalized in NEIGHBORHOOD_ALIASES:
        return {"type": "mls_area", "value": NEIGHBORHOOD_ALIASES[normalized]}

    # Try partial match on city names
    for alias, city in CITY_ALIASES.items():
        if normalized in alias or alias in normalized:
            return {"type": "city", "value": city}

    # Try partial match on neighborhood names
    for alias, prefix in NEIGHBORHOOD_ALIASES.items():
        if normalized in alias or alias in normalized:
            return {"type": "mls_area", "value": prefix}

    return {"type": "unknown", "value": area}
```

- [ ] **Step 2: Commit**

```bash
git add Cove/cove/services/angel_agent/areas.py
git commit -m "feat(angel-agent): add area resolution helper for tool queries

GRO-462"
```

---

## Chunk 2: Test Fixtures + Tool Implementations (TDD)

### Task 4: Test Fixtures

**Files:**
- Create: `Cove/tests/angel_agent/__init__.py`
- Create: `Cove/tests/angel_agent/conftest.py`

Seed data for tool tests: parcels, listings, market snapshots, listing events.
Uses Cove's existing app factory and DB session pattern.

- [ ] **Step 1: Create test package**

```python
# Cove/tests/angel_agent/__init__.py
```

- [ ] **Step 2: Write conftest.py with fixtures**

```python
# Cove/tests/angel_agent/conftest.py
"""Fixtures for Angel Agent tool tests.

Seeds parcels, listings, market snapshots, and listing events for testing
the 4 core tools: parcel_lookup, listing_search, market_stats, listing_detail.
"""

import os
import pytest
from datetime import date, datetime, timezone

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql://growdirect:growdirect_dev@localhost:5432/cove_test",
)

from cove import create_app
from cove.extensions import db as _db
from cove.models.parcel import Parcel
from cove.models.listing import Listing, ListingEvent
from cove.models.market_snapshot import MarketSnapshot


@pytest.fixture(scope="session")
def app():
    """Create test app once per session."""
    application = create_app("test")
    with application.app_context():
        _db.create_all()
        yield application
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope="function")
def db_session(app):
    """Per-test DB session with truncation cleanup."""
    with app.app_context():
        yield _db.session

        _db.session.rollback()
        for table in reversed(_db.metadata.sorted_tables):
            _db.session.execute(table.delete())
        _db.session.commit()
        _db.session.remove()


@pytest.fixture
def seed_parcels(db_session):
    """Seed 4 parcels across different cities and MLS areas."""
    parcels = [
        Parcel(
            apn="7573-006-008",
            address="1234 Granvia Altamira",
            street="Granvia Altamira",
            city="Rancho Palos Verdes",
            state="CA",
            zip_code="90275",
            mls_area="160 - Lunada Bay/Margate",
            bedrooms=3,
            bathrooms=2.0,
            sqft=1850,
            lot_size_sqft=7500,
            year_built=1965,
            property_type="Single Family Residence",
        ),
        Parcel(
            apn="7551-001-010",
            address="500 Via Almar",
            street="Via Almar",
            city="Palos Verdes Estates",
            state="CA",
            zip_code="90274",
            mls_area="164 - Valmonte",
            bedrooms=4,
            bathrooms=3.0,
            sqft=2400,
            lot_size_sqft=9000,
            year_built=1955,
            property_type="Single Family Residence",
        ),
        Parcel(
            apn="7588-020-005",
            address="100 Silver Spur Rd",
            street="Silver Spur Rd",
            city="Rolling Hills Estates",
            state="CA",
            zip_code="90274",
            mls_area="176 - Silver Spur",
            bedrooms=2,
            bathrooms=1.0,
            sqft=1200,
            lot_size_sqft=5000,
            year_built=1970,
            property_type="Condominium",
        ),
        # Parcel with no listing (standalone)
        Parcel(
            apn="7573-099-001",
            address="999 Crenshaw Blvd",
            street="Crenshaw Blvd",
            city="Rancho Palos Verdes",
            state="CA",
            zip_code="90275",
            mls_area="177 - Eastview",
            bedrooms=3,
            bathrooms=2.0,
            sqft=1600,
            lot_size_sqft=6000,
            year_built=1972,
            property_type="Single Family Residence",
        ),
    ]
    db_session.add_all(parcels)
    db_session.flush()
    return parcels


@pytest.fixture
def seed_listings(db_session, seed_parcels):
    """Seed 5 listings linked to parcels, plus 1 with NULL APN."""
    listings = [
        # Active in Lunada Bay
        Listing(
            mls_number="SB26-001",
            apn="7573-006-008",
            status="Active",
            list_price=2795000,
            list_date=date(2026, 4, 1),
            dom=12,
            listing_office="Compass",
            remarks="Beautiful ocean-view ranch in Lunada Bay.",
            hoa_fee=0,
            source="crmls_tp",
        ),
        # Closed in Valmonte
        Listing(
            mls_number="SB25-100",
            apn="7551-001-010",
            status="Closed",
            list_price=2595000,
            close_price=2500000,
            list_date=date(2025, 8, 1),
            close_date=date(2025, 9, 15),
            dom=45,
            listing_agent_name="Angelique Lyle",
            listing_office="Compass",
            buyer_agent_name="Other Agent",
            buyer_office="Keller Williams",
            remarks="Charming Valmonte home on tree-lined street.",
            hoa_fee=0,
            virtual_tour_url="https://example.com/tour/100",
            source="crmls_tp",
        ),
        # Active condo in RHE (low price)
        Listing(
            mls_number="SB26-050",
            apn="7588-020-005",
            status="Active",
            list_price=699000,
            list_date=date(2026, 3, 15),
            dom=29,
            listing_office="RE/MAX",
            remarks="Updated condo near shops.",
            hoa_fee=350,
            source="crmls_tp",
        ),
        # Closed in Lunada Bay (different price)
        Listing(
            mls_number="SB25-200",
            apn="7573-006-008",
            status="Closed",
            list_price=2900000,
            close_price=2850000,
            list_date=date(2025, 5, 1),
            close_date=date(2025, 6, 20),
            dom=50,
            source="crmls_tp",
        ),
        # Active with NULL APN (no parcel link)
        Listing(
            mls_number="SB26-999",
            apn=None,
            status="Active",
            list_price=1500000,
            list_date=date(2026, 4, 5),
            dom=8,
            listing_office="Coldwell Banker",
            source="crmls_tp",
        ),
    ]
    db_session.add_all(listings)
    db_session.flush()
    return listings


@pytest.fixture
def seed_events(db_session, seed_listings):
    """Seed listing events for the Valmonte closed listing."""
    events = [
        ListingEvent(
            mls_number="SB25-100",
            event_type="Price Chg",
            event_date=datetime(2025, 8, 20, tzinfo=timezone.utc),
            old_value="2695000",
            new_value="2595000",
            source="hot_sheet",
        ),
        ListingEvent(
            mls_number="SB25-100",
            event_type="Status Chg",
            event_date=datetime(2025, 9, 15, tzinfo=timezone.utc),
            old_value="Active",
            new_value="Closed",
            source="hot_sheet",
        ),
    ]
    db_session.add_all(events)
    db_session.flush()
    return events


@pytest.fixture
def seed_snapshots(db_session):
    """Seed market snapshots for tool tests."""
    snapshots = [
        # Monthly — Lunada Bay (most recent)
        MarketSnapshot(
            period_type="monthly",
            period_start=date(2026, 3, 1),
            period_end=date(2026, 3, 31),
            area="160 - Lunada Bay/Margate",
            area_type="mls_area",
            property_type="All",
            active_count=12,
            pending_count=2,
            closed_count=6,
            expired_count=0,
            new_listing_count=8,
            median_list_price=2795000,
            median_close_price=2560000,
            median_dom=7,
            median_ppsf=1027,
            inventory_months=2.0,
            list_to_close_ratio=1.018,
            yoy_median_price_change=-15.4,
            yoy_closed_count_change=0.0,
        ),
        # Monthly — RPV city level
        MarketSnapshot(
            period_type="monthly",
            period_start=date(2026, 3, 1),
            period_end=date(2026, 3, 31),
            area="Rancho Palos Verdes",
            area_type="city",
            property_type="All",
            active_count=45,
            pending_count=8,
            closed_count=25,
            expired_count=2,
            new_listing_count=30,
            median_list_price=2100000,
            median_close_price=1905000,
            median_dom=28,
            median_ppsf=805,
            inventory_months=1.8,
            list_to_close_ratio=0.99,
            yoy_median_price_change=-5.2,
            yoy_closed_count_change=8.7,
        ),
        # Monthly — peninsula-wide
        MarketSnapshot(
            period_type="monthly",
            period_start=date(2026, 3, 1),
            period_end=date(2026, 3, 31),
            area="Peninsula",
            area_type="peninsula",
            property_type="All",
            active_count=97,
            pending_count=15,
            closed_count=46,
            expired_count=3,
            new_listing_count=55,
            median_list_price=2200000,
            median_close_price=2017000,
            median_dom=16,
            median_ppsf=880,
            inventory_months=2.1,
            list_to_close_ratio=1.005,
            yoy_median_price_change=-10.4,
            yoy_closed_count_change=2.2,
        ),
    ]
    db_session.add_all(snapshots)
    db_session.flush()
    return snapshots
```

- [ ] **Step 3: Commit**

```bash
git add Cove/tests/angel_agent/__init__.py Cove/tests/angel_agent/conftest.py
git commit -m "test(angel-agent): add fixtures for tool tests

Seed parcels, listings, events, and market snapshots for TDD.
GRO-462"
```

---

### Task 5: parcel_lookup — Test + Implement

**Files:**
- Create: `Cove/tests/angel_agent/test_tools.py`
- Create: `Cove/cove/services/angel_agent/tools.py`

TDD: write failing tests first, then implement the handler.

- [ ] **Step 1: Write parcel_lookup tests**

```python
# Cove/tests/angel_agent/test_tools.py
"""Tests for Angel Agent tool handlers."""

import pytest


class TestParcelLookup:
    """parcel_lookup tool: APN, MLS#, and address search."""

    def test_by_apn_dashed(self, app, db_session, seed_parcels, seed_listings):
        from cove.services.angel_agent.tools import handle_parcel_lookup

        result = handle_parcel_lookup(db_session, {"query": "7573-006-008"})
        assert result["apn"] == "7573-006-008"
        assert result["address"] == "1234 Granvia Altamira"
        assert result["bedrooms"] == 3
        assert result["sqft"] == 1850
        # Should return the most recent listing (by list_date desc)
        assert result["mls_number"] == "SB26-001"
        assert "summary" in result

    def test_by_apn_stripped(self, app, db_session, seed_parcels, seed_listings):
        from cove.services.angel_agent.tools import handle_parcel_lookup

        result = handle_parcel_lookup(db_session, {"query": "7573006008"})
        assert result["apn"] == "7573-006-008"

    def test_by_mls_number(self, app, db_session, seed_parcels, seed_listings):
        from cove.services.angel_agent.tools import handle_parcel_lookup

        result = handle_parcel_lookup(db_session, {"query": "SB26-001"})
        assert result["mls_number"] == "SB26-001"
        assert result["status"] == "Active"
        assert result["list_price"] == 2795000
        assert result["bedrooms"] == 3  # From parcel join

    def test_by_address_fragment(self, app, db_session, seed_parcels, seed_listings):
        from cove.services.angel_agent.tools import handle_parcel_lookup

        result = handle_parcel_lookup(db_session, {"query": "Granvia"})
        assert result["address"] == "1234 Granvia Altamira"

    def test_no_match(self, app, db_session, seed_parcels, seed_listings):
        from cove.services.angel_agent.tools import handle_parcel_lookup

        result = handle_parcel_lookup(db_session, {"query": "nonexistent address xyz"})
        assert "No property found" in result["summary"]

    def test_parcel_no_listing(self, app, db_session, seed_parcels):
        """APN exists in parcels but has no listing — return parcel data only."""
        from cove.services.angel_agent.tools import handle_parcel_lookup

        result = handle_parcel_lookup(db_session, {"query": "7573-099-001"})
        assert result["apn"] == "7573-099-001"
        assert result["address"] == "999 Crenshaw Blvd"
        assert result["bedrooms"] == 3
        assert result.get("mls_number") is None

    def test_listing_no_parcel(self, app, db_session, seed_parcels, seed_listings):
        """Listing with NULL APN — return transaction data, no property chars."""
        from cove.services.angel_agent.tools import handle_parcel_lookup

        result = handle_parcel_lookup(db_session, {"query": "SB26-999"})
        assert result["mls_number"] == "SB26-999"
        assert result["list_price"] == 1500000
        assert result.get("bedrooms") is None
        assert result["has_parcel_record"] is False
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd ~/GrowDirect/Cove && python3 -m pytest tests/angel_agent/test_tools.py::TestParcelLookup -v 2>&1 | head -30
```
Expected: ImportError or ModuleNotFoundError for `handle_parcel_lookup`

- [ ] **Step 3: Implement parcel_lookup handler in tools.py**

```python
# Cove/cove/services/angel_agent/tools.py
"""Angel Agent tool definitions and handlers.

Each tool handler takes (db_session, params_dict) and returns a plain dict.
The execute_tool() dispatcher routes tool calls from the server's dispatch loop.
"""

import re
import logging
from datetime import date

from sqlalchemy.orm import Session

from cove.models.parcel import Parcel
from cove.models.listing import Listing

logger = logging.getLogger(__name__)

# --- APN regex patterns ---
APN_DASHED = re.compile(r"^\d{4}-\d{3}-\d{3}$")
APN_STRIPPED = re.compile(r"^\d{10}$")


def _normalize_apn(raw: str) -> str:
    """Convert stripped APN to dashed format: 7573006008 → 7573-006-008."""
    digits = re.sub(r"\D", "", raw)
    if len(digits) == 10:
        return f"{digits[:4]}-{digits[4:7]}-{digits[7:]}"
    return raw


def _build_property_card(parcel: Parcel | None, listing: Listing | None) -> dict:
    """Build a property card dict from a parcel and/or listing."""
    card: dict = {}

    if parcel:
        card["apn"] = parcel.apn
        card["address"] = parcel.address
        card["city"] = parcel.city
        card["bedrooms"] = parcel.bedrooms
        card["bathrooms"] = parcel.bathrooms
        card["sqft"] = parcel.sqft
        card["lot_sqft"] = parcel.lot_size_sqft
        card["year_built"] = parcel.year_built
        card["property_type"] = parcel.property_type
        card["has_parcel_record"] = True
    else:
        card["has_parcel_record"] = False

    if listing:
        card["mls_number"] = listing.mls_number
        card["status"] = listing.status
        card["list_price"] = listing.list_price
        card["close_price"] = listing.close_price
        card["dom"] = listing.dom
        card["list_date"] = str(listing.list_date) if listing.list_date else None
        card["last_sale_date"] = str(listing.close_date) if listing.close_date else None
        if not parcel:
            card["apn"] = listing.apn

    # Build summary
    parts = []
    if card.get("bedrooms") and card.get("bathrooms"):
        bath_str = int(card["bathrooms"]) if card["bathrooms"] == int(card["bathrooms"]) else card["bathrooms"]
        parts.append(f"{card['bedrooms']} bed / {bath_str} bath")
    if card.get("sqft"):
        parts.append(f"{card['sqft']:,} sqft")
    if card.get("city"):
        parts.append(f"in {card['city']}")
    if card.get("close_price"):
        parts.append(f"closed at ${card['close_price']:,.0f}")
    elif card.get("list_price"):
        parts.append(f"listed at ${card['list_price']:,.0f}")
    if card.get("status"):
        parts.append(f"({card['status']})")

    card["summary"] = " — ".join([", ".join(parts[:3])] + parts[3:]) if parts else "Property record"
    return card


def handle_parcel_lookup(session: Session, params: dict) -> dict:
    """Look up a property by APN, address fragment, or MLS number."""
    query = (params.get("query") or "").strip()
    if not query:
        return {"error": "invalid_input", "message": "query parameter is required"}

    # Detect query type
    if APN_DASHED.match(query) or APN_STRIPPED.match(query):
        # APN lookup
        apn = _normalize_apn(query)
        parcel = session.query(Parcel).filter(Parcel.apn == apn).first()
        listing = (
            session.query(Listing)
            .filter(Listing.apn == apn)
            .order_by(Listing.list_date.desc().nulls_last())
            .first()
        )
        if not parcel and not listing:
            return {"summary": f"No property found matching '{query}'", "results": []}
        return _build_property_card(parcel, listing)

    # MLS# lookup — alphanumeric with dash (e.g., SB26-001)
    if re.match(r"^[A-Za-z]{0,3}\d{2}-\d+$", query) or (query.isdigit() and 5 <= len(query) <= 9):
        listing = session.query(Listing).filter(Listing.mls_number == query).first()
        if not listing:
            return {"summary": f"No property found matching '{query}'", "results": []}
        parcel = listing.parcel
        return _build_property_card(parcel, listing)

    # Address fragment search
    parcels = (
        session.query(Parcel)
        .filter((Parcel.address + " " + Parcel.city).ilike(f"%{query}%"))
        .limit(5)
        .all()
    )

    if len(parcels) == 1:
        parcel = parcels[0]
        listing = (
            session.query(Listing)
            .filter(Listing.apn == parcel.apn)
            .order_by(Listing.list_date.desc().nulls_last())
            .first()
        )
        return _build_property_card(parcel, listing)

    if len(parcels) > 1:
        results = []
        for p in parcels:
            l = (
                session.query(Listing)
                .filter(Listing.apn == p.apn)
                .order_by(Listing.list_date.desc().nulls_last())
                .first()
            )
            results.append(_build_property_card(p, l))
        return {
            "summary": f"Multiple properties match '{query}' — showing {len(results)}",
            "results": results,
        }

    return {"summary": f"No property found matching '{query}'", "results": []}
```

- [ ] **Step 4: Run parcel_lookup tests**

```bash
cd ~/GrowDirect/Cove && python3 -m pytest tests/angel_agent/test_tools.py::TestParcelLookup -v
```
Expected: All 7 tests PASS

- [ ] **Step 5: Commit**

```bash
git add Cove/cove/services/angel_agent/tools.py Cove/tests/angel_agent/test_tools.py
git commit -m "feat(angel-agent): implement parcel_lookup tool with TDD

Handles APN (dashed/stripped), MLS#, and address fragment queries.
JOINs listing→parcel for property characteristics.
GRO-462"
```

---

### Task 6: listing_search — Test + Implement

**Files:**
- Modify: `Cove/tests/angel_agent/test_tools.py`
- Modify: `Cove/cove/services/angel_agent/tools.py`

- [ ] **Step 1: Write listing_search tests**

Append to `test_tools.py`:

```python
class TestListingSearch:
    """listing_search tool: area, price, beds, status, type filters."""

    def test_by_city(self, app, db_session, seed_parcels, seed_listings):
        from cove.services.angel_agent.tools import handle_listing_search

        result = handle_listing_search(db_session, {"area": "Rancho Palos Verdes"})
        assert result["total_matches"] >= 1
        # Should only return Active by default
        for r in result["results"]:
            assert r["status"] == "Active"

    def test_alias_rpv(self, app, db_session, seed_parcels, seed_listings):
        from cove.services.angel_agent.tools import handle_listing_search

        result = handle_listing_search(db_session, {"area": "RPV"})
        assert result["total_matches"] >= 1

    def test_peninsula_wide(self, app, db_session, seed_parcels, seed_listings):
        from cove.services.angel_agent.tools import handle_listing_search

        result = handle_listing_search(db_session, {"area": "peninsula"})
        # Should include listings from all cities
        assert result["total_matches"] >= 2

    def test_price_range(self, app, db_session, seed_parcels, seed_listings):
        from cove.services.angel_agent.tools import handle_listing_search

        result = handle_listing_search(
            db_session, {"area": "peninsula", "max_price": 1000000}
        )
        for r in result["results"]:
            assert r["list_price"] <= 1000000

    def test_closed_status(self, app, db_session, seed_parcels, seed_listings):
        from cove.services.angel_agent.tools import handle_listing_search

        result = handle_listing_search(
            db_session, {"area": "peninsula", "status": "Closed"}
        )
        for r in result["results"]:
            assert r["status"] == "Closed"

    def test_limit(self, app, db_session, seed_parcels, seed_listings):
        from cove.services.angel_agent.tools import handle_listing_search

        result = handle_listing_search(
            db_session, {"area": "peninsula", "limit": 2}
        )
        assert len(result["results"]) <= 2

    def test_min_price(self, app, db_session, seed_parcels, seed_listings):
        from cove.services.angel_agent.tools import handle_listing_search

        result = handle_listing_search(
            db_session, {"area": "peninsula", "min_price": 2000000}
        )
        for r in result["results"]:
            assert r["list_price"] >= 2000000

    def test_property_type_condo(self, app, db_session, seed_parcels, seed_listings):
        from cove.services.angel_agent.tools import handle_listing_search

        result = handle_listing_search(
            db_session, {"area": "peninsula", "property_type": "Condo"}
        )
        assert result["total_matches"] >= 1
        for r in result["results"]:
            assert "Condo" in r["property_type"]

    def test_output_includes_property_data(self, app, db_session, seed_parcels, seed_listings):
        """Results should include bedrooms/sqft from parcel join."""
        from cove.services.angel_agent.tools import handle_listing_search

        result = handle_listing_search(db_session, {"area": "Lunada Bay"})
        assert result["total_matches"] >= 1
        r = result["results"][0]
        assert "bedrooms" in r
        assert "sqft" in r
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd ~/GrowDirect/Cove && python3 -m pytest tests/angel_agent/test_tools.py::TestListingSearch -v 2>&1 | head -20
```
Expected: ImportError for `handle_listing_search`

- [ ] **Step 3: Implement listing_search handler**

Add to `tools.py`:

```python
from cove.services.angel_agent.areas import resolve_area


def handle_listing_search(session: Session, params: dict) -> dict:
    """Search listings by area, status, price range, beds, and property type."""
    area_input = params.get("area", "peninsula")
    status = params.get("status", "Active")
    min_price = params.get("min_price")
    max_price = params.get("max_price")
    min_beds = params.get("min_beds")
    property_type = params.get("property_type", "all")
    limit = min(params.get("limit", 10), 25)

    area = resolve_area(area_input)

    # Base query: listings joined to parcels
    q = session.query(Listing).outerjoin(Parcel, Listing.apn == Parcel.apn)

    # Status filter
    if status and status.lower() != "all":
        q = q.filter(Listing.status == status)

    # Area filter
    if area["type"] == "city":
        q = q.filter(Parcel.city == area["value"])
    elif area["type"] == "mls_area":
        q = q.filter(Parcel.mls_area.ilike(f"{area['value']} -%"))
    # "peninsula" and "unknown" — no area filter

    # Price filter
    if status and status.lower() == "closed":
        price_col = Listing.close_price
    else:
        price_col = Listing.list_price

    if min_price:
        q = q.filter(price_col >= min_price)
    if max_price:
        q = q.filter(price_col <= max_price)

    # Beds filter
    if min_beds:
        q = q.filter(Parcel.bedrooms >= min_beds)

    # Property type filter
    if property_type and property_type.lower() != "all":
        if property_type.upper() == "SFR":
            q = q.filter(Parcel.property_type.ilike("%Single Family%"))
        elif property_type.lower() == "condo":
            q = q.filter(Parcel.property_type.ilike("%Condo%"))

    # Sort
    if status and status.lower() == "closed":
        q = q.order_by(Listing.close_date.desc().nulls_last())
    else:
        q = q.order_by(Listing.list_date.desc().nulls_last())

    total = q.count()
    listings = q.limit(limit).all()

    results = []
    for listing in listings:
        parcel = listing.parcel
        entry = {
            "address": parcel.address if parcel else None,
            "city": parcel.city if parcel else None,
            "mls_number": listing.mls_number,
            "status": listing.status,
            "list_price": listing.list_price,
            "close_price": listing.close_price,
            "bedrooms": parcel.bedrooms if parcel else None,
            "bathrooms": parcel.bathrooms if parcel else None,
            "sqft": parcel.sqft if parcel else None,
            "dom": listing.dom,
            "property_type": parcel.property_type if parcel else None,
        }
        results.append(entry)

    area_label = area.get("value", area_input)
    price_desc = ""
    if max_price:
        price_desc = f" under ${max_price:,.0f}"
    elif min_price:
        price_desc = f" over ${min_price:,.0f}"

    summary = f"{total} {status.lower()} listing{'s' if total != 1 else ''} in {area_label}{price_desc}"

    return {"summary": summary, "total_matches": total, "results": results}
```

- [ ] **Step 4: Run listing_search tests**

```bash
cd ~/GrowDirect/Cove && python3 -m pytest tests/angel_agent/test_tools.py::TestListingSearch -v
```
Expected: All 9 tests PASS

- [ ] **Step 5: Commit**

```bash
git add Cove/cove/services/angel_agent/tools.py Cove/tests/angel_agent/test_tools.py
git commit -m "feat(angel-agent): implement listing_search tool with TDD

Filters by area (city/MLS area/peninsula), status, price, beds, property type.
JOINs to parcels for property data. Area alias resolution via areas.py.
GRO-462"
```

---

### Task 7: market_stats — Test + Implement

**Files:**
- Modify: `Cove/tests/angel_agent/test_tools.py`
- Modify: `Cove/cove/services/angel_agent/tools.py`

- [ ] **Step 1: Write market_stats tests**

Append to `test_tools.py`:

```python
class TestMarketStats:
    """market_stats tool: area + period_type → snapshot."""

    def test_monthly_mls_area(self, app, db_session, seed_snapshots):
        from cove.services.angel_agent.tools import handle_market_stats

        result = handle_market_stats(db_session, {"area": "Lunada Bay"})
        assert result["closed_count"] == 6
        assert result["median_close_price"] == 2560000
        assert result["median_dom"] == 7
        assert "summary" in result

    def test_city_area_type(self, app, db_session, seed_snapshots):
        """City name resolves to area_type='city'."""
        from cove.services.angel_agent.tools import handle_market_stats

        result = handle_market_stats(db_session, {"area": "RPV"})
        assert result["area"] == "Rancho Palos Verdes"
        assert result["closed_count"] == 25

    def test_peninsula_wide(self, app, db_session, seed_snapshots):
        from cove.services.angel_agent.tools import handle_market_stats

        result = handle_market_stats(db_session, {"area": "peninsula"})
        assert result["closed_count"] == 46

    def test_yoy_precomputed(self, app, db_session, seed_snapshots):
        """YoY values come from pre-computed columns, not derived."""
        from cove.services.angel_agent.tools import handle_market_stats

        result = handle_market_stats(db_session, {"area": "Lunada Bay"})
        assert result["yoy_median_price_change_pct"] == -15.4
        assert result["yoy_closed_count_change_pct"] == 0.0

    def test_no_snapshot(self, app, db_session, seed_snapshots):
        """Unknown area returns not_found error."""
        from cove.services.angel_agent.tools import handle_market_stats

        result = handle_market_stats(db_session, {"area": "Manhattan Beach"})
        assert "not_found" in result.get("error", "")
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd ~/GrowDirect/Cove && python3 -m pytest tests/angel_agent/test_tools.py::TestMarketStats -v 2>&1 | head -20
```

- [ ] **Step 3: Implement market_stats handler**

Add to `tools.py`:

```python
from cove.models.market_snapshot import MarketSnapshot


def handle_market_stats(session: Session, params: dict) -> dict:
    """Return market statistics for an area and period type."""
    area_input = params.get("area", "peninsula")
    period_type = params.get("period_type", "monthly")

    area = resolve_area(area_input)

    q = session.query(MarketSnapshot).filter(
        MarketSnapshot.period_type == period_type,
        MarketSnapshot.property_type == "All",
    )

    # Area + area_type filter
    if area["type"] == "peninsula":
        q = q.filter(MarketSnapshot.area_type == "peninsula")
    elif area["type"] == "city":
        q = q.filter(
            MarketSnapshot.area_type == "city",
            MarketSnapshot.area == area["value"],
        )
    elif area["type"] == "mls_area":
        q = q.filter(
            MarketSnapshot.area_type == "mls_area",
            MarketSnapshot.area.ilike(f"{area['value']} -%"),
        )
    else:
        # Unknown area — try exact match
        q = q.filter(MarketSnapshot.area.ilike(f"%{area_input}%"))

    # Most recent period
    snapshot = q.order_by(MarketSnapshot.period_start.desc()).first()

    if not snapshot:
        return {
            "error": "not_found",
            "message": f"No market data found for '{area_input}'",
        }

    # Format period label
    period_label = snapshot.period_start.strftime("%b %Y")
    area_label = snapshot.area
    # Clean up MLS area prefix for display
    if " - " in area_label:
        area_label = area_label.split(" - ", 1)[1]

    price_str = f"${snapshot.median_close_price:,.0f}" if snapshot.median_close_price else "N/A"
    summary = (
        f"{area_label} ({period_label}): median {price_str}, "
        f"{snapshot.median_dom} days on market, {snapshot.closed_count} closings"
    )

    return {
        "summary": summary,
        "area": area_label,
        "period": period_label,
        "period_type": snapshot.period_type,
        "active_count": snapshot.active_count,
        "closed_count": snapshot.closed_count,
        "median_list_price": snapshot.median_list_price,
        "median_close_price": snapshot.median_close_price,
        "median_dom": snapshot.median_dom,
        "median_ppsf": snapshot.median_ppsf,
        "inventory_months": snapshot.inventory_months,
        "list_to_close_ratio": snapshot.list_to_close_ratio,
        "yoy_median_price_change_pct": snapshot.yoy_median_price_change,
        "yoy_closed_count_change_pct": snapshot.yoy_closed_count_change,
    }
```

- [ ] **Step 4: Run market_stats tests**

```bash
cd ~/GrowDirect/Cove && python3 -m pytest tests/angel_agent/test_tools.py::TestMarketStats -v
```
Expected: All 5 tests PASS

- [ ] **Step 5: Commit**

```bash
git add Cove/cove/services/angel_agent/tools.py Cove/tests/angel_agent/test_tools.py
git commit -m "feat(angel-agent): implement market_stats tool with TDD

Queries market_snapshots with area_type resolution.
Uses pre-computed YoY columns. Filters on property_type='All'.
GRO-462"
```

---

### Task 8: listing_detail — Test + Implement

**Files:**
- Modify: `Cove/tests/angel_agent/test_tools.py`
- Modify: `Cove/cove/services/angel_agent/tools.py`

- [ ] **Step 1: Write listing_detail tests**

Append to `test_tools.py`:

```python
class TestListingDetail:
    """listing_detail tool: full record for a specific MLS number."""

    def test_full_detail(self, app, db_session, seed_parcels, seed_listings, seed_events):
        from cove.services.angel_agent.tools import handle_listing_detail

        result = handle_listing_detail(db_session, {"mls_number": "SB25-100"})
        assert result["mls_number"] == "SB25-100"
        assert result["status"] == "Closed"
        assert result["close_price"] == 2500000
        # Parcel data
        assert result["bedrooms"] == 4
        assert result["sqft"] == 2400
        # Extended fields
        assert result["remarks"] is not None
        assert result["listing_agent_name"] == "Angelique Lyle"
        assert result["listing_office"] == "Compass"
        assert result["buyer_office"] == "Keller Williams"
        # Events (ordered by event_date desc)
        assert len(result["events"]) == 2
        assert result["events"][0]["event_type"] == "Status Chg"  # 2025-09-15
        assert result["events"][1]["event_type"] == "Price Chg"   # 2025-08-20

    def test_not_found(self, app, db_session, seed_parcels, seed_listings):
        from cove.services.angel_agent.tools import handle_listing_detail

        result = handle_listing_detail(db_session, {"mls_number": "FAKE-999"})
        assert "not_found" in result.get("error", "")
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd ~/GrowDirect/Cove && python3 -m pytest tests/angel_agent/test_tools.py::TestListingDetail -v 2>&1 | head -15
```

- [ ] **Step 3: Implement listing_detail handler**

Add to `tools.py`:

```python
from cove.models.listing import ListingEvent


def handle_listing_detail(session: Session, params: dict) -> dict:
    """Return full detail for a specific MLS number, including events."""
    mls_number = (params.get("mls_number") or "").strip()
    if not mls_number:
        return {"error": "invalid_input", "message": "mls_number is required"}

    listing = session.query(Listing).filter(Listing.mls_number == mls_number).first()
    if not listing:
        return {"error": "not_found", "message": f"No listing found for MLS# {mls_number}"}

    parcel = listing.parcel
    card = _build_property_card(parcel, listing)

    # Extended fields
    card["remarks"] = listing.remarks
    card["hoa_fee"] = listing.hoa_fee
    card["virtual_tour_url"] = listing.virtual_tour_url
    card["listing_agent_name"] = listing.listing_agent_name
    card["listing_office"] = listing.listing_office
    card["buyer_agent_name"] = listing.buyer_agent_name
    card["buyer_office"] = listing.buyer_office
    card["architectural_style"] = parcel.architectural_style if parcel else None

    # Listing events
    events = (
        session.query(ListingEvent)
        .filter(ListingEvent.mls_number == mls_number)
        .order_by(ListingEvent.event_date.desc())
        .all()
    )
    card["events"] = [
        {
            "event_type": e.event_type,
            "event_date": str(e.event_date),
            "old_value": e.old_value,
            "new_value": e.new_value,
        }
        for e in events
    ]

    return card
```

- [ ] **Step 4: Run listing_detail tests**

```bash
cd ~/GrowDirect/Cove && python3 -m pytest tests/angel_agent/test_tools.py::TestListingDetail -v
```
Expected: All 2 tests PASS

- [ ] **Step 5: Run ALL tool tests**

```bash
cd ~/GrowDirect/Cove && python3 -m pytest tests/angel_agent/test_tools.py -v
```
Expected: All 23 tests PASS

- [ ] **Step 6: Commit**

```bash
git add Cove/cove/services/angel_agent/tools.py Cove/tests/angel_agent/test_tools.py
git commit -m "feat(angel-agent): implement listing_detail tool with TDD

Full listing record with parcel data, remarks, agent info, and event history.
GRO-462"
```

---

## Chunk 3: Tool Dispatch + Stubs, Server, Proxy

### Task 9: Tool Definitions + Dispatch + Stubs

**Files:**
- Modify: `Cove/cove/services/angel_agent/tools.py`

Add Anthropic-format tool definitions, the `execute_tool()` dispatcher, and
stub handlers for the 8 unimplemented tools.

- [ ] **Step 1: Add tool definitions and dispatcher to tools.py**

Add at the end of `tools.py`:

```python
# --- Tool Definitions (Anthropic API format) ---

TOOL_DEFINITIONS = [
    {
        "name": "parcel_lookup",
        "description": "Look up a property by APN (assessor parcel number), street address, or MLS listing number. Returns a property card with beds/baths/sqft, pricing, status, and location.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "APN (e.g. 7573-006-008), MLS number (e.g. SB26-001), or address fragment (e.g. 'Granvia Altamira')",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "listing_search",
        "description": "Search MLS listings by area, status, price range, bedrooms, and property type. Returns up to 25 matching listings sorted by date.",
        "input_schema": {
            "type": "object",
            "properties": {
                "area": {
                    "type": "string",
                    "description": "City (RPV, PVE, RHE, RH), neighborhood (Lunada Bay, Valmonte), or 'peninsula' for all areas",
                },
                "status": {
                    "type": "string",
                    "enum": ["Active", "Closed", "Pending", "all"],
                    "description": "Listing status filter. Default: Active",
                },
                "min_price": {"type": "integer", "description": "Minimum price filter"},
                "max_price": {"type": "integer", "description": "Maximum price filter"},
                "min_beds": {"type": "integer", "description": "Minimum bedrooms"},
                "property_type": {
                    "type": "string",
                    "enum": ["SFR", "Condo", "all"],
                    "description": "Property type filter. Default: all",
                },
                "limit": {"type": "integer", "description": "Max results (1-25). Default: 10"},
            },
            "required": ["area"],
        },
    },
    {
        "name": "market_stats",
        "description": "Get market statistics for an area — median prices, days on market, inventory, closings, and year-over-year trends.",
        "input_schema": {
            "type": "object",
            "properties": {
                "area": {
                    "type": "string",
                    "description": "City, neighborhood, or 'peninsula' for all areas",
                },
                "period_type": {
                    "type": "string",
                    "enum": ["monthly", "quarterly", "annual"],
                    "description": "Aggregation period. Default: monthly",
                },
            },
            "required": ["area"],
        },
    },
    {
        "name": "listing_detail",
        "description": "Get full detail for a specific MLS listing including remarks, agent info, HOA fees, and price/status change history.",
        "input_schema": {
            "type": "object",
            "properties": {
                "mls_number": {
                    "type": "string",
                    "description": "MLS listing number (e.g. SB26-001)",
                },
            },
            "required": ["mls_number"],
        },
    },
    # --- Stub tools (not yet implemented) ---
    {
        "name": "parcel_history",
        "description": "Ownership and transaction history for a property (coming soon).",
        "input_schema": {
            "type": "object",
            "properties": {"apn": {"type": "string"}},
            "required": ["apn"],
        },
    },
    {
        "name": "nearby_parcels",
        "description": "Find properties within a radius of a given location (coming soon).",
        "input_schema": {
            "type": "object",
            "properties": {"apn": {"type": "string"}, "radius_miles": {"type": "number"}},
            "required": ["apn"],
        },
    },
    {
        "name": "neighborhood_profile",
        "description": "Detailed neighborhood profile with character, amenities, and market position (coming soon).",
        "input_schema": {
            "type": "object",
            "properties": {"neighborhood": {"type": "string"}},
            "required": ["neighborhood"],
        },
    },
    {
        "name": "school_info",
        "description": "School ratings, feeder patterns, and enrollment for an area (coming soon).",
        "input_schema": {
            "type": "object",
            "properties": {"area": {"type": "string"}},
            "required": ["area"],
        },
    },
    {
        "name": "commute_estimate",
        "description": "Commute time estimates from a property to common destinations (coming soon).",
        "input_schema": {
            "type": "object",
            "properties": {"address": {"type": "string"}, "destination": {"type": "string"}},
            "required": ["address", "destination"],
        },
    },
    {
        "name": "cma_summary",
        "description": "Comparative market analysis summary for a property (coming soon).",
        "input_schema": {
            "type": "object",
            "properties": {"apn": {"type": "string"}},
            "required": ["apn"],
        },
    },
    {
        "name": "listing_strategy",
        "description": "Pricing and listing strategy recommendations based on market data (coming soon).",
        "input_schema": {
            "type": "object",
            "properties": {"apn": {"type": "string"}},
            "required": ["apn"],
        },
    },
    {
        "name": "capture_lead",
        "description": "Capture visitor contact information for follow-up (coming soon).",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "phone": {"type": "string"},
                "email": {"type": "string"},
            },
            "required": ["phone"],
        },
    },
]

# Handler registry
_HANDLERS = {
    "parcel_lookup": handle_parcel_lookup,
    "listing_search": handle_listing_search,
    "market_stats": handle_market_stats,
    "listing_detail": handle_listing_detail,
}

_STUB_TOOLS = {
    "parcel_history", "nearby_parcels", "neighborhood_profile",
    "school_info", "commute_estimate", "cma_summary",
    "listing_strategy", "capture_lead",
}


def get_tool_definitions() -> list[dict]:
    """Return tool definitions in Anthropic API format."""
    return TOOL_DEFINITIONS


def execute_tool(name: str, params: dict) -> dict:
    """Dispatch a tool call to its handler. Returns a dict result."""
    from cove.services.angel_agent.db import get_session

    if name in _STUB_TOOLS:
        return {
            "error": "not_implemented",
            "message": f"The {name} tool is coming soon. I can help with property lookups, listing searches, and market statistics right now.",
        }

    handler = _HANDLERS.get(name)
    if not handler:
        return {"error": "unknown_tool", "message": f"Unknown tool: {name}"}

    session = get_session()
    try:
        return handler(session, params)
    except Exception as e:
        logger.error("Tool %s failed: %s", name, e, exc_info=True)
        return {
            "error": "database_unavailable",
            "message": "I'm having trouble looking that up right now. Please try again in a moment.",
        }
    finally:
        session.close()
```

- [ ] **Step 2: Commit**

```bash
git add Cove/cove/services/angel_agent/tools.py
git commit -m "feat(angel-agent): add tool definitions, dispatcher, and 8 stubs

12 tool schemas registered. 4 implemented, 8 return not_implemented.
execute_tool() manages DB sessions and error handling.
GRO-461 GRO-462"
```

---

### Task 10: ASGI Server

**Files:**
- Create: `Cove/cove/services/angel_agent/server.py`

Raw ASGI app with /chat and /health endpoints, Anthropic SDK tool dispatch loop,
and in-memory rate limiting. Pattern adapted from Canary QA Agent.

- [ ] **Step 1: Write server.py**

```python
# Cove/cove/services/angel_agent/server.py
"""Angel Agent sidecar — raw ASGI app with Claude tool dispatch.

Endpoints:
    POST /chat  — chat with tool dispatch loop
    GET /health — health check with usage stats

Run: uvicorn cove.services.angel_agent.server:app --host 0.0.0.0 --port 8004
"""

import json
import logging
import os
import time
from typing import Any

logger = logging.getLogger(__name__)

# --- Config ---
DEFAULT_MODEL = os.getenv("ANGEL_AGENT_MODEL", "claude-sonnet-4-20250514")
MAX_TOKENS = 4096
MAX_TOOL_ITERATIONS = 10
MAX_TOOL_RESULT_BYTES = 8000
MAX_MESSAGES_PER_SESSION = 30
MAX_MESSAGES_PER_DAY = 150

# --- State ---
_start_time = time.time()
_session_counts: dict[str, int] = {}
_daily_counts: dict[str, int] = {}  # per session_id (proxy for per-user)
_daily_reset_day = 0


def _check_rate_limit(session_id: str) -> str | None:
    """Return an error message if rate limited, else None."""
    global _daily_reset_day

    # Reset daily counters at midnight (approximate)
    today = int(time.time() // 86400)
    if today != _daily_reset_day:
        _daily_counts.clear()
        _daily_reset_day = today

    session_count = _session_counts.get(session_id, 0)
    if session_count >= MAX_MESSAGES_PER_SESSION:
        return (
            f"Session limit reached ({MAX_MESSAGES_PER_SESSION} messages). "
            "Please start a new conversation."
        )
    daily_count = _daily_counts.get(session_id, 0)
    if daily_count >= MAX_MESSAGES_PER_DAY:
        return (
            f"Daily limit reached ({MAX_MESSAGES_PER_DAY} messages). "
            "Please try again tomorrow."
        )
    return None


async def handle_chat(data: dict) -> dict[str, Any]:
    """Process a chat request with tool dispatch loop."""
    messages = data.get("messages", [])
    session_id = data.get("session_id", "default")

    if not messages:
        return {"text": "No messages provided.", "tool_calls": [], "model": DEFAULT_MODEL, "usage": {}}

    # Rate limit check
    limit_msg = _check_rate_limit(session_id)
    if limit_msg:
        return {"text": limit_msg, "tool_calls": [], "model": DEFAULT_MODEL, "usage": {}}

    # Lazy imports to avoid import-time side effects
    from anthropic import Anthropic
    from cove.services.angel_agent.tools import get_tool_definitions, execute_tool
    from cove.services.angel_agent.system_prompt import build_system_prompt

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return {
            "text": "Angel is not configured yet. Please set ANTHROPIC_API_KEY.",
            "tool_calls": [],
            "model": DEFAULT_MODEL,
            "usage": {},
        }

    client = Anthropic(api_key=api_key)
    tool_definitions = get_tool_definitions()
    system_prompt = build_system_prompt()
    all_tool_calls: list[dict] = []

    # Tool dispatch loop
    for _ in range(MAX_TOOL_ITERATIONS):
        try:
            response = client.messages.create(
                model=DEFAULT_MODEL,
                max_tokens=MAX_TOKENS,
                system=system_prompt,
                tools=tool_definitions,
                messages=messages,
            )
        except Exception as e:
            logger.error("Anthropic API error: %s", e, exc_info=True)
            return {
                "text": "I'm having trouble connecting right now. Please try again.",
                "tool_calls": all_tool_calls,
                "model": DEFAULT_MODEL,
                "usage": {},
            }

        has_tool_use = any(b.type == "tool_use" for b in response.content)

        if not has_tool_use:
            text_parts = [b.text for b in response.content if b.type == "text"]
            break

        # Execute tool calls
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                logger.info("Angel → tool: %s(%s)", block.name, json.dumps(block.input, default=str)[:200])
                result = execute_tool(block.name, block.input)
                all_tool_calls.append({"tool": block.name, "input": block.input})

                result_str = json.dumps(result, default=str, ensure_ascii=False)
                if len(result_str) > MAX_TOOL_RESULT_BYTES:
                    result_str = result_str[:MAX_TOOL_RESULT_BYTES] + "... (truncated)"

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result_str,
                })

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})
    else:
        text_parts = ["I've reached the maximum number of lookups for this question. Could you try a simpler question?"]

    # Update rate limits
    _session_counts[session_id] = _session_counts.get(session_id, 0) + 1
    _daily_counts[session_id] = _daily_counts.get(session_id, 0) + 1

    return {
        "text": "\n".join(text_parts),
        "tool_calls": all_tool_calls,
        "model": DEFAULT_MODEL,
        "usage": {
            "session_remaining": MAX_MESSAGES_PER_SESSION - _session_counts.get(session_id, 0),
            "daily_remaining": MAX_MESSAGES_PER_DAY - _daily_count,
        },
    }


async def app(scope: dict, receive, send) -> None:
    """Minimal ASGI app — POST /chat and GET /health."""
    if scope["type"] != "http":
        return

    path = scope["path"]
    method = scope["method"]

    if method == "GET" and path == "/health":
        from cove.services.angel_agent.tools import get_tool_definitions

        body = json.dumps({
            "service": "angel-agent",
            "status": "healthy",
            "tools_loaded": len(get_tool_definitions()),
            "uptime_seconds": round(time.time() - _start_time),
            "daily_usage": sum(_daily_counts.values()),
            "daily_limit": MAX_MESSAGES_PER_DAY,
        }).encode()

        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": [[b"content-type", b"application/json"]],
        })
        await send({"type": "http.response.body", "body": body})
        return

    if method == "POST" and path == "/chat":
        # Read request body
        body = b""
        while True:
            message = await receive()
            body += message.get("body", b"")
            if not message.get("more_body", False):
                break

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            await _send_json(send, 400, {"error": "Invalid JSON"})
            return

        result = await handle_chat(data)
        await _send_json(send, 200, result)
        return

    # 404
    await _send_json(send, 404, {"error": "Not found"})


async def _send_json(send, status: int, data: dict) -> None:
    """Send a JSON response."""
    body = json.dumps(data, default=str, ensure_ascii=False).encode()
    await send({
        "type": "http.response.start",
        "status": status,
        "headers": [[b"content-type", b"application/json"]],
    })
    await send({"type": "http.response.body", "body": body})


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("ANGEL_AGENT_PORT", "8004"))
    logging.basicConfig(level=logging.INFO)
    logger.info("Angel Agent sidecar starting on port %d", port)
    uvicorn.run(
        "cove.services.angel_agent.server:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
    )
```

- [ ] **Step 2: Commit**

```bash
git add Cove/cove/services/angel_agent/server.py
git commit -m "feat(angel-agent): add ASGI server with tool dispatch loop

Raw ASGI app, POST /chat + GET /health. Anthropic SDK tool loop
with max 10 iterations and 8KB result truncation. In-memory rate limiting.
GRO-461"
```

---

### Task 11: Server Tests

**Files:**
- Create: `Cove/tests/angel_agent/test_server.py`

Test the ASGI app with mocked Anthropic API calls.

- [ ] **Step 1: Write server tests**

```python
# Cove/tests/angel_agent/test_server.py
"""Integration tests for the Angel Agent ASGI server."""

import json
import pytest
from unittest.mock import patch, MagicMock


@pytest.fixture
def send_request():
    """Helper to send ASGI requests to the server app."""
    from cove.services.angel_agent.server import app

    async def _send(method: str, path: str, body: dict | None = None):
        scope = {"type": "http", "method": method, "path": path}

        body_bytes = json.dumps(body).encode() if body else b""
        receive_called = False

        async def receive():
            nonlocal receive_called
            if not receive_called:
                receive_called = True
                return {"body": body_bytes, "more_body": False}
            return {"body": b"", "more_body": False}

        responses = []
        async def send(message):
            responses.append(message)

        await app(scope, receive, send)
        return responses

    return _send


@pytest.mark.asyncio
async def test_health_check(send_request):
    responses = await send_request("GET", "/health")
    assert responses[0]["status"] == 200
    body = json.loads(responses[1]["body"])
    assert body["service"] == "angel-agent"
    assert body["status"] == "healthy"
    assert "tools_loaded" in body
    assert body["tools_loaded"] == 12


@pytest.mark.asyncio
async def test_404(send_request):
    responses = await send_request("GET", "/nonexistent")
    assert responses[0]["status"] == 404


@pytest.mark.asyncio
async def test_chat_empty_messages(send_request):
    responses = await send_request("POST", "/chat", {"messages": []})
    assert responses[0]["status"] == 200
    body = json.loads(responses[1]["body"])
    assert "No messages" in body["text"]


@pytest.fixture(autouse=True)
def reset_rate_limits():
    """Reset rate limit state before each test."""
    from cove.services.angel_agent import server
    server._session_counts.clear()
    server._daily_counts.clear()
    yield
    server._session_counts.clear()
    server._daily_counts.clear()


@pytest.mark.asyncio
async def test_chat_returns_text(monkeypatch):
    """Mock Anthropic to return a simple text response."""
    from cove.services.angel_agent.server import handle_chat

    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

    mock_block = MagicMock()
    mock_block.type = "text"
    mock_block.text = "Hello! I'm Angel, your real estate assistant."

    mock_response = MagicMock()
    mock_response.content = [mock_block]

    with patch("anthropic.Anthropic") as MockAnthropic:
        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_response
        MockAnthropic.return_value = mock_client

        result = await handle_chat({
            "messages": [{"role": "user", "content": "Hello"}],
            "session_id": "test-text",
        })

    assert "Angel" in result["text"] or "Hello" in result["text"]
    assert result["tool_calls"] == []
    assert result["model"] is not None


@pytest.mark.asyncio
async def test_chat_tool_dispatch(monkeypatch):
    """Mock Anthropic to return a tool_use, then a text response."""
    from cove.services.angel_agent.server import handle_chat

    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

    # First response: tool_use
    tool_block = MagicMock()
    tool_block.type = "tool_use"
    tool_block.name = "parcel_history"  # stub tool
    tool_block.input = {"apn": "7573-006-008"}
    tool_block.id = "tool_123"

    first_response = MagicMock()
    first_response.content = [tool_block]

    # Second response: text
    text_block = MagicMock()
    text_block.type = "text"
    text_block.text = "That tool is coming soon."

    second_response = MagicMock()
    second_response.content = [text_block]

    with patch("anthropic.Anthropic") as MockAnthropic:
        mock_client = MagicMock()
        mock_client.messages.create.side_effect = [first_response, second_response]
        MockAnthropic.return_value = mock_client

        result = await handle_chat({
            "messages": [{"role": "user", "content": "Show me history"}],
            "session_id": "test-dispatch",
        })

    assert len(result["tool_calls"]) == 1
    assert result["tool_calls"][0]["tool"] == "parcel_history"
    assert "coming soon" in result["text"]


@pytest.mark.asyncio
async def test_rate_limit_session():
    """Session limit triggers after MAX_MESSAGES_PER_SESSION."""
    from cove.services.angel_agent import server

    server._session_counts["rate-test"] = server.MAX_MESSAGES_PER_SESSION

    result = await server.handle_chat({
        "messages": [{"role": "user", "content": "test"}],
        "session_id": "rate-test",
    })

    assert "Session limit" in result["text"]


@pytest.mark.asyncio
async def test_rate_limit_daily():
    """Daily limit triggers after MAX_MESSAGES_PER_DAY per session."""
    from cove.services.angel_agent import server

    server._daily_counts["daily-test"] = server.MAX_MESSAGES_PER_DAY

    result = await server.handle_chat({
        "messages": [{"role": "user", "content": "test"}],
        "session_id": "daily-test",
    })

    assert "Daily limit" in result["text"]
```

- [ ] **Step 2: Install pytest-asyncio if needed**

```bash
cd ~/GrowDirect/Cove && pip install pytest-asyncio 2>/dev/null; echo "done"
```

- [ ] **Step 3: Run server tests**

```bash
cd ~/GrowDirect/Cove && python3 -m pytest tests/angel_agent/test_server.py -v
```
Expected: All 7 tests PASS

- [ ] **Step 4: Commit**

```bash
git add Cove/tests/angel_agent/test_server.py
git commit -m "test(angel-agent): add ASGI server integration tests

Health check, 404, empty messages, mocked chat, tool dispatch, rate limiting.
GRO-461"
```

---

### Task 12: Update Flask Proxy

**Files:**
- Modify: `Cove/cove/angel/chat_routes.py`

Update the proxy to match the sidecar contract: `messages` (plural), 120s
timeout, passthrough response.

- [ ] **Step 1: Update chat_routes.py**

Replace the `chat()` function:

```python
@angel_chat_bp.route("/chat", methods=["POST"])
def chat():
    """Proxy a chat request to the angel-agent sidecar."""
    import httpx

    payload = request.get_json(silent=True)
    if not payload or not isinstance(payload.get("messages"), list) or not payload["messages"]:
        return jsonify({"error": "Missing or empty 'messages' array"}), 400

    try:
        with httpx.Client(timeout=120.0) as client:
            resp = client.post(
                f"{ANGEL_AGENT_URL}/chat",
                json=payload,
            )
            resp.raise_for_status()
            return jsonify(resp.json()), resp.status_code
    except httpx.ConnectError:
        current_app.logger.warning("Angel agent sidecar unreachable at %s", ANGEL_AGENT_URL)
        return jsonify({"error": "Chat service unavailable"}), 503
    except httpx.HTTPStatusError as exc:
        current_app.logger.error("Angel agent error: %s", exc)
        return jsonify({"error": "Chat service error"}), 502
```

- [ ] **Step 2: Commit**

```bash
git add Cove/cove/angel/chat_routes.py
git commit -m "fix(angel-agent): update proxy to messages array + 120s timeout

Contract change: 'message' (singular) → 'messages' (array).
Timeout: 30s → 120s for multi-turn tool dispatch.
GRO-461"
```

---

## Chunk 4: Docker + Smoke Test

### Task 13: Dockerfile

**Files:**
- Create: `Cove/Dockerfile.angel-agent`

- [ ] **Step 1: Write Dockerfile**

```dockerfile
# Cove/Dockerfile.angel-agent
# Angel Agent sidecar — Claude-powered real estate assistant
# Port 8004, read-only DB access, no Flask HTTP server

FROM python:3.12-slim

WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir \
    uvicorn \
    anthropic \
    sqlalchemy \
    flask-sqlalchemy \
    psycopg2-binary

# Copy only what the sidecar needs
COPY cove/__init__.py cove/__init__.py
COPY cove/extensions.py cove/extensions.py
COPY cove/models/ cove/models/
COPY cove/services/__init__.py cove/services/__init__.py
COPY cove/services/angel_agent/ cove/services/angel_agent/

EXPOSE 8004

CMD ["uvicorn", "cove.services.angel_agent.server:app", "--host", "0.0.0.0", "--port", "8004"]
```

- [ ] **Step 2: Commit**

```bash
git add Cove/Dockerfile.angel-agent
git commit -m "feat(angel-agent): add Dockerfile for sidecar container

Python 3.12-slim, minimal deps, copies only models + agent code.
GRO-461"
```

---

### Task 14: Docker Compose

**Files:**
- Modify: `Cove/devops/docker-compose.yml`

Read the file first, then add the angel-agent service.

- [ ] **Step 1: Read current docker-compose.yml**

```bash
cat ~/GrowDirect/Cove/devops/docker-compose.yml
```

- [ ] **Step 2: Add angel-agent service**

Add after the existing services (before `networks:`):

```yaml
  angel-agent:
    image: cove-angel-agent
    build:
      context: ../
      dockerfile: Dockerfile.angel-agent
    container_name: cove_angel_agent
    ports:
      - "8004:8004"
    environment:
      - DATABASE_URL=postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/cove
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - ANGEL_AGENT_PORT=8004
    networks:
      - growdirect
    restart: unless-stopped
```

Also add `ANGEL_AGENT_URL=http://angel-agent:8004` to the Flask service's
environment block so the proxy can reach the sidecar on the Docker network.

- [ ] **Step 3: Build and test**

```bash
cd ~/GrowDirect/Cove/devops && docker compose build angel-agent
cd ~/GrowDirect/Cove/devops && docker compose up -d angel-agent
curl -s http://localhost:8004/health | python3 -m json.tool
```
Expected: `{"service": "angel-agent", "status": "healthy", "tools_loaded": 12, ...}`

- [ ] **Step 4: Commit**

```bash
git add Cove/devops/docker-compose.yml
git commit -m "feat(angel-agent): add sidecar to docker-compose

cove-angel-agent on port 8004, joins growdirect network.
GRO-461"
```

---

### Task 15: Smoke Test Script

**Files:**
- Create: `Cove/scripts/smoke_test_angel.py`

Manual verification script that hits the real sidecar with real Anthropic API.

- [ ] **Step 1: Write smoke test**

```python
#!/usr/bin/env python3
"""Smoke test for Angel Agent sidecar.

Requires:
    - angel-agent container running on port 8004
    - ANTHROPIC_API_KEY set in container environment
    - cove database with listings and market snapshots

Usage:
    python3 scripts/smoke_test_angel.py
"""

import httpx
import json
import sys

BASE_URL = "http://localhost:8004"


def test_health():
    print("=== Health Check ===")
    resp = httpx.get(f"{BASE_URL}/health")
    data = resp.json()
    print(json.dumps(data, indent=2))
    assert data["status"] == "healthy", f"Unhealthy: {data}"
    assert data["tools_loaded"] == 12
    print("PASS\n")


def test_chat(message: str, label: str):
    print(f"=== {label} ===")
    print(f"User: {message}\n")
    resp = httpx.post(
        f"{BASE_URL}/chat",
        json={
            "messages": [{"role": "user", "content": message}],
            "session_id": "smoke-test",
        },
        timeout=120.0,
    )
    data = resp.json()
    print(f"Angel: {data['text'][:500]}")
    if data.get("tool_calls"):
        print(f"\nTools used: {[tc['tool'] for tc in data['tool_calls']]}")
    if data.get("usage"):
        print(f"Usage: {data['usage']}")
    print(f"\nPASS\n")
    return data


if __name__ == "__main__":
    try:
        test_health()
        test_chat(
            "What homes are active in Lunada Bay under $3M?",
            "Listing Search",
        )
        test_chat(
            "What's the market like in Valmonte?",
            "Market Stats",
        )
        test_chat(
            "Tell me about 7573-006-008",
            "Parcel Lookup",
        )
        print("=" * 40)
        print("ALL SMOKE TESTS PASSED")
    except Exception as e:
        print(f"\nFAILED: {e}", file=sys.stderr)
        sys.exit(1)
```

- [ ] **Step 2: Run smoke test (requires running sidecar + API key)**

```bash
cd ~/GrowDirect/Cove && python3 scripts/smoke_test_angel.py
```

- [ ] **Step 3: Commit**

```bash
git add Cove/scripts/smoke_test_angel.py
git commit -m "test(angel-agent): add manual smoke test script

Hits real sidecar with listing search, market stats, and parcel lookup.
GRO-461 GRO-462"
```

---

### Task 16: Run Full Test Suite + Final Verification

- [ ] **Step 1: Run all angel_agent tests**

```bash
cd ~/GrowDirect/Cove && python3 -m pytest tests/angel_agent/ -v
```
Expected: All tests PASS (23 tool tests + 7 server tests = 30 total)

- [ ] **Step 2: Run existing Cove tests to verify no regressions**

```bash
cd ~/GrowDirect/Cove && python3 -m pytest tests/ -v --timeout=60
```
Expected: All existing tests still pass

- [ ] **Step 3: Verify Docker health**

```bash
curl -s http://localhost:8004/health | python3 -m json.tool
```
Expected: healthy, 12 tools loaded

- [ ] **Step 4: Final commit if any fixes needed**

---

## Summary

| Task | What | Files | Tests |
|------|------|-------|-------|
| 1 | DB module | db.py, __init__.py | import check |
| 2 | System prompt | system_prompt.py | — |
| 3 | Area resolution | areas.py | — |
| 4 | Test fixtures | conftest.py | — |
| 5 | parcel_lookup | tools.py, test_tools.py | 7 tests |
| 6 | listing_search | tools.py, test_tools.py | 9 tests |
| 7 | market_stats | tools.py, test_tools.py | 5 tests |
| 8 | listing_detail | tools.py, test_tools.py | 2 tests |
| 9 | Tool dispatch + stubs | tools.py | — |
| 10 | ASGI server | server.py | — |
| 11 | Server tests | test_server.py | 7 tests |
| 12 | Proxy update | chat_routes.py | — |
| 13 | Dockerfile | Dockerfile.angel-agent | — |
| 14 | Docker compose | docker-compose.yml | build + health |
| 15 | Smoke test | smoke_test_angel.py | manual |
| 16 | Final verification | — | full suite |

**Total: 16 tasks, ~30 automated tests, ~14 commits**
