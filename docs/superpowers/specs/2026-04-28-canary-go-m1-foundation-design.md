# Canary Go — M1 Foundation Design

**Date:** 2026-04-28
**Status:** Approved
**Scope:** CanaryGo/ directory scaffold, go.mod, Docker Compose, CRDM + Identity + Multi-POS Substrate DDLs, sqlc codegen, service skeleton, first working /health endpoint

---

## Governing Thesis

M1 is not a DDL exercise — it is a toolchain proof. The highest-risk items in a greenfield Go/sqlc/pgx build are the code-generation pipeline, library version pinning, and Docker wiring, not the schema itself. Approach C (Skeleton-First) gets a running binary with a verified `/health` endpoint before any domain logic is written. Every subsequent service scaffolds into a proven foundation.

The clean-break rule is absolute: `CanaryGo/` is a separate tree from `Canary/`. Databases are `canary_go` and `canary_go_test`. The Python prototype stays on `canary`. Zero shared state.

---

## Locked Decisions

| Decision | Value |
|----------|-------|
| Local directory | `CanaryGo/` (within GrowDirect repo) |
| Go module name | `github.com/growdirect-llc/rapidpos` |
| Primary database | `canary_go` |
| Test database | `canary_go_test` |
| Go version | 1.22+ |
| PostgreSQL | 17 (shared growdirect_postgres :5432) |
| Valkey | 8 (shared growdirect_valkey :6379, DB 2 for Canary Go) |
| HTTP router | Chi v5 |
| DB driver | pgx/v5 |
| Query codegen | sqlc v2 |
| Migrations | golang-migrate/migrate v4 |
| Approach | C — Skeleton-First |

All internal imports use the full module path from day one:
```
github.com/growdirect-llc/rapidpos/internal/crdm
github.com/growdirect-llc/rapidpos/internal/db
```
No future refactor required at RapidPOS handoff. Handoff path: `git subtree split` or fresh push to `growdirect-llc/rapidpos`.

---

## Directory Layout

Follows `go-module-layout.md` SDD exactly. M1 creates the skeleton; only M1-relevant `cmd/` and `deploy/` subdirs are populated at this stage.

```
CanaryGo/
├── go.mod                          # module github.com/growdirect-llc/rapidpos
├── go.sum
├── CLAUDE.md                       # agent context for this service tree
├── Makefile                        # migrate-up, sqlc-gen, test, build targets
│
├── cmd/
│   ├── identity/
│   │   └── main.go                 # M1: Chi router, /health, /sessions/validate stub
│   ├── tsp/
│   │   └── main.go                 # M1: health check stub + Valkey stream consumer stub
│   ├── gateway/
│   │   └── main.go                 # M1: health check stub
│   ├── chirp/ alert/ fox/ owl/ analytics/ hawk/ bull/ asset/ item/
│   ├── inventory/ receiving/ transfer/ pricing/ employee/ customer/
│   └── returns/ report/ edge/  # main.go /health stubs for all 19 services (20 binaries)
│                                # M1 requires all stubs compiling — only identity has domain logic
│
├── internal/
│   ├── crdm/                       # ARTS-native canonical types — no dependencies
│   │   └── types.go                # Merchant, Location, Employee, Transaction structs
│   ├── arts/                       # ARTS POSLOG field constants
│   │   └── constants.go
│   ├── auth/                       # JWT middleware, RBAC, session parsing
│   │   ├── middleware.go
│   │   └── jwt.go
│   ├── db/                         # sqlc-generated query code + connection pool
│   │   ├── db.go                   # pgx pool setup, New() constructor
│   │   ├── sqlc/                   # hand-written SQL queries — sqlc input
│   │   │   ├── identity.sql        # queries for identity-owned tables
│   │   │   └── tsp.sql             # queries for tsp-owned tables
│   │   └── query/                  # sqlc output (generated — do not hand-edit)
│   ├── tenant/                     # Tenant isolation middleware
│   │   └── middleware.go
│   ├── config/                     # Env loading, fail-fast on missing vars
│   │   └── config.go
│   ├── pagination/                 # Cursor-based pagination helpers
│   │   └── pagination.go
│   └── testutil/                   # Fixtures, factories, DB helpers
│       └── db.go
│
├── deploy/
│   ├── migrations/
│   │   ├── 001_create_schemas.sql              # extensions + schema creation (FIRST, always)
│   │   ├── 002_identity_organizations.sql
│   │   ├── 003_identity_merchants.sql
│   │   ├── 004_identity_users_roles.sql
│   │   ├── 005_identity_employees_locations.sql
│   │   ├── 006_identity_source_systems.sql
│   │   ├── 007_identity_external_identities.sql
│   │   ├── 008_identity_oauth_tokens.sql
│   │   ├── 009_identity_sessions_audit.sql
│   │   ├── 010_tsp_sales_tables.sql
│   │   ├── 011_tsp_ingestion.sql
│   │   ├── 012_fox_cases.sql
│   │   ├── 013_fox_evidence_chain.sql          # includes hash-chain trigger
│   │   └── 014_seed_roles_source_systems.sql   # data seeds for static tables
│   └── docker-compose.yml                      # Canary Go services + DB init
│
└── sqlc.yaml                       # sqlc v2 config
```

---

## Migration Strategy

### Flat Numbering

All migrations live in `deploy/migrations/` as a single numbered sequence. The SDD's per-service subdirectory model (`deploy/migrations/<service>/`) is the long-term target; for M1 with 14 migration files, flat is simpler, safer, and avoids golang-migrate multi-directory coordination overhead.

**Post-M1 migration refactor cost:** When the per-service split happens, the following change together: `Makefile` migrate targets, `sqlc.yaml` schema paths, and the Docker Compose migrate command. This is a three-file coordinated change, not just a directory reorganization.

### Migration 001 — Foundation (runs first, always)

```sql
-- 001_create_schemas.sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "vector";

CREATE SCHEMA IF NOT EXISTS app;
CREATE SCHEMA IF NOT EXISTS sales;
CREATE SCHEMA IF NOT EXISTS metrics;
```

This migration must succeed before any table migration can run. The `vector` extension enables pgvector for Owl. `uuid-ossp` and `pgcrypto` provide `gen_random_uuid()` and encryption primitives.

### Migration Invariants

- Every DDL file is idempotent where possible (`CREATE TABLE IF NOT EXISTS`, `CREATE INDEX IF NOT EXISTS`)
- Every table: `id UUID PRIMARY KEY DEFAULT gen_random_uuid()`
- Every tenant-scoped table: `merchant_id UUID NOT NULL REFERENCES app.merchants(id)`
- Every table: `created_at TIMESTAMPTZ NOT NULL DEFAULT now()`, `updated_at TIMESTAMPTZ NOT NULL DEFAULT now()`
- Schema-qualified writes everywhere: `app.merchants`, `sales.transactions`, `metrics.daily_rollups`

### Fox Evidence Hash-Chain Trigger

Deployed in migration 013. This is a DB-level guarantee — not application code.

```sql
-- In 013_fox_evidence_chain.sql
CREATE OR REPLACE FUNCTION app.fox_evidence_immutable()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'evidence_records are append-only — UPDATE and DELETE are prohibited';
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_fox_evidence_immutable
    BEFORE UPDATE OR DELETE ON app.fox_evidence
    FOR EACH ROW EXECUTE FUNCTION app.fox_evidence_immutable();
```

### DB Name Override

All migrations and `DATABASE_URL` env vars use `canary_go` (not `canary`). The SDDs reference `canary` — that reflects the Python prototype naming. Canary Go is a clean break.

---

## Docker Compose

`CanaryGo/deploy/docker-compose.yml` joins the existing `growdirect` external network — it does not run its own postgres or valkey. It uses the shared `growdirect_postgres` container with `canary_go` / `canary_go_test` databases, and `growdirect_valkey` on DB 2.

```yaml
name: canarygo

networks:
  growdirect:
    external: true

services:
  canarygo-migrate:
    image: migrate/migrate:v4
    networks: [growdirect]
    volumes:
      - ../deploy/migrations:/migrations
    command: >
      -path=/migrations
      -database=postgres://growdirect:growdirect_dev@growdirect_postgres:5432/canary_go?sslmode=disable
      up
    depends_on:
      canarygo-dbinit:
        condition: service_completed_successfully

  canarygo-dbinit:
    image: postgres:17
    networks: [growdirect]
    entrypoint: >
      sh -c "
        psql -h growdirect_postgres -U growdirect -c 'CREATE DATABASE canary_go;' || true &&
        psql -h growdirect_postgres -U growdirect -c 'CREATE DATABASE canary_go_test;' || true
      "
    environment:
      PGPASSWORD: growdirect_dev

  canarygo-identity:
    image: canarygo-identity
    build:
      context: ../
      dockerfile: deploy/Dockerfile.identity
    networks: [growdirect]
    ports:
      - "8086:8086"
    environment:
      DATABASE_URL: postgres://growdirect:growdirect_dev@growdirect_postgres:5432/canary_go?sslmode=disable
      VALKEY_URL: redis://growdirect_valkey:6379/2
      INTERNAL_SERVICE_SECRET: dev-internal-secret
      SESSION_SECRET: dev-session-secret
      LOG_LEVEL: info
      PORT: "8086"
    depends_on:
      canarygo-migrate:
        condition: service_completed_successfully
```

A `Dockerfile.identity` is multi-stage: `golang:1.22-alpine` builder → `alpine:3.19` runtime. The pattern is identical for every service — only the `cmd/<service>` target changes.

---

## sqlc Configuration

`sqlc.yaml` at repo root. Version 2. pgx/v5 driver. One package per domain owner — queries for identity tables go in `internal/db/query/identity/`, tsp tables in `internal/db/query/tsp/`, etc.

```yaml
version: "2"
sql:
  - schema: "deploy/migrations"
    queries: "internal/db/sqlc/identity.sql"
    engine: "postgresql"
    gen:
      go:
        package: "dbidentity"
        out: "internal/db/query/identity"
        sql_package: "pgx/v5"
        emit_json_tags: true
        emit_params_struct_pointers: true
        emit_result_struct_pointers: true
        overrides:
          - db_type: "vector"
            go_type:
              import: "github.com/pgvector/pgvector-go"
              type: "pgvector.Vector"
  - schema: "deploy/migrations"
    queries: "internal/db/sqlc/tsp.sql"
    engine: "postgresql"
    gen:
      go:
        package: "dbtsp"
        out: "internal/db/query/tsp"
        sql_package: "pgx/v5"
        emit_json_tags: true
        emit_params_struct_pointers: true
        emit_result_struct_pointers: true
        overrides:
          - db_type: "vector"
            go_type:
              import: "github.com/pgvector/pgvector-go"
              type: "pgvector.Vector"
```

sqlc reads the migration files as the schema source. No separate schema.sql needed. The `vector` type override is required on every `sql:` block — sqlc will fail to generate if it encounters a `VECTOR(1024)` column without it.

---

## Identity Service — M1 Target

`cmd/identity/main.go` is the M1 proof of the full pipeline.

### What M1 Delivers

| Endpoint | Status | Notes |
|----------|--------|-------|
| `GET /health` | Required | DB ping + Valkey ping; returns 200 or 503 |
| `POST /sessions/validate` | Required | JWT parse + Valkey lookup; returns valid/invalid |
| `POST /merchants` | Stub | 501 Not Implemented |
| `POST /users` | Stub | 501 Not Implemented |
| All OAuth endpoints | Stub | 501 Not Implemented |

The stub endpoints exist so the router is fully wired and every other service can import the identity client and call validate without a 404.

### Health Check Contract

Every service implements this identically:

```go
// GET /health
{
  "ok": true,
  "service": "canary-identity",
  "version": "1.0.0",
  "checks": {
    "database": "ok",
    "valkey": "ok"
  }
}
```

503 on any dependency failure.

### Session Validate Contract

```go
// POST /sessions/validate
// Body: {"token": "..."}
// 200: {"valid": true, "merchant_id": "...", "user_id": "...", "roles": [...]}
// 401: {"valid": false}
```

JWT is parsed with `SESSION_SECRET`. Token hash is checked against Valkey key `session:<sha256(token)>`. Missing Valkey key = invalid (session was revoked).

---

## Makefile Targets

```makefile
.PHONY: migrate-up migrate-down sqlc-gen test build-identity

migrate-up:
	migrate -path=deploy/migrations \
	        -database=$(DATABASE_URL) up

migrate-down:
	migrate -path=deploy/migrations \
	        -database=$(DATABASE_URL) down 1

sqlc-gen:
	sqlc generate

test:
	DATABASE_URL=postgres://growdirect:growdirect_dev@localhost:5432/canary_go_test?sslmode=disable \
	go test ./... -v

build-identity:
	go build -o bin/identity ./cmd/identity
```

---

## Landmines and Mitigations

| Risk | Mitigation |
|------|-----------|
| **pgx/v4 vs v5 mismatch** | Pin `pgx/v5` in go.mod from day one. sqlc v2 generates pgx/v5-compatible code. Never mix v4 and v5 in the same binary. |
| **sqlc schema parse errors** | sqlc reads migrations as schema. Files must be valid PostgreSQL. The `vector` extension type `VECTOR(1024)` requires sqlc override config — add `overrides` in sqlc.yaml for vector columns. |
| **golang-migrate dirty state** | If a migration fails mid-way, the `schema_migrations` table marks the version dirty. Fix: `migrate force <version>` before re-running. Never delete and recreate the DB as the fix — it destroys the clean-break guarantee. |
| **DB 2 Valkey collision** | Python Canary uses DB 0. Canary Go uses DB 2. Never use DB 0 or DB 1 (Cove). Set `VALKEY_URL=redis://growdirect_valkey:6379/2` in all Canary Go env configs. |
| **`gen_random_uuid()` on PG 13+** | PostgreSQL 17 has this built-in. No extension needed. The `uuid-ossp` extension in migration 001 is a safety net for compatibility with older test environments. |
| **Fox trigger blocks integration tests** | Test factories that need to reset evidence records will be blocked by the immutability trigger. `testutil/db.go` must drop and recreate the `fox_evidence` table (not truncate with cascade) in test teardown, or use a test-mode flag that skips trigger installation. |
| **Valkey stream consumer group init** | `canary:events` and `canary:detection` consumer groups must be created with `XGROUP CREATE ... MKSTREAM` before the first consumer starts. Add this to service startup with an idempotent check. |
| **Windows cross-compile for edge** | `GOOS=windows GOARCH=amd64 go build ./cmd/edge` is needed for the Counterpoint poller. Add `build-edge-windows` to Makefile now so the target exists. |
| **Module path mismatch at handoff** | The module is `github.com/growdirect-llc/rapidpos`. At handoff, the remote must be `https://github.com/growdirect-llc/rapidpos` for `go get` to resolve. The local directory name `CanaryGo/` is irrelevant to Go's module resolution. |
| **SDD port conflict** | `go-module-layout.md` and `microservice-architecture.md` have divergent port maps. This spec follows `go-module-layout.md` (dated 2026-04-28, the canonical repo structure SDD). Identity = 8086. At M2 the port maps must be reconciled and the microservice-architecture.md updated. |

---

## Dependency Pinning

Versions locked in `go.mod`:

```
github.com/go-chi/chi/v5 v5.1.0
github.com/jackc/pgx/v5 v5.6.0
github.com/redis/go-redis/v9 v9.5.0
github.com/golang-migrate/migrate/v4 v4.17.1
github.com/pgvector/pgvector-go v0.2.1
github.com/golang-jwt/jwt/v5 v5.2.1
github.com/google/uuid v1.6.0
go.uber.org/zap v1.27.0
```

Do not upgrade during M1. Version changes require explicit decision and commit.

---

## M1 Build Sequence

| Step | What | Done When |
|------|------|-----------|
| 1 | `mkdir CanaryGo && go mod init github.com/growdirect-llc/rapidpos` | `go.mod` exists with correct module name |
| 2 | Directory scaffold per layout above | All dirs created, `.gitkeep` in empty dirs |
| 3 | `go.mod` dependencies added | `go mod tidy` passes clean |
| 4 | `CanaryGo/CLAUDE.md` with agent context | |
| 5 | `Makefile` with all targets | |
| 6 | `deploy/docker-compose.yml` | |
| 7 | `deploy/migrations/001` through `014` | All DDL files written |
| 8 | `docker compose up canarygo-dbinit canarygo-migrate` | Migrations apply clean, no dirty state |
| 9 | `sqlc.yaml` + `internal/db/sqlc/identity.sql` seed queries | |
| 10 | `sqlc generate` | Generated code in `internal/db/query/identity/` compiles |
| 11 | `internal/config/config.go` | Fail-fast env loader |
| 12 | `internal/db/db.go` | pgxpool.New(), ping |
| 13 | `cmd/identity/main.go` | Chi router, /health wired |
| 14 | `go build ./cmd/identity` | Binary compiles |
| 15 | `docker compose up canarygo-identity` | `curl :8086/health` → `{"ok":true}` |
| 16 | `internal/auth/jwt.go` + `/sessions/validate` | Session validate returns valid/invalid correctly |
| 17 | Integration test with synthetic retailer seed | One merchant, one user, one session round-trip |
| 18 | Stub health checks for all remaining services | All 19 service binaries (20 including edge) compile |

M1 is complete when step 17 passes. Step 18 is hardening — all services boot to a verified `/health`.

---

## Post-M1 Gate

M1 SI checklist (partial — full checklist applies at Service Introduction):

- [ ] `curl :8086/health` returns `{"ok":true}` with both checks green
- [ ] `POST /sessions/validate` with a valid JWT returns correct `merchant_id` and `roles`
- [ ] `POST /sessions/validate` with an expired JWT returns `{"valid":false}`
- [ ] All 14 migrations apply clean from scratch (`migrate down` to 0, `migrate up` to 14)
- [ ] `sqlc generate` produces code that compiles without modification
- [ ] All 19 service binaries (20 including edge) compile and return 200 from `/health`
- [ ] No dirty migration state after a clean run
- [ ] `canary_go` and `canary` databases confirmed isolated (no cross-DB references)

---

## Related

- `go-module-layout.md` — repo structure and service port map
- `microservice-architecture.md` — inter-service call graph
- `data-model.md` — 82+ tables, full DDL source
- `identity.md` — Identity service full SDD
- `docs/superpowers/specs/2026-04-28-canary-go-agent-pmo-architecture-design.md` — agent PMO context
- Linear: [GRO-638](https://linear.app/growdirect/issue/GRO-638) (CRDM & Data Model) · [GRO-639](https://linear.app/growdirect/issue/GRO-639) (Identity & Auth) · [GRO-640](https://linear.app/growdirect/issue/GRO-640) (Multi-POS Substrate) · [GRO-641](https://linear.app/growdirect/issue/GRO-641) (Service Skeleton)
