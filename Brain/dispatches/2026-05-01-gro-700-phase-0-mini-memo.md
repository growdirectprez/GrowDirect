---
date: 2026-05-01
type: dispatch
dispatch: GRO-700
phase: 0
project: gcp-native-rebuild
status: ready-for-review
companion: 2026-05-01-gro-700-phase-0-recovery-memo.md
gates: phase-1-wipe-blocked-on-founder-confirmation
---

# Mini-side recovery memo — GRO-700 Phase 0

**Thesis:** the mini is in better shape than expected. Working tree differs from `origin/main` by exactly one line (a `ownpalosverdes` deletion), the intake inbox is fully committed (1,654 tracked / 0 untracked), and 95 % of state is recoverable from GitHub. Five concrete items must be captured before wipe: the SSH key (`id_ed25519`), six `.env` files holding the Docker stack credentials, one local-only branch tip, two untracked working-tree items, and the memory bus / Postgres Docker volumes if any data on them isn't already mirrored to GCP. Production Canary stack has been running 5 days — a graceful tear-down decision is needed before wipe.

---

## 1. Mini state at a glance

| Item | Detail | Risk |
|------|--------|------|
| Hostname | `Geoffs-Mac-mini.local` (Darwin 25.3.0, arm64) | — |
| User | `gclyle` | — |
| `~/GrowDirect` branch | **`mini/dispatch-mini13-sdd-cleanup`** (local-only — not on origin) | Branch tip recoverable from origin/main; only 1 line of working-tree drift |
| Working-tree diff vs `origin/main` | 1 line: `ownpalosverdes` deleted | Negligible — confirm intentional, then commit/discard |
| Untracked in `~/GrowDirect` | `Canary-Retail-Brain/` (committed git clone of `growdirect-llc/canary-retail-brain`, 0 dirty), `devops/.env` (real shared-stack credentials) | `.env` is at risk; `Canary-Retail-Brain/` is a CLAUDE.md "no persistent clone" violation — safe to delete |
| Brain/raw/inbox/ | 1,654 tracked files, 0 untracked, 755 MB | Safe — already in GitHub |
| Disk usage | `~/GrowDirect` = 4.4 GB · root partition = 12 GB used / 124 GB free / 9 % | — |
| Sibling repos | `~/GrowDirect-archive-2026-04-25` (847 MB snapshot of Canary/Cove/devops from 2026-04-25) — historical | Optional preserve; redundant with git history |

## 2. Safe — already in GitHub

- All committed history on every branch
- All inbox content (tracked, mirrored to `growdirectprez/GrowDirect`)
- The `Canary-Retail-Brain/` clone is fully in sync with `growdirect-llc/canary-retail-brain`

## 3. At risk — must capture before wipe

| Item | Path | Action |
|------|------|--------|
| **`mini/dispatch-mini13-sdd-cleanup` branch tip** | local-only branch on mini | If `ownpalosverdes` deletion was intentional → commit + push to origin (and pull on laptop). If accidental → restore. Decision needed. |
| **`devops/.env` (untracked)** | `~/GrowDirect/devops/.env` | Holds shared-infra credentials (Postgres, Valkey, Ollama, pgAdmin). Must be backed up to 1Password. Will be regenerated for GCP, so consider whether values are even worth preserving. |
| **`Canary/devops/.env` and `.env.qa`** | `~/GrowDirect/Canary/devops/` | Canary Docker stack credentials (separate prod/QA databases). Back up to 1Password. |
| **`Canary/.env` and `.env.test`** | `~/GrowDirect/Canary/` | Flask app config. Back up to 1Password. |
| **`Cove/devops/.env`** | `~/GrowDirect/Cove/devops/` | Cove Docker stack credentials. Back up to 1Password. |
| **`~/.ssh/id_ed25519`** | mini's SSH identity | This is what mini uses to git push and SSH out. **Back up to 1Password before wipe.** Replaceable but means rotating any service that pins the public key. |
| **`~/.docker/config.json`** | mini Docker registry auth | Re-auth post-wipe; no preservation needed |

## 4. Docker stack — graceful tear-down decision

Stack has been running 5 days with these containers:

| Container | Status | Notes |
|-----------|--------|-------|
| `canary_prod_flask` | Up 5 days (healthy) | **Production Canary Flask app** |
| `canary_prod_tsp_sub1-4` | Up 5 days (healthy) | **Production TSP subscribers** |
| `canary_qa_app` | Up 5 days (healthy) | QA Canary app |
| `canary_qa_tsp_sub1-4` | Up 5 days (**unhealthy**) | QA subscribers — 5-day stale unhealth state |
| `devops-cove-web-1` | Up 5 days | Cove Flask app |
| `devops-cove-db-1` | Up 5 days (healthy) | Cove Postgres |
| `growdirect_postgres` | Up 5 days (healthy) | Shared Postgres (canary, cove, growdirect_memory) |
| `growdirect_valkey` | Up 5 days (healthy) | Shared cache/sessions |
| `growdirect_ollama` | Up 5 days (healthy) | Embeddings |

**Memory bus container is NOT in this list — http_code 000 on the health probe.** This contradicts the `gcp-foundation-runbook` and CLAUDE.md "Mini Docker Gate" assumptions. Either it was stopped manually, never restarted after a previous reboot, or has been broken for some time. Worth a short investigation before wipe (might point to a config issue worth knowing about for the GCP rebuild).

**Volumes worth evaluating:**

| Volume | Holds | Phase 1 disposition |
|--------|-------|---------------------|
| `growdirect_pgdata` | Shared Postgres — **canary**, **cove**, **growdirect_memory** databases | Memory bus is reseeded fresh on Cloud SQL (Phase 5). Canary/Cove production data → migrate or abandon? **Founder decision.** |
| `canary_qa_pg_data` | QA Canary Postgres | Throwaway — QA gets rebuilt on Cloud SQL `-staging` |
| `devops_cove_pgdata` | Cove Postgres (separate from shared `growdirect_postgres`) | Confirm which is the real Cove DB — duplicates or hand-off? |
| `growdirect_valkey_data` | Sessions, cache, task queue | Throwaway |
| `growdirect_ollama_data` | Embedding models (`qwen3-embedding:8b`) | Throwaway — Vertex AI text-embedding-005 in Phase 8 |
| `canary_qa_valkey_data` / `canary_qa_pgadmin_data` | QA helpers | Throwaway |
| `f33533ad8117...` (unnamed UUID) | Unknown | Investigate before wipe |

**Recommended graceful tear-down sequence (when Phase 1 is greenlit):**

1. Confirm production Canary stack has zero live customer load (it shouldn't, per the platform-thesis "first merchant onboarding is Phase 10")
2. `pg_dump` `growdirect_postgres` → `~/canary_prod_pgdump_2026-05-01.sql` → upload to GCS bucket
3. `pg_dump` `devops-cove-db-1` → `~/cove_pgdump_2026-05-01.sql` → upload to GCS bucket
4. `docker compose down` on each stack
5. `docker volume ls` post-shutdown — confirm volumes still present, do not prune
6. Then proceed to OS wipe

## 5. Branches — hygiene cleanup opportunity

Mini has these local branches (the `*` is current):

```
  gclyle/gro-549-solex-c2-productionize-scenario-runner-ux
  gclyle/gro-551-mini-self-review-and-hardening
  gclyle/gro-555-mini-operational-maintenance-pass
  main
  mini/dispatch-gro-557-rapidpos-dev-env
  mini/dispatch-gro-558-delivery-spec
* mini/dispatch-mini13-sdd-cleanup       ← LOCAL-ONLY
```

All except `mini/dispatch-mini13-sdd-cleanup` are mirrored on origin. The local-only one differs from `origin/main` by 1 line. **No real branch divergence to recover** — these are throwaway working branches.

Post-Phase-1, the new mini will start clean from `growdirectprez/main`. The branch list resets to just `main`.

## 6. Snapshots / archives on mini (optional preservation)

| Path | Size | What | Decision |
|------|------|------|----------|
| `~/GrowDirect-archive-2026-04-25` | 847 MB | Snapshot of `Canary/`, `Cove/`, `devops/` from 2026-04-25 | Already redundant with git history at SHA from that date — **safe to skip** unless founder wants the working-tree state preserved separately |

## 7. Memory bus reset implication (cross-reference)

CLAUDE.md mandates: *"Mini Hard Rule: Docker must be up before any dispatch work begins. No Docker, no ALX."* And: *"Step 3 must return a response. If it does not, the memory bus is down — diagnose before proceeding."*

The mini is currently in a state that violates this rule (Docker is up, memory bus is not). Two options:

- **(a)** Fix the memory bus on the mini before wipe — for continuity until Phase 5 brings it up on Cloud SQL pgvector
- **(b)** Accept that the mini is in degraded mode for the next ~5-10 working days and skip the fix; rebuild the memory bus directly on GCP

Recommendation: **(b)** — fixing it just to throw it away is wasted work. Update CLAUDE.md to relax the Mini Hard Rule for the duration of GRO-700 execution.

## 8. Pre-wipe action checklist (mini side)

```
[ ] decide ownpalosverdes deletion: commit + push to origin/main, or restore
[ ] back up all .env files to 1Password:
    devops/.env, Canary/devops/.env, Canary/devops/.env.qa,
    Canary/.env, Canary/.env.test, Cove/devops/.env
[ ] back up ~/.ssh/id_ed25519 to 1Password
[ ] decide Canary-Retail-Brain/ untracked dir: delete (per "no persistent clone" rule)
[ ] decide growdirect_pgdata fate: pg_dump to GCS, or abandon
[ ] decide devops_cove_pgdata fate: pg_dump to GCS, or abandon
[ ] confirm no live customer load on canary_prod_* (sanity check)
[ ] graceful docker compose down on all stacks (preserve volumes until OS wipe)
[ ] decide ~/GrowDirect-archive-2026-04-25 (847 MB): keep or discard
[ ] founder reviews this memo + laptop memo, signs off Phase 1
```

## 9. What this memo is NOT

- Not the OS wipe checklist (that's Phase 1, written separately when sign-off lands)
- Not a Cloud SQL migration plan (that's Phase 5)
- Not a recommendation on whether to migrate prod data — that's a founder decision

## 10. Acceptance — Mini Phase 0 closes when

1. This memo + laptop memo are reviewed and signed off
2. Every line item in §8 is checked off
3. Founder issues explicit "go" for Phase 1

---

**Linear:** [GRO-700](https://linear.app/growdirect/issue/GRO-700/wipe-and-rebuild-mini-as-gcp-native-dev-workstation)
**Author:** ALX (laptop session, ran via SSH against `mini`, 2026-05-01)
**Companion:** `Brain/dispatches/2026-05-01-gro-700-phase-0-recovery-memo.md` (laptop side)
