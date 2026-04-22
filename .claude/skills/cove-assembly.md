---
name: cove-assembly
roles-primary: [Jeremy]
stage: assembly
description: |
  Execute implementation plans for Cove. Use when you have a written plan to
  execute. Loads context, runs smoke tests between tasks, stops when blocked.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Write
  - Edit
  - TodoWrite
---

# Cove Assembly — Factory Process Plan Execution

> Delegates to: `factory-assembly` for standard plan execution.

Run the factory-assembly skill, then apply the Cove-specific checklist items below.

**Announce:** "I'm using cove-assembly to execute [plan name]."

## Cove-Specific Checklist Additions

After the standard factory-assembly checklist, verify:

- [ ] All 14 blueprints registered in `cove/__init__.py`
- [ ] New models imported in `cove/models/__init__.py` (required for Alembic detection)
- [ ] If new migration: reviewed generated file — Alembic sometimes gets relationships wrong
- [ ] Data paths use `cove/parcels/data/` (not bare `data/`)
- [ ] Docker stack healthy: `docker compose -f devops/docker-compose.yml ps`
- [ ] New routes respond (curl test against `http://localhost:5002/`)

## PII & Privacy Note

If adding routes that handle member data:
- Every entity fetch must check `entity.organization_id == current_user.organization_id` (IDOR prevention)
- File uploads must validate against `ALLOWED_UPLOAD_EXTENSIONS` from config
- Privacy consent gate: new member-facing routes must be covered by the `before_request` hook

## Blueprint Registration Pattern

```python
# cove/__init__.py
from cove.{module}.routes import bp as {module}_bp
app.register_blueprint({module}_bp, url_prefix="/{module}")
```

Expected count: 14 blueprints. Run `grep -c "register_blueprint" cove/__init__.py` to verify.

---

*Cove Assembly v1.0 — Factory Process Plan Execution*
*Delegates to: factory-assembly*
