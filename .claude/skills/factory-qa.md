---
name: factory-qa
roles-primary: [Compliance]
roles-assist: [Jim, Legal]
stage: qa
description: |
  Quality assurance pass. Route testing, auth checks, standards compliance, CSS validation, protected file audits.
---

# factory-qa — Quality Assurance

## Route testing

For every new or modified route:
- Hit it in a browser or with `curl` — does it return the expected response?
- Submit forms with valid data — does it succeed?
- Submit forms with invalid/missing data — does it show inline errors below each field (WTForms pattern)?
- Hit it while unauthenticated — does it redirect to login?

## Auth check

```bash
# grep every new route for @login_required
grep -n "def " <appname>/routes/<blueprint>.py
```

Every route that isn't explicitly public must have `@login_required`. No exceptions.

## Standards compliance

Check new models:
- `Mapped[]` type annotations — no `Column()` usage
- UUID primary key: `Mapped[uuid.UUID]`
- `created_at: Mapped[datetime]` and `updated_at: Mapped[datetime]` on every table

Check config:
- No hardcoded secrets in any file — everything from `os.environ` or `.env`
- No SQLite references anywhere

## CSS compliance

Check new/modified templates:
- Do they use component classes from `static/css/<appname>.css`?
- No raw Tailwind utility chains in templates (no `class="flex items-center gap-2 px-4 py-2 bg-blue-600..."`)
- No CDN `<script>` or `<link>` tags — all JS/CSS from `static/css/dist/main.css` and npm build

## Protected files audit

List every protected file touched during this GRO issue. For each one, confirm:
- The change was necessary for the feature (not incidental)
- The change is minimal

Protected files: `.env`, `wsgi.py`, `<appname>/extensions.py`, `Dockerfile`, `docker-compose*.yml`, Alembic `env.py`

## Fix before ship

Any issue found in QA = fix it now. Do not carry QA findings into the next session.
