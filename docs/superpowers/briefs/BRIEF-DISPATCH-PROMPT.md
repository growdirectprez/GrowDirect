# Wireframe Brief Dispatch — Autonomous Execution Prompt

Paste this entire prompt into a new Claude Code session. It is self-contained.

---

## YOUR MISSION

Write wireframe briefs for every screen in the Canary Go portal. This is a church session — spec work only, no code. Work autonomously through all six waves without stopping. Do not ask for approval between waves. Do not stop for clarification. Iterate until every brief is written and committed.

This is dispatch work for Linear issues GRO-782, GRO-783, GRO-784, GRO-785, GRO-786, GRO-787.

---

## SOURCE DOCUMENTS — READ THESE FIRST

Before writing a single brief, read all four source documents in full:

1. `/Users/gclyle/GrowDirect/docs/superpowers/specs/2026-05-04-canary-go-sitemap.md`
   — Canonical URL hierarchy, 12 nav sections, ~110 screens, roles, wave assignments, CP equivalents, origin flags (O/N/L4/FD)

2. `/Users/gclyle/GrowDirect/docs/superpowers/specs/2026-05-04-canary-go-screen-scenario-map.md`
   — Full user scenario enumeration per screen: entry points, display elements, actions, UX callouts, CP form equivalents

3. `/Users/gclyle/GrowDirect/docs/superpowers/specs/2026-05-04-counterpoint-canary-ux-crosswalk.md`
   — Counterpoint feature surface mapped against Canary; 10 UX displacement targets with design callouts

4. `/Users/gclyle/GrowDirect/docs/superpowers/specs/2026-05-04-canary-go-l4-gap-delta.md`
   — CRB L4 gap analysis: structural gaps (OTB, B2B layer, Distribution Recs) and lower-priority gaps per module

---

## BRIEF FORMAT — EVERY SCREEN GETS THIS

File: one markdown file per screen. No exceptions. Even single-page list screens get their own file.

```markdown
---
screen: <URL>
title: <Screen Title>
role: <LP | MGR | BYR | RCV | ADM | EMP — primary role(s)>
wave: <W1 | W2 | W3 | W4 | W5 | Cross>
origin: <O | N | L4 | FD>
cp_equivalent: <Counterpoint form name, or "None">
---

# <Screen Title>

**URL:** `<url>`  
**Primary role:** <role>  
**Entry points:** <how users reach this screen — nav item, link from X, notification deep-link, etc.>

## Layout

Describe the screen in layout zones. Use plain language — no wireframe syntax needed. Each zone gets one sentence on what lives there and why.

| Zone | Content | Notes |
|---|---|---|
| Header | ... | ... |
| Main content | ... | ... |
| Right rail / sidebar | ... | ... |
| Action bar | ... | ... |

*(Omit zones that don't apply. Add zones if the screen warrants it.)*

## Key Elements

The 3–5 most important UI elements. For each: what it is, what data it shows, any critical specs (column list, filter options, badge states, empty state).

### <Element name>
<Description. Column list if a table. States if a badge. Field list if a form.>

*(Repeat for each key element)*

## Interaction Flows

The 2–3 most important user actions. Format: trigger → what happens → result state.

1. **<Action name>:** <User does X> → <System does Y> → <Screen shows Z>
2. **<Action name>:** ...
3. **<Action name>:** ...

## UX Callout

One paragraph. What does Canary do here that Counterpoint cannot? What is the design decision that makes this screen worth building? If this is a net-new capability (no CP equivalent), state what problem it solves that was previously invisible or manual. Be specific — no generic "improved UX" language.

## Navigation Exits

Where does this screen lead? List the screens a user can reach from here via clicks, links, or actions.

- `<url>` — <why they'd go there>
- `<url>` — <why they'd go there>

## Open Questions

If any design decision is genuinely ambiguous (not answerable from source docs), list it here. Otherwise omit this section entirely.
```

---

## OUTPUT DIRECTORY STRUCTURE

```
docs/superpowers/briefs/
├── admin/          ← Admin + DevOps screens (GRO-787)
├── wave-1/         ← LP Investigator Core (GRO-782)
├── wave-2/         ← Store Ops + Devices (GRO-783)
├── wave-3/         ← Finance + Purchasing + Planning (GRO-784)
├── wave-4/         ← Merchandising + Labor (GRO-785)
└── wave-5/         ← W-Execution + Operations (GRO-786)
```

File naming: URL slug with slashes replaced by hyphens. Examples:
- `/alerts` → `alerts-list.md`
- `/alerts/:id` → `alerts-detail.md`
- `/cases/hawk` → `cases-hawk-list.md`
- `/cases/hawk/:id` → `cases-hawk-detail.md`
- `/inventory/count/new` → `inventory-count-new.md`
- `/inventory/count/:id` → `inventory-count-entry.md`
- `/inventory/count/:id/post` → `inventory-count-post.md`
- `/settings/allowlist/discounts` → `settings-allowlist-discounts.md`
- `/admin/devops/health` → `admin-devops-health.md`

---

## EXECUTION ORDER

Work in this sequence. Complete each group before moving to the next. Commit after each group.

### Group 0 — Admin + DevOps (9 screens) → `briefs/admin/`

```
/admin/users
/admin/users/:id
/admin/audit
/admin/config
/admin/tenants
/admin/tenants/:id
/admin/devops/health
/admin/devops/deployments
/admin/devops/infra
```

Commit: `feat(briefs): admin + devops wireframe briefs (9 screens)`

---

### Group 1 — Wave 1 LP Investigator Core (25 screens) → `briefs/wave-1/`

**Surveillance:**
```
/alerts
/alerts/:id
/chirps
/chirps/:id
/rules
/rules/:id
```

**Investigations:**
```
/cases/hawk
/cases/hawk/:id
/cases/hawk/:id/evidence
/cases/hawk/analytics
/cases/hawk/patterns
```

**Customers (W1 tabs — write as separate brief files even though they share a parent route):**
```
/customers
/customers/:id
/customers/:id → Risk tab
/customers/:id → Context tab
```

**Settings — LP substrate (allow-lists and store config share layout pattern; brief the first of each group fully, reference it for the rest):**
```
/settings/alert-routing
/settings/training-mode
/settings/allowlist/dead-count
/settings/allowlist/discounts
/settings/allowlist/voids
/settings/allowlist/comps
/settings/store/drawer
/settings/store/discounts
/settings/store/void-reasons
/settings/store/comp-reasons
```

Commit: `feat(briefs): wave 1 LP investigator core wireframe briefs (25 screens)`

---

### Group 2 — Wave 2 Store Ops + Devices (22 screens + 4 placeholders) → `briefs/wave-2/`

```
/transactions
/transactions/:id
/transactions/:id/proof
/items
/items/:id
/items/new
/items/:id/edit
/transfers
/transfers/new
/transfers/:id
/transfers/:id/receive
/transfers/:id/variance
/inventory/count
/inventory/count/new
/inventory/count/:id              ← dual persona: counter (mobile) + manager (portal)
/inventory/count/:id/post
/inventory/adjustments
/inventory/adjustments/new
/devices
/devices/:id
/devices/health
/reports/flash
/reports/category
/settings/store/locations
/settings/store/stations
/settings/catalog
```

**Placeholders (brief header + layout stub only — mark Open Questions section with "Deferred: camera/sensor integration spec required"):**
```
/devices/cameras
/devices/cameras/:id
/devices/sensors
/devices/sensors/:id
```

Commit: `feat(briefs): wave 2 store ops + devices wireframe briefs (22 screens + 4 placeholders)`

---

### Group 3 — Wave 3 Finance + Purchasing + Planning (28 screens) → `briefs/wave-3/`

```
/vendors
/vendors/:id
/orders/suggested
/orders/distribution
/orders
/orders/new
/orders/:id
/otb
/otb/:period
/receiving
/receiving/:id
/receiving/:id/close
/receiving/blind
/returns
/returns/:id
/reports/eod
/reports/finance
/reports/payments
/reports/tax
/reports/ar-aging
/reports/gift-cards
/reports/forecast
/agents
/agents/junctions
/agents/:id
/agents/config
/customers/:id → Commercial tab
/customers/:id → AR tab
/settings/payment
```

Commit: `feat(briefs): wave 3 finance + purchasing + planning wireframe briefs (28 screens)`

---

### Group 4 — Wave 4 Merchandising + Labor (15 screens) → `briefs/wave-4/`

```
/promotions
/markdowns
/markdowns/new
/markdowns/:id
/reports/range
/reports/price-history
/reports/markdowns
/reports/grid
/reports/pricing
/timecards
/timeclock
/timecards/export
/customers/:id → Loyalty tab
/settings/loyalty/programs
/settings/pricing/rules
```

Commit: `feat(briefs): wave 4 merchandising + labor wireframe briefs (15 screens)`

---

### Group 5 — Wave 5 W-Execution + Operations (9 screens) → `briefs/wave-5/`

```
/exceptions
/exceptions/:id
/cases
/cases/new
/cases/:id/evidence
/cases/:id/correlation
/cases/:id/remediate
/reports/cases
/settings/vertical-pack
```

Commit: `feat(briefs): wave 5 W-execution + operations wireframe briefs (9 screens)`

---

### Final commit

After all groups are done:

```
feat(briefs): complete Canary Go wireframe brief library — ~110 screens across 6 wave groups

Covers: Admin/DevOps (9), Wave 1 LP Core (25), Wave 2 Store Ops + Devices (22+4),
Wave 3 Finance + Purchasing + Planning (28), Wave 4 Merchandising + Labor (15),
Wave 5 W-Execution (9). Each brief: layout zones, key elements, interaction flows,
UX callout, navigation exits. Input for wireframe design sprint.
```

---

## DESIGN RULES — DO NOT VIOLATE

**Always:**
- Name the CP form being displaced (or state "None — net-new capability")
- Specify the hash/seal/proof element on any screen that touches transaction or evidence data — it is a non-negotiable design requirement
- Brief the mobile persona separately when a screen has one (`/inventory/count/:id`, `/receiving/:id`, `/timeclock`)
- State what is NOT on the screen when restraint is the design decision (especially `/timeclock`)

**Never:**
- Generic UX callouts ("cleaner interface", "better UX") — be specific about the mechanism
- Omit the empty state — every list/table brief must specify what shows when there's no data
- Brief a tab as a standalone screen without referencing the parent route

**For net-new capabilities (OTB, Distribution Recs, Demand Forecast, Agents/Junctions, Camera/Sensor placeholders, Cross-domain correlation):**
- The UX Callout section must explain what problem was previously invisible or handled manually, and exactly how Canary surfaces it

**Screen families that share a layout pattern — brief the first fully, note the inheritance for the rest:**
- Allow-list screens (4): fully brief `/settings/allowlist/dead-count`, reference for the other 3
- Store config LP threshold screens (4): fully brief `/settings/store/drawer`, reference for the other 3
- Finance report screens (EOD, Finance, Payments, Tax): brief EOD fully (most complex), reference for the others
- Wave 5 generalizes Wave 1: each Wave 5 brief must state "inherits from `<W1 equivalent>`" and document only the delta

---

## WHEN YOU FINISH EACH GROUP

1. Verify file count matches screen count for that group
2. Commit with the message above
3. Move immediately to the next group — do not pause, do not summarize to the user mid-run
4. After the final commit, output a one-paragraph completion summary with file count per group and any open questions you logged

---

## CONTEXT YOU NEED

**What Canary Go is:** A Go/GCP retail intelligence portal. "Above the POS" — reads from NCR Counterpoint via REST API, never writes to the register. 13-module spine. MCP-native architecture with 166 junctions. Target: multi-location SMB retail operators (L&G, farm/ranch, specialty). Primary channel: Rapid Garden POS (VAR partner).

**Primary UX differentiators:**
- Hash-chained evidentiary model — every transaction carries a cryptographic proof of integrity; no equivalent in CP
- Live transaction feed (Chirps) — operators see every transaction as it posts, not end-of-day
- Mobile-first physical count, transfer receipt, receiving, and clock-in — CP is Windows-desktop-only for all of these
- OTB budget control — CP has no OTB surface at all
- Distribution recommendations — machine-generated multi-location rebalancing; no CP equivalent
- Agents/Junction Map — 166 MCP junctions visualized; no concept of this in CP
- Cross-domain case correlation — same employee appears in LP case + timecard anomaly + receiving variance simultaneously

**User roles:**
- `LP` — Loss Prevention Investigator (primary Wave 1 user)
- `MGR` — Store Manager (primary Wave 2–3 user)
- `BYR` — Buyer / Merchandising Manager (primary Wave 3–4 user)
- `RCV` — Receiving Clerk (Wave 3)
- `ADM` — Admin / IT / Operator (cross-wave)
- `EMP` — Employee (time clock only)

---

## FACTORY ASSEMBLY — RUN AFTER ALL BRIEFS ARE COMMITTED

After the final brief group is committed, run the full factory pipeline to propagate the briefs into the knowledge substrate and produce the implementation plan.

### Step 1 — Index the briefs

```bash
cd /Users/gclyle/GrowDirect
python3 content-engine/engine.py registry build
```

This indexes all new brief files into the registry so the memory bus can find them.

### Step 2 — Seed the memory bus

```bash
python3 services/memory-bus/scripts/seed_standalone.py
```

Incremental by default — only seeds new and modified files. This makes every brief searchable via `memory_recall` in future sessions.

Verify seeding is progressing:
```bash
tail -f /tmp/memory-bus-seed.log
```

### Step 3 — Write the implementation plan

Using the brief library as input, invoke the `superpowers:writing-plans` skill to produce the Wave 1 implementation plan. The plan should cover:

- The navigation shell (sidebar, role-scoped visibility, routing)
- Wave 1 screens in build order (admin scaffold first, then LP core in dependency order)
- For each screen: what Go handler it needs, what template it needs, what data it reads, what MCP junctions it touches
- Test scaffolding per screen

Output: `docs/superpowers/plans/2026-05-04-canary-go-wave-1-implementation-plan.md`

### Step 4 — File implementation dispatches for Wave 1

After the plan is written, file Linear issues for each Wave 1 implementation block. Target: `mini` (state work). Use the plan's build-order groupings as the dispatch units. Each dispatch should reference:
- The brief file(s) it implements
- The plan section it corresponds to
- Expected output: committed Go handler + template + test

Title format: `implement <screen-group> — Wave 1 Canary Go portal`

Labels: `mini`, `ALX`, `Canary Builder`
Project: GRO (not Dispatch — these are engineering issues)

### Step 5 — Update Brain/wiki/canary-go-portal.md

Add a "Wireframe Brief Library" section linking to the brief index and noting the wave structure. This keeps the portal MOC current.

---

## ITERATION NOTE

If context fills before all groups are complete: commit what's done, note the last completed group in a comment on the relevant Linear issue (GRO-782 through GRO-787), then continue in a new session using this same prompt. The output directory structure and commit convention make it easy to resume — check which `briefs/wave-*/` directories exist and start from the first incomplete group.

---

Now begin. Start with Group 0 (Admin + DevOps). Do not stop until all groups are committed and the factory assembly steps are complete.
