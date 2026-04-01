# VIVA — Agentic Treasury Operations Engine

> Read `~/GrowDirect/CLAUDE.md` first. This file adds VIVA-specific context on top.

---

## Identity

- **App:** VIVA
- **One-liner:** Agentic treasury engine that makes idle protocol capital productive
- **Status:** Research phase (DAO Council verdict: 2026-03-31 — gated approval)
- **Primary entity:** Strategy (everything resolves to a strategy: signals feed strategies, strategies generate trades, trades produce P&L, P&L flows to treasury)
- **Users:** Internal only — GrowDirect treasury. No external customers.
- **Domain:** Treasury operations, prediction market trading, multi-strategy arbitrage

---

## Hard Rules

1. **Legal gate first.** No live capital deployment without formal legal opinion on CFTC, SEC, FinCEN, DUNA scope. Council verdict requires this.
2. **Paper trade before live.** Every strategy must run 8+ weeks in paper mode with >70% win rate after fees before any real capital touches it.
3. **Kill switch at -15%.** Not -40%. Per-strategy, automatic, no governance vote required.
4. **Per-strategy position limits.** No single strategy can hold >30% of deployed capital.
5. **Correlation monitoring.** If two strategies show >0.7 loss correlation, one shuts down automatically.
6. **Post-mortem on every loss >1% of capital.** Filed to `docs/post-mortems/`.
7. **Council governs strategies, not trades.** Council approves/rejects strategy proposals and risk envelopes. Individual trades execute autonomously within approved envelopes.
8. **No factory pipeline until Phase 3.** Research phases use spike/prototype workflow. Factory stages apply only after council approves graduation.

---

## Architecture

VIVA is NOT a standard Flask monolith. Council review confirmed it needs multiple services:

```
Viva/
├── CLAUDE.md                      # This file
├── .claude/
│   └── settings.json
├── devops/
│   └── docker-compose.yml         # Multi-service: api + workers
├── viva/                          # Python source
│   ├── __init__.py                # App factory (Flask — dashboard/API only)
│   ├── config.py                  # Env-based config classes
│   ├── extensions.py              # db, valkey, csrf
│   ├── models/                    # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── strategy.py            # Strategy proposals, approvals, parameters
│   │   ├── trade.py               # Individual trade records
│   │   ├── position.py            # Open positions, P&L tracking
│   │   ├── signal.py              # Market signals (price ticks, events)
│   │   └── council_verdict.py     # Council decisions (append-only audit)
│   ├── signals/                   # Signal Layer — runs as worker service
│   │   ├── __init__.py
│   │   ├── cex_feed.py            # CEX WebSocket consumer (Binance, Coinbase)
│   │   ├── prediction_feed.py     # Polymarket/Kalshi CLOB API consumer
│   │   ├── oracle_feed.py         # Chainlink oracle monitor
│   │   └── news_feed.py           # News/event ingestion
│   ├── strategies/                # Strategy Engine
│   │   ├── __init__.py
│   │   ├── base.py                # Abstract strategy interface
│   │   ├── latency_arb.py         # Latency arbitrage module
│   │   ├── oracle_arb.py          # Oracle arbitrage module
│   │   ├── news_driven.py         # News-driven trading module
│   │   ├── market_maker.py        # Market making module
│   │   └── cross_venue_arb.py     # Cross-venue arbitrage (Polymarket + Kalshi)
│   ├── execution/                 # Execution Layer — runs as worker service
│   │   ├── __init__.py
│   │   ├── order_manager.py       # Order lifecycle management
│   │   ├── position_tracker.py    # Real-time position state
│   │   ├── risk_monitor.py        # Drawdown, exposure, correlation checks
│   │   └── kill_switch.py         # Automatic halt — no governance vote
│   ├── council/                   # Council Layer — invoked on-demand
│   │   ├── __init__.py
│   │   ├── strategy_review.py     # Propose/approve/reject strategies
│   │   ├── risk_envelope.py       # Set/modify risk parameters
│   │   └── performance_review.py  # Periodic P&L and strategy audit
│   ├── dashboard/                 # Flask blueprint — read-only UI
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── templates/
│   ├── public/                    # Public routes (health, status)
│   │   ├── __init__.py
│   │   └── routes.py
│   └── auth/                      # Auth (Jeffe-only access)
│       ├── __init__.py
│       └── routes.py
├── templates/                     # Jinja2 base templates
├── static/                        # CSS, JS
├── migrations/                    # Alembic
├── tests/
│   ├── unit/                      # Strategy logic, risk calculations
│   ├── integration/               # Signal → Strategy → Execution flow
│   └── smoke/                     # Health check, dashboard renders
├── docs/
│   └── security/
└── wsgi.py                        # WSGI entry point (dashboard only)
```

### Service Topology

```
docker-compose services:
  api          — Flask dashboard + REST API (Gunicorn)
  signal-worker — Async signal ingestor (asyncio event loop, NOT Flask)
  exec-worker  — Trade execution worker (asyncio, reads from Valkey queue)
  risk-monitor — Continuous risk assessment (reads positions, enforces limits)
```

The `api` service is Flask. The workers are standalone Python asyncio processes.
This matches the Canary pattern where TSP consumers are separate services, not Flask.

---

## Data Model

| Table | Schema | Purpose |
|-------|--------|---------|
| strategies | app | Strategy definitions, parameters, approval status |
| trades | app | Individual trade records (append-only) |
| positions | app | Current open positions, mark-to-market |
| signals | app | Market data snapshots (time-series, pruned) |
| council_verdicts | app | Council decisions on strategies (append-only audit) |
| risk_snapshots | app | Periodic risk state captures |

---

## Config

```
DATABASE_URL=postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/viva
VALKEY_URL=redis://growdirect_valkey:6379/2
OLLAMA_URL=http://growdirect_ollama:11434
```

Port: 5003 (Flask API/dashboard)
Valkey DB: 2

---

## Phase Gates

| Phase | Gate | Criteria | Blocks |
|-------|------|----------|--------|
| 0 | Legal | Formal opinion on CFTC/SEC/FinCEN/DUNA | All code |
| 1 | Research | Paper trade 8 weeks, >70% win rate after fees | Live capital |
| 2 | Validation | 0.001 BTC live, 8 weeks consistent returns | Scale-up |
| 3 | Factory | Canary at 17+ merchants, Phase 2 passed | Full build |

---

## Protected Files

- `.env` — secrets, API keys (NEVER commit)
- `wsgi.py` — entry point
- `viva/extensions.py` — database connection
- `viva/execution/kill_switch.py` — safety-critical, council cannot override
- `devops/docker-compose.yml` — infrastructure
- `migrations/env.py` — migration config
