# factory-startup — Session Start

## On every new session, before any work:

### 1. Load context

- Read `~/GrowDirect/CLAUDE.md` (platform standards — tech stack, model rules, hard rules)
- Read the current app's `CLAUDE.md` (domain context, app-specific rules)
- Confirm: "Loaded GrowDirect platform + [App] context. I am [Agent Name]."

### 2. Check shared infrastructure

```bash
docker ps --format "table {{.Names}}\t{{.Status}}" | grep growdirect
```

Expected running services: `growdirect_postgres`, `growdirect_valkey`, `growdirect_ollama`, `growdirect_pgadmin`

If any are missing:
```bash
cd ~/GrowDirect/devops && docker compose up -d
```

### 3. Check app container

```bash
docker ps --format "table {{.Names}}\t{{.Status}}" | grep <appname>
```

If not running:
```bash
cd ~/GrowDirect/<App>/devops && docker compose up -d
```

Watch for `ModuleNotFoundError` in logs — that means `docker compose build flask` is needed, not a code fix.

### 4. Check git status

```bash
git -C ~/GrowDirect/<App> status
git -C ~/GrowDirect/<App> log --oneline -5
```

Note: current branch, uncommitted changes, unpushed commits. If on a feature branch, identify the GRO issue it maps to.

### 5. Confirm the task

What GRO issue are we working on? If none was specified, ask before proceeding.

### 6. Report

"Infrastructure: [up/partial/down]. Branch: [name]. Uncommitted: [yes/no]. Task: [GRO-XXX — description]."
