---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Jeremy Combined Session — growdirect.io Publish + gLog Swagger Schema
**Work Orders:** WO-JEREMY-PUBLISH + B-058 Dispatch 5
**Date:** February 28, 2026
**Dispatched by:** ALX
**Priority:** 🔴 HIGH — Jeffe has been waiting on the site. gLog Swagger is investor-facing.
**Session type:** Deploy + Documentation (NO TSP code this session)

---

## Why This Session

Condor is running B-066 + B-067-A right now. Those deliverables gate your next TSP build session. While Condor works, you clear two unblocked items that have been sitting on the board:

1. **growdirect.io publish** — deploy package is staged, just push it
2. **gLog Swagger schema** — API documentation only, no code

Neither touches the Canary codebase. Neither has dependencies. Both ship today.

---

## Context — Code Branch Executed Today

Before you start: the code branch happened this session.
- `sprint-5-baseline` tagged at `72d0082`
- `sprint-6-tsp` branch created at `996562f` (33 files, 3,247 lines)
- **You already pushed both to origin from the Mac Mini.** ✅
- Your working branch is now `sprint-6-tsp`. Do NOT switch branches during this session.

---

## Task 1: Publish growdirect.io (30 min)

Full work order: `_ALX/WorkOrders/Jeremy/WO-JEREMY-PUBLISH.md`

### Deploy Package
```
~/GrowDirect/growdirect-deploy/
├── index.html              ← landing page (bird + soundtrack + Jeffe's quote)
├── favicon.svg             ← bird icon
├── CNAME                   ← growdirect.io
├── README.md               ← patent-pending notice only
├── .gitignore
└── assets/
    ├── brand/ (apple-touch-icon, favicon PNGs)
    └── social/ (og-1200x630.png)
```

### Steps
1. Create repo `growdirectprez.github.io` on GitHub (public, no README)
2. From `~/GrowDirect/growdirect-deploy/`:
   ```bash
   git init
   git add -A
   git commit -m "Initial site launch — patent pending, Feb 2026"
   git branch -M main
   git remote add origin https://github.com/growdirectprez/growdirectprez.github.io.git
   git push -u origin main
   ```
3. Enable GitHub Pages: Settings → Pages → Deploy from branch → main / root → Save
4. Verify: `https://growdirectprez.github.io` loads within 60 seconds
5. Hand Jeffe the DNS instructions (A records + CNAME for GoDaddy). Do NOT touch MX records.

### What NOT to push
- Nothing from `_ALX/`, `Canary/`, or `Canary_IP/`
- No internal team names
- No credentials or API keys

### Done when
- Site loads at `growdirectprez.github.io`
- Jeffe can view from phone
- DNS instructions documented for custom domain step

---

## Task 2: gLog API Schema — Swagger Definition (45 min)

### Context
Read B-058 work order first: `_ALX/WorkOrders/WORKORDER_B058_WarChest_MasterDispatch.md`

This is **Dispatch 5** of the War Chest. API documentation only — no build, no deploy, no code. The Swagger definition IS the LEO asset. Will has already delivered LEO-friendly description language. Use it.

### What to Produce

**File:** Swagger/OpenAPI 3.0 YAML definition

**Endpoint:** `jeffe.io/glog` (future — schema definition only for now)

**Six properties:**
| Property | Type | Description |
|---|---|---|
| `merchant_id` | string | Square merchant identifier |
| `event_hash` | string | SHA-256 hash of the sealed evidence record |
| `inscription_id` | string | Bitcoin Ordinal inscription identifier |
| `block_height` | integer | Bitcoin block height at time of inscription |
| `previous_inscription_id` | string | Previous inscription in the chain (hash chain link) |
| `replay_from` | string | Earliest inscription ID to replay the full evidence chain |

### Coordinate with
- **Will:** LEO-friendly description language (already delivered — check `_ALX/WorkOrders/output/Will/`)
- **PhD:** Narrative framing (Brief 5 v2.0 delivered — check `_ALX/WorkOrders/output/PhD/`)

### Done when
- Swagger YAML committed (location TBD — can be in elJeffe API repo or staged for future commit)
- Schema validates against OpenAPI 3.0 spec
- Descriptions use Will's LEO terminology

---

## Standing Directives

- **B-063:** SDK version check is Step 0 of every session. `pip show squareup` → confirm v43+.
- **B-064:** Heartbeat rule applies. But this session is publish + docs — no TSP code.
- **No Canary code changes this session.** These are parallel-track items.

---

## Session Close

Update HANDOFF.md:
- growdirect.io: live URL, DNS instructions handed to Jeffe
- gLog Swagger: file location, validation status
- Note: waiting on Condor B-066 + B-067-A before next TSP session

Log timelog per TRIAGE Step 0.

---

*ALX | February 28, 2026 | WO-JEREMY-PUBLISH + B-058 D5*
*Parallel dispatch while Condor clears B-066 + B-067-A gates*
