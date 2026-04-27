---
id: sdd-cp-onboarding
title: NCR Counterpoint — Merchant Onboarding & Activation (Module O)
status: draft-1
version: 0.1.0
date: 2026-04-26
author: GrowDirect Engineering
linear: GRO-TBD
companion-sdds:
  - docs/sdds/canary/pos-adapter-substrate.md
  - docs/sdds/canary/ncr-counterpoint-store-station-adapter.md
  - docs/sdds/canary/ncr-counterpoint-customer-adapter.md
  - docs/sdds/canary/ncr-counterpoint-item-catalog-adapter.md
  - docs/sdds/canary/ncr-counterpoint-paycode-adapter.md
  - docs/sdds/canary/ncr-counterpoint-tsp-adapter.md
---

# NCR Counterpoint — Merchant Onboarding & Activation (Module O)

## 1. Purpose

This SDD specifies the end-to-end lifecycle of connecting a new NCR Counterpoint
merchant to Canary: from credential capture through Phase A reference-data seeding
through Phase C live transaction streaming. It is the activation orchestrator —
the code that calls every other adapter in the correct order and handles failure
at each stage.

Three audiences:
1. **The engineer** — what to build (service, routes, models, tasks).
2. **The installer** (Bart / Rapid POS field rep) — what the UI sequence looks like.
3. **The tenant** — what they see and when they know Canary is live.

## 2. Activation Phases

All Counterpoint tenant activations follow a strict three-phase sequence. Phases
must complete in order; a failure in an earlier phase blocks later phases.

```
Phase A — Reference Data (same-day, serial)
  ├── A1: Store discovery + cp_store_config + cp_station_config
  ├── A2: CustomerControl fetch (WALK_IN_CUST_NO per store)
  ├── A3: ItemCategories sync (cp_item_categories + cp_item_subcategories)
  └── A4: PayCode sync (cp_pay_codes, canonical_type derivation)

Phase B — Entity Seeding (hours 1-24, parallel)
  ├── B1: Customer roster sync (app.external_identities + cp_customer_profiles)
  └── B2: Item catalog sync (cp_item_catalog, full IM_ITEM pull)

Phase C — Transaction Stream (live, after B completes)
  └── C1: TSP poll loop activates (PS_DOC via GET /Documents)
```

Phase A runs serially within itself — stores must be loaded before CustomerControl
(which is per-store), ItemCategories before Items (which reference categories),
PayCodes before Documents (which reference PAY_COD). The dependency is enforced
at the service layer, not assumed.

Phase B steps can run in parallel (customers and items are independent).

Phase C does not start until Phase B is fully complete. Attempting to parse
a Document before the item catalog and customer roster are seeded produces
unresolvable cache-misses.

### Activation state machine

```
PENDING → A_IN_PROGRESS → A_COMPLETE → B_IN_PROGRESS → B_COMPLETE → LIVE
                │                             │
                ▼                             ▼
           A_FAILED                      B_FAILED
```

A `LIVE` tenant has all three phases complete and has the poll loop registered
in `poll_watermarks` for entity_type `document`.

## 3. Data Model Changes

### 3.1 app.cp_merchant_activations (new)

Tracks the activation lifecycle per tenant.

```sql
CREATE TABLE app.cp_merchant_activations (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id         UUID NOT NULL REFERENCES app.merchants(id),
    company_alias       TEXT NOT NULL,              -- Counterpoint company alias

    -- Connection parameters (encrypted creds stored in pos_tenant_credentials)
    server_host         TEXT NOT NULL,              -- e.g. "counterpoint.acme.com"
    server_port         INTEGER NOT NULL DEFAULT 8080,
    api_key             TEXT NOT NULL,              -- non-secret; used in headers
    -- HTTP Basic credentials live in pos_tenant_credentials, not here

    -- Activation state
    activation_state    TEXT NOT NULL DEFAULT 'PENDING',
    phase_a_started_at  TIMESTAMPTZ,
    phase_a_ended_at    TIMESTAMPTZ,
    phase_b_started_at  TIMESTAMPTZ,
    phase_b_ended_at    TIMESTAMPTZ,
    phase_c_started_at  TIMESTAMPTZ,
    last_error          TEXT,
    last_error_at       TIMESTAMPTZ,
    retry_count         INTEGER NOT NULL DEFAULT 0,

    -- Vertical / deployment profile
    vertical            TEXT NOT NULL DEFAULT 'general',    -- garden_center, hardware, etc.
    is_dry_run          BOOLEAN NOT NULL DEFAULT TRUE,      -- Phase C starts dry

    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),

    UNIQUE (merchant_id, company_alias)
);

CREATE INDEX idx_cp_activations_state
    ON app.cp_merchant_activations (activation_state)
    WHERE activation_state NOT IN ('LIVE', 'A_FAILED', 'B_FAILED');
```

### 3.2 Existing table modifications

The `app.merchants` and `app.pos_tenant_credentials` tables require no schema
changes for activation. The `app.cp_known_store_ids` table (specified in the
store/station SDD) is seeded during Phase A1.

## 4. CounterpointMerchantActivationService

```python
class CounterpointMerchantActivationService:
    """
    Orchestrates the full A→B→C activation of a new Counterpoint tenant.

    Designed to be invoked:
      - From the onboarding UI route (initial trigger)
      - From a retry task (async, on failure recovery)
      - From the activation health-check cron (detects stuck tenants)
    """

    def __init__(self, db: Session, merchant_id: UUID, company_alias: str):
        self.db = db
        self.merchant_id = merchant_id
        self.company_alias = company_alias
        self._activation: CpMerchantActivation | None = None

    # ------------------------------------------------------------------ #
    # Public entry points                                                  #
    # ------------------------------------------------------------------ #

    def begin(self) -> CpMerchantActivation:
        """Start activation from PENDING. Idempotent — returns existing if already started."""
        rec = self._load_or_create()
        if rec.activation_state == "PENDING":
            self._run_phase_a()
        elif rec.activation_state == "A_COMPLETE":
            self._run_phase_b()
        elif rec.activation_state == "B_COMPLETE":
            self._run_phase_c()
        elif rec.activation_state == "LIVE":
            return rec
        else:
            raise ActivationOrderError(
                f"Cannot begin: activation is in state {rec.activation_state}"
            )
        return self._activation

    def retry_from_failure(self) -> CpMerchantActivation:
        rec = self._load_or_create()
        if rec.activation_state == "A_FAILED":
            rec.activation_state = "PENDING"
            rec.retry_count += 1
            self.db.flush()
            self._run_phase_a()
        elif rec.activation_state == "B_FAILED":
            rec.activation_state = "A_COMPLETE"
            rec.retry_count += 1
            self.db.flush()
            self._run_phase_b()
        else:
            raise ActivationOrderError(
                f"No failure state to retry from: {rec.activation_state}"
            )
        return self._activation

    # ------------------------------------------------------------------ #
    # Phase implementations                                                #
    # ------------------------------------------------------------------ #

    def _run_phase_a(self):
        rec = self._activation
        rec.activation_state = "A_IN_PROGRESS"
        rec.phase_a_started_at = datetime.utcnow()
        self.db.flush()

        try:
            # A1: stores + stations (also seeds cp_known_store_ids)
            StoreStationAdapter(self.db, self.merchant_id, self.company_alias).seed()

            # A2: CustomerControl (WALK_IN_CUST_NO per store) — embedded in A1
            # CustomerControl is fetched inside StoreStationAdapter.seed()

            # A3: item categories
            ItemCategoriesAdapter(self.db, self.merchant_id, self.company_alias).seed()

            # A4: pay codes
            PayCodeAdapter(self.db, self.merchant_id, self.company_alias).seed()

        except Exception as exc:
            rec.activation_state = "A_FAILED"
            rec.last_error = str(exc)
            rec.last_error_at = datetime.utcnow()
            self.db.flush()
            raise

        rec.activation_state = "A_COMPLETE"
        rec.phase_a_ended_at = datetime.utcnow()
        self.db.flush()

        # Immediately kick off Phase B (async task)
        enqueue_activation_phase_b(self.merchant_id, self.company_alias)

    def _run_phase_b(self):
        rec = self._activation
        rec.activation_state = "B_IN_PROGRESS"
        rec.phase_b_started_at = datetime.utcnow()
        self.db.flush()

        try:
            # B1 and B2 run in parallel via task workers
            results = run_parallel([
                lambda: CustomerRosterAdapter(
                    self.db, self.merchant_id, self.company_alias).full_sync(),
                lambda: ItemCatalogAdapter(
                    self.db, self.merchant_id, self.company_alias).full_sync(),
            ])
            _check_parallel_results(results)

        except Exception as exc:
            rec.activation_state = "B_FAILED"
            rec.last_error = str(exc)
            rec.last_error_at = datetime.utcnow()
            self.db.flush()
            raise

        rec.activation_state = "B_COMPLETE"
        rec.phase_b_ended_at = datetime.utcnow()
        self.db.flush()

        # Phase C starts after B — seeds poll_watermarks and enables the loop
        self._run_phase_c()

    def _run_phase_c(self):
        rec = self._activation
        rec.phase_c_started_at = datetime.utcnow()
        self.db.flush()

        # Register the document poll watermark at epoch 0 — adapter will begin
        # from oldest available Documents on first poll
        _seed_poll_watermark(
            self.db, self.merchant_id, "counterpoint",
            self.company_alias, "document",
        )

        # Enable dry_run mode by default; installer or founder can flip
        # is_dry_run = False after calibration period
        rec.activation_state = "LIVE"
        self.db.flush()

        logger.info(
            "tenant_activated",
            merchant_id=str(self.merchant_id),
            company_alias=self.company_alias,
            dry_run=rec.is_dry_run,
        )
```

### ActivationOrderError

```python
class ActivationOrderError(Exception):
    """Raised when an activation phase is attempted out of order."""
```

## 5. Onboarding UI Flow

The Canary UI surfaces a four-step wizard for the installer. The wizard maps
1-to-1 onto the activation phases.

### Step 1 — Connection

Fields:
- **Server URL** (`server_host`) — e.g. `192.168.1.100` or `counterpoint.acme.com`
- **Port** (`server_port`) — default 8080
- **API Key** (`api_key`) — from Counterpoint NCR Office / Admin
- **Username** (`cp_username`) — HTTP Basic username
- **Password** (`cp_password`) — HTTP Basic password
- **Company Alias** (`company_alias`) — from Counterpoint server settings

On "Test Connection":
- Call `CounterpointAdapter.test_connection(credentials)`
- Test endpoint: `GET /APIVersion` — lightweight, no auth side effects
- Show success (version string) or failure (connection refused / 401 / timeout)
- On failure, surface the raw error — do not summarize it away

### Step 2 — Reference Data (Phase A)

Trigger: "Start Setup" button after successful connection test.

Progress display:
```
[✓] Stores and stations        2 stores, 6 stations
[✓] Customer control           Walk-in sentinel: CASH
[✓] Item categories            18 categories, 42 subcategories
[✓] Pay codes                  8 pay codes configured
```

Each row populates as the step completes. The UI polls `/api/activation/status`
every 5 seconds. On failure, shows the failed step with the error and a
"Retry" button.

### Step 3 — Data Seeding (Phase B)

Progress display (parallel bars):
```
Customers    [████████░░░░░░░░]  1,240 / 2,100 synced
Items        [██████████████░░]  4,820 / 5,500 synced
```

ETA shown once > 10% complete, derived from rows/second pace.

On completion: "Data seeded — Canary is ready to watch your transactions."

### Step 4 — Go Live (Phase C)

Toggle: **Dry Run Mode** (default ON)
- In dry run, Chirp rules fire internally but no alerts are surfaced to the tenant.
- Recommended calibration period: 7 days before flipping live.
- Installer can flip to live immediately if client wants immediate alerts.

"Activate" button:
- Seeds the document poll watermark (Phase C start)
- Shows the confirmation screen with:
  - Number of stores connected
  - Number of pay codes recognized
  - Dry run on/off status
  - Estimated time to first Chirp alert (based on next poll interval)

## 6. Routes

```python
# Onboarding wizard
GET   /settings/pos/connect                 # Step 1 — connection form
POST  /settings/pos/connect                 # Submit credentials; test + persist
GET   /settings/pos/activate                # Steps 2-4 — activation wizard UI
GET   /api/activation/status               # Poll: {state, phase_a_pct, phase_b_pct}
POST  /api/activation/retry                # Retry failed phase
POST  /api/activation/go-live              # Flip is_dry_run = False (Phase C)

# Already live
GET   /settings/pos/status                 # Connection health dashboard
POST  /settings/pos/disconnect             # Graceful tenant disconnect
```

## 7. Credential Storage

Credentials are stored in `app.pos_tenant_credentials` (specified in
`pos-adapter-substrate.md`) — AES-256-GCM encrypted blobs keyed on
`(merchant_id, source_code, company_alias)`.

The onboarding route:
1. Calls `test_connection()` with plaintext credentials
2. On success, calls `CredentialService.store(merchant_id, 'counterpoint', company_alias, creds)`
3. Never logs or persists plaintext credentials outside the encrypted blob

Password fields in the wizard use `<input type="password">`. The POST body
is processed in memory only — never echoed back or written to a log.

## 8. Vertical Profile Application

When `vertical = 'garden_center'` is selected at onboarding:

```python
def apply_vertical_profile(
    db: Session,
    merchant_id: UUID,
    vertical: str,
):
    """Seed vertical-specific rule configurations after Phase C activation."""
    if vertical == "garden_center":
        profiles = GARDEN_CENTER_ALLOW_LISTS     # from module-q-chirp-wiring SDD
    else:
        profiles = {}

    for rule_id, config in profiles.items():
        upsert_merchant_rule_config(db, merchant_id, rule_id, config, source_code="counterpoint")

    # Seed all Counterpoint-specific rules in is_dry_run=True by default
    for rule_id in COUNTERPOINT_RULE_IDS:
        upsert_merchant_rule_config(
            db, merchant_id, rule_id,
            {"is_dry_run": True, "source_code": "counterpoint"},
        )
```

`COUNTERPOINT_RULE_IDS` is the list `["C-1001", "C-1003", ..., "C-2001"]`
maintained in `rule_definitions.py`.

## 9. Activation Health Check (Cron)

A background job runs every 15 minutes to detect and alert on stuck activations:

```python
def activation_health_check():
    """Flag activations stuck in an IN_PROGRESS state for > 2 hours."""
    cutoff = datetime.utcnow() - timedelta(hours=2)
    stuck = db.query(CpMerchantActivation).filter(
        CpMerchantActivation.activation_state.in_(["A_IN_PROGRESS", "B_IN_PROGRESS"]),
        CpMerchantActivation.updated_at < cutoff,
    ).all()

    for rec in stuck:
        logger.error(
            "activation_stuck",
            merchant_id=str(rec.merchant_id),
            state=rec.activation_state,
            hours_stuck=(datetime.utcnow() - rec.updated_at).seconds // 3600,
        )
        # Optionally transition to *_FAILED for retry eligibility
```

## 10. Disconnection

A merchant can disconnect Counterpoint at any time. Graceful disconnect:

1. Remove all `poll_watermarks` for `(merchant_id, 'counterpoint', company_alias)`
2. Set `pos_tenant_credentials.credential_state = 'disconnected'`
3. Set `cp_merchant_activations.activation_state = 'DISCONNECTED'`
4. Do NOT delete `cp_*` attribute tables — historical data preserved for audit
5. Do NOT delete `app.external_identities` rows — they remain as an audit trail
6. Alert rules for the merchant remain but fire against no new events (harmless)

Reconnection resets the activation to `PENDING` and re-runs all phases.
Existing `cp_*` rows are overwritten (UPSERT) not duplicated.

## 11. Activation Ordering Enforcement

`ActivationOrderError` is raised at the service layer. It propagates to the
route handler and returns HTTP 409 with a structured error body:

```json
{
    "error": "activation_order_violation",
    "message": "Phase C cannot start before Phase B is complete.",
    "current_state": "A_COMPLETE",
    "required_state": "B_COMPLETE"
}
```

The wizard UI is driven by activation state — it never renders a "Go Live"
button unless the activation record is in `B_COMPLETE` or `LIVE`. The API
enforces the same constraint independently.

## 12. Phase B Progress Tracking

Phase B seeding of the full customer roster and item catalog is the longest
step — potentially hours for a large Counterpoint deployment. Progress is
tracked via:

```sql
CREATE TABLE app.cp_activation_progress (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    activation_id   UUID NOT NULL REFERENCES app.cp_merchant_activations(id),
    phase           TEXT NOT NULL,                    -- 'B1', 'B2'
    entity_type     TEXT NOT NULL,                    -- 'customer', 'item'
    rows_expected   INTEGER,                          -- NULL until first page
    rows_synced     INTEGER NOT NULL DEFAULT 0,
    pages_fetched   INTEGER NOT NULL DEFAULT 0,
    last_page_at    TIMESTAMPTZ,
    completed_at    TIMESTAMPTZ,

    UNIQUE (activation_id, entity_type)
);
```

Each adapter's `full_sync()` method updates this table after each page fetch.
The `/api/activation/status` route joins this table to compute percentage
complete for the wizard progress bars.

## 13. Acceptance Criteria

**AC-O-01 — Serial Phase A:** Phase A steps run in order A1→A2→A3→A4. If A3
(item categories) fails, A4 (pay codes) does not run. The activation record
shows `A_FAILED` with the failing step's error.

**AC-O-02 — Phase B parallel:** B1 (customers) and B2 (items) run concurrently.
If B1 fails, B2 may still complete; the overall Phase B result is FAILED if
either subtask fails. Progress bars for both steps update independently.

**AC-O-03 — Phase C gate:** A `POST /api/activation/go-live` request with
`activation_state != 'B_COMPLETE'` returns HTTP 409 with `activation_order_violation`.

**AC-O-04 — Connection test:** `GET /APIVersion` success with the provided
credentials is required before credentials are stored. A wrong password
returns the raw 401 error to the installer — not a masked "connection failed".

**AC-O-05 — Dry run default:** Phase C activation always starts with
`is_dry_run = True`. No Chirp alerts surface to the tenant until `is_dry_run`
is flipped to False by an explicit "Go Live" action.

**AC-O-06 — Vertical seeding:** A tenant activated with `vertical = 'garden_center'`
has the garden-center allow-list rules pre-seeded in `merchant_rule_configs`
at Phase C activation time. All seeded rules default to `is_dry_run = True`.

**AC-O-07 — Reconnect idempotency:** Disconnecting and reconnecting a tenant
does not create duplicate `cp_*` rows. Re-sync UPSERTs on `(merchant_id, natural_key)`.

**AC-O-08 — Stuck detection:** An activation stuck in `A_IN_PROGRESS` for > 2
hours appears in the `activation_stuck` structured log event. The health check
runs at most once every 15 minutes.

## 14. Open Questions

| ID | Question | Impact |
|---|---|---|
| O-OQ-01 | Rapid POS installer UX: does the installer use a Canary admin panel or a tenant-facing wizard? If installer-facing, the auth model for the wizard session differs (may require a separate installer role). | Route auth design |
| O-OQ-02 | How large are Phase B entity datasets in a typical garden center Counterpoint deployment? 5K customers / 10K items seems representative; 50K+ items changes the ETA display and may require cursor-pagination chunking. Confirm with Bart. | Phase B task timeout settings |
| O-OQ-03 | Counterpoint server connectivity from Canary cloud: does the REST endpoint require a VPN, tunnel, or local agent? If behind a NAT, the `server_host` field on the wizard may not be reachable from Canary's production instance. This could mean all CP polling runs from a customer-side agent binary. | Deployment topology |
| O-OQ-04 | `GET /APIVersion` as the connection-test endpoint: confirm this endpoint does not require a specific permission level beyond the merchant's existing API credentials. If it's admin-only, use a lower-privilege endpoint. | Connection test reliability |
| O-OQ-05 | Vertical profile list: `garden_center` is the initial vertical. What other verticals should be configurable at launch (hardware, florist, nursery-supply)? Each needs its own allow-list profile seed. | Scope of vertical_profile seeding |

---

## Related

- `docs/sdds/canary/pos-adapter-substrate.md` — POSAdapter ABC; pos_tenant_credentials; ActivationOrderError base
- `docs/sdds/canary/ncr-counterpoint-store-station-adapter.md` — Phase A1: StoreStationAdapter.seed()
- `docs/sdds/canary/ncr-counterpoint-item-catalog-adapter.md` — Phase B2: ItemCatalogAdapter.full_sync()
- `docs/sdds/canary/ncr-counterpoint-customer-adapter.md` — Phase B1: CustomerRosterAdapter.full_sync()
- `docs/sdds/canary/ncr-counterpoint-paycode-adapter.md` — Phase A4: PayCodeAdapter.seed()
- `docs/sdds/canary/ncr-counterpoint-tsp-adapter.md` — Phase C: document poll loop
- `docs/sdds/canary/ncr-counterpoint-module-q-chirp-wiring.md` — GARDEN_CENTER_ALLOW_LISTS; COUNTERPOINT_RULE_IDS
