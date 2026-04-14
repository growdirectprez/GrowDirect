# LP Integration

> **Type:** External Integration (Angel)
> **Status:** Proposed -- scaffolding code exists, not yet deployed
> **Namespace:** angel
> **Date:** 2026-04-13 (ops upgrade from 2026-04-06 design spec)
> **Dependencies:** Cove Flask (port 5002), PostgreSQL (`cove` DB), Twilio, Luxury Presence, Compass CRM
> **Wiki:** [[Brain/wiki/south-bay-wiki-architecture|South Bay Wiki Architecture]] -- [[Brain/projects/Angel|Angel MOC]]

---

## Purpose

LP Integration receives real estate lead submissions from AngeliqueLyle.com
(hosted on Luxury Presence) via HMAC-signed webhooks and a client-side JS
bridge fallback. It normalizes incoming payloads, stores leads in the `cove`
database, triggers SMS notification to Angelique via Twilio, and queues
asynchronous enrichment (APN matching, Compass CRM sync). LP's native CRM
remains the safety net -- every form submission is captured by LP first; the
Angel pipeline is additive.

---

## Dependencies

| Dependency | Type | Required | Notes |
|-----------|------|:--------:|-------|
| Cove Flask | App host | Yes | Angel is a Cove module, port 5002 |
| PostgreSQL (`cove` DB) | Database | Yes | `leads` table, `raw_payload` JSONB |
| Valkey DB 1 | Cache/session | Yes | Shared with Cove |
| Luxury Presence | External | Yes | Webhook source, CRM safety net |
| Twilio | External | No (degraded) | SMS notifications to Angelique |
| Compass CRM | External | No (degraded) | Async lead sync, not yet implemented |
| Ollama | Internal | No | Future: lead scoring, AI enrichment |

---

## Data Flow & PII Map

### What Enters

LP Custom Webhook or JS bridge sends `POST /api/webhooks/lp` with JSON body
and `X-Webhook-Signature` header (HMAC-SHA256). Payload originates from four
form types on AngeliqueLyle.com:

| Form | Fields Submitted | Interest Type |
|------|-----------------|---------------|
| Contact Form (Section 10) | first_name, last_name, email, phone, interest_select, message | varies |
| Welcome Guide (Section 07) | name, email, interest_select | `welcome_guide` |
| Let's Connect Modal | name, email, message | `general` |
| Home Worth Modal | address, name, email | `selling` |

### What's Stored

**Table: `leads`** (PostgreSQL, `cove` database)

| Field | Column Type | PII Classification | Encryption Status | Notes |
|-------|------------|:------------------:|:-----------------:|-------|
| `id` | String(36) PK | public | none | UUID, no PII |
| `apn` | String(20) | public | none | Parcel ID, defaults to "UNKNOWN" |
| `first_name` | String(100) | **sensitive** | **PLAINTEXT** | Contact PII |
| `last_name` | String(100) | **sensitive** | **PLAINTEXT** | Contact PII |
| `email` | String(255) | **sensitive** | **PLAINTEXT** | Contact PII |
| `phone` | String(20) | **sensitive** | **PLAINTEXT** | Contact PII |
| `interest_type` | String(50) | internal | none | Buying/selling/etc |
| `message` | Text | **sensitive** | **PLAINTEXT** | May contain personal details |
| `page_url` | String(500) | internal | none | Source page URL |
| `referrer` | String(500) | internal | none | HTTP referrer |
| `raw_payload` | JSONB | **sensitive** | **PLAINTEXT** | Full webhook body -- contains ALL PII fields |
| `lp_lead_id` | String(100) | internal | none | LP's internal ID |
| `status` | String(20) | internal | none | Pipeline stage |
| `created_at` | DateTime | internal | none | Record timestamp |
| `updated_at` | DateTime | internal | none | Last modification |

### What Exits

| Destination | Data Sent | Transport | Status |
|------------|-----------|-----------|--------|
| SMS (Twilio) | Lead name, interest type, page URL | HTTPS API | Not yet implemented |
| Compass CRM | Lead contact info, interest, source | HTTPS API | Not yet implemented |
| Angel dashboard (UI) | All lead fields | Cove Flask session-auth | Not yet built |
| Webhook response | `{status, lead_id}` | HTTPS 200 | Working |
| Application logs | Lead ID (truncated), name, email | stdout | **PII in logs** |

---

## External Integration: Signature Validation

### HMAC-SHA256 Verification

LP sends `X-Webhook-Signature: sha256=<hex_digest>` on every webhook POST.
The endpoint validates before processing:

```
1. Extract raw request body bytes (before JSON parse)
2. Read X-Webhook-Signature header
3. Split on "=" to get algorithm + provided digest
4. Reject if algorithm != "sha256" or header missing
5. Compute HMAC-SHA256(raw_body, LP_WEBHOOK_SECRET)
6. Constant-time compare via hmac.compare_digest()
7. Return 401 Unauthorized on mismatch
```

**Implementation:** `Angel/angel/routes/webhooks.py` -- `verify_webhook_signature()`

**Current state:** Correctly implemented with constant-time comparison. Uses
`hmac.compare_digest()` which prevents timing attacks.

### Credential Storage

| Secret | Current Storage | Production Target |
|--------|----------------|-------------------|
| `LP_WEBHOOK_SECRET` | `.env` file | AWS Secrets Manager |
| `TWILIO_SID` | `.env` file | AWS Secrets Manager |
| `TWILIO_AUTH_TOKEN` | `.env` file | AWS Secrets Manager |
| `SECRET_KEY` | `.env` (default: `dev-secret-key-change-in-prod`) | AWS Secrets Manager |

**Finding:** Config falls back to hardcoded dev secrets if env vars are missing.
`SECRET_KEY` default value is a known string. See Code Review Findings CR-06.

---

## External Integration: Retry & Idempotency

### LP Retry Behavior

LP retries on non-2xx responses. The endpoint must be idempotent to handle
retries safely.

**Current deduplication strategy (designed, not fully implemented):**

1. Match by `lp_lead_id` if LP provides an internal ID
2. Match by email + 5-minute window (same email within 5 min = same lead)
3. Match by phone + 5-minute window (fallback if email is blank)
4. Merge strategy: if duplicate arrives with additional fields, merge data
   rather than discard

**Current state:** Deduplication is specified but NOT implemented in code. Every
POST creates a new `Lead` record. Retries from LP will create duplicate leads.
See Code Review Findings CR-04.

### JS Bridge (Fallback Path)

The JS bridge (`angelique-behavior.js` -- `initWebhookBridge()`) captures form
`submit` events client-side and POSTs to the same endpoint with
`keepalive: true`. Both paths feed `/api/webhooks/lp`, so a single form
submission may arrive twice (once from LP webhook, once from JS bridge).
Deduplication is critical.

---

## External Integration: Degradation Behavior

### When Luxury Presence Is Down

LP is the source of truth for leads. If LP is unavailable:

- LP CRM still captures leads natively (safety net)
- LP webhook delivery to Angel stops -- leads are NOT lost, just delayed
- LP's retry mechanism will deliver missed webhooks when connectivity restores
- JS bridge also fails since the LP-hosted page is unreachable
- **Impact:** Angel sees no new leads until LP recovers
- **Mitigation:** None required -- LP CRM has the lead

### When Angel Backend Is Down

- LP native form handling continues uninterrupted (LP CRM has the lead)
- LP webhook gets non-2xx, queues for retry
- JS bridge `fetch()` fails silently (fire-and-forget with `keepalive`)
- **Impact:** Lead enrichment, SMS notification, and CRM sync delayed
- **Mitigation:** LP CRM is the safety net. Manual review of LP dashboard
  catches any leads missed during outage.

### When Twilio Is Down

- Lead is captured and stored normally
- SMS notification to Angelique fails
- **Impact:** Angelique doesn't get instant alert; must check dashboard
- **Mitigation:** Log Twilio errors, alert on consecutive failures, expose
  unnotified leads in dashboard. (Not yet implemented.)

### When Compass CRM Is Down

- Lead is captured and stored normally
- CRM sync fails, queued for retry
- **Impact:** Compass doesn't reflect new leads until sync catches up
- **Mitigation:** Retry queue with exponential backoff. (Not yet implemented.)

---

## API Contract

### Existing (Built)

| Method | Path | Purpose | Auth | Rate Limit |
|--------|------|---------|------|:----------:|
| POST | `/api/webhooks/lp` | Receive LP lead | HMAC-SHA256 | **None** |
| GET | `/api/webhooks/health` | Health check | None | None |

### Planned (Not Yet Built)

| Method | Path | Purpose | Auth |
|--------|------|---------|------|
| GET | `/api/leads` | List leads with filters | API key |
| GET | `/api/leads/<id>` | Single lead detail | API key |
| PATCH | `/api/leads/<id>` | Update lead stage/notes | API key |
| POST | `/api/leads/<id>/notify` | Trigger SMS to Angelique | API key |
| GET | `/api/stats/dashboard` | Lead pipeline summary | API key |
| POST | `/api/webhooks/lp/test` | Test webhook with sample payload | API key |

### Webhook Payload Schema

```json
{
  "first_name": "string",
  "last_name": "string",
  "email": "string",
  "phone": "string | null",
  "interest_type": "buying | selling | relocating | welcome_guide | exploring | general",
  "message": "string | null",
  "address": "string | null",
  "page_url": "string",
  "referrer": "string",
  "source": "lp_form | lp_webhook | angel_chat",
  "timestamp": "ISO 8601",
  "lp_lead_id": "string | null"
}
```

Field normalization is implemented: `name` splits to `first_name`/`last_name`,
`phone_number` maps to `phone`, `source_url` maps to `page_url`.

---

## Operations

### Startup Sequence

1. Cove Flask starts (port 5002)
2. `angel_webhook_bp` registered at `/api/webhooks`
3. DB tables created via `db.create_all()` (dev) or Alembic (prod)
4. `LP_WEBHOOK_SECRET` loaded from config

### Health Checks

| Endpoint | Method | Expected Response | Alert If |
|----------|--------|-------------------|----------|
| `/api/webhooks/health` | GET | `200 {status: "ok"}` | Non-200 for >60s |

### Failure Modes

| Failure | Detection | Impact | Recovery |
|---------|-----------|--------|----------|
| HMAC secret missing | `logger.error` on first request | All webhooks rejected 401 | Set `LP_WEBHOOK_SECRET` env var |
| Database unreachable | 500 response + exception log | Leads not stored | DB restart; LP retries |
| Malformed JSON | 400 response | Single lead dropped | Fix sender payload |
| No contact info | 422 response | Intentional rejection | Expected behavior |

### Monitoring (Target State)

| Metric | Alert Threshold | Current Status |
|--------|----------------|:--------------:|
| Webhook 401 rate | >5/hour | Not implemented |
| Webhook 500 rate | >0/hour | Not implemented |
| Lead creation rate | 0 for >24h (business hours) | Not implemented |
| Twilio failure rate | >0 consecutive | Not implemented |
| Dedup collision rate | >10% of total | Not implemented |

### Configuration (Environment Variables)

| Variable | Required | Default | Purpose |
|----------|:--------:|---------|---------|
| `LP_WEBHOOK_SECRET` | Yes | `""` (empty) | HMAC-SHA256 key for webhook validation |
| `LP_SITE_URL` | No | -- | CORS allowlist for AngeliqueLyle.com |
| `TWILIO_SID` | No | -- | SMS notification sender |
| `TWILIO_AUTH_TOKEN` | No | -- | SMS authentication |
| `TWILIO_FROM_NUMBER` | No | -- | SMS source number |
| `ANGELIQUE_PHONE` | No | -- | SMS destination |
| `SECRET_KEY` | Yes | `dev-secret-key-change-in-prod` | Flask session signing |
| `DATABASE_URL` | Yes | local Docker DSN | PostgreSQL connection |
| `VALKEY_URL` | No | `redis://growdirect_valkey:6379/3` | Session/cache backend |

---

## Deployment

### Docker Service Definition

Angel runs inside the `cove-flask` container. No separate container for LP
Integration. The webhook blueprint is registered as part of Cove's app factory.

```yaml
# In Cove/devops/docker-compose.yml
cove-flask:
  image: cove-flask
  ports:
    - "5002:5002"
  environment:
    - LP_WEBHOOK_SECRET=${LP_WEBHOOK_SECRET}
    - TWILIO_SID=${TWILIO_SID}
    - TWILIO_AUTH_TOKEN=${TWILIO_AUTH_TOKEN}
  networks:
    - growdirect
```

### AWS Target

| Component | AWS Service | Notes |
|-----------|------------|-------|
| Flask app | ECS Fargate | Cove task definition includes Angel |
| Database | RDS PostgreSQL 17 | `cove` database, shared with Cove |
| Secrets | AWS Secrets Manager | All credentials from env vars |
| Load balancer | ALB | TLS termination, route `/api/webhooks/*` |
| DNS | Route 53 | API subdomain for webhook endpoint |

### CI/CD Requirements

- Webhook endpoint must be externally reachable (LP needs to POST to it)
- TLS required (LP sends sensitive PII over the wire)
- CORS headers for `angeliquelyle.com` and `*.luxurypresence.com`
- Health check must pass before routing traffic

---

## Code Review Findings

### CR-01: All Lead PII Stored Plaintext (P0 -- Blocks Production)

**Description:** `first_name`, `last_name`, `email`, `phone`, and `message`
are stored as plaintext `String`/`Text` columns in the `leads` table. A
database compromise exposes all lead contact information in cleartext.

**Affected code:** `Angel/angel/models/lead.py` lines 45-55

**Recommended fix:** Implement field-level AES-256-GCM encryption using
Canary's `crypto.py` pattern. Encrypt `email`, `phone`, `first_name`,
`last_name`, and `message` at rest. Decrypt only on authenticated read.

**Linear:** GRO-xxx (to be created)

---

### CR-02: Raw Webhook Payload Preserves All PII (P0 -- Blocks Production)

**Description:** The `raw_payload` JSONB column stores the complete webhook
body including all contact fields. Even if individual columns are later
encrypted, the raw payload retains plaintext copies of every PII field.

**Affected code:** `Angel/angel/routes/webhooks.py` line 137:
`raw_payload=payload`

**Recommended fix:** Redact PII fields from `raw_payload` before storage.
Keep structural fields (`interest_type`, `page_url`, `source`, `timestamp`,
`lp_lead_id`) for debugging. Replace contact fields with `"[REDACTED]"`.

**Linear:** GRO-xxx (to be created)

---

### CR-03: PII Logged in Application Logs (P1 -- Before GA)

**Description:** Lead creation success log includes first name, last name, and
email address in plaintext:
```python
logger.info("Webhook: lead created %s (%s %s / %s)", lead.id[:8], first_name, last_name, email)
```
Also logs `request.remote_addr` (IP address) on signature failure.

**Affected code:** `Angel/angel/routes/webhooks.py` lines 143-148, line 89

**Recommended fix:** Log only `lead.id` (truncated) and `interest_type`. Remove
name and email from log messages. Hash or mask IP addresses in security logs.

**Linear:** GRO-xxx (to be created)

---

### CR-04: No Idempotency / Deduplication Implemented (P1 -- Before GA)

**Description:** The deduplication strategy is documented (match by
`lp_lead_id`, then email+5min, then phone+5min) but not implemented. Every
webhook POST creates a new `Lead` record. LP retries on non-2xx will produce
duplicates. The JS bridge + LP webhook dual-delivery path guarantees duplicates.

**Affected code:** `Angel/angel/routes/webhooks.py` lines 124-139 -- no
dedup check before `db.session.add(lead)`.

**Recommended fix:** Before creating a new lead, query for existing leads
matching `lp_lead_id` (if present) or `email` + `created_at` within 5 minutes.
If found, merge additional fields and return 200 with existing `lead_id`.

**Linear:** GRO-xxx (to be created)

---

### CR-05: No Rate Limiting on Webhook Endpoint (P1 -- Before GA)

**Description:** `POST /api/webhooks/lp` has no rate limiting. A compromised
or misconfigured LP instance (or an attacker with the webhook URL) could flood
the endpoint with requests, filling the database and exhausting resources.
HMAC validation provides authentication but not rate control.

**Affected code:** `Angel/angel/routes/webhooks.py` -- no Flask-Limiter or
equivalent middleware.

**Recommended fix:** Apply Flask-Limiter to the webhook endpoint. Suggested
limits: 60 requests/minute per source IP, 10 requests/minute per unique email.

**Linear:** GRO-xxx (to be created)

---

### CR-06: Hardcoded Dev Secret Key Fallback (P0 -- Blocks Production)

**Description:** `SECRET_KEY` defaults to the string
`dev-secret-key-change-in-prod` if the environment variable is missing. If
deployed without the env var set, session cookies are signed with a known key.
`LP_WEBHOOK_SECRET` defaults to empty string, which would cause all webhook
signature checks to fail (safe-fail, but loses leads silently).

**Affected code:** `Angel/angel/config.py` lines 17, 37

**Recommended fix:** In `ProdConfig`, raise an error at startup if
`SECRET_KEY` or `LP_WEBHOOK_SECRET` is missing or set to a default value.
All secrets must come from AWS Secrets Manager in production.

**Linear:** GRO-xxx (to be created)

---

### CR-07: No Audit Trail for Lead Status Changes (P1 -- Before GA)

**Description:** The `Lead.advance()` method changes `status` and
`updated_at` but does not log who changed the status, when, or from what
previous value. No audit table or event log exists for lead pipeline
transitions.

**Affected code:** `Angel/angel/models/lead.py` lines 88-94

**Recommended fix:** Create a `lead_events` table that records
`(lead_id, old_status, new_status, changed_by, changed_at, notes)` for
every pipeline transition. Hook into `advance()` or use SQLAlchemy event
listeners.

**Linear:** GRO-xxx (to be created)

---

### CR-08: No Data Retention Policy (P1 -- Before GA)

**Description:** Leads are stored indefinitely. No automated purge exists
for old leads, raw payloads, or audit data. CA real estate regulations and
CCPA require defined retention periods and right-to-deletion support.

**Recommended fix:** Implement retention policy: leads marked `archived`
or `closed` for >12 months eligible for PII scrub (keep anonymized record
for analytics). Raw payloads purged after 90 days. Audit logs retained 24
months. Provide deletion endpoint for CCPA requests.

**Linear:** GRO-xxx (to be created)

---

### CR-09: Error Responses May Leak Internals (P2 -- Post-Launch)

**Description:** The 500 error handler returns `{"error": "Database error"}`
which is acceptably generic, but the exception is logged with full traceback
via `logger.exception()`. In a misconfigured logging setup, stack traces
could be exposed. No structured error response format is enforced.

**Affected code:** `Angel/angel/routes/webhooks.py` lines 152-155

**Recommended fix:** Ensure production logging goes to a secure log
aggregator (CloudWatch), not stdout. Standardize error response bodies.
Never include traceback content in HTTP responses (already correct).

**Linear:** GRO-xxx (to be created)

---

### CR-10: Lead Model Status Values Inconsistent (P2 -- Post-Launch)

**Description:** The `Lead` model defines two different status lists.
`LEAD_STAGES` (line 20) has 9 stages (identified through archived).
`Lead.advance()` (line 90) validates against 5 stages (new, contacted,
qualified, converted, closed). The `status` column default is `"new"` which
is not in `LEAD_STAGES`. The webhook handler sets `status="new"` which is in
neither the 9-stage list.

**Affected code:** `Angel/angel/models/lead.py` lines 20-30, 68-69, 88-94

**Recommended fix:** Consolidate to a single authoritative stage list.
Use the 9-stage pipeline from `LEAD_STAGES` with `"new"` as an alias for
`"identified"`, or add `"new"` to the stage list. Update `advance()` to
validate against the canonical list.

**Linear:** GRO-xxx (to be created)

---

### CR-11: No `source` Column on Lead Model (P2 -- Post-Launch)

**Description:** The SDD design spec calls for a `source` column to
distinguish leads from `lp_form`, `lp_webhook`, `angel_chat`, and `manual`.
The column does not exist in the model. Attribution between the JS bridge
and LP webhook paths is impossible.

**Affected code:** `Angel/angel/models/lead.py` -- column absent

**Recommended fix:** Add `source: Mapped[str] = mapped_column(String(20),
nullable=False, default="lp_form")` and set it based on payload metadata.

**Linear:** GRO-xxx (to be created)

---

## Production Readiness Checklist

- [ ] **PII encrypted at rest** -- CR-01: All contact fields stored plaintext
- [ ] **Raw payloads redacted** -- CR-02: Full PII preserved in raw_payload JSONB
- [ ] **Secrets in AWS Secrets Manager** -- CR-06: Currently in .env with hardcoded fallbacks
- [ ] **Health check endpoint responds** -- `/api/webhooks/health` returns 200 OK
- [ ] **Audit logging for sensitive operations** -- CR-07: No audit trail for pipeline changes
- [ ] **Data retention policy implemented** -- CR-08: No retention or purge automation
- [ ] **Rate limiting on public endpoints** -- CR-05: No rate limiting on webhook endpoint
- [ ] **Error responses don't leak internals** -- CR-09: Acceptable but unstructured
- [ ] **Idempotency on webhook ingestion** -- CR-04: No deduplication implemented
- [ ] **PII removed from application logs** -- CR-03: Name and email in log messages
- [ ] **CORS configured for production domains** -- Specified but not yet deployed
- [ ] **Twilio SMS notification working** -- Not yet implemented
- [ ] **Compass CRM sync working** -- Not yet implemented
- [ ] **All 4 LP form types tested end-to-end** -- No integration tests exist
- [ ] **TLS enforced on webhook endpoint** -- Requires ALB/Cloudflare in production

---

*Filed per GrowDirect doc standards: `docs/sdds/angel/lp-integration.md`*
*Service type: External Integration (Angel)*
*Source code: `Angel/angel/routes/webhooks.py`, `Angel/angel/models/lead.py`, `Angel/angel/config.py`*
*Ops upgrade: 2026-04-13 per `docs/superpowers/specs/2026-04-13-sdd-ops-upgrade-design.md`*
