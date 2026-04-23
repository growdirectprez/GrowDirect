# Canary Goes Primetime — Consolidated Dispatch
## Date: 2026-04-23
## Window: 3–4 days
## Supersedes: all prior dispatches dated 2026-04-22

---

## What this is

One founder's loss prevention platform goes in front of seasoned enterprise
retail engineers. They'll see:

1. **canary.growdirect.io** — static product site (GitHub Pages)
2. **canary.growdirect.app** — live clickable demo (Flask, Mac Mini, Cloudflare)
3. **The Method** — how one domain expert + AI agents built this
4. **The GitHub repo** — clean, cloneable, self-documenting

The pitch isn't "use Canary." The pitch is: "Your domain experts with 20
years of institutional knowledge can't get engineering time. Give them
this toolkit and they ship in weeks. When the engagement ends, the client
gets a running system with a knowledge base their team can actually
maintain. Not a PowerPoint. A leave-behind."

Canary is the proof. The Method is the product. The Brain is the moat.

---

## Existing dispatches (status + disposition)

| File | Status | Disposition |
|---|---|---|
| `dispatch-code-2026-04-22-demo-reseed.md` (root) | Ready to execute | **USE AS-IS** for Track A reseed. Best-scoped dispatch in the stack. |
| `dispatch-brain-scaffold-design.md` (docs/) | Phase 1 DONE | **CONTINUE** — Phase 2 next. Brain assessment at `Brain/raw/inbox/_brain-assessment-v1.md`. |
| `playbook-brain-scaffold-design.md` (docs/) | Source of truth for GRO-520 | **REFERENCE** — don't duplicate, follow it. |
| `dispatch-site-2026-04-22.md` (docs/dispatches/) | Not started | **ABSORBED** into Track A below. Delete after this dispatch executes. |
| `dispatch-demo-prep-2026-04-22.md` (docs/dispatches/) | Planning only, 880 lines | **SUPERSEDED** by this dispatch. Delete after execution. |
| `dispatch-api-docs-gateway-2026-04-22.md` (docs/dispatches/) | Not started | **ABSORBED** into Track A. Delete after. |
| `dispatch-vscode-library-narrative-2026-04-22.md` (docs/dispatches/) | Not started | **ABSORBED** into Track A. Delete after. |
| `playbook-method-katz-reverse-engineer.md` (docs/) | Not started | **PARKED** — future work, not on critical path. |
| `playbook-retail-ops-model.md` (docs/) | Not started | **PARKED** — feeds story but doesn't ship this week. |
| `playbook-solex-square-merchant.md` (docs/) | Not started | **PARKED** — design partner play, post-Primetime. |

---

## Two tracks, one goal

**Track A: Ship It** — everything the audience clicks on works.
**Track B: Leave-Behind** — everything the audience clones and reads is clean.

Track C (code hardening) is a separate dispatch after A+B land.

---

# TRACK A: SHIP IT

## A1. Demo Reseed (Day 1 — Code session)

**Execute `dispatch-code-2026-04-22-demo-reseed.md` as written.** That
dispatch is 400+ lines, fully scoped, commit-by-commit. Summary:

- Rewrite `devops/seeds/level_b_demo.py` for consolidated single-DB schema
  (`canary` DB, 3 schemas: app/sales/metrics)
- Schema-qualify all inserts, env-var credentials, explicit timestamps
- Suspicious Steve's 11-week arc: baseline → drift → pattern → active
  (Feb 1 → today), risk score 0.00 → 0.92
- 4 other employees stay clean (risk < 0.20) for contrast
- 3 locations (Torrance, Redondo, Rolling Hills)
- ~1,300 transactions, 8-12 alerts, 1 fox case with evidence chain
- Full metrics population: daily_metrics, employee_daily_metrics,
  hourly_metrics, entity_risk_scores, risk_score_history, baselines
- Wire reseed into `/oauth/merchant-reset` with `{reseed: true}` flag
- Integration tests for idempotency + coverage + Steve arc
- 4 commits, definition of done at bottom of that dispatch

**After reseed completes, verify every screen:**

| Screen | Expected |
|---|---|
| `/home` | Alerts, risk trends, Saturday peaks |
| `/chirps` | 8-12 alerts across categories, various severity |
| `/owl` | 11-week baselines, Steve at top of risk leaderboard |
| `/fox` | Open case for Steve, 3+ evidence items, timeline |
| `/employees` | 5 employees, Steve's trend ramping, others flat |
| `/metrics` | Period-over-period populated, no empty states |

## A2. API Docs Gateway (Day 1 — same Code session)

From `dispatch-api-docs-gateway-2026-04-22.md`:

1. Update `docs/api/canary-api-v1.yaml` to match current blueprints
2. Serve interactive Redoc at `/devops/api`
3. Wire into ops nav
4. Commit: `feat(docs): update OpenAPI spec + serve Redoc at /devops/api (GRO-169)`

## A3. Static Site Updates (Day 2 — Code session in growdirectprez.github.io)

### A3a. Technical Library

Restore War Chest source HTML from GrowDirect monorepo (git commit `fd3db16`,
path `docs/_archive/ip-vault/warchest/site/`). Reformat 6 docs into a
Technical Library with shared dark-theme stylesheet:

| Source file | Library title |
|---|---|
| `the-crdm.html` | The CRDM — Canonical Reference Data Model |
| `the-architecture.html` | Platform Architecture |
| `how-we-build.html` | How We Build — The Factory |
| `eljeffe.html` | El Jeffe — Detection Protocol |
| `the-chirp.html` | The Chirp — Detection Engine |
| `canary_technical_roadshow_v1.0.html` | Technical Roadshow |

Rules: preserve real content (don't regenerate), shared `canary-docs.css`,
consistent nav across all docs, human-readable filenames.

### A3b. Tech Library Narrative Uplift

From `dispatch-vscode-library-narrative-2026-04-22.md`: the 5 existing
tiles (Atlas, CRDM, Field Registry, Detection Catalog, Risk Dictionary)
need narrative introductions that tell the story, not just show the data.
Frame each as "here's what agents built from the API spec."

### A3c. Portfolio Section

Add to `index.html` (growdirect.io hub). Replace "What's Built" section:

- **Canary LP** — Loss prevention analytics. 29 rules, 8 categories, TSP pipeline. Link to canary.growdirect.io.
- **Cove** — HOA governance. 81 lots, parcel GIS, document management. Coming soon.
- **Angel** — Real estate intelligence. pgvector similarity, agent sidecar. Coming soon.
- **Consulting** — Solo founder, full-stack builder. 20+ years retail data platforms. The Method story.

### A3d. Canary Gated Section

Update `canary/index.html` gated area (password: `canary2026`):
- Clickable links to all 6 Technical Library docs
- Remove sales strategy content
- Add "Launch Demo" button → `https://canary.growdirect.app`

### A3e. Deploy

Commit + push to trigger GitHub Pages. Verify both sites.

## A4. Mac Mini Deployment (Day 2-3 — Code session)

### A4a. Production Compose

Create `devops/docker-compose.production.yml` based on `localhost.yml`:
- No source volume mounts (baked into image)
- `CANARY_ENV=production`, `CANARY_HOST=canary.growdirect.app`
- `SQUARE_ENVIRONMENT=sandbox`
- `SQUARE_REDIRECT_URL=https://canary.growdirect.app/oauth/callback`
- Gunicorn: 2 workers, 4 threads
- No nginx (Cloudflare handles TLS)
- `restart: unless-stopped`

### A4b. Cloudflare Tunnel

Adapt `devops/scripts/setup_qa_tunnel.sh` → `setup_production_tunnel.sh`:

| Setting | QA (existing) | Production (new) |
|---|---|---|
| Host | 192.168.10.117 (iMac) | 192.168.10.102 (Mac Mini) |
| Tunnel name | `canary-qa` | `canary-production` |
| Hostname | `qa.growdirect.app` | `canary.growdirect.app` |

Set up as persistent service (survives reboot).

### A4c. Deploy Script

Create `devops/scripts/deploy.sh`:
- Build image locally
- `docker save | ssh | docker load` to Mini
- Restart compose stack
- Run `demo-reset.sh`
- Health check

### A4d. Demo Reset One-Liner

Create `devops/scripts/demo-reset.sh`:
```bash
#!/bin/bash
set -euo pipefail
echo "=== Canary Demo Reset ==="
python devops/scripts/test_reset.py --seed
python devops/seeds/level_b_demo.py --wipe
echo "Running health checks..."
bash devops/scripts/health-check-all.sh
echo "=== Demo Ready ==="
```

### A4e. Square Sandbox Verify

- OAuth flow works through Cloudflare tunnel
- `square_oauth_wired.py` uses `connect.squareupsandbox.com` when sandbox
- Add demo mode fallback: `?demo=1` skips OAuth, goes to pre-seeded data

### A4f. End-to-End Verify

1. canary.growdirect.io loads → click "Launch Demo"
2. Redirects to canary.growdirect.app
3. Every nav item populated, no empty states
4. No console errors, no broken links

## A5. Method Page (Day 3 — Code session)

### Purpose

The page that makes enterprise architects lean forward. Not "how we
built Canary" — "how we replace a $20M transformation program."

### Route: `/ops/method`

One Jinja2 template (`templates/ops/method.html`), one blueprint route.
No new dependencies. Alpine.js for interactivity. Atlas SVGs embedded.

### Panel 1: The Factory Pipeline
- 9-stage visual flow (preflight → close)
- Each stage: inputs, outputs, MCP tools, role
- Show a real GRO issue flowing through
- Source: `factory-manifest.json`, `Brain/projects/Factory.md`

### Panel 2: The Gateway Pattern
- Square as reference implementation (149 events, public API)
- Agent-built parsers → CRDM (99 tables) → Field Registry → Detection Rules
- "Swap Square for SAP — same agents, same pattern"
- Source: `docs/field-registry.json`, `canary/services/parsers/`,
  `docs/webhook-usecase-map.json`, Atlas `fig-i02`

### Panel 3: Documentation as Code
- SDD → chunks → pgvector embeddings → similarity search
- 16 SDD cards, clickable
- Live Owl `knowledge_search` query demo
- Source: `Canary/docs/sdds/v2/`, memory bus

### Panel 4: The Knowledge Graph
- Brain wiki as D3 force-directed graph (221 nodes, 13 prefix clusters)
- Click a node → shows article
- Connections: SDD → wiki → code → memory
- Source: `Brain/REGISTRY.json`, wiki articles

### Panel 5: Agentic Workflow
- 12 MCP servers as service mesh (Atlas `fig-o01`)
- Live QA Agent demo: type query → watch tool calls → trace chain
- "3 domains (Canary, Cove, Angel), same MCP pattern"
- Source: MCP manifest endpoints, QA Agent at `/ops/qa`

### Panel 6: The Numbers
Auto-generated:
- Lines of Python, models, migrations, SDDs, wiki articles, Atlas diagrams,
  detection rules, MCP servers, factory stages, skills
- "Built by: 1 founder + AI. Timeline: months, not years."

---

# TRACK B: LEAVE-BEHIND

## B1. Brain Wiki — Canary Articles (Day 1-2)

Canary has 6 wiki articles. Angel has 37. Fix this. Create from existing
SDDs + code:

| New article | Source |
|---|---|
| `canary-tsp-pipeline.md` | `docs/sdds/v2/webhook-pipeline.md` |
| `canary-chirp-rules.md` | `docs/sdds/v2/chirp.md` |
| `canary-fox-case-management.md` | `docs/sdds/v2/fox.md` |
| `canary-owl-search.md` | `docs/sdds/v2/owl.md` |
| `canary-metrics-engine.md` | `docs/sdds/v2/analytics.md` |
| `canary-square-integration.md` | `docs/sdds/v2/identity.md` |
| `canary-goose-credit.md` | `docs/sdds/v2/goose.md` |
| `canary-factory-workflow.md` | `Brain/projects/Factory.md` |
| `canary-mcp-layer.md` | 12 MCP servers, manifests |
| `canary-deployment.md` | Docker, tunnel, health checks |

Follow `Brain/templates/wiki-article.md` format. Each article readable
by an enterprise engineer on day one. Update `Brain/projects/Canary.md`
MOC to link all of them.

## B2. Brain Federation — GRO-520 Phase 2-4 (Day 2-3)

Phase 1 assessment is done (`Brain/raw/inbox/_brain-assessment-v1.md`).
Continue per `docs/playbook-brain-scaffold-design.md`:

- **Phase 2:** Compile source inputs (raw + compiled + summarized brief)
- **Phase 3:** Design 8 workstreams (taxonomy, layout, manifests, query
  protocol, exposure, registry, governance, change management)
- **Phase 4:** Draft Brain Federation SDD v0.9

Key findings from Phase 1 that shape the design:
- Prefix-as-scope is already 80% of the federation — codify it
- `growdirect-*` (86 files) needs ops-public / ops-private / ops-sensitive split
- 217 cross-repo links are load-bearing — federation must preserve them
- `raw/inbox/` (1,280 binaries) is source material, never published
- Personal layer is empty today — formalize the slot but don't over-design

**This produces the SDD, not the migration.** No files move. The spec
locks before execution begins.

## B3. CLAUDE.md Rewrites (Day 2)

Rewrite as onboarding docs for a human engineer, not just AI agents:

**Root CLAUDE.md:**
- Add "New Engineer Start Here" section
- Explain Documentation as Code for humans
- Link to Brain/projects/Method.md
- Explain memory bus + how to query it

**Canary/CLAUDE.md:**
- Add "Architecture at a Glance" (reference Atlas fig-o01)
- Add "First 30 Minutes" quickstart
- Explain 3 schemas and what each contains
- Link to 16 SDDs as subsystem documentation
- Explain demo-reset workflow

## B4. Memory Bus Cleanup (Day 3)

```sql
-- Audit
SELECT memory_type, layer, count(*) FROM alx_memories GROUP BY 1, 2 ORDER BY 3 DESC;
SELECT status, count(*) FROM alx_sessions GROUP BY 1;

-- Clean
DELETE FROM alx_sessions WHERE status = 'abandoned';
```

Prepare 3-4 canned demo queries:
- "What decisions were made about detection rules?"
- "How does the TSP pipeline work?"
- "What's the data model for fox cases?"
- "What architectural patterns does Canary use?"

Verify embedding quality — spot-check similarity results.

## B5. Repo Cleanup (Day 1 — do first)

### Canary/

**Delete:**
- `data/` (empty)
- `.worktrees/qa-agent-tier-0/` (orphaned)
- `devops/deploy_reports/DEPLOY_*.txt` (7 stale Feb logs)
- `devops/prompts/ux/UX_BUILD_OUTPUT.txt`
- `devops/prompts/_debug_502_notification_service.txt`
- `docs/Canary-Blue-Ocean-Strategy-Analysis.md`
- `docs/superpowers/data/wpbca-parcels-seed.csv` (Cove data)
- `docs/superpowers/plans/2026-03-23-cove-mvp.md` (wrong repo)
- `docs/superpowers/specs/2026-03-23-cove-governance-platform-design.md` (wrong repo)
- `docs/strategic/Canary_Platform_Overview_v1.0_1.docx` (duplicate)
- `static/landing/` (belongs in GitHub Pages repo, not Flask app)

**Commit uncommitted changes:**
- `canary/blueprints/square_oauth_wired.py` — merchant-reset fix (review + commit)
- `templates/app/base_app.html` — template tweaks (review + commit)

**Update .gitignore:** add `.claude/settings.local.json`, `devops/pgadmin-servers.json`

**Fix hardcoded password:**
```python
# level_b_demo.py line 35 — change to:
PG_PASS = os.environ.get("SEED_PG_PASS", "canary_dev_2026")
```

### GrowDirect/ monorepo root

**Delete root junk:**
- `10584-max.jpeg`, `13328-max.jpeg`, `15658-max.jpeg`
- `2025_Tax_Prep_Workbook.xlsx`, `2025_Tax_Strategy_Brief.docx`
- `AngeliqueLyle-LP-Integration-Spec.docx` (or move to Angel/docs/)
- `formspree.rtf`
- `Torrance _ San Pedro - Sheet A08...html` (or move to Seacove/docs/)

**Clean restored git artifacts:**
- `docs/_archive/ip-vault/warchest/site/` (53 files — in git at fd3db16)
- `docs/_archive/workorders/`

**Batch commit Brain changes:**
```bash
git add Brain/ Angel/knowledge/ .obsidian/
git commit -m "brain: batch wiki updates — Cove research, Angel knowledge, project MOCs"
```

**Add to .gitignore:** `.claude/scheduled_tasks.lock`, `devops/pgadmin-servers.json`

## B6. Add Repo Governance Files (Day 3)

- `LICENSE` — decide: MIT, Apache 2.0, or proprietary
- `SECURITY.md` — responsible disclosure contact
- Rewrite `README.md` for enterprise audience (architecture, schema,
  quick start, live demo link, "built by" story)

---

# EXECUTION SCHEDULE

| Day | Track A (Ship It) | Track B (Leave-Behind) |
|---|---|---|
| **1** | A1: Demo reseed (Code session) | B5: Repo cleanup (both repos) |
| **1** | A2: API docs gateway (same session) | B1: Start Canary wiki articles |
| **2** | A3: Static site updates (GitHub Pages session) | B2: GRO-520 Phases 2-3 (Cowork session) |
| **2** | | B3: CLAUDE.md rewrites |
| **3** | A4: Mac Mini deploy + tunnel | B2: GRO-520 Phase 4 (SDD draft) |
| **3** | A5: Method page (panels 1-3) | B4: Memory bus cleanup |
| **4** | A5: Method page (panels 4-6) | B6: Repo governance files |
| **4** | A4f: End-to-end verify | Full walkthrough rehearsal |

---

# TRACK C: CODE HARDENING (separate dispatch, after A+B)

Not in scope for this sprint. Scoped here so it's declared, not forgotten.

- Grep for TODO, HACK, FIXME, stub, NotImplementedError across codebase
- Dead route audit (routes that return 501 or raise NotImplementedError)
- Empty service methods (wired but no-op)
- Error handling pass (bare except, missing validation)
- Console.error / print statement cleanup
- Git history cleanup (squash messy commit runs if going public)
- Type hint coverage on public interfaces
- Dependency audit (unused packages in requirements.txt)
- Test coverage report + gap analysis

---

# PARKED WORKSTREAMS (post-Primetime)

| Workstream | File | When |
|---|---|---|
| Katz method reverse-engineering | `docs/playbook-method-katz-reverse-engineer.md` | After Method page ships — enriches the consulting model |
| Retail ops model synthesis | `docs/playbook-retail-ops-model.md` | After raw/inbox binaries are extracted — feeds Canary roadmap |
| Solex Square merchant | `docs/playbook-solex-square-merchant.md` | After demo is stable — design partner for beta |
| Brain migration execution | GRO-520 follow-up | After Federation SDD v1.0 locks |
| GRO-520 Phases 5-7 | `docs/playbook-brain-scaffold-design.md` | After SDD v0.9 draft, includes review + lock cycle |

---

# CLEANUP: Old Dispatches

After this dispatch is in execution, delete:

```bash
rm dispatch-code-2026-04-22-demo-reseed.md  # absorbed into A1
rm docs/dispatches/dispatch-site-2026-04-22.md  # absorbed into A3
rm docs/dispatches/dispatch-demo-prep-2026-04-22.md  # superseded
rm docs/dispatches/dispatch-api-docs-gateway-2026-04-22.md  # absorbed into A2
rm docs/dispatches/dispatch-vscode-library-narrative-2026-04-22.md  # absorbed into A3b
rm docs/_archive/dispatch-cowork-2026-04-15.md  # stale
```

Keep:
- `docs/dispatch-brain-scaffold-design.md` — active, GRO-520
- `docs/playbook-brain-scaffold-design.md` — active, GRO-520 source of truth
- `docs/playbook-method-katz-reverse-engineer.md` — parked
- `docs/playbook-retail-ops-model.md` — parked
- `docs/playbook-solex-square-merchant.md` — parked

---

# KEY REFERENCES

| Resource | Path / Location |
|---|---|
| Demo reseed (full spec) | `dispatch-code-2026-04-22-demo-reseed.md` (root) |
| Brain assessment | `Brain/raw/inbox/_brain-assessment-v1.md` |
| Brain playbook | `docs/playbook-brain-scaffold-design.md` |
| Factory manifest | `factory-manifest.json` |
| Factory MOC | `Brain/projects/Factory.md` |
| Method MOC | `Brain/projects/Method.md` |
| Canary MOC | `Brain/projects/Canary.md` |
| SDDs (16) | `Canary/docs/sdds/v2/` |
| Atlas diagrams (60+) | `Canary/docs/atlas/` |
| Field registry | `Canary/docs/field-registry.json` |
| Webhook use-case map | `Canary/docs/webhook-usecase-map.json` |
| War Chest sources | git commit `fd3db16`, `docs/_archive/ip-vault/warchest/site/` |
| Previous site build | git commit `5464b9f`, `site/` |
| Square sandbox merchant | `MLE55GCYANCYT` |
| Mac Mini | 192.168.10.102 |
| iMac (QA tunnel) | 192.168.10.117 |
| Existing tunnel script | `Canary/devops/scripts/setup_qa_tunnel.sh` |
| Memory bus | `services/memory-bus/` |
| Content engine | `content-engine/engine.py` |
| GitHub Pages repo | `growdirectprez.github.io` (separate) |

