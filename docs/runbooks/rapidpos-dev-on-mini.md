---
classification: internal
owner: GrowDirect LLC
type: runbook
audience: ALX (mini-resident) + future Dispatch operators on the mini
date: 2026-04-25
status: living
linear-issue: GRO-557
tags: [mini, rapidpos, retailspine, dev-environment, runbook]
---

# RapidPOS dev environment on the mini — runbook

Operating manual for using the GrowDirect mini (192.168.10.102) as the live development environment for Canary's RapidPOS / RetailSpine work. The mini is also the production host for canary.growdirect.app, qa.growdirect.app, and abalonecove.org — **production must keep serving** through every dev iteration.

## Why the mini, not the laptop

Per the founder's reframe (2026-04-25): *"we are going to treat the mini as dev for the RapidPOS project so we can relax constraints for this; the mini is self contained; it will take over mastering the code base as we add in more of the retail spine."* The mini's dual role — production hosting + dev for one named project — is intentional. Discipline rules below preserve the production posture under that load.

## Topology

```
                         ┌─────────────────────────────────────┐
                         │         GrowDirect Mini             │
                         │      192.168.10.102 / 16 GB / M4    │
                         │                                     │
   internet ────cloudflared tunnel──┐                          │
                         │          ▼                          │
                         │  ┌──────────────────┐               │
                         │  │ canary_prod_*    │ :5100         │
                         │  │ (4 TSP subs)     │               │
                         │  │ canary_qa_app    │ :5001 (qa)    │
                         │  │ devops-cove-web  │ :5002         │
                         │  └──────────────────┘  ← PROD       │
                         │           │                         │
                         │  ┌──────────────────┐               │
                         │  │ growdirect_*     │ shared infra  │
                         │  │  postgres :5432  │               │
                         │  │  valkey   :6379  │               │
                         │  │  ollama   :11434 │               │
                         │  │  pgadmin  :5050  │               │
                         │  └──────────────────┘               │
                         │                                     │
                         │  ┌──────────────────┐               │
                         │  │ canary-flask:dev │ :5200 ← DEV   │
                         │  │ (this runbook)   │               │
                         │  └──────────────────┘               │
                         └─────────────────────────────────────┘
```

**Port allocation:**

| Service | Port | Visibility | Purpose |
|---|---|---|---|
| `canary_prod_flask` | 5100 (127.0.0.1 → cloudflared) | public via canary.growdirect.app | **prod — never touch** |
| `canary_qa_app` | 5001 (LAN) | public via qa.growdirect.app | QA / second-flavor demo |
| `devops-cove-web-1` | 5002 | public via abalonecove.org | Cove prod |
| `canary-flask:dev` | 5200 (127.0.0.1 only) | host-only | this runbook's territory |
| Shared infra (postgres / valkey / ollama / pgadmin) | 5432 / 6379 / 11434 / 5050 | host-only (after GRO-552) | shared by prod, QA, dev |

Dev iterates against **shared** postgres + valkey + ollama. Use a separate database (`canary_dev`) inside the shared postgres to isolate dev data from prod.

## Working-tree layout

| Path | Purpose | Remote |
|---|---|---|
| `~/GrowDirect/` | Platform repo (this runbook lives here) | `git@github.com:growdirectprez/GrowDirect.git` |
| `~/GrowDirect/Canary/` | Canary working tree (gitignored at platform level) | `git@github.com:growdirect-llc/canary-retail.git` |
| `~/GrowDirect/Cove/` | Cove working tree (gitignored at platform level) | `git@github.com:growdirectprez/Cove.git` |
| `~/GrowDirect/Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/` | NCR Counterpoint API spec corpus (read-only reference) | `https://github.com/NCRCounterpointAPI/APIGuide.git` |

## First-time setup (idempotent)

If any working tree is missing, restore it from origin. The platform `.gitignore` excludes `/Canary/` and `/Cove/`, so they sit cleanly as separate repos inside the platform working tree.

```bash
cd ~/GrowDirect

# Canary — note: redirected from old `growdirectprez/growdirect-ops`
[ -d Canary/.git ] || git clone git@github.com:growdirect-llc/canary-retail.git Canary

# Cove
[ -d Cove/.git ] || git clone git@github.com:growdirectprez/Cove.git Cove

# Counterpoint API corpus (read-only reference; not committed to platform repo)
mkdir -p Brain/raw/inbox/rapid-pos
[ -d Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/.git ] || \
  git clone https://github.com/NCRCounterpointAPI/APIGuide.git \
            Brain/raw/inbox/rapid-pos/ncr-counterpoint-api
```

Verify:

```bash
git -C ~/GrowDirect/Canary status --short --branch   # → ## main...origin/main
git -C ~/GrowDirect/Cove   status --short --branch   # → ## main...origin/main
ls   ~/GrowDirect/Brain/raw/inbox/rapid-pos/ncr-counterpoint-api/Endpoints/ | head -3
```

## Daily edit/test/commit loop

### 1. Pull latest

```bash
cd ~/GrowDirect/Canary && git pull --ff-only origin main
```

### 2. Cut a working branch from a Linear Dispatch issue

Branch naming follows the dispatch's stated convention (e.g. `mini/dispatch-mini1-ej-spine-naming` for GRO-559). If the dispatch doesn't specify, fall back to Linear's `gitBranchName` field on the issue.

```bash
git checkout -b mini/dispatch-<short-name> origin/main
```

### 3. Edit code

Use your editor of choice. The `~/GrowDirect/Canary/` tree is the live source of truth on the mini.

### 4. Run the dev container (when you need to exercise behavior)

For a single-process boot test (no full stack):

```bash
cd ~/GrowDirect/Canary
docker build -t canary-flask:dev -f devops/Dockerfile .
docker run --rm -d \
  --name canary_dev_smoke \
  --network growdirect \
  -p 127.0.0.1:5200:5001 \
  -e DATABASE_URL=postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/canary_dev \
  -e VALKEY_URL=redis://:valkey_dev@growdirect_valkey:6379/8 \
  -e FLASK_ENV=development \
  canary-flask:dev
curl -sf http://127.0.0.1:5200/health
docker stop canary_dev_smoke
```

For a full hot-reload dev stack on top of `docker-compose.localhost.yml`:

```bash
cd ~/GrowDirect/Canary
./devops/scripts/dev.sh up        # start with hot reload (DEV_RELOAD=true)
./devops/scripts/dev.sh logs      # tail flask logs
./devops/scripts/dev.sh restart   # restart flask only
./devops/scripts/dev.sh down      # stop dev stack
```

The dev stack uses `docker-compose.dev.yml` as a thin override on top of `docker-compose.localhost.yml`. Hot-reload covers Python edits; rebuild only when `requirements*.txt` or the `Dockerfile` change:

```bash
./devops/scripts/dev.sh build
```

### 5. Run tests inside the dev container

`pytest` lives inside the image, not on the host. The host `python3` is 3.9; the image is 3.12.

```bash
docker run --rm \
  -v $(pwd):/app \
  --network growdirect \
  -e DATABASE_URL=postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/canary_test \
  canary-flask:dev \
  python -m pytest tests/unit/ -x -q
```

Or, with the dev stack running, exec into the live container:

```bash
docker exec -it <canary_dev_flask> python -m pytest tests/unit/ -x -q
```

### 6. Commit

```bash
git add <paths>
git commit -m "<dispatch-prefix>: <message>"
```

Commit-message convention: prefix with the dispatch identifier (e.g. `Mini-1: …`, `Dev-2: …`). Footer should include `Co-Authored-By` for any AI-assisted edits.

### 7. Push to origin

The mini's SSH key is authorized for both `growdirect-llc/canary-retail` and `growdirectprez/Cove`. SSH agent / key forwarding is **not** required — the local key signs.

```bash
git push -u origin mini/dispatch-<short-name>
```

GitHub will print a PR-ready URL. Open the PR via the URL or via `gh pr create` if `gh` is installed.

### 8. Post the Done comment on the Linear issue

Per the (forthcoming) `dispatch-coordination-protocol.md`, include:
- Branch + commit SHA
- Files touched
- Verification output (test results, import check, etc.)
- Any caveats or follow-ups
- Then move the issue to `Done`.

## Production-safety rules

These rules exist because the mini hosts production. Violating them risks an outage on canary.growdirect.app or abalonecove.org.

1. **Never `docker stop`, `docker rm`, or `docker compose down` against `canary_prod_*` or `devops-cove-*` containers without coordinating a maintenance window.**
2. **Never recreate (`docker compose up -d --force-recreate`) without checking which containers will be touched.** Use `--no-deps` or specify services explicitly.
3. **Don't edit `devops/docker-compose.yml` (platform shared infra) on the dev branch.** That file is shared across prod/QA/dev. Changes belong in their own dispatch (e.g. GRO-552 covers the LAN-binding fix).
4. **Don't edit cloudflared config (`/etc/cloudflared/config.yml`).** The tunnel is the single point of failure for all four public hostnames.
5. **Use a separate database (`canary_dev`) for dev work.** Don't run migrations against the `canary` (prod) database from a dev branch.
6. **Image tags matter.** Build dev images as `canary-flask:dev`, never as `canary-flask:production`. The prod containers are pinned to `:production` and won't auto-update.

## Concurrent-worker coordination

Multiple workers (humans + agents) can be on the mini at once. To avoid collisions:

- **Comment on the Linear issue before starting** (use the Starting / Done structure from GRO-559's comments as a template until `Brain/wiki/dispatch-coordination-protocol.md` is authored — see GRO-557 follow-up notes).
- **Check for `In Progress` siblings** on related issues before recreating shared containers.
- **Don't move tickets to `Done` without verifiable evidence** (commit SHA, container state, test output).

## Caveats current as of 2026-04-25

- The Canary repo's GitHub URL was renamed: `growdirectprez/growdirect-ops.git` → `github.com/growdirect-llc/canary-retail.git`. The redirect works, but local clones from before the rename will print a redirect notice on push. Update the remote: `git remote set-url origin git@github.com:growdirect-llc/canary-retail.git`.
- The mini's host Python is 3.9.6; Canary expects 3.12. Use the dev image, not the host Python, for any tooling that needs to match CI.
- Shared infra (`postgres`, `valkey`, `pgadmin`, `cove-db`) is currently bound to `0.0.0.0` at runtime despite compose declaring `127.0.0.1`. Tracked in GRO-552. Until that lands, do not place sensitive data in dev databases.
- The `~/GrowDirect-archive-2026-04-25/Canary/` and `Cove/` directories still exist as a snapshot. They are not the live tree; if you find yourself there, `cd ~/GrowDirect/Canary` instead. Cleanup is a maintenance follow-up.

## References

- GRO-557 — this runbook's parent issue
- GRO-551 audit — `docs/superpowers/specs/2026-04-25-mini-self-review.md` § Layer 2
- GRO-558 — POS-agnostic adapter substrate (the work this dev environment serves)
- NCR Counterpoint SDD — `docs/sdds/canary/ncr-counterpoint-retail-spine-integration.md`
- Mini reframe brief — `docs/superpowers/briefs/2026-04-25-mini-reframe-and-trim.md`
- Memory: `project_alx_mini_role.md`, `project_mini_mission_and_steady_state.md`
