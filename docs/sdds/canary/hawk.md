# Hawk — Ops-Contract Case Management & Card Factory

**Wiki:** [[Brain/wiki/canary-architecture|Canary Architecture]]
**Architecture:** [[docs/sdds/canary/architecture|Canary Architecture SDD]]
**Method:** [[Brain/projects/Method|Method MOC]]
**Predecessor:** [[docs/sdds/canary/fox|Fox SDD]] — Fox evidence chain is an EBR class inside Hawk
**Migration:** `hawk_a00001` (live on `canary` DB)

## Purpose

Hawk is Canary's ops-contract case management system — the successor to Fox's flat case model. Where Fox treated every investigation as a generic case with a linear state machine, Hawk introduces **incident-typed cases** with structured wizard templates, dual-track action codes (internal DE / external PV), compliance obligation tracking, and a **card factory** that generates embeddable, versionable case summary documents.

Hawk does not replace Fox's evidence chain. Fox's INSERT-only evidence tables (`fox_evidence`, `fox_evidence_access_log`), hash-chain integrity triggers, and access-logging discipline remain the evidentiary backbone. Hawk adds the investigation structure that Fox lacked: what kind of incident, what resolution track applies, what actions are legally permissible, and what compliance obligations attach.

### Key Distinctions from Fox

| Dimension | Fox | Hawk |
|---|---|---|
| Case typing | Generic (`case_type` enum) | 63 incident types across 5 classes with wizard templates |
| Action model | Free-text action types | Coded actions on internal/external tracks derived from incident class |
| Resolution track | Single status machine | Dual-track: internal (DE) and external (PV) with class-specific action codes |
| Compliance | None | `hawk_compliance_obligations` — due dates, filing status, obligation types |
| Card output | None | Structured Markdown cards with JSONB frontmatter, versioning, pgvector embedding |
| Wizard UI | None | Per-incident-type JSONB templates defining form fields and validation |

## Dependencies

| Dependency | Type | Required | Purpose |
|---|---|---|---|
| PostgreSQL 17 (`canary` DB, `app` schema) | Database | Yes | All hawk_ tables, pgvector for card embeddings |
| Fox evidence tables | Internal | Yes | `fox_evidence`, `fox_evidence_access_log` — Hawk cases link to Fox evidence chain via `fox_case_id` |
| Valkey 8 (DB 0) | Cache | Yes | Session backend for JWT auth |
| Canary Flask (port 5001) | Host process | Yes | Hawk blueprints run inside the Canary Flask container |
| `canary.middleware.jwt_auth` | Internal | Yes | JWT authentication and RBAC |
| `canary.db.session_factory` | Internal | Yes | Database session management |
| `canary.mcp` base kit | Internal | Yes | MCP tool registration and blueprint creation |
| Ollama (`qwen3-embedding:8b`) | External | Soft | Card embedding — asynchronous, not blocking |

## Data Model

All tables in the `app` schema of the `canary` database. Eight tables in four logical tiers. Migration: `hawk_a00001`.

### Tier 0 — Reference Data (seed-populated)

**hawk_incident_types:** Defines the 63 incident types that structure every Hawk case. PK: `type_code` (String, e.g., `cash_theft`, `grab_and_run`). Fields: `incident_class` (critical_smart_alert / external / internal_de / internal_pv / incident), `de_pv_flag` (de / pv / null — determines action track), `wizard_template` (JSONB — form field definitions per incident type), `resolution_track` (internal / external / incident). 63 seed rows across 5 classes.

**hawk_sources:** Where the case originated. PK: `id` (UUID). Fields: `source_code` (unique, e.g., `CCTV`, `EBR_TRANSACTION_REVIEW`, `TIP_ANONYMOUS`), `source_class` (surveillance / electronic / human / audit / external), `display_name`. 31 seed rows.

### Tier 1 — Investigation Records

**hawk_cases:** Root investigation record. PK: `id` (UUID). Tenant-scoped by `merchant_id` (FK merchants.id). Fields: `location_id`, `incident_class`, `incident_type` (FK hawk_incident_types.type_code), `case_status` (see Workflows), `opened_at`, `closed_at`, `card_id` (FK hawk_cards.id, nullable — set when first card generated), `fox_case_id` (FK fox_cases.id, nullable — backward link to Fox evidence chain). Indexes: (merchant_id, case_status), (merchant_id, incident_class), (incident_type).

**hawk_subjects:** Persons/entities of interest. PK: `id` (UUID). Fields: `case_id` (FK hawk_cases.id), `subject_type` (employee / vendor / external), `employee_id` (nullable FK), `vendor_entity_id` (nullable), `external_name` (nullable — used only when subject is not in Canary's entity registry), `notes`. Constraint: exactly one of employee_id / vendor_entity_id / external_name must be non-null.

**hawk_actions:** Investigation actions on coded tracks. PK: `id` (UUID). Fields: `case_id` (FK hawk_cases.id), `action_code` (e.g., TERMINATED_WITH_PROSECUTION, CORRECTIVE_ACTION, RELEASED_TO_GUARDIAN), `action_track` (internal / external — derived from incident class at validation), `actioned_by`, `actioned_at`, `notes`.

**hawk_compliance_obligations:** Regulatory/policy obligations attached to cases. PK: `id` (UUID). Fields: `case_id` (FK hawk_cases.id), `obligation_type` (String — e.g., police_report_filing, insurance_claim, hr_documentation), `due_date`, `filed_at` (nullable — set when obligation is satisfied), `notes`.

### Tier 2 — Immutable Audit Trail (APPEND-ONLY)

**hawk_timeline:** Append-only event log. PK: `id` (UUID). Fields: `case_id` (FK hawk_cases.id), `merchant_id` (FK), `event_type` (created / status_change / subject_added / action_taken / card_generated / obligation_created / obligation_filed / note_added), `actor_id`, `description`, `event_data` (JSONB — structured metadata per event type), `occurred_at`. No soft-delete. INSERT-only discipline inherited from Fox pattern.

### Tier 3 — Card Factory

**hawk_cards:** Structured case summary documents. PK: `id` (UUID). Fields: `case_id` (FK hawk_cases.id), `card_body` (Text — Markdown narrative), `frontmatter` (JSONB — structured metadata: card_type, case_id, merchant_id, incident_class, de_pv_flag, subject_types, generated_by), `card_version` (Integer — increments on regeneration), `generated_at`, `invalidated_at` (nullable — set when a newer version supersedes), `vector` (pgvector(1024) — embedding for memory bus recall, populated asynchronously).

Card generation queries the case + subjects + actions + timeline and renders a Markdown narrative with JSONB frontmatter. Previous valid card is invalidated (soft — `invalidated_at` set) when a new version generates. The card corpus is the Owl recall surface for Hawk investigations.

## Workflows

### Case Lifecycle FSM

```
open → investigating
investigating → pending_review | escalated
pending_review → escalated | closed | referred_to_le
escalated → closed | referred_to_le
closed          (terminal)
referred_to_le  (terminal)
```

Enforced by `advance_workflow` MCP tool. Invalid transitions rejected with error. Every transition writes a `hawk_timeline` entry (event_type=status_change, event_data carries old_status/new_status).

### Incident Type → Action Track Resolution

When an action is added to a case, the action_code is validated against the case's incident class:

- **internal_de** cases → internal action track: CLOSED_UNFOUNDED, CORRECTIVE_ACTION, INTERVIEWED_NO_CASE, QUIT_PRIOR_TO_INTERVIEW, QUIT_PRIOR_TO_RESOLUTION, REPORTED_TO_ATF, TERMINATED_NO_PROSECUTION, TERMINATED_WITH_PROSECUTION, UNDER_INVESTIGATION
- **external** cases → external action track: CLOSED_UNFOUNDED, PROSECUTED, RELEASED_TO_ADULT, RELEASED_TO_GUARDIAN, RELEASED_TO_POLICE, UNDER_INVESTIGATION
- **internal_pv** cases → internal action track (same as DE)
- **critical_smart_alert** / **incident** → either track permitted (operator chooses)

### Card Generation Pipeline

1. `generate_card(case_id, actor_id)` MCP tool invoked
2. Query case + all subjects + all actions + timeline summary
3. Render Markdown narrative from template (incident-type-aware)
4. Build JSONB frontmatter with structured metadata
5. If previous valid card exists: set `invalidated_at = now()` on it
6. Insert new `hawk_cards` row with `card_version = previous + 1`
7. Write `hawk_timeline` entry (event_type=card_generated)
8. Return card_id, card_version, card_body preview
9. Asynchronously: memory bus embeds card_body → `vector` column via Ollama

### Wizard Template Resolution

Each incident type carries a `wizard_template` JSONB field that defines the form fields a UI renders when creating a case of that type. The `get_wizard_template(incident_type)` MCP tool returns this template for client-side form generation.

Template fields are incident-type-specific — a `grab_and_run` wizard asks for entry/exit points and merchandise description, while a `register_discrepancies` wizard asks for drawer ID, session ID, and variance amount.

## API Contract

### MCP Tools (`canary-hawk` — `/hawk/*`)

9 tools registered via `MCPRegistry`.

| Tool | Category | Description |
|---|---|---|
| `create_case` | cases | Open a case with merchant_id, location_id, incident_type, narrative, source_code, assigned_to. Validates incident_type against seed data. Returns case object. |
| `get_case` | cases | Get full case details by ID — incident type, status, subjects, actions, card reference. |
| `list_cases` | cases | List cases with merchant_id filter + optional status, incident_class, limit. |
| `advance_workflow` | cases | Transition status through FSM. Validates transition legality. Writes timeline. |
| `add_subject` | cases | Link employee/vendor/external to case. Validates exactly-one-identifier constraint. |
| `add_action` | cases | Add coded action. Validates action_code against case's incident class action track. |
| `generate_card` | cards | Generate or regenerate a case summary card. Versions and invalidates previous. |
| `get_timeline` | cases | Get append-only event log for a case. |
| `get_wizard_template` | reference | Return wizard_template JSONB for an incident type. |

### MCP Blueprint Endpoints

| Endpoint | Purpose |
|---|---|
| `GET /hawk/manifest` | Server manifest (name, version, tool count) |
| `GET /hawk/tools` | List all 9 tools with schemas |
| `POST /hawk/tools/<name>` | Invoke a tool by name |
| `GET /hawk/health` | Health check |

### REST Endpoints

REST surface mirrors MCP tools for UI/BFF consumption. Same JWT auth and RBAC as Fox. Endpoint prefix: `/api/hawk/*`. Contract follows the same pattern as Fox REST (see `fox.md` §API Contract).

## Operations

### Startup Sequence

Hawk loads as Flask blueprints registered in `wsgi.py` during Canary Flask boot. Seed data (63 incident types, 31 sources) is verified at startup — missing seed rows trigger a warning log, not a crash.

### Health Checks

| Endpoint | What it checks | Expected response |
|---|---|---|
| `GET /hawk/health` | MCP server alive, tool count, seed data present | `{"service": "canary-hawk", "healthy": true, "tools": 9}` |

### Failure Modes

| Failure | Impact | Behavior |
|---|---|---|
| PostgreSQL down | All Hawk operations fail | 500 errors on all endpoints |
| Missing seed data | Case creation fails for unknown incident_type | 400 error with "unknown incident type" |
| Card generation with no subjects/actions | Card generated but sparse | Allowed — card body reflects empty investigation state |
| Ollama unavailable | Card embedding deferred | Card persists without vector; embedding retried on next memory bus cycle |
| Fox evidence tables missing | Evidence linking fails | Hawk cases can still be created; evidence chain operations return errors |

### Configuration

No Hawk-specific environment variables. All config inherited from Canary Flask. Seed data loaded from migration `hawk_a00001`.

## Relationship to Fox

Hawk does **not** drop or migrate Fox tables. The relationship is:

1. **`hawk_cases.fox_case_id`** — optional FK to `fox_cases.id`. When a Hawk case needs evidence chain operations, it links to a Fox case. Fox's INSERT-only evidence tables handle all evidentiary storage.
2. **Fox remains operational** for existing Square-era cases. No data migration of historical Fox cases to Hawk.
3. **New cases** created through the Hawk MCP tools or UI get Hawk's incident-typed structure. Evidence attachment still routes through Fox's evidence chain.
4. **CRB/NCR vault references** to "Fox case management" will update to "Hawk ops-contract" on the next vault sync. The Fox evidence discipline (INSERT-only, hash-chained, trigger-enforced) is preserved and referenced by name.

## Seed Data Summary

### Incident Types (63 rows, 5 classes)

| Class | Count | Examples |
|---|---|---|
| critical_smart_alert | 17 | bulk_sweeper, grab_and_run, register_manipulation, organized_retail_crime |
| external | 7 | shoplifting_adult, shoplifting_juvenile, robbery, burglary |
| internal_de | 15 | cash_theft, merchandise_theft, time_theft, vendor_fraud |
| internal_pv | 15 | register_discrepancies, procedural_non_compliance, safety_violation |
| incident | 9 | slip_and_fall, property_damage, medical_emergency |

### Sources (31 rows, 5 classes)

| Class | Count | Examples |
|---|---|---|
| surveillance | 4 | CCTV, LPTV, BODY_CAMERA, COVERT_CAMERA |
| electronic | 7 | EBR_TRANSACTION_REVIEW, EBR_REFUND_ANALYSIS, EAS_ALARM, INVENTORY_AUDIT_SYSTEM |
| human | 8 | TIP_ANONYMOUS, TIP_NAMED, OBSERVATION_EMPLOYEE, OBSERVATION_CUSTOMER |
| audit | 7 | AUDIT_FINDING, CASH_AUDIT, INVENTORY_AUDIT, RECEIVING_AUDIT |
| external | 5 | POLICE_REPORT, VENDOR_REPORT, INSURANCE_CLAIM, CUSTOMER_COMPLAINT |

## Production Readiness

- [x] Schema deployed — `hawk_a00001` migration live
- [x] Seed data loaded — 63 incident types, 31 sources
- [x] FSM validated — status transitions enforced at service layer
- [x] Fox evidence chain preserved — INSERT-only triggers unchanged
- [ ] MCP tools implemented — **pending** (service + blueprint code)
- [ ] REST endpoints implemented — **pending**
- [ ] Card generation pipeline implemented — **pending**
- [ ] Card embedding wired to memory bus — **pending**
- [ ] Wizard template UI consumption — **pending** (frontend)
- [ ] Hawk timeline INSERT-only trigger — **pending** (add to migration)

## Source Files

| File | Purpose | Status |
|---|---|---|
| `alembic/versions/hawk_a00001_*.py` | Schema migration + seed data | **Live** |
| `canary/services/hawk/` | Hawk service layer | **Planned** |
| `canary/blueprints/hawk_wired.py` | REST API blueprint | **Planned** |
| `canary/blueprints/hawk_mcp.py` | MCP blueprint | **Planned** |
| `canary/models/hawk/` | SQLAlchemy models | **Planned** |

---
*Canary LP | GrowDirect LLC | Confidential*
