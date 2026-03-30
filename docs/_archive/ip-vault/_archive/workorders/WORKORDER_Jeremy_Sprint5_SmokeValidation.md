---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# WORK ORDER: Jeremy — Sprint 5 Smoke Validation + Level B Demo Data Load
*Issued by ALX · February 26, 2026 · Priority: 🔴 CRITICAL — Demo Monday March 3*

**Context:** Today's View is live at `http://192.168.10.102:5002/companion/demo`. The stack is serving. Now we need to confirm that the Sprint 3/5 schema work (migrations, triggers, hash chain) is correctly loaded on the Mac Mini Docker container, that the app can be smoke-tested end-to-end, and that the Level B demo data (Offset Coffee scenario) is loaded and readable through the UI.

**Goal:** Walk out of this session with one sentence: "The Mac Mini stack is running, all migrations are at HEAD, the Level B seed data is loaded, and I can tap through Today's View → Chirp → Process 4 wizard on a phone connected to local WiFi."

**Jim's Friday dry-run depends on this work order being complete.**

---

## PART 1 — VERIFY STACK STATE ON MAC MINI

Before loading any data, confirm the container is in the state we think it's in.

### Step 1A: Services Health Check

SSH into the Mac Mini and confirm all containers are healthy:

```bash
ssh jeffe@192.168.10.102
cd ~/GrowDirect/Canary
docker compose --env-file devops/.env.alpha3x -f devops/docker-compose.alpha3x.yml ps
```

**Expected:** All core services healthy or running:
- `canary_postgres` — healthy
- `canary_flask` — healthy
- `canary_valkey` — healthy
- `canary_pgbouncer` — healthy

If any service is not healthy: run `docker logs <service_name>` and fix before proceeding. Do not move to Step 1B with a sick container.

### Step 1B: Migration State Check

Confirm all three databases are at Alembic HEAD:

```bash
docker exec canary_flask alembic -c canary/migrations/alembic.ini current
docker exec canary_flask alembic -c canary/migrations/sales/alembic.ini current
docker exec canary_flask alembic -c canary/migrations/metrics/alembic.ini current
```

**Expected:** Each returns `<revision_hash> (head)` — no pending migrations.

If any database is NOT at HEAD: run `upgrade head` for that database only:

```bash
docker exec canary_flask alembic -c canary/migrations/<config>.ini upgrade head
```

Then re-run the check. All three must be at HEAD before proceeding.

### Step 1C: Immutability Trigger Verification

Confirm the 22 INSERT-only triggers deployed in Sprint 5 Phase 2 are active:

```bash
docker exec canary_postgres psql -U canary -d canary_app -c "
SELECT trigger_name, event_object_table
FROM information_schema.triggers
WHERE trigger_schema = 'public'
ORDER BY event_object_table, trigger_name;
"
```

**Expected:** 22 triggers across the 10 immutability-protected tables (see CRDM v1.0 for the full list — sales, refund_links, transactions, fox_evidence, etc.).

If trigger count is below 22: the hash chain migrations (003/004) may not have applied. Re-run migrations and verify pgcrypto extension is loaded.

### Step 1D: Dev Loop Baseline

Run a quick test pass to confirm the container is not in a broken state before any data manipulation:

```bash
docker exec canary_flask pytest tests/ -v --tb=short \
  --ignore=tests/browser --ignore=tests/e2e \
  -m "not docker" \
  -q
```

**Expected:** 536 pass / 0 fail (matching the last clean baseline).

**If tests fail:** Triage before loading any data. A broken baseline means data loading may mask real failures. Fix the tests first.

---

## PART 2 — LEVEL B DEMO SEED DATA

This data represents a single Offset Coffee location on a normal Tuesday. It is designed so that Jim's Friday dry-run produces a realistic, navigable demo experience for a specialty coffee merchant.

### Merchant & Account Setup

Create or verify a merchant account seeded with the following profile:

| Field | Value |
|---|---|
| Business name | Offset Coffee — Torrance |
| Business type | Specialty coffee, café |
| Location | 1 location (Torrance, CA) |
| POS system | Square |
| Owner login | `demo_owner` / password per `.env.alpha3x` |
| Manager login | `demo_manager` / password per `.env.alpha3x` |

**Note:** Use the existing test credential pattern from `.env.alpha3x.template`. Do not hardcode passwords in this work order.

### Employees

Seed 3 employees for the timecard and "who touched it last?" wizard step:

| Name | Role | Notes |
|---|---|---|
| Maria Santos | Shift Supervisor | Morning closer — associated with the variance Chirp |
| Alex Kim | Barista | Afternoon shift |
| Jordan Lee | Barista | Evening shift |

### Transactions (35 minimum)

Load a realistic Tuesday at a specialty coffee shop. Mix:

| Type | Count | Notes |
|---|---|---|
| SALE | 28 | Lattes $6.50, cappuccinos $5.75, pastries $4.25, drip coffee $3.50. Occasional tip lines. Realistic item names and cents. |
| RETURN | 3 | One wrong order refund (~$6.50), one pastry returned unopened (~$4.25), one split transaction correction (~$11.00). All processed by Maria Santos. |
| VOID | 1 | Register mis-ring, immediately voided by Alex Kim. |
| POST_VOID | 1 | End-of-day batch correction. |
| NO_SALE | 2 | Drawer opens without transaction (making change). Morning and mid-shift. |

Transaction timestamps should span a realistic Tuesday: 6:45 AM open through 8:30 PM close.

**Total transaction volume:** approximately $280–$320 gross sales for the day.

### Cash Drawer Shifts

| Shift | Status | Opening Cash | Closing Cash | Variance | Notes |
|---|---|---|---|---|---|
| Morning (Maria, 6:45 AM – 2:00 PM) | CLOSED | $200.00 | $182.00 | **–$18.00** | This is the Chirp trigger. Cash short $18 at Maria's close. |
| Evening (Jordan, 2:00 PM – 8:30 PM) | CLOSED | $200.00 | $201.50 | +$1.50 | Within tolerance — no Chirp. |

**Important:** The $18 morning shortage MUST trigger Chirp C-102 (CASH_VARIANCE_THRESHOLD). This is the demo centerpiece — the merchant sees this Chirp on Today's View, taps it, and walks through Process 4. If this Chirp does not fire, the demo has no story.

### Active Chirps (2 — required for peek indicator)

The Chirp peek indicator only appears when 2+ Chirps are active. We need exactly two active Chirps going into Jim's dry-run.

| Chirp | Rule | Status | Display Text |
|---|---|---|---|
| C-1 (HERO) | C-102 CASH_VARIANCE_THRESHOLD | ACTIVE | "Drawer short $18 — Morning shift · Maria Santos" |
| C-2 (PEEK) | C-001 HIGH_REFUND_FREQUENCY | ACTIVE | "3 refunds today — review with Maria" |

This gives Today's View: hero banner (the shortage), peek indicator (+1 more: refund pattern), and the Process 4 wizard is the primary demo flow.

### 1 Resolved Chirp

Seed one previously resolved Chirp to show the merchant what "cleared" looks like:

| Chirp | Rule | Status | Resolved By | Notes |
|---|---|---|---|---|
| C-0 (RESOLVED) | C-201 HIGH_NO_SALE_FREQUENCY | RESOLVED | Jordan Lee | 3 no-sales yesterday — resolved, documented. |

### Fox Case (1 — owner-only visibility)

Seed one in-progress Fox case so the Owner login can see the Fox tab is functional:

| Field | Value |
|---|---|
| Case type | Cash variance investigation |
| Status | IN_PROGRESS |
| Created from | Manual (not from wizard — keeps it simple) |
| Assigned to | demo_owner |
| Notes | "Morning shortage under review. Maria interviewed." |

This case should have at least one `case_timeline` entry and one `case_evidence` entry with a dummy file hash. This verifies the hash chain is working, gives Jim something to show the owner persona, and confirms the Fox tables are populated.

---

## PART 3 — SMOKE TEST CHECKLIST

Once data is loaded, run through each of these checks before declaring done. These are the same checks Jim will run Friday — do them yourself first so Jim has a clean surface.

### 3A: Today's View on Phone

Connect a phone to the same WiFi as the Mac Mini. Open:
```
http://192.168.10.102:5002/companion/demo
```

Verify:
- [ ] Today's View loads in under 10 seconds (cold load)
- [ ] Greeting shows the owner or manager name (not "user" or blank)
- [ ] Hero banner shows: "Drawer short $18 — Morning shift · Maria Santos" (or equivalent)
- [ ] Chirp peek indicator is visible below the hero ("+ 1 more: 3 refunds today…")
- [ ] At least 2 action cards visible — "Count the Drawer" and one other time-appropriate card
- [ ] Health bar renders without layout break on mobile viewport

### 3B: Chirp Tap → Wizard Launch

From Today's View on phone:
- [ ] Tap the hero Chirp banner
- [ ] Process 4 wizard launches (full-screen overlay, no page reload)
- [ ] Wizard title references the cash shortage ($18)
- [ ] Step 1 shows "Was the drawer actually short $18?" with Yes/No
- [ ] Tapping Yes advances to Step 2
- [ ] Step 2 shows the employee list — Maria Santos appears
- [ ] Step 3 shows 4 cause cards (refund missed / math error / theft / other)
- [ ] Step 4 shows the fix checklist
- [ ] Step 5 shows the "add to playbook" toggle
- [ ] Step 6 shows completion screen
- [ ] Chirp marked RESOLVED after wizard completes
- [ ] Returns to Today's View — hero Chirp is gone or updated

### 3C: Role Gating Spot Check

Log in as `demo_manager`:
- [ ] Fox tab NOT visible in navigation
- [ ] Navigating directly to `/fox/cases` returns 403 or redirect

Log in as `demo_owner`:
- [ ] Fox tab visible
- [ ] Fox case from Part 2 is accessible
- [ ] case_timeline shows at least 1 entry

### 3D: Evidence Chain Spot Check

Using psql or a direct DB query, verify the immutability layer is working:

```bash
docker exec canary_postgres psql -U canary -d canary_app -c "
SELECT entry_id, entry_hash, previous_chain_hash
FROM fox_evidence
LIMIT 5;
"
```

- [ ] Records have non-null `entry_hash` (SHA-256 computed on INSERT)
- [ ] Records have `previous_chain_hash` or NULL for first record (chain linked)
- [ ] Attempt UPDATE on any evidence record → expect "CHAIN OF CUSTODY VIOLATION" error

---

## PART 4 — LAUNCH.JSON FIX

This was flagged as a remaining task from yesterday. Resolve it this session.

Identify the launch configuration issue in VS Code / dev tooling that is preventing clean debug runs. If it's a path or interpreter issue, fix it. If it's a non-critical tooling preference, document what the issue is and what the workaround is so Jeffe and Jim aren't confused by it during the Friday dry-run.

---

## ACCEPTANCE CRITERIA

| # | Criterion | Owner |
|---|---|---|
| AC-1 | All three databases at Alembic HEAD on Mac Mini container | Jeremy |
| AC-2 | 22 immutability triggers confirmed active | Jeremy |
| AC-3 | Dev loop baseline: 536 pass / 0 fail before and after data load | Jeremy |
| AC-4 | Level B seed data loaded: merchant, 3 employees, 35+ transactions, 2 cash drawer shifts | Jeremy |
| AC-5 | 2 active Chirps (C-102 hero + C-001 peek) are firing and visible on Today's View | Jeremy |
| AC-6 | Today's View loads on phone in under 10 seconds cold | Jeremy |
| AC-7 | Process 4 wizard launches from hero tap, completes all 6 steps, Chirp resolves | Jeremy |
| AC-8 | Role gating: demo_manager cannot access Fox routes | Jeremy |
| AC-9 | Fox case from seed data visible to demo_owner, evidence chain non-null | Jeremy |
| AC-10 | launch.json issue documented or resolved | Jeremy |

**The gate test:** Jim picks up his phone, opens `http://192.168.10.102:5002/companion/demo`, and can tap from Today's View → Chirp → Process 4 wizard → Done, without asking Jeremy a question.

---

## WHAT IS OUT OF SCOPE FOR THIS WORK ORDER

- Square OAuth or live webhook ingestion (seed data is sufficient)
- Multi-location switching
- Role gating beyond the spot check in 3C
- Playwright / E2E automated tests (Jim owns the manual dry-run)
- iMac → cloud deploy pipeline
- Any Sprint 6 work

---

## FILE LOCATIONS

| File | Path |
|---|---|
| This work order | `_ALX/WorkOrders/WORKORDER_Jeremy_Sprint5_SmokeValidation.md` |
| Deploy script (reference) | `Canary/devops/canary_deploy.sh` |
| Jim's scenario scripts | `_ALX/WorkOrders/output/Jim/Jim_2A_TodaysView_DayInLife_Scripts.md` |
| Jim's wizard QA mapping | `_ALX/WorkOrders/output/Jim/Jim_2B_Wizard_Flow_QA_Mapping.md` |
| Art v1.1 wireframe | `_ALX/WorkOrders/output/Art/TodaysView_Wireframe_v1.1.html` |
| CRDM v1.0 | `Canary_IP/Markdown/CRDM/CRDM_v1.0.md` |

---

## ESTIMATED EFFORT

**4–6 hours.** Migration validation and smoke tests are mechanical if the stack is healthy. The seed data load is the bulk of the work — write it once as a Python seed script (`devops/seeds/level_b_demo.py`) so it can be re-run cleanly if Jim finds issues Friday and we need to reset.

**Recommend:** Write the seed script first (Part 2), run it, then do smoke tests (Part 3). That way you have a repeatable reset path for Friday.

---

## HANDOFF TO JIM

When this work order is complete, update HANDOFF.md with:
- Mac Mini URL confirmed working on phone
- Seed script location
- Any known limitations or workarounds Jim should know before Friday dry-run
- Any AC items that are partial — be honest, Jim needs to know what to expect

---

*Issued by ALX.*
*Acceptance review: Jim dry-run Friday Feb 28. If Jim can tap from Today's View to Process 4 completion without asking Jeremy a question, this work order passes.*
