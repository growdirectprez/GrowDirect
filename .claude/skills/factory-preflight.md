---
name: factory-preflight
roles-primary: [ALX]
roles-assist: [Eva]
stage: preflight
description: |
  Infrastructure health checks and context loading before any factory stage.
  Replaces factory-startup. Runs red/yellow/green checks on Docker, PostgreSQL,
  Valkey, Ollama, Linear, git, and memory bus. Loads CLAUDE.md, manifest, and
  GRO issue context. Identifies app for stage branching.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - TodoWrite
  - mcp__a018de2b-6aea-4cf1-aa2a-20375d7d8e69__get_issue
---

# factory-preflight — Infrastructure & Context

> Replaces `factory-startup`. Runs before any factory stage.

**Announce at start:** "Running factory-preflight — checking infrastructure and loading context."

## 1. Read the manifest

```bash
cat ~/GrowDirect/factory-manifest.json
```

Confirm the pipeline order and identify which stage you're about to enter.

## 2. Infrastructure checks

Run each check. Report as GREEN / YELLOW / RED.

### Docker stack

```bash
docker ps --format "table {{.Names}}\t{{.Status}}" | grep growdirect
```

- GREEN: All 4 containers healthy (postgres, valkey, ollama, pgadmin)
- YELLOW: Some containers unhealthy or restarting
- RED: Docker not running or no growdirect containers

If RED: `cd ~/GrowDirect/devops && docker compose up -d`

### PostgreSQL

```bash
docker exec growdirect_postgres pg_isready -U growdirect
```

- GREEN: accepting connections
- YELLOW: accepting but slow (>2s response)
- RED: not accepting connections

### Valkey

```bash
docker exec growdirect_valkey valkey-cli ping
```

- GREEN: PONG
- YELLOW: PONG but USED_MEMORY > 80%
- RED: no response

### Ollama

```bash
curl -sf http://localhost:11434/api/tags | python3 -c "import sys,json; tags=json.load(sys.stdin).get('models',[]); names=[m['name'] for m in tags]; print('Models:', names); sys.exit(0 if any('qwen3' in n for n in names) else 1)"
```

- GREEN: qwen3-embedding model loaded
- YELLOW: Ollama running but model not loaded — `docker exec growdirect_ollama ollama pull qwen3-embedding:8b`
- RED: Ollama unreachable

### Git status

```bash
git status --porcelain
```

- GREEN: clean working tree
- YELLOW: uncommitted changes (warn, don't block)
- RED: not a git repository

### Linear MCP

Use `get_issue` tool to fetch the GRO issue. If it returns data, GREEN. If issue not found, YELLOW. If MCP unreachable, RED.

### Memory bus (optional)

```bash
curl -sf http://localhost:8003/health 2>/dev/null || echo "NOT RUNNING"
```

- GREEN: healthy response
- YELLOW: not running (optional, continue without it)

## 3. Gate decision

- Any RED → STOP. Report what's broken and how to fix it. Do not proceed.
- All GREEN/YELLOW → proceed. List any YELLOW warnings.

## 4. Load context

1. Read `~/GrowDirect/CLAUDE.md` (platform standards)
2. Read the current app's `CLAUDE.md` if working in an app directory
3. Read `~/GrowDirect/factory-manifest.json`
4. Load GRO issue description from Linear (already fetched in step 2)
5. Query memory bus for prior art: `memory_recall` with GRO issue title (skip if memory bus not running)

## 5. Identify app context

Determine which app this work targets:
- From GRO issue project field (Canary / Cove / Platform)
- From current working directory
- From explicit user input

This determines which `{app}-{stage}.md` overrides apply at each pipeline stage.

## 6. Report

```
Preflight: [GREEN/YELLOW/RED]
  Docker:     [status]
  PostgreSQL: [status]
  Valkey:     [status]
  Ollama:     [status]
  Git:        [status]
  Linear:     [status]
  Memory Bus: [status]

App: [canary / cove / platform]
Branch: [current branch]
Task: GRO-XXX — [title]

[Any YELLOW warnings listed here]
```
