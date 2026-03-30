---
type: research
domain: canary
status: active
created: 2026-03-19
updated: 2026-03-19
---
# Canary LP — Operations, Deployment & Team

> **Domain:** Infrastructure, deployment, testing, team roles, development workflow
> **Last Updated:** 2026-03-19 | **Classification:** Confidential

---

## Team Structure

**Jeffe (CEO)** — Founder. Real person, not an agent. All product decisions route through Jeffe. North Star keeper. Issues are GRO-prefixed in Linear.

**ALX (COO / Agent)** — Chief of Staff and primary development agent. Built and maintains the codebase. Operates via Claude Code with pgvector contextual memory (954+ curated memories). Session protocol: run `/alx-startup` before any work, load context via `session_start` MCP tool.

**Owl** — Retail Intelligence Engine (AI). Archetype: The Sentinel. Powered by qwen3:14b via Ollama. Systems thinker, research rigor, plain English delivery. Falls back to deterministic scoring if Ollama is unreachable.

**Tom** — Systems Architect. Validates DDL, schema migrations, infrastructure decisions. All database changes require Tom's review.

**Syd** — Legal counsel. Reviews protocol specs, investor materials, compliance.

**Jim** — QA and testing. Virtual Gym Agent spec for automated testing scenarios.

**Will** — Community and marketing. Manages Square Seller Community engagement, lead qualification.

**Jeremy** — Pipeline engineering. Core pipeline build work orders (Square OAuth through inscription).

Rule: Virtual team member names never appear in external-facing output.

---

## Development Workflow — The Factory Process

All development follows the Canary skill set enforcing the Factory Process:

| Stage | Skill | Enforcement |
|-------|-------|-------------|
| Vision/scope | `jeffe-review` | North Star alignment, one-line test, founder's lens |
| Planning | `canary-blueprint` | GRO issue required, scope check, Factory stages, data integrity flags |
| Implementation | `canary-tdd` | Test-first. RED before GREEN. Data accuracy. |
| Debugging | `canary-debug` | Root cause before fix. 3-fix limit. Canary surfaces. |
| Execution | `canary-assembly` | Guardian checks, smoke tests between tasks, stop-and-retriage |
| Verification | `canary-verify` | Evidence before assertions. North Star check. |
| QA | `canary-qa` | Diff-aware route/service testing. Lazy pipe detector. Health score. |
| Review | `canary-review` | Factory compliance. Data integrity. Infrastructure check. |
| Ship | `canary-ship` | QA gate → pre-landing review → bisectable commits → PR |
| Deploy | `canary-deploy` | 7-step gated pipeline |

### Protected Files (Guardian Required)
These files can only be modified through the `critical-file-guardian` skill, which enforces approval, validation, and SHA256 manifest tracking (`.guardian-manifest`):
- `.env` — credentials and config
- `wsgi.py` — single WSGI entry point
- `canary/db/session_factory.py` — DB session setup
- `Dockerfile` / `docker-compose.*.yml` — container and stack config

### No Lazy Pipes Standard
Every service, route, and pipeline must pass the Completeness Gate before being marked done:
1. Data goes IN — verify the write (integration test)
2. Data comes OUT — verify the read (integration test)
3. Row counts match — verify nothing lost or duplicated (SQL count)
4. Route responds — verify the API contract (curl + JSON validation)

---

## Deployment Infrastructure

### Lab Network
- **Internet:** Frontier Fiber (47.154.122.225) → DSR-250 router (192.168.10.1)
- **Dev Machine:** MacBook (192.168.10.102) — primary development, Ollama inference
- **QA Machine:** iMac (192.168.10.117) — QA environment
- **WiFi Bridge:** Google Nest WiFi to household segment (192.168.86.x, isolated)

### Environments

| Env | Machine | IP | URL | Compose File |
|-----|---------|-----|-----|-------------|
| Dev | MacBook | 192.168.10.102 | https://dev.growdirect.app | docker-compose.localhost.yml |
| QA | iMac | 192.168.10.117 | https://qa.growdirect.app | docker-compose.qa.yml |

### Docker Containers
8 active containers: Flask (canary-app), PostgreSQL (canary-db), Valkey (canary-valkey), nginx, 4 TSP subscribers. Total Docker images: 24.5GB (18.6GB reclaimable). Build cache: 27.6GB (20.6GB reclaimable).

### Cloudflare Tunnels
Shared `canary-qa` tunnel with hostname-based routing. Both machines always-on, outbound-only connections. Zero-trust access without port forwarding.

### Deploy Scripts
- `canary_deploy.sh` — Universal local orchestration (flags: --full, --app, --migrate, --test, --fast, --profile qa)
- `remote_deploy.sh` — Push to QA via SSH (runs canary_deploy.sh on iMac)
- `boot_localhost.sh` — Quick start for local dev
- Makefile targets: `make up`, `make health`, `make test`, `make migrate`, `make rebuild`

### Infrastructure Roadmap
- Phase 1 (Now): Tighten local lab (QA tunnel, disk cleanup, automated backups)
- Phase 2 (When needed): Mac Studio M2 Ultra (192.168.10.103) for dedicated Ollama (~$115/mo amortized)
- Phase 3 (Scale): Lightweight AWS (S3 backups, CloudFront landing, keep app local)
- Phase 4 (SLA): Full cloud migration (ECS, RDS, ElastiCache) when audits require it

Principle: "Local first, cloud behind a gate. No unmetered API connections."

---

## Testing Architecture

### Three-Layer Test Gates

| Layer | Location | Runner | Gate |
|-------|----------|--------|------|
| Unit | tests/unit/ | `python3 -m pytest tests/unit/` | CI blocks merge |
| Integration | tests/integration/ | `python3 -m pytest tests/integration/ -m postgres` | Before QA push |
| Smoke | tests/smoke/ | `python3 -m pytest tests/smoke/` | After every rebuild |

### Test Data
Square sandbox merchant: MLE55GCYANCYT (Default Test Account). Multi-location farmers market vendor: Penn High School, Redondo Beach, Torrance Certified, Default DC. 6 team members including "Suspicious Steve" (fraud test persona). Integration test scenario: Saturday at Torrance with 7 transactions triggering 4 Chirp alerts (rapid refunds, cash variance, after-hours).

### Row Count Discipline
Every data pipeline test must verify:
- Before: count rows in target table
- Execute: run the pipeline/operation
- After: count rows in target table
- Delta: does the change match exactly what was expected?
- Content: query the actual rows — do the values match the input?

---

## GitNexus Integration

Repository indexed by GitNexus: 1,323 files, 6,791 nodes, 17,036 edges, 375 communities, 300 processes. Last indexed: 2026-03-18. Commit: 46e0560b. The `.gitnexus/lbug` file (96MB) contains the full semantic graph for codebase navigation and relationship mapping.

---

## Task Management

All tasks tracked in Linear with GRO- prefix. No issue = no work. Active work orders cover pipeline build (GRO-47), multi-tenant architecture (GRO-18), operations console (GRO-73), and war chest content (B-058). 60+ work orders in the IP/workorders directory document completed and planned work.

---

*Canary LP | GrowDirect Inc. | Confidential*
