---
type: research
domain: canary
status: active
created: 2026-03-19
updated: 2026-03-19
---

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]

# Canary / GrowDirect — Project Reference Library
**Version:** 1.0
**Created:** February 17, 2026
**Maintained by:** Alex (COO/Chief of Staff), PhD (Research Framework)
**Purpose:** Living catalog of academic papers, SDKs, APIs, industry journals, books, and data sources that underpin Canary's technical and strategic claims. Built for footnotes, investor deck citations, conference papers, and credibility on bleeding-edge work.

**Jeffe directive (Feb 17):** *"We're going to be able to cite references to add credibility to some of this stuff that is out there on the bleeding edge."*

---

## How to Use This Document

- **Adding a reference:** Append to the appropriate section. Use the template at the bottom of each section.
- **Citing in documents:** Format as `[Author, Year — Title]` with full entry in this library.
- **Status flags:** 📚 Cataloged | ✅ Read/summarized | 🔗 SDK integrated | 🔄 Pending download

---

## Section 1 — Bitcoin, Lightning & Ordinals

### Books & Theses

| Title | Author | Year | Relevance | Status |
|---|---|---|---|---|
| *Softwar: A Novel Theory on Power Projection and the National Strategic Significance of Bitcoin* | Jason Lowery | 2023 | Bitcoin as physical security infrastructure — "The Dome." Our competitive moat framing. Core to Canary's Bitcoin-native architecture philosophy. | ✅ Referenced |
| *The Bitcoin Standard: The Decentralized Alternative to Central Banking* | Saifedean Ammous | 2018 | Austrian economics foundation for Bitcoin treasury strategy, sound money philosophy (Mary & Jane's grounding) | 📚 Cataloged |
| *Inventing Bitcoin* | Yan Pritzker | 2019 | Concise Bitcoin technical primer — useful for merchant education materials, onboarding content | 📚 Cataloged |
| *21 Lessons: What I've Learned from Falling Down the Bitcoin Rabbit Hole* | Gigi | 2019 | Bitcoin philosophy for non-technical audiences — useful for Canary merchant communications | 📚 Cataloged |

### Academic Papers

| Title | Authors | Year | Source | Relevance | Status |
|---|---|---|---|---|---|
| Bitcoin: A Peer-to-Peer Electronic Cash System | Satoshi Nakamoto | 2008 | https://bitcoin.org/bitcoin.pdf | Foundation. SHA-256 integrity model underlying Fox's chain of custody design. | ✅ Referenced |
| Ordinals: Arbitrary Data Inscription on Bitcoin | Casey Rodarmor | 2023 | https://ordinals.com/docs | Technical spec for Bitcoin Ordinals — directly relevant to Fox Chain of Custody Ledger (Sprint 2). ~50 sats per inscription. | 📚 Cataloged — Jeremy to review |
| Lightning Network Paper | Poon & Dryja | 2016 | https://lightning.network/lightning-network-paper.pdf | Micropayment channels — foundation for Goose module and pay-per-query metering design | ✅ Referenced |

### SDKs & Developer APIs

| Tool | Purpose | URL | Integrated? |
|---|---|---|---|
| OrdinalsBot API | Programmatic Bitcoin Ordinal minting. Cost ~50 sats/inscription. Supports JSON payloads. | https://ordinalsbot.com/docs | 🔄 Pending — Jeremy to prototype |
| Gamma.io API | Alternative Ordinal minting platform with creator tools | https://gamma.io | 🔄 Pending — Jeremy to evaluate |
| LND (Lightning Network Daemon) | Full Lightning node implementation — basis for micropayment metering | https://github.com/lightningnetwork/lnd | 📚 Cataloged |
| BTCPay Server | Self-hosted Bitcoin/Lightning payment processor — Goose module foundation | https://btcpayserver.org/docs | ✅ Integrated (Goose module) |
| Boltz Exchange | Non-custodial Lightning swap service — useful for sats-to-fiat bridge | https://boltz.exchange/docs | 📚 Cataloged |
| Strike API | Consumer Lightning wallet with developer API — target remittance partner | https://strike.me/developers | 📚 Cataloged |

---

## Section 2 — Point of Sale APIs & Retail Infrastructure

### Developer Documentation

| Platform | Docs URL | SDK Languages | Webhook Support | Status |
|---|---|---|---|---|
| Square Developer Portal | https://developer.squareup.com/docs | Python, Node.js, Java, PHP, Ruby, .NET, Go | Yes — real-time | ✅ Integrated (MVP built) |
| Square Marketplace Submission | https://developer.squareup.com/us/en/solutions-partner-program | N/A | N/A | 🔄 In progress — Eva/Syd |
| Clover Developer Portal | https://docs.clover.com/dev/docs/home | Android SDK, REST | Yes — event-triggered (seconds-to-minutes) | 🔄 Jeremy spike |
| Clover SDK Examples (GitHub) | https://github.com/clover/export-api-examples | Various | N/A | 📚 Cataloged |
| Toast Developer Guide | https://doc.toasttab.com/doc/devguide/index.html | REST | Yes | 📚 Low priority |
| Toast OpenAPI Reference | https://toastintegrations.redoc.ly/openapi | N/A | N/A | 📚 Low priority |
| Shopify Partner API | https://shopify.dev/docs/api | REST, GraphQL | Yes | 📚 Future phase |

### Industry Standards

| Standard | Description | URL | Relevance |
|---|---|---|---|
| APEx Common Retail Data Model (CRDM) | 14-entity canonical retail data model — PhD mapped Canary schema at ~70% coverage | Internal reference | ✅ Mapped (see CRDM Mapping Analysis doc) |
| ARTS (Association for Retail Technology Standards) | UPC/product schema standard — relevant to Catalog Scout / competitive price lookup | https://www.omg.org/retail/ | 📚 Cataloged |
| NRF Loss Prevention Standards | Industry LP definitions and metric standards | https://nrf.com/research/total-retail-loss | 📚 Cataloged |

---

## Section 3 — Retail Loss Prevention Research

### Academic & Industry Papers

| Title | Authors/Source | Year | URL | Relevance | Status |
|---|---|---|---|---|---|
| 2023 National Retail Security Survey | NRF / Loss Prevention Research Council | 2023 | https://nrf.com/research/national-retail-security-survey | Total retail loss benchmarks. Key stat: shrink = 1.6% of sales. Investor pitch anchor. | ✅ Referenced |
| Total Retail Loss Framework | Professor Adrian Beck, University of Leicester | 2016 | Academic journals | Defines Total Retail Loss (TRL) — the framework underlying Owl module | 📚 Cataloged — PhD to summarize |
| Exception-Based Reporting in LP | Sysrepublic / LP Media | ~2010 | https://losspreventionmedia.com/eyeonlp-sysrepublic-captures-data-and-creates-value-for-the-retail-industry/ | Jeffe's EBR platform at Sysrepublic — origin story + credibility anchor | ✅ Referenced |
| 7-Eleven Human Trafficking Case (DOJ) | DOJ / Federal Prosecution | 2013 | https://csnews.com/7-eleven-franchisee-gets-prison-time-exploiting-illegal-aliens | Jeffe's case — data forensics → federal prosecution. Canary's proof of concept at scale. | ✅ Referenced (Jeffe_Quotes.md) |

### Key Industry Reports (Annual)

| Report | Publisher | URL | Notes |
|---|---|---|---|
| Total Retail Loss Report (annual) | NRF | https://nrf.com | Update reference each year. 2023: $112B total retail loss in US |
| Global Retail Theft Barometer | Checkpoint Systems (now Sensormatic) | Various | Benchmarks shrink rates by country/vertical |
| RILA Loss Prevention Conference Proceedings | RILA | https://rila.org | Jeffe presented at RILA Dallas (7-Eleven case) |
| LPM Insider / LP Magazine | Loss Prevention Media | https://losspreventionmedia.com | Industry trade — good for trend research, Will's lead gen |

---

## Section 4 — Fraud Detection, ML & Digital Forensics

### Academic Papers

| Title | Authors | Year | Relevance | Status |
|---|---|---|---|---|
| Credit Card Fraud Detection Using Machine Learning | Various (IEEE, ACM libraries) | 2018–2024 | Baseline ML fraud detection algorithms — relevant to Fox threat scoring (Sprint 4) | 🔄 PhD to curate 3-5 seminal papers |
| Anomaly Detection in Retail Transactions | Various | Ongoing | Exception-based reporting algorithmic foundations | 🔄 PhD to curate |
| Digital Forensics Evidence Standards | NIST SP 800-86 | 2006 (updated) | https://csrc.nist.gov/publications/detail/sp/800-86/final | Standards for digital evidence collection — applies to Fox chain of custody design | 📚 Cataloged |

### Fraud Pattern Libraries

| Source | Description | Status |
|---|---|---|
| FBI IC3 Annual Report | Internet Crime Complaint Center — retail fraud trends | https://www.ic3.gov/Annual/Reports — 📚 Cataloged |
| FinCEN SAR Activity Reviews | Suspicious Activity Report patterns — relevant to SAR compliance module | https://fincen.gov — 📚 Cataloged |
| DEA ARCOS Database | Drug enforcement tracking by pharmacy — Hawk module foundation | https://www.deadiversion.usdoj.gov/arcos/ — 📚 Cataloged |

---

## Section 5 — Public Datasets (External Data Enrichment / Catalog Scout)

*Primary research responsibility: Will. Architecture: Tom. Query integration: Jeremy/PhD.*

### Government Health & Fraud Data

| Dataset | Source | URL | Size | Format | CA Subset | Fraud Relevance |
|---|---|---|---|---|---|---|
| Medicaid Provider Spending | HHS/DOGE (Feb 2026 release) | https://opendata.hhs.gov/datasets/medicaid-provider-spending | 3.36 GB ZIP | CSV (~227M rows, 2018–2024) | Yes (filter by state) | ⭐⭐⭐⭐⭐ |
| CA Healthcare Payments | California Open Data | https://data.ca.gov/dataset/healthcare-payments-data-snapshot | Medium | CSV | Native | ⭐⭐⭐⭐⭐ |
| CMS Part D Prescriber Data | CMS | https://data.cms.gov/provider-summary-by-type-of-service/medicare-part-d-prescribers | Large | CSV | Filter by state | ⭐⭐⭐⭐ |
| DEA ARCOS Retail Drug Summary | DEA | https://www.deadiversion.usdoj.gov/arcos/retail_drug_summary/ | Medium | CSV | Yes | ⭐⭐⭐ |

### Retail Economics & Sales

| Dataset | Source | URL | Update Freq | Format | Notes |
|---|---|---|---|---|---|
| Advance Retail Sales (RSXFS) | Federal Reserve / FRED | https://fred.stlouisfed.org/series/RSXFS | Monthly | CSV | Baseline retail trend benchmarking |
| Warehouse and Retail Sales | U.S. Census via Data.gov | https://catalog.data.gov/dataset/warehouse-and-retail-sales | Monthly | CSV/JSON | DSD/wholesale movement baseline |
| CA Retail Sales Tax Data | CA Board of Equalization | https://www.cdtfa.ca.gov/statistics/ | Quarterly | CSV | CA-specific retail volume |

### Geographic & Demographic Enrichment

| Dataset | Source | URL | Format | Notes |
|---|---|---|---|---|
| American Community Survey (ACS) | U.S. Census | https://data.census.gov | CSV/API | ZIP-level income, demographics — Catalog Scout foundation |
| NOAA Weather API | NOAA | https://www.weather.gov/documentation/services-web-api | JSON API (free) | Weather by location/date — Jeffe's "January sales drop" use case |
| OpenWeatherMap API | OpenWeather | https://openweathermap.org/api | JSON API (free tier) | Historical weather — simpler than NOAA for prototyping |
| Business Patterns (ZIP Code) | U.S. Census | https://www.census.gov/programs-surveys/cbp.html | CSV | Retail establishment counts by ZIP — competitive context |

### API Discovery Tools (Catalog Scout Foundation)

| Tool | Purpose | URL | Notes |
|---|---|---|---|
| APIs.guru | Largest directory of public OpenAPI/Swagger specs | https://apis.guru | Starting catalog for Catalog Scout — 2000+ APIs indexed |
| SwaggerHub | Swagger/OpenAPI hosting and discovery | https://swaggerhub.com | Source for schema discovery |
| Public APIs List | Curated list of free public APIs | https://github.com/public-apis/public-apis | Good for seeding Catalog Scout's built-in catalog |
| Postman Public API Network | 50,000+ public API collections | https://www.postman.com/explore | Includes schemas + examples |

---

## Section 6 — Bitcoin Standard & Sound Money

### Academic & Foundational References

| Title | Author | Year | Relevance |
|---|---|---|---|
| The Theory of Money and Credit | Ludwig von Mises | 1912 | Austrian economics foundation — Mary & Jane's monetary philosophy |
| The Road to Serfdom | F.A. Hayek | 1944 | Sound money / spontaneous order — Bitcoin philosophical foundation |
| The Bitcoin Whitepaper | Satoshi Nakamoto | 2008 | See Section 1 |
| Softwar Thesis | Jason Lowery | 2023 | See Section 1 |
| Broken Money | Lyn Alden | 2023 | Comprehensive monetary history leading to Bitcoin — investor pitch backdrop |

---

## Section 7 — Industry Journals & Trade Publications

| Publication | Focus | URL | Relevant Sections |
|---|---|---|---|
| Loss Prevention Magazine | LP industry | https://losspreventionmedia.com | Technology, case studies, fraud trends |
| Retail TouchPoints | Retail tech | https://retailtouchpoints.com | POS, analytics, shrink management |
| Chain Store Age | Multi-unit retail ops | https://chainstoreage.com | Operations, LP, vendor management |
| Drug Store News | Pharmacy retail | https://drugstorenews.com | Hawk module vertical |
| Cannabis Business Times | Cannabis retail | https://cannabisbusinesstimes.com | Mary & Jane vertical |
| Bitcoin Magazine | Bitcoin | https://bitcoinmagazine.com | Lightning, Ordinals, merchant adoption |
| Journal of Financial Crime | Academic fraud research | https://emeraldpublishing.com | Peer-reviewed fraud detection papers |
| RILA Insights | Retail LP industry association | https://rila.org/insights | Conference proceedings, research |

---

## Section 8 — Conference & Event Resources

| Event | Focus | When | URL | Notes |
|---|---|---|---|---|
| NRF Big Show | Retail industry | January (annual) | https://nrf.com/events/nrf | Jeffe roadshow target |
| RILA Loss Prevention Conference | Retail LP | Annual | https://rila.org | Jeffe presented here (2013, 7-Eleven case) |
| Shoptalk | Retail tech | Spring | https://shoptalk.com | Jeffe roadshow target |
| Money 20/20 | Fintech/payments | October | https://money2020.com | Bitcoin/Lightning merchant adoption angle |
| Bitcoin Conference (BTC 2026) | Bitcoin | Annual | https://b.tc/conference | Core audience for Bitcoin-native retail pitch |

---

## Section 9 — Alpha 3X Stack References (Due Diligence)

**⚡ Full due diligence catalog:** See `Markdown/Research/Canary_Alpha3X_Stack_References_v1.0.md`

**Compiled February 21, 2026** — PhD, Tom, Jeremy research across all 11 stack layers. 300+ source URLs cataloged with documentation, Docker deployment, security, integration, license, and benchmark references for: PostgreSQL 17, Keycloak 26, Hasura v2 CE, Directus 11, Apache Superset, Apache Airflow, Flask, Square SDK, infrastructure (Nginx, Traefik, Docker Compose, Portainer, PgBouncer, Redis/Valkey), Bitcoin/Lightning (BTCPay Server, OrdinalsBot, LNURL-auth), and monitoring (Prometheus, Grafana, Loki).

**Key findings:**
- ⚠️ **Superset** is at v6.0.0 (Blueprint says 4.x)
- ⚠️ **Airflow** is at v3.0.0 (Blueprint says 2.x; 2.x EOL April 2026)
- ⚠️ **Square SDK** is at v43.2.0 (Canary pinned at v35)
- ⚠️ **Hasura v3** is cloud-only/proprietary — must use v2 CE (Apache-2.0)
- ⚠️ **Directus BSL 1.1** — Syd review required ($5M revenue threshold, converts to GPL-3.0 April 2026)
- ⚠️ **Redis** changed to RSALv2/SSPLv1 — Valkey (BSD-3, Linux Foundation) recommended as drop-in replacement
- ⚠️ **LNURL-auth** — no Keycloak plugin exists; custom SPI development required (post-MVP)
- ✅ **10 of 11 stack layers** cleared with permissive licenses (Apache-2.0, MIT, BSD, ISC)

---

## Adding References — Template

To add a new entry to any section, use this format:

```
| [Title] | [Author/Source] | [Year] | [URL] | [1–2 sentence relevance to Canary] | [📚 Cataloged / ✅ Read / 🔗 SDK integrated] |
```

**Who should update this:**
- **PhD** — Academic papers, research frameworks, new journals
- **Will** — Public datasets, fraud pattern research, new government data releases
- **Jeremy** — SDK integrations, API documentation, developer tools
- **Jess** — Formatting, version control, brand consistency
- **Alex** — Strategic references, investor deck sources, conference resources

---

*Canary LP | Confidential*
*v1.0 — Created February 17, 2026*
*Next review: February 28, 2026*
