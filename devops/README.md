# GrowDirect Shared Development Infrastructure

A single Docker Compose stack that runs all shared services for every GrowDirect app. Individual app Flask containers attach to the `growdirect` network and connect to these shared services.

## Start

```bash
cd ~/GrowDirect/devops
docker compose up -d
```

## Stop

```bash
cd ~/GrowDirect/devops
docker compose down
```

## Wipe everything (volumes too)

```bash
cd ~/GrowDirect/devops
docker compose down -v
```

---

## Services

| Service | Container | Host Port | Purpose |
|---------|-----------|-----------|---------|
| PostgreSQL 17 + pgvector | `growdirect_postgres` | `5432` | All app databases |
| Valkey 8 | `growdirect_valkey` | `6379` | Session store, cache, task queue |
| pgAdmin 4 | `growdirect_pgadmin` | `5050` | Database browser → http://localhost:5050 |
| Ollama | `growdirect_ollama` | `11434` | Local LLM inference → http://localhost:11434 |

### pgAdmin login

- Email: `admin@growdirect.com`
- Password: `admin`

---

## How apps connect

All app Flask containers must join the `growdirect` network. In each app's `docker-compose.yml`:

```yaml
networks:
  default:
    external: true
    name: growdirect
```

Then use these hostnames in environment variables:

| Setting | Value |
|---------|-------|
| Postgres host | `growdirect_postgres` |
| Postgres port | `5432` |
| Postgres user | `growdirect` |
| Postgres password | `growdirect_dev` |
| Valkey host | `growdirect_valkey` |
| Valkey port | `6379` |

Example DATABASE_URL for the `canary` app:

```
DATABASE_URL=postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/canary
```

Example VALKEY_URL:

```
VALKEY_URL=redis://:valkey_dev@growdirect_valkey:6379/<db_number>
```

---

## Databases

The following databases are created on first boot by `init-db/01-create-databases.sql`:

| Database | App | Notes |
|----------|-----|-------|
| `canary` | Canary | Production database |
| `canary_test` | Canary | Test runner database |
| `canary_memory` | growdirect | ALX agent knowledge graph |
| `cove` | Cove | Production database |
| `cove_test` | Cove | Test runner database |

All databases have the `vector` extension enabled (pgvector).

---

## Adding a new app database

1. Edit `init-db/01-create-databases.sql` and add:

```sql
CREATE DATABASE <appname> OWNER growdirect;
CREATE DATABASE <appname>_test OWNER growdirect;

\c <appname>
CREATE EXTENSION IF NOT EXISTS vector;

\c <appname>_test
CREATE EXTENSION IF NOT EXISTS vector;
```

2. Recreate the postgres container to apply (only needed if postgres was already running):

```bash
cd ~/GrowDirect/devops
docker compose down postgres
docker compose up -d postgres
```

Note: init scripts only run on a fresh data volume. If the volume already exists, connect to postgres and run the SQL manually:

```bash
docker exec -it growdirect_postgres psql -U growdirect -c "CREATE DATABASE <appname> OWNER growdirect;"
docker exec -it growdirect_postgres psql -U growdirect -d <appname> -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

---

## Network

All containers share the `growdirect` Docker network. Docker DNS resolves container names to IP addresses automatically within this network.

```
growdirect network
├── growdirect_postgres   (postgres:5432)
├── growdirect_valkey     (valkey:6379)
├── growdirect_pgadmin
├── growdirect_ollama     (ollama:11434)
├── canary_localhost_flask   (attached from Canary stack)
└── cove_localhost_flask     (attached from Cove stack)
```
