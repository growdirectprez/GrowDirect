# Prompt — Land the May 12 demo, gate senior dev engagement post-demo

## FRESH SESSION PROTOCOL — NO ASSUMED CHAT STATE

Every session in this repo starts with no assumed state from prior chat threads. Load context **only** from canonical sources:

1. This delivery prompt (the file you are reading)
2. Files listed in "Context to load before working" — read in order
3. `AGENTS.md` and `CLAUDE.md` (root) — always in scope
4. Brain wiki articles, SDDs, and capability cards reachable via `memory_recall` and `context_assemble`
5. Linear dispatch description and comments for the active ticket (GRO-802 here)
6. Repository state at session start (fresh clone or pulled `main`)

**Rules:**

- If a fact is not grounded in a canonical source, ask rather than guess. "I think we decided X last session" is not a canonical source.
- Decisions that matter live in Brain, in Linear comments, in wiki articles, in SDDs, in commits — not in chat memory. If it's not committed to one of those, it doesn't exist.
- `memory_recall()` and `context_assemble()` calls are mandatory at session start for domain work, per the memory bus section of `CLAUDE.md`. Do not skip them in the name of "fresh start" — fresh chat is not fresh corpus.
- Never reference "previous Claude responses," "earlier iterations," or "what we decided last week" unless that decision is grounded in Brain, Linear, an SDD, or a commit. If you can't cite it, it didn't happen.

**New contributor onboarding clause:**

When a partner or new contributor joins, they must:

- Start with a fresh Claude/Cursor project + fresh `git clone` of `growdirectprez/GrowDirect`
- Read this full prompt + `CLAUDE.md` + `AGENTS.md` as the single source of truth before touching any code
- Follow the "Context to load before working" table in order
- Run the `memory_recall` calls listed below
- First deliverable: walk the onboarding path, propose patches via PR for any confusing surfaces or gaps (per the dispatch protocol in `AGENTS.md`)

This protocol applies to the entire May 12 demo workstream and all subsequent senior-dev onboarding. Senior dev engagement remains gated until after the dry run (May 13+).

---

**Owner:** ALX (laptop) · **Status:** active · **Date:** 2026-05-05 · **Demo dry run:** 2026-05-12 (T-7) · **Parent dispatch:** GRO-802 (In Progress) · **Backlog reference:** GRO-803

## Governing thesis

The win is a real project online by May 12 — `demo.growdirect.io` clickable with a Square sandbox OAuth flow, `canary.growdirect.io` readable as the v1 vault, and a discovery endpoint Claude can wire into his own MCP. Everything else is parked. The senior dev engagement is **gated to post-demo by design** — onboarding into a working system is a different, better experience than onboarding into a half-built one, and founder time the next 7 days is the constraint. The next 2–3 days collapse Workstream 1 (Square OAuth) and Workstream 3 (v1 vault) to the bone, with Workstream 2 (discovery package) sequenced for mid-week once the visible artifact is up.

## Context to load before working

Read in this order. Do not skip.

| File / ticket | Why |
| --- | --- |
| `AGENTS.md` | Tool stack, service map, first-5-minutes protocol |
| `CLAUDE.md` (root) | Operating posture, session discipline, file layout, Fresh Session Protocol |
| Linear `GRO-802` | Active demo prep dispatch — the source of truth for May 12 |
| Linear `GRO-803` | Cohort hub backlog — context only, not active |
| `Brain/projects/Canary.md` | Project MOC with all wiki links |
| `Brain/wiki/cards/store-ops-capability-model.md` | 7-layer capability synthesis |
| `Brain/wiki/canary-go-portal.md` | SDD index, Linear links |
| `docs/superpowers/audits/2026-05-05-canarygo-readiness-audit.md` | Platform state as of today |
| `docs/conventions/scaffold-template.md` | Service scaffold convention |

Then call (mandatory, in this order):

```
memory_recall("Square OAuth canonical events")
memory_recall("canary-site v1 vault landing page")
context_assemble(topic="canary retail spine")
```

## Decisions already locked

- Subdomains: `canary.growdirect.io` (vault) · `demo.growdirect.io` (Square OAuth dashboard)
- Square environment: sandbox only
- v1 vault is wiki-only — no cohort framing, no contribution model surfaced; CONTRIBUTING in public mirror is a placeholder by design
- Public Go repo strategy: option (c) mirror script (`growdirect-llc/canary-go`), no monorepo split this week
- Python prototype: archived, not surfaced externally
- Senior dev engagement: gated to post-demo (May 13+)
- Cohort identity issuance via GCP Identity (Cloud Identity Free, not Workspace) is the leaning direction for GRO-803 — not implemented this week
- Prompts go to `docs/prompts/`. Plans go to `docs/superpowers/plans/`. Prompts orient sessions; plans capture execution sequence.

## The 7-day shape (T-7 to T-0)

| Day | Date | Workstream focus | Visible deliverable |
| --- | --- | --- | --- |
| Day 1 | 2026-05-05 (today) | WS1 + WS3 scaffolding | Square OAuth Go port started · DNS for both subdomains · canary-site repo scaffolded |
| Day 2 | 2026-05-06 | WS1 OAuth depth | Token persistence working in `app.pos_tenant_credentials` (AES-GCM) · merchant info fetch verified against sandbox |
| Day 3 | 2026-05-07 | WS1 dashboard + WS3 landing | First dashboard render (locations + last 10 payments) · vault landing page copy + SDD index draft |
| Day 4 | 2026-05-08 | WS1 devops panel | Connection panel, live webhook feed, rate limit headroom, test connection button |
| Day 5 | 2026-05-09 | WS2 discovery + mirror sync | `GET /v1/discovery/canary` returning OpenAPI + MCP registry + fixtures · public mirror script runs, `growdirect-llc/canary-go` populated |
| Day 6 | 2026-05-10 | Polish + integration | End-to-end walkthrough as if Claude is connecting · audit log + dlq tail filtered to source=square wired · vault coding standards page committed |
| Day 7 | 2026-05-11 | Dry run runbook + buffer | `docs/superpowers/runbooks/2026-05-12-demo-dry-run.md` committed · contingency time absorbed |

Internal dry run: 2026-05-12.

## Next 2–3 days, in detail

### Day 1 — today (2026-05-05)

1. **DNS** — confirm `demo.growdirect.io` and `canary.growdirect.io` records pointed at Cloud Run gateway and GitHub Pages respectively. If either is unset, set it now. Estimated: 30 min.
2. **Square OAuth Go port begin** — port the OAuth handshake from the Python prototype (`Canary/`) into a Go handler mounted on the existing Cloud Run gateway binary. Token storage skeleton in `app.pos_tenant_credentials`, encryption stubbed. End-of-day target: handshake redirect works against Square sandbox, even if persistence is not finalized.
3. **canary-site scaffold** — clone `growdirectprez/canary-site` to `/tmp/canary-site-$$`, scaffold landing page + SDD index page + coding standards page as empty stubs with frontmatter. Push. Delete clone. Per the no-persistent-clone rule.
4. **Commit cadence**: `demo(square): port oauth handshake stub` and `demo(vault): scaffold landing + sdd-index + coding-standards`.
5. **Linear update**: comment on GRO-802 with end-of-Day-1 status.

### Day 2 — 2026-05-06

1. **Square OAuth depth** — finish token persistence (AES-GCM via existing crypto package), expiry handling, refresh flow. Verify against Square sandbox: connect → fetch merchant info → store tokens → re-fetch using stored tokens.
2. **First dashboard render** — server-rendered template showing merchant name, location list, last 10 payments. Plain HTML + Tailwind. No JS framework.
3. **Linear update**: comment on GRO-802 end-of-Day-2.

### Day 3 — 2026-05-07

1. **Devops module Square panel** — connection panel (token validity, last_polled_at, expires_at), test connection button, audit log tail filtered to source=square. Wire to the existing devops UI patterns.
2. **Vault landing page copy** — write the landing page properly. One paragraph "what this project is" tied to platform thesis. Link to public repo (`growdirect-llc/canary-go`), live demo (`demo.growdirect.io`), SDD index. Apply brand voice — confident, opinionated, not corporate-neutral.
3. **SDD index draft** — curate 8–12 SDDs in reading order with one-line summaries. Pull from `docs/sdds/go-handoff/`.
4. **Linear update**: comment on GRO-802 end-of-Day-3.

## Senior dev engagement — gated to post-demo

**Not this week.** Founder time the next 7 days is the constraint, and onboarding a senior dev costs 4–8 hours of founder time the senior dev's first day. That budget is not available pre-demo.

**Action this week (low-cost):**

1. File a Linear dispatch in the Dispatch project: `Senior dev guidance — TBD — engagement scope and onboarding`. Status: Backlog. Target/laptop. Priority: Medium. Description specifies the engagement scope options (CI vs devcontainer vs code review vs pair programming), the onboarding path, the dispatch protocol explainer, and the first dispatch ("walk the onboarding path, propose patches to gaps").
2. **Do not draft a separate `external-engagement.md` doc.** The senior dev onboards through the actual repo's existing surfaces — this prompt + `AGENTS.md` + `CLAUDE.md` + Brain. Their first deliverable is the patch set that fixes whatever was confusing.
3. **Trigger condition for opening this dispatch:** 2026-05-13, day after the demo lands.

**Why not earlier:** the demo is the priority. A working `demo.growdirect.io` is a credibility surface during onboarding the senior dev can interact with. A half-built one is the opposite.

## Operating discipline reminders

- This is a **state session** for the duration of the demo work. Architectural tangents get captured as `/church` notes and redirected. Do not let demo work drift into design.
- Each day's commits land on `main` via PR per GRO-802. Commit format: `demo(<workstream>): <one-line>`.
- Brand voice runs against externally-facing copy (vault landing page, README in public mirror). Use the brand-voice skill family before committing public-facing prose.
- Brain wiki updates land in `Brain/wiki/` — not as loose files. Re-seed memory bus after any wiki additions: `python3 services/memory-bus/scripts/seed_standalone.py`.
- The founder is in flow when typing into chat. Filter when writing to disk. No exceptions.

## Open questions for founder (surface, do not assume)

1. **Senior dev engagement scope** — CI? Devcontainer? Code review? Pair programming? Each pulls a different shape of dev. Pick one or rank before filing the engagement dispatch.
2. **GCP Identity flavor for GRO-803** — Cloud Identity Free (identity only) or Workspace (identity + mailbox + Drive)? Leaning Cloud Identity Free; founder to ratify.
3. **Square OAuth scope creep risk** — if the OAuth port surfaces unexpected complexity (unlikely given the Python prototype works), do we descope the devops Square panel for Day 4 to keep dashboard solid? Pre-decide the contingency.
4. **Discovery package timing** — Day 5 is the slot. If WS1 slips, does WS2 slip with it or does WS3 (vault) absorb the slack? Pre-decide.

## How to land this work

- Each dispatch comment on GRO-802 includes: artifacts produced (paths), commit SHAs, one-paragraph summary, what's next.
- End of Day 7: dry run runbook committed at `docs/superpowers/runbooks/2026-05-12-demo-dry-run.md`.
- Senior dev engagement dispatch filed in Backlog by end of Day 1 so it's pre-loaded for May 13.
- This prompt referenced from GRO-802 description as the active execution prompt.

## Verification before declaring done

- `demo.growdirect.io` resolves, presents Square OAuth start screen, completes handshake against sandbox, renders dashboard with real data.
- `canary.growdirect.io` resolves, landing page reads cleanly, SDD index links work, coding standards page covers scaffold-template + factory + dispatch protocol.
- `growdirect-llc/canary-go` public mirror has README, LICENSE, CONTRIBUTING placeholder, and curated paths from CanaryGo.
- `GET /v1/discovery/canary` returns valid OpenAPI 3.0 + MCP registry, exercised end-to-end by a test client.
- Dry run runbook executes cleanly in a fresh session, no founder hand-holding required.

If any of those fail on May 11, the work is not done. Slip the dry run by 24 hours rather than ship a broken artifact.
