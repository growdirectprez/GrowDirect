---
date: 2026-04-24
type: runbook
classification: confidential
owner: GrowDirect LLC
phase: G3-G5 critical workstream
audience: founder
---

# Secret Rotation + History Rewrite Runbook

## Why this runbook exists

Phase G2 security audit surfaced **four committed secrets in HEAD** plus
one HIGH that touches existing archive content. Spec success criterion
SC10 mandates these be **rotated AND purged from history** before
partner access — "documented" is not sufficient.

This runbook is the ordered procedure. Founder executes the rotations
(only the founder has access to the issuing services); the history
rewrite is a single-shot operation against the GrowDirect repo.

**Schedule-critical path.** The full workstream is ~2–4 hours of careful
work plus a force-push that affects every open branch and worktree. If
it slips, the 2026-04-28 partner window slips.

---

## Pre-flight (5 min)

- [ ] **P0. Confirm no in-flight pushes from other workspaces.** Force-push
      will rewrite shared history. If another laptop / CI runner / agent
      pushes between rotation and rewrite, work gets lost.
- [ ] **P1. Snapshot current state.** `git -C /Users/gclyle/GrowDirect tag pre-secret-rewrite-2026-04-24` — pre-rewrite rollback anchor.
- [ ] **P2. Take a clone-as-backup.** `git clone --mirror /Users/gclyle/GrowDirect ~/GrowDirect-backup-2026-04-24.git` — full history including refs, in case a refspec needs recovery.
- [ ] **P3. Verify `git filter-repo` is installed.** `which git-filter-repo` (preferred over BFG — keeps signatures clean and is more flexible). Install via `brew install git-filter-repo` if missing.

---

## Track 1 — Rotate at issuing services (founder, in any order)

Each secret stays valid until you rotate. The historical commit content
is NOT purged in this track — that happens in Track 2. The rotation in
this track makes the leaked credential useless before the leak is
purged from history.

### S1 — Firecrawl API key (`fc-fec9…8821e`)

Location in code: `.mcp.json:8` in HEAD. Untracked in cleanup branch
(committed `git rm --cached` in `b8beb48`); still present in history.

- [ ] **S1.1** Log into Firecrawl → API Keys → revoke `fc-fec9…8821e`.
- [ ] **S1.2** Create a new key. Copy the new value.
- [ ] **S1.3** Update local `.mcp.json` (now gitignored) with the new value:
      ```bash
      # Edit .mcp.json line 8 with the new key
      ```
- [ ] **S1.4** Restart any MCP-enabled processes that read `.mcp.json` (Claude Code, etc.).
- [ ] **S1.5** Verify the new key works: trigger a Firecrawl call from any MCP-enabled session.
- [ ] **S1.6** Confirm the old key returns 401 / no-auth: `curl -H "Authorization: Bearer fc-fec9…8821e" https://api.firecrawl.dev/...` should fail.

### S2 — Obsidian REST API key (`75a1…2d5b`)

Location in code: `.mcp.json:17` in HEAD. Same untrack-in-cleanup status
as S1.

- [ ] **S2.1** Open Obsidian → Settings → Community Plugins → Local REST API → Settings → API Key → "Generate New Key" (revokes the old one).
- [ ] **S2.2** Copy the new key.
- [ ] **S2.3** Update local `.mcp.json` with the new value.
- [ ] **S2.4** Restart any process that reads `.mcp.json`.
- [ ] **S2.5** Verify the new key works: `curl -H "Authorization: Bearer <new-key>" https://localhost:27124/` returns 200.

### S3 — GitHub PAT (`ghp_2FwZ…AAX`)

Location in code: `docs/_archive/ip-vault/timelogs/2026/02-February/daily/2026-02-25.md:383`. The annotation says "rotate after demo week" — the rotation may already have happened.

- [ ] **S3.1** Verify the leaked PAT is still active: `curl -H "Authorization: token ghp_2FwZ…AAX" https://api.github.com/user`. If 401, it's already rotated — skip to S3.4.
- [ ] **S3.2** If active: GitHub → Settings → Developer Settings → Personal Access Tokens → revoke `ghp_2FwZ…AAX`.
- [ ] **S3.3** Generate a replacement if any local script depends on the old PAT (check shell history for `GITHUB_TOKEN=ghp_2FwZ…`).
- [ ] **S3.4** Document disposition in this runbook (rotated / was-already-rotated).

### S4 — `CANARY_ENCRYPTION_KEY` Fernet (`BHDJWBeEEtNrcqq…`)

Locations: `docs/sdds/canary/architecture.md:517` (in this repo) +
`docs/_archive/plans/2026-03-26-…md` + Canary repo S-8/S-9 references
(per security audit). Coordinate single rotation across both repos.

- [ ] **S4.1** Verify what this key encrypts in the Canary deployment. `grep -rn "CANARY_ENCRYPTION_KEY" /Users/gclyle/GrowDirect/Canary/canary/ 2>&1 | head -10`.
- [ ] **S4.2** If used in production: this is an **operational rotation**, not just a credential rotation. Plan a re-encryption pass for whatever data the key protects (likely OAuth tokens, session secrets, or PII at rest).
- [ ] **S4.3** Generate a new Fernet key: `python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`.
- [ ] **S4.4** Decrypt-and-re-encrypt any data encrypted under the old key. (Specific to Canary's encryption usage — coordinate with Canary's S-8/S-9 sprint owners.)
- [ ] **S4.5** Update Canary's deployment env var (`.env` on prod host, or whatever secrets manager Canary uses).
- [ ] **S4.6** Roll Canary instances to pick up the new key.
- [ ] **S4.7** Document the disposition in this runbook.

### S5 — Square sandbox token (HIGH, not CRITICAL — H-1 from security audit)

Reachable from `docs/_archive/ip-vault/_archive/dispatches/` and
`_archive/workorders/` — 5 files, 13 leak hits combined. Same token
already remediated as Canary S-3.

- [ ] **S5.1** Confirm Canary already rotated this token: check Canary's S-3 sprint disposition.
- [ ] **S5.2** If still active: Square Developer Dashboard → Sandbox → Personal Access Tokens → rotate.
- [ ] **S5.3** Note: this is a sandbox token; risk is lower than prod credentials but still HIGH per spec.

---

## Track 2 — History rewrite (one shot, after all of Track 1)

Once **all five secrets are rotated and verified dead**, purge them from
git history. This is the destructive step. Do NOT run until founder
confirms Track 1 complete and rollback anchor (P1) is set.

### Strategy

Use `git filter-repo --replace-text` to rewrite content in place — the
files stay; the secret strings get redacted to `***REDACTED***`.
This is non-destructive to non-secret content, and it preserves
authorship, dates, and signatures.

### Steps

- [ ] **R1. Stop all writes to the GrowDirect repo.** No active sessions
      committing. No CI runs. No backup processes.

- [ ] **R2. Author the replacement file.** Create `/tmp/secrets-to-purge.txt`:

```
# Secrets to redact from git history. Format: pattern==>replacement
# Use exact strings; filter-repo treats them as literal.

fc-fec9...REPLACE_WITH_FULL_LEAKED_KEY_FROM_GITLEAKS_REPORT...8821e==>***REDACTED-FIRECRAWL***
75a1...REPLACE_WITH_FULL_LEAKED_KEY...2d5b==>***REDACTED-OBSIDIAN***
ghp_2FwZ...REPLACE_WITH_FULL_LEAKED_PAT...AAX==>***REDACTED-GITHUB-PAT***
BHDJWBeEEtNrcqq...REPLACE_WITH_FULL_LEAKED_FERNET...==>***REDACTED-CANARY-ENCRYPTION-KEY***
EAAAlKhZ...REPLACE_WITH_FULL_LEAKED_SQUARE_TOKEN...==>***REDACTED-SQUARE-SANDBOX***
```

Get the full secret strings from `docs/audit-2026-04-23/security-tool-output/gitleaks.json` — open in an editor, find each finding, copy the full secret value into the patterns above.

- [ ] **R3. Dry-run the rewrite.**

```bash
cd /tmp
git clone --mirror /Users/gclyle/GrowDirect /tmp/gd-rewrite-test.git
cd /tmp/gd-rewrite-test.git
git filter-repo --replace-text /tmp/secrets-to-purge.txt --force
git log --all --oneline -p | grep -E "(fc-fec9|75a1.*2d5b|ghp_2FwZ|BHDJWBeEEtNrcqq|EAAAlKhZ)" | head -5
```

Expected: no output (all secrets redacted). If patterns still appear, they didn't fully match — adjust the patterns.

- [ ] **R4. Apply the rewrite to the actual repo.**

```bash
cd /Users/gclyle/GrowDirect
git filter-repo --replace-text /tmp/secrets-to-purge.txt --force
```

This removes the origin remote (filter-repo behavior). Re-add:
```bash
git remote add origin git@github.com:growdirectprez/GrowDirect.git  # use the actual remote URL
```

- [ ] **R5. Verify post-rewrite state.**

```bash
git log --all --oneline -p | grep -E "(fc-fec9|75a1.*2d5b|ghp_2FwZ|BHDJWBeEEtNrcqq|EAAAlKhZ)"
# Should be empty.

git status
git log --oneline -10  # should look the same with new commit hashes
```

- [ ] **R6. Re-run gitleaks to verify clean.**

```bash
gitleaks detect --source /Users/gclyle/GrowDirect --no-banner
# Should report 0 findings.
```

- [ ] **R7. Force-push to origin.**

⚠️ **This is the destructive remote step.** Once you push, every developer / agent / CI runner with a clone of GrowDirect must re-clone or do a careful `git fetch && git reset --hard origin/<branch>`.

```bash
git push --force-with-lease origin main
git push --force-with-lease origin chore/cto-readiness-audit-2026-04-24
git push --force-with-lease origin chore/cto-readiness-housekeeping  # if still useful
# Push tags:
git push --force origin --tags
```

- [ ] **R8. Notify any collaborators / agents / CI** that history was rewritten and they need to re-clone.

- [ ] **R9. Clean up worktrees.** Worktrees point at old commit hashes. Either remove and re-add, or `git fetch --all` then `git reset --hard <new-hash>` inside each worktree.

---

## Track 3 — Verification (post-rewrite)

- [ ] **V1.** Re-run gitleaks against fresh clone — 0 findings.
- [ ] **V2.** Re-run trufflehog (filesystem + git) against fresh clone — 0 findings for the rotated secrets.
- [ ] **V3.** Verify `.mcp.json` is correctly gitignored: `git check-ignore .mcp.json` should print the path.
- [ ] **V4.** Update `docs/audit-2026-04-23/security.md` with rotation dispositions per finding (rotated, history rewritten, verified dead).
- [ ] **V5.** Commit the rotation-disposition update on `chore/cto-readiness-audit-2026-04-24`.
- [ ] **V6.** Update SC10 status in `docs/audit-2026-04-23/cleanup-report.md` — mark CRITICAL committed-secret findings as RESOLVED with rotation timestamp.

---

## Rollback (if something goes wrong)

If R3-R6 reveal an unexpected issue (replacement broke a non-secret string, history corruption, etc.):

```bash
cd /Users/gclyle/GrowDirect
git reset --hard pre-secret-rewrite-2026-04-24  # the tag from P1
# Or restore from the mirror clone in P2:
# rsync -a ~/GrowDirect-backup-2026-04-24.git/ /Users/gclyle/GrowDirect/.git/
```

Force-push has no clean rollback once it lands on origin — that's why R3 dry-run is mandatory.

---

## Open coordination items

- **Canary repo S4.** The Canary encryption key may also live in Canary's git history. After GrowDirect rewrite, run gitleaks against Canary repo and apply the same pattern there if needed. Coordinate with Canary's S-8/S-9 sprint owners.
- **Force-push timing.** Do not force-push during a partner-access window. Schedule for off-hours of the partner.
- **`.gitignore` enforcement.** `.mcp.json` is now gitignored on this branch but the rule needs to land on `main` to prevent re-commit. Phase G5 merge brings the rule onto main.

---

## Checklist completion gate

Phase G3 cannot close until all four CRITICAL secrets and the HIGH
Square sandbox token have rotation + history-rewrite dispositions
recorded in this runbook. Phase G7 cannot tag `cto-review-ready` until
gitleaks reports 0 findings against a fresh clone.

When all boxes are checked: founder signs off, audit report SC10
field updates from "TRIGGERED" to "RESOLVED", and the rotate-and-
rewrite workstream is closed.

---

*Runbook authored 2026-04-24 from Phase G2 security audit findings
(security.md C-1, C-2, C-3, C-4 + H-1). Spec authority: SC10 in
docs/superpowers/specs/2026-04-23-cto-readiness-audit-design.md.*
