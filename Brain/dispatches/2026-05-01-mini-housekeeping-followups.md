---
date: 2026-05-01
type: dispatch
parent: GRO-700
status: founder-action-pending
gates: 1Password
---

# Mini-side housekeeping — pending founder action

GRO-700 v3 closed today; the mini's Docker stack was parked (15 containers stopped, 8 volumes preserved). The mini is now in a dormant dev-workstation state. Two categories of housekeeping remain. Neither blocks anything; both are best done at founder's convenience because they require 1Password access (agent-side cannot perform).

## 1Password backups

The following items live only on the mini (or only on the laptop, for the last one) and would be inconvenient to lose:

| Item | Location | What it is | Replaceable? |
|------|----------|------------|--------------|
| `~/.ssh/id_ed25519` | mini | Mini's SSH identity (used for `git push` from mini and incoming `ssh mini` from laptop) | Yes, but means rotating any service that pins the public key |
| `devops/.env` | mini `~/GrowDirect/devops/` | Shared-stack credentials (Postgres, Valkey, Ollama, pgAdmin) for the now-parked Docker stack | Yes — values are throwaway since the stack is parked, but founder may want them archived |
| `Canary/devops/.env` + `.env.qa` | mini `~/GrowDirect/Canary/devops/` | Canary prod + QA Docker stack credentials | Yes — Canary Python is frozen anyway |
| `Canary/.env` + `.env.test` | mini `~/GrowDirect/Canary/` | Canary Flask app config | Yes |
| `Cove/devops/.env` | mini `~/GrowDirect/Cove/devops/` | Cove Docker stack credentials | Yes |
| **`CF_DASH_Token.rtf`** | **laptop `~/GrowDirect/` ROOT** | Cloudflare dashboard token, untracked, sitting at repo root | High-value — move to 1Password and DELETE from repo root |

The Cloudflare token is the most urgent because it's a credential at the repo root (untracked, but easy to accidentally `git add -A`). The `.env` files are lower urgency.

## Volume disposition decision (also founder-deferred)

Per the GRO-700 v3 mini memo §8, the parked Docker volumes hold:

- `growdirect_pgdata` — canary + cove + growdirect_memory databases
- `devops_cove_pgdata` — separate Cove DB
- `canary_qa_pg_data`, `canary_qa_pgadmin_data`, `canary_qa_valkey_data` — QA helpers
- `growdirect_valkey_data`, `growdirect_ollama_data` — shared infra dev state
- `f33533ad8117b681b04dc52cb4632d1fa4e691068345b52e65181e40a2e002a2` — unidentified UUID volume

**Decision pending:** for each volume, `pg_dump` to GCS for archival, or abandon. Default if no decision: leave them on the mini disk (they're not consuming compute, just disk — 9% disk usage on the mini, plenty of headroom).

## Recommended sequence (whenever convenient)

1. Move `CF_DASH_Token.rtf` → 1Password, delete from `~/GrowDirect/`
2. Backup `~/.ssh/id_ed25519` → 1Password (mini SSH key)
3. Optional: backup the 5 `.env` files to 1Password (only valuable if founder wants the historical secret values for any reason)
4. Decide volume fate when in the mood

## What's been done

- 27 stale Linear tickets cancelled (GRO-558, 568-579, 563-567, 326, 516, 519, 554, 556, 599, 629, 665, 669)
- 14 compliance tickets cancelled (GRO-686-699, with a small hygiene successor at GRO-720)
- Mini Docker stack parked (15 containers stopped, volumes preserved)
- Mini git state cleaned up (local-only branch deleted, persistent vault clone removed, on `main` synced with origin)
- ALXjr identity sunset (`Brain/wiki/cards/agent-alxjr-decision.md` status: approved)
- GRO-700 v3 → Done (drop zone CI/CD pipeline live, Cloud SQL + pgvector verified)

## Linear

The mini-side memo at `Brain/dispatches/2026-05-01-gro-700-phase-0-mini-memo.md` §8 has the original pre-wipe checklist. With the wipe deferred indefinitely, that checklist's items are reframed as the housekeeping above — same items, different urgency.
