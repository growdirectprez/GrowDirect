---
name: canary-ship
roles-primary: [Jeremy]
roles-assist: [DevOps]
stage: ship
description: |
  Finish and ship a development branch. Use when implementation is complete,
  all tests pass, and you need to decide how to integrate the work. Runs
  pre-landing review, organizes bisectable commits, creates PR with evidence,
  bridges to canary-deploy for QA pipeline. Replaces superpowers:finishing-a-development-branch.
allowed-tools:
  - Read
  - Bash
  - Edit
  - Write
  - Grep
  - Glob
---

# Canary Ship — Finishing a Development Branch

> "If this thing works we might have to rebuild everything and consume months
> of costs because I was lazy." — Jeffe, Feb 23, 2026

## Overview

Pre-flight -> QA gate -> Pre-landing review -> Bisectable commits -> Ship -> Post-ship.

This is a **structured, automated workflow**. Once the user says "ship it",
run straight through. Only stop for failing tests, critical review findings,
or merge conflicts.

**Announce at start:** "I'm using canary-ship to complete this work."

---

## Step 1: Pre-Flight

```bash
BRANCH=$(git branch --show-current)
echo "Branch: $BRANCH"
if [ "$BRANCH" = "main" ]; then
  echo "ABORT: Ship from a feature branch, not main."
  exit 1
fi
git diff main...HEAD --stat
git log main..HEAD --oneline
git status --short
```

If there are uncommitted changes, stage and commit them before proceeding.

---

## Step 2: QA Gate — canary-qa

**Run canary-qa in diff-aware mode.** Mandatory before shipping.

Health score >= 75 -> proceed. Health score < 75 -> STOP. Fix before shipping.

---

## Step 3: Merge origin/main

```bash
git fetch origin main
git merge origin/main --no-edit
```

**If merge conflicts:** Simple conflicts auto-resolve. Complex or ambiguous -> STOP.

---

## Step 4: Run Tests (on merged code)

```bash
python3 -m pytest tests/unit/ -v
python3 -m pytest tests/smoke/ -v --timeout=30
python3 -m pytest tests/integration/ -m postgres -v
curl -sf http://localhost:5001/health | python3 -m json.tool
```

**If any test fails:** STOP. Do not proceed.

---

## Step 5: Pre-Landing Review

Review the diff for structural issues that tests don't catch.

**Pass 1 (CRITICAL — stop if found):**
- Data safety: UPDATE/DELETE on canary_sales, raw SQL without params, missing FK constraints, false positive risk
- Infrastructure safety: missing pip packages, unguarded protected file edits, new ports, sqlite3 imports

**Pass 2 (INFORMATIONAL — note but don't stop):**
- Code quality: SQLAlchemy 2.0 syntax, type hints, no _v2 variants
- Factory Process: tests exist, GRO references in commits
- Lazy Pipe Check: hardcoded routes, non-persisting services
- Pipeline Architecture: merchant isolation, gLog flow, UUID principle

---

## Step 6: Bisectable Commits

**Commit ordering (earlier first):**
- Infrastructure (migrations, config, route registrations)
- Models (with tests)
- Services (with tests)
- Routes (with tests)
- Templates/Static
- Ship commit (version bump, Linear reference)

Each commit must be independently valid. No broken imports.

**Commit message format:**
```
<type>(GRO-XXX): <summary>
```
Types: `feat`, `fix`, `chore`, `refactor`, `test`, `docs`

---

## Step 7: Present Ship Options

```
1. Push and create a Pull Request
2. Merge back to main locally
3. Deploy to QA (canary-deploy pipeline)
4. Keep the branch as-is
5. Discard this work
```

### Option 1: Push and Create PR (recommended)

```bash
git push -u origin $BRANCH
gh pr create --title "feat(GRO-XXX): <summary>" --body "$(cat <<'EOF'
## Summary
<bullet points>

## Pre-Landing Review
<findings or "Clean — no issues found.">

## QA Report
<health score and key findings>

## Test Results
- [x] Unit tests: N passed / 0 failed
- [x] Smoke tests: N passed / 0 failed
- [x] Integration tests: N passed / 0 failed
- [x] Health endpoint: 200 OK

## GRO Issue
GRO-XXX
EOF
)"
```

### Option 2: Merge Locally

```bash
git checkout main && git pull origin main && git merge $BRANCH
python3 -m pytest tests/unit/ -v
python3 -m pytest tests/smoke/ -v --timeout=30
git branch -d $BRANCH
```

---

## Step 8: Post-Ship

- Update Linear issue status
- Store decisions to pgvector memory
- Log follow-up work as new Linear issues

---

## Red Flags — STOP

- Shipping with failing tests
- Shipping with QA health score < 75
- Force-pushing without explicit request
- Skipping the pre-landing review
- Merging without testing the merged result
- Shipping a route that returns hardcoded JSON

---

*Canary Ship v2.0 — Finishing a Development Branch*
*Replaces: superpowers:finishing-a-development-branch*
