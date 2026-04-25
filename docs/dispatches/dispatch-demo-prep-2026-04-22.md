---
classification: confidential
owner: GrowDirect LLC
---

# Epic: Canary Goes Primetime
## Sprint window: 3–4 days (2026-04-22 → 2026-04-26)
## For: Claude Code sessions in GrowDirect/Canary/

---

### The pitch

Canary is going in front of seasoned enterprise retail engineers — people who
build loss prevention systems at scale for Walmart, Target, Kroger. They're
way beyond Square. What fascinates them is the journey: one founder with AI
built a functionally complete LP analytics platform in months, prototyping
what would take their teams a year. The ask isn't "use Canary" — it's "look
what's possible, then hand this to your engineering team to harden to your
enterprise standards."

### What they'll see

1. **canary.growdirect.io** — static product site (GitHub Pages, already built)
2. **canary.growdirect.app** — live, clickable demo (Flask app on Mac Mini
   at 192.168.10.102, Cloudflare tunnel, Square sandbox)
3. **GitHub repo** — clean, public-ready codebase they can clone and inspect

### What "done" looks like

- Enterprise engineer clicks canary.growdirect.io → reads the pitch
- Clicks "Launch Demo" → lands on canary.growdirect.app
- Clicks through dashboard, alerts, fox cases, employee risk, metrics
- Every page has real data, no empty states, no broken links
- They clone the repo → clean history, no secrets, professional README
- They read the schema → 3 schemas, clean models, proper migrations
- They trace the pipeline → TSP consumers, Chirp rules, Fox cases
- They think: "this is real, and it was built by one person with AI"

---

## Day 1: Clean House

### 1A. Repo cleanup — Canary/

**Delete stale artifacts:**

| Path | Reason |
|---|---|
| `data/` | Empty directory |
| `.worktrees/qa-agent-tier-0/` | Orphaned empty worktree |
| `devops/deploy_reports/DEPLOY_*.txt` (7 files) | Feb 2026 deploy logs |
| `devops/prompts/ux/UX_BUILD_OUTPUT.txt` | Session artifact |
| `devops/prompts/_debug_502_notification_service.txt` | One-off debug log |
| `docs/Canary-Blue-Ocean-Strategy-Analysis.md` | Loose strategic doc — Brain or delete |

**Delete cross-project contamination:**

| Path | Reason |
|---|---|
| `docs/superpowers/data/wpbca-parcels-seed.csv` | Cove data — wrong repo |
| `docs/superpowers/plans/2026-03-23-cove-mvp.md` | Cove plan — wrong repo |
| `docs/superpowers/specs/2026-03-23-cove-governance-platform-design.md` | Cove spec — wrong repo |

Review remaining `docs/superpowers/` (atlas-mcp, qa-agent plans/specs) —
move to `docs/sdds/v2/` or delete if superseded. If empty after, remove dir.

**Delete duplicates:**
- `docs/strategic/Canary_Platform_Overview_v1.0_1.docx` (duplicate with `_1` suffix)

**Decide fate of `static/landing/`:**
- `index.html`, `prototype.html`, `roadshow.html` — these are static site
  pages. If they belong in `growdirectprez.github.io`, delete from here.

**Commit uncommitted changes:**
- `canary/blueprints/square_oauth_wired.py` — merchant-reset onboarded fix (review + commit)
- `templates/app/base_app.html` — template tweaks (review + commit)

**Update .gitignore:**
```
# Add these lines
.claude/settings.local.json
devops/pgadmin-servers.json
```

**Clean caches:**
```bash
find . -name "__pycache__" -type d -not -path "./.venv/*" -not -path "./.venv-mcp/*" -exec rm -rf {} + 2>/dev/null
find . -name ".DS_Store" -delete
find . -name "*.pyc" -not -path "./.venv/*" -delete
```

### 1B. Repo cleanup — GrowDirect/ monorepo root

**Delete root-level junk:**

| File | Action |
|---|---|
| `10584-max.jpeg`, `13328-max.jpeg`, `15658-max.jpeg` | Delete — unlabeled images |
| `2025_Tax_Prep_Workbook.xlsx`, `2025_Tax_Strategy_Brief.docx` | Delete — personal finance |
| `AngeliqueLyle-LP-Integration-Spec.docx` | Move to Angel/docs/ or delete |
| `formspree.rtf` | Delete |
| `Torrance _ San Pedro - Sheet A08...html` | Move to Seacove/docs/ or delete |

**Clean restored git artifacts:**
- `docs/_archive/ip-vault/warchest/site/` (53 files) — restored from git, delete from HEAD
- `docs/_archive/workorders/` — same

**Batch commit Brain changes (114 modified + 17 new wiki articles):**
```bash
git add Brain/ Angel/knowledge/ .obsidian/
git commit -m "brain: batch wiki updates — Cove research, Angel knowledge, project MOCs"
```

### 1C. Secrets audit

**Current state: GOOD.** .env was never committed. No hardcoded API keys in code.

**Fix:** Hardcoded dev passwords in seed scripts need env var fallbacks
(they already have them in test_reset.py, but level_b_demo.py hardcodes):
```python
# level_b_demo.py line 35 — change:
PG_PASS = "canary_dev_2026"
# to:
PG_PASS = os.environ.get("SEED_PG_PASS", "canary_dev_2026")
```

**For public repo, also:**
- Verify no secrets in git history: `git log -p --all -S 'sq0csb' -- '*.py'`
- Verify .env.template has placeholder values only (it does)
- Add `SECURITY.md` with responsible disclosure contact
- Add `LICENSE` file (decide: MIT, Apache 2.0, or proprietary)

---

## Day 2: Demo Data Pipeline

### 2A. Enhance level_b_demo.py for richer data

Current: single Saturday scenario at Torrance. Enhance:

- **Multiple fox cases** in different states (open, investigating, escalated, closed)
  — 4-6 cases so the Fox case list looks populated
- **More alert variety** — 2-3 alerts per category (cash variance, after-hours,
  excessive discounts, off-clock) not just refunds
- **Second location data** — Redondo Beach (LOC_REDONDO_ID already defined) with
  its own transactions and different risk profile
- **Employee risk spread** — Steve high (0.6-0.8), one medium (0.3-0.5), rest low
- Keep existing seed IDs stable, add new `demo-` prefixed IDs
- Keep idempotent (ON CONFLICT DO NOTHING)

### 2B. Create seed_time_advance.py (NEW)

File: `devops/scripts/seed_time_advance.py`

Each demo reset should produce current-looking data, not a frozen 90-day window.

**Logic:**
1. Read most recent `metric_date` in `daily_metrics`
2. Generate daily_metrics + employee_daily_metrics from there to today
3. Generate period_metrics (weekly + monthly rollups) for new data
4. Recalculate baselines to include new data
5. Create 1-2 new alerts + fox cases per month of advanced time

**Usage:**
```bash
python devops/scripts/seed_time_advance.py                     # advance to today
python devops/scripts/seed_time_advance.py --target 2026-05-15 # advance to date
python devops/scripts/seed_time_advance.py --days 30           # advance N days
```

Use same realistic cafe patterns from seed_dashboard_sandbox.py (weekend
bumps, Sam Chen elevated risk, occasional anomaly days).

### 2C. Add --demo flag to test_reset.py

```bash
python devops/scripts/test_reset.py --demo
```

The `--demo` flag:
1. Purge (existing behavior)
2. Run level_b_demo.py
3. Run seed_dashboard_sandbox.py
4. Run seed_time_advance.py
5. Print summary with row counts

Keep `--seed` (purge + level_b_demo only) and bare (purge only) unchanged.

### 2D. Create demo-reset.sh (one-liner)

File: `devops/scripts/demo-reset.sh`

```bash
#!/bin/bash
set -euo pipefail
echo "=== Canary Demo Reset ==="
python devops/scripts/test_reset.py --demo
echo ""
echo "Seeding Square sandbox..."
python devops/scripts/seed_full_sandbox.py --reset --phase all
echo ""
echo "Running health checks..."
bash devops/scripts/health-check-all.sh
echo ""
echo "=== Demo Ready ==="
echo "Visit: https://canary.growdirect.app"
```

Runnable inside Docker:
```bash
docker compose -f devops/docker-compose.localhost.yml exec flask \
  bash devops/scripts/demo-reset.sh
```

---

## Day 3: Deploy to Mac Mini

### 3A. Create production compose

File: `devops/docker-compose.production.yml`

Based on `docker-compose.localhost.yml` but production-hardened:

- No volume mounts for source code (baked into image)
- No hot-reload
- `CANARY_ENV=production`
- `CANARY_HOST=canary.growdirect.app`
- Gunicorn: 2 workers, 4 threads (Mini has limited RAM)
- No nginx container (Cloudflare handles TLS termination)
- Flask listens on 5001, Cloudflare tunnel points to localhost:5001
- Health check endpoint on `/health`
- `restart: unless-stopped` on all services
- Square sandbox connection:
  - `SQUARE_ENVIRONMENT=sandbox`
  - `SQUARE_REDIRECT_URL=https://canary.growdirect.app/oauth/callback`

### 3B. Create Cloudflare tunnel script for Mac Mini

File: `devops/scripts/setup_production_tunnel.sh`

Adapt `setup_qa_tunnel.sh` for the Mac Mini deployment:

| Setting | QA (existing) | Production (new) |
|---|---|---|
| Host | 192.168.10.117 (iMac) | 192.168.10.102 (Mac Mini) |
| Tunnel name | `canary-qa` | `canary-production` |
| Hostname | `qa.growdirect.app` | `canary.growdirect.app` |
| Flask port | 5001 | 5001 |

The script should:
1. SSH to Mac Mini
2. Install/verify cloudflared
3. Create tunnel `canary-production`
4. Route `canary.growdirect.app` → localhost:5001
5. Set up as systemd/launchd service (persistent across reboots)
6. Verify with health check

### 3C. Create deploy script

File: `devops/scripts/deploy.sh`

Deploys the current code to the Mac Mini:

```bash
#!/bin/bash
# Canary LP — Deploy to Mac Mini (192.168.10.102)
set -euo pipefail

MINI_HOST="192.168.10.102"
MINI_USER="gclyle"
DEPLOY_DIR="/opt/canary"  # or ~/GrowDirect/Canary on the Mini

echo "=== Canary Deploy to Mac Mini ==="

# 1. Build Docker image locally
docker build -t canary-flask -f Dockerfile .

# 2. Save + transfer image (or use registry)
docker save canary-flask | ssh ${MINI_USER}@${MINI_HOST} 'docker load'

# 3. SSH in and restart stack
ssh ${MINI_USER}@${MINI_HOST} << 'REMOTE'
  cd ${DEPLOY_DIR}
  docker compose -f devops/docker-compose.production.yml pull
  docker compose -f devops/docker-compose.production.yml up -d
  sleep 10
  docker compose -f devops/docker-compose.production.yml exec flask \
    bash devops/scripts/demo-reset.sh
REMOTE

echo "=== Deploy Complete ==="
echo "Verify: https://canary.growdirect.app/health"
```

### 3D. Square sandbox for production demo

Verify the OAuth flow works with Cloudflare tunnel:
- `SQUARE_REDIRECT_URL=https://canary.growdirect.app/oauth/callback`
- Square sandbox OAuth goes through `connect.squareupsandbox.com`
- Ensure `square_oauth_wired.py` uses sandbox URLs when `SQUARE_ENVIRONMENT=sandbox`

Add **demo mode fallback**: if Square sandbox is flaky during a live demo,
a `?demo=1` query param (or a toggle in settings) should skip OAuth and
go straight to pre-seeded data. The merchant-reset already resets onboarded
state — demo mode just needs to bypass the connect step.

---

## Day 4: Polish + Verify

### 4A. UI polish

Walk through every page with seeded data and verify:

**Dashboard:**
- All widgets render (no empty states)
- Period-over-period comparisons show (time-advance seeder makes this work)
- Employee risk heatmap shows differentiation (Steve=red, others green/yellow)

**Alerts:**
- 15+ alerts across multiple categories
- Each clickable with detail view showing triggering transaction(s)
- Mix of statuses: new, acknowledged, investigating, resolved

**Fox Cases:**
- 4-6 cases in various states
- At least one with full timeline (opened → evidence → escalated → resolved)
- Evidence items reference real transactions

**General:**
- No broken links or 404s
- No console errors
- Fast loading (all data local)
- Works on tablet (booth demo scenarios)
- Dark theme consistent with GrowDirect brand

### 4B. README for public consumption

Rewrite `README.md` for the enterprise audience:

```markdown
# Canary LP — Loss Prevention Analytics for Square Merchants

Real-time transaction monitoring, anomaly detection, and case management
for Square POS merchants. Built as a prototype demonstrating what's
possible with modern AI-assisted development.

## Architecture

- **Stack:** Python 3.12 / Flask 3 / SQLAlchemy 2.0 / PostgreSQL 17 / Valkey 8
- **Pipeline:** Triple Subscriber Pipeline (TSP) — 4 Valkey stream consumers
  processing webhook events in real time
- **Detection:** Chirp engine — 29 rules across 8 categories with 3 execution tiers
- **Investigation:** Fox case management with evidence-grade documentation
- **Analytics:** Multi-dimensional metrics with employee risk scoring

## Schema

Three PostgreSQL schemas:
- `canary_app` — merchants, employees, locations, detection rules, alerts, cases
- `canary_sales` — transactions, line items, tenders, refunds, cash drawer events
- `canary_metrics` — daily/period metrics, baselines, risk scores, scorecards

## Quick Start

[Docker setup instructions here]

## Live Demo

https://canary.growdirect.app

## Built By

Solo founder prototype — designed to demonstrate rapid AI-assisted development
of domain-specific analytics platforms. See the journey at growdirect.io.
```

### 4C. Health checks + verification

```bash
# Infrastructure
bash devops/scripts/health-check-all.sh

# Data verification
psql -h localhost -U canary -d canary -c "
  SELECT 'daily_metrics' as tbl, count(*) FROM canary_metrics.daily_metrics
  UNION ALL SELECT 'alerts', count(*) FROM canary_app.alerts
  UNION ALL SELECT 'fox_cases', count(*) FROM canary_app.fox_cases
  UNION ALL SELECT 'transactions', count(*) FROM canary_sales.transactions
  UNION ALL SELECT 'employees', count(*) FROM canary_app.employees;
"
```

**Minimums for primetime:**

| Table | Min rows |
|---|---|
| daily_metrics | 180+ |
| employee_daily_metrics | 400+ |
| alerts | 15+ |
| fox_cases | 4+ |
| transactions | 20+ |
| employees | 5 |
| period_metrics | 20+ |

### 4D. End-to-end verification

1. Open `canary.growdirect.io` → static site loads, looks professional
2. Click "Launch Demo" → redirects to `canary.growdirect.app`
3. App loads with login/connect screen
4. Click through every nav item — no empty states
5. Clone repo on a fresh machine → clean, no secrets, builds in Docker
6. `docker compose up` → app starts, health check passes

---

## Files created / modified

| File | Action | Day |
|---|---|---|
| `devops/scripts/seed_time_advance.py` | **NEW** | 2 |
| `devops/scripts/demo-reset.sh` | **NEW** | 2 |
| `devops/docker-compose.production.yml` | **NEW** | 3 |
| `devops/scripts/setup_production_tunnel.sh` | **NEW** | 3 |
| `devops/scripts/deploy.sh` | **NEW** | 3 |
| `SECURITY.md` | **NEW** | 1 |
| `LICENSE` | **NEW** | 1 |
| `README.md` | Rewrite for public | 4 |
| `devops/scripts/test_reset.py` | Add `--demo` flag | 2 |
| `devops/seeds/level_b_demo.py` | Richer demo data + env var passwords | 2 |
| `.gitignore` | Add local config entries | 1 |
| Various | Cleanup deletes | 1 |

## Key references

- Mac Mini: 192.168.10.102 (deploy target)
- iMac: 192.168.10.117 (existing QA tunnel)
- Square sandbox merchant: MLE55GCYANCYT
- Demo seed IDs: `demo-` prefix (see level_b_demo.py)
- Database: `canary` — schemas `canary_app`, `canary_sales`, `canary_metrics`
- Dev credentials: canary / canary_dev_2026
- Existing tunnel script: `devops/scripts/setup_qa_tunnel.sh` (adapt for production)
- Compose for dev: `devops/docker-compose.localhost.yml`
- Docker entry: `./devops/scripts/dev.sh up`
- Static site repo: `growdirectprez.github.io` (separate from monorepo)



---

## The Second Demo: Behind the Curtain

The enterprise audience doesn't just want to see the app. They want to see
HOW it was built — the agentic workflow, the knowledge pipeline, the factory
process. This is the part that makes them say "I need to do this at my company."

### What already exists (leverage these)

1. **Atlas Browser** (`/ops/atlas`) — 60+ architecture diagrams organized by
   category (pipeline, lifecycle, orchestration, infrastructure, journey,
   protocol). Already renders SVGs with category pills and navigation.

2. **12 MCP Servers** — owl, chirp, alert, fox, analytics, identity, tsp,
   raas, bff, condor, atlas, ops. Each has a manifest endpoint. The Owl
   server alone exposes: ask, search, knowledge_search, dashboard, score_payment.

3. **QA Agent** (`/ops/qa`) — Claude-powered interactive test assistant with
   MCP tool access. Live conversational interface.

4. **Ops Console** (`/ops/test-lab`) — scenario fire/batch/poll endpoints
   for testing the detection pipeline.

5. **16 SDDs** in `docs/sdds/v2/` — architecture, chirp, fox, owl, tsp,
   analytics, alert, identity, raas, goose, etc.

6. **135 Brain wiki articles** — curated knowledge graph in Obsidian.

7. **Memory Bus** — pgvector-backed memory store with 10 memory types,
   4 layers (corp/canary/cove/shared), 11 domains. Embeddings via Ollama
   (qwen3-embedding:8b, 1024-dim vectors).

8. **Factory Pipeline** — 9-stage pipeline (preflight → research → blueprint →
   tdd → assembly → verify → qa → ship → close) defined in factory-manifest.json.

9. **Content Engine** — CLI for scan, dedup, triage, ingest, registry. Bridges
   filesystem to Brain knowledge layer.

### What to build: "The Method" demo walkthrough

Create a new ops page: `/ops/method` (or repurpose the test-lab as the demo hub).

This page tells the story visually as a click-through walkthrough:

**Panel 1: The Factory Pipeline**
- Render the 9-stage pipeline as a visual flow (use Atlas SVGs or build new)
- Each stage expandable: inputs, outputs, MCP tools used, skill invoked
- Show a real GRO issue flowing through the pipeline (pick one that shipped)

**Panel 2: Documentation as Code**
- SDD → chunks → pgvector embeddings → similarity search
- Show the 16 SDDs as cards, click one to see the real content
- Show how `content-engine registry check "chirp detection"` finds related articles
- Show a pgvector similarity query in action (Owl knowledge_search)

**Panel 3: The Knowledge Graph**
- Visualize the Brain wiki as a network (135 nodes)
- Use the Obsidian graph data or build a D3 force-directed graph
- Click a node → shows the wiki article
- Show connections: SDD → wiki articles → code files → memory chunks

**Panel 4: Agentic Workflow**
- Show the 12 MCP servers as a service mesh
- Atlas SVG `fig-o01-service-mesh.svg` already exists
- Show a live demo: type a query into QA Agent, watch it call MCP tools,
  trace the tool chain, show the result
- This is the "wow" moment — a real AI agent using real tools on real data

**Panel 5: The Numbers**
- Auto-generated stats dashboard:
  - X lines of Python code (count via `find . -name "*.py" | xargs wc -l`)
  - 16 SDDs, 135 wiki articles, 60+ architecture diagrams
  - 29 detection rules, 3 schemas, 27 Alembic migrations
  - 12 MCP servers, 9 factory stages
  - Built by: 1 founder + AI pair programming
  - Timeline: months, not years

### Implementation approach: reverse-engineer elegance

Don't build a new frontend framework. Use what Canary already has:

1. **Jinja2 templates** with the existing dark theme
2. **Alpine.js** for interactivity (accordion panels, tab switching)
3. **Atlas SVGs** embedded directly (already styled for dark theme)
4. **Live API calls** to MCP manifest endpoints for real data
5. **Owl knowledge_search** endpoint for live similarity search demo
6. **QA Agent chat** already works — just needs a curated starting prompt

The demo page should be ONE template (`templates/ops/method.html`) with
a corresponding blueprint route. No new dependencies.

### Curated demo script

Prepare a click-through script for the presenter:

1. Start at canary.growdirect.io → "This is our public face"
2. Click "Launch Demo" → canary.growdirect.app dashboard
3. Walk through: alerts → fox case → employee risk → metrics
4. "Now let me show you how this was built"
5. Navigate to `/ops/method`
6. Walk through the 5 panels
7. Live demo: ask Owl a question, watch it search
8. Live demo: fire a test scenario, watch Chirp detect it
9. "One founder. AI pair programming. A few months. Questions?"

### Day assignment

This is Day 2-3 work, parallel to the data pipeline:
- Day 2: Build the `/ops/method` template with panels 1-3 (static content,
  Atlas SVGs, SDD cards)
- Day 3: Wire up panels 4-5 (live QA Agent, auto-stats), polish transitions
- Day 4: Rehearse the demo script end-to-end

---

## Updated execution order

| Day | Morning | Afternoon |
|---|---|---|
| 1 | Repo cleanup (both repos) | Secrets audit + .gitignore + commit batch |
| 2 | Demo data pipeline (time-advance, richer seeds, --demo flag) | Method page panels 1-3 (factory, docs-as-code, knowledge graph) |
| 3 | Deploy to Mac Mini (compose, tunnel, demo-reset) | Method page panels 4-5 (agentic, numbers) + Square sandbox verify |
| 4 | README rewrite + UI polish pass | End-to-end walkthrough + rehearsal |



---

## The Real Pitch (Read This First)

Canary is not the product. Canary is the PROOF.

The product is: **One domain expert + AI tools = a leave-behind system that
the client's own people can understand, maintain, and extend.**

The audience (enterprise retail engineers) already knows how to build LP
systems. What they don't know is how to reposition their 50-person engineering
org when one consultant with institutional knowledge can prototype in months
what used to take their team a year.

The demo answers three questions:
1. **What did you build?** → Canary (the app)
2. **How did you build it?** → The Method (factory pipeline, agentic roles,
   Brain knowledge graph, SDDs, memory bus, 45 skills)
3. **What do you leave behind?** → A self-documenting system their engineers
   can clone, read, and own

That third question is the sale. The CLAUDE.md files, the Brain wiki, the
SDDs, the memory bus — those aren't internal scaffolding. They're the
**maintenance manual** that makes the handoff work. An enterprise team
inheriting Canary should be able to:
- Read CLAUDE.md and understand the architecture in 10 minutes
- Read any SDD and know exactly what a subsystem does
- Query the memory bus and get context on past decisions
- Open the Brain wiki and navigate the knowledge graph
- Run the factory pipeline on a new GRO issue and watch it work

If those artifacts are messy, the "leave-behind" story falls apart.

---

## Day 1 (revised): Knowledge Layer Cleanup

This is now the FIRST priority — before demo data, before deployment.
The knowledge layer IS the differentiator.

### 1A. Brain wiki audit

**Current state:** 135 wiki articles. Breakdown by prefix:
- angel (37) — real estate intelligence
- cove (31) — HOA governance  
- coac (18) — COAC bylaws/governance
- foundation (10) — structural/foundation docs
- card (9) — card processing
- secure (6) — legacy Secure product
- peninsula (5) — Angel neighborhood content
- canary (5) — **only 5 Canary articles for the flagship product**
- wpbca (5) — HOA association
- seacove (3) — SketchUp project
- misc (6) — one-offs

**Problem:** Canary has 5 wiki articles. Angel has 37. The product we're
demoing has the thinnest knowledge layer. This undercuts the leave-behind story.

**Fix — create these Canary wiki articles (from existing SDDs + code):**

| Article | Source |
|---|---|
| `canary-tsp-pipeline.md` | docs/sdds/v2/webhook-pipeline.md + code |
| `canary-chirp-rules.md` | docs/sdds/v2/chirp.md + detection_rules |
| `canary-fox-case-management.md` | docs/sdds/v2/fox.md + code |
| `canary-owl-search.md` | docs/sdds/v2/owl.md + code |
| `canary-metrics-engine.md` | docs/sdds/v2/analytics.md + code |
| `canary-square-integration.md` | docs/sdds/v2/identity.md + OAuth code |
| `canary-goose-credit.md` | docs/sdds/v2/goose.md + code |
| `canary-factory-workflow.md` | Factory.md + factory-manifest.json |
| `canary-mcp-layer.md` | 12 MCP servers, manifest endpoints |
| `canary-deployment.md` | Docker compose, tunnel, health checks |

That brings Canary to 15 wiki articles — still lean, but covers every major
subsystem. Each article should follow the Brain/templates/wiki-article.md
template and be readable by an enterprise engineer on day one.

**Also clean up:**
- Remove `-raw` suffix articles that are unprocessed intake dumps (the angel
  neighborhood `-raw` files should be either processed or archived)
- Verify all 7 MOCs in Brain/projects/ link to current wiki articles
- Run `content-engine/engine.py registry build` to rebuild REGISTRY.json

### 1B. CLAUDE.md files — rewrite as onboarding guides

These are currently written for AI agents. Rewrite them so a HUMAN engineer
can read them as onboarding documentation:

**Root CLAUDE.md (200 lines):** Good structure. Add:
- "New Engineer Start Here" section at top
- Explain the Documentation as Code flow for humans
- Link to Brain/projects/Method.md as the methodology overview
- Explain what the memory bus does and how to query it

**Canary/CLAUDE.md (335 lines):** Already comprehensive. Enhance:
- Add "Architecture at a Glance" diagram reference (Atlas fig-o01)
- Add "First 30 Minutes" quickstart for a new engineer
- Explain what each of the 3 schemas contains and why
- Link to the 16 SDDs as the subsystem documentation
- Explain the demo-reset workflow

**Cove/CLAUDE.md (433 lines):** Review for currency but lower priority for
this demo.

### 1C. Memory bus cleanup

**Tables:**
- `alx_sessions` — session lifecycle records
- `alx_memories` — decision/finding/context/architecture memories with
  pgvector embeddings (1024-dim, qwen3-embedding:8b)

**Cleanup tasks:**
- Count total memories: `SELECT memory_type, count(*) FROM alx_memories GROUP BY 1`
- Delete stale/abandoned sessions: `DELETE FROM alx_sessions WHERE status = 'abandoned'`
- Verify embedding quality: spot-check a few similarity searches
- Document the memory types and what each contains

**For the demo:** The memory bus should be queryable live. Prepare 3-4
canned queries that show impressive results:
- "What decisions were made about the detection rule engine?"
- "How does the TSP pipeline work?"
- "What's the data model for fox cases?"

### 1D. .claude/ settings cleanup

**Root .claude/:**
- `launch.json` — review, keep if useful
- `scheduled_tasks.lock` — add to .gitignore
- `settings.local.json` — add to .gitignore
- `skills/` (45 factory skills) — these ARE the product, keep clean
- `worktrees/` — gitignored, fine

**Canary/.claude/:**
- `settings.json` — permission config, keep
- `settings.local.json` — local overrides, gitignore

### 1E. SDDs — verify completeness

16 SDDs in `Canary/docs/sdds/v2/`:
```
alert.md, alx.md, analytics.md, architecture.md, chirp.md,
data-model.md, external-identities.md, fox.md, goose.md,
identity.md, multi-pos-architecture-proof.md, ops.md, owl.md,
raas.md, ui-bff.md, webhook-pipeline.md
```

**Quick audit:** Each SDD should have:
- Status marker (draft/current/deprecated)
- Last-updated date
- Summary readable by enterprise engineer
- Link to relevant Atlas diagrams
- Link to relevant wiki articles

Fix any that are stale or missing these fields.

### 1F. Brain/raw/inbox triage

36 files in `Brain/raw/inbox/`. These are unprocessed intake files — many are
from Lyle's enterprise consulting career (Kroger, Secure, Appriss):

**Keep + process:** Files that tell the founder story
- `kroger-*` files (8 files) — show enterprise LP domain expertise
- `secure-*` files (8 files) — show the Secure product lineage
- `appriss-*` file — industry data spec context

**Keep as-is:** Currently processed files
- `brain-health-check-*` — meta, keep

**Archive or delete:** One-off intake files that don't serve the demo

**For the demo story:** The raw inbox files ARE the institutional knowledge
that got encoded into Canary. "These Kroger specs from 2017? They became
detection rules. That Secure architecture? It became the TSP pipeline.
The domain expertise didn't disappear — it got encoded."

---

## Updated 4-Day Plan

| Day | Morning | Afternoon |
|---|---|---|
| **1** | Brain wiki: create 10 Canary articles from SDDs | CLAUDE.md rewrites + memory bus cleanup |
| **2** | Demo data pipeline (seeds, time-advance, --demo flag) | Method page panels 1-3 (factory, docs-as-code, knowledge graph) |
| **3** | Deploy Mac Mini (compose, tunnel, demo-reset) | Method page panels 4-5 + Square sandbox verify |
| **4** | README + repo cleanup + secrets audit | End-to-end walkthrough: app → method → knowledge → leave-behind |

### The closer

The last slide of the demo isn't a feature list. It's:

> "Everything you just saw — the app, the documentation, the knowledge graph,
> the factory pipeline, the 45 AI skills — this is what your client gets when
> the engagement ends. Not a PowerPoint. Not a handoff meeting. A running
> system with a knowledge base their team can actually maintain.
>
> Your people with 20 years of operational knowledge? They're not being
> replaced. They're being repositioned. Give them the right tools and they
> become the builders."



---

## Method Page: "The Gateway Pattern" Panel

### The point

Square isn't the product. Square is the reference implementation. 149 webhook
events, public API, sandbox — it's the proving ground. The pattern is: take
ANY system that emits events, point agents at the API spec, build the
canonical model, trace every data element end to end.

### What to show (already built, just needs surfacing)

**Step 1: API Spec → Parser Generation**
- Source: Square's 149 webhook event types
- Show: `canary/services/parsers/` — the agent-built parsers
- Show: `docs/api/canary-api-v1.yaml` — the API contract
- Frame: "Agents read the spec, built the parsers. Swap Square for SAP and
  the same agents build SAP parsers."

**Step 2: Parsers → Canonical Model (CRDM)**
- Source: Raw Square JSON payloads
- Show: The CRDM — 99 tables across 3 schemas (app, sales, metrics)
- Show: `canary/models/` — 60+ SQLAlchemy models
- Show: Atlas diagram `fig-i02-database-schema-architecture.svg`
- Frame: "The canonical model is what survives the source system. Square goes
  away, the CRDM stays. That's the leave-behind."

**Step 3: Field Registry — End-to-End Data Lineage**
- Source: `docs/field-registry.json` + `docs/field-registry.md`
- Source: `docs/field-registry/` subdirectory (extraction docs, coverage matrix)
- Show: Every field traced from Square webhook JSON → parser → canonical
  table → downstream consumer (Chirp rules, Fox evidence, metrics engine)
- Show: `docs/webhook-usecase-map.json` — which events drive which use cases
- Frame: "This is the data dictionary that Big 4 teams spend 6 months
  building manually and still get wrong. Agents built it by scanning the
  codebase. It stays current because agents maintain it."

**Step 4: Detection Rules on Top of Canonical Data**
- Source: 29 Chirp rules across 8 categories
- Show: Rules reference canonical model fields, not Square-specific fields
- Frame: "Detection logic is decoupled from the source system. Change the
  POS, keep the rules. That's the architecture that enterprises need and
  never build because the data dictionary is always wrong."

**Step 5: Brain Captures the Business Meaning**
- Show: Wiki articles that explain what each field MEANS in business terms
  (not just the technical mapping)
- Show: Memory bus queries returning context about detection rules
- Frame: "The canonical model tells you WHERE the data goes. The Brain
  tells you WHY it matters. Both are queryable. Both persist after the
  engagement ends."

### Visual: The Gateway Pattern (generic)

```
┌─────────────────┐
│  Source System   │ ← Any: Square, SAP, Oracle, Shopify, custom
│  (Event Stream)  │
└────────┬────────┘
         │ webhooks / events / API
         ▼
┌─────────────────┐
│  Agent Parsers   │ ← Generated from API spec by agents
│  (TSP Pipeline)  │
└────────┬────────┘
         │ canonical records
         ▼
┌─────────────────┐
│  Canonical Model │ ← CRDM: source-agnostic, survives system swap
│  (CRDM)          │
└────────┬────────┘
         │ field references
    ┌────┴────┬──────────┐
    ▼         ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐
│ Detect │ │ Report │ │ Manage │
│ (Chirp)│ │(Metrics│ │  (Fox) │
│        │ │Engine) │ │        │
└────────┘ └────────┘ └────────┘
         │
         ▼
┌─────────────────┐
│  Knowledge Layer │ ← Brain + Memory Bus + Field Registry
│  (Leave-Behind)  │    "What it means, why it matters"
└─────────────────┘
```

This diagram should be rendered as an Atlas-style SVG on the Method page.
The left side shows the Canary implementation (Square → TSP → CRDM).
The right side shows the generic pattern (Any System → Agents → Canonical).

### Files to reference

| Artifact | Path |
|---|---|
| Field registry (JSON) | `docs/field-registry.json` |
| Field registry (readable) | `docs/field-registry.md` |
| Coverage matrix | `docs/field-registry/square-coverage-matrix.md` |
| Webhook use-case map | `docs/webhook-usecase-map.json` |
| Parser code | `canary/services/parsers/` |
| Models (canonical) | `canary/models/sales/`, `canary/models/app/`, `canary/models/metrics/` |
| API spec | `docs/api/canary-api-v1.yaml` |
| Schema ERDs | `docs/erds/` (7 Mermaid diagrams) |
| CRDM mapping doc | War Chest source: `the-crdm.html` (git fd3db16) |
| Detection rules | `canary/services/chirp/` + SDD `docs/sdds/v2/chirp.md` |

