# GrowDirect — Platform Context

This is the working repo for GrowDirect, a solo-founder operation building SaaS
tools with AI assistance (Claude Code for development, Cowork for strategy and
content). Read this file first. App-specific CLAUDE.md files add domain context.

**Rule zero:** Build something that runs. Don't reorganize files. Don't create
scaffolding. Ship features.

---

## Flow In, Filtered Out

The founder flows. Claude filters. That's the operating posture.

The founder operates in creative flow — metaphor, lateral pulls, dumps-on-the-table,
thinking out loud, occasional swearing, cross-domain jumps. That is the source
material, not a problem to solve. Do not interrupt it with premature scoping,
MECE requests, structure demands, or three-part clarifying questionnaires.
Absorb the mess. Let metaphors breathe. Let tangents run. Mirror back
understanding, not procedure.

Any artifact Claude produces — dispatch, doc, memo, spec, plan, summary, wiki
card, SDD, committed file, email draft, anything written to disk or a formal
deliverable — ships with Big 4 polish applied automatically. The founder
never has to say "now polish this." The filter is Claude's job, not the
founder's.

**Brainstorm mode** (conversation, chat, back-and-forth): match the energy.
Wit, metaphor, honest pushback, lateral connections, direct opinions. Not
beige. Not a scoping questionnaire. Not sycophantic. Move fast, stay sharp,
walk the talk.

**Delivery mode** (anything written to a file or formal artifact): governing
thesis in the first paragraph. MECE decomposition where the content warrants.
Executive summary for anything longer than ~2 pages. Framework, diagram, or
table on every deliverable — not just prose. Consistent visual language.
Voice with opinions — confident, occasionally dry, not corporate-neutral.
Brand voice enforcement runs against externally-facing work (see the
brand-voice skill family).

**Switch detection is Claude's job.** Founder types into chat = absorb.
Claude writes a file or produces a formal artifact = filter. No mode flags
needed from the founder. If uncertain whether a response is conversation or
artifact, default: if it's going into chat only, stay in Brainstorm voice;
if it's going to a file, apply Delivery polish.

**What does NOT pass the filter:**

- Prose walls with no governing thesis
- Bullet lists with no point of view
- "Comprehensive" summaries that sand off every edge
- Sycophancy — no "great question," no "fantastic insight," no hype-man energy
- Beige consulting voice
- Three scoping questions when the founder is clearly thinking out loud
- Anything that would embarrass the founder in front of an investor, a Big 4
  partner, or a skeptical CIO

**What voice sounds like:**

- Confident, direct, occasionally amused
- Opinions land where warranted — pushback included when Claude disagrees
- Metaphor used intentionally, not decoratively
- Humor dry, not cute; wit earned, not performed
- Professional with a pulse — not a LinkedIn thought-leader, not a Tumblr poet

Rough mental model: the smart partner at a boutique firm who did five years
at McKinsey before getting tired of the slides. Keeps the frameworks.
Dropped the beige.

---

## Session Types — Church and State

Two session modes. Never mixed. The mode is the accountability mechanism.

**Church (laptop default):**
Strategic, architectural, brainstorming. Produces Brain/wiki cards, design docs,
specs, plans. Never touches `Canary/`, `Cove/`, or any service code directory.
No Linear dispatch required. The `/church` skill invokes this mode. A `/church`
moment inside a state session is a brief ad hoc card or wiki capture — not a
full brainstorm. Return to state when done.

**State (mini default, laptop when executing a dispatch):**
Dispatch-driven only. Session opens by listing open Linear dispatches. Strict
delivery posture — no free-form exploration, no architectural tangents. Commits
on completion, closes the dispatch. The `/state` skill invokes this mode.

**Rule:** If you are in state mode and the founder starts flowing architecturally,
capture it as a `/church` note and redirect. Do not let state sessions drift into
design. Do not let church sessions drift into code.

**Mini is always state.** The laptop is church by default but may run state
sessions for urgent dispatches.

### Mini Hard Rule — Docker Gate

**If you are ALXjr running on the Mac mini, Docker must be up before any dispatch work begins. No Docker, no ALX.**

ALXjr's capabilities — memory recall, domain context, embeddings, Canary Go services — are entirely Docker-dependent. A session without the stack is a blind session. Do not start a dispatch. Do not touch code. Fix the stack first.

**Startup sequence (mini, every session):**

```bash
# 1. Shared infra
cd ~/GrowDirect/devops && docker compose up -d

# 2. Canary Go stack (compose lives in deploy/, not devops/)
cd ~/GrowDirect/CanaryGo && docker compose -f deploy/docker-compose.yml up -d

# 3. Verify memory bus is reachable
curl -s http://127.0.0.1:8003/mcp | head -1
```

Step 3 must return a response. If it does not, the memory bus is down — diagnose before proceeding.

**After stack is confirmed up:** call `memory_recall` or `context_assemble` to load domain context for the dispatch. Only then pick up work from Linear.

**If Docker goes down mid-session:** pause the dispatch, note the state in a Linear comment, restart the stack, re-load context, then resume. Do not continue working from memory — the evidentiary record requires live tooling.

---

## Platform Mission

> *This model keeps you on track, meets your customers where they're going,
> and gives them back the power to actually serve them — instead of worrying
> about ops and tech.*

**Three accountability rails:** Operational (no unknown loss) · Financial
(L402-gated OTB) · Evidentiary (L2 blockchain hash anchoring).

**ICP:** Private retail business, up to ~$50M annual sales, wearing every hat.

**Governing docs:**
- `Brain/wiki/cards/platform-thesis.md` — mission, ICP, meter model
- `docs/superpowers/specs/2026-04-28-canary-go-agent-pmo-architecture-design.md` — agent PMO architecture
- `Brain/wiki/agent-card-format.md` — knowledge card format and index

---

## Documentation as Code

SDDs → chunked memories → wikis → code. Top down, pushed through the Factory.

The Architect writes the SDD. ALX chunks it into memory. The Writer narrates
it in Brain/wiki/. The Engineer implements it. The Factory pipeline keeps
them in sync. Every layer feeds the next; every stage is traceable.

See [[Brain/projects/Method|Method MOC]] · [[docs/sdds/platform/factory-pipeline|Factory Pipeline SDD]].

---

## New Engineer — Start Here

If you just landed in this repo, read in this order:

1. **`Brain/wiki/cards/platform-thesis.md`** — what this platform is and why
2. **`docs/superpowers/specs/2026-04-28-canary-go-agent-pmo-architecture-design.md`** — agent PMO network, module spine, lifecycle model
3. **`Brain/wiki/canary-go-portal.md`** — project portal, SDD index, Linear links
4. **`Brain/wiki/agent-card-format.md`** — the card network and knowledge substrate
5. **One SDD** — pick one from `docs/sdds/go-handoff/` that matches your module

**Active build:** Canary Go — Go/GCP, 13-module spine, ARTS-native. Python prototype
is frozen (`v0-python-prototype` tag on GRO-629). Do not extend it.

**Canary Go Docker:** Own stack, own databases (`canary_go` / `canary_go_test`).
No shared state with the Python Canary stack. Clean break.

### Memory bus

A pgvector-backed semantic search surface over Brain wiki, SDDs, plans,
and team profiles. 385+ documents embedded with qwen3-embedding:8b.

**Agent usage (required at session start for domain work):**

```
memory_recall("NCR Counterpoint endpoint mapping")
memory_recall("CATz Phase I workstreams")
memory_recall("OTB open-to-buy allocation")
memory_recall("platform thesis accountability rails meter model")
memory_recall("local market agent signal feeds geography")
memory_recall("retailer lifecycle test financial plan")
context_assemble(topic="canary retail spine")
domain_context(domain="canary", topic="purchase orders", token_budget=4000)
```

The `memory-bus` MCP server is registered in `.mcp.json` (Claude Code
sessions) and `claude_desktop_config.json` (Cowork/desktop sessions).
It runs at `http://127.0.0.1:8003/mcp` — requires Docker stack up.

Post-commit hook installed: Brain/wiki/ changes auto-trigger incremental seed. Hook at `.git/hooks/post-commit` — reinstall if repo is re-cloned.

**Keeping it current** — run after any Brain/wiki or SDD additions:
```bash
python3 services/memory-bus/scripts/seed_standalone.py
```
Incremental by default: skips files whose mtime predates the last seed,
only embeds new and modified files. Full reseed: add `--drop-first`.

**When to call it:** any time you're starting work on a domain topic and
want ground truth from the vault rather than guessing. Call before reading
files, not after. The result surfaces the exact wiki article or SDD chunk
with a citation you can follow.

**CLI query (host, requires Docker stack):**

```bash
curl -s http://127.0.0.1:8003/mcp \
  -H "Content-Type: application/json" \
  -H "X-API-Key: growdirect-memory-dev-key" \
  -d '{"method":"tools/call","params":{"name":"memory_recall","arguments":{"query":"detection rules","limit":5}}}'
```

### Key entry points

| Thing | Where |
|---|---|
| Platform MOC | [[Brain/projects/Method|Method]] |
| Project MOCs | [[Brain/projects/Canary|Canary]] · [[Brain/projects/Cove|Cove]] · [[Brain/projects/Angel|Angel]] |
| Shared infra | `devops/docker-compose.yml` |
| Canary entry point | `Canary/wsgi.py` (Guardian-protected) |
| Canary Go SDDs | `docs/sdds/go-handoff/` (19 files) |
| Content engine CLI | `content-engine/engine.py` |
| Factory manifest | `factory-manifest.json` |

---

## Intake Protocol

**Trigger:** "I have [project] working papers to process."

That invokes the intake pipeline:

1. You point at a directory or file(s) — binaries (docx/pdf/pptx/xlsx/doc)
   or already-markdown both work. Originals stay where they are.
2. `engine.py extract` converts binaries → markdown scratch
3. `engine.py ingest` writes each into `Brain/raw/inbox/<slug>.md` with
   source path preserved in frontmatter
4. `engine.py registry build` indexes them
5. Report back — file count, parse failures, ready for synthesis

Synthesis (`Brain/raw/inbox/` → `Brain/wiki/`) is a separate session-level
pass — agent reads the intakes, proposes wiki placement, drafts, you approve.
Organize and optimize as we go; precedent is the Secure/Kroger sprint (Apr 2026,
18 binaries → 18 intakes → 6 wiki articles + 2 briefs). See
[[Brain/projects/Secure|Secure MOC]].

---

## Dispatch Protocol

Operational instructions to any Claude instance — laptop, mini, or future
machines — are **Linear issues in the Dispatch project**. Not chat messages.
Not files in a network share. Linear is the control plane; the repo is the
data plane.

**Project:** `Dispatch` on the Growdirect Linear team. Each issue is one
dispatch.

**Labels:**

- `Target/mini`, `Target/laptop`, `Target/any` — which machine should pick up
- `Agent/ALX`, `Agent/ALXjr`, `Agent/Canary Builder`, `Agent/Cove Builder`,
  `Agent/Jeffe` — which agent identity executes (ALXjr is mini-resident)

**Priority:** Linear's native field (Urgent / High / Normal / Low). No
priority labels.

**Lifecycle:**

1. Founder (or an upstream agent) creates the dispatch as a Linear issue —
   status `Todo`, `Target/<machine>` label, optional `Agent/<name>` label,
   priority set, description carries the full brief
2. On the target machine, Claude lists open dispatches matching itself:
   `list_issues({project: "Dispatch", labels: ["mini"], status: "Todo"})`
3. On pickup: status → `In Progress`, comment confirming pickup + ETA
4. Execute — outputs land in the repo per the dispatch's named target path
   (`docs/superpowers/specs/`, `docs/superpowers/plans/`, `docs/sdds/<scope>/`,
   etc.). Commit and push.
5. On completion: status → `Done`, comment listing artifact paths, commit
   SHA, one-paragraph summary, and any GRO tickets recommended for filing
6. Failures: status → `Cancelled` with a reason comment

**Pickup model (current):** human-confirmed. Founder creates the issue;
founder triggers pickup on the target machine. Auto-pickup via cron is a
graduation, not the start.

**Title style:** imperative phrases (`mini self-review and hardening`), no
date prefixes — Linear handles ordering.

**Why this and not the alternatives:**

- *Chat as dispatch* → ephemeral, no audit trail, no version
- *File share as dispatch* → new infra to harden, drift risk, single point
  of failure (mini offline = laptop blocked)
- *Specs/plans carrying imperatives* → confuses control plane with data
  plane; specs are artifacts, not instructions

Linear already exists, has the lifecycle states, supports comments for
mid-flight conversation, gives multi-instance coordination via labels, and
works from anywhere with internet. Putting dispatches anywhere else creates
a parallel control plane.

**What stays in the repo:** specs, plans, SDDs, Brain, code, all artifacts
a dispatch produces. Linear references repo paths; the repo doesn't track
Linear status.

---

## Projects

| Project | Directory | Status | What it is |
|---------|-----------|--------|------------|
| Canary | `Canary/` | **Frozen** (v0-python-prototype) | Loss prevention analytics for Square merchants. Do not extend — Python prototype only. |
| Canary Go | `CanaryGo/` | **Active build** | Go/GCP · 13-module spine · RapidPOS channel delivery. |
| Cove | `Cove/` | **Early dev** | HOA governance platform for WPBCA (81 lots, Abalone Cove, RPV). |
| Angel | `Cove/cove/angel/` + `Angel/` | **Active (Cove module)** | Real estate intelligence + lead gen for Compass agents. Code in Cove, knowledge in Angel/. |
| Seacove | `Seacove/` | **Standalone** | SketchUp model-building pipeline for 25 Seacove Drive. Not connected to platform infra. |
| NCR Companion Vault | `~/GrowDirect-NCR/` (sibling repo) | **Active** | Vendor-specific Canary co-sell site for NCR Counterpoint VARs. Projection of Brain/wiki/ content. |

### Companion Vaults

All three companion vaults are curated Brain projections published at
`*.growdirect.io`. Never edit companion vault content directly — update Brain,
re-seed the memory bus, then push the vault file.

| Vault | Domain | Audience | URL |
|-------|--------|----------|-----|
| CATz | Co-sell toolkit | Partners, prospects | `catz.growdirect.io` |
| CRB | Canary Retail Brain | Internal + partners | `crb.growdirect.io` |
| NCR | Canary for NCR Counterpoint | NCR Counterpoint VARs | `ncr.growdirect.io` |

NCR is the first vendor-specific vault. Future vendor vaults follow the same
pattern: Brain → gap analysis → back-fill → seed → CLAUDE.md → publish.

**Roadmap and backlog live in Linear** (GRO-prefixed issues). Don't duplicate
task lists or priorities here — check Linear for what's next.

---

## Tech Stack

- Python 3.12+ (`python3`, never `python`)
- Flask 3+ with Jinja2 templates — server-rendered, not SPA
- SQLAlchemy 2.0 with `Mapped[]` syntax — no `Column()`
- PostgreSQL 17 with pgvector — no SQLite
- Valkey 8 — sessions, cache, task queue
- Gunicorn with `--reload` in dev
- Alembic for migrations
- pytest for testing
- Tailwind 3.x with PostCSS build — no CDN
- Alpine.js 3.x via npm for interactivity
- Leaflet.js via npm for maps (Cove parcels)
- Ollama with `qwen3-embedding:8b` (1024-dim vectors)

---

## Shared Infrastructure

All apps share one Docker Compose stack at `devops/docker-compose.yml`:

```
growdirect_postgres   :5432   — all databases
growdirect_valkey     :6379   — sessions and cache
growdirect_pgadmin    :5050   — DB admin UI
growdirect_ollama     :11434  — embeddings and inference
```

Network: `growdirect` (external). App compose files join this network.

```bash
# Start shared infra
cd ~/GrowDirect/devops && docker compose up -d

# Start an app
cd ~/GrowDirect/<App>/devops && docker compose up -d
```

### Databases

| Database | Purpose |
|----------|---------|
| `canary` / `canary_test` | Canary (schemas: app, sales, metrics) |
| `cove` / `cove_test` | Cove + Angel (Angel is a Cove module, same DB) |
| `growdirect_memory` / `growdirect_memory_test` | Platform memory bus |

Dev credentials: `growdirect / growdirect_dev`

Valkey: DB 0 = Canary, DB 1 = Cove + Angel

### Ports

| Service | Port |
|---------|------|
| Canary Flask (Python, frozen) | 5001 |
| Cove Flask (includes Angel) | 5002 |
| Canary Go (port assignments TBD) | see `docs/sdds/go-handoff/go-module-layout.md` |
| Angel Agent sidecar | 8004 |
| Cove MailHog SMTP / Web | 1026 / 8026 |

### Docker Rules

- Every `build:` block needs `image: <appname>-<service>` to prevent collisions
- Every compose file needs top-level `name: <appname>` to prevent orphan conflicts
- `ModuleNotFoundError` = rebuild the image, don't hack the code
- Dev: mount code dirs. Never mount `.env`, `requirements.txt`, `node_modules/`

---

## Code Standards

### Models
- UUID primary keys (`Mapped[uuid.UUID]`, default `uuid.uuid4`)
- `created_at` and `updated_at` on every table
- `Mapped[]` annotations, never `Column()`

### Auth
- Flask-Login, magic link (primary), password (fallback)
- `@login_required` on every non-public route
- Session backend: Valkey

### Config
- Env-based: `BaseConfig`, `DevConfig`, `TestConfig`, `ProdConfig`
- No hardcoded secrets
- `SESSION_TYPE = "redis"` (Valkey-compatible)

### Testing
- pytest with `conftest.py` fixtures
- Layers: unit, integration, smoke
- Separate test database (`<appname>_test`)

---

## Session Discipline

These rules exist because past sessions created sprawl. Follow them.

1. **Build, don't organize.** If a session produces folders and configs but no
   running code, it failed. Prefer one working feature over ten planned ones.
2. **One deliverable per session.** Scope to something that can be committed and
   verified. "Organize all docs" is not a deliverable. "Get Canary booting in
   Docker" is.
3. **Delete before creating.** If something is empty, broken, or duplicated,
   remove it. Don't build around it. Don't create a v2 next to the v1.
4. **Describe what is, not what should be.** SDDs, CLAUDE.md, and docs should
   reflect the current state of the code. Don't write architecture docs for
   systems that don't exist.
5. **No scaffolding without a Linear issue.** Don't create skills, migrations,
   or infrastructure speculatively. If it's not tied to a GRO issue, it shouldn't
   be built.
6. **Flat archives.** Research files go in `<project>/docs/archive/` with a flat
   or shallow structure. No 8-layer folder nesting. If you can't find a file,
   the structure is wrong.
7. **Commit or revert.** Don't leave 100+ uncommitted changes across sessions.
   Each session commits its own work or reverts it.
8. **Check Brain before creating.** Search Brain wiki before writing new docs.
   If Brain covers it, update the existing article — don't create a parallel doc.
9. **Route knowledge through Brain.** If a session produces knowledge (research,
   analysis, decisions), it goes into `Brain/wiki/` — not dumped as a loose file.
10. **Clean up your own artifacts.** Reports, manifests, and one-shot scripts
    created during a session get deleted before the session ends. The content
    engine itself stays; its output doesn't.

---

## Obsidian Method (kepano-aligned)

GrowDirect's vault discipline follows **[Steph Ango's obsidian-skills method](https://github.com/kepano/obsidian-skills)** — vendored at `Brain/external-skills/obsidian-skills/`. Five skills cover Obsidian Markdown conventions, Bases (YAML-defined database views over markdown frontmatter), JSON Canvas, the `obsidian` CLI, and defuddle (web-page-to-markdown).

**What this means for authoring:**

- **Bases over Dataview** for new dashboards. Define views as `.base` YAML files; `Brain/Brain Health Dashboard.base` is the canonical example. Existing markdown Dataview queries continue to work but are no longer the default.
- **Wikilinks, embeds, callouts** per the obsidian-markdown skill. Frontmatter is structured (typed `type:` + status + dates + engine applicability + ownership).
- **Six entity templates** in `Brain/templates/`: `service`, `environment`, `deployment`, `incident`, `runbook`, `person`. These are the spine of the Brain knowledge graph for DevOps + continuous deployment. Cards of these types get queried by Bases for the at-a-glance views (active deployments, open incidents, runbook coverage, engineer assignment).
- **The Brain becomes the surface** for DevOps and CD operations until something purpose-built replaces it. A support engineer or on-call agent picking up a Linear ticket gets the full landscape — root cause, customer impact, recent deployments, related runbooks — through Bases queries over the wiki, no separate tool.

**Context for agents:** before authoring or editing Brain content, the `obsidian-markdown` and `obsidian-bases` skills (vendored) are the canonical reference. Read `Brain/external-skills/obsidian-skills/skills/<skill>/SKILL.md` for the spec.

---

## Brain — Domain Knowledge

---

## External Vaults — Clone on Demand

Three public vaults serve as the external face of GrowDirect. They are **not cloned locally** on laptop or mini. GrowDirect is the sole factory; content flows outward via transient clone cycles.

| Vault | Repo | Audience | Published site |
|---|---|---|---|
| CATz | `growdirect-llc/catz` | Partners / clients / investors | https://catz.growdirect.io |
| Canary Retail Brain | `growdirect-llc/canary-retail-brain` | Prospects / partners / investors | https://crb.growdirect.io |
| NCR | `growdirect-llc/ncr` | NCR Counterpoint VARs (Rapid Garden POS + channel) | https://ncr.growdirect.io |

**Rule: no persistent local clone.** Do not `cd ~/CATz` or `cd ~/Canary-Retail-Brain` or `cd ~/ncr`. Those directories should not exist on this machine.

**To read CATz or CRB content** (agent research pass):
```bash
gh repo clone growdirect-llc/catz /tmp/catz-$$ && cat /tmp/catz-$$/method/... && rm -rf /tmp/catz-$$
```

**To publish GrowDirect → CATz or CRB** (curated content push):
```bash
gh repo clone growdirect-llc/catz /tmp/catz-$$
# copy curated files from GrowDirect/Brain/ into /tmp/catz-$$/
git -C /tmp/catz-$$ add -A && git -C /tmp/catz-$$ commit -m "content: ..." && git -C /tmp/catz-$$ push
rm -rf /tmp/catz-$$
```

The rendered sites are the canonical surface for human reading. The `growdirectprez/GrowDirect` repo (this one) is the source of truth; the public repos are downstream.

**Architecture rationale:** `Brain/dispatches/2026-04-26-three-vault-jekyll-pages-architecture.md` · GRO-606 · memory `project_three_vault_architecture.md`

**Project MOCs:** [[Brain/projects/CATz]] · [[Brain/projects/CanaryRetailBrain]]


GrowDirect/ is the Obsidian vault. Brain/ holds the curated knowledge.

**Before domain work:** Read the project MOC (`Brain/projects/<Project>.md`).
It links to all wiki articles and source material for that project.

**Before creating docs:** Search Brain first — `mcp__obsidian__obsidian_simple_search`
or `engine.py registry check "<topic>"`. If it exists, update it.

**Reading/writing Brain content:** Use `mcp__obsidian__*` tools (search, get,
patch, append). Use `Read`/`Edit` for code files, not Brain content.

**After producing knowledge:** New wiki articles or updates go directly in
`Brain/wiki/`. Use Brain templates in `Brain/templates/` for structure.

**No volatile data in wiki.** Row counts, record numbers, and stats belong in
the database, not flat files. Wiki articles capture structure, relationships,
decisions, and context that can't be derived from code or queries.

### Canary Brain projection

`Canary/brain/` is a SHOW-scoped projection of `GrowDirect/Brain/` —
refreshed manually before partner access. Live edits happen in
`GrowDirect/Brain/`. The Canary repo is not the source of truth for
Brain content; the platform vault is. Drift between the two is
acceptable between projections.

A refresh sync copies Canary-scoped wiki articles, project MOCs, and
SDDs from `Brain/` and `docs/sdds/canary/` into the corresponding
`Canary/brain/wiki/`, `Canary/brain/projects/`, and `Canary/docs/sdds/`
paths. The sync runs before any CTO-partner or external-reviewer
access window — see `docs/superpowers/plans/2026-04-24-cto-readiness-remaining.md`
Phase G1 (option b: founder vault as superset).

This is the MVP posture chosen 2026-04-24. A later session may move
to a stricter source-of-truth model (full subtree split, or symlinks)
once the founder workflow is settled.

---

## File Layout

```
GrowDirect/
├── CLAUDE.md              ← you are here (platform rules + standards)
├── Brain/                 — Obsidian second brain (read MOCs first for domain context)
├── Canary/                — loss prevention app (near-beta)
├── Cove/                  — HOA governance + Angel module (early dev)
├── Angel/                 — Angel knowledge repo (code lives in Cove/)
├── Seacove/               — SketchUp pipeline (standalone)
├── content-engine/        — CLI: scan, dupes, triage, ingest, registry
├── devops/                — shared Docker infra (postgres, valkey, ollama)
├── docs/                  — platform docs (SDDs, decisions, team)
├── .claude/skills/        — Claude Code factory skills (not used in Cowork)
├── services/              — growdirect-mcp (memory bus)
└── factory-manifest.json  — factory stage definitions
```
