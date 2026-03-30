---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Jeremy Wave 2 Session — B-067-B Dashboard Wiring + B-036 SDK→CRDM Alignment
**Work Orders:** B-067-B + B-036
**Date:** February 28, 2026 (queued — fires after Condor Wave 1 delivers)
**Dispatched by:** ALX
**Priority:** 🔴 HIGH — B-067-B completes the dashboard for Jeffe. B-036 gates Tom's B-035 DDL.
**Session type:** Build + Audit
**Depends on:** Condor B-066 + B-067-A (coding standards + capability map)

---

## GATE CHECK — DO NOT START UNTIL THESE EXIST

```
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Condor/B067_SquareCapabilityMap_v1.0.md
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Condor/Square_TSP_CodingStandards_v1.0.md
```

If either file is missing, STOP. Condor hasn't delivered yet. Do NOT build from guesses.

---

## Context — What Happened Since Last Jeremy Session

1. **Code branch executed.** You're on `sprint-6-tsp` at `996562f`. Pushed to origin. ✅
2. **Wave 1 dispatched.** You published growdirect.io + delivered gLog Swagger (B-058 D5).
3. **Condor delivered B-066 + B-067-A.** You now have:
   - Coding standards for all future TSP/Square work
   - Capability map with exact SDK method names for all 16 API families
   - Questions doc with any ambiguities flagged
4. **Qwen delivered B-067-C.** Dashboard HTML shell at `Canary/static/square_explorer.html`.
5. **Tom delivered B-068 reconciliation.** Foundation Layer COMPLETE.

**READ THE CODING STANDARDS FIRST.** `Square_TSP_CodingStandards_v1.0.md` is your bible for this session and every TSP session after.

---

## Task 1: B-067-B — Square Capability Explorer Backend (1-2 hours)

### Read First
```
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Condor/B067_SquareCapabilityMap_v1.0.md
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Condor/Square_TSP_CodingStandards_v1.0.md
/Users/geofflyle/GrowDirect/Canary/square/square-python-sdk/README.md
/Users/geofflyle/GrowDirect/Canary/static/square_explorer.html  (Qwen's shell)
```

### Full session prompt
`_ALX/WorkOrders/dispatches/Jeremy_B067B_APIModule.md` — contains the complete scaffold, return schema, and Flask blueprint spec. Follow it exactly.

### Build Two Files
1. **Explorer Module:** `canary/services/square_capability_explorer.py`
   - 16 `explore_*` functions, one per API family
   - Fill in all `pass` stubs using Condor's capability map SDK method names
   - Return schema: `{api_family, status, count, data, sdk_call, error}`
   - Dispatch table `EXPLORER_REGISTRY` already scaffolded

2. **Flask Blueprint:** `canary/blueprints/square_explorer_wired.py`
   - `GET /explore/<api_family>` → JSON
   - `GET /explorer` → serves `static/square_explorer.html`
   - Register in `canary/blueprints/registry.py`

### Wire Qwen's Shell
After building the backend, update Condor's capability map values into Qwen's dashboard HTML:
- Replace `TODO: Condor B-067-A` placeholders with real LP signals and TSP components
- Verify fetch URLs in JS match your Flask route (`/explore/<family>`)

### Test All 16
```bash
cd /Users/geofflyle/GrowDirect/Canary
python -c "
from canary.services.square_capability_explorer import EXPLORER_REGISTRY
for name, fn in EXPLORER_REGISTRY.items():
    result = fn()
    print(f'{name}: {result[\"status\"]} ({result[\"count\"]} records)')
"
```

### Scope Gap List
Write `scope_not_granted` results to:
```
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Jeremy/B067_ScopeGapList.md
```
Routes to Syd (OAuth expansion) + Eva (Phase 2 planning).

### Done When
- All 16 explore functions return real sandbox data (or clean scope_not_granted)
- Flask blueprint registered and serving
- Dashboard loads at `/explorer` and fetches live data on click
- Scope gap list on disk

---

## Task 2: B-036 — Square SDK → CRDM Alignment Audit (1-2 hours)

### Read First
```
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/WORKORDER_Jeremy_SquareSDK_CRDMAlignment.md
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Condor/B067_SquareCapabilityMap_v1.0.md
/Users/geofflyle/GrowDirect/Canary_IP/Markdown/Specs/Square_API_LP_Coverage_Analysis_Jeremy_v1.0.md
/Users/geofflyle/GrowDirect/Canary/square/square-python-sdk/README.md
```

### Why This Matters
Tom is waiting to finalize B-035 partition DDL. His schema is designed against our assumptions of what Square delivers. Before he writes DDL we build production on, you verify field-by-field that Square actually gives us what we assumed.

### Eight Verifications (from work order)

| # | Check | Verdict Needed |
|---|---|---|
| 1 | Timestamp precision | Sufficient for hourly sub-partitions? |
| 2 | Cash drawer events | Webhook push or poll-only? |
| 3 | Timecard data | Real-time state accessible for Chirp eval? |
| 4 | Card fingerprint by tender type | Full availability matrix |
| 5 | Inventory adjustments | Real-time or batch? |
| 6 | Line item detail | Full detail in `order.updated` webhook? |
| 7 | Gift card / loyalty webhook availability | Which events are push vs pull? |
| 8 | Webhook payload vs API response differences | Any fields in API but missing from webhook? |

### Use Your Explorer
You literally just built all 16 explore functions. Use them to verify real sandbox responses against CRDM assumptions. Check actual field names, types, presence/absence.

### Deliverable
```
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Jeremy/Jeremy_SquareSDK_CRDMAlignment.md
```

For each of the 8 checks:
- **Verified** or **Gap Found**
- If gap: specific field, what we assumed vs what Square actually sends, impact on CRDM/partition design
- Recommendations for Tom

### Done When
- All 8 verifications have a verdict
- Material schema gaps (if any) routed to Tom with specific field-level detail
- `card_fingerprint` availability matrix complete (routes to Syd immediately if gaps)

---

## Standing Directives

- **B-063:** `pip show squareup` → confirm v44+ before first SDK call
- **B-064:** Heartbeat rule — every line traces to a TSP PRD or a board item
- **Coding standards:** Follow Condor's `Square_TSP_CodingStandards_v1.0.md` for all SDK interaction patterns
- **All reads for B-036.** No writes to the CRDM schema — that's Tom's job.
- **Commit B-067-B to `sprint-6-tsp` branch.** This is production code.

---

## Session Close

Commit new files to `sprint-6-tsp`:
```bash
git add canary/services/square_capability_explorer.py canary/blueprints/square_explorer_wired.py canary/blueprints/registry.py
git commit -m "feat(sprint6): B-067-B Square Capability Explorer — 16 API families, Flask blueprint"
```

Update HANDOFF.md:
- B-067-B: delivered, dashboard functional, scope gap list location
- B-036: 8 verdicts, material gaps (if any), Tom unblocked (yes/no)
- Note: Tom can start B-035 DDL after reading this output

Log timelog per TRIAGE Step 0.

---

*ALX | February 28, 2026 | Wave 2 — Jeremy B-067-B + B-036*
*Completes the B-067 dashboard for Jeffe. Unblocks Tom for B-035 DDL.*
