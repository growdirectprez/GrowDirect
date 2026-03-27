# Docker Standard

Every GrowDirect app follows this exact structure. No variations without a Linear issue.

## Compose Template

`docker/docker-compose.yml` — exact structure every app follows:

```yaml
services:
  postgres:
    image: pgvector/pgvector:pg17
    container_name: <appname>_localhost_postgres
    environment:
      POSTGRES_USER: <appname>
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: <appname>
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U <appname> -d <appname>"]
      interval: 5s
      start_period: 10s
      retries: 10

  valkey:
    image: valkey/valkey:8-alpine
    container_name: <appname>_localhost_valkey
    healthcheck:
      test: ["CMD", "valkey-cli", "ping"]
      interval: 5s
      retries: 5

  flask:
    build:
      context: ../
      dockerfile: Dockerfile
    container_name: <appname>_localhost_flask
    command: gunicorn --bind 0.0.0.0:<port> --workers 1 --threads 4 --timeout 120 --reload wsgi:app
    ports:
      - "<port>:<port>"
    env_file: ../.env
    depends_on:
      postgres: { condition: service_healthy }
      valkey: { condition: service_healthy }
    healthcheck:
      test: python -c "from urllib.request import urlopen; urlopen('http://localhost:<port>/health')"
      interval: 10s
      start_period: 20s
      retries: 5

volumes:
  postgres_data:
```

## Dockerfile Template

Two-stage build. Non-root user. Python 3.12-slim base.

```dockerfile
# Stage 1: dependencies
FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: runtime
FROM python:3.12-slim
WORKDIR /app

# Non-root user
RUN addgroup --system app && adduser --system --ingroup app app

COPY --from=builder /install /usr/local
COPY . .

RUN chown -R app:app /app
USER app

EXPOSE <port>
CMD ["gunicorn", "--bind", "0.0.0.0:<port>", "--workers", "1", "--threads", "4", "--timeout", "120", "wsgi:app"]
```

## Health Check Patterns

**HTTP endpoint (flask):**
```yaml
test: python -c "from urllib.request import urlopen; urlopen('http://localhost:<port>/health')"
interval: 10s
start_period: 20s
retries: 5
```

Flask must expose `GET /health` returning 200. No auth required on this route.

**CLI ping (valkey):**
```yaml
test: ["CMD", "valkey-cli", "ping"]
interval: 5s
retries: 5
```

**pg_isready (postgres):**
```yaml
test: ["CMD-SHELL", "pg_isready -U <appname> -d <appname>"]
interval: 5s
start_period: 10s
retries: 10
```

All services must have health checks. `depends_on` always uses `condition: service_healthy`, never `condition: service_started`.

## Port Allocation Table

| App | Flask | Postgres (host) | Valkey | pgAdmin | Other |
|-----|-------|-----------------|--------|---------|-------|
| Canary | 5001 | 5432 | 6379 | 5050 | nginx 443/80, Owl 8001, QA 8002 |
| Cove | 5002 | 5433 | 6380 | 5051 | MailHog SMTP 1026, Web 8026 |

New apps: claim ports in the next available block and update this table + CLAUDE.md.

## Container Naming

Pattern: `<appname>_localhost_<service>`

Examples:
- `canary_localhost_postgres`
- `canary_localhost_valkey`
- `canary_localhost_flask`
- `cove_localhost_postgres`

Consistent naming makes `docker ps` readable and scripts portable across apps.

## Startup Order

```
postgres (healthy) → valkey (healthy) → flask (starts)
```

Flask waits for both upstream services to pass their health checks before starting. This is enforced via `depends_on` with `condition: service_healthy`. Never use `condition: service_started`.

## Volume Mounts

**Development** — source mount with `--reload` so edits are live:
```yaml
volumes:
  - ../:/app
```

Combined with `--reload` in the gunicorn command, code changes take effect without a container restart.

**Production** — code is COPY'd at build time, no source mount:
```dockerfile
COPY . .
```

The production image is immutable. Source mounts are never used in staging or production compose files.
