# Canary Go M1 Foundation Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stand up the complete CanaryGo/ monorepo scaffold, run 14 DDL migrations against a clean `canary_go` database, prove sqlc codegen works end-to-end, and ship a running `canary-identity` service returning `{"ok":true}` from `GET /health`.

**Architecture:** Skeleton-first — toolchain is the risk, not the schema. Every decision in this plan follows the locked spec at `docs/superpowers/specs/2026-04-28-canary-go-m1-foundation-design.md`. The Go module `github.com/growdirect-llc/rapidpos` lives in `CanaryGo/` (sibling to `Canary/` in the GrowDirect repo). All 19 service binaries compile by end of M1; only `identity` has domain logic.

**Tech Stack:** Go 1.22+, Chi v5, pgx/v5, sqlc v2, golang-migrate v4, PostgreSQL 17 (`canary_go` DB), Valkey 8 (DB 2), go-redis v9, golang-jwt/jwt v5, zap

---

## Chunk 1: Project Scaffold

**Files:**
- Create: `CanaryGo/go.mod`
- Create: `CanaryGo/CLAUDE.md`
- Create: `CanaryGo/Makefile`
- Create: `CanaryGo/deploy/Dockerfile.identity`
- Create: `CanaryGo/deploy/docker-compose.yml`

---

### Task 1: Initialize the Go module

**Pre-condition:** Run from `~/GrowDirect/` (the repo root). The shared Docker stack (`growdirect_postgres`, `growdirect_valkey`) must be up before any migration step.

**Files:**
- Create: `CanaryGo/go.mod`

- [ ] **Step 1.1: Create directory and initialize module**

```bash
mkdir -p ~/GrowDirect/CanaryGo
cd ~/GrowDirect/CanaryGo
go mod init github.com/growdirect-llc/rapidpos
```

Expected: `go.mod` created with `module github.com/growdirect-llc/rapidpos` and `go 1.22`

- [ ] **Step 1.2: Add all pinned dependencies**

```bash
cd ~/GrowDirect/CanaryGo
go get github.com/go-chi/chi/v5@v5.1.0
go get github.com/jackc/pgx/v5@v5.6.0
go get github.com/redis/go-redis/v9@v9.5.0
go get github.com/golang-migrate/migrate/v4@v4.17.1
go get github.com/pgvector/pgvector-go@v0.2.1
go get github.com/golang-jwt/jwt/v5@v5.2.1
go get github.com/google/uuid@v1.6.0
go get go.uber.org/zap@v1.27.0
go mod tidy
```

Expected: `go.sum` generated, `go mod tidy` exits 0 with no output.

- [ ] **Step 1.3: Verify go.mod has correct module and versions**

```bash
head -5 go.mod
grep "github.com/jackc/pgx/v5" go.mod
grep "github.com/go-chi/chi/v5" go.mod
```

Expected: first line is `module github.com/growdirect-llc/rapidpos`, both deps present at specified versions.

- [ ] **Step 1.4: Commit**

```bash
git add CanaryGo/go.mod CanaryGo/go.sum
git commit -m "feat(canarygo): initialize Go module github.com/growdirect-llc/rapidpos"
```

---

### Task 2: Directory scaffold

**Files:**
- Create: directory tree under `CanaryGo/`

- [ ] **Step 2.1: Create all cmd/ directories**

```bash
cd ~/GrowDirect/CanaryGo
mkdir -p cmd/identity cmd/tsp cmd/gateway cmd/chirp cmd/alert cmd/fox \
         cmd/owl cmd/analytics cmd/hawk cmd/bull cmd/asset cmd/item \
         cmd/inventory cmd/receiving cmd/transfer cmd/pricing \
         cmd/employee cmd/customer cmd/returns cmd/report cmd/edge
```

- [ ] **Step 2.2: Create all internal/ directories**

```bash
mkdir -p internal/crdm internal/arts internal/auth \
         internal/db/sqlc internal/db/query/identity internal/db/query/tsp \
         internal/tenant internal/config internal/pagination internal/testutil
```

- [ ] **Step 2.3: Create deploy/ directories**

```bash
mkdir -p deploy/migrations deploy/cloud-run deploy/edge
```

- [ ] **Step 2.4: Add .gitkeep to all empty directories**

Git does not track empty directories. Every directory created in Steps 2.1–2.3 that will not have files written until a later chunk needs a `.gitkeep` so the scaffold commit is complete and re-clone produces the correct tree.

```bash
# cmd/ stubs — all empty until Chunk 4 writes them
for svc in tsp gateway chirp alert fox owl analytics hawk bull \
           asset item inventory receiving transfer pricing \
           employee customer returns report edge; do
    touch cmd/$svc/.gitkeep
done

# Internal query dirs — empty until sqlc generates into them
touch internal/db/query/identity/.gitkeep
touch internal/db/query/tsp/.gitkeep

# Deploy output dirs
touch deploy/cloud-run/.gitkeep
touch deploy/edge/.gitkeep
```

Note: `cmd/identity/` is excluded — Chunk 4 writes its files immediately.

- [ ] **Step 2.5: Commit scaffold**

```bash
cd ~/GrowDirect
git add CanaryGo/
git commit -m "feat(canarygo): directory scaffold per go-module-layout SDD"
```

---

### Task 3: CLAUDE.md for CanaryGo/

**Files:**
- Create: `CanaryGo/CLAUDE.md`

- [ ] **Step 3.1: Write CLAUDE.md**

```markdown
# CanaryGo — Agent Context

## Module
`github.com/growdirect-llc/rapidpos` — monorepo, single go.mod at root.

## This build
Greenfield Go service tree for the Canary Go platform. 19 services (20 binaries with edge).
Active milestone: M1 Foundation. See spec: `docs/superpowers/specs/2026-04-28-canary-go-m1-foundation-design.md`.

## Stack
Go 1.22+ · Chi v5 · pgx/v5 · sqlc v2 · golang-migrate v4 · PostgreSQL 17 · Valkey 8

## Databases
Primary: `canary_go` on growdirect_postgres :5432
Test:    `canary_go_test` on growdirect_postgres :5432
Valkey:  DB 2 on growdirect_valkey :6379

## Never
- Never import from Canary/ (Python prototype — frozen)
- Never use pgx/v4 — this codebase is pgx/v5 only
- Never write raw SQL strings in service code — all queries go through sqlc
- Never use `canary` or `canary_test` DB names — those belong to the Python prototype
- Never use Valkey DB 0 (Python Canary) or DB 1 (Cove)

## Service ports (go-module-layout.md)
identity :8086 · tsp :8080 · chirp :8081 · hawk :8082 · fox :8083 · owl :8084
bull :8085 · alert :8087 · analytics :8088 · asset :8089 · item :8090

## SDDs (read before touching a service)
`docs/sdds/go-handoff/` — data-model.md, go-module-layout.md, microservice-architecture.md, identity.md

## sqlc
- Input queries: `internal/db/sqlc/<service>.sql`
- Generated output: `internal/db/query/<service>/` — do not hand-edit
- Run: `make sqlc-gen` (requires sqlc binary installed)

## Migrations
- Path: `deploy/migrations/` (flat numbered, 001–014 for M1)
- Run: `make migrate-up DATABASE_URL=...`
- Dirty state fix: `migrate -path=deploy/migrations -database=$DATABASE_URL force <version>`
```

- [ ] **Step 3.2: Commit**

```bash
cd ~/GrowDirect
git add CanaryGo/CLAUDE.md
git commit -m "feat(canarygo): agent context CLAUDE.md"
```

---

### Task 4: Makefile

**Files:**
- Create: `CanaryGo/Makefile`

- [ ] **Step 4.1: Write Makefile**

```makefile
.PHONY: migrate-up migrate-down migrate-test-up sqlc-gen test \
        build-identity build-all build-edge-windows lint

# Default DATABASE_URL — override on command line
DATABASE_URL ?= postgres://growdirect:growdirect_dev@localhost:5432/canary_go?sslmode=disable
TEST_DATABASE_URL ?= postgres://growdirect:growdirect_dev@localhost:5432/canary_go_test?sslmode=disable

migrate-up:
	migrate -path=deploy/migrations \
	        -database="$(DATABASE_URL)" up

migrate-down:
	migrate -path=deploy/migrations \
	        -database="$(DATABASE_URL)" down 1

migrate-test-up:
	migrate -path=deploy/migrations \
	        -database="$(TEST_DATABASE_URL)" up

sqlc-gen:
	sqlc generate

test:
	DATABASE_URL="$(TEST_DATABASE_URL)" \
	VALKEY_URL=redis://localhost:6379/2 \
	SESSION_SECRET=test-session-secret \
	INTERNAL_SERVICE_SECRET=test-internal-secret \
	go test ./... -v -count=1

build-identity:
	go build -o bin/identity ./cmd/identity

build-all:
	@for svc in identity tsp gateway chirp alert fox owl analytics hawk bull \
	            asset item inventory receiving transfer pricing employee \
	            customer returns report; do \
	    echo "Building $$svc..."; \
	    go build -o bin/$$svc ./cmd/$$svc || exit 1; \
	done
	@echo "Building edge..."
	go build -o bin/edge ./cmd/edge

build-edge-windows:
	GOOS=windows GOARCH=amd64 go build -o bin/edge.exe ./cmd/edge

lint:
	go vet ./...
```

- [ ] **Step 4.2: Verify Makefile parses**

```bash
cd ~/GrowDirect/CanaryGo
make lint
```

Expected: `no Go files` errors for empty packages — that is fine. No parse errors in the Makefile itself.

- [ ] **Step 4.3: Commit**

```bash
cd ~/GrowDirect
git add CanaryGo/Makefile
git commit -m "feat(canarygo): Makefile with migrate, sqlc-gen, test, build targets"
```

---

### Task 5: Dockerfile.identity and Docker Compose

**Files:**
- Create: `CanaryGo/deploy/Dockerfile.identity`
- Create: `CanaryGo/deploy/docker-compose.yml`

- [ ] **Step 5.1: Write Dockerfile.identity**

```dockerfile
# deploy/Dockerfile.identity
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /identity ./cmd/identity

FROM alpine:3.19
RUN apk add --no-cache ca-certificates tzdata
COPY --from=builder /identity /identity
ENTRYPOINT ["/identity"]
```

- [ ] **Step 5.2: Write docker-compose.yml**

```yaml
name: canarygo

networks:
  growdirect:
    external: true

services:
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

  canarygo-migrate:
    image: migrate/migrate:v4
    networks: [growdirect]
    volumes:
      - ./migrations:/migrations
    command: >
      -path=/migrations
      -database=postgres://growdirect:growdirect_dev@growdirect_postgres:5432/canary_go?sslmode=disable
      up
    depends_on:
      canarygo-dbinit:
        condition: service_completed_successfully

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

Note: the volume mount is `./migrations` (relative to the compose file at `deploy/`), which resolves to `deploy/migrations/`.

- [ ] **Step 5.3: Verify shared Docker network exists**

```bash
docker network ls | grep growdirect
```

Expected: one line with `growdirect` and driver `bridge`. If missing: `cd ~/GrowDirect/devops && docker compose up -d`.

- [ ] **Step 5.4: Commit**

```bash
cd ~/GrowDirect
git add CanaryGo/deploy/
git commit -m "feat(canarygo): Dockerfile.identity + docker-compose.yml with shared growdirect network"
```

---

## Chunk 2: Migrations

**Files:**
- Create: `CanaryGo/deploy/migrations/001_create_schemas.up.sql` through `014_seed_roles_source_systems.up.sql`

> **NAMING REQUIRED:** golang-migrate's `file://` source only recognizes files matching `{version}_{title}.up.sql` (or `.down.sql`). Files named just `NNN_title.sql` are silently ignored — `migrate up` will run 0 migrations and show "no change." Every file below uses the `.up.sql` suffix. Down migrations are deferred to post-M1.

All migrations follow these invariants (do not deviate):
- `CREATE TABLE IF NOT EXISTS` (idempotent)
- `CREATE INDEX IF NOT EXISTS` (idempotent)
- UUID PKs: `id UUID PRIMARY KEY DEFAULT gen_random_uuid()`
- Tenant scope: `merchant_id UUID NOT NULL REFERENCES app.merchants(id)`
- Audit columns: `created_at TIMESTAMPTZ NOT NULL DEFAULT now()`, `updated_at TIMESTAMPTZ NOT NULL DEFAULT now()`

---

### Task 6: Foundation migration (001)

**Files:**
- Create: `CanaryGo/deploy/migrations/001_create_schemas.up.sql`

- [ ] **Step 6.1: Write migration 001**

```sql
-- 001_create_schemas.up.sql
-- Extensions must come before schemas; schemas before all tables.
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "vector";

CREATE SCHEMA IF NOT EXISTS app;
CREATE SCHEMA IF NOT EXISTS sales;
CREATE SCHEMA IF NOT EXISTS metrics;
```

- [ ] **Step 6.2: Verify shared infra is up**

```bash
docker ps | grep growdirect_postgres
docker ps | grep growdirect_valkey
```

Expected: both containers running. If not: `cd ~/GrowDirect/devops && docker compose up -d`.

- [ ] **Step 6.3: Run dbinit to create databases**

```bash
cd ~/GrowDirect/CanaryGo
docker compose -f deploy/docker-compose.yml run --rm canarygo-dbinit
```

Expected: one or two lines like `CREATE DATABASE` or `ERROR:  database "canary_go" already exists` (both are OK — `|| true` swallows the error).

- [ ] **Step 6.4: Apply migration 001 only**

```bash
DATABASE_URL="postgres://growdirect:growdirect_dev@localhost:5432/canary_go?sslmode=disable"
migrate -path=deploy/migrations -database="$DATABASE_URL" up 1
```

Expected: `1/u create_schemas (Xms)` — no errors.

- [ ] **Step 6.5: Verify schemas exist**

```bash
psql -h localhost -U growdirect -d canary_go \
  -c "\dn" -c "SELECT extname FROM pg_extension WHERE extname IN ('uuid-ossp','pgcrypto','vector');"
```

Expected: `app`, `sales`, `metrics` in schema list; all three extensions present.

---

### Task 7: Identity domain migrations (002–009)

**Files:**
- Create: `CanaryGo/deploy/migrations/002_identity_organizations.up.sql`
- Create: `CanaryGo/deploy/migrations/003_identity_merchants.up.sql`
- Create: `CanaryGo/deploy/migrations/004_identity_users_roles.up.sql`
- Create: `CanaryGo/deploy/migrations/005_identity_employees_locations.up.sql`
- Create: `CanaryGo/deploy/migrations/006_identity_source_systems.up.sql`
- Create: `CanaryGo/deploy/migrations/007_identity_external_identities.up.sql`
- Create: `CanaryGo/deploy/migrations/008_identity_oauth_tokens.up.sql`
- Create: `CanaryGo/deploy/migrations/009_identity_sessions_audit.up.sql`

- [ ] **Step 7.1: Write 002_identity_organizations.up.sql**

```sql
-- 002_identity_organizations.up.sql
CREATE TABLE IF NOT EXISTS app.organizations (
    id                  UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    org_name            TEXT        NOT NULL,
    billing_email       TEXT,
    subscription_tier   TEXT        NOT NULL DEFAULT 'starter'
                                    CHECK (subscription_tier IN ('starter','professional','enterprise')),
    billing_provider    TEXT        CHECK (billing_provider IN ('square','manual','none')),
    billing_external_id TEXT,
    billing_status      TEXT        CHECK (billing_status IN ('trialing','active','past_due','canceled','comped')),
    is_active           BOOLEAN     NOT NULL DEFAULT true,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_by          UUID,
    modified_by         UUID,
    db_status           TEXT        NOT NULL DEFAULT 'active'
                                    CHECK (db_status IN ('draft','active','archived')),
    db_effective_from   TIMESTAMPTZ,
    db_effective_to     TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_organizations_is_active ON app.organizations (is_active);
```

- [ ] **Step 7.2: Write 003_identity_merchants.up.sql**

```sql
-- 003_identity_merchants.up.sql
CREATE TABLE IF NOT EXISTS app.merchants (
    id                  UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id     UUID        NOT NULL REFERENCES app.organizations(id),
    source_merchant_id  TEXT        NOT NULL UNIQUE,
    merchant_name       TEXT        NOT NULL,
    currency            CHAR(3)     NOT NULL DEFAULT 'USD',
    is_active           BOOLEAN     NOT NULL DEFAULT true,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_merchants_organization_id ON app.merchants (organization_id);
CREATE INDEX IF NOT EXISTS idx_merchants_source_merchant_id ON app.merchants (source_merchant_id);

CREATE TABLE IF NOT EXISTS app.merchant_settings (
    id                      UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id             UUID        NOT NULL UNIQUE REFERENCES app.merchants(id),
    timezone                TEXT        NOT NULL DEFAULT 'UTC',
    language                TEXT        NOT NULL DEFAULT 'en',
    date_format             TEXT,
    calendar_type           TEXT        NOT NULL DEFAULT 'calendar_month'
                                        CHECK (calendar_type IN ('nrf_454','calendar_month')),
    fiscal_year_start_month SMALLINT,
    fiscal_week_start_day   SMALLINT,
    fiscal_pattern          TEXT,
    notif_email_enabled     BOOLEAN     NOT NULL DEFAULT true,
    notif_sms_enabled       BOOLEAN     NOT NULL DEFAULT false,
    notif_in_app_enabled    BOOLEAN     NOT NULL DEFAULT true,
    notif_quiet_hours_start SMALLINT,
    notif_quiet_hours_end   SMALLINT,
    notif_severity_threshold TEXT,
    notif_daily_limit       INTEGER,
    notif_phone             TEXT,
    theme                   TEXT,
    show_employee_names     BOOLEAN     NOT NULL DEFAULT false,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_merchant_settings_merchant_id ON app.merchant_settings (merchant_id);
```

- [ ] **Step 7.3: Write 004_identity_users_roles.up.sql**

```sql
-- 004_identity_users_roles.up.sql
CREATE TABLE IF NOT EXISTS app.roles (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    role_name   TEXT        NOT NULL UNIQUE,
    description TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_roles_role_name ON app.roles (role_name);

CREATE TABLE IF NOT EXISTS app.users (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id     UUID        NOT NULL REFERENCES app.merchants(id),
    username        TEXT        NOT NULL,
    email           TEXT        NOT NULL,
    display_name    TEXT,
    is_active       BOOLEAN     NOT NULL DEFAULT true,
    last_login_at   TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_by      UUID,
    modified_by     UUID,
    db_status       TEXT        NOT NULL DEFAULT 'active'
                                CHECK (db_status IN ('draft','active','archived')),
    db_effective_from TIMESTAMPTZ,
    db_effective_to   TIMESTAMPTZ,
    CONSTRAINT uq_users_merchant_email UNIQUE (merchant_id, email)
);

CREATE INDEX IF NOT EXISTS idx_users_merchant_id ON app.users (merchant_id);
CREATE INDEX IF NOT EXISTS idx_users_email ON app.users (email);

CREATE TABLE IF NOT EXISTS app.user_roles (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id UUID        NOT NULL REFERENCES app.merchants(id),
    user_id     UUID        NOT NULL REFERENCES app.users(id),
    role_id     UUID        NOT NULL REFERENCES app.roles(id),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_by  UUID,
    modified_by UUID
);

CREATE INDEX IF NOT EXISTS idx_user_roles_merchant_id ON app.user_roles (merchant_id);
CREATE INDEX IF NOT EXISTS idx_user_roles_user_id ON app.user_roles (user_id);
```

- [ ] **Step 7.4: Write 005_identity_employees_locations.up.sql**

```sql
-- 005_identity_employees_locations.up.sql
CREATE TABLE IF NOT EXISTS app.employees (
    id                  UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id         UUID        NOT NULL REFERENCES app.merchants(id),
    square_employee_id  TEXT        NOT NULL,
    employee_name       TEXT        NOT NULL,
    email               TEXT,
    risk_score          NUMERIC(4,3) NOT NULL DEFAULT 0.0
                                    CHECK (risk_score BETWEEN 0.0 AND 1.0),
    is_active           BOOLEAN     NOT NULL DEFAULT true,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_by          UUID,
    modified_by         UUID,
    db_status           TEXT        NOT NULL DEFAULT 'active'
                                    CHECK (db_status IN ('draft','active','archived')),
    db_effective_from   TIMESTAMPTZ,
    db_effective_to     TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_employees_merchant_id ON app.employees (merchant_id);
CREATE INDEX IF NOT EXISTS idx_employees_square_employee_id ON app.employees (merchant_id, square_employee_id);

CREATE TABLE IF NOT EXISTS app.locations (
    id                  UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id         UUID        NOT NULL REFERENCES app.merchants(id),
    square_location_id  TEXT        NOT NULL,
    location_name       TEXT        NOT NULL,
    address_line1       TEXT,
    address_line2       TEXT,
    city                TEXT,
    state               TEXT,
    postal_code         TEXT,
    coordinates         JSONB,
    is_active           BOOLEAN     NOT NULL DEFAULT true,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_by          UUID,
    modified_by         UUID,
    db_status           TEXT        NOT NULL DEFAULT 'active'
                                    CHECK (db_status IN ('draft','active','archived')),
    db_effective_from   TIMESTAMPTZ,
    db_effective_to     TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_locations_merchant_id ON app.locations (merchant_id);
CREATE INDEX IF NOT EXISTS idx_locations_square_location_id ON app.locations (merchant_id, square_location_id);

CREATE TABLE IF NOT EXISTS app.location_hierarchy (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id UUID        NOT NULL REFERENCES app.merchants(id),
    name        TEXT        NOT NULL,
    level       SMALLINT    NOT NULL,
    parent_id   UUID        REFERENCES app.location_hierarchy(id),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_by  UUID,
    modified_by UUID,
    db_status   TEXT        NOT NULL DEFAULT 'active'
                            CHECK (db_status IN ('draft','active','archived')),
    db_effective_from TIMESTAMPTZ,
    db_effective_to   TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_location_hierarchy_merchant_id ON app.location_hierarchy (merchant_id);
CREATE INDEX IF NOT EXISTS idx_location_hierarchy_parent_id ON app.location_hierarchy (parent_id);

CREATE TABLE IF NOT EXISTS app.user_employee_links (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id UUID        NOT NULL REFERENCES app.merchants(id),
    user_id     UUID        NOT NULL REFERENCES app.users(id),
    employee_id UUID        NOT NULL REFERENCES app.employees(id),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_by  UUID,
    modified_by UUID
);

CREATE INDEX IF NOT EXISTS idx_user_employee_links_merchant_id ON app.user_employee_links (merchant_id);

CREATE TABLE IF NOT EXISTS app.employee_location_assignments (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id UUID        NOT NULL REFERENCES app.merchants(id),
    employee_id UUID        NOT NULL REFERENCES app.employees(id),
    location_id UUID        NOT NULL REFERENCES app.locations(id),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_by  UUID,
    modified_by UUID
);

CREATE INDEX IF NOT EXISTS idx_emp_loc_assignments_merchant_id ON app.employee_location_assignments (merchant_id);
CREATE INDEX IF NOT EXISTS idx_emp_loc_assignments_employee_id ON app.employee_location_assignments (employee_id);
```

- [ ] **Step 7.5: Write 006_identity_source_systems.up.sql**

```sql
-- 006_identity_source_systems.up.sql
CREATE TABLE IF NOT EXISTS app.source_systems (
    code         TEXT        PRIMARY KEY,
    display_name TEXT        NOT NULL,
    category     TEXT        NOT NULL,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS app.merchant_sources (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id     UUID        NOT NULL REFERENCES app.merchants(id),
    source_code     TEXT        NOT NULL REFERENCES app.source_systems(code),
    raas_namespace  TEXT,
    status          TEXT        NOT NULL DEFAULT 'active'
                                CHECK (status IN ('active','disconnected')),
    metadata_json   JSONB,
    disconnected_at TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_by      UUID,
    modified_by     UUID
);

CREATE INDEX IF NOT EXISTS idx_merchant_sources_merchant_id ON app.merchant_sources (merchant_id);

CREATE TABLE IF NOT EXISTS app.customers (
    id                  UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id         UUID        NOT NULL REFERENCES app.merchants(id),
    square_customer_id  TEXT        NOT NULL,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_by          UUID,
    modified_by         UUID,
    db_status           TEXT        NOT NULL DEFAULT 'active'
                                    CHECK (db_status IN ('draft','active','archived')),
    db_effective_from   TIMESTAMPTZ,
    db_effective_to     TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_customers_merchant_id ON app.customers (merchant_id);
CREATE INDEX IF NOT EXISTS idx_customers_square_customer_id ON app.customers (merchant_id, square_customer_id);

CREATE TABLE IF NOT EXISTS app.products (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id     UUID        NOT NULL REFERENCES app.merchants(id),
    square_item_id  TEXT        NOT NULL,
    product_name    TEXT        NOT NULL,
    sku             TEXT,
    upc             TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_by      UUID,
    modified_by     UUID,
    db_status       TEXT        NOT NULL DEFAULT 'active'
                                CHECK (db_status IN ('draft','active','archived')),
    db_effective_from TIMESTAMPTZ,
    db_effective_to   TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_products_merchant_id ON app.products (merchant_id);
```

- [ ] **Step 7.6: Write 007_identity_external_identities.up.sql**

```sql
-- 007_identity_external_identities.up.sql
CREATE TABLE IF NOT EXISTS app.external_identities (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id UUID        NOT NULL REFERENCES app.merchants(id),
    entity_type TEXT        NOT NULL
                            CHECK (entity_type IN ('employee','location','device','product','customer')),
    entity_id   UUID        NOT NULL,
    source_code TEXT        NOT NULL REFERENCES app.source_systems(code),
    external_id TEXT        NOT NULL,
    is_primary  BOOLEAN     NOT NULL DEFAULT true,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_by  UUID,
    modified_by UUID,
    CONSTRAINT uq_ext_id_merchant_source_entity
        UNIQUE (merchant_id, source_code, entity_type, external_id),
    CONSTRAINT uq_ext_id_merchant_entity_source
        UNIQUE (merchant_id, entity_type, entity_id, source_code)
);

CREATE INDEX IF NOT EXISTS idx_ext_id_lookup
    ON app.external_identities (merchant_id, source_code, entity_type, external_id);
CREATE INDEX IF NOT EXISTS idx_ext_id_reverse
    ON app.external_identities (merchant_id, entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_ext_id_merchant ON app.external_identities (merchant_id);
```

- [ ] **Step 7.7: Write 008_identity_oauth_tokens.up.sql** (Multi-POS Substrate)

```sql
-- 008_identity_oauth_tokens.up.sql
-- Hawk (Square) OAuth credentials
CREATE TABLE IF NOT EXISTS app.hawk_oauth_tokens (
    id                      UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id             UUID        NOT NULL REFERENCES app.merchants(id),
    access_token_encrypted  TEXT        NOT NULL,
    refresh_token_encrypted TEXT,
    token_type              TEXT        NOT NULL DEFAULT 'bearer',
    expires_at              TIMESTAMPTZ NOT NULL,
    scopes                  TEXT,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_by              UUID,
    modified_by             UUID
);

CREATE INDEX IF NOT EXISTS idx_hawk_oauth_tokens_merchant_id ON app.hawk_oauth_tokens (merchant_id);

-- Bull (NCR Counterpoint) API credentials
CREATE TABLE IF NOT EXISTS app.bull_api_credentials (
    id                  UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id         UUID        NOT NULL REFERENCES app.merchants(id),
    api_key_encrypted   TEXT        NOT NULL,
    endpoint_url        TEXT        NOT NULL,
    is_active           BOOLEAN     NOT NULL DEFAULT true,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_by          UUID,
    modified_by         UUID
);

CREATE INDEX IF NOT EXISTS idx_bull_api_credentials_merchant_id ON app.bull_api_credentials (merchant_id);

CREATE TABLE IF NOT EXISTS app.bull_poll_watermarks (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id     UUID        NOT NULL REFERENCES app.merchants(id),
    endpoint_name   TEXT        NOT NULL,
    last_modified   TIMESTAMPTZ NOT NULL DEFAULT '1970-01-01 00:00:00+00',
    last_run_at     TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_bull_poll_watermarks_merchant_endpoint
        UNIQUE (merchant_id, endpoint_name)
);

CREATE INDEX IF NOT EXISTS idx_bull_poll_watermarks_merchant_id ON app.bull_poll_watermarks (merchant_id);

CREATE TABLE IF NOT EXISTS app.bull_merchant_config (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id     UUID        NOT NULL UNIQUE REFERENCES app.merchants(id),
    poll_interval_s INTEGER     NOT NULL DEFAULT 300,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS app.bull_event_log (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id UUID        NOT NULL REFERENCES app.merchants(id),
    event_type  TEXT        NOT NULL,
    payload     JSONB,
    processed_at TIMESTAMPTZ,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_bull_event_log_merchant_id ON app.bull_event_log (merchant_id);
```

- [ ] **Step 7.8: Write 009_identity_sessions_audit.up.sql**

```sql
-- 009_identity_sessions_audit.up.sql
CREATE TABLE IF NOT EXISTS app.audit_log (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id UUID        REFERENCES app.merchants(id),
    user_id     UUID        REFERENCES app.users(id),
    action      TEXT        NOT NULL,
    resource    TEXT,
    resource_id UUID,
    ip_address  TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_audit_log_merchant_id ON app.audit_log (merchant_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_user_id ON app.audit_log (user_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_created_at ON app.audit_log (created_at);

CREATE TABLE IF NOT EXISTS app.interest_signups (
    id         UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    email      TEXT        NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

---

### Task 8: TSP and Fox migrations (010–013)

**Files:**
- Create: `CanaryGo/deploy/migrations/010_tsp_sales_tables.up.sql`
- Create: `CanaryGo/deploy/migrations/011_tsp_ingestion.up.sql`
- Create: `CanaryGo/deploy/migrations/012_fox_cases.up.sql`
- Create: `CanaryGo/deploy/migrations/013_fox_evidence_chain.up.sql`

- [ ] **Step 8.1: Write 010_tsp_sales_tables.up.sql**

```sql
-- 010_tsp_sales_tables.up.sql
CREATE TABLE IF NOT EXISTS sales.transactions (
    id                      UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id             UUID        NOT NULL REFERENCES app.merchants(id),
    external_id             TEXT        NOT NULL,
    location_id             UUID        REFERENCES app.locations(id),
    employee_id             UUID        REFERENCES app.employees(id),
    customer_id             UUID        REFERENCES app.customers(id),
    arts_business_date      DATE        NOT NULL,
    arts_workstation_id     TEXT,
    transaction_type        TEXT        NOT NULL DEFAULT 'SALE',
    total_cents             BIGINT      NOT NULL DEFAULT 0,
    subtotal_cents          BIGINT      NOT NULL DEFAULT 0,
    tax_cents               BIGINT      NOT NULL DEFAULT 0,
    tip_cents               BIGINT      NOT NULL DEFAULT 0,
    discount_cents          BIGINT      NOT NULL DEFAULT 0,
    tender_type             TEXT,
    card_fingerprint        TEXT,
    card_last4              TEXT,
    card_bin                TEXT,
    card_exp_month          SMALLINT,
    card_exp_year           SMALLINT,
    statement_description   TEXT,
    payload                 JSONB,
    source_code             TEXT        REFERENCES app.source_systems(code),
    created_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_transactions_external_id UNIQUE (merchant_id, external_id)
);

CREATE INDEX IF NOT EXISTS idx_transactions_merchant_id ON sales.transactions (merchant_id);
CREATE INDEX IF NOT EXISTS idx_transactions_merchant_date ON sales.transactions (merchant_id, arts_business_date);
CREATE INDEX IF NOT EXISTS idx_transactions_employee_id ON sales.transactions (employee_id);
CREATE INDEX IF NOT EXISTS idx_transactions_location_id ON sales.transactions (location_id);

CREATE TABLE IF NOT EXISTS sales.line_items (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id     UUID        NOT NULL REFERENCES app.merchants(id),
    transaction_id  UUID        NOT NULL REFERENCES sales.transactions(id),
    product_id      UUID        REFERENCES app.products(id),
    external_id     TEXT,
    quantity        NUMERIC(10,4) NOT NULL DEFAULT 1,
    unit_price_cents BIGINT     NOT NULL DEFAULT 0,
    total_cents     BIGINT      NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_line_items_transaction_id ON sales.line_items (transaction_id);
CREATE INDEX IF NOT EXISTS idx_line_items_merchant_id ON sales.line_items (merchant_id);

CREATE TABLE IF NOT EXISTS sales.line_item_discounts (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id     UUID        NOT NULL REFERENCES app.merchants(id),
    line_item_id    UUID        NOT NULL REFERENCES sales.line_items(id),
    discount_name   TEXT,
    discount_cents  BIGINT      NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_line_item_discounts_line_item_id ON sales.line_item_discounts (line_item_id);

CREATE TABLE IF NOT EXISTS sales.refund_links (
    id                  UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id         UUID        NOT NULL REFERENCES app.merchants(id),
    refund_transaction_id UUID      NOT NULL REFERENCES sales.transactions(id),
    original_transaction_id UUID    NOT NULL REFERENCES sales.transactions(id),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_refund_links_merchant_id ON sales.refund_links (merchant_id);
CREATE INDEX IF NOT EXISTS idx_refund_links_original ON sales.refund_links (original_transaction_id);

CREATE TABLE IF NOT EXISTS sales.cash_drawer_shifts (
    id                  UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id         UUID        NOT NULL REFERENCES app.merchants(id),
    location_id         UUID        REFERENCES app.locations(id),
    employee_id         UUID        REFERENCES app.employees(id),
    external_id         TEXT        NOT NULL,
    opened_at           TIMESTAMPTZ NOT NULL,
    closed_at           TIMESTAMPTZ,
    expected_cents      BIGINT,
    actual_cents        BIGINT,
    discrepancy_cents   BIGINT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_cash_drawer_shifts_external UNIQUE (merchant_id, external_id)
);

CREATE INDEX IF NOT EXISTS idx_cash_drawer_shifts_merchant_id ON sales.cash_drawer_shifts (merchant_id);

CREATE TABLE IF NOT EXISTS sales.cash_drawer_events (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id     UUID        NOT NULL REFERENCES app.merchants(id),
    shift_id        UUID        NOT NULL REFERENCES sales.cash_drawer_shifts(id),
    employee_id     UUID        REFERENCES app.employees(id),
    event_type      TEXT        NOT NULL,
    amount_cents    BIGINT,
    occurred_at     TIMESTAMPTZ NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_cash_drawer_events_shift_id ON sales.cash_drawer_events (shift_id);
```

- [ ] **Step 8.2: Write 011_tsp_ingestion.up.sql**

```sql
-- 011_tsp_ingestion.up.sql
CREATE TABLE IF NOT EXISTS app.ingestion_log (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id     UUID        NOT NULL REFERENCES app.merchants(id),
    event_id        TEXT        NOT NULL UNIQUE,
    source_code     TEXT        REFERENCES app.source_systems(code),
    chain_hash      TEXT        NOT NULL,
    received_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    processed_at    TIMESTAMPTZ,
    stage           TEXT        NOT NULL DEFAULT 'seal'
                                CHECK (stage IN ('seal','parse','merkle','detect'))
);

CREATE INDEX IF NOT EXISTS idx_ingestion_log_merchant_id ON app.ingestion_log (merchant_id);
CREATE INDEX IF NOT EXISTS idx_ingestion_log_event_id ON app.ingestion_log (event_id);

CREATE TABLE IF NOT EXISTS app.merkle_batches (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id UUID        NOT NULL REFERENCES app.merchants(id),
    batch_id    TEXT        NOT NULL UNIQUE,
    root_hash   TEXT        NOT NULL,
    event_count INTEGER     NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_merkle_batches_merchant_id ON app.merkle_batches (merchant_id);

CREATE TABLE IF NOT EXISTS app.detection_rules (
    id                UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    rule_id           TEXT        NOT NULL UNIQUE,
    category          TEXT        NOT NULL,
    severity          TEXT        NOT NULL
                                  CHECK (severity IN ('critical','high','medium','low','info')),
    default_threshold NUMERIC,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_detection_rules_rule_id ON app.detection_rules (rule_id);

CREATE TABLE IF NOT EXISTS app.merchant_rule_config (
    id               UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id      UUID        NOT NULL REFERENCES app.merchants(id),
    rule_id          UUID        NOT NULL REFERENCES app.detection_rules(id),
    is_enabled       BOOLEAN     NOT NULL DEFAULT true,
    custom_threshold NUMERIC,
    notify_enabled   BOOLEAN     NOT NULL DEFAULT true,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_by       UUID,
    modified_by      UUID
);

CREATE INDEX IF NOT EXISTS idx_merchant_rule_config_merchant_id ON app.merchant_rule_config (merchant_id);

CREATE TABLE IF NOT EXISTS app.alerts (
    id           UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id  UUID        NOT NULL REFERENCES app.merchants(id),
    rule_id      UUID        NOT NULL REFERENCES app.detection_rules(id),
    severity     TEXT        NOT NULL CHECK (severity IN ('critical','high','medium','low','info')),
    status       TEXT        NOT NULL DEFAULT 'OPEN'
                             CHECK (status IN ('OPEN','ACKNOWLEDGED','INVESTIGATING','ESCALATED','DISMISSED')),
    source_table TEXT        NOT NULL,
    source_id    UUID        NOT NULL,
    employee_id  UUID        REFERENCES app.employees(id),
    location_id  UUID        REFERENCES app.locations(id),
    impact_cents BIGINT      NOT NULL DEFAULT 0,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_alerts_merchant_id ON app.alerts (merchant_id);
CREATE INDEX IF NOT EXISTS idx_alerts_merchant_status ON app.alerts (merchant_id, status);

CREATE TABLE IF NOT EXISTS app.alert_history (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    alert_id    UUID        NOT NULL REFERENCES app.alerts(id),
    actor_id    UUID        REFERENCES app.users(id),
    from_status TEXT,
    to_status   TEXT        NOT NULL,
    note        TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_alert_history_alert_id ON app.alert_history (alert_id);
```

- [ ] **Step 8.3: Write 012_fox_cases.up.sql**

```sql
-- 012_fox_cases.up.sql
CREATE TABLE IF NOT EXISTS app.fox_cases (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id     UUID        NOT NULL REFERENCES app.merchants(id),
    alert_id        UUID        REFERENCES app.alerts(id),
    status          TEXT        NOT NULL DEFAULT 'OPEN'
                                CHECK (status IN ('OPEN','ACTIVE','PENDING_REVIEW','CLOSED','ARCHIVED')),
    case_type       TEXT        NOT NULL,
    title           TEXT        NOT NULL,
    description     TEXT,
    assigned_to     UUID        REFERENCES app.users(id),
    opened_by       UUID        REFERENCES app.users(id),
    closed_at       TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_fox_cases_merchant_id ON app.fox_cases (merchant_id);
CREATE INDEX IF NOT EXISTS idx_fox_cases_merchant_status ON app.fox_cases (merchant_id, status);

CREATE TABLE IF NOT EXISTS app.fox_subjects (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id UUID        NOT NULL REFERENCES app.merchants(id),
    case_id     UUID        NOT NULL REFERENCES app.fox_cases(id),
    name        TEXT        NOT NULL,
    entity_id   UUID,
    entity_type TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_fox_subjects_case_id ON app.fox_subjects (case_id);

CREATE TABLE IF NOT EXISTS app.fox_timeline (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id UUID        NOT NULL REFERENCES app.merchants(id),
    case_id     UUID        NOT NULL REFERENCES app.fox_cases(id),
    actor_id    UUID        REFERENCES app.users(id),
    event_type  TEXT        NOT NULL,
    description TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_fox_timeline_case_id ON app.fox_timeline (case_id);
```

- [ ] **Step 8.4: Write 013_fox_evidence_chain.up.sql**

```sql
-- 013_fox_evidence_chain.up.sql
-- Evidence records are append-only. The trigger below enforces this at the DB level.
CREATE TABLE IF NOT EXISTS app.fox_evidence (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id     UUID        NOT NULL REFERENCES app.merchants(id),
    case_id         UUID        NOT NULL REFERENCES app.fox_cases(id),
    record_type     TEXT        NOT NULL,
    record_payload  JSONB       NOT NULL,
    chain_hash      TEXT        NOT NULL,
    uploaded_by     TEXT,
    file_path       TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_fox_evidence_case_id ON app.fox_evidence (case_id);
CREATE INDEX IF NOT EXISTS idx_fox_evidence_merchant_id ON app.fox_evidence (merchant_id);

CREATE TABLE IF NOT EXISTS app.fox_evidence_access_log (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    evidence_id UUID        NOT NULL REFERENCES app.fox_evidence(id),
    accessed_by TEXT        NOT NULL,
    ip_address  TEXT,
    accessed_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_fox_evidence_access_log_evidence_id ON app.fox_evidence_access_log (evidence_id);

-- Immutability trigger: UPDATE and DELETE on fox_evidence are prohibited.
CREATE OR REPLACE FUNCTION app.fox_evidence_immutable()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'fox_evidence is append-only — UPDATE and DELETE are prohibited';
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_fox_evidence_immutable ON app.fox_evidence;
CREATE TRIGGER trg_fox_evidence_immutable
    BEFORE UPDATE OR DELETE ON app.fox_evidence
    FOR EACH ROW EXECUTE FUNCTION app.fox_evidence_immutable();
```

---

### Task 9: Seed migration and verify all migrations

**Files:**
- Create: `CanaryGo/deploy/migrations/014_seed_roles_source_systems.up.sql`

- [ ] **Step 9.1: Write 014_seed_roles_source_systems.up.sql**

```sql
-- 014_seed_roles_source_systems.up.sql
INSERT INTO app.roles (role_name, description)
VALUES
    ('admin',    'Platform administrator — full access'),
    ('owner',    'Merchant owner — full tenant access'),
    ('manager',  'Store manager — operational access'),
    ('operator', 'Store operator — transaction and alert access'),
    ('member',   'Team member — read-only operational'),
    ('viewer',   'Read-only viewer')
ON CONFLICT (role_name) DO NOTHING;

INSERT INTO app.source_systems (code, display_name, category)
VALUES
    ('square',       'Square',             'POS'),
    ('counterpoint', 'NCR Counterpoint',   'POS'),
    ('clover',       'Clover',             'POS')
ON CONFLICT (code) DO NOTHING;
```

- [ ] **Step 9.2: Apply all 14 migrations**

```bash
cd ~/GrowDirect/CanaryGo
DATABASE_URL="postgres://growdirect:growdirect_dev@localhost:5432/canary_go?sslmode=disable"
migrate -path=deploy/migrations -database="$DATABASE_URL" up
```

Expected: 14 lines like `N/u <name> (Xms)` with no errors. Final line: `no change`.

- [ ] **Step 9.3: Verify tables exist**

```bash
psql -h localhost -U growdirect -d canary_go \
  -c "\dt app.*" \
  -c "\dt sales.*" \
  -c "\dt metrics.*"
```

Expected: ~30+ tables in `app`, 6 tables in `sales`, 0 in `metrics` (no metrics migrations yet).

- [ ] **Step 9.4: Verify seed data**

```bash
psql -h localhost -U growdirect -d canary_go \
  -c "SELECT role_name FROM app.roles ORDER BY role_name;" \
  -c "SELECT code FROM app.source_systems ORDER BY code;"
```

Expected: 6 roles (admin, member, manager, operator, owner, viewer), 3 source systems (clover, counterpoint, square).

- [ ] **Step 9.5: Verify fox immutability trigger**

```bash
psql -h localhost -U growdirect -d canary_go -c "
SELECT trigger_name, event_manipulation
FROM information_schema.triggers
WHERE trigger_name = 'trg_fox_evidence_immutable';
"
```

Expected: two rows — one for UPDATE, one for DELETE.

- [ ] **Step 9.6: Apply migrations to test DB**

```bash
DATABASE_URL="postgres://growdirect:growdirect_dev@localhost:5432/canary_go_test?sslmode=disable"
migrate -path=deploy/migrations -database="$DATABASE_URL" up
```

Expected: same 14 lines as above.

- [ ] **Step 9.7: Commit all migrations**

```bash
cd ~/GrowDirect
git add CanaryGo/deploy/migrations/
git commit -m "feat(canarygo): 14 DDL migrations — CRDM, identity, multi-POS substrate, fox evidence chain"
```

---

## Chunk 3: sqlc Config + Internal Packages

**Files:**
- Create: `CanaryGo/sqlc.yaml`
- Create: `CanaryGo/internal/db/sqlc/identity.sql`
- Create: `CanaryGo/internal/db/sqlc/tsp.sql`
- Create: `CanaryGo/internal/config/config.go`
- Create: `CanaryGo/internal/db/db.go`
- Create: `CanaryGo/internal/crdm/types.go`
- Create: `CanaryGo/internal/arts/constants.go`
- Create: `CanaryGo/internal/auth/jwt.go`
- Create: `CanaryGo/internal/auth/middleware.go`
- Create: `CanaryGo/internal/tenant/middleware.go`
- Create: `CanaryGo/internal/pagination/pagination.go`
- Create: `CanaryGo/internal/testutil/db.go`

---

### Task 10: sqlc configuration and seed queries

**Files:**
- Create: `CanaryGo/sqlc.yaml`
- Create: `CanaryGo/internal/db/sqlc/identity.sql`
- Create: `CanaryGo/internal/db/sqlc/tsp.sql`

- [ ] **Step 10.1: Write sqlc.yaml**

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

- [ ] **Step 10.2: Write internal/db/sqlc/identity.sql**

These are the minimal queries needed by M1. Each query must include the sqlc annotation comment.

```sql
-- internal/db/sqlc/identity.sql

-- name: GetMerchantByID :one
SELECT id, organization_id, source_merchant_id, merchant_name, currency, is_active,
       created_at, updated_at
FROM app.merchants
WHERE id = $1;

-- name: GetMerchantBySourceID :one
SELECT id, organization_id, source_merchant_id, merchant_name, currency, is_active,
       created_at, updated_at
FROM app.merchants
WHERE source_merchant_id = $1;

-- name: GetUserByEmail :one
SELECT id, merchant_id, username, email, display_name, is_active, last_login_at,
       created_at, updated_at
FROM app.users
WHERE merchant_id = $1 AND email = $2 AND db_status = 'active';

-- name: GetUserByID :one
SELECT id, merchant_id, username, email, display_name, is_active, last_login_at,
       created_at, updated_at
FROM app.users
WHERE id = $1 AND db_status = 'active';

-- name: GetUserRoles :many
SELECT r.role_name
FROM app.user_roles ur
JOIN app.roles r ON r.id = ur.role_id
WHERE ur.user_id = $1 AND ur.merchant_id = $2;

-- name: CreateOrganization :one
INSERT INTO app.organizations (org_name, subscription_tier)
VALUES ($1, $2)
RETURNING id, org_name, subscription_tier, is_active, created_at, updated_at;

-- name: CreateMerchant :one
INSERT INTO app.merchants (organization_id, source_merchant_id, merchant_name, currency)
VALUES ($1, $2, $3, $4)
RETURNING id, organization_id, source_merchant_id, merchant_name, currency, is_active,
          created_at, updated_at;

-- name: CreateUser :one
INSERT INTO app.users (merchant_id, username, email, display_name)
VALUES ($1, $2, $3, $4)
RETURNING id, merchant_id, username, email, display_name, is_active, created_at, updated_at;

-- name: UpdateUserLastLogin :exec
UPDATE app.users
SET last_login_at = now(), updated_at = now()
WHERE id = $1;
```

- [ ] **Step 10.3: Write internal/db/sqlc/tsp.sql**

Minimal queries for M1 (TSP service is a stub in M1, but sqlc.yaml references this file and it must exist and parse).

```sql
-- internal/db/sqlc/tsp.sql

-- name: InsertIngestionLog :one
INSERT INTO app.ingestion_log (merchant_id, event_id, source_code, chain_hash, stage)
VALUES ($1, $2, $3, $4, $5)
RETURNING id, merchant_id, event_id, source_code, chain_hash, received_at, stage;

-- name: GetIngestionLogByEventID :one
SELECT id, merchant_id, event_id, source_code, chain_hash, received_at, processed_at, stage
FROM app.ingestion_log
WHERE event_id = $1;

-- name: InsertTransaction :one
INSERT INTO sales.transactions (
    merchant_id, external_id, location_id, employee_id,
    arts_business_date, transaction_type, total_cents,
    subtotal_cents, tax_cents, tender_type, source_code
)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
RETURNING id, merchant_id, external_id, arts_business_date, total_cents, created_at;
```

- [ ] **Step 10.4: Run sqlc generate**

```bash
cd ~/GrowDirect/CanaryGo
sqlc generate
```

Expected: exits 0, no output. Two generated packages appear:
- `internal/db/query/identity/` with `db.go`, `models.go`, `query.sql.go`
- `internal/db/query/tsp/` with the same three files

- [ ] **Step 10.5: Verify generated code compiles**

```bash
go build ./internal/db/query/...
```

Expected: exits 0. If `vector` type causes errors, verify the `overrides` stanza in sqlc.yaml is present on the affected sql block.

- [ ] **Step 10.6: Commit**

```bash
cd ~/GrowDirect
git add CanaryGo/sqlc.yaml CanaryGo/internal/db/
git commit -m "feat(canarygo): sqlc v2 config + seed queries for identity and tsp"
```

---

### Task 11: internal/config

**Files:**
- Create: `CanaryGo/internal/config/config.go`

- [ ] **Step 11.1: Write config.go**

```go
// internal/config/config.go
package config

import (
	"fmt"
	"os"
)

type Config struct {
	DatabaseURL           string
	ValkeyURL             string
	InternalServiceSecret string
	SessionSecret         string
	LogLevel              string
	Port                  string
	ServiceName           string
}

// Load reads required environment variables and panics on missing ones.
// Call at service startup before any other initialization.
func Load(serviceName string) *Config {
	cfg := &Config{
		DatabaseURL:           require("DATABASE_URL"),
		ValkeyURL:             require("VALKEY_URL"),
		InternalServiceSecret: require("INTERNAL_SERVICE_SECRET"),
		SessionSecret:         require("SESSION_SECRET"),
		LogLevel:              getOr("LOG_LEVEL", "info"),
		Port:                  getOr("PORT", "8080"),
		ServiceName:           serviceName,
	}
	return cfg
}

func require(key string) string {
	v := os.Getenv(key)
	if v == "" {
		panic(fmt.Sprintf("required environment variable %s is not set", key))
	}
	return v
}

func getOr(key, def string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return def
}
```

- [ ] **Step 11.2: Verify it compiles**

```bash
cd ~/GrowDirect/CanaryGo
go build ./internal/config/
```

Expected: exits 0.

- [ ] **Step 11.3: Commit**

```bash
cd ~/GrowDirect
git add CanaryGo/internal/config/
git commit -m "feat(canarygo): config package with fail-fast env loader"
```

---

### Task 12: internal/db (connection pool)

**Files:**
- Create: `CanaryGo/internal/db/db.go`

- [ ] **Step 12.1: Write db.go**

```go
// internal/db/db.go
package db

import (
	"context"
	"fmt"

	"github.com/jackc/pgx/v5/pgxpool"
)

// Connect creates a pgxpool from the given DATABASE_URL and verifies connectivity.
// Returns the pool; caller is responsible for pool.Close().
func Connect(ctx context.Context, databaseURL string) (*pgxpool.Pool, error) {
	config, err := pgxpool.ParseConfig(databaseURL)
	if err != nil {
		return nil, fmt.Errorf("db: parse config: %w", err)
	}

	pool, err := pgxpool.NewWithConfig(ctx, config)
	if err != nil {
		return nil, fmt.Errorf("db: create pool: %w", err)
	}

	if err := pool.Ping(ctx); err != nil {
		pool.Close()
		return nil, fmt.Errorf("db: ping: %w", err)
	}

	return pool, nil
}
```

- [ ] **Step 12.2: Verify it compiles**

```bash
cd ~/GrowDirect/CanaryGo
go build ./internal/db/
```

Expected: exits 0.

- [ ] **Step 12.3: Commit**

```bash
cd ~/GrowDirect
git add CanaryGo/internal/db/db.go
git commit -m "feat(canarygo): db package with pgxpool Connect helper"
```

---

### Task 13: internal/crdm, arts, tenant, pagination

These packages are structural — they compile as stubs in M1. Domain logic fills in at M2+.

**Files:**
- Create: `CanaryGo/internal/crdm/types.go`
- Create: `CanaryGo/internal/arts/constants.go`
- Create: `CanaryGo/internal/tenant/middleware.go`
- Create: `CanaryGo/internal/pagination/pagination.go`

- [ ] **Step 13.1: Write internal/crdm/types.go**

```go
// internal/crdm/types.go
// Canonical Retail Data Model — ARTS POSLOG-aligned Go types.
// All services use these types for cross-service data contracts.
// Do not define competing structs in service packages.
package crdm

import (
	"time"

	"github.com/google/uuid"
)

type Merchant struct {
	ID               uuid.UUID
	OrganizationID   uuid.UUID
	SourceMerchantID string
	MerchantName     string
	Currency         string
	IsActive         bool
	CreatedAt        time.Time
	UpdatedAt        time.Time
}

type Location struct {
	ID               uuid.UUID
	MerchantID       uuid.UUID
	SourceLocationID string
	LocationName     string
	City             string
	State            string
	IsActive         bool
}

type Employee struct {
	ID               uuid.UUID
	MerchantID       uuid.UUID
	SourceEmployeeID string
	EmployeeName     string
	RiskScore        float64
	IsActive         bool
}

type TransactionHeader struct {
	ID                  uuid.UUID
	MerchantID          uuid.UUID
	ExternalID          string
	ARTSBusinessDate    time.Time
	ARTSWorkstationID   string
	TransactionType     string
	TotalCents          int64
	SubtotalCents       int64
	TaxCents            int64
	TipCents            int64
	DiscountCents       int64
	TenderType          string
	SourceCode          string
}

type User struct {
	ID          uuid.UUID
	MerchantID  uuid.UUID
	Username    string
	Email       string
	DisplayName string
	IsActive    bool
	Roles       []string
}
```

- [ ] **Step 13.2: Write internal/arts/constants.go**

```go
// internal/arts/constants.go
// ARTS POSLOG field constants used across all transaction parsing.
package arts

const (
	TransactionTypeSale   = "SALE"
	TransactionTypeRefund = "REFUND"
	TransactionTypeVoid   = "VOID"

	TenderTypeCash        = "CASH"
	TenderTypeCard        = "CARD"
	TenderTypeGiftCard    = "GIFT_CARD"
	TenderTypeOther       = "OTHER"

	SourceSquare       = "square"
	SourceCounterpoint = "counterpoint"
	SourceClover       = "clover"
)
```

- [ ] **Step 13.3: Write internal/tenant/middleware.go**

```go
// internal/tenant/middleware.go
package tenant

import (
	"context"
	"net/http"

	"github.com/google/uuid"
)

type contextKey string

const merchantIDKey contextKey = "merchant_id"

// FromContext retrieves the merchant_id injected by the auth middleware.
func FromContext(ctx context.Context) (uuid.UUID, bool) {
	v, ok := ctx.Value(merchantIDKey).(uuid.UUID)
	return v, ok
}

// InjectMerchantID is called by auth middleware after JWT validation.
func InjectMerchantID(ctx context.Context, id uuid.UUID) context.Context {
	return context.WithValue(ctx, merchantIDKey, id)
}

// RequireMerchant returns 401 if no merchant_id is in context.
func RequireMerchant(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if _, ok := FromContext(r.Context()); !ok {
			http.Error(w, `{"error":"unauthorized"}`, http.StatusUnauthorized)
			return
		}
		next.ServeHTTP(w, r)
	})
}
```

- [ ] **Step 13.4: Write internal/pagination/pagination.go**

```go
// internal/pagination/pagination.go
package pagination

import (
	"net/http"
	"strconv"
)

const defaultLimit = 50
const maxLimit = 200

type Params struct {
	Limit  int
	Offset int
}

func FromRequest(r *http.Request) Params {
	limit := defaultLimit
	offset := 0

	if l := r.URL.Query().Get("limit"); l != "" {
		if v, err := strconv.Atoi(l); err == nil && v > 0 && v <= maxLimit {
			limit = v
		}
	}
	if o := r.URL.Query().Get("offset"); o != "" {
		if v, err := strconv.Atoi(o); err == nil && v >= 0 {
			offset = v
		}
	}
	return Params{Limit: limit, Offset: offset}
}
```

- [ ] **Step 13.5: Write internal/testutil/db.go**

```go
// internal/testutil/db.go
package testutil

import (
	"context"
	"os"
	"testing"

	"github.com/jackc/pgx/v5/pgxpool"
)

// MustConnect connects to the test database from DATABASE_URL env var.
// Calls t.Fatal if connection fails. Returns the pool; caller should defer pool.Close().
func MustConnect(t *testing.T) *pgxpool.Pool {
	t.Helper()
	url := os.Getenv("DATABASE_URL")
	if url == "" {
		t.Fatal("testutil: DATABASE_URL not set — run tests via 'make test'")
	}
	pool, err := pgxpool.New(context.Background(), url)
	if err != nil {
		t.Fatalf("testutil: connect: %v", err)
	}
	if err := pool.Ping(context.Background()); err != nil {
		t.Fatalf("testutil: ping: %v", err)
	}
	t.Cleanup(pool.Close)
	return pool
}

// TruncateTables truncates the given schema-qualified tables within a transaction.
// Use in test setup to ensure a clean state. Does NOT truncate fox_evidence (append-only).
func TruncateTables(t *testing.T, pool *pgxpool.Pool, tables ...string) {
	t.Helper()
	ctx := context.Background()
	for _, table := range tables {
		if _, err := pool.Exec(ctx, "TRUNCATE TABLE "+table+" CASCADE"); err != nil {
			t.Fatalf("testutil: truncate %s: %v", table, err)
		}
	}
}
```

- [ ] **Step 13.6: Verify all packages compile**

```bash
cd ~/GrowDirect/CanaryGo
go build ./internal/...
```

Expected: exits 0.

- [ ] **Step 13.7: Commit**

```bash
cd ~/GrowDirect
git add CanaryGo/internal/crdm/ CanaryGo/internal/arts/ \
        CanaryGo/internal/tenant/ CanaryGo/internal/pagination/ \
        CanaryGo/internal/testutil/
git commit -m "feat(canarygo): internal packages — crdm, arts, tenant, pagination, testutil"
```

---

### Task 14: internal/auth (JWT)

**Files:**
- Create: `CanaryGo/internal/auth/jwt.go`
- Create: `CanaryGo/internal/auth/middleware.go`
- Create: `CanaryGo/internal/auth/jwt_test.go`

- [ ] **Step 14.1: Write the failing test first**

```go
// internal/auth/jwt_test.go
package auth_test

import (
	"testing"
	"time"

	"github.com/google/uuid"
	"github.com/growdirect-llc/rapidpos/internal/auth"
)

func TestSignAndVerifyClaims(t *testing.T) {
	secret := "test-secret-at-least-32-bytes-long!!"
	merchantID := uuid.New()
	userID := uuid.New()
	roles := []string{"owner", "manager"}

	token, err := auth.SignToken(secret, merchantID, userID, roles, 8*time.Hour)
	if err != nil {
		t.Fatalf("SignToken: %v", err)
	}
	if token == "" {
		t.Fatal("expected non-empty token")
	}

	claims, err := auth.VerifyToken(secret, token)
	if err != nil {
		t.Fatalf("VerifyToken: %v", err)
	}
	if claims.MerchantID != merchantID {
		t.Errorf("MerchantID: got %v want %v", claims.MerchantID, merchantID)
	}
	if claims.UserID != userID {
		t.Errorf("UserID: got %v want %v", claims.UserID, userID)
	}
	if len(claims.Roles) != 2 {
		t.Errorf("Roles: got %v want %v", claims.Roles, roles)
	}
}

func TestExpiredToken(t *testing.T) {
	secret := "test-secret-at-least-32-bytes-long!!"
	token, _ := auth.SignToken(secret, uuid.New(), uuid.New(), []string{"owner"}, -1*time.Second)

	_, err := auth.VerifyToken(secret, token)
	if err == nil {
		t.Fatal("expected error for expired token, got nil")
	}
}

func TestInvalidSignature(t *testing.T) {
	token, _ := auth.SignToken("secret-a-at-least-32-bytes-long!!", uuid.New(), uuid.New(), nil, time.Hour)
	_, err := auth.VerifyToken("secret-b-at-least-32-bytes-long!!", token)
	if err == nil {
		t.Fatal("expected error for wrong secret, got nil")
	}
}
```

- [ ] **Step 14.2: Run test — expect failure**

```bash
cd ~/GrowDirect/CanaryGo
go test ./internal/auth/ -v
```

Expected: compilation error — `auth` package does not exist yet.

- [ ] **Step 14.3: Write internal/auth/jwt.go**

```go
// internal/auth/jwt.go
package auth

import (
	"crypto/sha256"
	"fmt"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"github.com/google/uuid"
)

type Claims struct {
	MerchantID uuid.UUID `json:"merchant_id"`
	UserID     uuid.UUID `json:"user_id"`
	Roles      []string  `json:"roles"`
	jwt.RegisteredClaims
}

// SignToken creates a signed JWT for the given principal.
func SignToken(secret string, merchantID, userID uuid.UUID, roles []string, ttl time.Duration) (string, error) {
	claims := Claims{
		MerchantID: merchantID,
		UserID:     userID,
		Roles:      roles,
		RegisteredClaims: jwt.RegisteredClaims{
			IssuedAt:  jwt.NewNumericDate(time.Now()),
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(ttl)),
		},
	}
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString([]byte(secret))
}

// VerifyToken parses and validates a JWT. Returns Claims on success.
func VerifyToken(secret, tokenStr string) (*Claims, error) {
	token, err := jwt.ParseWithClaims(tokenStr, &Claims{}, func(t *jwt.Token) (interface{}, error) {
		if _, ok := t.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("unexpected signing method: %v", t.Header["alg"])
		}
		return []byte(secret), nil
	})
	if err != nil {
		return nil, err
	}
	claims, ok := token.Claims.(*Claims)
	if !ok || !token.Valid {
		return nil, fmt.Errorf("invalid token")
	}
	return claims, nil
}

// TokenHash returns SHA-256 hex of a token string — used as Valkey key suffix.
func TokenHash(token string) string {
	h := sha256.Sum256([]byte(token))
	return fmt.Sprintf("%x", h)
}
```

- [ ] **Step 14.4: Write internal/auth/middleware.go**

```go
// internal/auth/middleware.go
package auth

import (
	"net/http"
	"strings"

	"github.com/growdirect-llc/rapidpos/internal/tenant"
)

// BearerMiddleware extracts the Authorization Bearer token, verifies it, and
// injects merchant_id into context. Returns 401 on missing or invalid token.
func BearerMiddleware(sessionSecret string) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			header := r.Header.Get("Authorization")
			if !strings.HasPrefix(header, "Bearer ") {
				http.Error(w, `{"error":"missing_token"}`, http.StatusUnauthorized)
				return
			}
			tokenStr := strings.TrimPrefix(header, "Bearer ")
			claims, err := VerifyToken(sessionSecret, tokenStr)
			if err != nil {
				http.Error(w, `{"error":"invalid_token"}`, http.StatusUnauthorized)
				return
			}
			ctx := tenant.InjectMerchantID(r.Context(), claims.MerchantID)
			next.ServeHTTP(w, r.WithContext(ctx))
		})
	}
}
```

- [ ] **Step 14.5: Run test — expect pass**

```bash
cd ~/GrowDirect/CanaryGo
go test ./internal/auth/ -v
```

Expected: `PASS` for all three test cases (SignAndVerify, Expired, InvalidSignature).

- [ ] **Step 14.6: Commit**

```bash
cd ~/GrowDirect
git add CanaryGo/internal/auth/
git commit -m "feat(canarygo): auth package — JWT sign/verify, bearer middleware"
```

---

## Chunk 4: Identity Service + All Service Stubs

**Files:**
- Create: `CanaryGo/cmd/identity/main.go`
- Create: `CanaryGo/cmd/identity/server.go`
- Create: `CanaryGo/cmd/identity/handlers.go`
- Create: `CanaryGo/cmd/identity/main_test.go`
- Create: `CanaryGo/cmd/<all-other-services>/main.go` (19 stubs)

---

### Task 15: Identity service — write tests first (TDD)

**Files:**
- Create: `CanaryGo/cmd/identity/main_test.go`

- [ ] **Step 15.1: Write integration tests**

```go
// cmd/identity/main_test.go
package main_test

import (
	"bytes"
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"os"
	"strings"
	"testing"
	"time"

	"github.com/google/uuid"
	"github.com/growdirect-llc/rapidpos/internal/auth"
	"github.com/growdirect-llc/rapidpos/internal/config"
	"github.com/growdirect-llc/rapidpos/internal/db"
	"github.com/redis/go-redis/v9"
)

func testServer(t *testing.T) http.Handler {
	t.Helper()
	cfg := config.Load("canary-identity")
	pool, err := db.Connect(context.Background(), cfg.DatabaseURL)
	if err != nil {
		t.Fatalf("db connect: %v", err)
	}
	t.Cleanup(pool.Close)

	rdb := redis.NewClient(&redis.Options{Addr: parseValkeyAddr(cfg.ValkeyURL)})
	t.Cleanup(func() { rdb.Close() })

	return NewServer(pool, rdb, cfg)
}

func TestHealthEndpoint(t *testing.T) {
	srv := testServer(t)
	req := httptest.NewRequest(http.MethodGet, "/health", nil)
	w := httptest.NewRecorder()
	srv.ServeHTTP(w, req)

	if w.Code != http.StatusOK {
		t.Fatalf("health: got %d want 200", w.Code)
	}

	var resp map[string]interface{}
	if err := json.NewDecoder(w.Body).Decode(&resp); err != nil {
		t.Fatalf("decode health: %v", err)
	}
	if resp["ok"] != true {
		t.Errorf("health.ok: got %v want true", resp["ok"])
	}
	checks, _ := resp["checks"].(map[string]interface{})
	if checks["database"] != "ok" {
		t.Errorf("health.checks.database: got %v want ok", checks["database"])
	}
}

func TestSessionValidate_MissingBody(t *testing.T) {
	srv := testServer(t)
	req := httptest.NewRequest(http.MethodPost, "/sessions/validate", nil)
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()
	srv.ServeHTTP(w, req)

	if w.Code != http.StatusUnauthorized {
		t.Fatalf("validate missing: got %d want 401", w.Code)
	}
}

func TestSessionValidate_ExpiredToken(t *testing.T) {
	srv := testServer(t)
	cfg := config.Load("canary-identity")

	token, _ := auth.SignToken(cfg.SessionSecret, uuid.New(), uuid.New(), []string{"owner"}, -1*time.Second)

	body, _ := json.Marshal(map[string]string{"token": token})
	req := httptest.NewRequest(http.MethodPost, "/sessions/validate", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()
	srv.ServeHTTP(w, req)

	if w.Code != http.StatusUnauthorized {
		t.Fatalf("expired: got %d want 401", w.Code)
	}
}

func TestSessionValidate_ValidToken_NotInValkey(t *testing.T) {
	srv := testServer(t)
	cfg := config.Load("canary-identity")

	// A cryptographically valid JWT that was never registered in Valkey
	token, _ := auth.SignToken(cfg.SessionSecret, uuid.New(), uuid.New(), []string{"owner"}, time.Hour)

	body, _ := json.Marshal(map[string]string{"token": token})
	req := httptest.NewRequest(http.MethodPost, "/sessions/validate", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()
	srv.ServeHTTP(w, req)

	// Valid JWT but no Valkey session = invalid (revocation check)
	if w.Code != http.StatusUnauthorized {
		t.Fatalf("valid-jwt-no-valkey: got %d want 401", w.Code)
	}
}

// parseValkeyAddr extracts host:port from a redis:// URL.
// Handles redis://host:port/db format.
func parseValkeyAddr(url string) string {
	url = strings.TrimPrefix(url, "redis://")
	parts := strings.SplitN(url, "/", 2)
	return parts[0]
}
```


- [ ] **Step 15.2: Run tests — expect compile failure**

```bash
cd ~/GrowDirect/CanaryGo
DATABASE_URL="postgres://growdirect:growdirect_dev@localhost:5432/canary_go_test?sslmode=disable" \
VALKEY_URL="redis://localhost:6379/2" \
SESSION_SECRET="test-session-secret-at-least-32-bytes!" \
INTERNAL_SERVICE_SECRET="test-internal-secret" \
go test ./cmd/identity/ -v
```

Expected: compile failure — `NewServer not defined`.

---

### Task 16: Identity service implementation

**Files:**
- Create: `CanaryGo/cmd/identity/server.go`
- Create: `CanaryGo/cmd/identity/handlers.go`
- Create: `CanaryGo/cmd/identity/main.go`

- [ ] **Step 16.1: Write cmd/identity/server.go**

```go
// cmd/identity/server.go
package main

import (
	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/growdirect-llc/rapidpos/internal/config"
	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/redis/go-redis/v9"
	"net/http"
)

// NewServer wires the Chi router and all routes.
// Accepts injected dependencies so tests can pass a test DB and Valkey client.
func NewServer(pool *pgxpool.Pool, rdb *redis.Client, cfg *config.Config) http.Handler {
	r := chi.NewRouter()
	r.Use(middleware.RealIP)
	r.Use(middleware.Logger)
	r.Use(middleware.Recoverer)

	h := &handlers{pool: pool, rdb: rdb, cfg: cfg}

	r.Get("/health", h.health)
	r.Post("/sessions/validate", h.sessionsValidate)

	// Stubs — wired so callers don't get 404; returns 501 until M2
	r.Post("/merchants", stub)
	r.Get("/merchants/{id}", stub)
	r.Patch("/merchants/{id}", stub)
	r.Post("/oauth/authorize", stub)
	r.Get("/oauth/callback", stub)
	r.Post("/oauth/refresh", stub)
	r.Delete("/oauth/disconnect", stub)
	r.Post("/sessions", stub)
	r.Delete("/sessions/{token}", stub)
	r.Post("/users", stub)
	r.Get("/users/{id}", stub)
	r.Patch("/users/{id}", stub)

	return r
}

func stub(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusNotImplemented)
	w.Write([]byte(`{"error":"not_implemented"}`))
}
```

- [ ] **Step 16.2: Write cmd/identity/handlers.go**

```go
// cmd/identity/handlers.go
package main

import (
	"context"
	"crypto/sha256"
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/growdirect-llc/rapidpos/internal/auth"
	"github.com/growdirect-llc/rapidpos/internal/config"
	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/redis/go-redis/v9"
)

type handlers struct {
	pool *pgxpool.Pool
	rdb  *redis.Client
	cfg  *config.Config
}

type healthResponse struct {
	OK      bool              `json:"ok"`
	Service string            `json:"service"`
	Version string            `json:"version"`
	Checks  map[string]string `json:"checks"`
}

func (h *handlers) health(w http.ResponseWriter, r *http.Request) {
	checks := map[string]string{
		"database": "ok",
		"valkey":   "ok",
	}
	statusCode := http.StatusOK

	if err := h.pool.Ping(r.Context()); err != nil {
		checks["database"] = "error: " + err.Error()
		statusCode = http.StatusServiceUnavailable
	}
	if err := h.rdb.Ping(r.Context()).Err(); err != nil {
		checks["valkey"] = "error: " + err.Error()
		statusCode = http.StatusServiceUnavailable
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(statusCode)
	json.NewEncoder(w).Encode(healthResponse{
		OK:      statusCode == http.StatusOK,
		Service: h.cfg.ServiceName,
		Version: "1.0.0",
		Checks:  checks,
	})
}

type validateRequest struct {
	Token string `json:"token"`
}

type validateResponse struct {
	Valid      bool     `json:"valid"`
	MerchantID string   `json:"merchant_id,omitempty"`
	UserID     string   `json:"user_id,omitempty"`
	Roles      []string `json:"roles,omitempty"`
}

func (h *handlers) sessionsValidate(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	var req validateRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil || req.Token == "" {
		w.WriteHeader(http.StatusUnauthorized)
		json.NewEncoder(w).Encode(validateResponse{Valid: false})
		return
	}

	claims, err := auth.VerifyToken(h.cfg.SessionSecret, req.Token)
	if err != nil {
		w.WriteHeader(http.StatusUnauthorized)
		json.NewEncoder(w).Encode(validateResponse{Valid: false})
		return
	}

	// Revocation check — token must exist in Valkey
	key := fmt.Sprintf("session:%x", sha256.Sum256([]byte(req.Token)))
	if exists, err := h.rdb.Exists(context.Background(), key).Result(); err != nil || exists == 0 {
		w.WriteHeader(http.StatusUnauthorized)
		json.NewEncoder(w).Encode(validateResponse{Valid: false})
		return
	}

	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(validateResponse{
		Valid:      true,
		MerchantID: claims.MerchantID.String(),
		UserID:     claims.UserID.String(),
		Roles:      claims.Roles,
	})
}
```

- [ ] **Step 16.3: Write cmd/identity/main.go**

```go
// cmd/identity/main.go
package main

import (
	"context"
	"net/http"
	"strings"

	"github.com/growdirect-llc/rapidpos/internal/config"
	"github.com/growdirect-llc/rapidpos/internal/db"
	"github.com/redis/go-redis/v9"
	"go.uber.org/zap"
)

func main() {
	cfg := config.Load("canary-identity")

	logger, _ := zap.NewProduction()
	defer logger.Sync()

	pool, err := db.Connect(context.Background(), cfg.DatabaseURL)
	if err != nil {
		logger.Fatal("db connect", zap.Error(err))
	}
	defer pool.Close()

	rdb := redis.NewClient(&redis.Options{
		Addr: parseValkeyAddr(cfg.ValkeyURL),
		DB:   2,
	})
	defer rdb.Close()

	srv := NewServer(pool, rdb, cfg)
	addr := ":" + cfg.Port
	logger.Info("starting", zap.String("service", cfg.ServiceName), zap.String("addr", addr))
	if err := http.ListenAndServe(addr, srv); err != nil {
		logger.Fatal("listen", zap.Error(err))
	}
}

func parseValkeyAddr(url string) string {
	url = strings.TrimPrefix(url, "redis://")
	parts := strings.SplitN(url, "/", 2)
	return parts[0]
}

// parseValkeyDB is unused at startup (DB=2 hardcoded) but available for test helpers.
func parseValkeyDB(valkeyURL string) int {
	// Always DB 2 for Canary Go. Clean-break from Python (DB 0) and Cove (DB 1).
	return 2
}
```

- [ ] **Step 16.4: Run identity tests — expect pass**

```bash
cd ~/GrowDirect/CanaryGo
DATABASE_URL="postgres://growdirect:growdirect_dev@localhost:5432/canary_go_test?sslmode=disable" \
VALKEY_URL="redis://localhost:6379/2" \
SESSION_SECRET="test-session-secret-at-least-32-bytes!" \
INTERNAL_SERVICE_SECRET="test-internal-secret" \
go test ./cmd/identity/ -v
```

Expected: `PASS` for all four tests (health, missing body, expired token, valid-jwt-no-valkey).

- [ ] **Step 16.5: Build identity binary**

```bash
cd ~/GrowDirect/CanaryGo
go build -o bin/identity ./cmd/identity
```

Expected: exits 0, `bin/identity` created.

- [ ] **Step 16.6: Commit**

```bash
cd ~/GrowDirect
git add CanaryGo/cmd/identity/
git commit -m "feat(canarygo): identity service — /health + /sessions/validate, all stubs wired"
```

---

### Task 17: Boot identity in Docker

- [ ] **Step 17.1: Build and start**

```bash
cd ~/GrowDirect/CanaryGo
docker compose -f deploy/docker-compose.yml up --build canarygo-identity -d
```

Expected: image builds (may take 1-2 min first time), container starts.

- [ ] **Step 17.2: Verify /health**

```bash
curl -s http://localhost:8086/health | python3 -m json.tool
```

Expected:
```json
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

If `"ok": false` — check `docker compose logs canarygo-identity` for the failing check.

- [ ] **Step 17.3: Verify /sessions/validate returns 401 on empty body**

```bash
curl -s -X POST http://localhost:8086/sessions/validate \
     -H "Content-Type: application/json" \
     -d '{}'
```

Expected: `{"valid":false}`

- [ ] **Step 17.4: Commit container verification note**

```bash
cd ~/GrowDirect
git commit --allow-empty -m "chore(canarygo): identity service verified running in Docker — curl :8086/health → ok"
```

---

### Task 18: All remaining service stubs

Each of the 18 remaining services (tsp, gateway, chirp, alert, fox, owl, analytics, hawk, bull, asset, item, inventory, receiving, transfer, pricing, employee, customer, returns, report, edge) gets a minimal `main.go`. The pattern is identical — only the service name and port change.

**Files:**
- Create: `CanaryGo/cmd/<service>/main.go` for each of the 18 services

- [ ] **Step 18.1: Write the stub template**

The following is the template. `<SERVICE_NAME>` and `<PORT>` are replaced per service.

```go
// cmd/<service>/main.go
package main

import (
	"encoding/json"
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/growdirect-llc/rapidpos/internal/config"
	"go.uber.org/zap"
)

const serviceName = "<SERVICE_NAME>"

func main() {
	cfg := config.Load(serviceName)
	logger, _ := zap.NewProduction()
	defer logger.Sync()

	r := chi.NewRouter()
	r.Use(middleware.RealIP, middleware.Logger, middleware.Recoverer)
	r.Get("/health", healthHandler(cfg))

	addr := ":" + cfg.Port
	logger.Info("starting", zap.String("service", serviceName), zap.String("addr", addr))
	if err := http.ListenAndServe(addr, r); err != nil {
		logger.Fatal("listen", zap.Error(err))
	}
}

func healthHandler(cfg *config.Config) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(map[string]interface{}{
			"ok":      true,
			"service": cfg.ServiceName,
			"version": "1.0.0",
			"checks":  map[string]string{},
		})
	}
}
```

- [ ] **Step 18.2: Write all 19 stub files using a generation script**

Apply the template above once per service. The safest approach is a shell loop — it produces one file per service with no manual substitution errors. Run from `~/GrowDirect/CanaryGo`:

```bash
cd ~/GrowDirect/CanaryGo

declare -A PORTS
PORTS[tsp]=8080 PORTS[gateway]=8079 PORTS[chirp]=8081 PORTS[alert]=8087
PORTS[fox]=8083 PORTS[owl]=8084 PORTS[analytics]=8088 PORTS[hawk]=8082
PORTS[bull]=8085 PORTS[asset]=8089 PORTS[item]=8090 PORTS[inventory]=8091
PORTS[receiving]=8092 PORTS[transfer]=8093 PORTS[pricing]=8094
PORTS[employee]=8095 PORTS[customer]=8096 PORTS[returns]=8097 PORTS[report]=8098

for svc in "${!PORTS[@]}"; do
  port=${PORTS[$svc]}
  # Remove .gitkeep now that we're writing the real file
  rm -f cmd/$svc/.gitkeep
  cat > cmd/$svc/main.go << GOEOF
// cmd/$svc/main.go
package main

import (
	"encoding/json"
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/growdirect-llc/rapidpos/internal/config"
	"go.uber.org/zap"
)

const serviceName = "canary-$svc"

func main() {
	cfg := config.Load(serviceName)
	logger, _ := zap.NewProduction()
	defer logger.Sync()

	r := chi.NewRouter()
	r.Use(middleware.RealIP, middleware.Logger, middleware.Recoverer)
	r.Get("/health", healthHandler(cfg))

	addr := ":" + cfg.Port
	logger.Info("starting", zap.String("service", serviceName), zap.String("addr", addr))
	if err := http.ListenAndServe(addr, r); err != nil {
		logger.Fatal("listen", zap.Error(err))
	}
}

func healthHandler(cfg *config.Config) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(map[string]interface{}{
			"ok":      true,
			"service": cfg.ServiceName,
			"version": "1.0.0",
			"checks":  map[string]string{},
		})
	}
}
GOEOF
done
```

- [ ] **Step 18.2a: Verify all 19 stub files were created**

```bash
cd ~/GrowDirect/CanaryGo
for svc in tsp gateway chirp alert fox owl analytics hawk bull \
           asset item inventory receiving transfer pricing employee \
           customer returns report; do
    [ -f "cmd/$svc/main.go" ] && echo "OK: $svc" || echo "MISSING: $svc"
done
```

Expected: 19 lines of `OK: <service>`.

Edge has no HTTP port — it's the Counterpoint poller. Write it separately:

- [ ] **Step 18.2b: Write edge stub**

```bash
rm -f cmd/edge/.gitkeep
cat > cmd/edge/main.go << 'GOEOF'
// cmd/edge/main.go
package main

import "go.uber.org/zap"

func main() {
	logger, _ := zap.NewProduction()
	defer logger.Sync()
	logger.Info("canary-edge: Counterpoint poller stub — M5 implementation")
	// Edge runs as a Windows Service alongside Counterpoint + SQL Server.
	// No HTTP port. Polls Counterpoint REST API, emits intelligence packets to GCP.
}
GOEOF
```

```go
// cmd/edge/main.go
package main

import (
	"go.uber.org/zap"
)

func main() {
	logger, _ := zap.NewProduction()
	defer logger.Sync()
	logger.Info("canary-edge: Counterpoint poller stub — M5 implementation")
	// Edge runs as a Windows Service alongside Counterpoint + SQL Server.
	// No HTTP port. Polls Counterpoint REST API, emits intelligence packets to GCP.
}
```

- [ ] **Step 18.3: Build all binaries**

```bash
cd ~/GrowDirect/CanaryGo
make build-all
```

Expected: 20 binaries in `bin/` — all exit 0. No compile errors.

- [ ] **Step 18.4: Verify edge Windows cross-compile**

```bash
make build-edge-windows
```

Expected: `bin/edge.exe` created (even on macOS host).

- [ ] **Step 18.5: Commit all stubs**

```bash
cd ~/GrowDirect
git add CanaryGo/cmd/
git commit -m "feat(canarygo): all 19 service stubs compiling — M1 service skeleton complete"
```

---

### Task 19: M1 Gate verification

- [ ] **Step 19.1: Fresh migration round-trip on test database**

M1 has no down migrations (deferred to post-M1). Verify idempotency and clean state using the test database instead.

```bash
cd ~/GrowDirect/CanaryGo
# Apply all 14 migrations to test DB (created during dbinit)
TEST_DB="postgres://growdirect:growdirect_dev@localhost:5432/canary_go_test?sslmode=disable"
migrate -path=deploy/migrations -database="$TEST_DB" up
```

Expected: `14/u 014_seed_roles_source_systems (Xms)` on first run.

```bash
# Run again — must be a no-op (idempotent DDL)
migrate -path=deploy/migrations -database="$TEST_DB" up
```

Expected: `no change` — confirms all `CREATE TABLE IF NOT EXISTS` / `CREATE INDEX IF NOT EXISTS` invariants hold.

- [ ] **Step 19.2: Full test suite**

```bash
cd ~/GrowDirect/CanaryGo
make test
```

Expected: all tests pass. Minimum: auth package (3 tests), identity package (4 tests).

- [ ] **Step 19.3: Confirm DB isolation**

```bash
psql -h localhost -U growdirect -c "\l" | grep canary
```

Expected: `canary`, `canary_test` (Python), `canary_go`, `canary_go_test` — four separate databases. No cross-database foreign keys.

- [ ] **Step 19.4: Run the full gate checklist**

The test suite (Task 19.2) already covers expired-token and revocation scenarios. The gate step verifies the live container and binary count only.

```bash
# /health returns ok with all checks green
curl -s http://localhost:8086/health

# Empty body → 401 (no JWT parsing required, no external dependencies)
curl -s -X POST http://localhost:8086/sessions/validate \
     -H "Content-Type: application/json" \
     -d '{}'

# Confirm all 20 binaries built
ls bin/ | wc -l
```

Expected: health returns `{"ok":true,"service":"canary-identity","version":"1.0.0","checks":{"database":"ok","valkey":"ok"}}`, validate returns `{"valid":false}`, binary count is `20`.

- [ ] **Step 19.5: Final commit**

```bash
cd ~/GrowDirect
git add CanaryGo/
git commit -m "feat(canarygo): M1 Foundation complete — all gate checks passed"
```

---

## M1 Gate Checklist

Before marking M1 done:

- [ ] `curl :8086/health` → `{"ok":true}` with `database: ok` and `valkey: ok`
- [ ] `POST /sessions/validate` with valid JWT + no Valkey key → `{"valid":false}`
- [ ] `POST /sessions/validate` with expired JWT → `{"valid":false}`
- [ ] `make test` passes with 0 failures
- [ ] `make build-all` exits 0 — 20 binaries in `bin/`
- [ ] `make build-edge-windows` exits 0
- [ ] `migrate down --all && migrate up` on `canary_go` exits 0 — no dirty state
- [ ] `sqlc generate` exits 0 after any migration change
- [ ] `canary_go` and `canary` databases confirmed separate (no cross-DB foreign keys)
- [ ] `make build-all` exits 0 and `ls bin/ | wc -l` returns 20 — compilation is the M1 health proof for non-identity stubs

---

## Notes for Executor

1. **Valkey DB 2:** All `VALKEY_URL` values must end in `/2`. DB 0 = Python Canary. DB 1 = Cove. Never use 0 or 1.
2. **Dirty migration state:** If any migration leaves a dirty version, fix with `migrate force <version>` — never drop and recreate the DB.
3. **sqlc regenerate always:** Any migration change requires `make sqlc-gen` to re-read the schema. Stale generated code will compile but produce wrong queries.
4. **Fox trigger test isolation:** `testutil.TruncateTables` excludes `fox_evidence` by design. To reset fox state in tests: `DROP TABLE app.fox_evidence CASCADE` then re-apply migrations 012–013. Do not bypass the trigger.
5. **Port authority:** This plan follows `go-module-layout.md`. If you see a different port in `microservice-architecture.md`, that SDD needs updating — it does not override this plan.
6. **parseValkeyAddr:** The helper strips `redis://` and the `/db` suffix. If your Valkey URL format differs, adjust it — the DB number is hardcoded to 2 in `main.go`.
