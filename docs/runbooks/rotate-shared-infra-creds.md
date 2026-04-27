---
classification: internal
type: runbook
date: 2026-04-25
last-rotation: 2026-04-25 (GRO-553)
---

# Rotate Shared Infrastructure Credentials

Rotation of the credentials behind `growdirect_postgres`, `growdirect_valkey`, `growdirect_pgadmin`, and the legacy `devops-cove-db-1`. The shared compose, canary prod compose, canary qa compose, and cove archive compose all use env var substitution; the actual values live in gitignored `.env` files.

## What touches these creds

**Producers (where passwords live as the source of truth):**

| Service | Where stored | Auth model |
|---|---|---|
| `growdirect_postgres` user `growdirect` | postgres-internal (set via `ALTER USER`) | scram-sha-256 |
| `growdirect_valkey` | runtime arg `--requirepass` (set on container start) | requirepass |
| `growdirect_pgadmin` admin | env var `PGADMIN_DEFAULT_PASSWORD` (set on container start) | basic auth |
| `devops-cove-db-1` user `cove` | postgres-internal (set via `ALTER USER`) | scram-sha-256 |

**Consumer .env files (each consumes one or more producer):**

| .env path | Used by | Vars |
|---|---|---|
| `~/GrowDirect/devops/.env` | shared `devops/docker-compose.yml` | `POSTGRES_PASSWORD`, `VALKEY_PASSWORD`, `PGADMIN_DEFAULT_PASSWORD`, `COVE_DB_PASSWORD` |
| `~/GrowDirect/Canary/.env` | canary prod compose `env_file: ../.env` | App vars (SECRET_KEY, SQUARE_*, CANARY_*, etc.) |
| `~/GrowDirect/Canary/devops/.env` | canary prod compose substitution | `POSTGRES_PASSWORD`, `VALKEY_PASSWORD` |
| `~/GrowDirect-archive-2026-04-25/Canary/devops/.env.qa` | canary qa compose substitution + env_file | `POSTGRES_PASSWORD`, `VALKEY_PASSWORD`, app vars |
| `~/GrowDirect-archive-2026-04-25/Cove/devops/.env` | cove archive compose substitution | `COVE_DB_USER`, `COVE_DB_PASSWORD` |

## Pre-rotation checklist

1. Maintenance window scheduled — production canary and cove will see ~30-60s of 5xx during the recreate window.
2. Cloudflared tunnel daemon healthy.
3. Take a snapshot of current state:
   ```
   docker ps --format '{{.Names}} | {{.Status}}'
   curl -sI https://canary.growdirect.app
   curl -sI https://qa.growdirect.app
   curl -sI https://abalonecove.org
   ```
4. Backup .env files:
   ```
   cp ~/GrowDirect/devops/.env ~/GrowDirect/devops/.env.bak.$(date +%Y%m%d)
   cp ~/GrowDirect/Canary/.env ~/GrowDirect/Canary/.env.bak.$(date +%Y%m%d)
   ```

## Rotation sequence

### 1. Generate new credentials

```bash
NEW_POSTGRES_PASSWORD=$(openssl rand -hex 16)
NEW_VALKEY_PASSWORD=$(openssl rand -hex 16)
NEW_PGADMIN_PASSWORD=$(openssl rand -hex 16)
NEW_COVE_DB_PASSWORD=$(openssl rand -hex 16)
```

### 2. Apply at source (DB-internal first; existing connections survive)

```bash
# Postgres user
docker exec growdirect_postgres psql -U growdirect \
  -c "ALTER USER growdirect WITH PASSWORD '$NEW_POSTGRES_PASSWORD'"

# Cove legacy DB user
docker exec devops-cove-db-1 psql -U cove \
  -c "ALTER USER cove WITH PASSWORD '$NEW_COVE_DB_PASSWORD'"
```

### 3. Update .env files

Update all five .env paths above. Each file should have the new value for the password var(s) it owns.

### 4. Recreate valkey (this drops all valkey clients briefly)

```bash
cd ~/GrowDirect/devops && docker compose up -d --force-recreate valkey
sleep 5
# verify
docker exec growdirect_valkey valkey-cli -a "$NEW_VALKEY_PASSWORD" ping  # PONG
docker exec growdirect_valkey valkey-cli -a "<old>" ping  # NOAUTH
```

### 5. Recreate consumers

```bash
# Canary prod
cd ~/GrowDirect/Canary/devops && \
  docker compose -f docker-compose.production.yml up -d --force-recreate

# Canary qa
cd ~/GrowDirect-archive-2026-04-25/Canary/devops && \
  docker compose --env-file .env.qa -f docker-compose.qa.yml up -d --force-recreate

# Cove
cd ~/GrowDirect-archive-2026-04-25/Cove/devops && \
  docker compose -f docker-compose.prod.yml up -d --force-recreate
```

### 6. Verify

```bash
# Services healthy
docker ps --format '{{.Names}} | {{.Status}}'

# Tunnels green
curl -sI https://canary.growdirect.app  # 302
curl -sI https://qa.growdirect.app      # 302
curl -sI https://abalonecove.org        # 200

# Old creds rejected (TCP path)
docker run --rm --network growdirect \
  -e PGPASSWORD=<old> postgres:17-alpine \
  psql -h growdirect_postgres -U growdirect -d growdirect -c "select 1"
# Should fail with: FATAL: password authentication failed

# New creds accepted
docker run --rm --network growdirect \
  -e PGPASSWORD="$NEW_POSTGRES_PASSWORD" postgres:17-alpine \
  psql -h growdirect_postgres -U growdirect -d growdirect -c "select 1"
# Should return: 1
```

## Recovery if something goes sideways

If a consumer fails to start after recreate (e.g., missing env var, encryption key):

1. **Don't panic.** The DB-side passwords are already rotated; you can't roll back without `ALTER USER` again.
2. Check logs: `docker logs --tail 50 <container>` — look for `KeyError`, `RuntimeError`, missing config.
3. Compare missing vars against `~/GrowDirect-archive-2026-04-25/Canary/.env` (historical reference).
4. Append the missing var to the relevant `.env` file and recreate just that container.
5. Common gotcha: `SECRET_KEY` is required for canary in production but doesn't match the `(CANARY_|SQUARE_|FLASK_|...)` prefix patterns. The historical value lives in the archive .env.

## Out of scope (for separate dispatches)

- **`growdirect_pgadmin` activation.** The shared compose declares the service; not currently running on the mini. Bring up via `docker compose -f ~/GrowDirect/devops/docker-compose.yml up -d pgadmin` if a UI is wanted. Will use port 5050 (currently free since `canary_qa_pgadmin` was retired in GRO-552).
- **Cove migration.** The `cove-web` still talks to legacy `cove-db` (47 MB, 27 tables). Long-term: dump → restore to `growdirect_postgres.cove` → cutover → retire legacy. Until then, the cove user pwd lives in two places (legacy DB `cove` user, plus the `cove` database stub on shared postgres).
- **Move archive composes into live repo.** Currently `Canary/devops/docker-compose.qa.yml` and `Cove/devops/docker-compose.prod.yml` only exist in `~/GrowDirect-archive-2026-04-25/`. Long-term home is the live repo with proper .env separation.

## When to rotate

- After any session where creds are exposed (e.g., shared via screenshare, accidentally pasted into chat, stored in a deprovisioned location).
- Quarterly minimum.
- When team membership changes for anyone with mini access.

## Audit trail

Each rotation should be recorded:
- Linear comment on a "credential rotation" parent issue with the rotation date and the dispatch ID
- Git commit on the runbook touching `last-rotation:` field
- DON'T paste the actual new password values anywhere — they live only in the gitignored .env files
