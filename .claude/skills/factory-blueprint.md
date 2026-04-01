---
name: factory-blueprint
description: |
  Plan writing for multi-step tasks. Produces architecture decisions, file structure tables, and numbered task lists with acceptance criteria.
---

# factory-blueprint — Plan Writing

## Pre-flight

1. Confirm a GRO issue exists. No ticket = no work. Ask if none was given.
2. Read **`~/GrowDirect/CLAUDE.md`** (platform standards) **and** the app's `CLAUDE.md` — in that order. The platform file defines the canonical patterns (UUID type, model syntax, config, auth). The app file adds domain context. When the app's existing code contradicts the platform standard, the platform standard wins for new code.
3. Check if the other app already solved this problem (Hard Rule 8). If yes, model the solution on it.

### Platform standard compliance (mandatory before drafting)

Before writing any plan that includes new tables, models, or schemas:

- **UUID PKs:** `Mapped[uuid.UUID]` with `default=uuid.uuid4`. NOT `String(36)` even if every existing table in the app uses it. `String(36)` is a historical holdover — flag it in the plan but do not propagate it.
- **Timestamps:** `created_at: Mapped[datetime]` and `updated_at: Mapped[datetime]` on every table.
- **Model syntax:** SQLAlchemy 2.0 `Mapped[]` annotations. No `Column()`.
- **Relationships:** `Mapped[list["Model"]]` with `back_populates`.
- **FK compatibility:** New FKs pointing to existing `String(36)` PKs use `String(36)` for compatibility. Document this as tech debt, not as the pattern to follow.
- **Cross-reference existing specs:** Check `docs/superpowers/specs/` and `docs/sdds/` for related designs. Note what this plan supersedes or complements.

If any of these are violated in the plan, stop and fix before moving to task list.

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

## Document filing

Plans are working documents — they live in the session, not filed permanently.
If the plan produces lasting artifacts, file them per CLAUDE.md § Document Filing Rules:

- **Architecture decisions** → `docs/decisions/YYYY-MM-DD-{title}.md`
- **New or updated SDD** → `docs/sdds/{namespace}/{service}.md`
- **Superseded docs** → `docs/_archive/YYYY-MM-DD-{name}.md`

Get confirmation before moving to TDD.
