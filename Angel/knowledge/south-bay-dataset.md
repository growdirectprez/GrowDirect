# South Bay Proprietary Dataset — Architecture

## The Vision

Build a proprietary real estate intelligence dataset covering the entire
South Bay — every parcel, every transaction, every agent, every school,
every permit, every grant deed — that no one else has assembled in one place.

This isn't just for Angelique. This is the data moat for Angel as a platform.
Any Compass agent (or any agent, period) who uses Angel gets access to
intelligence their competitors can't match.

Angelique is the first customer. The South Bay dataset is the product.

---

## Dataset Scope

### Geographic Coverage

| Area | Cities | Zip Codes | Est. Parcels |
|------|--------|-----------|-------------|
| Palos Verdes Peninsula | PVE, RPV, Rolling Hills, RHE | 90274, 90275 | ~25,000 |
| Beach Cities | Manhattan Beach, Hermosa Beach, Redondo Beach | 90266, 90254, 90277, 90278 | ~35,000 |
| Torrance | Torrance (all neighborhoods) | 90501-90505 | ~45,000 |
| Harbor Area | San Pedro, Wilmington, Harbor City | 90731, 90732, 90744, 90710 | ~40,000 |
| Inland South Bay | Gardena, Carson, Lomita | 90247, 90248, 90745, 90717 | ~35,000 |
| **Total** | **~15 cities** | **~20 zip codes** | **~180,000 parcels** |

### Data Layers

```
Layer 1: PARCEL (foundation — APN-keyed)
  └── LA County Assessor: APN, address, lot size, zoning, year built, sqft,
      use code, owner name, mailing address, assessed value, tax amount

Layer 2: TRANSACTIONS (what happened)
  └── CRMLS: listing history, list price, close price, DOM, status changes,
      listing agent, buyer agent, property photos, descriptions
  └── County Recorder: grant deeds, trust transfers, foreclosures, liens
  └── ATTOM: 10-year sales history, mortgage data, foreclosure status

Layer 3: AGENTS (who's active)
  └── CRMLS Member resource: agent name, MLS ID, office, contact
  └── DRE licensee file: DRE#, license status, broker affiliation
  └── Derived: transaction count, volume, neighborhoods, market share

Layer 4: VALUATIONS (what it's worth)
  └── ATTOM AVM: automated valuation model estimates
  └── County Assessor: assessed value (often below market)
  └── CRMLS: comparable sales (radius + timeframe)
  └── Derived: Zestimate-killer using our own comp model

Layer 5: SCHOOLS (decision driver)
  └── GreatSchools API: ratings, test scores, reviews
  └── PVPUSD / MBUSD / TUSD: enrollment, boundary maps, programs
  └── Derived: feeder patterns, school-to-neighborhood mapping
  └── Angelique overlay: personal experience annotations

Layer 6: COMMUNITY (Cove bridge)
  └── Cove data model: HOA membership, assessments, ARC applications
  └── Derived: community health, turnover rate, improvement activity

Layer 7: SIGNALS (predictive intelligence)
  └── Likely-to-sell scores (Compass + SmartZip)
  └── Permit activity (LADBS): renovation = staying or prepping to sell
  └── Ownership duration: long-term owners = equity-rich prospects
  └── Life events: trust transfers, estate filings, divorce filings (public record)
  └── Market signals: price reductions, expired listings, DOM thresholds

Layer 8: BEHAVIORAL (digital signals)
  └── GA4: OwnPalosVerdes.com visitor data (geo, pages, time on site)
  └── Meta Pixel: retargeting audiences
  └── Email engagement: open/click/reply rates by contact
```

---

## Data Sources & Access

### Tier 1: Available Now (Free or Low Cost)

| Source | Data | Access Method | Cost |
|--------|------|---------------|------|
| LA County Assessor | Parcels, owners, assessed values, tax | [Open Data Portal](https://data.lacounty.gov) + ArcGIS API | Free |
| LA County Recorder | Grant deeds, transfers (1977-present) | Name/AIN/doc# search; bulk via PRA request | Free (copies: $1-3/page) |
| CA DRE Licensee File | All licensed agents: name, DRE#, status, broker | Excel download, updated daily | Free |
| GreatSchools | School ratings, test scores, reviews | API (free tier) | Free |
| US Census / ACS | Demographics, income, household data by tract | Census API | Free |
| Redfin Data Center | Migration patterns, market trends by zip | CSV download | Free |
| Google Keyword Planner | Search volume for target keywords | Google Ads account | Free |

### Tier 2: Requires Angelique's Access

| Source | Data | Access Method | Cost |
|--------|------|---------------|------|
| CRMLS | Full MLS: listings, agents, offices, transactions | RESO Web API (OData) | Included with MLS membership |
| Compass CRM | Contacts, collections, pipeline, Likely to Sell | Compass platform (manual or API if available) | Included with Compass |
| Compass Private Exclusives | Pre-market listings, PE performance data | Compass agent dashboard | Included |

### Tier 3: Paid APIs (Phase 2)

| Source | Data | Access Method | Cost |
|--------|------|---------------|------|
| ATTOM | 158M properties: sales, AVM, permits, hazards, mortgage | REST API | From $95/mo |
| SmartZip | Predictive seller likelihood scores | Platform + API | ~$500-800/mo |
| LinkedIn Sales Navigator | Employer hiring data, relocation signals | Web + API | ~$80/mo |
| SEMrush or Ahrefs | Keyword data, competitor analysis, SERP tracking | API | ~$120-230/mo |

### Tier 4: Cove Bridge (Internal)

| Source | Data | Access Method | Cost |
|--------|------|---------------|------|
| Cove PostgreSQL | Parcels, members, ownership, assessments, ARC apps | Direct DB query (shared infra) | Free (internal) |

---

## Database Schema (Angel PostgreSQL)

### Core Tables

```sql
-- Every parcel in the South Bay. The spine.
CREATE TABLE parcels (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    apn             VARCHAR(20) UNIQUE NOT NULL,  -- Assessor Parcel Number
    address         TEXT NOT NULL,
    city            VARCHAR(50) NOT NULL,
    zip             VARCHAR(10) NOT NULL,
    neighborhood    VARCHAR(100),                  -- derived / manually tagged
    county          VARCHAR(50) DEFAULT 'Los Angeles',
    state           VARCHAR(2) DEFAULT 'CA',
    lat             DECIMAL(10, 7),
    lng             DECIMAL(10, 7),
    lot_sqft        INTEGER,
    living_sqft     INTEGER,
    year_built      INTEGER,
    bedrooms        INTEGER,
    bathrooms       DECIMAL(3, 1),
    property_type   VARCHAR(50),                   -- SFR, condo, townhome, land
    zoning          VARCHAR(20),
    use_code        VARCHAR(20),
    assessed_value  DECIMAL(14, 2),
    tax_amount      DECIMAL(10, 2),
    school_district VARCHAR(50),
    elementary      VARCHAR(100),
    middle_school   VARCHAR(100),
    high_school     VARCHAR(100),
    cove_community_id UUID,                        -- FK to Cove if in managed HOA
    embedding       VECTOR(1024),                  -- semantic search via Ollama
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Every ownership record. Who owns what, since when.
CREATE TABLE owners (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    parcel_id       UUID NOT NULL REFERENCES parcels(id),
    apn             VARCHAR(20) NOT NULL,
    owner_name      TEXT NOT NULL,
    mailing_address TEXT,
    ownership_start DATE,                          -- from grant deed date
    ownership_end   DATE,                          -- NULL = current owner
    acquisition_price DECIMAL(14, 2),
    transfer_type   VARCHAR(50),                   -- grant deed, trust, foreclosure
    document_number VARCHAR(50),                   -- county recorder doc#
    is_current      BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Every MLS listing event. The transaction layer.
CREATE TABLE listings (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    parcel_id       UUID NOT NULL REFERENCES parcels(id),
    apn             VARCHAR(20) NOT NULL,
    mls_number      VARCHAR(20) UNIQUE,
    status          VARCHAR(30) NOT NULL,           -- active, pending, closed, expired, withdrawn
    list_price      DECIMAL(14, 2),
    close_price     DECIMAL(14, 2),
    original_price  DECIMAL(14, 2),
    price_per_sqft  DECIMAL(10, 2),
    dom             INTEGER,                        -- days on market
    cdom            INTEGER,                        -- cumulative DOM
    list_date       DATE,
    close_date      DATE,
    expiration_date DATE,
    listing_agent_id UUID REFERENCES agents(id),
    buyer_agent_id  UUID REFERENCES agents(id),
    listing_office  VARCHAR(200),
    buyer_office    VARCHAR(200),
    property_type   VARCHAR(50),
    description     TEXT,
    photos_url      TEXT[],                         -- array of media URLs
    was_private_exclusive BOOLEAN DEFAULT FALSE,
    was_coming_soon BOOLEAN DEFAULT FALSE,
    source          VARCHAR(30) DEFAULT 'crmls',
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Every agent who's touched a deal in the South Bay.
CREATE TABLE agents (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    mls_id          VARCHAR(30),                   -- CRMLS member ID
    dre_number      VARCHAR(20),                   -- CA DRE license number
    full_name       TEXT NOT NULL,
    first_name      VARCHAR(100),
    last_name       VARCHAR(100),
    email           VARCHAR(200),
    phone           VARCHAR(30),
    office_name     VARCHAR(200),
    brokerage       VARCHAR(200),                  -- Compass, Coldwell Banker, etc.
    is_our_agent    BOOLEAN DEFAULT FALSE,          -- Angelique = TRUE
    license_status  VARCHAR(20),                   -- from DRE file
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Derived market intelligence per neighborhood.
CREATE TABLE neighborhood_stats (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    neighborhood    VARCHAR(100) NOT NULL,
    city            VARCHAR(50) NOT NULL,
    zip             VARCHAR(10),
    period          VARCHAR(10) NOT NULL,           -- '2026-Q1', '2026-03', etc.
    median_price    DECIMAL(14, 2),
    avg_price       DECIMAL(14, 2),
    avg_dom         INTEGER,
    avg_ppsf        DECIMAL(10, 2),
    total_sold      INTEGER,
    total_active    INTEGER,
    total_pending   INTEGER,
    total_expired   INTEGER,
    inventory_months DECIMAL(4, 1),
    yoy_price_change DECIMAL(5, 2),                -- percentage
    top_agent_id    UUID REFERENCES agents(id),     -- market share leader
    our_agent_deals INTEGER,                        -- Angelique's deals this period
    our_market_share DECIMAL(5, 2),                 -- percentage
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

-- SEO keyword targets mapped to neighborhoods + authority.
CREATE TABLE seo_targets (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    keyword         TEXT NOT NULL,
    search_volume   INTEGER,                       -- monthly
    difficulty      INTEGER,                       -- 0-100
    neighborhood    VARCHAR(100),
    category        VARCHAR(50),                   -- neighborhood, school, market, relocation
    our_authority   INTEGER,                       -- deals in this zone (higher = stronger)
    priority_score  DECIMAL(5, 2),                 -- calculated from formula
    content_url     TEXT,                           -- OwnPalosVerdes page if exists
    content_status  VARCHAR(30),                   -- planned, drafted, published, ranking
    target_rank     INTEGER,                       -- where we want to be
    current_rank    INTEGER,                       -- where we are (from SERP tracking)
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Lead signals generated from data mining.
CREATE TABLE lead_signals (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    parcel_id       UUID NOT NULL REFERENCES parcels(id),
    apn             VARCHAR(20) NOT NULL,
    signal_type     VARCHAR(50) NOT NULL,           -- new_listing, price_reduction, grant_deed, etc.
    signal_date     DATE NOT NULL,
    signal_data     JSONB,                          -- flexible payload per signal type
    lead_score      INTEGER,                        -- 1-100
    pipeline_stage  VARCHAR(30),
    assigned_to     UUID REFERENCES agents(id),
    actioned_at     TIMESTAMP,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Content briefs generated from transaction data + SEO targets.
CREATE TABLE content_briefs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    seo_target_id   UUID REFERENCES seo_targets(id),
    title           TEXT NOT NULL,
    keyword         TEXT NOT NULL,
    content_type    VARCHAR(50),                   -- blog, guide, comparison, market_report
    authority_proof TEXT,                           -- "12 deals in Lunuda Bay, $38M volume"
    outline         JSONB,                         -- structured outline
    word_count      INTEGER,
    status          VARCHAR(30),                   -- planned, assigned, drafted, published
    published_url   TEXT,
    publish_date    DATE,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

## Data Ingestion Pipeline

### Phase 1: Foundation (Immediate — Free Data)

```
1. LA County Assessor Open Data → parcels table
   - Download parcel data (ArcGIS / data.lacounty.gov)
   - Filter to South Bay zip codes
   - Load ~180,000 parcels with owner, lot, assessed value

2. CA DRE Licensee File → agents table
   - Download daily Excel file
   - Filter to LA County brokers/agents
   - Load name, DRE#, license status, broker affiliation
   - Match Angelique: DRE# 01475592

3. GreatSchools API → school fields on parcels
   - For each parcel, get assigned schools
   - Load ratings, feeder patterns
   - Tag parcels with school district + specific schools

4. Cove Bridge → cove_community_id on parcels
   - For APNs that exist in Cove communities (WPBCA, etc.)
   - Link parcel to Cove membership data
```

### Phase 2: Transaction Layer (Requires CRMLS Access)

```
5. CRMLS RESO API → listings + agents tables
   - Initial pull: all closed/active/pending listings in South Bay zips
   - Filter by date range (start with 5 years, expand to max available)
   - Match listings to parcels by address/APN
   - Extract listing agent + buyer agent → agents table
   - Daily incremental sync via ModificationTimestamp

6. Angelique's Transaction History → is_our_agent flag
   - Filter listings by her MLS agent ID (both sides)
   - Flag her agent record: is_our_agent = TRUE
   - Calculate her power zones, price bands, seasonal patterns
```

### Phase 3: Intelligence Layer (Paid APIs)

```
7. ATTOM API → enrich parcels + owners
   - AVM estimates for every parcel
   - 10-year sales history (fills gaps before CRMLS data)
   - Permit history, hazard data, mortgage data
   - Owner demographics and mailing address

8. County Recorder → owners table (transfer events)
   - Grant deeds, trust transfers for South Bay parcels
   - Historical ownership chain
   - Bulk via PRA request or scrape public index
```

### Phase 4: Predictive Layer

```
9. Lead Scoring Model
   - Train on historical data: which signals predicted a listing?
   - Features: ownership duration, equity, permit activity, neighborhood trends
   - Output: likely-to-sell score per parcel

10. SEO Intelligence
    - Keyword research for all target terms
    - SERP tracking for ranking positions
    - Content gap analysis vs. competitors
    - Priority scoring using authority matrix
```

---

## What This Enables

### For Angelique (Immediate Value)

- "Show me every home that sold in Lunada Bay last quarter" → instant
- "Who are the top 5 agents in RPV by volume?" → competitive intelligence
- "Generate a market report for my Valmonte sellers" → data-backed content
- "Which of my past clients have the most equity?" → referral opportunities
- "What should I write about next?" → SEO brief with authority proof

### For Angel as a Platform (Long-Term Value)

- Any Compass agent in the South Bay could use this dataset
- Market share analysis by agent, office, brokerage, neighborhood
- Predictive lead scoring that improves with more data
- Content engine that auto-generates market reports
- The first RE-focused MCP service layer — backed by proprietary data

### For the Cove Bridge (Cross-Platform Value)

- HOA communities tracked in Cove become lead-gen zones in Angel
- Ownership transfers in Cove trigger lead signals in Angel
- ARC applications (property improvements) feed the likely-to-sell model
- Community health metrics inform neighborhood investment signals
