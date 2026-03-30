---
name: factory-blueprint
description: |
  Plan writing for multi-step tasks. Produces architecture decisions, file structure tables, and numbered task lists with acceptance criteria.
---

# factory-blueprint — Plan Writing

## Pre-flight

1. Confirm a GRO issue exists. No ticket = no work. Ask if none was given.
2. Read the app's `CLAUDE.md` — understand existing models, routes, and patterns.
3. Check if the other app already solved this problem (Hard Rule 8). If yes, model the solution on it.

## Plan header

```
# [GRO-XXX] — [Feature Name]
Date: YYYY-MM-DD
App: [App name]
Issue: [GRO-XXX URL]
Goal: [One sentence — what exists when this is done]
```

## Architecture section

Answer each of these before writing tasks:

- **Models:** New tables or columns? Use `Mapped[]`, UUID PKs, `created_at`/`updated_at`. List any protected files touched (`extensions.py`, `env.py`, etc.) and justify why.
- **Routes:** URL, HTTP method, auth required (yes/no), response type (HTML/JSON/redirect).
- **Services:** New service functions? What do they take and return?
- **Templates:** New templates or changes to existing? Component classes from `<appname>.css` — no raw utility chains.
- **Tests:** Which test file? Which scenarios (happy path, validation error, auth required, not found)?
- **Migrations:** Is a new Alembic revision needed?

## File structure table

| Action | File | Responsibility |
|--------|------|----------------|
| create/edit | `path/to/file.py` | what this file does |

## Task list

Each task must be completable in 2–5 minutes. Format:

```
### Task N — [name]
1. Write failing test in `tests/...`
2. Run: `python3 -m pytest tests/path/test_file.py::test_name -v` → confirm it fails
3. Implement: [specific file and function]
4. Run test again → confirm it passes
5. Run smoke: `python3 -m pytest tests/ -k smoke -v`
6. Commit: `git commit -m "feat: [description] (GRO-XXX)"`
```

Maximum 8 tasks per plan. If a feature needs more, split it into two GRO issues.

## Protected files checklist

List any protected files this plan touches:
- [ ] `.env` — required because: ___
- [ ] `wsgi.py` — required because: ___
- [ ] `<appname>/extensions.py` — required because: ___
- [ ] `Dockerfile` — required because: ___
- [ ] `docker-compose*.yml` — required because: ___
- [ ] Alembic `env.py` — required because: ___

## Quality checklist (pre-task)

- [ ] No SQLite references
- [ ] All new models use `Mapped[]`, UUID PKs, timestamps
- [ ] All new routes have `@login_required` (or justified public)
- [ ] No hardcoded secrets — config from env
- [ ] No CDN links — JS/CSS via npm
- [ ] CSS: component classes only, no raw utility chains

## Save location

`~/GrowDirect/<App>/docs/plans/YYYY-MM-DD-<feature-name>.md`

Get confirmation before moving to TDD.
