---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Bug Report: SQLite Removal + Technical Debt Audit
**Filed by:** ALX  
**Date:** February 25, 2026  
**Sprint:** Sprint 5 / Sprint 6 (post-demo)  
**Assigned to:** Jeremy + Qwen  
**Priority:** See severity per bug — demo-week items flagged 🔴

---

## Background

Audit triggered by: `rig-compose.yml` contained `DATABASE_URL: sqlite:///data/canary.db` for the Flask service. This surfaced a broader question — is SQLite gone everywhere? Answer: **mostly, but not completely.** The codebase has fully migrated to PostgreSQL at the infrastructure level, but several files still reference SQLite directly in ways that need fixing.

The confirmed good news: **no SQLite references in application logic or devops compose files** (excluding the single error in `rig-compose.yml`, now fixed). The remaining issues are in config fallbacks, legacy scaffolding, and one dangerously active file.

---

## BUGS — Fix These

---

### 🔴 BUG-RIG-001 — `rig-compose.yml`: Flask wired to SQLite
**File:** `_ALX/ubuntu-rig/rig-compose.yml`  
**Line:** Flask service environment block  
**Severity:** 🔴 CRITICAL — would silently use SQLite on the rig, ignoring PostgreSQL entirely  
**Status:** **FIXED by ALX this session** — changed to `postgresql://...`

**What was there:**
```yaml
DATABASE_URL: sqlite:///data/canary.db
```
**What it is now:**
```yaml
DATABASE_URL: postgresql://${POSTGRES_USER:-canary}:${POSTGRES_PASSWORD}@postgres:5432/canary_app
```
**No action needed from Jeremy/Qwen.** Logged for awareness.

---

### 🔴 BUG-DB-001 — `canary/database.py`: Entire module is SQLite-only
**File:** `canary/database.py`  
**Severity:** 🔴 HIGH — this module is actively called by `init_db.py` and `canary/models/__init__.py` re-exports its symbols  
**Sprint target:** Sprint 5 (before demo if possible, Sprint 6 at latest)

This entire module uses `sqlite3` directly. It defines `get_db()`, `init_db()`, `migrate_db()`, `execute_sql()`, etc., all wired to SQLite. The SQLAlchemy/PostgreSQL models in `canary/models/` are the correct implementation. `canary/database.py` is a parallel legacy layer that should not exist.

**Current situation:**
- `canary/models/__init__.py` re-exports `ALL_CREATE_STATEMENTS`, `ALL_INDEX_STATEMENTS`, `ALL_TRIGGER_STATEMENTS`, `MIGRATION_STATEMENTS` from `canary/models_legacy.py`
- `canary/database.py` calls `init_db()` using `sqlite3.connect()` with those same DDL statements
- The SQLAlchemy models (`canary/models/app/`, `canary/models/sales/`, etc.) are the real schema — defined for PostgreSQL
- These two schema definitions are not synchronized and will diverge

**What to do:**
1. Audit which callers depend on `canary/database.py` — specifically `get_db()` and `init_db()`. Search: `from canary.database import`, `canary.database.get_db`, `canary.database.init_db`
2. Replace any remaining `canary.database.get_db()` call sites with the SQLAlchemy session factory
3. Replace `canary.database.init_db()` with Alembic migration (already in place — Jeremy delivered migrations 001-004 in Sprint 5 Phase 2)
4. Once callers are migrated: deprecate `canary/database.py` — add a module-level warning, then delete in Sprint 6

---

### 🔴 BUG-DB-002 — `canary/config.py`: SQLite default fallback in production config
**File:** `canary/config.py`  
**Severity:** 🔴 HIGH — if `DATABASE_URL` env var is missing (e.g., forgotten in `.env.rig`), the app silently falls back to SQLite instead of failing loudly  
**Sprint target:** Sprint 5

```python
# CURRENT (dangerous fallback):
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    f'sqlite:///{DATA_DIR}/canary.db'
)

# Also in TestingConfig — this one is intentional and correct:
DATABASE_URL = 'sqlite:///:memory:'
```

**What to do:**
- `DevelopmentConfig`: Change default fallback to the local PostgreSQL URL — `postgresql://canary:canary@localhost:5432/canary_app`. Developers should be running PostgreSQL. If they're not, they should get an error, not silently switch to SQLite.
- `ProductionConfig`: Remove the fallback entirely. Add `DATABASE_URL` to the `validate()` method (it's already there — just confirm it's enforced).
- `TestingConfig`: **Leave `sqlite:///:memory:` alone.** This is intentional. In-memory SQLite for unit tests is correct and fast. Do not change.

---

### 🟠 BUG-DB-003 — `canary/models_legacy.py`: SQLite DDL still lives in the canonical schema path
**File:** `canary/models_legacy.py`  
**Severity:** 🟠 MEDIUM — not immediately breaking, but it's the wrong source of truth  
**Sprint target:** Sprint 6

`canary/models_legacy.py` contains full SQLite DDL for every table (CREATE TABLE IF NOT EXISTS statements using SQLite-specific syntax like `INTEGER PRIMARY KEY AUTOINCREMENT`). This file is re-exported through `canary/models/__init__.py` as `ALL_CREATE_STATEMENTS`.

The correct schema is in the Alembic migrations (already delivered in Sprint 5). Having both creates drift risk.

**What to do:**
- Sprint 6: Once the PostgreSQL migration path is verified stable on the rig, remove `ALL_CREATE_STATEMENTS` / `ALL_INDEX_STATEMENTS` / `ALL_TRIGGER_STATEMENTS` / `MIGRATION_STATEMENTS` from `models_legacy.py` 
- Remove the re-export from `canary/models/__init__.py`
- Alembic becomes the single source of truth for schema
- Keep the dataclass DTOs (`User`, `Session`, `AuditLogEntry`, etc.) in `models_legacy.py` only as long as they're used by the raw SQLite auth layer — track callsites and eliminate

---

### 🟠 BUG-DB-004 — `app.py`: Entire file is SQLite-wired legacy code still callable
**File:** `app.py` (root)  
**Severity:** 🟠 MEDIUM — the file redirects to `wsgi.py` if run directly, but it's still importable and contains active SQLite logic  
**Sprint target:** Sprint 6

`app.py` is the original pre-Alpha3X Flask app. It:
- Imports `sqlite3` directly
- Defines its own `get_db()` using `sqlite3.connect(DB_PATH)` 
- Has full route handlers that hit SQLite directly (no SQLAlchemy, no blueprints)
- Has `save_transaction_and_broadcast()` that does raw SQLite inserts

The file has a redirect guard — if run as `__main__`, it launches `wsgi.py` instead and logs a warning. But nothing prevents another module from importing `app.py` and accidentally calling its `get_db()`.

**What to do:**
- Confirm no other file imports from `app.py` directly: `grep -r "from app import" --include="*.py"`
- Once confirmed safe: add `raise ImportError("app.py is deprecated — use wsgi.py")` at the top of the file to prevent accidental imports
- Sprint 6: Delete `app.py` entirely after confirming wsgi.py has full feature parity

---

### 🟠 BUG-DB-005 — `config.py` (root): Active SQLite config
**File:** `config.py` (root, not `canary/config.py`)  
**Severity:** 🟠 MEDIUM — this is a separate root-level config file that is completely SQLite-hardcoded  
**Sprint target:** Sprint 5/6

```python
# config.py (root):
DATABASE_URL = "sqlite:///example.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
```

This imports from `models.py` (root), which is also legacy. It creates an engine pointed at `sqlite:///example.db` — a file that doesn't exist in the current setup.

**What to do:**
- Check if any current code imports from root `config.py`: `grep -r "from config import" --include="*.py" | grep -v venv`
- If no active imports: mark as dead code with a comment and schedule for Sprint 6 deletion
- If active imports found: route to Jeremy for immediate replacement

---

### 🟠 BUG-DB-006 — `models.py` (root): Orphaned legacy SQLAlchemy models
**File:** `models.py` (root)  
**Severity:** 🟠 MEDIUM — defines `Transaction`, `TransactionTender`, `Webhook` with wrong schema (missing most fields), wired to SQLite via root `config.py`  
**Sprint target:** Sprint 6

Root `models.py` defines three skeletal models with wrong field sets (e.g., `Transaction` has only `id`, `amount`, `status` — missing `merchant_id`, `payment_id`, `employee_id`, and 20+ other fields). These shadow the real models in `canary/models/sales/transactions.py`.

**What to do:**
- Verify root `models.py` is not imported by any active code path
- Mark as dead code, delete in Sprint 6

---

### 🟡 BUG-DB-007 — `.env` and `.env.template`: SQLite DATABASE_URL committed as default
**Files:** `.env`, `.env.template`, `.env.test`  
**Severity:** 🟡 LOW-MEDIUM — `.env` is gitignored but present on disk; templates are committed  
**Sprint target:** Sprint 5 (templates) / cleanup pass

All three files have:
```
DATABASE_URL=sqlite:///data/canary.db
```

`.env.template` and `.env.test` are committed to the repo and used by new developers to set up their environment. If someone follows the template, they'll be developing against SQLite.

**What to do:**
- Update `DATABASE_URL` in `.env.template` and `.env.test` to the local PostgreSQL URL: `postgresql://canary:canary@localhost:5432/canary_app`  
- Add a comment: `# Requires local PostgreSQL — see devops/docker-compose.alpha3x.yml`
- Update `.env` on disk (Jeffe's local) to match
- Add `POSTGRES_PASSWORD=canary` to `.env.template` so it's complete

---

### 🟡 BUG-DB-008 — `init_db.py`: Uses `sqlite_master` to verify table creation
**File:** `init_db.py` (root)  
**Severity:** 🟡 LOW — this file is already documented as legacy, but it queries `sqlite_master` which doesn't exist in PostgreSQL  
**Sprint target:** Sprint 6

```python
cursor = db.execute(
    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
)
```

`sqlite_master` is SQLite-specific. The PostgreSQL equivalent is `information_schema.tables` or `pg_catalog.pg_tables`. If anyone runs `python init_db.py` against a PostgreSQL database, it will fail with `relation "sqlite_master" does not exist`.

**What to do:**
- Update the verification query to use `information_schema.tables` (works in both SQLite and PostgreSQL for forward compatibility)
- Or just delete `init_db.py` in Sprint 6 — Alembic handles initialization

---

### 🟡 BUG-DB-009 — Stale artifact files in Canary root
**Files:** `:memory:`, `:memory:-journal`  
**Severity:** 🟡 LOW — cosmetic/hygiene  
**Sprint target:** Anytime

There are two files literally named `:memory:` and `:memory:-journal` in the Canary root. These are SQLite database files created when SQLite opened a `:memory:` path as a literal filename instead of an in-memory DB — this happens when the path string isn't handled correctly by sqlite3 in certain edge cases.

**What to do:**
- `git rm ":memory:" ":memory:-journal"` (quotes required — the colon is part of the filename)
- Add to `.gitignore`: `:memory:` and `:memory:-journal`

---

### 🟡 BUG-DB-010 — `canary/config.py`: `DATABASE_ENABLE_WAL` flag is SQLite-specific
**File:** `canary/config.py`  
**Severity:** 🟡 LOW — WAL mode is a SQLite concept. PostgreSQL handles WAL internally and this flag has no effect. It's harmless but misleading.  
**Sprint target:** Sprint 6

```python
DATABASE_ENABLE_WAL = True  # Write-Ahead Logging for concurrent access
```

PostgreSQL always uses WAL. This config flag only ever did anything in the SQLite `canary/database.py` layer. Once that's gone, this is dead config.

**What to do:**
- Remove `DATABASE_ENABLE_WAL` from all Config classes when `canary/database.py` is deprecated
- Leave it for now — it's harmless

---

## Summary Table

| Bug ID | File | Issue | Severity | Sprint |
|---|---|---|---|---|
| BUG-RIG-001 | `_ALX/ubuntu-rig/rig-compose.yml` | Flask → SQLite URL | 🔴 CRITICAL | **FIXED** |
| BUG-DB-001 | `canary/database.py` | Entire module is SQLite-only | 🔴 HIGH | Sprint 5/6 |
| BUG-DB-002 | `canary/config.py` | SQLite default fallback in prod | 🔴 HIGH | Sprint 5 |
| BUG-DB-003 | `canary/models_legacy.py` | SQLite DDL as canonical schema | 🟠 MEDIUM | Sprint 6 |
| BUG-DB-004 | `app.py` | Legacy SQLite routes still importable | 🟠 MEDIUM | Sprint 6 |
| BUG-DB-005 | `config.py` (root) | Hardcoded `sqlite:///example.db` | 🟠 MEDIUM | Sprint 5/6 |
| BUG-DB-006 | `models.py` (root) | Orphaned SQLAlchemy/SQLite models | 🟠 MEDIUM | Sprint 6 |
| BUG-DB-007 | `.env`, `.env.template`, `.env.test` | SQLite default in committed templates | 🟡 LOW | Sprint 5 |
| BUG-DB-008 | `init_db.py` | `sqlite_master` query fails on PostgreSQL | 🟡 LOW | Sprint 6 |
| BUG-DB-009 | `:memory:`, `:memory:-journal` | Stale SQLite artifact files in root | 🟡 LOW | Anytime |
| BUG-DB-010 | `canary/config.py` | `DATABASE_ENABLE_WAL` is SQLite-only | 🟡 LOW | Sprint 6 |

---

## Recommended Sprint 5 (This Week) Scope

Focus only on what could cause a production failure or mislead a developer:

1. **BUG-DB-002** — Fix `canary/config.py` SQLite fallback. Small change, high value.
2. **BUG-DB-007** — Update `.env.template` + `.env.test` to PostgreSQL URL. 2-minute fix.
3. **BUG-DB-009** — Delete the `:memory:` files. `git rm` + `.gitignore`. 1 minute.

Everything else can be Sprint 6 cleanup. None of it blocks the demo.

---

## What Does NOT Need to Change

- `TestingConfig.DATABASE_URL = 'sqlite:///:memory:'` — **intentional, leave it**
- `venv/` SQLite dialect files — third-party, not our code
- The immutability trigger DDL in `models_legacy.py` — these are the SQLite trigger definitions used by the legacy layer. They're wrong for PostgreSQL (PostgreSQL uses different trigger syntax and the Sprint 5 Alembic migrations already deliver the correct PostgreSQL versions). Leave them until the legacy layer is fully deprecated.

---

*Filed by ALX · February 25, 2026 · Derived from full codebase audit*
*Route: Jeremy (architecture decisions) + Qwen (mechanical fixes under Jeremy supervision)*
