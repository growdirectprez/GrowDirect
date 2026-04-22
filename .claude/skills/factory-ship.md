---
name: factory-ship
roles-primary:[Engineer]
roles-assist:[DevOps]
stage: ship
description: |
  Pre-ship checklist and deployment. Tests green, migrations reviewed, git log clean, push to remote, Linear status update.
---

# factory-ship — Ship

## Pre-ship checklist

### 1. Final test run (evidence required)

```bash
python3 -m pytest tests/ -v
```

Paste the summary line. Do not proceed with any failures.

### 2. Migrations applied

```bash
docker exec <appname>_flask alembic upgrade head
```

Must complete with no errors. Check `alembic current` to confirm head is applied.

### 3. Git log review

```bash
git log --oneline origin/main..HEAD
```

Every commit should:
- Reference the GRO issue number (e.g., `feat: add member invite flow (GRO-123)`)
- Be a meaningful unit — not "fix", not "wip", not "changes"

If commits are messy, clean them up before pushing. No force-push to main.

### 4. No uncommitted changes

```bash
git status
```

Clean working tree only. Stage and commit or stash anything outstanding.

### 5. Push to remote

```bash
git push origin <branch>
```

### 6. Update Linear

- Move the GRO issue to "Done" (or "In Review" if PR review is required)
- Add a comment with the commit range or PR link

## Ship is complete when

Tests pass, migrations applied, git log clean, pushed, Linear updated.
