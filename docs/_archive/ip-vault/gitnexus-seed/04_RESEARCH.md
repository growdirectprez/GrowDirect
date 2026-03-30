---
type: research
domain: canary
status: active
created: 2026-03-19
updated: 2026-03-19
---
# Canary LP — Research Lineage & Industry Context

> **Domain:** IBM BI heritage, LP patterns, academic references, industry analysis
> **Last Updated:** 2026-03-19 | **Classification:** Confidential

---

## IBM Retail Business Intelligence Lineage

Canary LP modernizes the architecture pioneered by IBM's Retail Business Intelligence (V7, 2004–2005). IBM's three-layer approach mapped directly to Canary's current design:

### Layer Mapping: IBM → Canary

**RDWM (Retail Data Warehouse Model) → TSP Pipeline**
IBM: DB2 ETL pipeline ingesting POS data nightly into a star schema warehouse. Batch processing, 24-hour latency.
Canary: Real-time Square webhooks → Valkey Streams → three-stage subscriber pipeline. Sub-second latency. Same data normalization goal, modern event-driven execution.

**RBSTs (Retail Business Solution Templates) → Chirp Rules + Metrics Schema**
IBM: 14 pre-built data marts for specific retail analytics domains (Loss Prevention, Customer Analytics, Promotional Effectiveness, Store Operations, etc.). Each mart had hardcoded SQL queries.
Canary: 26+ parameterized detection rules across 8 categories, plus a star schema metrics layer. Rules are configurable per merchant, not hardcoded per data mart.

**RSDM (Retail Services Data Model) → CRDM v1.0/v1.1**
IBM: Metadata classification layer defining how POS data maps to warehouse dimensions. Used XML schemas and ARTS (Association for Retail Technology Standards) alignment.
Canary: Canonical Retail Data Model with typed fields, enum definitions, and source system abstraction. Same goal as RSDM (normalize heterogeneous POS data), modern execution (JSON schemas, PostgreSQL types, FK to source_systems reference table).

### What IBM Couldn't Do
IBM's constraint was delivery to executive dashboards — quarterly reports for LP directors. Canary's innovation is delivery to the store floor via mobile-first UX. IBM required data warehouse teams, ETL engineers, and report builders. Canary requires a Square OAuth connection and $29/month.

IBM's LP BST (Loss Prevention Business Solution Template) had four core report categories that map directly to Chirp:
- Baseline exception reports → C-001–C-030 (threshold anomalies)
- Cashier exceptions → C-063–C-068 (cash variance)
- Inventory discrepancy → C-080–C-085 (adjustment anomalies)
- Employee schedule compliance → C-040–C-042 (off-clock detection)

---

## LP Dashboard Pattern Catalog

Source: Speights et al. (2017) — Loss Prevention Research Council. Analysis of 197 figures across 13 chapters; 52 rated HIGH relevance to Canary dashboard design.

### Eight Visualization Pattern Categories

**1. Time-Series & Trends**
Incident density over time, normalized risk trends, dual time-series comparisons. Used for Owl's velocity trend analysis and daily digest generation. Maps to Canary: hourly_metrics, daily_metrics trend charts.

**2. Store/Location Comparison**
Revenue baseline comparisons, shrink ranking across locations, benchmarking against peer merchants. Maps to Canary: location_metrics, multi-merchant org dashboards.

**3. Distribution Analysis**
Percentile tables, empirical rule application (68-95-99.7), log-scale distributions for skewed data. Maps to Canary: employee scoring distributions, transaction amount histograms.

**4. LP Initiative Measurement**
Before/after comparisons, A/B testing frameworks, ROI calculation for LP interventions. Maps to Canary: rule effectiveness tracking, intervention outcome measurement.

**5. Risk Scoring & Driver Analysis**
Multi-predictor regression models, predicted vs. actual comparisons. Maps to Canary: Chirp composite scoring (C-070+), employee risk profiles.

**6. Classification & Segmentation**
Confusion matrices, ROC curves, KS lift charts for model evaluation. Maps to Canary: future Tier 3 AI model evaluation, detection rule precision/recall.

**7. Correlation & Scatter**
Employee theft vs. shrink correlation, sales vs. theft relationships. Maps to Canary: Owl's drill analysis, cross-metric exploration.

**8. Taxonomy & Reference**
Analytics activities taxonomy, metrics classification, ORC (Organized Retail Crime) network diagrams. Maps to Canary: field registry, rule category taxonomy.

### Gap Analysis
Canary currently has: Owl natural language search, Chirp alert feed, Fox case timeline. Needs: trend charts (time-series), distribution histograms, scatter plots, A/B framework, segmentation view. These are planned dashboard enhancements.

---

## ARTS Standards Alignment

The Archive contains extensive ARTS (Association for Retail Technology Standards) documentation. ARTS defines the standard data model for retail technology interoperability. Canary's CRDM draws from ARTS concepts while simplifying for SMB use cases:
- ARTS Transaction entity → Canary transactions table
- ARTS TenderLineItem → Canary transaction_tenders
- ARTS RetailStoreItem → Canary transaction_line_items
- ARTS WorkstationID → Canary device_id field

The CRDM is intentionally simpler than full ARTS compliance but maintains conceptual alignment for future enterprise integration.

---

## Cannabis Retail Risk Dictionary

Specialized detection rules for cannabis retail vertical. Cannabis merchants face unique LP challenges: high product value, regulatory reporting requirements (seed-to-sale tracking mandates), cash-heavy operations (banking restrictions), and elevated employee theft rates.

The risk dictionary maps cannabis-specific scenarios to Chirp rule categories: diversion detection (product leaves inventory without corresponding sale), compliance gaps (missing seed-to-sale entries), cash variance patterns specific to cash-heavy businesses, and discount abuse on high-value products.

---

## Alpha3X Stack Research

Technical evaluation of the infrastructure stack powering Canary's v3 architecture. Covers:
- PostgreSQL 17 with pgvector for semantic search and knowledge graph
- Valkey 8 as Redis-compatible streams engine (chosen over Redis for licensing clarity)
- Docker Compose orchestration with multi-service dependency management
- Ollama for local AI inference (qwen3:14b, 9.3GB model on Mac Mini)
- Cloudflare Tunnel for zero-trust access without port forwarding
- Alembic for multi-schema migration management

---

## Reference Library

The Canary Reference Library catalogs external sources that informed the product design:
- Loss Prevention Research Council publications (shrink statistics, detection methodologies)
- Square API documentation and webhook event schemas
- Bitcoin Ordinals specification and inscription tooling
- Avalanche smart contract documentation (NameRegistry pattern)
- PostgreSQL RLS and multi-tenant design patterns
- Flask application factory patterns and blueprint organization

---

*Canary LP | GrowDirect Inc. | Confidential*
