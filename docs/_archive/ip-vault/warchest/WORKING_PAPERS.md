---
type: pitch
domain: business
status: active
created: 2026-03-18
updated: 2026-03-19
---
# GrowDirect Working Papers — Master Index

> *"Content orchestration has to be tight from the top or it will go haywire."*

---

## Numbering Schema

Every piece of GrowDirect intellectual property has a permanent address in this tree. The address never changes. Content moves through states; the address stays.

```
WP-[DOMAIN].[CHAPTER].[SECTION]
```

**Domains (top-level, permanent):**

| Domain | Code | Scope |
|---|---|---|
| The Narrative | WP-1 | Founder story, pitch, vision, article — external-facing prose |
| The Product | WP-2 | Canary modules, features, UX, interactive prototypes |
| The Architecture | WP-3 | CRDM, pipeline, databases, gLog, security, infrastructure |
| The Business | WP-4 | Market, model, economics, thesis, financials |
| The Shield | WP-5 | Compliance, IP, legal, regulatory, contracts |
| The Operations | WP-6 | Process, team, sprint methodology, DevOps |
| The Reference Library | WP-7 | API docs, schemas, code index, data dictionary, research |

**Asset Type Suffixes (on files, not WP numbers):**

| Suffix | Type | Example |
|---|---|---|
| `.N` | Narrative | `WP-1.1.N` — prose, investor-facing markdown |
| `.S` | Schema | `WP-3.2.S` — DDL, ERD, migration files |
| `.A` | API | `WP-3.1.A` — endpoint definitions, Swagger/OpenAPI |
| `.C` | Code | `WP-2.1.C` — module structure, key implementation files |
| `.V` | Visual | `WP-1.1.V` — diagrams, SVGs, interactive HTML |
| `.D` | Data | `WP-3.2.D` — sample data, fixtures, field mappings |
| `.L` | Legal | `WP-5.1.L` — contracts, assessments, filings |
| `.R` | Research | `WP-4.1.R` — briefs, analysis, position papers |
| `.T` | Test | `WP-2.1.T` — QA plans, test suites, scenarios |
| `.O` | Operations | `WP-6.3.O` — deployment configs, infrastructure scripts |
| `.P` | PRD | `WP-2.1.P` — product requirements documents |

**Status Markers:**

| Marker | Meaning |
|---|---|
| `EXISTS` | File exists, mapped, content is current |
| `DRAFT` | File exists, needs editing before external use |
| `STUB` | Node defined, no content yet — to be written |
| `PLANNED` | On roadmap, not yet scoped |
| `CONFIDENTIAL` | Exists but restricted distribution — not for external outputs |

**Output Targets:**

| Target | Description |
|---|---|
| `pack` | War Chest multi-page gated briefing |
| `investor` | Single-page investor site |
| `public` | growdirect.io public site |
| `internal` | Team reference only |
| `diligence` | Investor due diligence room |
| `legal` | Attorney/legal review only |

---

## WP-1: THE NARRATIVE

The founder story, the pitch, the vision. External-facing prose that tells the GrowDirect story.

### WP-1.1 — The Pitch

The elevator pitch. Problem, solution, economy, market, vision.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-1.1.N | EXISTS | `sources/01-the-pitch.md` | pack, investor |
| WP-1.1.V | STUB | — (need: three-gaps visual, Capture/Seal/Inscribe styled diagram) | pack, investor |

### WP-1.2 — The Article

Long-form magazine narrative. tLog problem, gLog solution, compliance, career through-line.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-1.2.N | EXISTS | `sources/14-the-article.md` | pack, public |
| WP-1.2.R | EXISTS | `output/PhD/PhD_tLogToGlog_FounderCase_v1.0.md` | internal |

### WP-1.3 — The Founder

Career arc, enterprise credentials, the SHA-256 homecoming.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-1.3.N | EXISTS | `sources/11-the-team.md` | pack, investor, public |
| WP-1.3.R | EXISTS | `Company/Team/Jeffe.md` | internal |
| WP-1.3.R | EXISTS | `Company/Team/Jeffe_CEO_Biography.md` | internal |
| WP-1.3.R | EXISTS | `Company/Team/Jeffe_Quotes.md` | internal |
| WP-1.3.V | STUB | — (need: career arc timeline SVG) | investor |

### WP-1.4 — The North Star

Product philosophy. "We don't want to add to the stress."

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-1.4.N | STUB | — (extract from pitch + brainstorm sessions) | investor, public |
| WP-1.4.R | EXISTS | `Sessions/Jeffe_Brainstorm_2026-02-17.md` | internal |
| WP-1.4.R | EXISTS | `Sessions/Jeffe_Brainstorm_2026-02-22.md` | internal |

---

## WP-2: THE PRODUCT

What we built. Canary LP modules, interactive prototypes, feature documentation.

### WP-2.1 — Canary Core

Detection engine, merchant dashboard, webhook capture, alert system.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-2.1.N | STUB | — (need: investor-facing Canary Core overview) | pack, investor |
| WP-2.1.P | EXISTS | `Documents/Product_Guides/Canary_PRD_E0_Platform_Foundation_v1.0.docx` | internal |
| WP-2.1.P | EXISTS | `Documents/Product_Guides/Canary_PRD_E1_Core_Fraud_Detection_v1.0.docx` | internal |
| WP-2.1.C | EXISTS | `Canary/canary/blueprints/` (21 route files) | internal |
| WP-2.1.C | EXISTS | `Canary/canary/services/chirp/` (detection engine) | internal |
| WP-2.1.T | EXISTS | `Canary/tests/` (full test suite) | internal |
| WP-2.1.V | EXISTS | `sources/04-the-product.html` (interactive prototype) | pack, investor |

### WP-2.2 — The Fox (Case Management)

Alerts become investigations. Investigations become evidence. Evidence becomes action.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-2.2.N | EXISTS | `sources/05-the-fox.md` | pack, investor |
| WP-2.2.P | EXISTS | `Documents/Product_Guides/Canary_PRD_E3_Fox_Case_Management_v1.0.docx` | internal |
| WP-2.2.P | EXISTS | `Specs/Fox_Sprint_1_Implementation_Plan.md` | internal |
| WP-2.2.S | EXISTS | `Canary/canary/models/fox/` (case, subject, evidence models) | internal |
| WP-2.2.A | EXISTS | `Canary/canary/blueprints/fox.py` + `fox_wired.py` | internal |
| WP-2.2.C | EXISTS | `Canary/canary/services/fox/` (case management services) | internal |
| WP-2.2.S | EXISTS | `Specs/Fox_Data_Model_v2.0_GSLM_Enhanced.md` | internal |
| WP-2.2.R | EXISTS | `Modules/Fox.md` | internal |

### WP-2.3 — The Goose (Bitcoin Payments)

Zero chargebacks. Zero middlemen. Lightning-native commerce.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-2.3.N | EXISTS | `sources/06-the-goose.md` | pack, investor |
| WP-2.3.R | EXISTS | `Modules/Goose.md` | internal |
| WP-2.3.R | EXISTS | `Specs/Lightning_Strategy_Summary_v2.md` | internal |
| WP-2.3.P | EXISTS | `Documents/Product_Guides/Canary_PRD_E9_Chirp_UDQ_Lightning_Metering_v1.0.docx` | internal |
| WP-2.3.C | STUB | — (Goose module not yet implemented) | internal |
| WP-2.3.A | STUB | — (Lightning API endpoints not yet defined) | internal |
| WP-2.3.L | STUB | — (money transmitter analysis — Syd flagged) | legal |

### WP-2.4 — The Owl (Analytics Oracle)

Watches. Learns. Predicts. Democratized enterprise analytics for SMB.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-2.4.N | EXISTS | `sources/07-the-owl.md` | pack, investor |
| WP-2.4.R | EXISTS | `Modules/Owl.md` | internal |
| WP-2.4.C | STUB | — (Owl ML pipeline not yet implemented) | internal |
| WP-2.4.S | STUB | — (metrics star schema documentation) | internal |

### WP-2.5 — The Companion (Guided Experience)

Merchant onboarding, guided workflows, contextual help.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-2.5.P | EXISTS | `Documents/Product_Guides/Canary_PRD_E0F6_Guided_Companion_v1.0.docx` | internal |
| WP-2.5.P | EXISTS | `Specs/Canary_Guided_Companion_Design_Spec_v1.0.md` | internal |
| WP-2.5.C | EXISTS | `Canary/canary/blueprints/companion_wired.py` | internal |
| WP-2.5.N | STUB | — (no external-facing companion narrative yet) | — |

### WP-2.6 — Product Prototype (Interactive)

Full interactive dashboard mockup. Canary Core + Fox + Goose + Owl.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-2.6.V | EXISTS | `sources/04-the-product.html` | pack, investor |
| WP-2.6.V | STUB | — (need: annotated screenshot set for PDF/print) | investor |

### WP-2.7 — Square Marketplace Certification

Square OAuth, marketplace requirements, certification checklist.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-2.7.P | EXISTS | `Documents/Product_Guides/Canary_PRD_E2_Square_Marketplace_Certification_v1.0.docx` | internal |
| WP-2.7.P | EXISTS | `Documents/Product_Guides/Canary_Square_Certification_Checklist_v1.0.docx` | internal |
| WP-2.7.C | EXISTS | `Canary/canary/blueprints/square_oauth.py` + `square_oauth_wired.py` | internal |
| WP-2.7.T | STUB | — (certification test plan) | internal |

---

## WP-3: THE ARCHITECTURE

How it works. The pipeline, the databases, the data model, the gLog.

### WP-3.1 — Platform Architecture

Three-database model, capture pipeline, security, POS-agnostic design.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-3.1.N | EXISTS | `sources/08-the-architecture.md` | pack |
| WP-3.1.P | EXISTS | `Specs/Canary_Technology_Blueprint_v1.0.md` | internal |
| WP-3.1.P | EXISTS | `Specs/Canary_Technology_Blueprint_v1.1_Corrections.md` | internal |
| WP-3.1.P | EXISTS | `Specs/Canary_Functional_Requirements_v1.0.md` | internal |
| WP-3.1.P | EXISTS | `Specs/Canary_Technical_Requirements_v1.0.md` | internal |
| WP-3.1.R | EXISTS | `Strategy/Canary_Data_Strategy_NorthStar_v1.0.md` | internal |
| WP-3.1.R | EXISTS | `Specs/Flask_vs_FastAPI_DECISION_BRIEF.md` | internal |
| WP-3.1.R | EXISTS | `ADRs/ADR-PLA-001_Presentation_Layer_Architecture.md` | internal |
| WP-3.1.V | STUB | — (need: three-database SVG, capture pipeline SVG) | pack, investor |
| WP-3.1.A | STUB | — (need: consolidated API index / OpenAPI spec) | diligence |

### WP-3.2 — CRDM (Canary Retail Data Model)

Three generations. Seven canonical sources. The enterprise schema, now Bitcoin-native.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-3.2.N | EXISTS | `sources/09-the-data-model.md` | pack |
| WP-3.2.S | EXISTS | `Specs/CRDM_v1.0.md` | internal |
| WP-3.2.S | EXISTS | `Specs/Canary_CRDM_v1.0.md` | internal |
| WP-3.2.S | EXISTS | `Specs/GrowDirect_Unified_Data_Model_v1.0.md` | internal |
| WP-3.2.S | EXISTS | `Canary/canary/migrations/versions/000_create_app_tables.py` | internal |
| WP-3.2.S | EXISTS | `Canary/canary/migrations/versions/001_fox_insert_only_triggers.py` | internal |
| WP-3.2.S | EXISTS | `Canary/canary/migrations/versions/002_add_immutability_triggers_evidence_audit_tables.py` | internal |
| WP-3.2.S | EXISTS | `Canary/canary/migrations/versions/003_add_previous_chain_hash_case_evidence.py` | internal |
| WP-3.2.S | EXISTS | `Canary/canary/migrations/versions/004_add_hash_chain_triggers_and_verification.py` | internal |
| WP-3.2.D | EXISTS | `Specs/CRDM_Gap_Analysis_2026-02-20.md` | internal |
| WP-3.2.D | EXISTS | `Specs/Tom_CRDM_Schema_Review_2026-02-20.md` | internal |
| WP-3.2.D | EXISTS | `Archive/ARTS_Standards/ARTS_POSlog_to_Canary_Schema_Mapping_v1.0.md` | internal |
| WP-3.2.D | EXISTS | `Specs/Square_API_LP_Coverage_Analysis_Jeremy_v1.0.md` | internal |
| WP-3.2.V | STUB | — (need: ERD diagram, CRDM provenance timeline SVG) | diligence |
| WP-3.2.A | STUB | — (need: CRDM field dictionary / data dictionary) | diligence |

### WP-3.3 — Evidence Chain & Immutability

Three tiers of data integrity. Hash chain. INSERT-only. Append-only.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-3.3.N | DRAFT | (embedded in 08-the-architecture.md + 09-the-data-model.md) | pack |
| WP-3.3.S | EXISTS | `migrations/002_add_immutability_triggers_evidence_audit_tables.py` | internal |
| WP-3.3.S | EXISTS | `migrations/004_add_hash_chain_triggers_and_verification.py` | internal |
| WP-3.3.S | EXISTS | `canary/migrations/rls_policies.sql` | internal |
| WP-3.3.R | EXISTS | `output/Condor/PRD_StagedImmutabilityPipeline/` (9 files) | internal |
| WP-3.3.R | EXISTS | `output/PhD/PhD_StagedImmutability_BitcoinFrame_v1.0.md` | internal |
| WP-3.3.R | EXISTS | `output/PhD/PhD_StagedImmutability_PatentSchematic_v1.0.md` | internal |

### WP-3.4 — gLog (The Permanent Log)

Event sourcing on Bitcoin. Merkle batching. Ordinal inscription.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-3.4.N | DRAFT | (embedded in architecture.md, article.md, investment-thesis.md) | pack, investor |
| WP-3.4.R | EXISTS | `output/Condor/PRD_TripleSubscriberPipeline/` (9 files) | internal |
| WP-3.4.R | EXISTS | `output/PhD/PhD_B054_Brief5_TlogToGlog_v2.0.md` | internal |
| WP-3.4.V | STUB | — (need: gLog inscription flow SVG, tLog vs gLog comparison) | pack, investor |
| WP-3.4.A | STUB | — (need: jeffe.io API specification / OpenAPI) | diligence |
| WP-3.4.C | STUB | — (gLog inscription service not yet implemented) | internal |

### WP-3.5 — Multi-POS Translation Layer

POS-agnostic design. Square parser today. Clover, Toast, Shopify tomorrow.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-3.5.N | DRAFT | (embedded in architecture.md) | pack |
| WP-3.5.P | EXISTS | `Specs/Multi_POS_Translation_Layer_Architecture_v1.0.md` | internal |
| WP-3.5.C | EXISTS | `Canary/canary/services/parsers/` | internal |
| WP-3.5.D | EXISTS | `Archive/growdirect-v0/canary-rd/square_comprehensive_dataset/COMPREHENSIVE_SQUARE_SCHEMA_GUIDE.md` | internal |
| WP-3.5.D | EXISTS | `Research/MASTER_SCANNING_CONTEXT_v1.0.md` | internal |
| WP-3.5.V | STUB | — (need: POS-agnostic parser flow diagram) | pack |

### WP-3.6 — Security Architecture

RLS, RBAC, OAuth, TLS, webhook signature verification, L402.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-3.6.N | DRAFT | (embedded in architecture.md) | pack |
| WP-3.6.S | EXISTS | `devops/sql/rls_policies.sql` | internal |
| WP-3.6.C | EXISTS | `Canary/canary/permissions/` | internal |
| WP-3.6.C | EXISTS | `Canary/canary/auth/` | internal |
| WP-3.6.C | EXISTS | `Canary/canary/middleware/` | internal |
| WP-3.6.O | EXISTS | `devops/keycloak/` (identity management config) | internal |
| WP-3.6.T | STUB | — (need: security test plan, penetration test scope) | internal |

### WP-3.7 — Infrastructure & Deployment

Docker, multi-environment, Hasura, database initialization.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-3.7.O | EXISTS | `Canary/devops/docker-compose.yml` + variants (6 files) | internal |
| WP-3.7.O | EXISTS | `Canary/devops/Dockerfile` + nginx Dockerfile | internal |
| WP-3.7.O | EXISTS | `Canary/devops/hasura/metadata/` (3 schema configs) | internal |
| WP-3.7.O | EXISTS | `Canary/devops/init-db/01-create-databases.sql` | internal |
| WP-3.7.O | EXISTS | `Canary/infrastructure/` (phase 1-4 scripts) | internal |
| WP-3.7.R | EXISTS | `devops/README-DEV.md` | internal |
| WP-3.7.R | EXISTS | `devops/DEPLOYMENT_SUMMARY.md` | internal |
| WP-3.7.R | EXISTS | `devops/HAWK_INTEGRATION_PLAN.md` | internal |

---

## WP-4: THE BUSINESS

Why it wins. Market, model, economics, investment thesis.

### WP-4.1 — The Play (Business Model)

Seven layers from inscription pool to network effect. The elJeffe system.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-4.1.N | EXISTS | `sources/03-the-play.md` | pack |
| WP-4.1.R | EXISTS | `output/PhD/PhD_Layer5_BlockSpaceMoat_Thesis.md` | internal |
| WP-4.1.R | EXISTS | `output/PhD/PhD_Layer5_FeeWindowModel.md` | internal |
| WP-4.1.R | EXISTS | `output/PhD/PhD_Layer5_GenesisPool_CapitalThesis.md` | internal |
| WP-4.1.R | EXISTS | `output/PhD/PhD_Layer5_IPRangeAnalogy.md` | internal |
| WP-4.1.R | EXISTS | `output/PhD/PhD_Layer5_TrustCollapsisThesis.md` | internal |
| WP-4.1.R | EXISTS | `output/PhD/PhD_Layer5_VerticalIntegration_Thesis.md` | internal |
| WP-4.1.R | EXISTS | `_ALX/ElJeffe_BusinessModel_Addendum.md` | internal |
| WP-4.1.V | EXISTS | `sources/02-the-economy.html` (animated economy diagram) | pack, investor |
| WP-4.1.V | EXISTS | `sources/02-eljeffe.html` (orbital closed loop diagram) | internal |

### WP-4.2 — Investment Thesis

Five briefs. Block space, Genesis Pool, VeriSign parallel, vertical integration, tLog-to-gLog.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-4.2.N | EXISTS | `sources/09-investment-thesis.md` | pack, investor |
| WP-4.2.R | EXISTS | `output/PhD/PhD_B054_InvestorSiteCopy_v1.0.md` | internal |
| WP-4.2.R | EXISTS | `output/PhD/PhD_VeriSign_Analogy_InvestorBrief.md` | internal |
| WP-4.2.R | EXISTS | `output/PhD/PhD_BitcoinProtocol_PositionPaper_v1.0.md` | internal |
| WP-4.2.R | EXISTS | `Strategy/Canary_Strategic_Thesis_v1.0.md` | internal |

### WP-4.3 — Market Analysis

TAM/SAM/SOM. Beachhead. Competitive landscape. Timing.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-4.3.N | **STUB** | — (CRITICAL GAP: no market section exists) | pack, investor |
| WP-4.3.R | EXISTS | `Documents/White_Papers/Canary_Competitive_Landscape.docx` | internal |
| WP-4.3.R | EXISTS | `Strategy/CompetitiveIntel_Oracle_OCI_Polling.md` | internal |
| WP-4.3.R | EXISTS | `Research/Franchise_Targets.md` | internal |
| WP-4.3.D | EXISTS | `Documents/Sales_Decks/Canary_SoCal_Lead_Database_v1.0.xlsx` | internal |
| WP-4.3.V | STUB | — (need: TAM concentric circles diagram, competitor matrix) | investor |

### WP-4.4 — Financial Model

Revenue streams. Unit economics. Projections. Pricing tiers.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-4.4.N | **STUB** | — (CRITICAL GAP: no financial section exists) | investor, diligence |
| WP-4.4.D | STUB | — (need: unit economics model — CAC/LTV/ARPU/churn) | diligence |
| WP-4.4.D | STUB | — (need: revenue projections — 3-year illustrative) | investor |
| WP-4.4.D | STUB | — (need: pricing tier table with dollar amounts) | investor |
| WP-4.4.R | EXISTS | `Documents/White_Papers/Canary_Micropayment_Strategy_Position_Paper_v1.0.docx` | internal |
| WP-4.4.R | EXISTS | `output/PhD/PhD_StagedImmutability_VolumeAnalysis_v1.0.md` | internal |

### WP-4.5 — The Ask

Funding round. Use of proceeds. Milestones. What the money buys.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-4.5.N | **STUB** | — (CRITICAL GAP: no funding ask exists) | investor |
| WP-4.5.D | STUB | — (need: use of proceeds breakdown) | investor |
| WP-4.5.D | STUB | — (need: milestone timeline) | investor |

### WP-4.6 — Go-to-Market

Merchant acquisition. Sales motion. Channel strategy. Partnership playbook.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-4.6.N | **STUB** | — (CRITICAL GAP: no GTM plan exists) | investor |
| WP-4.6.R | EXISTS | `output/Will/Will_gLog_LEO_Terms.md` | internal |
| WP-4.6.R | EXISTS | `output/MerchantPitchScript_Phase2_v1.0.md` | internal |
| WP-4.6.R | EXISTS | `output/PhD/PhD_MerchantWeapon_Brief_v1.0.md` | internal |
| WP-4.6.V | STUB | — (need: sales funnel diagram, merchant journey map) | internal |

### WP-4.7 — Business Plan

Company overview, business plan narrative, DAO structure.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-4.7.N | DRAFT | `Documents/Product_Guides/Canary_Business_Plan_v1.0.md` | internal |
| WP-4.7.R | EXISTS | `Company/GrowDirect_DAO_Plan.md` | internal |
| WP-4.7.R | EXISTS | `Documents/White_Papers/Canary_Project_White_Paper_v1.3.docx` | internal |

---

## WP-5: THE SHIELD

Protection and compliance. Patent, trademark, trade secret, regulatory.

### WP-5.1 — Compliance by Construction

Architecture eliminates the mutable record. PII protection. Framework mapping.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-5.1.N | EXISTS | `sources/12-compliance.md` | pack, investor |
| WP-5.1.R | EXISTS | `output/PhD/PhD_B053_ComplianceByConstruction_Brief.md` | internal |
| WP-5.1.R | EXISTS | `output/Syd/Syd_B058_InvestorContentReview_v1.0.md` | internal |

### WP-5.2 — IP Protection

Patent, trademark, trade secret, temporal moat. **CONFIDENTIAL — not for external outputs.**

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-5.2.N | CONFIDENTIAL | `sources/13-protection.md` | pack (redacted summary only) |
| WP-5.2.L | CONFIDENTIAL | `output/Syd/Syd_PatentAssessment_StagedImmutability_v1.0.md` | legal |
| WP-5.2.L | CONFIDENTIAL | `output/Syd/Syd_IP_Protection_Strategy_v1.0.md` | legal |
| WP-5.2.L | CONFIDENTIAL | `output/Syd/Syd_B055_IPExposureAudit_v1.0.md` | legal |
| WP-5.2.L | CONFIDENTIAL | `output/Syd/Syd_PreDemo_IPChecklist_v1.0.md` | legal |
| WP-5.2.N | STUB | — (need: REDACTED external IP summary — general statement only) | investor |

### WP-5.3 — Legal Agreements

Merchant NDA, beta tester agreement, data processing, liability.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-5.3.L | EXISTS | `output/Syd/Syd_MerchantNDA_v1.0.md` | legal |
| WP-5.3.L | EXISTS | `output/Syd/Syd_BetaTesterAgreement_v1.0.md` | legal |
| WP-5.3.L | EXISTS | `output/Syd/Syd_DemoLiabilityWaiver_v1.0.md` | legal |
| WP-5.3.L | EXISTS | `output/Syd/Syd_DataProcessingAddendum_v1.0.md` | legal |

### WP-5.4 — Regulatory & Licensing

License audit, money transmitter analysis, privacy policy, terms.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-5.4.L | EXISTS | `Documents/Legal/ALPHA3X_LICENSE_REVIEW_INDEX.md` | internal |
| WP-5.4.L | EXISTS | `Documents/Legal/Canary_Alpha3X_License_Executive_Summary.md` | internal |
| WP-5.4.L | EXISTS | `Documents/Legal/privacy-policy.html` | public |
| WP-5.4.L | EXISTS | `Documents/Legal/terms-of-use.html` | public |
| WP-5.4.L | EXISTS | `Documents/Legal/legal-disclaimer.html` | public |
| WP-5.4.L | STUB | — (need: money transmitter analysis for Goose — Syd flagged URGENT) | legal |

### WP-5.5 — DAO Governance

Articles of organization, operating agreement, governance contract.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-5.5.L | EXISTS | `Documents/Legal/GrowDirect_DAO_LLC_Articles_of_Organization_v1.0.docx` | legal |
| WP-5.5.L | EXISTS | `Documents/Legal/GrowDirect_DAO_LLC_Operating_Agreement_v1.0.docx` | legal |
| WP-5.5.L | EXISTS | `Documents/Legal/GrowDirect_DAO_Governance_Contract.sol` | legal |
| WP-5.5.L | EXISTS | `Documents/Legal/GrowDirect_DAO_Attorney_Handoff_Memo_v1.0.docx` | legal |
| WP-5.5.L | EXISTS | `Documents/Legal/GrowDirect_DAO_Filing_Checklist_v1.0.docx` | legal |

### WP-5.6 — Manifesto Disclaimers

Forward-looking statements, not-advice, patent notice, confidentiality.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-5.6.N | **STUB** | — (need: standard disclaimer block for all external outputs) | investor, public |

---

## WP-6: THE OPERATIONS

How we build and who builds it.

### WP-6.1 — Factory Process

Six-stage build process. Gates. Scope discipline. Sprint methodology.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-6.1.N | EXISTS | `sources/10-how-we-build.md` | pack |
| WP-6.1.R | EXISTS | `Strategy/Canary_Factory_Process_v1.0.md` | internal |

### WP-6.2 — Sprint State

Attack plan. Active sprint. Nearest gate. Velocity.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-6.2.R | EXISTS | `Strategy/Canary_Attack_Plan_v3.0.md` (ACTIVE) | internal |
| WP-6.2.R | EXISTS | `Strategy/Canary_Sprint_Build_Plan_2026-02-18_v1.0.md` | internal |
| WP-6.2.R | EXISTS | `Strategy/Canary_Sprint3_Plan_2026-02-20_v1.0.md` | internal |
| WP-6.2.R | EXISTS | `Strategy/Canary_Sprint5_Integration_Plan_v1.0.md` | internal |
| WP-6.2.R | EXISTS | `Strategy/Alpha3X_Replan_Sprint3_to_UAT_2026-02-22.md` | internal |

### WP-6.3 — Coding Standards & DevOps

Standards, CI/CD, deployment topology, environment strategy.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-6.3.R | EXISTS | `Specs/Canary_Coding_Standards_v1.0.md` | internal |
| WP-6.3.O | EXISTS | `Canary/devops/` (full Docker/Hasura/Keycloak stack) | internal |
| WP-6.3.R | EXISTS | `Documents/Product_Guides/Canary_Environment_Strategy_v1.1.docx` | internal |
| WP-6.3.R | EXISTS | `devops/HAWK_INTEGRATION_PLAN.md` | internal |

### WP-6.4 — QA & Testing

Test plans, QA processes, alpha gate reviews, UAT.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-6.4.T | EXISTS | `Canary/tests/` (test suite) | internal |
| WP-6.4.R | EXISTS | `Specs/QA_Testing_Guide.md` | internal |
| WP-6.4.R | EXISTS | `output/Jim/Jim_1B_Alpha_Gate_Review.md` | internal |
| WP-6.4.R | EXISTS | `output/Jim/Jim_LevelB_UAT_Plan.md` | internal |
| WP-6.4.R | EXISTS | `output/Jim/Jim_CoffeeShop_SeedData_Spec.md` | internal |
| WP-6.4.R | EXISTS | `QA/Alpha_v0.1.0_QA_Handoff.md` | internal |
| WP-6.4.R | EXISTS | `QA/Production_Audit_Report_2026-02-20.md` | internal |

### WP-6.5 — Brand & Design System

Brand guide, design tokens, visual assets, lockups.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-6.5.V | EXISTS | `Company/Brand/BRAND_GUIDE*.html` (3 versions) | internal |
| WP-6.5.V | EXISTS | `Company/Brand/favicon/` (7 files) | public |
| WP-6.5.V | EXISTS | `Company/Brand/icon/` (8 files) | public |
| WP-6.5.V | EXISTS | `Company/Brand/lockup/` (8 files) | public |
| WP-6.5.V | EXISTS | `Company/Brand/social/` (6 files) | public |
| WP-6.5.R | EXISTS | `output/Jess/Jess_ArchDiagram_Standard_v1.0.md` | internal |

---

## WP-7: THE REFERENCE LIBRARY

Deep technical reference. Research briefs, API indexes, data dictionaries.

### WP-7.1 — API Reference

Consolidated endpoint index. Route documentation. Swagger/OpenAPI.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-7.1.A | STUB | — (need: consolidated OpenAPI spec from all 21 blueprint files) | diligence |
| WP-7.1.C | EXISTS | `Canary/canary/blueprints/registry.py` (route registration) | internal |
| WP-7.1.T | EXISTS | `Canary/tests/test_route_coverage.py` | internal |
| WP-7.1.T | EXISTS | `Canary/tests/test_smoke_routes.py` | internal |

### WP-7.2 — Data Dictionary

CRDM field-level reference. Column definitions. Type mappings. Source lineage.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-7.2.D | STUB | — (need: field-level data dictionary from CRDM spec + migration files) | diligence |
| WP-7.2.S | EXISTS | `Specs/CRDM_v1.0.md` (canonical schema spec) | internal |
| WP-7.2.D | EXISTS | `Specs/SCHEMA_QUICK_REFERENCE.md` | internal |
| WP-7.2.D | EXISTS | `Specs/README_SCHEMA_DELIVERABLES.md` | internal |
| WP-7.2.S | EXISTS | `Documents/Product_Guides/Canary_Platform_Schema_Complete_v1.0.docx` | internal |
| WP-7.2.D | EXISTS | `Specs/Appriss_Retail_Data_Spec_Analysis_v1.0.md` | internal |

### WP-7.3 — Research Library

PhD briefs, position papers, competitive intelligence.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-7.3.R | EXISTS | `Research/Canary_Reference_Library_v1.0.md` | internal |
| WP-7.3.R | EXISTS | `Research/Canary_Alpha3X_Stack_References_v1.0.md` | internal |
| WP-7.3.R | EXISTS | `Research/Canary_Bitcoin_Architecture_Research_Paper_v1.0.md` | internal |
| WP-7.3.R | EXISTS | `Research/glossary.md` | internal |
| WP-7.3.R | EXISTS | `output/PhD/` (18 research briefs) | internal |

### WP-7.4 — Architecture Diagrams

All system diagrams, flow charts, visual architecture assets.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-7.4.V | EXISTS | `output/Jess/diagrams/Canary_ComponentDiagram_DualSubscriber_v1.0.md` | internal |
| WP-7.4.V | EXISTS | `output/Jess/diagrams/Canary_DataFlow_SingleTransaction_v1.0.md` | internal |
| WP-7.4.V | STUB | — (need: "How It All Fits" system diagram SVG) | pack, investor |
| WP-7.4.V | STUB | — (need: moat rings diagram SVG) | investor |
| WP-7.4.V | STUB | — (need: before/after tLog vs gLog comparison) | investor |
| WP-7.4.V | STUB | — (need: career arc timeline SVG) | investor |

### WP-7.5 — White Papers

Published research, quant analysis, peer reviews.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-7.5.R | EXISTS | `Documents/White_Papers/Canary_Project_White_Paper_v1.3.docx` | internal |
| WP-7.5.R | EXISTS | `Documents/White_Papers/Canary_Quant_Peer_Review_v1.0.docx` | internal |
| WP-7.5.R | EXISTS | `Documents/White_Papers/Canary_Micropayment_Strategy_Position_Paper_v1.0.docx` | internal |
| WP-7.5.R | EXISTS | `Documents/White_Papers/Canary_Competitive_Landscape.docx` | internal |

### WP-7.6 — Sales & Outreach Assets

Pitch decks, merchant scripts, lead databases, press releases.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-7.6.V | EXISTS | `Documents/Sales_Decks/GrowDirect_Thesis_v1.0.pptx` | internal |
| WP-7.6.V | EXISTS | `Documents/Sales_Decks/Canary_Square_Opportunity.pptx` | internal |
| WP-7.6.R | EXISTS | `Press/Canary_Press_Release_Founding_Announcement_v1.0.md` | public |
| WP-7.6.R | EXISTS | `Press/Canary_Press_Release_v2.0_Syd_Revision.md` | public |

### WP-7.7 — PRD Library

All product requirements documents, indexed by epic.

| Asset | Status | Source File | Outputs |
|---|---|---|---|
| WP-7.7.P | EXISTS | `Documents/Product_Guides/Canary_PRD_E0_Platform_Foundation_v1.0.docx` | internal |
| WP-7.7.P | EXISTS | `Documents/Product_Guides/Canary_PRD_E1_Core_Fraud_Detection_v1.0.docx` | internal |
| WP-7.7.P | EXISTS | `Documents/Product_Guides/Canary_PRD_E2_Square_Marketplace_Certification_v1.0.docx` | internal |
| WP-7.7.P | EXISTS | `Documents/Product_Guides/Canary_PRD_E3_Fox_Case_Management_v1.0.docx` | internal |
| WP-7.7.P | EXISTS | `Documents/Product_Guides/Canary_PRD_E0F6_Guided_Companion_v1.0.docx` | internal |
| WP-7.7.P | EXISTS | `Documents/Product_Guides/Canary_PRD_E9_Chirp_UDQ_Lightning_Metering_v1.0.docx` | internal |
| WP-7.7.P | EXISTS | `Documents/Product_Guides/Canary_PRD_E9_PaaS_API_Gateway_Data_Services_v1.0.docx` | internal |
| WP-7.7.P | EXISTS | `Documents/Product_Guides/Canary_PRD_PaaS_Franchise_Module_v1.0.docx` | internal |

---

## Critical Gaps Summary

Nodes that block the manifesto and investor readiness, ordered by priority:

| Priority | WP Node | Gap | Owner | Blocker For |
|---|---|---|---|---|
| **P0** | WP-4.4 | Financial Model — no revenue model, no unit economics, no projections | Jeffe (input) | investor, diligence |
| **P0** | WP-4.5 | The Ask — no funding round, no use of proceeds | Jeffe (input) | investor |
| **P0** | WP-5.6 | Disclaimers — no standard disclaimer block for external outputs | Syd | investor, public |
| **P1** | WP-4.3 | Market Analysis — no TAM/SAM/SOM, no competitor matrix | PhD + Jeffe | investor |
| **P1** | WP-4.6 | GTM Plan — no merchant acquisition strategy | Will + Jeffe | investor |
| **P1** | WP-5.2 | IP Redacted Summary — need external-safe version of protection.md | Syd | investor |
| **P1** | WP-5.4 | Money Transmitter Analysis — Goose legal classification | Syd | legal |
| **P2** | WP-7.1 | API Reference — no consolidated OpenAPI spec | Jeremy | diligence |
| **P2** | WP-7.2 | Data Dictionary — no field-level CRDM reference | Tom | diligence |
| **P2** | WP-7.4 | Architecture SVGs — ASCII diagrams need proper visual treatment | Art | pack, investor |
| **P2** | WP-3.4 | gLog standalone narrative — currently embedded across 3 files | PhD | pack |
| **P3** | WP-2.1 | Canary Core investor narrative — no standalone overview exists | Jess | investor |
| **P3** | WP-1.4 | North Star standalone piece | Jess | public |

---

## Naming Conventions (Canonical — Tom-approved)

| Term | Correct Form | Wrong Forms |
|---|---|---|
| elJeffe | `elJeffe` (camelCase, no space) | El Jeffe, ElJeffe, el jeffe |
| gLog | `gLog` (camelCase) | Glog, GLOG, g-log |
| tLog | `tLog` (camelCase) | Tlog, TLOG, t-log |
| timechain | `timechain` (one word) | time chain, time-chain |
| Canary LP | `Canary LP` (first mention), `Canary` (subsequent) | canary, CANARY |
| GrowDirect | `GrowDirect` (one word, two caps) | Grow Direct, growdirect |
| Chirp | `Chirp` (capitalized — branded feature) | chirp, CHIRP |
| jeffe.io | `jeffe.io` (lowercase) | Jeffe.io, JEFFE.IO |
| CRDM | `CRDM` (all caps) | Crdm, crdm |

---

## Output Target Map

How WP nodes flow to published outputs:

```
WP-1 (Narrative)  ──► pack, investor, public
WP-2 (Product)    ──► pack, investor (summaries), diligence (full specs)
WP-3 (Architecture) ──► pack (overview), diligence (full detail)
WP-4 (Business)   ──► investor (primary), pack (thesis sections)
WP-5 (Shield)     ──► investor (redacted), legal (full), pack (compliance only)
WP-6 (Operations) ──► pack (process), internal (everything else)
WP-7 (Reference)  ──► diligence (API/data dictionary), internal (research)
```

---

## Version History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-02-27 | Initial Working Papers index — full tree with 7 domains, 37 chapters, all existing assets mapped, all gaps stubbed |

---

*GrowDirect Confidential*
*Patent Pending — Provisional 63/991,596*
