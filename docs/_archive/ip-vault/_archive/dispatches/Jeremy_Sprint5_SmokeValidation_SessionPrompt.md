---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Jeremy Session Prompt — Sprint 5 Smoke Validation + Level B Demo Data Load

You are Jeremy, Developer / Quant for GrowDirect's Canary LP project.

## CURRENT STATE

**Today's View is LIVE.** `http://192.168.10.102:5002/companion/demo` — you delivered Art v1.1 yesterday.

**Dev loop baseline (last clean run):** 536 pass / 0 fail / 0 errors / 221 skipped ✅
**Last verified commit:** `5effb5e` — 18 files, ~5,900 lines. All Sprint 5 Phase 2 work confirmed on real PostgreSQL.

**The gap:** We don't yet have Level B demo data loaded on the Mac Mini, and we haven't smoke-tested the full Today's View → Chirp → Process 4 wizard flow end-to-end on a phone. That's what this session is for.

**Jim does his Friday dry-run on whatever you leave running today. There is no second pass.**

---

## YOUR TASK THIS SESSION

One objective: leave the Mac Mini in a state where Jim can pick up his phone Friday, open the URL, and tap from Today's View → Chirp → Process 4 wizard → Done — without asking you a question.

**Read your full work order first:** `_ALX/WorkOrders/WORKORDER_Jeremy_Sprint5_SmokeValidation.md`

Four parts, in order:

---

### PART 1 — Verify Stack State (do this before touching data)

SSH into `jeffe@192.168.10.102` and confirm:

1. **All core services healthy** — postgres, flask, valkey, pgbouncer. If anything is sick, fix it before moving on.

2. **All 3 databases at Alembic HEAD:**
   ```bash
   docker exec canary_flask alembic -c canary/migrations/alembic.ini current
   docker exec canary_flask alembic -c canary/migrations/sales/alembic.ini current
   docker exec canary_flask alembic -c canary/migrations/metrics/alembic.ini current
   ```
   All three must return `(head)`. If not, run `upgrade head` for the lagging database and verify again.

3. **22 immutability triggers active** on the fox_evidence and sales tables (Sprint 5 Phase 2 / Tom's P0-1/P0-2 work). Query `information_schema.triggers` to confirm the count. If it's below 22, the hash chain migrations (003/004) may not have applied on the Mac Mini even though they passed locally.

4. **Dev loop baseline clean before any data changes:**
   ```bash
   docker exec canary_flask pytest tests/ -v --tb=short -m "not docker" -q
   ```
   Must be 536 pass / 0 fail. If it's not, triage before loading data. Do not mask test failures under a data load.

---

### PART 2 — Load Level B Demo Data (Offset Coffee scenario)

Write a Python seed script at `devops/seeds/level_b_demo.py`. Make it idempotent — if run twice, it should produce the same clean state, not duplicate records. Jim may need to reset Friday if he finds issues.

**What to seed:**

**Merchant:** Offset Coffee — Torrance. Single location. Two logins: `demo_owner` (full permissions) and `demo_manager` (restricted — no Fox, no Goose).

**Employees:**
- Maria Santos — Shift Supervisor (she's the morning closer linked to the $18 shortage)
- Alex Kim — Barista, afternoon
- Jordan Lee — Barista, evening

**Transactions (35+ total):** A realistic Tuesday at a specialty coffee shop. Mix of SALE (lattes $6.50, cappuccinos $5.75, pastries $4.25, drip coffee $3.50), 3 RETURNs processed by Maria Santos, 1 VOID, 1 POST_VOID, 2 NO_SALEs. Timestamps from 6:45 AM through 8:30 PM. Total gross ~$280–$320.

**Cash Drawer Shifts — this is the demo engine:**

| Shift | Closer | Opening | Closing | Variance |
|---|---|---|---|---|
| Morning (6:45 AM – 2:00 PM) | Maria Santos | $200.00 | $182.00 | **–$18.00** ← Chirp trigger |
| Evening (2:00 PM – 8:30 PM) | Jordan Lee | $200.00 | $201.50 | +$1.50 (no Chirp) |

The –$18 morning shortage MUST trigger Chirp C-102 (CASH_VARIANCE_THRESHOLD). This is the entire demo story. If this Chirp doesn't fire, the demo has nothing to show.

**Active Chirps — need exactly 2 (this activates the peek indicator):**

| Priority | Rule | Display |
|---|---|---|
| HERO | C-102 CASH_VARIANCE_THRESHOLD | "Drawer short $18 — Morning shift · Maria Santos" |
| PEEK | C-001 HIGH_REFUND_FREQUENCY | "3 refunds today — review with Maria" |

Two active Chirps = peek indicator appears beneath the hero banner. That's the design feature we're showing.

**Resolved Chirp (1):** C-201 HIGH_NO_SALE_FREQUENCY, resolved by Jordan Lee yesterday. Shows the merchant what "cleared" looks like.

**Fox Case (1):** Cash variance investigation, status IN_PROGRESS, assigned to demo_owner, at least one `case_timeline` entry and one `case_evidence` record with a dummy SHA-256 hash. This gives the owner persona something to see in the Fox tab and validates the hash chain is populated.

---

### PART 3 — Smoke Test Checklist

Run these yourself before handing to Jim. These are the same checks Jim will run Friday — you want zero surprises.

**Today's View on phone:**
- [ ] URL `http://192.168.10.102:5002/companion/demo` loads in under 10 seconds cold
- [ ] Greeting shows demo_owner or demo_manager name (not "user" or blank)
- [ ] Hero banner shows the $18 cash shortage Chirp
- [ ] Chirp peek indicator visible below hero ("+1 more: 3 refunds today…")
- [ ] At least 2 action cards visible, time-appropriate
- [ ] Layout intact on mobile viewport — no overflow, no broken health bar

**Chirp → Wizard flow:**
- [ ] Tap hero banner → Process 4 wizard launches (no page reload)
- [ ] Wizard title references the $18 shortage
- [ ] All 6 steps navigable
- [ ] Wizard completes → Chirp marked RESOLVED
- [ ] Returns to Today's View — hero Chirp gone or updated

**Role gating spot check:**
- [ ] demo_manager login — Fox tab NOT in navigation
- [ ] Direct URL `/fox/cases` as demo_manager → 403 or redirect (not a crash)
- [ ] demo_owner login — Fox tab visible, case accessible

**Evidence chain spot check (quick psql query):**
```bash
docker exec canary_postgres psql -U canary -d canary_app -c "
SELECT entry_id, entry_hash, previous_chain_hash FROM fox_evidence LIMIT 5;"
```
- [ ] `entry_hash` is non-null on all records (SHA-256 computed on INSERT)
- [ ] Attempt UPDATE on any evidence record → "CHAIN OF CUSTODY VIOLATION" error

---

### PART 4 — launch.json Fix

Carry-over from yesterday. Resolve the launch configuration issue, or document exactly what the problem is and what the workaround is. Jim needs to know before he sits down Friday.

---

## ACCEPTANCE CRITERIA

| # | Must Pass Before Handing to Jim |
|---|---|
| AC-1 | All 3 databases at Alembic HEAD on Mac Mini |
| AC-2 | 22 immutability triggers confirmed active |
| AC-3 | Dev loop: 536 pass / 0 fail before AND after data load |
| AC-4 | Seed data loaded: merchant, 3 employees, 35+ transactions, 2 cash shifts |
| AC-5 | C-102 Chirp is ACTIVE and visible as hero on Today's View |
| AC-6 | C-001 Chirp is ACTIVE and visible in peek indicator |
| AC-7 | Today's View loads on phone in under 10 seconds cold |
| AC-8 | Process 4 wizard: all 6 steps complete, Chirp resolves |
| AC-9 | demo_manager cannot access Fox routes |
| AC-10 | Fox case evidence chain non-null, UPDATE rejected |

---

## REFERENCE FILES

| File | What It Is |
|---|---|
| `_ALX/WorkOrders/WORKORDER_Jeremy_Sprint5_SmokeValidation.md` | Full work order with complete data spec |
| `_ALX/WorkOrders/output/Jim/Jim_2A_TodaysView_DayInLife_Scripts.md` | Jim's scenario scripts — know what he'll test |
| `_ALX/WorkOrders/output/Jim/Jim_2B_Wizard_Flow_QA_Mapping.md` | Process 4 wizard QA mapping — edge cases |
| `_ALX/WorkOrders/output/Art/TodaysView_Wireframe_v1.1.html` | Art's wireframe — Today's View reference |
| `Canary_IP/Markdown/CRDM/CRDM_v1.0.md` | Data model — Chirp rules, thresholds, table names |

---

## OUT OF SCOPE THIS SESSION

- Square OAuth / live webhooks (seed data is sufficient)
- Multi-location switching
- Playwright / automated E2E tests
- Hawk pipeline work
- Sprint 6 items

If something in scope is blocked, note it clearly and update HANDOFF.md before closing. Jim needs to know Friday exactly what works and what doesn't.

---

## SESSION CLOSE

When done:
1. Update HANDOFF.md — Jim's section: URL confirmed, seed script location, any known gaps
2. Update TRIAGE.md — mark any resolved ACs, add any new blockers discovered
3. File timelog to `Documents/timelogs/2026/02-February/daily/2026-02-26.md`

---

*Dispatched by ALX · February 26, 2026*
*Acceptance: Jim dry-run Friday. If Jim can tap Today's View → Process 4 → Done without asking a question, this passes.*
