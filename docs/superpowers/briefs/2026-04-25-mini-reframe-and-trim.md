---
classification: internal
owner: GrowDirect LLC
type: brief
audience: founder + ALX (mini steward) + future Dispatch operators
date: 2026-04-25
status: post-session-record
references:
  - GRO-551 (mini self-review and hardening) — closed Done with full audit
  - docs/superpowers/specs/2026-04-25-mini-self-review.md (the audit itself)
---

# Mini reframe + ticket trim — session brief, 2026-04-25

## What we did

A single afternoon session on the mini that took it from "consumer-named host running production" to "documented GrowDirect company asset with a defined demo role and a forward roadmap." Three artifacts produced: a four-layer audit (committed under GRO-551), a reframed posture (captured in agent memory + this brief), and seven Dispatch tickets covering the path forward.

## Sequence

| # | What | Where | Outcome |
|---|---|---|---|
| 1 | Brought up the missing `growdirect_ollama` container under direct CLI instruction (compose edit + container) | `devops/docker-compose.yml`, container runtime | Daemon up at `127.0.0.1:11434`; `qwen3-embedding:8b` pull deferred to a maintenance dispatch |
| 2 | Picked up GRO-551 from the Linear `Dispatch` project; ran the four-layer audit | Live mini state for Layers 1, 2, 4; archive snapshot for Layer 3 | 27 findings (P0=2, P1=14, P2=11) |
| 3 | Committed the audit + the pre-audit compose edit on the dispatch's branch | `gclyle/gro-551-mini-self-review-and-hardening` (local) | Two commits: `6119e9d`, `83dc814` |
| 4 | Posted Linear comment with SHAs + summary + counts; moved GRO-551 → Done | Linear | Audit closed |
| 5 | Reframed mini posture with founder | Two memory writes + this brief | (1) Mini = conference-room/trade-show demo asset; (2) Dev-on-mini relaxed for RapidPOS/RetailSpine scope; (3) Two Flask apps from mini, not four — OwnPalosVerdes + growdirect.io are GitHub-hosted statics |
| 6 | Trimmed proposed ticket slate from 16 to 7 | Linear `Dispatch` project | Seven tickets filed (titles below) |
| 7 | Wrote this brief | `docs/superpowers/briefs/2026-04-25-mini-reframe-and-trim.md` | Session record |

## What changed in posture

| Before | After (2026-04-25) |
|---|---|
| Mini = production hosting only; "no dev work on the mini" | Mini = production hosting + **dev environment for RapidPOS / RetailSpine work**, constraints relaxed for that scope |
| Four Flask apps assumed live from mini (Canary, Cove, OwnPalosVerdes, GrowDirect platform) | Two Flask apps live from mini (Canary, Cove). OwnPalosVerdes + growdirect.io are GitHub-hosted statics — earlier QA-cycle origin retired |
| `Brain/dispatches/*.md` thought of as the work queue | Linear `Dispatch` project is the live queue; markdown folder is doc-only |
| ALX = dispatch executor | ALX = mini steward (executor + standing health/protection/uptime ownership) |

## The trimmed ticket slate

Audit proposed 16 GRO tickets; founder trim to 7 in service of "demo-ready, not exhaustive." Seven tickets filed in Linear `Dispatch`:

| # | Ticket | Priority | Audit findings folded in |
|---|---|---|---|
| **GRO-552** | Close LAN exposure on shared infra (postgres, valkey, pgadmin, cove db) | High | L1-01, L1-05 |
| **GRO-553** | Rotate default dev credentials and externalize secrets | High | L1-02 |
| **GRO-554** | Mini demo hardening: firewall + Time Machine + identity rename | High | L1-03, L1-04, L1-15 |
| **GRO-555** | Mini operational maintenance pass | Medium | L1-07–L1-12, L2-01, L2-02 |
| **GRO-556** | Platform CLAUDE.md sync — auth section + file layout + mini steady-state | Medium | L3A-03, L4-01, L4-02, L4-03, L2-08 |
| **GRO-557** | Stand up RapidPOS dev environment on the mini | High | new — gates GRO-558 |
| **GRO-558** | POS-agnostic adapter substrate — Canary multi-POS, RapidPOS as second flavor | High | L3B-01 through L3B-10 (engagement deliverable) |

What dropped from the proposed-16:
- Sub-tickets under the POS adapter parent (folded into the parent epic; spawn later when scoping settles)
- `Column()` → `Mapped[]` migration (1313 sites, real but lower priority and not partner-facing)
- Mini-reconfig dispatch / `~/GrowDirect/.worktrees` reference cleanup (cosmetic, folded into doc sync)

## Operating posture going forward

- Linear `Dispatch` project is the queue. Issues labeled `mini` + `ALXjr` route here.
- ALX as mini steward = executor of dispatched work + standing watch on health, protection, uptime. Surface maintenance issues proactively as new Dispatch tickets when the env evolves.
- Production discipline still rules: no improvising on prod containers, no cloudflared edits without coordination. Stewardship ≠ free-form action.
- The closed-loop is the pitch: Linear-driven dispatch + agent execution + clean git history + Brain-as-knowledge-graph, all observable on a single conference-room machine. Every behavior demonstrated on the mini is a behavior a deployed-at-customer ALX would also need.

## Open items

- **Audit branch not yet pushed** to `origin/gclyle/gro-551-mini-self-review-and-hardening` — awaiting founder confirmation per the no-push-without-ask rule.
- **Sequencing of GRO-552 through GRO-558** — founder's call. My read: GRO-552 + GRO-553 (close LAN exposure + rotate creds) before any partner sees the mini; GRO-557 (dev environment standup) before GRO-558 (adapter substrate) since 557 gates 558.

## Provenance

- Author: ALX (mini-resident, CLI-only)
- Founder: Jeffe (CLI conversation, 2026-04-25)
- Branch: `gclyle/gro-551-mini-self-review-and-hardening`
- Method: Live system inspection + git/Docker/lsof/scutil/curl + Linear MCP. No new tooling.
