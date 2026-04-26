---
classification: internal
type: wiki
date: 2026-04-25
last-compiled: 2026-04-25
needs-review: 2026-05-09
source-archive: /Volumes/My Passport/CLIENTS/DELIVERY/ + /Volumes/My Passport/macpro/Users/geoff/Documents/ (sanitized)
provenance: Brain/wiki/founder-context-secure-engagement-archive.md
---

# Solution Description — Document Template

A reusable template for "Solution Description" documents — the artifact that explains how a proposed integration will work, written for a mid-technical audience at the customer plus the delivery team. This is one of the early Elaboration-phase deliverables in the cross-engagement delivery framework (artifact H, Solution Architecture and Solution Design). Use as the starting structure for any Canary integration solution-description.

## Audience and intent

**Audience:** customer's IT lead and customer's project manager (mid-technical), plus the delivery team (technical). Not for executives — it has too much detail. Not for developers — it does not have enough detail.

**Intent:** to make the integration understandable and contractable. The reader should finish the document able to (a) explain the integration to a colleague, (b) identify the network and infrastructure that needs to be in place, (c) recognize the data structures the customer is committing to maintain.

**What it is not:** not a contract, not a Statement of Work, not a low-level technical specification. It is a shared mental model document.

## Length and format

- **5 to 8 pages typical.** Shorter loses contractibility; longer loses readability.
- **Word document with one architecture diagram, optional UI screenshots, one or two data-format examples.**
- **Single author, single version line.** Treat as a living doc with versions, not a static deliverable.
- **No code. No SQL. No configuration files.** Those belong in deeper artifacts (interface specs, configuration checklist).

## Structure (eight sections)

The exemplar followed a tight structure. Use it as the skeleton.

### 1. Document Version History

A table at the very top. Four columns: Author, Date Issued, Version, Comment. One row per revision. The first row is `1.0.0 — Generic architecture document` (the initial version). Subsequent rows are revisions in response to customer feedback.

The version table is governance metadata. It tells any reader, immediately, who owns the document and how mature it is. A solution description without a version table is not yet a deliverable — it is a draft.

### 2. Introduction

Two to three sentences. Says what the document describes (the integration in question) and what the integration is for (the analyst outcome).

State the two parties of the integration: "the platform" (your product) and "the customer's [system]" (the third-party system being integrated). Avoid product names that could change; refer to the platform by its product family.

Then a bullet list of "the following new components will be added" — this is the document's headline. The reader, after reading the bullet list, should know the shape of the integration.

### 3. High-Level Integration Architecture

The diagram + the prose explaining the diagram.

**Diagram requirements:**
- Show the customer's network and the platform's network as separate boxes.
- Show every system involved: source systems (DVR, POS, ERP), platform, analyst client.
- Show the data paths and label each arrow with the protocol and direction (HTTPS, SFTP, push/pull, on-demand vs scheduled).
- Annotate any cross-boundary arrows with security implications (CORS, VPN, mutual TLS).

**Prose requirements:**
- One paragraph per arrow, explaining what flows when.
- One paragraph on what the integration assumes about the customer's network (reachability, browser configuration, latency budgets).
- One paragraph on what the integration does NOT do (push events, store data, synchronize state).

### 4. UI Walkthrough

Step-by-step description of what the analyst experiences. Imperative voice ("the analyst clicks the camera icon"). Two to four screenshots if available. The walkthrough should be concrete enough that a customer reader can imagine themselves using it, but not so detailed that minor UI changes invalidate the document.

This section is the most likely to bond the reader to the integration. Spend the screenshots here.

### 5. Data Structures and Reference Data

A field-by-field table for any data structure the customer is responsible for maintaining. The exemplar's camera-reference-table table is the model — one row per field, columns for field name and purpose. Do not specify SQL types here; that is for the interface spec.

Include:
- File format (delimiter, encoding, line terminator)
- Field list with purpose
- Notes on uniqueness, nullability, and any reserved fields for forward compatibility
- A statement of who maintains this data (customer feed, vendor feed, joint maintenance)

### 6. Examples

At least one concrete data sample. The exemplar shows one example camera-reference-data row. Examples make the document executable: they let a customer reader build a mental model of "what would my data look like in this format?"

If file-based, show a complete sample file (3-5 rows). If API-based, show a complete request/response pair.

### 7. Operational Considerations

Half a page. The pragmatic gotchas the integration will surface:
- Network access requirements
- Browser configuration (CORS, allowed origins)
- Credential storage and rotation
- Time zone handling
- Failure modes the customer should know about

This section is the document's truthfulness test. A solution description that omits operational considerations reads as a sales document, not a delivery document. Customers learn to distrust the latter.

### 8. (Optional) Privacy and Security Posture

Half a page. Required when the integration touches personal data, surveillance footage, biometrics, financial records, or anything regulated.

Cover:
- What personal data flows where
- What is stored vs streamed-only
- Who is the controller for each data type (platform vendor vs customer)
- How DSARs (data-subject access requests) and deletion requests are fulfilled
- Audit-trail provisions

For a clean integration that streams without storing (the pattern in the exemplar), this section can be brief. For an integration that ingests and retains, it must be thorough.

## Sections to add for Canary engagements

The exemplar predates the cloud-native era and the post-GDPR privacy bar. For modern Canary solution descriptions, add three sections to the eight above:

### 9. Identifiers, IDs, and Token Format

Specifies the key model. For each identifier the integration uses: format (UUID, opaque string, ULID), generation owner (platform, customer, third-party), uniqueness scope (global, per-tenant, per-customer), and lifecycle (when minted, when retired).

This section is what lets a developer build the integration without slack. Without it, every implementation question becomes a customer call.

### 10. Failure Modes and Error Handling

A table of failure modes. Columns: Failure, Symptom, Root cause, Recovery. Five to ten rows.

This section is the most-skipped, most-valuable. Customers who read it trust the document.

### 11. Monitoring and Observability

What the customer can see. What the platform vendor can see. What metrics are emitted, what dashboards exist, what alerts fire and to whom. For SaaS deployments, what the customer's status-page experience looks like during a partial outage.

### 12. Deployment Topology

Whether the integration is per-tenant, multi-tenant, region-specific. Whether tenant data is isolated at network, database, or application level. Whether failover is hot, warm, or cold. Whether DR is in-region or cross-region.

For a packaged SaaS platform like Canary, this is increasingly contractual.

### 13. Decommissioning and Data Deletion

How the customer offboards. What data the platform vendor retains after offboarding. What the customer can export. What the deletion timeline is. What is the data-residency posture for retained metadata vs purged user data.

This section is what GDPR Article 17 ("right to erasure") requires of every modern integration.

## Style conventions

- **Imperative voice** for behavior: "the platform connects to the DVR", not "the platform will connect."
- **Plain English noun phrases** for system names: "the platform", "the DVR", "the customer's network." Avoid product-specific noun phrases that the document will outlive.
- **No marketing adjectives.** "Seamless", "robust", "industry-leading" do not belong in a solution description. They erode trust with a technical reader.
- **Diagrams over prose** where possible. A clear diagram replaces three paragraphs of network description.
- **Tables for data and configuration.** Tables make field-by-field reading scannable.
- **Citation of supporting docs.** Reference deeper docs (interface spec, configuration checklist, support and operations guide) by name; do not duplicate their content.

## Versioning and ownership

The Document Version History table (Section 1) is the governance contract. Conventions:

- **Major version (1.x.x → 2.x.x)** — architectural change. New diagram, possibly new components.
- **Minor version (1.0.x → 1.1.x)** — feature addition. New section or new field, no architectural change.
- **Patch version (1.0.0 → 1.0.1)** — clarification, typo, additional example. No technical change.

The author is a single person, named in the table. Reviews from delivery, support, and customer-services should be acknowledged in the comment column but should not appear as additional authors. One author per document keeps editorial responsibility clear.

## Where this template fits in the engagement

The Solution Description is produced during Elaboration (per the cross-engagement delivery framework). It is one of the artifacts that satisfies Quality Gate 2 (Scope: Are the requirements defined?). It is shared with the customer for review and approval before Gate 3 (Plan: Can we do it within time and budget?).

Specifically:
- Drafted by the Tech Lead during the "Document Proposed Solution" task in Elaboration.
- Reviewed at the Design Authority workshop (W3).
- Approved by the customer before development begins.
- Updated through versioning during Construction if scope changes.
- Referenced by the Support and Operations Guide (artifact L) at handover.
- Becomes the single source of truth for "what was built and why" after the engagement closes.

A Solution Description that ages well — that remains accurate three years after handover — is the artifact future support engineers and future Canary engagements will rely on. Write it for that future reader, not for the customer's current PM.
