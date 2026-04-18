---
type: spec
domain: fox
status: active
created: 2026-03-19
updated: 2026-03-19
---
# Fox Case Management System — Data Model v2.0
**GSLM-Enhanced Edition**

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]

**Version:** 2.0
**Date:** February 17, 2026
**Author:** Tom (Systems Architect) + Jeremy (Developer Quant)
**Status:** Engineering Ready — Sprint 1 Approved
**Based On:** GSLM Entity Pattern Analysis + Fox Technical Specification v1.0

---

## Document Purpose

This specification defines the complete data model for the Fox Case Management System, incorporating enterprise retail data modeling patterns from the Global Source Logic Model (GSLM). The design ensures Fox can scale from small Square merchants to enterprise retail operations while maintaining data integrity, audit compliance, and forensic evidence standards.

---

## Design Principles

### 1. GSLM-Inspired Patterns
- **Effective Dating**: All entities track temporal validity (`created_at`, `updated_at`, `effective_date`, `expiry_date`)
- **Status Tracking**: Explicit status codes with state transition history
- **Many-to-Many Relationships**: Junction tables for complex relationships (cases ↔ subjects, evidence ↔ cases)
- **Hierarchical Entities**: Parent-child relationships for organizational structures
- **Attribute Localization**: Separation of base records from localized/narrative content

### 2. Forensic Integrity
- **Immutable Evidence**: Evidence records are append-only; modifications create new versions
- **Chain of Custody**: Every evidence item tracks custody transfers with timestamps
- **Audit Trail**: All state changes logged to timeline with actor attribution
- **Cryptographic Verification**: Hash-chained timeline events for tamper detection

### 3. Bitcoin-Native Architecture
- **Lightning Payments**: Case submission fees tracked in `lightning_payments` table
- **BOLO Network Staking**: Merchant reputation tracked in `merchant_stakes` table
- **Decentralized Identity**: LNURL-auth pubkeys as primary identity primitive
- **Economic Incentives**: Stake-based network access prevents spam/abuse

---

## Entity Relationship Overview

### Core Entities (Sprint 1)
1. **fox_cases** — Case master record
2. **fox_subjects** — Individuals/entities under investigation
3. **fox_evidence** — Evidence items (photos, videos, documents, transactions)
4. **fox_timeline_events** — Chronological case activity log
5. **fox_case_notes** — Narrative investigation notes
6. **fox_attachments** — File storage metadata
7. **fox_case_status_history** — State transition audit trail

### Junction Tables (Sprint 1)
8. **fox_case_subjects** — Many-to-many: cases ↔ subjects
9. **fox_evidence_cases** — Many-to-many: evidence ↔ cases

### Extended Entities (Sprint 2+)
10. **fox_bolo_alerts** — Be On the Lookout network alerts
11. **fox_bolo_confirmations** — Merchant confirmations of BOLO matches
12. **fox_evidence_custody_log** — Chain of custody transfers
13. **fox_case_collaborators** — Multi-merchant case sharing
14. **fox_external_reports** — Law enforcement/insurance integration

---

## Entity Definitions

## 1. fox_cases

**Description:** Master record for all Fox cases. A case represents a formal investigation into suspicious activity, fraud, theft, or policy violation. Cases aggregate evidence, subjects, notes, and timeline events into a single investigative package.

**GSLM Pattern:** Mirrors `SKUItem` structure with status tracking, effective dating, and parent-child relationships.

| Attribute | Type | Nullable | Default | Description |
|-----------|------|----------|---------|-------------|
| **case_id** | SERIAL | NOT NULL | PK | Unique case identifier (auto-increment) |
| **case_number** | VARCHAR(50) | NOT NULL | UNIQUE | Human-readable case number (e.g., "CASE-2026-00123") |
| **merchant_id** | INTEGER | NOT NULL | FK | Foreign key to `merchants` table |
| **alert_id** | INTEGER | NULL | FK | Foreign key to `alerts` table (if case originated from Canary alert) |
| **case_title** | VARCHAR(255) | NOT NULL | | Short case description (e.g., "Employee theft - Register 3") |
| **case_description** | TEXT | NULL | | Detailed initial case description |
| **case_status_code** | VARCHAR(20) | NOT NULL | 'open' | Current status: 'open', 'investigating', 'resolved', 'closed', 'archived' |
| **case_type_code** | VARCHAR(50) | NULL | | Case category: 'theft', 'fraud', 'refund_abuse', 'policy_violation', 'vendor_fraud', 'safety', 'other' |
| **priority_code** | VARCHAR(20) | NOT NULL | 'medium' | Priority: 'low', 'medium', 'high', 'critical' |
| **severity_score** | INTEGER | NULL | | Numeric severity (1-10) for sorting/filtering |
| **estimated_loss_amount** | DECIMAL(10,2) | NULL | | Estimated financial loss (USD) |
| **actual_loss_amount** | DECIMAL(10,2) | NULL | | Confirmed financial loss after investigation |
| **recovery_amount** | DECIMAL(10,2) | NULL | | Amount recovered (restitution, insurance, etc.) |
| **assigned_to_user_id** | INTEGER | NULL | FK | User assigned to investigate case |
| **created_by_user_id** | INTEGER | NOT NULL | FK | User who created the case |
| **parent_case_id** | INTEGER | NULL | FK | Parent case (for related/linked cases) |
| **effective_date** | TIMESTAMP | NOT NULL | NOW() | When case officially opened |
| **target_close_date** | TIMESTAMP | NULL | | Target resolution date |
| **actual_close_date** | TIMESTAMP | NULL | | Actual resolution date |
| **created_at** | TIMESTAMP | NOT NULL | NOW() | Record creation timestamp |
| **updated_at** | TIMESTAMP | NOT NULL | NOW() | Last update timestamp |
| **deleted_at** | TIMESTAMP | NULL | | Soft delete timestamp |

**Indexes:**
- PRIMARY KEY (`case_id`)
- UNIQUE INDEX (`case_number`)
- INDEX (`merchant_id`, `case_status_code`)
- INDEX (`created_at` DESC)
- INDEX (`priority_code`, `case_status_code`)

**Constraints:**
- FOREIGN KEY (`merchant_id`) REFERENCES `merchants(id)`
- FOREIGN KEY (`alert_id`) REFERENCES `alerts(id)`
- FOREIGN KEY (`assigned_to_user_id`) REFERENCES `users(id)`
- FOREIGN KEY (`created_by_user_id`) REFERENCES `users(id)`
- FOREIGN KEY (`parent_case_id`) REFERENCES `fox_cases(case_id)`
- CHECK (`case_status_code` IN ('open', 'investigating', 'resolved', 'closed', 'archived'))
- CHECK (`priority_code` IN ('low', 'medium', 'high', 'critical'))
- CHECK (`severity_score` BETWEEN 1 AND 10)

---

## 2. fox_subjects

**Description:** Individuals or entities under investigation. A subject can be an employee, customer, vendor, contractor, or external party. Subjects can be associated with multiple cases through the `fox_case_subjects` junction table.

**GSLM Pattern:** Mirrors `Merchandise` logical entity with hierarchical relationships and multiple identifier types (like `ArticleItem` supports UPC/PLU/EAN).

| Attribute | Type | Nullable | Default | Description |
|-----------|------|----------|---------|-------------|
| **subject_id** | SERIAL | NOT NULL | PK | Unique subject identifier |
| **merchant_id** | INTEGER | NOT NULL | FK | Foreign key to `merchants` table |
| **subject_type_code** | VARCHAR(50) | NOT NULL | | Type: 'employee', 'customer', 'vendor', 'contractor', 'external', 'unknown' |
| **subject_status_code** | VARCHAR(20) | NOT NULL | 'active' | Status: 'active', 'suspended', 'terminated', 'cleared', 'unknown' |
| **parent_subject_id** | INTEGER | NULL | FK | Parent subject (for organizational hierarchies) |
| **first_name** | VARCHAR(100) | NULL | | Subject first name |
| **last_name** | VARCHAR(100) | NULL | | Subject last name |
| **display_name** | VARCHAR(255) | NULL | | Preferred display name |
| **employee_id** | VARCHAR(50) | NULL | | Employee identifier (if employee) |
| **external_id** | VARCHAR(100) | NULL | | External system identifier (POS, HR, vendor system) |
| **email** | VARCHAR(255) | NULL | | Email address |
| **phone** | VARCHAR(50) | NULL | | Phone number |
| **address_line1** | VARCHAR(255) | NULL | | Street address |
| **address_line2** | VARCHAR(255) | NULL | | Apartment/unit |
| **city** | VARCHAR(100) | NULL | | City |
| **state** | VARCHAR(50) | NULL | | State/province |
| **postal_code** | VARCHAR(20) | NULL | | ZIP/postal code |
| **country** | VARCHAR(50) | NULL | 'US' | Country code |
| **date_of_birth** | DATE | NULL | | Date of birth (if known) |
| **ssn_last4** | VARCHAR(4) | NULL | | Last 4 of SSN (encrypted at rest) |
| **notes** | TEXT | NULL | | General notes about subject |
| **risk_score** | INTEGER | NULL | | Risk score (0-100) based on case history |
| **total_cases** | INTEGER | NOT NULL | 0 | Count of associated cases |
| **total_loss_amount** | DECIMAL(10,2) | NOT NULL | 0.00 | Cumulative loss across all cases |
| **effective_date** | TIMESTAMP | NOT NULL | NOW() | When subject record became effective |
| **expiry_date** | TIMESTAMP | NULL | | When subject record expires (e.g., contractor term end) |
| **created_at** | TIMESTAMP | NOT NULL | NOW() | Record creation timestamp |
| **updated_at** | TIMESTAMP | NOT NULL | NOW() | Last update timestamp |
| **deleted_at** | TIMESTAMP | NULL | | Soft delete timestamp |

**Indexes:**
- PRIMARY KEY (`subject_id`)
- INDEX (`merchant_id`, `subject_type_code`)
- INDEX (`employee_id`)
- INDEX (`external_id`)
- INDEX (`email`)
- INDEX (`risk_score` DESC)
- FULLTEXT INDEX (`first_name`, `last_name`, `display_name`)

**Constraints:**
- FOREIGN KEY (`merchant_id`) REFERENCES `merchants(id)`
- FOREIGN KEY (`parent_subject_id`) REFERENCES `fox_subjects(subject_id)`
- CHECK (`subject_type_code` IN ('employee', 'customer', 'vendor', 'contractor', 'external', 'unknown'))
- CHECK (`subject_status_code` IN ('active', 'suspended', 'terminated', 'cleared', 'unknown'))
- CHECK (`risk_score` BETWEEN 0 AND 100)

---

## 3. fox_evidence

**Description:** Evidence items attached to cases. Evidence can be photos, videos, documents, transaction logs, witness statements, or physical items. Evidence records are immutable; modifications create new versions with custody trail.

**GSLM Pattern:** Mirrors `PackItem` structure with many-to-many relationships and chain of custody tracking (like pack-to-SKU breakout).

| Attribute | Type | Nullable | Default | Description |
|-----------|------|----------|---------|-------------|
| **evidence_id** | SERIAL | NOT NULL | PK | Unique evidence identifier |
| **merchant_id** | INTEGER | NOT NULL | FK | Foreign key to `merchants` table |
| **evidence_type_code** | VARCHAR(50) | NOT NULL | | Type: 'receipt', 'video', 'photo', 'document', 'transaction', 'witness_statement', 'physical_item', 'other' |
| **evidence_number** | VARCHAR(50) | NOT NULL | UNIQUE | Human-readable evidence number (e.g., "EV-2026-00456") |
| **evidence_title** | VARCHAR(255) | NOT NULL | | Short description (e.g., "Register 3 video - 2026-02-17 14:30") |
| **evidence_description** | TEXT | NULL | | Detailed description of evidence |
| **collected_date** | TIMESTAMP | NOT NULL | NOW() | When evidence was collected |
| **collected_by_user_id** | INTEGER | NOT NULL | FK | User who collected the evidence |
| **source_location** | VARCHAR(255) | NULL | | Physical/logical location where evidence was collected |
| **chain_custody_status** | VARCHAR(50) | NOT NULL | 'secured' | Status: 'secured', 'in_transit', 'released', 'compromised', 'destroyed' |
| **current_custodian_user_id** | INTEGER | NULL | FK | User currently responsible for evidence |
| **storage_location** | VARCHAR(255) | NULL | | Where evidence is physically stored |
| **retention_date** | TIMESTAMP | NULL | | Date when evidence can be purged (compliance) |
| **file_hash_sha256** | VARCHAR(64) | NULL | | SHA-256 hash of digital evidence file (for integrity verification) |
| **blockchain_timestamp** | VARCHAR(255) | NULL | | Bitcoin blockchain timestamp (if timestamped) |
| **is_critical** | BOOLEAN | NOT NULL | FALSE | Critical evidence flag (affects retention) |
| **is_admissible** | BOOLEAN | NULL | | Legal admissibility assessment |
| **version_number** | INTEGER | NOT NULL | 1 | Version number (for evidence updates) |
| **previous_version_id** | INTEGER | NULL | FK | Previous version of this evidence (if modified) |
| **created_at** | TIMESTAMP | NOT NULL | NOW() | Record creation timestamp |
| **updated_at** | TIMESTAMP | NOT NULL | NOW() | Last update timestamp |
| **deleted_at** | TIMESTAMP | NULL | | Soft delete timestamp |

**Indexes:**
- PRIMARY KEY (`evidence_id`)
- UNIQUE INDEX (`evidence_number`)
- INDEX (`merchant_id`, `evidence_type_code`)
- INDEX (`collected_date` DESC)
- INDEX (`chain_custody_status`)
- INDEX (`file_hash_sha256`)

**Constraints:**
- FOREIGN KEY (`merchant_id`) REFERENCES `merchants(id)`
- FOREIGN KEY (`collected_by_user_id`) REFERENCES `users(id)`
- FOREIGN KEY (`current_custodian_user_id`) REFERENCES `users(id)`
- FOREIGN KEY (`previous_version_id`) REFERENCES `fox_evidence(evidence_id)`
- CHECK (`evidence_type_code` IN ('receipt', 'video', 'photo', 'document', 'transaction', 'witness_statement', 'physical_item', 'other'))
- CHECK (`chain_custody_status` IN ('secured', 'in_transit', 'released', 'compromised', 'destroyed'))

---

## 4. fox_timeline_events

**Description:** Chronological log of all case activity. Every action (case created, evidence added, note added, status changed, subject added) creates a timeline event. Timeline is the source of truth for "what happened when" and provides immutable audit trail.

**GSLM Pattern:** Combines audit trail concepts from Finance domain with temporal validity tracking.

| Attribute | Type | Nullable | Default | Description |
|-----------|------|----------|---------|-------------|
| **event_id** | SERIAL | NOT NULL | PK | Unique event identifier |
| **case_id** | INTEGER | NOT NULL | FK | Foreign key to `fox_cases` |
| **event_type_code** | VARCHAR(50) | NOT NULL | | Type: 'case_created', 'case_updated', 'evidence_added', 'note_added', 'subject_added', 'status_changed', 'assignment_changed', 'custody_transfer', 'bolo_broadcast', 'external_report_filed', 'other' |
| **event_timestamp** | TIMESTAMP | NOT NULL | NOW() | When event occurred |
| **actor_user_id** | INTEGER | NULL | FK | User who triggered the event |
| **actor_type** | VARCHAR(50) | NOT NULL | 'user' | Actor type: 'user', 'system', 'api', 'webhook', 'external' |
| **event_title** | VARCHAR(255) | NOT NULL | | Short event description |
| **event_description** | TEXT | NULL | | Detailed event description |
| **related_entity_type** | VARCHAR(50) | NULL | | Related entity: 'evidence', 'subject', 'note', 'attachment', 'bolo', 'report' |
| **related_entity_id** | INTEGER | NULL | | Foreign key to related entity |
| **metadata_json** | JSONB | NULL | | Additional structured data (before/after values, etc.) |
| **previous_event_id** | INTEGER | NULL | FK | Previous event in timeline (for hash chaining) |
| **event_hash** | VARCHAR(64) | NULL | | SHA-256 hash of (event + previous_hash) for integrity |
| **created_at** | TIMESTAMP | NOT NULL | NOW() | Record creation timestamp |

**Indexes:**
- PRIMARY KEY (`event_id`)
- INDEX (`case_id`, `event_timestamp` DESC)
- INDEX (`event_type_code`)
- INDEX (`actor_user_id`)
- INDEX (`related_entity_type`, `related_entity_id`)
- INDEX (`event_hash`)

**Constraints:**
- FOREIGN KEY (`case_id`) REFERENCES `fox_cases(case_id)`
- FOREIGN KEY (`actor_user_id`) REFERENCES `users(id)`
- FOREIGN KEY (`previous_event_id`) REFERENCES `fox_timeline_events(event_id)`

---

## 5. fox_case_notes

**Description:** Narrative investigation notes added by case investigators. Notes support markdown formatting and can be edited for a grace period (5 minutes) after creation. After grace period, notes are immutable; edits create new timeline events.

**GSLM Pattern:** Mirrors `MerchandiseAttributeInCountry` pattern — separates narrative content from base case record.

| Attribute | Type | Nullable | Default | Description |
|-----------|------|----------|---------|-------------|
| **note_id** | SERIAL | NOT NULL | PK | Unique note identifier |
| **case_id** | INTEGER | NOT NULL | FK | Foreign key to `fox_cases` |
| **author_user_id** | INTEGER | NOT NULL | FK | User who wrote the note |
| **note_text** | TEXT | NOT NULL | | Note content (markdown supported) |
| **note_type_code** | VARCHAR(50) | NOT NULL | 'general' | Type: 'general', 'interview', 'observation', 'conclusion', 'followup', 'resolution' |
| **is_private** | BOOLEAN | NOT NULL | FALSE | Private note (visible only to author) |
| **is_internal** | BOOLEAN | NOT NULL | TRUE | Internal note (not shared with external parties) |
| **edited_at** | TIMESTAMP | NULL | | Last edit timestamp |
| **edit_count** | INTEGER | NOT NULL | 0 | Number of edits (for audit) |
| **created_at** | TIMESTAMP | NOT NULL | NOW() | Record creation timestamp |
| **updated_at** | TIMESTAMP | NOT NULL | NOW() | Last update timestamp |
| **deleted_at** | TIMESTAMP | NULL | | Soft delete timestamp |

**Indexes:**
- PRIMARY KEY (`note_id`)
- INDEX (`case_id`, `created_at` DESC)
- INDEX (`author_user_id`)
- FULLTEXT INDEX (`note_text`)

**Constraints:**
- FOREIGN KEY (`case_id`) REFERENCES `fox_cases(case_id)`
- FOREIGN KEY (`author_user_id`) REFERENCES `users(id)`
- CHECK (`note_type_code` IN ('general', 'interview', 'observation', 'conclusion', 'followup', 'resolution'))

---

## 6. fox_attachments

**Description:** File storage metadata for evidence attachments (photos, videos, PDFs). Files stored in object storage (S3); this table tracks metadata, access URLs, and file integrity hashes.

| Attribute | Type | Nullable | Default | Description |
|-----------|------|----------|---------|-------------|
| **attachment_id** | SERIAL | NOT NULL | PK | Unique attachment identifier |
| **evidence_id** | INTEGER | NOT NULL | FK | Foreign key to `fox_evidence` |
| **file_name** | VARCHAR(255) | NOT NULL | | Original filename |
| **file_type** | VARCHAR(100) | NOT NULL | | MIME type (e.g., "image/jpeg", "video/mp4", "application/pdf") |
| **file_size_bytes** | BIGINT | NOT NULL | | File size in bytes |
| **file_extension** | VARCHAR(20) | NOT NULL | | File extension (e.g., ".jpg", ".mp4", ".pdf") |
| **storage_key** | VARCHAR(500) | NOT NULL | UNIQUE | Object storage key (S3 path) |
| **storage_bucket** | VARCHAR(255) | NOT NULL | | Object storage bucket name |
| **file_hash_sha256** | VARCHAR(64) | NOT NULL | | SHA-256 hash of file content |
| **thumbnail_url** | VARCHAR(500) | NULL | | Thumbnail image URL (for photos/videos) |
| **download_url** | VARCHAR(500) | NULL | | Presigned download URL (expires) |
| **uploaded_by_user_id** | INTEGER | NOT NULL | FK | User who uploaded the file |
| **virus_scan_status** | VARCHAR(50) | NOT NULL | 'pending' | Virus scan: 'pending', 'clean', 'infected', 'failed' |
| **virus_scan_date** | TIMESTAMP | NULL | | When virus scan completed |
| **is_encrypted** | BOOLEAN | NOT NULL | TRUE | File encryption status |
| **encryption_key_id** | VARCHAR(255) | NULL | | KMS key ID (for encrypted files) |
| **created_at** | TIMESTAMP | NOT NULL | NOW() | Record creation timestamp |
| **deleted_at** | TIMESTAMP | NULL | | Soft delete timestamp |

**Indexes:**
- PRIMARY KEY (`attachment_id`)
- UNIQUE INDEX (`storage_key`)
- INDEX (`evidence_id`)
- INDEX (`file_hash_sha256`)
- INDEX (`virus_scan_status`)

**Constraints:**
- FOREIGN KEY (`evidence_id`) REFERENCES `fox_evidence(evidence_id)`
- FOREIGN KEY (`uploaded_by_user_id`) REFERENCES `users(id)`
- CHECK (`virus_scan_status` IN ('pending', 'clean', 'infected', 'failed'))

---

## 7. fox_case_status_history

**Description:** Audit trail of all case status transitions. Every time a case status changes, a record is written to this table with before/after values, timestamp, and actor. Immutable log for compliance and forensic analysis.

**GSLM Pattern:** Explicit status history tracking with actor attribution.

| Attribute | Type | Nullable | Default | Description |
|-----------|------|----------|---------|-------------|
| **history_id** | SERIAL | NOT NULL | PK | Unique history record identifier |
| **case_id** | INTEGER | NOT NULL | FK | Foreign key to `fox_cases` |
| **from_status_code** | VARCHAR(20) | NULL | | Previous status (NULL if initial status) |
| **to_status_code** | VARCHAR(20) | NOT NULL | | New status |
| **changed_by_user_id** | INTEGER | NOT NULL | FK | User who made the change |
| **change_reason** | TEXT | NULL | | Reason for status change |
| **transition_timestamp** | TIMESTAMP | NOT NULL | NOW() | When status changed |
| **created_at** | TIMESTAMP | NOT NULL | NOW() | Record creation timestamp |

**Indexes:**
- PRIMARY KEY (`history_id`)
- INDEX (`case_id`, `transition_timestamp` DESC)
- INDEX (`to_status_code`)

**Constraints:**
- FOREIGN KEY (`case_id`) REFERENCES `fox_cases(case_id)`
- FOREIGN KEY (`changed_by_user_id`) REFERENCES `users(id)`
- CHECK (`from_status_code` IN ('open', 'investigating', 'resolved', 'closed', 'archived'))
- CHECK (`to_status_code` IN ('open', 'investigating', 'resolved', 'closed', 'archived'))

---

## 8. fox_case_subjects (Junction Table)

**Description:** Many-to-many relationship between cases and subjects. A case can have multiple subjects; a subject can appear in multiple cases. This junction table tracks the relationship with role and involvement metadata.

**GSLM Pattern:** Mirrors `PackItemBreakout` many-to-many pattern.

| Attribute | Type | Nullable | Default | Description |
|-----------|------|----------|---------|-------------|
| **case_subject_id** | SERIAL | NOT NULL | PK | Unique relationship identifier |
| **case_id** | INTEGER | NOT NULL | FK | Foreign key to `fox_cases` |
| **subject_id** | INTEGER | NOT NULL | FK | Foreign key to `fox_subjects` |
| **subject_role_code** | VARCHAR(50) | NOT NULL | | Role in case: 'suspect', 'accomplice', 'witness', 'victim', 'informant', 'other' |
| **involvement_level** | VARCHAR(50) | NULL | | Involvement: 'primary', 'secondary', 'peripheral', 'unknown' |
| **added_by_user_id** | INTEGER | NOT NULL | FK | User who added subject to case |
| **notes** | TEXT | NULL | | Notes about subject's role in this case |
| **created_at** | TIMESTAMP | NOT NULL | NOW() | Record creation timestamp |
| **deleted_at** | TIMESTAMP | NULL | | Soft delete timestamp |

**Indexes:**
- PRIMARY KEY (`case_subject_id`)
- UNIQUE INDEX (`case_id`, `subject_id`)
- INDEX (`subject_id`)
- INDEX (`subject_role_code`)

**Constraints:**
- FOREIGN KEY (`case_id`) REFERENCES `fox_cases(case_id)`
- FOREIGN KEY (`subject_id`) REFERENCES `fox_subjects(subject_id)`
- FOREIGN KEY (`added_by_user_id`) REFERENCES `users(id)`
- CHECK (`subject_role_code` IN ('suspect', 'accomplice', 'witness', 'victim', 'informant', 'other'))
- CHECK (`involvement_level` IN ('primary', 'secondary', 'peripheral', 'unknown'))

---

## 9. fox_evidence_cases (Junction Table)

**Description:** Many-to-many relationship between evidence and cases. A single piece of evidence (e.g., surveillance video) can be used in multiple cases. A case aggregates evidence from multiple sources.

**GSLM Pattern:** Many-to-many junction table with metadata.

| Attribute | Type | Nullable | Default | Description |
|-----------|------|----------|---------|-------------|
| **evidence_case_id** | SERIAL | NOT NULL | PK | Unique relationship identifier |
| **evidence_id** | INTEGER | NOT NULL | FK | Foreign key to `fox_evidence` |
| **case_id** | INTEGER | NOT NULL | FK | Foreign key to `fox_cases` |
| **relevance_score** | INTEGER | NULL | | Relevance to case (0-10) |
| **is_key_evidence** | BOOLEAN | NOT NULL | FALSE | Key evidence flag |
| **added_by_user_id** | INTEGER | NOT NULL | FK | User who linked evidence to case |
| **notes** | TEXT | NULL | | Notes about evidence relevance to this case |
| **created_at** | TIMESTAMP | NOT NULL | NOW() | Record creation timestamp |
| **deleted_at** | TIMESTAMP | NULL | | Soft delete timestamp |

**Indexes:**
- PRIMARY KEY (`evidence_case_id`)
- UNIQUE INDEX (`evidence_id`, `case_id`)
- INDEX (`case_id`)
- INDEX (`relevance_score` DESC)

**Constraints:**
- FOREIGN KEY (`evidence_id`) REFERENCES `fox_evidence(evidence_id)`
- FOREIGN KEY (`case_id`) REFERENCES `fox_cases(case_id)`
- FOREIGN KEY (`added_by_user_id`) REFERENCES `users(id)`
- CHECK (`relevance_score` BETWEEN 0 AND 10)

---

## Database Diagram (ASCII ERD)

```
┌─────────────────┐         ┌──────────────────┐         ┌──────────────────┐
│   fox_cases     │◄───────┤fox_case_subjects │────────►│  fox_subjects    │
│                 │         │                  │         │                  │
│ • case_id (PK)  │         │ • case_id (FK)   │         │ • subject_id (PK)│
│ • case_number   │         │ • subject_id (FK)│         │ • employee_id    │
│ • merchant_id   │         │ • subject_role   │         │ • risk_score     │
│ • case_status   │         └──────────────────┘         │ • total_cases    │
│ • priority      │                                       └──────────────────┘
│ • severity      │         ┌──────────────────┐
└────────┬────────┘         │fox_evidence_cases│
         │                  │                  │         ┌──────────────────┐
         │                  │ • evidence_id(FK)│────────►│  fox_evidence    │
         └─────────────────►│ • case_id (FK)   │         │                  │
                            │ • relevance      │         │ • evidence_id(PK)│
                            └──────────────────┘         │ • evidence_type  │
                                                         │ • file_hash      │
         ┌──────────────────┐                           │ • custody_status │
         │fox_timeline_     │                           └────────┬─────────┘
         │     events       │                                    │
         │                  │                                    │
         │ • event_id (PK)  │                           ┌────────▼─────────┐
         │ • case_id (FK)   │                           │ fox_attachments  │
         │ • event_type     │                           │                  │
         │ • event_hash     │                           │ • attachment_id  │
         │ • actor_user_id  │                           │ • evidence_id(FK)│
         └──────────────────┘                           │ • storage_key    │
                                                        │ • file_hash      │
         ┌──────────────────┐                           └──────────────────┘
         │ fox_case_notes   │
         │                  │         ┌──────────────────┐
         │ • note_id (PK)   │         │fox_case_status_  │
         │ • case_id (FK)   │         │    history       │
         │ • note_text      │         │                  │
         │ • note_type      │         │ • history_id (PK)│
         └──────────────────┘         │ • case_id (FK)   │
                                      │ • from_status    │
                                      │ • to_status      │
                                      └──────────────────┘
```

---

## Sprint 1 Implementation Order

Jeremy's build sequence for Alembic migration:

### Phase 1: Core Tables (Day 1-2)
1. `fox_cases` (master table first)
2. `fox_subjects` (independent entity)
3. `fox_evidence` (independent entity)

### Phase 2: Activity Tracking (Day 2-3)
4. `fox_timeline_events` (depends on fox_cases)
5. `fox_case_notes` (depends on fox_cases)
6. `fox_case_status_history` (depends on fox_cases)

### Phase 3: Relationships (Day 3-4)
7. `fox_case_subjects` (junction: cases ↔ subjects)
8. `fox_evidence_cases` (junction: evidence ↔ cases)
9. `fox_attachments` (depends on fox_evidence)

---

## Data Integrity Rules

### Immutability Constraints
- `fox_timeline_events` — NEVER update or delete (append-only)
- `fox_case_status_history` — NEVER update or delete (append-only)
- `fox_evidence` — Updates create new version, link via `previous_version_id`
- `fox_case_notes` — 5-minute edit grace period, then immutable

### Soft Delete Pattern
All tables use `deleted_at` timestamp for soft deletes:
- NULL = active record
- NOT NULL = deleted record (hidden from queries)
- Physical deletion only for compliance (GDPR/CCPA right to erasure)

### Cascade Rules
- `DELETE fox_cases` → soft delete all child records (notes, timeline, status history)
- `DELETE fox_subjects` → blocked if active case associations exist
- `DELETE fox_evidence` → blocked if attached to active cases
- `DELETE merchants` → blocked if active cases exist

### Hash Chain Integrity
`fox_timeline_events` uses blockchain-style hash chaining:
```sql
event_hash = SHA256(
  event_id ||
  case_id ||
  event_timestamp ||
  event_type_code ||
  previous_event_id ||
  previous_event_hash
)
```

If any past event is modified, hash chain breaks → tamper detection.

---

## Performance Considerations

### Expected Scale (Year 1)
- 1,000 merchants
- 50 cases/merchant/year = 50,000 cases
- 10 subjects/case = 500,000 subjects (with duplicates)
- 5 evidence items/case = 250,000 evidence records
- 20 timeline events/case = 1,000,000 timeline records

### Query Optimization
- All foreign keys indexed
- Composite indexes on high-traffic queries (merchant_id + status)
- FULLTEXT indexes for search (subjects, notes)
- Partitioning strategy (TBD): partition `fox_timeline_events` by year if >10M rows

### Caching Strategy
- Cache frequently accessed case metadata (Redis)
- Cache subject risk scores (updated nightly)
- Invalidate cache on status change, evidence add, note add

---

## Security & Compliance

### Encryption
- All PII fields encrypted at rest (AES-256)
- `fox_attachments` files encrypted in S3 (KMS)
- `ssn_last4` stored hashed + salted

### Access Control
- Row-level security: users see only their merchant's cases
- Role-based: 'owner' sees all, 'manager' sees assigned, 'employee' sees created
- Audit log: all queries logged to `access_log` table

### Retention Policy
- Active cases: retain indefinitely
- Closed cases: retain 7 years (default)
- Evidence: retain per `retention_date` field
- Timeline/notes: never purge (audit trail)

### Compliance Flags
- GDPR right to erasure: supported via soft delete + physical purge
- Data subject access requests: query all tables for subject_id/email
- Legal holds: `is_on_legal_hold` flag prevents deletion

---

## API Design Implications

### REST Endpoints (Implied by Schema)

**Cases:**
- `GET /api/cases` — List cases (filter by status, priority, date)
- `POST /api/cases` — Create case
- `GET /api/cases/:id` — Get case detail
- `PATCH /api/cases/:id` — Update case (triggers timeline event)
- `DELETE /api/cases/:id` — Soft delete case

**Subjects:**
- `GET /api/subjects` — List subjects (filter by type, risk score)
- `POST /api/subjects` — Create subject
- `GET /api/subjects/:id` — Get subject detail
- `PATCH /api/subjects/:id` — Update subject

**Evidence:**
- `GET /api/evidence` — List evidence (filter by type, case)
- `POST /api/evidence` — Upload evidence (multipart/form-data)
- `GET /api/evidence/:id` — Get evidence metadata
- `GET /api/evidence/:id/download` — Download evidence file

**Timeline:**
- `GET /api/cases/:id/timeline` — Get case timeline (paginated)

**Notes:**
- `POST /api/cases/:id/notes` — Add note to case
- `PATCH /api/notes/:id` — Edit note (within 5-minute window)

---

## Next Steps

1. **Jeremy:** Create Alembic migration following Phase 1-2-3 sequence
2. **Jeremy:** Add indexes after table creation (separate migration)
3. **Jeremy:** Write unit tests for cascade rules, soft delete, hash chain
4. **Tom:** Review migration SQL before commit
5. **Eva:** Test migration on staging environment
6. **Jess:** Update API documentation with endpoint definitions

---

**Document Status:** ✅ APPROVED FOR SPRINT 1 IMPLEMENTATION

**Sign-off:**
- Tom (Systems Architect): ✅ Schema reviewed, GSLM patterns applied
- Eva (Program Manager): ✅ Sprint 1 scope confirmed
- Jeremy (Developer Quant): Ready to build migration

---

*Fox Data Model v2.0 | GSLM-Enhanced Edition | Canary LP | Confidential*
