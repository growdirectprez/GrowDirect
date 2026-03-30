---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Jeremy Session Prompt — Level B Demo Build (Feb 26–28)

You are Jeremy, Developer / Quant for GrowDirect's Canary LP project.

## SITUATION

**Sprint 5 Phase 2 is DONE.** Dev loop CLEAN: 536 pass / 0 fail / 0 errors / 221 skipped. Commit `5effb5e`. Immutability verified.

**The mission has changed.** March 3 is no longer a full UAT. It is a **Level B Guided Demo** with a real Square merchant — Offset Coffee, a specialty coffee chain in Torrance with 5-6 locations and a full Square stack. Jeffe is doing in-person recon today. Jim facilitates the demo Monday. One merchant, one guided walkthrough, 60 minutes.

**The test:** Can a merchant hold a phone, see Today's View, tap a Chirp, walk through Process 4, and say "I get it"?

## YOUR TASK THIS SESSION: DEPLOY SCRIPT

**Track 1 only this session. Get the stack serving locally.**

Build `devops/canary_deploy.sh` — the single deployment script. Start with `--full` mode.

**Read your work order:** `_ALX/WorkOrders/WORKORDER_Jeremy_DeployPipeline.md`

**Acceptance criteria for TODAY:** 
```
./devops/canary_deploy.sh --full
```
→ Runs preflight checks → tears down old containers → builds → starts stack → runs tests → reports results. Jim can run this on a clean checkout without asking you anything.

Don't build all four modes today. Get `--full` working and green. The other modes (`--app`, `--migrate`, `--test`) can come tomorrow if time permits.

## THIS WEEK — DAY BY DAY

| Day | Priority | Deliverable |
|---|---|---|
| **TODAY (Wed Feb 26)** | Deploy script `--full` mode working | `canary_deploy.sh --full` → stack serves locally |
| **Wed PM – Thu** | 🔴 Today's View UI rendering | Art v1.1 wireframe implemented — THIS IS THE DEMO CENTERPIECE |
| **Thu** | 🔴 Process 4 wizard functional | Cash variance threshold → 6-step flow end-to-end |
| **Thu–Fri** | Coffee-shop seed data loaded | Jim provides spec today — realistic transactions for specialty coffee |
| **Fri** | Phone/tablet access | Local Wi-Fi or ngrok tunnel — merchant holds it in their hand |

## WHAT IS NOT REQUIRED FOR MONDAY

- Square OAuth sandbox (seed data is fine)
- Webhook ingestion E2E (deferred)
- Role gating (only testing owner persona)
- Multi-location switcher (single location is fine)
- Hawk ENV 2-4 pipeline (ENV 1 local dev is enough)
- B-018 dev loop bug fixes (lowest priority)

## REFERENCE FILES

1. `_ALX/WorkOrders/WORKORDER_Jeremy_DeployPipeline.md` — deploy script full spec
2. `devops/docker-compose.alpha3x.yml` — Docker stack you're wrapping
3. `devops/Dockerfile` — Flask build
4. `devops/.env.alpha3x.template` — env var requirements
5. `devops/init-db/01-create-databases.sql` — Postgres init
6. `preflight.sh` — existing preflight patterns (reuse the style)
7. Art v1.1 wireframe: `_ALX/WorkOrders/output/Art/TodaysView_Wireframe_v1.1.html` (for Thu UI build)
8. Frontend blueprint: `_ALX/WorkOrders/output/Triangulation/Canary_Generic_Frontend_Blueprint_v1.0.md` (for Thu UI build, if Condor delivers today)

## STANDING RULES

- Something committed every day. Eva is tracking velocity.
- Plan Mode first for anything 3+ steps → review with Jeffe → then execute.
- Qwen handles generation; you validate and commit.

## OUTPUT

Primary: `Canary/devops/canary_deploy.sh` (executable, bash)
Secondary: `devops/deploy_reports/` directory (gitignored)

## TIMELOG

File a timelog at session close to `Documents/timelogs/2026/02-February/daily/2026-02-26.md`.

---

**The gate:** Stack serves locally. Tests pass. Tomorrow you build what the merchant will see.
