---
name: canary-preflight
description: |
  Session bootstrap for Canary development. Run at the start of every session.
  Delegates to factory-preflight for shared infrastructure, then adds Canary-specific
  checks: stack health, git hygiene, env validation, guardian manifest, tunnel health,
  memory recall, and Linear status. Use when: starting a session, 'ALX', '/alx',
  or any variation of 'start up' / 'check the stack'.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
---

# Canary Preflight — Session Bootstrap

Run this at the start of every Canary session. No exceptions. No skipping steps.

**Announce at start:** "I'm using canary-preflight to bootstrap this session."

## Step 0: Factory Preflight

Run `factory-preflight` first. It checks shared infrastructure (Docker, PostgreSQL,
Valkey, Ollama, git, Linear, memory bus). If any shared service fails, fix it before
proceeding to Canary-specific checks.

## Step 1: Stack Health

Verify Canary containers are running and Flask is responding:

```bash
cd ~/GrowDirect/Canary && docker compose -f devops/docker-compose.localhost.yml ps
curl -s http://localhost:5001/health
```

If containers are down:

```bash
cd ~/GrowDirect/Canary && ./devops/scripts/boot_localhost.sh
```

If Flask is unhealthy:

```bash
cd ~/GrowDirect/Canary && docker compose -f devops/docker-compose.localhost.yml logs flask --tail=50
```

**Do not proceed until `/health` returns 200.** Fix it. Don't report it.

## Step 2: Git Hygiene

Check for stale branches and open PRs. Jeffe is solo — there should be zero parallel work.

```bash
cd ~/GrowDirect/Canary
echo "=== Current branch ===" && git branch --show-current
echo "=== Open PRs ===" && gh pr list --state open
echo "=== Unmerged local branches ===" && git branch --no-merged main
echo "=== Merged branches to clean ===" && git branch --merged main | grep -v '^\*' | grep -v 'main'
```

**If open PRs exist:** flag them to Jeffe. Merge or close before starting new work.
**If merged branches exist:** delete them (`git branch -d <name>`).
**If unmerged branches exist:** flag them — may be abandoned work.

One branch at a time. Merge before starting the next issue.

## Step 3: Env Validation

```bash
cd ~/GrowDirect/Canary && python3 devops/scripts/validate_env.py --template .env.template --env-file .env
```

If MISSING or EMPTY: stop and tell Jeffe. Do not create or overwrite `.env`.

## Step 4: Guardian Manifest Check

Verify all protected files match their `.guardian-manifest` hashes:

```bash
cd ~/GrowDirect/Canary && python3 -c "
import hashlib, json, os
with open('.guardian-manifest', 'r') as f:
    m = json.load(f)
drift = []
for path, entry in m.get('files', {}).items():
    if not os.path.exists(path):
        drift.append((path, 'MISSING'))
        continue
    with open(path, 'rb') as fh:
        actual = hashlib.sha256(fh.read()).hexdigest()
    if actual != entry.get('sha256', ''):
        drift.append((path, 'MODIFIED'))
if drift:
    print('GUARDIAN ALERT — protected files changed outside guardian process:')
    for path, status in drift:
        print(f'  {status}: {path}')
else:
    print('Guardian manifest OK — all protected files match.')
"
```

**If drift detected:** STOP. Show Jeffe which files changed. Do not proceed until
Jeffe decides whether to accept the current state or investigate. Use `file-guardian`
to update the manifest if Jeffe approves.

**If manifest file missing:** Generate it — run the file-guardian skill's initial setup.

## Step 5: Tunnel Health

Verify Cloudflare Tunnel is running and `dev.growdirect.app` is reachable:

```bash
cloudflared tunnel info canary-dev 2>/dev/null && curl -s -o /dev/null -w "%{http_code}" https://dev.growdirect.app/health
```

If tunnel is down:

```bash
cloudflared tunnel run canary-dev &
```

If `/health` fails through tunnel but works on `localhost:5001`: tunnel config issue — check `~/.cloudflared/config.yml`.

## Step 6: ALX Memory Recall

Before writing any code, recall relevant context from the ALX pgvector memory store
(954+ curated memories: SDDs, architecture, patterns, codebase knowledge).

```bash
cd ~/GrowDirect/Canary && curl -s -X POST http://localhost:5001/alx/tools/memory_recall \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $(grep CANARY_MCP_API_KEY .env | cut -d= -f2)" \
  -d '{"params": {"query": "YOUR_TOPIC_HERE", "limit": 10}, "context": {}}' | python3 -m json.tool
```

Replace `YOUR_TOPIC_HERE` with the task context. Recall before touching unfamiliar files.

**Auth note:** The `X-API-Key` header is required (SDD-059). The key is read from `.env`
at runtime. The MCP blueprint expects params wrapped in `{"params": {...}, "context": {}}`.

## Step 7: Linear Status

Pull current state from Linear project **Canary** (GRO-prefixed issues).

- If Jeffe gave a GRO number: that's the task — skip the overview, go straight to work.
- If no GRO number: present Jeffe with one-line status per active issue.
- If Linear board is empty: tell Jeffe the board is clean and ask what's next.

## Shorthand Commands

| Command | Action |
|---|---|
| `ALX` or `/alx` | Run this preflight sequence |
| `session close` | Run `canary-close` |
| `>>status` | One-paragraph project state from Linear |
| `>>north star` | "We don't want to add to the stress. We want to ease it." |
| `>>dispatch [task]` | Route to the right agent (load profile from `docs/profiles/`) |
| `>>timelog` | Run `project-timelog` |
| `>>workorder [GRO-XXX]` | Generate execution-ready work order for agent dispatch |

---

*Canary Preflight v1.0 — Session Bootstrap*
*Delegates to: factory-preflight (shared infra)*
*Replaces: alx-startup*
