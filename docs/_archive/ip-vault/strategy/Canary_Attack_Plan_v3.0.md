---
type: strategy
domain: business
status: active
created: 2026-03-19
updated: 2026-03-19
---
# Canary LP — Attack Plan v3.0

**Date:** February 23, 2026
**Author:** Eva (Program Manager)
**Classification:** Internal — Team Operations
**Status:** ACTIVE — Sprint 5 AutoBuild running. iMac on Ubuntu. Phase 1 Boot DONE.

> *"Do it right, do it once."* — Jeffe

---

## Product North Star

> "We don't want to add to the stress. We want to ease it."
> — Jeffe, Feb 26, 2026

Every interaction with Canary must reduce merchant cognitive load.
If it requires recovery steps, explanation, or back-and-forth, it fails.
Measure everything against this sentence.

---

## Where We Are (Feb 23)

- **iMac QA box:** Ubuntu, Docker + PostgreSQL running, code pulled via terminal. Portainer retired.
- **Sprint 5 AutoBuild:** Running on Qwen (local, $0). Outputs landing now.
- **Codebase:** ~4,000 lines of syntactically valid Python across 35 models, 11 blueprints, 26 Chirp rules, Fox case service. Never integration-tested on real hardware.
- **MVP scope:** FROZEN at 27 features / 174 AC / ~31% complete.
- **Cost to date:** ~$3.25 cloud (43 Qwen prompts, ~165 SP).
- **Syd:** Out of office. 7 legal items parked.

### What's DONE (no longer tracked)

| Category | Summary |
|----------|---------|
| Sprints 1–4.5 | 43 prompts, ~165 SP, all code generated |
| P0 data integrity | INSERT-only triggers, hash chain verification, Fox evidence immutability |
| P1 schema fixes | transaction_type enum, cash_variance_cents, merchant_id, timestamps, rule_id uniqueness |
| Infrastructure | Docker Compose (alpha3x), Nginx, Keycloak realm, init-db scripts, env template |
| Blueprint prep | Flask vs FastAPI analysis (keep Flask), license review brief, version corrections |
| Phase 1 Boot | All 12 Docker services healthy on iMac Ubuntu |
| Planning docs | 4 PRDs (E0–E3), Factory Process, CRDM Bible, Technology Blueprint, Business Plan draft |
| Secrets | `devops/scripts/generate_env.sh` — all secrets env-injected |
| Fraud library | `tests/fixtures/scenarios.yaml` — 12 scenarios drafted |

---

## THE GATE

| # | Gate | Owner | Status |
|---|------|-------|--------|
| **R-1** | Technology Blueprint sign-off | PhD + Tom + Jeremy | ⬜ **IN REVIEW — everything downstream waits** |

**Sprint 5 can proceed in parallel with R-1 on the iMac.** The Blueprint review covers architectural decisions; Sprint 5 validates whether existing generated code runs. Both need to be green before UAT.

---

## ACTIVE — Sprint 5: Integration Validation (~55 SP remaining)

**Goal:** Prove ~4,000 lines of code actually run on real hardware.
**Where:** iMac Ubuntu, terminal, Docker.
**Full plan:** `Markdown/Strategy/Canary_Sprint5_Integration_Plan_v1.0.md`

### Phase 2: Schema (NEXT — after Qwen finishes)

| # | Task | Owner | SP | Status |
|---|------|-------|-----|--------|
| S5-07 | Run Alembic migrations against real PostgreSQL | Jeremy + Tom | 5 | ⬜ |
| S5-08 | Validate INSERT-only triggers fire | Tom | 2 | ⬜ |
| S5-09 | Validate hash chain verification | Jeremy | 2 | ⬜ |
| S5-10 | Run RLS policy validation | Tom + Jeremy | 3 | ⬜ |

### Phase 3: Data (after Schema is green)

| # | Task | Owner | SP | Status |
|---|------|-------|-----|--------|
| S5-11 | Seed data pump — 12 fraud scenarios | Jeremy | 3 | ⬜ |
| S5-12 | Square OAuth sandbox flow E2E | Jeremy | 3 | ⬜ |
| S5-13 | Webhook ingestion E2E (HMAC → parse → DB → Chirp) | Jeremy | 5 | ⬜ |
| S5-14 | Fox case lifecycle E2E | Jeremy | 3 | ⬜ |

### Phase 4: Tests (after Data flows)

| # | Task | Owner | SP | Status |
|---|------|-------|-----|--------|
| S5-15 | Run 276+ unit tests against PostgreSQL | Jim + Jeremy | 5 | ⬜ |
| S5-16 | Run E2E test methods against live app | Jim | 3 | ⬜ |
| S5-17 | Run Playwright browser tests | Jim | 3 | ⬜ |
| S5-18 | Triage and fix critical failures | Jeremy | 8 | ⬜ |

### Phase 5: Clickthrough (after Tests triaged)

| # | Task | Owner | SP | Status |
|---|------|-------|-----|--------|
| S5-19 | Jim's merchant journey clickthrough | Jim | 3 | ⬜ |
| S5-20 | Jeffe's CEO walkthrough | Jeffe + Eva | 2 | ⬜ |
| S5-21 | Bug fix sprint from clickthrough findings | Jeremy | 5 | ⬜ |

**Sprint 5 Exit:** Jim signs off. Jeffe has seen it running. UAT gate clears.

---

## PARKED — Do After Sprint 5

| # | Task | Owner | Notes |
|---|------|-------|-------|
| B-1 | Guided Companion route scaffolding (E0-F6) | Jeremy + Art | PRD delivered, Art can wireframe now |
| B-2 | Companion data model → CRDM mapping | Tom | Blocked by R-15 |
| B-5 | SMS Notification service (E1-F13) | Jeremy | Needs TCPA review from Syd |
| B-7 | Wireframe mockups (3 core screens) | Art | Unblocked — can start |
| B-11 | Business Plan polish → investor approval | Eva + Syd + Jess → Jeffe | Draft exists |
| R-12 | Square SDK v35→v43 migration assessment | Jeremy | Independent — can do anytime |
| R-30 | SQLAlchemy 2.0 migration | Tom + Jeremy | Tech debt, not blocking |
| R-31 | Soft-delete field standardization | Tom + Jeremy | Tech debt, not blocking |
| G-1–G-6 | Jim's Virtual Gym QA agent | Eva + Jeremy | Post Sprint 5 |
| B-12 | LEO-optimize Marketplace listing | Will + Jeremy | Pre-launch |
| R-13 | PRD updates for new stack | Eva + Jess | After R-1 gate |

---

## PARKED — Syd's Batch (7 items, when she returns)

| Item | Description |
|------|-------------|
| R-6 | Directus BSL 1.1 license decision (due Mar 31) |
| S-1 | Square partner terms review |
| S-2 | Ordinal chain-of-custody legal analysis |
| S-3 | Open-source licensing decision |
| B-6 | TCPA/SMS opt-in consent review |
| E-1 | Square Marketplace cert checklist (Syd portion) |
| W-2 | "Caught Steve" marketing content review |

**Contingency:** If Syd is out past Mar 3, R-6 gets temporary risk acceptance. Only R-6 is a shipping blocker.

---

## PARKED — Jeffe Action Items

| Item | Description |
|------|-------------|
| Confirm Tom Hoover's school (Ohio U vs Ohio State) | Biographical disambiguation |
| Scan handwritten North Stars materials | Physical artifacts from Tom Murnane, Herb Kleinberger, Diane Ellis |
| Scan Management Horizons conference book | ~1995-96 foundational retail strategy |
| Verify Dan Lyle / Nike Audit Committee via SEC EDGAR | Factual verification before external use |

---

## Timeline (Eva's Honest Estimate — updated Feb 23)

| Milestone | Target | Notes |
|-----------|--------|-------|
| Sprint 5 AutoBuild completes | Feb 23 | Qwen running now |
| Phase 2 Schema on iMac | Feb 24–25 | Alembic is the biggest risk |
| Phase 3 Data flows E2E | Feb 26–27 | Parser mismatches expected |
| Phase 4 Tests triaged | Feb 28–Mar 3 | 8 SP buffer for unknowns |
| Phase 5 Clickthrough | Mar 3–5 | Jim + Jeffe on iMac |
| R-1 Blueprint sign-off | Feb 28 | PhD + Tom + Jeremy |
| **Alpha 3X Gate (R-15)** | **Mar 7–14** | **Both Sprint 5 + R-1 must be green** |
| Companion wireframes (Art) | March | Art unblocked, can start now |
| UAT ready | Mar 14–21 | Jim signs off |

---

## Deprecated Docs (archived, no longer maintained)

| Document | Replaced By |
|----------|-------------|
| `Canary_Attack_Plan_2026-02-17_v1.0.md` (v2.0) | This document (v3.0) |
| `Alpha3X_Replan_Sprint3_to_UAT_2026-02-22.md` | Sprint 5 Plan + this document |

---

---

*"Ship daily means ship something that runs, not something that compiles."* — Eva

*Canary LP | Confidential*
