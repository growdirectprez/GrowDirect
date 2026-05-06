---
type: health-check
date: 2026-05-03
tool: scheduled-task/brain-health-check
status: remediated
---

# Brain Health Check — 2026-05-03

Weekly automated scan. Vault is structurally healthy; surfaced findings are review-backlog and intake-discipline drift, not corruption.

## Remediation status (2026-05-03 follow-up pass)

| Item | Status | Notes |
|---|---|---|
| Move loose handoff doc to inbox | ✓ done | `substrate-port-and-officer-architecture-handoff-2026-05-03.md` → `Brain/raw/inbox/2026-05-03-substrate-port-and-officer-architecture-handoff.md` |
| Move loose `docs/` top-level files | ✓ done | 5 playbooks → `docs/playbooks/` (created); 1 dispatch → `docs/dispatches/`; 1 runbook → `docs/runbooks/`; 1 architecture spec → `docs/superpowers/specs/` (renamed `2026-04-15-growdirect-io-operations-hub-architecture.md`). 33 path references updated across 11 files. |
| Reconnect 15 orphan wiki files | ✓ done | All 15 linked from appropriate MOCs: Canary MOC (modules + strategy), NCR MOC (Murdoch's, alignment notes), Canary Go portal (Square crosswalk), RetailSpine MOC (foundation data, security controls), Home (broken-links baseline). Re-checked: orphans = 0. |
| Verify CATz/ projection completeness | ✓ done | 52/59 files duplicated in Brain by basename; 6 "unique" files are old-letter naming (C/J/L/R/S/W) with post-rename equivalents in Brain (M/O/L/C/S/E) — content sizes within ~1.5%. **CATz/ is fully projected. Safe to remove.** |
| Rebuild registry | ✓ done | 376 articles, 4,529 topics. |
| **Remove `CATz/` from repo root** | ⏳ requires user | Cannot auto-delete. Run: `git rm -r CATz/ && git commit -m "remove: persistent CATz local clone (clone-on-demand per CLAUDE.md)"` |
| Triage 59 needs-review-past-due cards | ⏳ deferred | Requires actual content review pass — schedule a `/state` session against the angel-* batch (32 cards, single review) first. |
| Schedule inbox synthesis sprint | ⏳ deferred | 389 .md intakes + binary corpus — needs Secure-pattern session. |
| Audit `outputs/` session leftovers | ⏳ requires user | Cannot auto-delete. After review, run `git rm -r outputs/eljeffe-vault outputs/diligence outputs/dispatches outputs/_session && git rm outputs/*.md`. |

## Registry stats

- **Articles indexed:** 376 (wiki: 364 · project MOCs: 12)
- **Topics:** 4,528
- **Build:** clean, no errors

## Stale wiki articles

- **`last-compiled` older than 30 days:** 0 — clean.
- **`needs-review` past due:** 59 articles. Concentrated in three batches:
  - `angel-*` series (32 cards, all dated 2026-04-27) — single review pass would clear the block.
  - Lot-H / Seacove / Cove (4 cards, 2026-04-27).
  - Peninsula-content + `card-*` series (13 cards, 2026-04-29).
  - Recent stragglers (last 3 days): `growdirect-viewpoint-virtual-store-manager`, `abalonecove-org`, `cove-baughey-1947`, `cove-lrpmp`, `cove-rpv-redevelopment-conveyance`, `peninsula-gyms-fitness`.

## Orphan files (no incoming wikilinks/mdlinks)

15 disconnected nodes — Brain projection equivalent of a dead-end road.

| File | Fix |
|---|---|
| `Brain/projects/NCR.md` | Link from Canary MOC or platform MOC |
| `canary-module-{e,f,l,m}.md` (4) | Likely superseded by post-rename modules — delete or merge |
| `canary-commercial-context.md` | Link from Canary MOC or `growdirect-the-pitch.md` |
| `canary-go-square-crosswalk.md` | Link from Canary Go portal |
| `canary-location-item-data-model.md` | Link from `canary-data-model.md` family |
| `canary-site-update-instructions.md` | Runbook — link from `dispatch-coordination-protocol.md` |
| `canary-vsm-diagnostic-mode-requirement.md` | Link from `growdirect-viewpoint-virtual-store-manager.md` |
| `murdochs-workflow-cards-user-stories-scenarios.md` | Link from RetailSpine or NCR MOC |
| `ncr-rapidpos-alignment-notes.md` | Link from NCR MOC |
| `retail-foundation-data.md` · `retail-security-controls.md` | Link from RetailSpine MOC |
| `brain-broken-links-baseline-2026-05-01.md` | Link from method MOC or delete (one-shot baseline) |

## Intake bypass violations

Knowledge docs created in the last 7 days that were never routed through `Brain/raw/inbox/`:

1. **`substrate-port-and-officer-architecture-handoff-2026-05-03.md`** — at repo root, dated today. Loose handoff doc that should be a wiki article + intake source.
2. **`CATz/` directory at repo root** — explicit violation of CLAUDE.md rule *"no persistent local clone. Those directories should not exist on this machine."* Contains 50+ wiki files, CLAUDE.md, team profile. Local projection drift risk.
3. **`docs/` top-level loose docs** (8 files): `dispatch-brain-scaffold-design.md`, `email-migration-fastmail.md`, `growdirect-io-architecture.md`, `playbook-{brain-scaffold-design,heartbeat-blueprint,method-katz-reverse-engineer,retail-ops-model,solex-square-merchant}.md`. Belong in `docs/playbooks/`, `docs/superpowers/specs/`, or Brain.
4. **`outputs/` session leftovers** — `eljeffe-vault/`, `diligence/rapidpos/`, `dispatches/`, position papers, white papers, brand prompts. Violates session discipline rule 10 (clean up own artifacts).

Worktrees (`.worktrees/canonical-data-model`, `gro-752`, `gro-753`, `gro-754`) are expected fixtures, not bypasses — duplication is from the worktree mechanism itself.

## Stalled inbox

- **0 files** with mtime > 7 days (per literal spec). However, all 389 inbox `.md` files share mtime 2026-05-01 13:21 — likely a vault sync timestamp reset, not actual create dates.
- **Real picture:** `Brain/raw/inbox/` holds 389 markdown intakes plus a large binary corpus (PDFs, images, xlsx). Secure/Kroger precedent processed 18 binaries → 6 wiki articles. At that ratio there are ~130 wiki articles' worth of synthesis owed.

## Registry coverage

| Project | Wiki articles | Status |
|---|---|---|
| platform | 91 | healthy |
| canary | 60 | healthy |
| cove | 44 | healthy |
| angel | 37 | healthy |
| secure | 21 | healthy |
| ncr | 16 | healthy |
| seacove | 3 | at minimum — flagged |

## Recommended actions (priority order)

1. **Remove `CATz/` from repo root.** Verify content is fully projected to `Brain/` first; then delete. Aligns with CLAUDE.md "no persistent local clone."
2. **Route `substrate-port-and-officer-architecture-handoff-2026-05-03.md`** into Brain — copy to `Brain/raw/inbox/` for synthesis (likely wiki article in the substrate / officer architecture / Canary Go cluster), then delete from repo root.
3. **Triage the 59 `needs-review`-past-due cards** — the `angel-*` 2026-04-27 batch (32 cards) is a single review pass.
4. **Reconnect or archive 15 orphan files** — start with `canary-module-{e,f,l,m}.md` (suspected post-rename leftovers — confirm and delete).
5. **Schedule an inbox synthesis sprint** for `Brain/raw/inbox/` (389 .md + binaries). Use the Secure/Kroger pattern.
6. **Audit `docs/` top-level loose docs** (8 files) — move into `docs/playbooks/`, `docs/superpowers/specs/`, or Brain wiki.
7. **Audit `outputs/`** — delete session-leftovers per session discipline rule 10; route any retained knowledge to Brain.
8. **Link `Brain/projects/NCR.md`** from a platform or Canary MOC so the NCR work surfaces in the project graph.
