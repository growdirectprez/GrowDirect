# Chunk 8 — Canary Platform Mechanics (Schemas `app`, `q`, `ledger`, `memory`)

**Anchor**: Canary Go platform spec — these are not ARTS entities. They're Canary-specific mechanics that ride above ARTS.
**Modules**: Q (Loss Prevention) + cross-cutting (identity, audit, ledger, agent memory).
**Entities**: 15 (across 4 schemas).

## Domain narrative

ARTS covers retail business entities. Canary's value-add is the **agentic platform layer above retail**: detection rules that emit signals, cases that investigate them, evidence chains that prove integrity, ledger positions that track per-tenant cost-to-serve, and the agent memory + audit infrastructure that ties it together.

This chunk follows a different rule than chunks 2-7: instead of folding sources, we **preserve existing Canary patterns** where they work and only redesign where SMB-2030 + ARTS-anchoring rules apply. Most identity/audit entities already exist in current `app` schema and are well-formed (UUID PKs, schema-per-tenant, Postgres-native). We name them in canonical, preserve as-is, and add the missing q-schema, ledger-schema, and memory-schema entities.

The Q schema is the **operational canary** (the warning-bird metaphor): detection rules emit signals → signals open cases → cases collect evidence → evidence anchors to L2 blockchain → cases drive actions. The ledger schema is the **financial canary** (the accountability rails): every operation costs satoshis, tracked per-tenant, payable via L402, anchored to chain.

---

## Q schema — Loss Prevention (6 entities)

### q.detection_rules

**Module**: Q.

```sql
CREATE TABLE q.detection_rules (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       uuid NOT NULL REFERENCES app.tenants(id),
  rule_code       text NOT NULL,                              -- merchant or system-assigned
  name            text NOT NULL,
  description     text,
  rule_category   text NOT NULL,                              -- shrink | fraud | discount_abuse | tender_pattern | scan_avoidance | refund_pattern | drawer_variance | etc.
  rule_definition jsonb NOT NULL,                             -- the actual rule logic — SQL template + thresholds + filters
  severity        text NOT NULL DEFAULT 'medium',             -- low | medium | high | critical
  status          text NOT NULL DEFAULT 'active',             -- active | paused | retired
  evaluation_frequency text NOT NULL DEFAULT 'on_event',      -- on_event | hourly | daily | weekly
  attributes      jsonb NOT NULL DEFAULT '{}',
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, rule_code)
);

CREATE INDEX idx_qrules_tenant ON q.detection_rules(tenant_id);
CREATE INDEX idx_qrules_category ON q.detection_rules(rule_category);
CREATE INDEX idx_qrules_active ON q.detection_rules(tenant_id, evaluation_frequency) WHERE status = 'active';
```

**Lifecycle**: producers `mcp.q.rule.{create,update,activate,pause}`; consumers `mcp.q.detection.evaluate-on-event`, `mcp.q.detection.scheduled-batch`, `mcp.q.metrics.rule-effectiveness`.

**Provenance**: Canary current `app.detection_rules` (preserved with q-schema move + JSONB rule definition). Folds CRDM `CRDM_OperatorAction` patterns + scorecard signals from recovery DDL.

### q.detections

**Module**: Q. (Append-only event log of detected signals.)

```sql
CREATE TABLE q.detections (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id           uuid NOT NULL REFERENCES app.tenants(id),
  rule_id             uuid NOT NULL REFERENCES q.detection_rules(id),
  detected_at         timestamptz NOT NULL DEFAULT now(),
  source_entity_type  text NOT NULL,                              -- transaction | line_item | tender | drawer_event | shift | cashier_action
  source_entity_id    uuid NOT NULL,
  location_id         uuid REFERENCES l.locations(id),
  cashier_employee_id uuid REFERENCES e.employees(id),
  customer_id         uuid REFERENCES c.customers(id),
  severity            text NOT NULL,
  signal_strength     numeric(5,4),                                -- 0.0-1.0 confidence
  evidence            jsonb NOT NULL DEFAULT '{}',                 -- snapshot of source data
  case_id             uuid REFERENCES q.cases(id),                 -- nullable — case opened only if escalated
  status              text NOT NULL DEFAULT 'new',                 -- new | acknowledged | escalated_to_case | dismissed | duplicate
  acknowledged_at     timestamptz,
  acknowledged_by     uuid REFERENCES app.users(id),
  attributes          jsonb NOT NULL DEFAULT '{}',
  created_at          timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_qdet_tenant ON q.detections(tenant_id);
CREATE INDEX idx_qdet_rule ON q.detections(rule_id, detected_at);
CREATE INDEX idx_qdet_source ON q.detections(source_entity_type, source_entity_id);
CREATE INDEX idx_qdet_location ON q.detections(location_id, detected_at);
CREATE INDEX idx_qdet_cashier ON q.detections(cashier_employee_id, detected_at) WHERE cashier_employee_id IS NOT NULL;
CREATE INDEX idx_qdet_case ON q.detections(case_id) WHERE case_id IS NOT NULL;
CREATE INDEX idx_qdet_unresolved ON q.detections(tenant_id, status) WHERE status NOT IN ('dismissed', 'duplicate');
```

**Lifecycle**: producers `mcp.q.detection.emit-from-rule`; consumers `mcp.q.case.escalate-from-detection`, `mcp.alert.notify-from-detection`, `mcp.metrics.q-detection-volume`.

**Provenance**: Canary current `app.alerts` (split into detections + cases for clarity — current spec conflates them).

### q.cases

**Module**: Q.

```sql
CREATE TABLE q.cases (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id           uuid NOT NULL REFERENCES app.tenants(id),
  case_number         text NOT NULL,
  case_type           text NOT NULL DEFAULT 'investigation',      -- investigation | incident | dispute | compliance_review
  title               text NOT NULL,
  description         text,
  severity            text NOT NULL,
  status              text NOT NULL DEFAULT 'open',                -- open | active | pending_action | resolved | closed | reopened
  primary_subject_id  uuid REFERENCES q.subjects(id),
  primary_location_id uuid REFERENCES l.locations(id),
  assigned_to         uuid REFERENCES app.users(id),
  opened_at           timestamptz NOT NULL DEFAULT now(),
  resolved_at         timestamptz,
  resolution_type     text,                                       -- substantiated | unsubstantiated | recovered | restitution | termination | no_action
  loss_amount_estimated numeric(14,4),
  loss_amount_recovered numeric(14,4),
  attributes          jsonb NOT NULL DEFAULT '{}',
  created_at          timestamptz NOT NULL DEFAULT now(),
  updated_at          timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, case_number)
);

CREATE INDEX idx_qcases_tenant ON q.cases(tenant_id);
CREATE INDEX idx_qcases_subject ON q.cases(primary_subject_id);
CREATE INDEX idx_qcases_location ON q.cases(primary_location_id);
CREATE INDEX idx_qcases_assigned ON q.cases(assigned_to);
CREATE INDEX idx_qcases_active ON q.cases(tenant_id, status) WHERE status NOT IN ('resolved', 'closed');
```

**Lifecycle**: producers `mcp.q.case.{create,assign,update-status,resolve,reopen}`; consumers `mcp.audit.case-history`, `mcp.metrics.case-resolution-cycle-time`.

**Provenance**: Canary current `app.fox_cases` + `app.hawk_cases` (consolidated — current spec has 7 + 8 = 15 cols across 2 case tables; canonical is 1 case table with `case_type` discriminator). Recovery DDL `Case_Custom`, `CaseCentre`, `Video_CaseManagement` were precursors to this design.

### q.case_evidence

**Module**: Q. (Evidence chain — append-only with hash for L2 blockchain anchoring.)

```sql
CREATE TABLE q.case_evidence (
  id                      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id               uuid NOT NULL REFERENCES app.tenants(id),
  case_id                 uuid NOT NULL REFERENCES q.cases(id) ON DELETE RESTRICT,
  evidence_type           text NOT NULL,                              -- transaction_snapshot | video_clip | photo | document | witness_statement | system_log | scan_replay
  source_entity_type      text,                                       -- e.g., transaction
  source_entity_id        uuid,
  payload                 jsonb NOT NULL DEFAULT '{}',                -- the evidence content (or pointer to object storage URL)
  payload_hash            text NOT NULL,                              -- SHA-256 of canonical-JSON payload
  prev_evidence_hash      text,                                       -- chain reference
  blockchain_anchor_id    uuid REFERENCES ledger.blockchain_anchors(id),  -- when batched into L2 anchor
  collected_by            uuid REFERENCES app.users(id),
  collected_at            timestamptz NOT NULL DEFAULT now(),
  attributes              jsonb NOT NULL DEFAULT '{}',
  created_at              timestamptz NOT NULL DEFAULT now()
  -- append-only — never updated, never deleted (audit / chain-of-custody)
);

CREATE INDEX idx_qev_tenant ON q.case_evidence(tenant_id);
CREATE INDEX idx_qev_case ON q.case_evidence(case_id, collected_at);
CREATE INDEX idx_qev_hash ON q.case_evidence(payload_hash);
CREATE INDEX idx_qev_unanchored ON q.case_evidence(tenant_id) WHERE blockchain_anchor_id IS NULL;
```

**Lifecycle**: producers `mcp.q.evidence.collect-from-{transaction,video,document,system}`; consumers `mcp.ledger.blockchain-anchor.batch-evidence`, `mcp.q.evidence.access-log`, `mcp.audit.chain-of-custody.verify`.

**Provenance**: Canary current `app.fox_evidence` + `app.fox_evidence_access_log` (preserved with explicit blockchain anchor FK). Cryptographic accountability rail per platform thesis (memory `project_platform_thesis_locked`).

### q.case_actions

**Module**: Q.

```sql
CREATE TABLE q.case_actions (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       uuid NOT NULL REFERENCES app.tenants(id),
  case_id         uuid NOT NULL REFERENCES q.cases(id) ON DELETE CASCADE,
  action_type     text NOT NULL,                                  -- note | status_change | assignment_change | evidence_collected | external_notification | resolution
  performed_by    uuid REFERENCES app.users(id),
  performed_at    timestamptz NOT NULL DEFAULT now(),
  details         jsonb NOT NULL DEFAULT '{}',
  created_at      timestamptz NOT NULL DEFAULT now()
  -- append-only
);

CREATE INDEX idx_qact_tenant ON q.case_actions(tenant_id);
CREATE INDEX idx_qact_case ON q.case_actions(case_id, performed_at);
CREATE INDEX idx_qact_type ON q.case_actions(action_type);
```

**Lifecycle**: producers `mcp.q.case-action.log` (every state change writes one); consumers `mcp.audit.case-action-history`.

**Provenance**: Canary current `app.fox_case_actions` + `app.fox_case_timeline` (consolidated to single action log per §6 cardinality rule).

### q.subjects

**Module**: Q. (Party-like — people / entities involved in cases. Distinct from c.customers / e.employees because subjects can be unknown / external / suspected without being formal master records.)

```sql
CREATE TABLE q.subjects (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id           uuid NOT NULL REFERENCES app.tenants(id),
  subject_code        text NOT NULL,                              -- merchant or system-assigned
  subject_type        text NOT NULL,                              -- known_employee | known_customer | known_vendor | suspected_individual | unknown_person | external_party
  display_name        text NOT NULL,                              -- may be "Suspect #1" for unknowns
  related_employee_id uuid REFERENCES e.employees(id),            -- if subject is a known employee
  related_customer_id uuid REFERENCES c.customers(id),            -- if subject is a known customer
  related_vendor_id   uuid REFERENCES m.vendors(id),              -- if subject is a vendor (RTV fraud, kickbacks)
  description         text,
  identifiers         jsonb DEFAULT '{}',                          -- {phone, email, license_plate, badge_id, photo_urls — all PII tier 2-3, encrypted}
  attributes          jsonb NOT NULL DEFAULT '{}',
  status              text NOT NULL DEFAULT 'active',             -- active | resolved | dismissed
  created_at          timestamptz NOT NULL DEFAULT now(),
  updated_at          timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, subject_code)
);

CREATE INDEX idx_qsub_tenant ON q.subjects(tenant_id);
CREATE INDEX idx_qsub_employee ON q.subjects(related_employee_id) WHERE related_employee_id IS NOT NULL;
CREATE INDEX idx_qsub_customer ON q.subjects(related_customer_id) WHERE related_customer_id IS NOT NULL;
CREATE INDEX idx_qsub_type ON q.subjects(subject_type);
```

**Lifecycle**: producers `mcp.q.subject.{create,update,resolve,merge}`; consumers `mcp.q.case.assign-primary-subject`, `mcp.audit.subject-investigation-history`.

**Provenance**: Canary current `app.fox_subjects` + `app.hawk_subjects` (consolidated). Critical privacy/PII handling — `identifiers` JSONB encrypted at rest.

---

## ledger schema — Cost-to-Serve + Accountability Rails (5 entities)

### ledger.stock_ledger_entries

**Module**: F + D cross-cut.

```sql
CREATE TABLE ledger.stock_ledger_entries (
  id                      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id               uuid NOT NULL REFERENCES app.tenants(id),
  inventory_movement_id   uuid NOT NULL REFERENCES i.inventory_movements(id),
  posted_at               timestamptz NOT NULL DEFAULT now(),
  item_id                 uuid NOT NULL REFERENCES m.items(id),
  location_id             uuid NOT NULL REFERENCES l.locations(id),
  quantity_delta          numeric(14,4) NOT NULL,
  cost_per_unit           numeric(14,4) NOT NULL,                   -- cost at posting time
  cost_amount             numeric(14,4) GENERATED ALWAYS AS (quantity_delta * cost_per_unit) STORED,
  cost_method             text NOT NULL DEFAULT 'weighted_average', -- weighted_average | fifo | lifo | specific
  gl_account_id           uuid REFERENCES f.gl_accounts(id),
  attributes              jsonb NOT NULL DEFAULT '{}',
  created_at              timestamptz NOT NULL DEFAULT now()
  -- append-only
);

CREATE INDEX idx_sl_tenant ON ledger.stock_ledger_entries(tenant_id);
CREATE INDEX idx_sl_movement ON ledger.stock_ledger_entries(inventory_movement_id);
CREATE INDEX idx_sl_item_location ON ledger.stock_ledger_entries(item_id, location_id, posted_at);
CREATE INDEX idx_sl_gl ON ledger.stock_ledger_entries(gl_account_id);
```

**Lifecycle**: producer `mcp.ledger.stock-ledger.post-from-movement` (atomic with inventory movement); consumer `mcp.financial.cogs.aggregate`, `mcp.metrics.margin.compute`.

**Provenance**: Canary current `ledger.stock_ledger_entries` — preserved with explicit FK to `i.inventory_movements`. Provides financial-valuation counterpart to physical movement log.

### ledger.ildwac_positions

**Module**: F. (ILDWAC = the satoshi cost-to-serve rollup per memory `project_satoshi_cost_model`.)

```sql
CREATE TABLE ledger.ildwac_positions (
  id                      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id               uuid NOT NULL REFERENCES app.tenants(id),
  position_period         tstzrange NOT NULL,                       -- the window this position covers
  cadence_step            text NOT NULL,                            -- minute | hour | day | week | month (the cadence-ladder tier per memory)
  l_storage_satoshis      bigint NOT NULL DEFAULT 0,                -- L = storage cost in satoshis
  w_workload_satoshis     bigint NOT NULL DEFAULT 0,                -- W = workload cost
  c_capture_satoshis      bigint NOT NULL DEFAULT 0,                -- C = capture-fidelity cost
  total_satoshis          bigint GENERATED ALWAYS AS (l_storage_satoshis + w_workload_satoshis + c_capture_satoshis) STORED,
  bytes_under_management  bigint,                                   -- the bytes input from CRDM-sizing-template-derived calc (GRO-732)
  workload_units          bigint,                                   -- queries / writes / events processed
  capture_tier            text,                                     -- low | medium | high | full (per CRDM TLOG detail level)
  invoiced_at             timestamptz,                               -- when L402-OTB charged this position
  payment_proof           text,                                     -- L402 receipt / on-chain reference
  attributes              jsonb NOT NULL DEFAULT '{}',
  created_at              timestamptz NOT NULL DEFAULT now()
  -- append-only after invoiced
);

CREATE INDEX idx_ildwac_tenant ON ledger.ildwac_positions(tenant_id);
CREATE INDEX idx_ildwac_period ON ledger.ildwac_positions USING gist(position_period);
CREATE INDEX idx_ildwac_cadence ON ledger.ildwac_positions(cadence_step);
CREATE INDEX idx_ildwac_unbilled ON ledger.ildwac_positions(tenant_id) WHERE invoiced_at IS NULL;
```

**Lifecycle**: producers `mcp.ledger.ildwac.compute-position` (per cadence step), `mcp.ledger.ildwac.invoice-position` (when ready to bill); consumers `mcp.l402.charge-tenant-position`, `mcp.metrics.cost-to-serve-by-tenant`.

**Provenance**: Per memory `project_satoshi_cost_model` and GRO-732 (sizing template input layer). Net-new — no source modeled this. ARTS doesn't cover platform cost-to-serve.

### ledger.rib_batches

**Module**: F. (RIB = Receipt-In-Batch — accumulates receipts for cost averaging.)

```sql
CREATE TABLE ledger.rib_batches (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id           uuid NOT NULL REFERENCES app.tenants(id),
  item_id             uuid NOT NULL REFERENCES m.items(id),
  location_id         uuid REFERENCES l.locations(id),
  batch_period        tstzrange NOT NULL,
  total_quantity      numeric(14,4) NOT NULL DEFAULT 0,
  total_cost          numeric(14,4) NOT NULL DEFAULT 0,
  weighted_avg_cost   numeric(14,4) GENERATED ALWAYS AS (CASE WHEN total_quantity > 0 THEN total_cost / total_quantity ELSE 0 END) STORED,
  receipt_count       int NOT NULL DEFAULT 0,
  closed_at           timestamptz,                                 -- when batch closed and posted to position
  attributes          jsonb NOT NULL DEFAULT '{}',
  created_at          timestamptz NOT NULL DEFAULT now(),
  updated_at          timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_rib_tenant ON ledger.rib_batches(tenant_id);
CREATE INDEX idx_rib_item_location ON ledger.rib_batches(item_id, location_id);
CREATE INDEX idx_rib_period ON ledger.rib_batches USING gist(batch_period);
CREATE INDEX idx_rib_open ON ledger.rib_batches(tenant_id) WHERE closed_at IS NULL;
```

**Lifecycle**: producers `mcp.ledger.rib-batch.{create,append-receipt,close}`; consumers `mcp.ledger.stock-ledger.post-from-rib-close`, `mcp.metrics.cost-trend`.

**Provenance**: Canary current `ledger.rib_batches` — preserved. Per memory `project_ilwac_bitcoin_standard`.

### ledger.l402_otb_budgets

**Module**: F. (L402 = Lightning Network 402 protocol; OTB = Open-To-Buy budget gate.)

```sql
CREATE TABLE ledger.l402_otb_budgets (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id           uuid NOT NULL REFERENCES app.tenants(id),
  budget_period       tstzrange NOT NULL,
  scope_type          text NOT NULL,                              -- tenant_total | category | location | service
  scope_id            uuid,                                       -- references the scope entity (NULL for tenant_total)
  budget_satoshis     bigint NOT NULL,
  consumed_satoshis   bigint NOT NULL DEFAULT 0,
  remaining_satoshis  bigint GENERATED ALWAYS AS (budget_satoshis - consumed_satoshis) STORED,
  hard_limit          boolean NOT NULL DEFAULT false,             -- if true, blocks operations when exhausted
  alert_threshold_pct numeric(5,4) DEFAULT 0.80,                  -- alert when consumed >= threshold * budget
  status              text NOT NULL DEFAULT 'active',             -- active | exhausted | paused | closed
  attributes          jsonb NOT NULL DEFAULT '{}',
  created_at          timestamptz NOT NULL DEFAULT now(),
  updated_at          timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_otb_tenant ON ledger.l402_otb_budgets(tenant_id);
CREATE INDEX idx_otb_period ON ledger.l402_otb_budgets USING gist(budget_period);
CREATE INDEX idx_otb_active ON ledger.l402_otb_budgets(tenant_id, scope_type) WHERE status = 'active';
```

**Lifecycle**: producers `mcp.ledger.otb.{set-budget,consume,close-period}`; consumers `mcp.l402.gate.check-before-operation`, `mcp.alert.budget-threshold-breach`.

**Provenance**: Per platform thesis memory `project_platform_thesis_locked` — L402-gated OTB is one of three accountability rails (operational, financial, evidentiary). Net-new.

### ledger.blockchain_anchors

**Module**: F + Q cross-cut. (The L2 blockchain hash anchoring records — third accountability rail.)

```sql
CREATE TABLE ledger.blockchain_anchors (
  id                  uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id           uuid REFERENCES app.tenants(id),            -- nullable for cross-tenant batch anchors
  anchor_type         text NOT NULL,                              -- evidence_batch | ildwac_position | gl_period | merkle_root
  payload_hash        text NOT NULL,                              -- the hash being anchored
  merkle_root         text,                                        -- if Merkle-batched, the root of the tree
  anchored_at         timestamptz NOT NULL DEFAULT now(),
  l2_chain            text NOT NULL DEFAULT 'lightning',          -- lightning | rgb | liquid | rsk
  l2_transaction_id   text,                                        -- the on-chain reference
  l2_block_height     bigint,
  l2_proof            jsonb,                                       -- proof of inclusion
  related_entity_count int,                                        -- how many entities this anchor batched
  status              text NOT NULL DEFAULT 'pending',             -- pending | confirmed | failed
  attributes          jsonb NOT NULL DEFAULT '{}',
  created_at          timestamptz NOT NULL DEFAULT now()
  -- append-only
);

CREATE INDEX idx_anchor_tenant ON ledger.blockchain_anchors(tenant_id);
CREATE INDEX idx_anchor_type ON ledger.blockchain_anchors(anchor_type);
CREATE INDEX idx_anchor_payload_hash ON ledger.blockchain_anchors(payload_hash);
CREATE INDEX idx_anchor_pending ON ledger.blockchain_anchors(tenant_id) WHERE status = 'pending';
```

**Lifecycle**: producers `mcp.ledger.anchor.{batch-evidence,batch-position,submit-to-l2,confirm}`; consumers `mcp.q.evidence.verify-anchor`, `mcp.audit.cryptographic-integrity.verify`.

**Provenance**: Per platform thesis (third rail: evidentiary). Net-new. Enables third-party verification of evidence and cost rollups without trusting Canary as a custodian.

---

## app schema — Cross-Cutting Platform (4 entities)

These are essentials. Most current Canary `app.*` entities (organizations, merchants, users, roles, settings, feature_flags, source_systems, merchant_sources, external_identities, audit_log, etc.) are preserved as-is from the current spec. We name the canonical-essential subset here.

### app.tenants

**Module**: cross-cutting.

```sql
CREATE TABLE app.tenants (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id uuid NOT NULL,                                  -- references app.organizations (current Canary spec)
  tenant_code     text NOT NULL,
  name            text NOT NULL,
  status          text NOT NULL DEFAULT 'active',                 -- active | onboarding | suspended | terminated | archived
  schema_name     text NOT NULL,                                  -- physical schema name (per schema-per-tenant strategy)
  region          text NOT NULL DEFAULT 'us-west',                -- data residency region
  attributes      jsonb NOT NULL DEFAULT '{}',
  created_at      timestamptz NOT NULL DEFAULT now(),
  updated_at      timestamptz NOT NULL DEFAULT now(),
  UNIQUE (organization_id, tenant_code),
  UNIQUE (schema_name)
);
```

**Lifecycle**: producers `mcp.tenant.{onboard,suspend,terminate,archive}`; consumers `every other entity in the canonical references this`.

**Provenance**: Implicit in current Canary spec via `app.merchants` + `app.merchant_settings`. Promoted to first-class `app.tenants` for clarity (every other entity has `tenant_id REFERENCES app.tenants(id)`).

### app.users

**Preserve as-is from current Canary `app.users`.** Auth identity per `Brain/wiki/canary-go-portal.md`.

### app.audit_log

**Module**: cross-cutting.

```sql
CREATE TABLE app.audit_log (
  id              uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       uuid REFERENCES app.tenants(id),
  user_id         uuid REFERENCES app.users(id),
  action_type     text NOT NULL,                                  -- create | update | delete | view | export | login | logout | impersonate
  entity_type     text NOT NULL,                                  -- e.g., 'm.items', 't.transactions'
  entity_id       uuid,
  changes         jsonb,                                          -- before/after diff
  context         jsonb DEFAULT '{}',                             -- {ip_address, user_agent, request_id}
  performed_at    timestamptz NOT NULL DEFAULT now()
  -- append-only
);

CREATE INDEX idx_audit_tenant ON app.audit_log(tenant_id, performed_at);
CREATE INDEX idx_audit_user ON app.audit_log(user_id, performed_at);
CREATE INDEX idx_audit_entity ON app.audit_log(entity_type, entity_id);
CREATE INDEX idx_audit_action ON app.audit_log(action_type, performed_at);
```

**Lifecycle**: producer `mcp.audit.log` (called from every state-mutating MCP service via middleware); consumer `mcp.audit.report.{by-user,by-entity,by-time}`.

**Provenance**: Canary current `app.audit_log` — preserved as core platform mechanic.

### app.external_identities

**Preserve as-is from current Canary `app.external_identities`.** Maps canonical entity IDs to source-system IDs (POS-native cashier IDs, Square Customer IDs, Counterpoint AR_CUST IDs, etc.). Critical for federation — referenced by every entity that has `external_ids jsonb` for individual mappings, plus this table for join queries.

---

## memory schema — Agent Memory (preserved)

`memory.alx_memories` and `memory.alx_sessions` — preserved as-is from current Canary spec. These are the agent persistence layer (semantic search via pgvector) referenced by `mcp.vault.*` and `mcp.memory.*` services.

---

## Domain summary

**15 entities (6 q + 5 ledger + 4 app explicitly designed; ~10 more app/memory entities preserved as-is from current Canary spec)**:

**q schema (LP)**:
- `q.detection_rules` — JSONB rule definitions, multi-frequency
- `q.detections` — append-only signal log
- `q.cases` — unified case_type discriminator (folds Fox + Hawk current 15 cols → 1 table)
- `q.case_evidence` — append-only with hash chain + blockchain anchor FK
- `q.case_actions` — append-only state log
- `q.subjects` — Party-like with cross-FK to employee/customer/vendor

**ledger schema (cost-to-serve + accountability)**:
- `ledger.stock_ledger_entries` — financial valuation per inventory movement
- `ledger.ildwac_positions` — satoshi cost-to-serve per cadence step (GRO-732 input layer)
- `ledger.rib_batches` — receipt-in-batch cost averaging
- `ledger.l402_otb_budgets` — L402-gated open-to-buy
- `ledger.blockchain_anchors` — L2 hash anchoring (third accountability rail)

**app schema (cross-cutting)**:
- `app.tenants` — promoted from implicit
- `app.users` — preserved
- `app.audit_log` — preserved
- `app.external_identities` — preserved

**memory schema** — `memory.alx_memories` + `memory.alx_sessions` preserved

**Folded from sources**:
- Canary current `app.fox_*` (7 tables) + `app.hawk_*` (8 tables) → 6 q-schema entities (50% reduction via unification)
- Canary current `app.detection_rules` + `app.alerts` + `app.alert_history` → `q.detection_rules` + `q.detections` (cleaner separation: rules vs detections vs cases)
- ILDWAC + L402-OTB + blockchain-anchor — net-new per platform thesis

**MCP service junctions defined for this domain (~30)**:
- Q: rule.{create,update,activate,pause}, detection.{evaluate-on-event, scheduled-batch, emit-from-rule}, case.{create,assign,update-status,resolve,reopen,escalate-from-detection}, evidence.{collect-from-*, access-log}, case-action.log, subject.{create,update,resolve,merge}
- Ledger: stock-ledger.post-from-movement, ildwac.{compute-position, invoice-position}, rib-batch.{create, append-receipt, close}, otb.{set-budget, consume, close-period}, anchor.{batch-evidence, batch-position, submit-to-l2, confirm}
- App: tenant.{onboard,suspend,terminate,archive}, audit.log, audit.report.*

## Status

- **Chunk 8 complete.** 15 Canary platform mechanics entities. Q (Loss Prevention) consolidated. Ledger (cost-to-serve + 3 accountability rails) implemented per platform thesis.
- **Resume**: Chunk 9 — Module ownership tagging across the 13-module spine. Cross-table that maps every canonical entity to its primary module + cross-module touches.
