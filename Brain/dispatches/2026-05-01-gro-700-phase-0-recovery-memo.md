---
date: 2026-05-01
type: dispatch
dispatch: GRO-700
phase: 0
project: gcp-native-rebuild
status: ready-for-review
gates: phase-1-wipe-blocked-on-founder-confirmation
---

# Recovery memo — GRO-700 Phase 0 (audit + pre-wipe gate)

**Thesis:** the laptop is mostly safe — origin/main is the source of truth and 95 % of working state is already pushed. Three concrete artifacts will be lost on wipe unless captured now: an unpushed branch tip, a Cloudflare token at the repo root, and a 464-file intake working set in `Brain/raw/inbox/`. The mini is a separate, larger inventory job that cannot be done from this laptop. **Phase 1 (wipe) does not start until founder confirms that the items in §6 are captured.**

---

## 1. Laptop state at a glance

| Repo | Path | Branch | Ahead | Uncommitted | Untracked | Status |
|------|------|--------|-------|-------------|-----------|--------|
| **GrowDirect** (factory) | `~/GrowDirect` | main | **2** | 5 modified | ~470 (incl. 464 in `Brain/raw/inbox/`) | At risk — see §3, §4 |
| GrowDirect-CATz | `~/GrowDirect-CATz` | main | 0 | 0 | 1 (`_site/` build) | Safe to delete; CLAUDE.md "no persistent clone" |
| GrowDirect-CRB | `~/GrowDirect-CRB` | main | 0 | 0 | 1 (`_site/` build) | Safe to delete; CLAUDE.md "no persistent clone" |
| GrowDirect-NCR | `~/GrowDirect-NCR` | main | 0 | 0 | 2 (`.obsidian/`, `canary-data-model.md`) | **Real content not on remote — capture before wipe** |
| abalonecove | `~/abalonecove` | main | 0 | 0 | 0 | Clean ✓ |
| canary-site | `~/canary-site` | main | 0 | 0 | 0 | Clean ✓ |
| growdirectprez.github.io | `~/growdirectprez.github.io` | main | 0 | 0 | 2 (`growdirect-leaf.png`, `.svg`) | **Untracked design assets — capture or commit** |
| Angel | `~/Angel` | — | — | — | — | Empty shell, not a git repo — verify with founder |

## 2. Safe — already in GitHub (no action needed)

- All committed history on `main` for every repo above (HEAD on remotes)
- Brain/wiki/, docs/sdds/, code under Canary/, CanaryGo/, Cove/, Seacove/ as committed
- `~/abalonecove`, `~/canary-site` working trees are clean

## 3. At risk — laptop ~/GrowDirect

| Item | Detail | Action |
|------|--------|--------|
| **2 unpushed commits on main** | `34c1ea2` GCP foundation runbook · `2f01a3b` workspace-admin-runbook (GRO-719) | `git push origin main` before wipe |
| **5 modified, uncommitted files** | `Brain/REGISTRY.json` (+10,731 lines — registry rebuild from inbox), `Brain/wiki/agent-card-format.md`, `Brain/wiki/canary-go-portal.md`, `Seacove/arc/cli.py` (+83 lines real code), `docs/sdds/go-handoff/go-module-layout.md` | Commit or stash + push; `Seacove/arc/cli.py` is real code, do not discard |
| **`CF_DASH_Token.rtf` at repo root** | 620 bytes, untracked, dated 2026-04-27 — Cloudflare dashboard token | **Move to 1Password (or `private/`) before wipe.** Should never have been at repo root per CLAUDE.md "no loose files" rule. |
| **`store-ops-prototype.html` at repo root** | Untracked HTML scratch | Decide: commit, archive, or discard. Currently violates "no loose files" |
| **`Brain/raw/inbox/` — 464 untracked files** | Active intake queue (.ppt, .docx, .pdf, .md extracts), incl. `_queue.md` (29 KB, modified 2026-05-01 06:21) | These are gitignored binaries + intake markdown. Either: (a) push the markdown extracts via `engine.py ingest` + commit, then archive binaries to a backup volume; or (b) tar the entire `Brain/raw/inbox/` tree to external/cloud storage before wipe. **Do not lose `_queue.md`** — it's the synthesis state. |

## 4. At risk — sibling repos

| Item | Where | Action |
|------|-------|--------|
| `canary-data-model.md` (NCR vault) | `~/GrowDirect-NCR/` untracked | Commit + push to `growdirect-llc/ncr` before wipe (or move to GrowDirect/Brain/ if it belongs there) |
| `growdirect-leaf.png` + `.svg` | `~/growdirectprez.github.io/` untracked | Commit + push, or archive design assets |
| `~/GrowDirect-CATz`, `-CRB`, `-NCR` persistent clones | All three | Per CLAUDE.md "External Vaults" rule, these should NOT exist persistently. Will not be re-cloned post-wipe — fresh transient `gh repo clone /tmp/...` becomes the new pattern. |

## 5. At risk — user-level credentials and config

| Path | Holds | Action |
|------|-------|--------|
| `~/.ssh/` | `id_canary` private key, `authorized_keys`, `config`, `known_hosts` | **Backup to 1Password or hardware token before wipe.** Replaceable but inconvenient. |
| `~/.config/gh/hosts.yml` | GitHub CLI auth tokens | Re-auth after wipe via `gh auth login` (no backup needed) |
| `~/.docker/config.json` | Docker Hub / registry auth | Re-auth after wipe |
| `~/.claude/` | Claude Code sessions, settings, scheduled tasks, history | Sessions and history are nice-to-have; `settings.json` and any project-scoped configs in `.claude/` should be checked for local-only customizations |
| `~/.config/gcloud/` | (empty — gcloud not yet installed on laptop) | No action — Phase 2 sets this up fresh |

## 6. Mini-side known unknowns (cannot inventory from laptop)

The dispatch title is "wipe and rebuild **mini**" — but the audit so far is laptop-only. The mini hosts state that this laptop cannot see:

- The mini's `~/GrowDirect` checkout — **uncommitted state unknown**
- Docker stack persistent volumes: Postgres data, Valkey state, Ollama models, **memory bus seed** (385+ embeddings)
- Mini-resident `~/.ssh/`, `~/.config/gcloud/`, `~/.docker/`
- Anything dropped onto the mini that was never pushed (intake binaries, scratch dirs, `.env` files)
- Mini-side `~/GrowDirect/Canary/.env`, `Cove/.env`, etc. — likely diverge from laptop versions

**Recommended:** before any wipe, run an equivalent Phase 0 audit on the mini itself (SSH or directly), produce a parallel mini-side memo, then merge findings. The memory bus is rebuilt fresh by `seed_standalone.py` post-Phase 5, so its volume is throwaway — but uncommitted code or intake material on the mini is not.

## 7. Project-ID discrepancy (decide before Phase 2)

Two competing project layouts in current docs:

| Source | Date | Layout |
|--------|------|--------|
| `Brain/wiki/cards/gcp-foundation-runbook.md` (committed `34c1ea2`) | 2026-05-01 | Single project: `canary-rapidpos` (billing linked, 6 APIs enabled, `canary-deploy` SA created) |
| GRO-700 description | 2026-04-29 | Three projects: `growdirect-canary-prod`, `-staging`, `-dev` |

The runbook reflects what was actually built. GRO-700 was authored two days earlier. **Founder decision needed:** treat `canary-rapidpos` as `-prod` (and add `-staging`/`-dev` later) or rename/restructure now. Recommendation: keep `canary-rapidpos` as the staging/sandbox project, create `growdirect-canary-prod` clean for production load, defer `-dev` until Cloud Workstations is up. No rebuild required, additive only.

## 8. Pre-wipe action checklist (Phase 0 → Phase 1 gate)

```
[ ] git -C ~/GrowDirect push origin main                         (push the 2 unpushed commits)
[ ] decide: commit, stash, or discard the 5 modified files       (especially Seacove/arc/cli.py — real code)
[ ] move CF_DASH_Token.rtf → 1Password, delete from repo
[ ] decide store-ops-prototype.html: commit, archive, or discard
[ ] tar -czf ~/Desktop/brain-raw-inbox-2026-05-01.tar.gz ~/GrowDirect/Brain/raw/inbox/
    OR ingest then archive — do not lose _queue.md
[ ] git -C ~/GrowDirect-NCR add canary-data-model.md && commit && push
[ ] git -C ~/growdirectprez.github.io add growdirect-leaf.* && commit && push
[ ] backup ~/.ssh/ to 1Password (id_canary key + config)
[ ] run equivalent audit on the mini, produce mini-side memo
[ ] founder reviews this memo + mini memo, signs off on Phase 1
```

## 9. What this memo is NOT

- Not a wipe checklist for the mini OS reinstall (that's part of Phase 1, written separately when sign-off lands)
- Not a project-restructure plan (that belongs in Phase 2 alongside the project-ID decision)
- Not the Cloud Workstations spec (Phase 3, separate)

## 10. Acceptance — Phase 0 closes when

1. This memo is reviewed and signed off by founder
2. Mini-side parallel audit memo is filed alongside this one
3. Every line item in §8 is checked off
4. Founder issues explicit "go" for Phase 1

---

**Linear:** [GRO-700](https://linear.app/growdirect/issue/GRO-700/wipe-and-rebuild-mini-as-gcp-native-dev-workstation)
**Author:** ALX (laptop session, 2026-05-01)
**Next dispatch artifact:** mini-side audit memo (ALXjr, on the mini)
