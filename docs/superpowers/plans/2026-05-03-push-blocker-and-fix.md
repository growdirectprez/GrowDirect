# Push blocker — `.nsf` files in commit `8e4e1cd` — fix path

**Author:** ALX (laptop session, 2026-05-02 evening)
**Status:** diagnosis complete · fix path validated · execution deferred (parallel session active)
**For:** the next session that reaches Wave 4 of `2026-05-03-canary-gcp-blinking-multi-track-kickoff.md` and needs to push to origin

---

## TL;DR

A historical commit on `main` carries 692 MB of Lotus Notes `.nsf` archives that exceed GitHub's 100 MB hard limit. **Every push to `origin/main` is rejected by the pre-receive hook.** The cleanup is a single `git filter-repo` pass + a `.gitignore` update + a normal push (no force-push needed because the bad commit is local-only).

This file exists because the cleanup couldn't be executed in the laptop session that diagnosed it — a parallel session was actively writing to `main` and to multiple worktrees at the time. The right moment for the cleanup is **between waves** when no session is writing.

---

## Diagnosis

**Bad commit:** `8e4e1cd` — *"test: trigger redeploy"* — Friday 2026-05-01 16:55:44 -0700

That commit was a broad `git add` that swept the working tree and accidentally tracked these binaries (none referenced by any code, none intentional):

| File | Size | GitHub status |
|---|---|---|
| `Brain/raw/inbox/NOTES/Glyle1.nsf` | 614 MB | ❌ exceeds 100 MB hard limit |
| `Brain/raw/inbox/NOTES/gclyle.nsf` | 67 MB | ⚠ over 50 MB recommended |
| `Brain/raw/inbox/NOTES/GLyle.nsf` | 3.5 MB | ok individually but bundled |
| `Brain/raw/inbox/NOTES/names.nsf` | 3.0 MB | ok individually but bundled |
| `Brain/raw/inbox/NOTES/perweb.nsf` | 1.6 MB | ok individually but bundled |
| `Brain/raw/inbox/NOTES/bookmark.nsf` | 1.5 MB | ok individually but bundled |
| **Total** | **~692 MB** | |

The `.nsf` files are 22-year-old Lotus Notes archives (dated 2003-2005) — personal historical artifacts, not project data, not referenced anywhere in the codebase.

**Containment:** the bad commit is only on local `main`. `git branch -r --contains 8e4e1cd` returns nothing. `origin/main` is at `39a5b4d` (research RapidPOS feature map) — well upstream of the bad commit.

**Affected commits:** all unpushed commits on `main` (currently 31+ depending on what the parallel session has shipped) plus every topic branch built on top of them.

---

## The fix — execute when no session is writing

### Pre-flight

1. **Confirm no active sessions are writing.** Check `git worktree list` — if there are active worktrees with uncommitted changes, wait. Check `ps aux | grep claude` — if other Claude Code processes have working directories under this repo, coordinate before proceeding.
2. **Confirm the bad commit is still only local.** `git branch -r --contains 8e4e1cd` should return nothing.
3. **Stash any pending work** — `git filter-repo` refuses to run on a dirty tree. If `git status` shows anything modified or staged, commit or stash it first.

### Execute

```bash
# 1. Install git-filter-repo (one-time, via Homebrew)
brew install git-filter-repo

# 2. Strip the entire NOTES/ directory from all history.
#    This rewrites every commit that touched anything in that path.
#    Files remain on disk in the working tree — they're just removed from git tracking.
cd /Users/gclyle/GrowDirect
git filter-repo --path Brain/raw/inbox/NOTES --invert-paths

# 3. Add .gitignore entries so this can't happen again.
#    Append to the existing /Users/gclyle/GrowDirect/.gitignore.
#
#    DELIBERATELY narrow: block by file extension, not directory.
#    Brain/raw/inbox/ IS tracked content per the intake protocol (CLAUDE.md
#    "Intake Protocol" section — engine.py ingest writes markdown there).
#    We must NOT block the inbox or any of its subdirectories — we only
#    want to prevent binaries (which never belong in git) from getting
#    accidentally swept in again, anywhere in the tree.
cat >> .gitignore <<'EOF'

# Lotus Notes binaries — historical personal artifacts, never belong in git.
# These got swept into commit 8e4e1cd by a broad git add; cleanup ran
# 2026-05-03 (see docs/superpowers/plans/2026-05-03-push-blocker-and-fix.md).
*.nsf
*.id

# Brainstorm scratch (per-session local state, also swept in 8e4e1cd)
.superpowers/brainstorm/*/

# Obsidian per-user workspace state (also swept in 8e4e1cd)
Brain/.obsidian/workspace.json
EOF

git add .gitignore
git commit -m "gitignore: exclude .nsf archives + brainstorm scratch + Obsidian workspace state

Following the cleanup of commit 8e4e1cd's accidental sweep of 692 MB of
Lotus Notes archives, add explicit gitignore patterns to prevent the same
class of accidental track from recurring."

# 4. Push main — fast-forward to origin (origin/main is at 39a5b4d, no force-push needed).
#    git filter-repo removes the 'origin' remote by default as a safety; re-add it.
git remote add origin git@github.com:growdirectprez/GrowDirect.git || true
git push origin main

# 5. Push the topic branches.
#    git filter-repo will have rewritten their SHAs too — verify with `git log --oneline`
#    on each branch before pushing. They should fast-forward cleanly to origin since
#    none have been pushed before.
for branch in $(git branch --list 'gclyle/*' --format='%(refname:short)'); do
  echo "=== Pushing $branch ==="
  git push -u origin "$branch"
done
```

### Verification

```bash
# Confirm the .nsf files are gone from history.
git log --all --diff-filter=A --name-only -- "*.nsf" 2>&1 | head
# Expected: empty output (no commits with .nsf adds remain)

# Confirm files are still on disk (they should be — filter-repo doesn't touch the working tree).
ls -lh Brain/raw/inbox/NOTES/*.nsf 2>&1 | head
# Expected: the same 6 files visible as before

# Confirm origin/main has all the cleaned commits.
git fetch origin && git log --oneline origin/main..HEAD
# Expected: empty (no local commits ahead of origin/main)
```

---

## What about the `.nsf` files themselves?

They stay on disk under `Brain/raw/inbox/NOTES/` — the founder's personal historical archives. Future commits won't sweep them in (the new gitignore handles that). What to actually do with them is the founder's call:

- **Keep where they are** — `Brain/raw/inbox/NOTES/` was likely intended as the staging area for content extraction (`engine.py extract`) before files get processed into `Brain/wiki/`. They can sit there indefinitely; they're just gitignored.
- **Move to a non-repo location** — if the founder doesn't want them mingled with repo content, move to `~/Documents/lotus-notes-archives/` or similar. Decision to make later.
- **Extract content first** — Lotus Notes archives can be opened with the Notes client or various tools. If there's content in them worth surfacing into Brain, do that before deciding where they live. Decision to make later.

None of this is blocking — the cleanup above unblocks the push regardless of what happens to the files.

---

## Why force-push is NOT needed

This is the question that warrants paranoia, so explicit reasoning:

- Force-push is required when the remote has commits that the local doesn't, and the local rewrote shared history.
- Here, `origin/main` is at `39a5b4d`. After cleanup, local `main` is at `39a5b4d` + N rewritten commits. Local strictly extends origin → fast-forward.
- The bad commit (`8e4e1cd`) is **not on origin** → rewriting it doesn't conflict with anything published.
- Topic branches have never been pushed → first push is `git push -u origin <branch>`, no force needed.

If a future session creates a branch FROM `8e4e1cd` (or any of its descendants) and pushes it before the cleanup, this analysis changes. Don't push topic branches that include the bad commit until after the cleanup runs.

---

## Why this happened (root cause + prevention)

A `git add .` or similar broad-pattern stage in commit `8e4e1cd` swept in:

- 6 `.nsf` files (692 MB)
- `.superpowers/brainstorm/1247-1777259063/*` (per-session brainstorm scratch — should never be tracked)
- `Brain/.obsidian/workspace.json` and other per-user Obsidian state
- `Brain/raw/.extract/BP/*.md` (content-extraction scratch)
- A few other transient files

The commit message — *"test: trigger redeploy"* — suggests the author was forcing a CI redeploy and didn't realize the working tree had this much accumulated cruft.

**Prevention** (covered by the new gitignore patterns):
- `*.nsf` blocks any future Lotus Notes file from being staged
- `Brain/raw/inbox/NOTES/` blocks the directory specifically
- `.superpowers/brainstorm/*/` blocks per-session brainstorm scratch
- `Brain/.obsidian/workspace.json` blocks per-user Obsidian state

The deeper prevention is **never use `git add .` or `git add -A` without first reviewing `git status`** — codified in the platform CLAUDE.md ("When staging files, prefer adding specific files by name").

---

## Cross-references

- Commit `8e4e1cd` ("test: trigger redeploy", 2026-05-01) — the offending commit
- Linear [GRO-739](https://linear.app/growdirect/issue/GRO-739) — parent dispatch (the GCP-MVP work this push unblocks)
- `docs/superpowers/plans/2026-05-03-canary-gcp-blinking-multi-track-kickoff.md` — the plan whose Wave 4 needs the push to work
- `feedback_just_commit_no_three_card_monte` — relevant memory: when the call is obvious, just execute (this fix has obvious shape)
- Platform CLAUDE.md "Committing changes with git" section — guidance against `git add -A` / `git add .`
