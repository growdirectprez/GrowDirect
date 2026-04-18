---
type: spec
domain: fox
status: active
created: 2026-03-19
updated: 2026-03-19
---
# Fox Sprint 1 Implementation Plan

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]

**Sprint:** Fox Sprint 1 - Core Case Management
**Target:** Q2 2026
**Goal:** A store manager can create a case in 60 seconds after an incident
**Dev Lead:** Jeremy
**Product:** Eva
**Technical Spec:** `Fox_Module_Technical_Specification_v1.0.html`

---

## Sprint Objective

Ship the **minimum viable case management system** that allows merchants to:
1. Create a case from a Canary alert in <60 seconds
2. Auto-capture digital forensic fields (device_id, card_fingerprint, risk_level)
3. Upload evidence with SHA-256 hashing and immutable storage
4. Track case lifecycle (incident → investigating → action_taken → closed)
5. Maintain audit trail for law enforcement chain of custody

---

## Database Schema (7 Tables)

### Core Tables
1. **`cases`** - Case record with incident details, loss amounts, forensic fields
2. **`subjects`** - Person profiles (suspects, witnesses, employees)
3. **`case_subjects`** - Many-to-many linking cases to subjects

### Evidence Layer (IMMUTABLE)
4. **`case_evidence`** - File storage with SHA-256 hash (INSERT-ONLY)
5. **`evidence_access_log`** - Who viewed/downloaded evidence (INSERT-ONLY)

### Timeline & Actions
6. **`case_timeline`** - Append-only chronological log of case events
7. **`case_actions`** - Task tracking (report to police, issue trespass, etc.)

**Location:** All tables in `canary_app` schema
**SQL DDL:** See Fox spec Section 3, lines 788-976
**RLS:** All tables filtered by `merchant_id` (existing pattern)

---

## User Stories

### US-1: Auto-Create Case from Alert
**As a** store manager
**I want** Canary alerts above severity threshold to auto-create Fox cases
**So that** I don't lose evidence when an incident happens

**Acceptance Criteria:**
- [ ] When Canary alert severity ≥ "high", auto-create Fox case
- [ ] Case is pre-populated with:
  - Merchant location (from session)
  - Incident time (alert timestamp)
  - Case number (format: `FOX-{year}-{store_code}-{seq}`)
  - Triggering alert ID
  - Digital forensic fields (device_id, card_fingerprint, risk_level from JSONB)
- [ ] Transaction log is auto-attached as evidence
- [ ] Case timeline logs "Case created from Canary alert #{alert_id}"

**Integration Point:** `alerts.py` → new function `create_fox_case_from_alert(alert_id)`

---

### US-2: Manual Case Creation
**As a** store manager
**I want** to manually create a case for incidents Canary didn't catch
**So that** I can document shoplifting, employee theft, or incidents without transaction data

**Acceptance Criteria:**
- [ ] Incident form with 6 required fields (completable in <60 seconds):
  - What happened? (free text)
  - Incident class (External | Internal | Incident | Critical)
  - Incident type (dropdown, 5-8 options per class)
  - Estimated loss ($)
  - Date/time (default NOW, editable)
  - Store location (auto-populated from session)
- [ ] Case number auto-generated on save
- [ ] Case appears in "My Open Cases" list immediately
- [ ] Case timeline logs "Case created by {user_name}"

**UI Location:** New route `/fox/cases/new`
**Reference:** Fox spec Section 5 (Incident Report Form), lines 1449-1488

---

### US-3: Evidence Upload with Hash Verification
**As a** store manager
**I want** to upload photos, receipts, and videos to a case
**So that** I have evidence for law enforcement or civil recovery

**Acceptance Criteria:**
- [ ] Drag-and-drop file upload zone
- [ ] Accepted file types: JPG, PNG, PDF, MP4, MOV
- [ ] Each file is SHA-256 hashed on upload
- [ ] File hash stored in `case_evidence.file_hash`
- [ ] Evidence table is INSERT-ONLY (no UPDATE or DELETE)
- [ ] Evidence access is logged (view, download, export)
- [ ] Case timeline logs "Evidence added: {filename}"

**Storage:** S3 bucket or local file system
**Path format:** `/evidence/{merchant_id}/{case_id}/{file_hash}.{ext}`

---

### US-4: Case Workbench (Single-Page View)
**As an** investigator
**I want** to see all case data on one screen
**So that** I can quickly review incident details, subjects, evidence, and timeline

**Acceptance Criteria:**
- [ ] Single-page view at `/fox/cases/{case_id}`
- [ ] Sections:
  - Case header (number, class, type, status, loss amount)
  - Incident details (description, date, location)
  - Subjects (with photos if uploaded)
  - Evidence list (with download buttons)
  - Timeline (chronological, newest first)
  - Actions (pending tasks, checkboxes)
- [ ] All data loads in <2 seconds
- [ ] Page is printable (CSS print styles)

**Reference:** F-105 in Fox spec

---

### US-5: Case List & Search
**As a** store manager
**I want** to see my open cases and search by date, type, or case number
**So that** I can find cases quickly

**Acceptance Criteria:**
- [ ] Cases list at `/fox/cases` with columns:
  - Case number
  - Incident type
  - Date
  - Status
  - Loss amount
- [ ] Default sort: newest first
- [ ] Filters: Status (open/closed), Class, Date range
- [ ] Search by case number or description
- [ ] Click row to open case workbench

---

### US-6: Subject Profile
**As an** investigator
**I want** to create a subject profile with photo and identification
**So that** I can track repeat offenders across multiple cases

**Acceptance Criteria:**
- [ ] Subject form with fields:
  - Name (first, last, alias)
  - Date of birth, sex
  - Physical description (height, weight, hair, eyes)
  - Photo upload (camera button for mobile capture)
  - ID type, number, state
  - Contact info (phone, email, address)
- [ ] Subject profiles are merchant-scoped (RLS by merchant_id)
- [ ] Subject can be linked to multiple cases
- [ ] Subject profile shows "Total Cases" and "Total Loss" (auto-calculated)
- [ ] Photo stored same as evidence (S3/filesystem, SHA-256 hash)

**Reference:** F-401, F-403 in Fox spec

---

### US-7: Immutable Audit Trail
**As a** system architect (Tom)
**I want** evidence and timeline tables to be INSERT-ONLY
**So that** we maintain chain of custody for law enforcement

**Acceptance Criteria:**
- [ ] `case_evidence` has no `updated_at` or `deleted_at` columns
- [ ] `evidence_access_log` has no `updated_at` or `deleted_at` columns
- [ ] `case_timeline` has no `updated_at` or `deleted_at` columns
- [ ] Database constraints enforce INSERT-ONLY:
  ```sql
  -- Prevent UPDATE and DELETE on evidence tables
  CREATE RULE no_update_evidence AS ON UPDATE TO case_evidence DO INSTEAD NOTHING;
  CREATE RULE no_delete_evidence AS ON DELETE TO case_evidence DO INSTEAD NOTHING;
  ```
- [ ] Unit tests verify UPDATE and DELETE fail on immutable tables

**Philosophy:** "This is people's lives and jobs. If we accuse someone, we have to be sure and have the facts."

---

## Sprint 1 Feature Checklist

- [ ] **F-101:** Incident creation with Square location auto-lookup
- [ ] **F-102:** Case numbering (auto-generated `FOX-{year}-{store}-{seq}`)
- [ ] **F-103:** Case classification (4 classes, simplified type list)
- [ ] **F-104:** Case lifecycle (incident → investigating → action_taken → closed → referred)
- [ ] **F-105:** Case workbench (single-page view of all case data)
- [ ] **F-401:** Subject profile (basic demographics + photo)
- [ ] **F-403:** Identification capture
- [ ] **F-501:** File attachments with SHA-256 hashing and access logging
- [ ] **F-1101:** RBAC (viewer, analyst, manager, admin)
- [ ] **F-1103:** Audit trail (immutable, hash-chained)
- [ ] **NEW:** Auto-case creation from Canary alerts above severity threshold
- [ ] **NEW:** Digital forensic fields on case record (device_id, card_fingerprint, risk_level from JSONB)

---

## Technical Implementation Notes

### 1. Database Setup
**File:** `canary/migrations/0XX_add_fox_tables.py`

```python
def upgrade():
    # Create 7 Fox Sprint 1 tables
    # See Fox spec Section 3 for full SQL DDL
    pass
```

**Jeremy:** Copy SQL from Fox spec lines 788-976, adapt to Alembic migration format.

### 2. Auto-Case Creation Hook
**File:** `canary/alerts.py`

```python
def create_fox_case_from_alert(alert_id):
    """
    Creates a Fox case when alert severity >= 'high'.
    Pre-populates case with:
    - merchant_id, location_id from alert
    - incident_date = alert.detected_at
    - device_id, card_fingerprint, risk_level from transaction JSONB
    - auto-attach transaction log as evidence
    """
    alert = Alert.query.get(alert_id)
    if alert.severity not in ['high', 'critical']:
        return None

    # Extract forensic fields from transaction JSONB
    txn = alert.transaction
    device_id = txn.raw_data.get('payment', {}).get('device_details', {}).get('device_id')
    card_fingerprint = txn.raw_data.get('payment', {}).get('card_details', {}).get('card', {}).get('fingerprint')
    risk_level = txn.raw_data.get('payment', {}).get('risk_evaluation', {}).get('risk_level')

    # Create case
    case = Case(
        merchant_id=alert.merchant_id,
        location_id=alert.location_id,
        case_number=generate_case_number(alert.merchant_id),
        incident_class='external',  # Default, user can change
        incident_type='fraud',       # Default, user can change
        incident_date=alert.detected_at,
        triggering_alert_id=alert.id,
        device_id=device_id,
        card_fingerprint=card_fingerprint,
        risk_level=risk_level,
        created_by_id=1  # System user
    )
    db.session.add(case)
    db.session.flush()

    # Auto-attach transaction as evidence
    evidence = CaseEvidence(
        case_id=case.id,
        merchant_id=alert.merchant_id,
        file_name=f"transaction_{txn.id}.json",
        file_type='application/json',
        storage_path=f"/evidence/{alert.merchant_id}/{case.id}/txn_{txn.id}.json",
        file_hash=hashlib.sha256(json.dumps(txn.raw_data).encode()).hexdigest(),
        evidence_type='transaction_log',
        uploaded_by_id=1  # System user
    )
    db.session.add(evidence)

    # Log to timeline
    timeline = CaseTimeline(
        case_id=case.id,
        merchant_id=alert.merchant_id,
        entry_type='case_created',
        entry_text=f"Case auto-created from Canary alert #{alert.id}",
        occurred_at=datetime.utcnow()
    )
    db.session.add(timeline)

    db.session.commit()
    return case.id
```

**Integration:** Call this from `alerts.py` after alert is created and severity is determined.

### 3. Case Number Generation
**File:** `canary/models/case.py`

```python
def generate_case_number(merchant_id):
    """
    Format: FOX-{year}-{store_code}-{seq}
    Example: FOX-2026-SOMA-0042
    """
    year = datetime.now().year
    merchant = Merchant.query.get(merchant_id)
    store_code = merchant.store_code or f"M{merchant_id}"  # Fallback if no store_code

    # Get max sequence for this merchant this year
    last_case = Case.query.filter(
        Case.merchant_id == merchant_id,
        Case.case_number.like(f"FOX-{year}-{store_code}-%")
    ).order_by(Case.case_number.desc()).first()

    if last_case:
        seq = int(last_case.case_number.split('-')[-1]) + 1
    else:
        seq = 1

    return f"FOX-{year}-{store_code}-{seq:04d}"
```

### 4. Evidence Upload with SHA-256
**File:** `canary/routes/fox.py`

```python
@fox_bp.route('/cases/<int:case_id>/evidence/upload', methods=['POST'])
def upload_evidence(case_id):
    file = request.files['file']
    if not file:
        return jsonify({'error': 'No file provided'}), 400

    # Read file bytes and compute hash
    file_bytes = file.read()
    file_hash = hashlib.sha256(file_bytes).hexdigest()

    # Save to storage
    storage_path = f"/evidence/{g.merchant_id}/{case_id}/{file_hash}.{file.filename.split('.')[-1]}"
    with open(storage_path, 'wb') as f:
        f.write(file_bytes)

    # Create evidence record
    evidence = CaseEvidence(
        case_id=case_id,
        merchant_id=g.merchant_id,
        file_name=file.filename,
        file_type=file.content_type,
        file_size_bytes=len(file_bytes),
        storage_path=storage_path,
        file_hash=file_hash,
        evidence_type='photo',  # Or detect from content_type
        uploaded_by_id=g.user.id
    )
    db.session.add(evidence)

    # Log access
    log = EvidenceAccessLog(
        evidence_id=evidence.id,
        merchant_id=g.merchant_id,
        user_id=g.user.id,
        action='upload',
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent')
    )
    db.session.add(log)

    # Timeline entry
    timeline = CaseTimeline(
        case_id=case_id,
        merchant_id=g.merchant_id,
        entry_type='evidence_added',
        entry_text=f"Evidence added: {file.filename}",
        actor_id=g.user.id
    )
    db.session.add(timeline)

    db.session.commit()
    return jsonify({'evidence_id': evidence.id}), 201
```

---

## Sprint 1 Acceptance Criteria (Final Gate)

- [ ] A store owner can create a case in under 60 seconds
- [ ] An alert from Canary auto-creates a case with evidence pre-attached
- [ ] Evidence files are SHA-256 hashed at upload
- [ ] Every evidence access is logged (view, download, export)
- [ ] Case timeline is append-only and shows complete chronological record
- [ ] Cases cannot be deleted; only soft-deleted via `deleted_at` timestamp
- [ ] Evidence cannot be modified after upload; INSERT-only constraint enforced at DB level
- [ ] Database migration runs cleanly on dev, staging, production
- [ ] Unit tests cover:
  - Case creation
  - Evidence upload and hashing
  - Auto-case creation from alert
  - INSERT-only enforcement on immutable tables
- [ ] Integration test: Create alert → verify Fox case auto-created
- [ ] Documentation updated:
  - `README.md` (Fox module added)
  - API docs (new endpoints)
  - Database ERD (Fox tables added)

---

## Dependencies

- [ ] Tom: Review unified 21-entity data model against 3-database architecture (**BLOCKER**)
- [ ] Jess: Document Fox module in project README
- [ ] PhD: parse_payment_to_transaction v2 (22+ field extraction) - **OPTIONAL for Sprint 1**, but recommended to ship in parallel

---

## Sprint 1 Timeline

**Week 1 (Feb 17-21):**
- [ ] Database migration (7 tables)
- [ ] Case model, CaseEvidence model, Subject model
- [ ] Basic CRUD routes (`/fox/cases`, `/fox/cases/new`, `/fox/cases/<id>`)

**Week 2 (Feb 24-28):**
- [ ] Auto-case creation from alerts
- [ ] Evidence upload with SHA-256
- [ ] Case workbench UI (single-page view)

**Week 3 (Mar 3-7):**
- [ ] Subject profile form
- [ ] Case list with filters
- [ ] Unit tests + integration tests

**Week 4 (Mar 10-14):**
- [ ] QA, bug fixes
- [ ] Documentation
- [ ] Demo to Jeffe
- [ ] **SHIP SPRINT 1**

---

## Next: Sprint 2 Preview

**Sprint 2 Goal:** Investigators can document interviews, track police involvement, and catalog losses.

**New Tables:**
- `case_journal` (append-only investigator notes)
- `interview_records` (witness/suspect statements)
- `police_information` (case number, officer, department)
- `loss_items` (SKU-level loss tracking with recovery status)
- `video_evidence` (DVR metadata, camera locations)
- `payload_schema_registry` (Square webhook schema drift detection)
- `payload_schema_changes` (log of JSONB field changes over time)

**Sprint 2 ships:** parse_payment_to_transaction v2 (22+ field extraction from JSONB)

---

**Eva's Note to Jeremy:**

This is the cleanest handoff I've ever written. PhD gave us SQL, acceptance criteria, integration points, and even sample code. All you have to do is copy/paste and adapt to our existing patterns.

**Start here:**
1. Read Fox spec Section 3 (SQL DDL)
2. Create Alembic migration
3. Run on dev database
4. Implement `create_fox_case_from_alert()` in `alerts.py`
5. Build incident form UI

Questions? Slack me. Let's ship this in 4 weeks.

—**Eva**
