# Canary RapidPOS Site — Design Module Brief
**Target:** `canary.growdirect.io/rapidpos`
**Generated:** 2026-04-26
**Purpose:** Feed to Claude.ai Design Module to generate each page as a self-contained HTML artifact.

---

## Instructions to Claude.ai Design Module

You are building a multi-page technical website for **Canary RapidPOS** — a product by GrowDirect LLC. The site lives at `canary.growdirect.io/rapidpos`. Each page is a standalone HTML file with no external dependencies. No frameworks, no CDN, no build step. Every CSS rule is in a `<style>` block in the `<head>`. Every icon is inline SVG or a Unicode character. Every diagram is CSS/SVG — no image tags except the logo.

Build one page at a time. After generating a page, wait for "next" before continuing. Copy the `<style>` block and shared components exactly from page to page — visual consistency is critical.

---

## Visual Design System

### Do NOT replicate the existing Armstrong proposal.
The old proposal had: dark green full-page cover background, fixed left sidebar, heavy box-heavy sections, consulting-deck energy. This site is different — cleaner, more editorial, technical credibility first.

### Color Tokens

```css
:root {
  /* Base */
  --bg:           #F5F0E8;   /* parchment — page background */
  --bg-alt:       #EAE4D6;   /* slightly darker parchment — alternate rows, cards */
  --surface:      #FFFFFF;   /* white — card surfaces, code block bg */

  /* Green palette */
  --green-dark:   #1C3A2B;   /* primary text, headings, nav background */
  --green-mid:    #2A5240;   /* secondary headings, hover states */
  --green-light:  #4CAF7D;   /* accent, active states, diagram nodes */
  --green-faint:  rgba(76,175,125,0.10);  /* subtle tint backgrounds */

  /* Gold palette */
  --gold:         #BF8700;   /* CTAs, callout borders, key numbers */
  --gold-light:   #E8A800;   /* hover gold, highlighted stats */
  --gold-faint:   rgba(191,135,0,0.12);   /* callout backgrounds */

  /* Text */
  --text-primary:  #1C3A2B;  /* body copy — use green-dark, not black */
  --text-secondary:#3A3A3A;
  --text-muted:    #6B6B6B;
  --text-on-dark:  #F5F0E8;

  /* Borders */
  --border:        #D0C9BB;
  --border-subtle: rgba(28,58,43,0.10);

  /* Code */
  --code-bg:       #1C3A2B;
  --code-text:     #4CAF7D;
  --code-comment:  rgba(76,175,125,0.55);
}
```

### Typography

```css
/* Import in <head> — one link tag */
/* https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,wght@0,300;0,400;0,600;0,700;1,400&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap */

body       { font-family: 'Inter', system-ui, sans-serif; }
h1, h2, h3 { font-family: 'Source Serif 4', Georgia, serif; }
code, pre  { font-family: 'IBM Plex Mono', monospace; }
```

**Scale:**
- `h1` — 48px / weight 700 / line-height 1.08 / tracking -0.02em
- `h2` — 32px / weight 600 / line-height 1.2
- `h3` — 20px / weight 600 / line-height 1.3
- `body` — 16px / weight 400 / line-height 1.7
- `caption / label` — 11px / weight 700 / letter-spacing 0.1em / uppercase / color var(--gold)

### Layout

Max content width: `960px`, centered, `padding: 0 32px`.

**Shared top nav** (every page except `store-2030` and `armstrong`):
- Background: `var(--green-dark)`, height 56px
- Left: wordmark `CANARY` in Source Serif 4 italic + `/ RapidPOS` in Inter 400 muted
- Center: page links — Overview · Architecture · Endpoints · Quickstart
- Right: `Store of the Future →` link in gold, `Book a Call` button (gold border, small)
- Mobile: collapse to hamburger

**Page hero** (technical pages):
- NOT a full dark-green cover. A contained header block, max 280px tall.
- Background: `var(--green-dark)`, left-aligned text, eyebrow label in gold uppercase, h1 in white Source Serif 4, one-sentence subhead in muted text-on-dark.
- Bottom edge: a 4px gold rule, then page transitions to parchment background.

**Section spacing:** `padding: 80px 0` between major sections. `40px` between subsections.

### Component Patterns

**Callout box:**
```html
<div class="callout">
  <div class="callout-label">Key insight</div>
  <p>Content here.</p>
</div>
```
Style: gold-faint background, 2px left border in `var(--gold)`, `padding: 20px 24px`, rounded 6px.

**Stat block:**
```html
<div class="stat-grid">
  <div class="stat"><span class="stat-number">22,000+</span><span class="stat-label">Active NCR retailers</span></div>
</div>
```
Style: number in 42px Source Serif 4 bold green-dark, label in 12px Inter muted uppercase.

**Code block:**
```html
<pre class="code-block"><code>// content</code></pre>
```
Style: `var(--code-bg)` background, `var(--code-text)` monospace, `padding: 20px 24px`, rounded 8px, subtle left border in green-light.

**Layer diagram** (architecture pages): CSS flexbox stack, each layer a horizontal band. Green-dark for owned layers, gold-border for the prize layer. No images — pure CSS.

**Two-column layout (text + diagram):**
```html
<div class="split-layout">
  <div class="split-text">...</div>
  <div class="split-visual">...</div>
</div>
```
Style: `display:grid; grid-template-columns: 1fr 1fr; gap: 64px; align-items: start`.

**Tag / badge:**
Small inline pill: `background: var(--green-faint); color: var(--green-dark); border: 1px solid var(--green-light); padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 600`.

---

## Site Map

| File | URL | Purpose |
|---|---|---|
| `index.html` | `/rapidpos/` | Overview — what RapidPOS is, who it's for, the 3-layer pitch |
| `architecture.html` | `/rapidpos/architecture` | Technical deep dive — MCP layers, CRDM, data flow |
| `endpoints.html` | `/rapidpos/endpoints` | MCP tool reference — schemas, inputs, outputs |
| `integrate.html` | `/rapidpos/integrate` | VAR Quickstart — prerequisites, first live call in 15 min |
| `store-2030.html` | `/rapidpos/store-2030` | Store of the Future 2030 — vision pitch, presentation mode |
| `armstrong.html` | `/rapidpos/armstrong` | Armstrong Garden Centers — the applied pitch |
| `wiki-template.html` | `/rapidpos/ncr/modules/T-transaction-pipeline` | Reusable wiki page template — all vault pages use this shell |
| `ncr/**` | `/rapidpos/ncr/` | NCR Vault — full content copy rendered in site design system |
| `crb/**` | `/rapidpos/crb/` | Canary Retail Brain — full content copy |
| `catz/**` | `/rapidpos/catz/` | CATz Method — full content copy |

---

## Page 1: Overview (`index.html`)

**Audience state of mind:** Technical evaluator. Just landed here from a VAR conversation or a LinkedIn post. Has 90 seconds. Wants to know: is this real, is it technically legible, does it apply to me.

**Hero:**
- Eyebrow label: `CANARY · RAPIDPOS MCP SERVER`
- H1: `The missing layer between your POS and the AI economy`
- Subhead: `NCR Counterpoint retailers now have a direct API connection to every AI agent their customers use. RapidPOS delivers it. GrowDirect built it.`
- No buttons in hero — let the content earn the CTA.

**Section 1 — What it is (2 columns: text left, layer diagram right):**

Text:
> The customer's AI agent wants to query your inventory, check a price, look up their loyalty points, and put something on hold — right now, from wherever they are. RapidPOS is the VAR. GrowDirect built the MCP Server that sits between RapidPOS's existing NCR Counterpoint integration and every AI agent channel your retailer operates.
>
> This is not a chatbot integration. It is an MCP-native API layer that speaks JSON-RPC 2.0 over HTTPS + SSE — the same protocol Claude, GPT-4o, and every major AI assistant uses natively. The retailer's data stays in Counterpoint. The intelligence lives in the CRDM. The connection point is RapidPOS MCP Server.

Layer diagram (5 layers, CSS stack):
- Layer 5: `Customer AI Agent` — Claude / GPT-4o / Gemini (gray, not owned)
- Layer 4: `RapidPOS MCP Server` — **GOLD BORDER, labeled "The Prize"** — GrowDirect
- Layer 3: `NCR Counterpoint REST API` (green-dark)
- Layer 2: `Counterpoint POS` (green-dark)
- Layer 1: `Store Hardware / Terminals` (green-dark)

Caption under diagram: *"Layer 4 is the only layer nobody owns yet. Whoever builds it across 22,000+ NCR retailers controls the agent interface for every store on the platform."*

**Section 2 — Three capabilities (3-card grid):**

Card 1: **Inventory Intelligence**
> Real-time stock lookup across all store locations. "Is the Blue Agave in stock in Pasadena?" — answered in under 2 seconds via Counterpoint API + Redis cache.

Card 2: **Customer & Loyalty**
> Customer profile, purchase history, and loyalty balance — surfaced via MCP tool. The agent knows the customer before they speak.

Card 3: **Transactional**
> Holds, layaways, account payments. The agent doesn't just answer — it acts. On behalf of the customer, through the same Counterpoint transaction flow.

Cards: white surface on parchment bg, thin green-light top border, gold label, clean body copy. No icons.

**Section 3 — Stat block (3 stats in a row):**
- `22,000+` — Active NCR Counterpoint retailers in the VAR channel
- `13` — Canary platform modules on the CRDM spine
- `0` — Specialty retailers with a live MCP endpoint today

**Section 4 — Callout:**
> CRDM — NCR doesn't have it. RapidPOS doesn't have it. Canary does. It is the moat.

**Footer CTA:** `Read the architecture →` (links to `architecture.html`) and `Book a technical call` (gold button, mailto link).

---

## Page 2: Architecture (`architecture.html`)

**Audience state of mind:** Engineer or technical CTO. Wants to see: is the data model real, how does streaming work, what's the latency story, what do I actually integrate against.

**Hero:**
- Eyebrow: `TECHNICAL ARCHITECTURE`
- H1: `The CRDM is the foundation. Everything else is a module.`
- Subhead: `Three-database PostgreSQL architecture connected to a live NCR Counterpoint transaction stream. The MCP Server sits on top. The agents sit on top of that.`

**Section 1 — The CRDM (split layout: description left, schema visual right):**

Text:
> The Centralized Retail Data Model is a three-database PostgreSQL architecture that normalizes every transaction from every Counterpoint terminal into a unified canonical data model. It is the layer that neither NCR Counterpoint nor RapidPOS provides — and what all 13 Canary modules depend on.

Schema visual (CSS table/grid showing 3 databases):

```
canary_app      ← Customer profiles, store config, loyalty, user accounts
canary_sales    ← Transactions, line items, returns, holds, markdowns
canary_metrics  ← Aggregated signals, demand curves, replenishment queues
```

Each database as a styled box: green-dark header, column list in monospace, border in green-light.

**Section 2 — Transaction Streaming Pipeline:**

> Phase 1 polls the NCR Counterpoint REST API on a 60-second cycle — every sale, return, hold, and markdown from every terminal flows into canary_sales. Phase 2 upgrades to webhook push — inventory events fire on transaction, cache invalidated in real time. The CRDM goes from 60-second to sub-second accuracy.

Code block showing example tool call:
```json
{
  "tool": "inventory_lookup",
  "params": {
    "sku": "AGAVE-BLU-5G",
    "store_ids": ["PAS", "MON", "LAG"],
    "include_holds": true
  }
}
```

Example response:
```json
{
  "sku": "AGAVE-BLU-5G",
  "stores": [
    { "id": "PAS", "on_hand": 4, "on_hold": 1, "available": 3 },
    { "id": "MON", "on_hand": 0 },
    { "id": "LAG", "on_hand": 7, "available": 7 }
  ],
  "cache_age_seconds": 18
}
```

**Section 3 — MCP Protocol:**

> The MCP Server exposes tools over JSON-RPC 2.0 via HTTPS with Server-Sent Events for streaming responses. Any MCP-compatible AI client connects without custom integration — Claude, GPT-4o, and any agent built on the Model Context Protocol speaks this natively.

Small diagram: `Agent → HTTPS/SSE → MCP Server → Counterpoint REST API → Counterpoint DB`

**Section 4 — Security model:**
> API key authentication per retailer tenant. All Counterpoint credentials stay server-side — the MCP client never sees them. Rate limiting at the MCP layer (not passed through to Counterpoint). Read-only tools have no state side effects. Transactional tools (holds, payments) require explicit customer consent scoping.

**Section 5 — 13 Modules table:**

| Module | Name | Description |
|--------|------|-------------|
| T | Transaction Streaming | Live Counterpoint feed → CRDM |
| R | Customer Record | Profile, history, Sunset zone, garden record |
| I | Inventory | Real-time stock across all locations |
| P | Pricing | POS pricing, promotions, and markdown rules |
| L | Loyalty | Points balance, tier, redemption |
| D | Diagnostics | Plant symptom → diagnosis → treatment → product |
| Q | Replenishment | Demand signals, reorder queues |
| W | Wayfinding | Store layout, product location |
| A | Associate | Staff availability and expertise routing |
| S | Seasonal | Zone-specific calendar, planting windows |
| K | Knowledge | Domain vault — species library, care notes |
| M | Merchandising | Planogram, assortment, markdown rules |
| G | Google | Merchant Center feed, Shopping inventory |

---

## Page 3: Endpoints (`endpoints.html`)

**Audience state of mind:** Engineer building an integration. Wants exact schemas. Treat this like API documentation.

**Hero:**
- Eyebrow: `MCP TOOL REFERENCE`
- H1: `Endpoints`
- Subhead: `All tools exposed by the RapidPOS MCP Server. JSON-RPC 2.0. Read-only tools return immediately; transactional tools require customer consent scope.`

For each tool, use this repeating block structure:
```
[TOOL NAME BADGE]  tool_name
Description: one sentence
Input schema | Output schema | Notes
Example call | Example response
```

**Tools to document (6 primary):**

**1. inventory_lookup**
- Description: Real-time stock query across one or more store locations.
- Inputs: `sku` (string, required), `store_ids` (array, optional — omit for all stores), `include_holds` (bool, default false)
- Output: per-store `on_hand`, `on_hold`, `available`, `cache_age_seconds`
- Note: cached via Redis; cache TTL 60s Phase 1, event-invalidated Phase 2.

**2. customer_profile**
- Description: Retrieve customer record by email or loyalty ID.
- Inputs: `lookup_type` (enum: email|loyalty_id), `value` (string)
- Output: `customer_id`, `name`, `loyalty_tier`, `points_balance`, `purchase_history_summary`, `garden_record`
- Note: requires `customer:read` consent scope.

**3. loyalty_balance**
- Description: Point balance and tier for a known customer.
- Inputs: `customer_id` (string)
- Output: `points`, `tier`, `next_tier_threshold`, `expiry_date`

**4. place_hold**
- Description: Reserve an item at a specific store for a customer.
- Inputs: `sku`, `store_id`, `customer_id`, `quantity` (int, default 1), `hold_duration_hours` (int, default 48)
- Output: `hold_id`, `expires_at`, `confirmation`
- Note: requires `transactions:write` consent scope. Creates a Counterpoint hold record.

**5. price_lookup**
- Description: Current POS price for a SKU, including active promotions.
- Inputs: `sku`, `store_id`, `customer_id` (optional — applies loyalty pricing if provided)
- Output: `regular_price`, `sale_price`, `promotion_name`, `loyalty_price`

**6. plant_diagnostic**
- Description: Symptom-to-treatment lookup from the domain knowledge vault.
- Inputs: `symptoms` (array of strings), `plant_type` (string, optional), `sunset_zone` (int, optional)
- Output: `diagnosis`, `confidence`, `treatment_steps`, `recommended_products` (with SKUs), `care_notes`
- Note: knowledge layer tool — does not hit Counterpoint. Returns from domain vault.

---

## Page 4: VAR Quickstart (`integrate.html`)

**Audience:** A RapidPOS VAR engineer setting up a retailer. 15-minute guide to first live call.

**Hero:**
- Eyebrow: `VAR QUICKSTART`
- H1: `First live call in 15 minutes`
- Subhead: `Prerequisites, credentials, and a working inventory_lookup call against your Counterpoint instance.`

**Structure:** numbered steps with code blocks. Clean, minimal. Think Stripe Docs, not a PowerPoint.

**Step 1 — Prerequisites**
- NCR Counterpoint 8.5.x or higher
- RapidPOS VAR account (contact: `vars@growdirect.io`)
- Docker (for local dev) or access to your deployment environment
- A Counterpoint API key with inventory read permissions

**Step 2 — Environment**
```bash
# Pull the server image
docker pull growdirect/rapidpos-mcp:latest

# Configure environment
export COUNTERPOINT_API_URL=https://your-cp-instance.com/api
export COUNTERPOINT_API_KEY=your_key_here
export TENANT_ID=your_retailer_id
export REDIS_URL=redis://localhost:6379
```

**Step 3 — Start the server**
```bash
docker run -p 3000:3000 \
  -e COUNTERPOINT_API_URL \
  -e COUNTERPOINT_API_KEY \
  -e TENANT_ID \
  -e REDIS_URL \
  growdirect/rapidpos-mcp:latest
```

**Step 4 — First call**
```bash
curl -X POST http://localhost:3000/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_mcp_api_key" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "inventory_lookup",
      "arguments": { "sku": "TEST-SKU", "store_ids": ["STORE1"] }
    },
    "id": 1
  }'
```

**Step 5 — Connect an agent**

> Any MCP-compatible agent connects by pointing at `http://localhost:3000/mcp` with a valid API key. No custom integration layer required. Claude, any Claude Code session, or any custom agent built on the MCP SDK connects natively.

**Callout at bottom:**
> Need the full implementation guide or help with a retailer-specific Counterpoint config? Contact `vars@growdirect.io`. Response within one business day.

---

## Page 5: Store of the Future (`store-2030.html`)

**Audience:** Executive, CTO, strategic partner. This is the vision page. Different visual treatment — break out of the doc layout into something more like a premium editorial / annual report spread.

**IMPORTANT: Different layout for this page.**
- NO top nav bar. Instead: minimal top stripe with `CANARY · RAPIDPOS` wordmark left and `← Back to docs` right, in parchment on green-dark, height 44px.
- Full-width sections with alternating backgrounds. No max-width constraint on the hero.
- Large typography. More whitespace. Let the content breathe.
- The gold rule `<hr>` is used as a section divider — `height: 2px; background: var(--gold); border: none; width: 80px; margin: 0 auto 60px`.

**Section 1 — Opening (full-width dark green):**
- Parchment text on green-dark background
- Large pull quote: *"In 2030, a customer's AI agent will walk into your store before they do."*
- Body: *The retail transaction of 2030 doesn't start at the register. It starts when the customer's AI begins shopping on their behalf — querying inventory, comparing prices, checking loyalty balances, reserving items — all before the customer leaves the house. The retailers that built the API layer to connect to that agent own the relationship. The ones that didn't are waiting for foot traffic that never arrives.*
- Full-width. Centered. No max-width.

**Section 2 — The 2030 Customer Journey (parchment bg):**
Present as a horizontal timeline with 5 moments. Each moment: an icon (inline SVG or emoji — use sparingly), a moment label, and 2 sentences.

1. **Agent queries inventory** — *Thursday, 7pm. The customer asks their AI to find a 5-gallon Blue Agave near Pasadena. The agent calls inventory_lookup. Three stores return results in 1.8 seconds.*
2. **Agent reserves the item** — *Place_hold fires. Counterpoint creates a 48-hour hold at the Pasadena store. The customer gets a confirmation. No human involved.*
3. **Customer walks in** — *Saturday morning. The associate's tablet shows the customer's profile: name, loyalty tier, garden record, the hold. The conversation starts from context, not from scratch.*
4. **Loyalty applied at checkout** — *loyalty_balance pulls the current points. The promotion applies automatically. The customer pays less. They remember it.*
5. **Agent follows up** — *10 days later. The knowledge vault surfaces a care reminder. The agent sends it. The customer comes back.*

**Section 3 — The business case (two columns):**
Left — text:
> The NCR Counterpoint VAR channel has 22,000+ active retailers. Pet supply, nursery, hardware, wine, outdoor goods, sporting equipment. Every one of them faces the same structural gap: their customer's AI can transact, but there is no endpoint to connect to. RapidPOS already has the VAR relationships. GrowDirect built the layer. The distribution math is straightforward.

Right — large stat block:
- `22,000+` retailers in the NCR Counterpoint VAR channel
- `$0` current MCP endpoint revenue across the entire channel
- `Layer 4` is unowned. First to scale wins.

**Section 4 — Gold section (parchment bg, gold-border callout):**
> This is not a 2030 prediction. The protocol is live. The server is running. The first retailer is connected. Armstrong Garden Centers — 31 stores, 136 years, 1,184 employee-owners — is the proof of concept. The conversation about what comes next starts here.

**CTA:**
Two buttons side by side: `Read the Armstrong Pitch →` (gold fill) and `See the Architecture` (green border).

---

## Page 6: Armstrong (`armstrong.html`)

**Audience:** Armstrong decision-maker or a partner reviewing the applied pitch. This is the condensed proposal — solution-first, no strategy theater. The positioning and competitive analysis from the old Armstrong proposal is gone. What remains: here is the problem, here is what we built, here is how it works for Armstrong specifically.

**IMPORTANT: Same special layout as store-2030 — no doc nav, minimal top stripe.**

**Hero (full-width, green-dark):**
- Eyebrow: `ARMSTRONG GARDEN CENTERS · APPLIED PITCH`
- H1: *Armstrong + RapidPOS = The first MCP-native specialty retailer in America.*
- Subhead: *31 stores. 136 years of horticultural expertise. NCR Counterpoint live. The CRDM is being built. ALX goes live when it is.*
- No decorative background texture. Clean. Let the type carry it.

**Section 1 — The gap (parchment):**
Short. Two paragraphs.

> Armstrong has 31 stores, 136 years of SoCal horticultural expertise, and a 100% ESOP structure that makes every associate a stakeholder in the outcome. The business has three structural advantages that no competitor can replicate: local knowledge encoded in its horticulturists, a supply chain that grows native plants at scale, and the trust of a customer base that drives 40 minutes for the right plant.
>
> The gap is that none of it travels beyond the store floor. The horticulturist's expertise ends when the customer leaves. ALX closes the gap — not as a chatbot, as a persistent, zone-aware, inventory-connected garden horticulturist available 24 hours a day across every AI channel Armstrong operates.

**Section 2 — What ALX is (split layout):**
Left text:
> ALX is the VSM persona running on Canary's CRDM. It knows the customer's Sunset zone. It remembers what they planted last September. It checks whether the agave is in stock at Pasadena before they make the drive. It follows up in August to say it's time to plant. ALX™ is a trademark of GrowDirect LLC.

Right: a clean list of 6 VSM capabilities as pills/tags:
`Inventory Lookup` · `Customer Garden Record` · `Plant Diagnostics` · `Seasonal Calendar` · `Loyalty & Pricing` · `Store Wayfinding`

**Section 3 — The Armstrong Horticulture Vault:**
> Every other retail AI solution starts with generic training data and specializes later. ALX starts with the Vault — a structured knowledge base built from Armstrong's 136 years of SoCal horticultural expertise: the Sunset zone matrix for Zones 21–24, a plant diagnostics library (86+ conditions mapped to symptom → diagnosis → treatment → product), the SoCal seasonal calendar (month-by-month, zone-specific), and a full species library with provenance and care notes.

**Section 4 — Two-phase delivery (timeline or two-column):**

Phase 1:
> Stand up the CRDM: the three-database PostgreSQL architecture connected to the NCR Counterpoint transaction stream. Every sale, return, hold, and markdown from every terminal flows into one canonical data warehouse. This phase ends when the data is clean, current, and unified across all 31 stores.

Phase 2:
> With the CRDM live, each of the 13 Canary modules is configured against real Armstrong transaction history. The RapidPOS MCP Server goes live. ALX is not installed cold — it is configured against years of actual Armstrong data, which means it is useful on day one.

**Section 5 — Armstrong at a glance (stat block):**
- `31` Stores across Southern California
- `136` Years of horticultural expertise
- `1,184` Employee-owners (100% ESOP)
- `13` Canary modules on the CRDM spine
- `0` MCP endpoints among specialty garden retailers today

**Section 6 — The channel opportunity (callout):**
> Armstrong is one of 22,000+ retailers in the NCR Counterpoint VAR channel. The Armstrong Horticulture Vault is the template — domain-adapted for each vertical. The platform business is: same CRDM architecture, same MCP server, new vault per vertical, distributed via RapidPOS's existing VAR relationships. Armstrong proves the model.

**Closing CTA:**
- `canary@growdirect.io`
- `Read the full architecture →`
- No pricing on this page.

---

---

## Vault Content Pages — Wiki Template

The site also hosts inline copies of three knowledge vaults — NCR, CRB (Canary Retail Brain), and CATz — rendered in the same design system as the technical docs. These replace the separate Quartz sites at `ncr.growdirect.io`, `crb.growdirect.io`, and `catz.growdirect.io` for this context. All vault content is served under the `/rapidpos/` path.

### URL structure

```
canary.growdirect.io/rapidpos/
├── ncr/                        ← NCR Counterpoint Vault
│   ├── index.html              ← vault home (from Home.md)
│   ├── integration/
│   │   └── index.html
│   ├── modules/
│   │   ├── index.html
│   │   ├── T-transaction-pipeline.html
│   │   ├── R-customer.html
│   │   └── ... (one file per module)
│   ├── agents/
│   ├── pitch/
│   ├── sandbox/
│   └── verticals/
├── crb/                        ← Canary Retail Brain
│   ├── index.html
│   ├── platform/
│   ├── modules/
│   └── case-studies/
└── catz/                       ← CATz Method
    ├── index.html
    ├── method/
    ├── agents/
    ├── proof-cases/
    └── ...
```

### Wiki page template spec

**Layout:** Same top nav as technical pages. Below nav: a two-column layout — narrow left sidebar (vault nav), main content area.

**Left sidebar** (240px, fixed, green-dark bg):
- Vault name as header: e.g., `NCR VAULT` in gold uppercase label, then vault tagline in small muted text
- Collapsible section groups matching the vault's folder structure
- Active page highlighted in green-light with left accent bar
- Links styled identically to a Quartz sidebar but in the site's CSS — no Quartz dependency

```html
<nav class="wiki-sidebar">
  <div class="wiki-vault-header">
    <span class="label">NCR VAULT</span>
    <p>RapidPOS MCP Server — reference and integration</p>
  </div>
  <div class="wiki-section">
    <div class="wiki-section-label">Integration</div>
    <a href="/rapidpos/ncr/integration/" class="wiki-nav-link">Overview</a>
  </div>
  <div class="wiki-section">
    <div class="wiki-section-label">Modules</div>
    <a href="/rapidpos/ncr/modules/T-transaction-pipeline" class="wiki-nav-link active">T — Transaction Pipeline</a>
    <a href="/rapidpos/ncr/modules/R-customer" class="wiki-nav-link">C — Customer</a>
    <!-- ... -->
  </div>
</nav>
```

**Main content area** (fills remaining width, max ~720px of readable text):
- Breadcrumb at top: `RapidPOS / NCR Vault / Modules / T — Transaction Pipeline`
- `h1` from the markdown file's first `#` heading
- Body content: standard markdown → HTML conversion
- `h2`, `h3` rendered in Source Serif 4 with a subtle gold-left-border rule on `h2`
- Code blocks use the same `code-block` style as the technical pages (green-dark bg, green-light text)
- Internal links between vault pages use relative paths within `/rapidpos/ncr/`
- Callout blocks (Obsidian `> [!note]` syntax) → styled as the site's `callout` component
- Back-links section at the bottom: `Referenced by:` with linked page names

**Vault switcher** in the sidebar footer: small links to switch between NCR / CRB / CATz vaults. Keeps the user within the site.

```html
<div class="vault-switcher">
  <span class="label">Vaults</span>
  <a href="/rapidpos/ncr/" class="vault-link active">NCR</a>
  <a href="/rapidpos/crb/" class="vault-link">CRB</a>
  <a href="/rapidpos/catz/" class="vault-link">CATz</a>
</div>
```

### Markdown conversion conventions

When converting vault `.md` files to HTML for this site:

| Markdown | HTML output |
|---|---|
| `# Heading` | `<h1>` with Source Serif 4 |
| `## Heading` | `<h2>` with gold left-border rule |
| `### Heading` | `<h3>` |
| ` ```code``` ` | `<pre class="code-block"><code>` |
| `> [!note]` | `<div class="callout">` |
| `> [!warning]` | `<div class="callout callout-warning">` (gold border → red border) |
| `[[wikilink]]` | `<a href="/rapidpos/ncr/slugified-name">` |
| `**bold**` | `<strong>` |
| `*italic*` | `<em>` |
| Tables | `<table class="wiki-table">` — styled with alternating row shading in parchment/bg-alt |
| Frontmatter `---` | Strip entirely — do not render |

### Page 7: Wiki template page (generate this as one artifact)

Generate a single `wiki-template.html` that demonstrates the full wiki layout using a representative NCR vault article — `T — Transaction Pipeline` from the modules section. This is the reusable template. Subsequent vault pages are produced by swapping in content while keeping the surrounding shell identical.

The template page should include:
- The full top nav (same as technical pages)
- The two-column wiki layout (sidebar + content)
- The vault switcher in the sidebar footer
- A breadcrumb
- One complete rendered article showing all element types: headings, body copy, a code block, a callout, a table, and internal links
- The back-links section at the bottom

**Sample content for the template (T — Transaction Pipeline):**

> **T — Transaction Pipeline** is the data foundation module. It connects the NCR Counterpoint REST API to the CRDM in real time, normalizing every transaction — sales, returns, holds, markdowns — from every terminal into `canary_sales`. Every other Canary module depends on T being live and current.
>
> **Phase 1:** Polling at 60-second intervals. Every Counterpoint terminal's transaction log is pulled on the cycle, diffed against the last snapshot, and written to `canary_sales`. Idempotent — safe to replay.
>
> **Phase 2:** Webhook push. Counterpoint fires an event on every transaction. The TSP receives it, validates it, and writes to `canary_sales` in under 500ms. Cache in Redis is invalidated on the event. Inventory accuracy goes from 60s to near-instant.
>
> **Schema note:** Every transaction row in `canary_sales` includes `store_id`, `terminal_id`, `transaction_type` (SALE|RETURN|HOLD|MARKDOWN), `sku`, `quantity`, `unit_price`, `customer_id` (nullable), and `counterpoint_transaction_id` for traceability back to the source system.

---

## Generation Instructions

Generate pages in this order:
1. `index.html` — establish the design system here; all other pages copy from it
2. `architecture.html`
3. `endpoints.html`
4. `integrate.html`
5. `store-2030.html` — use the alternate layout
6. `armstrong.html` — use the alternate layout
7. `wiki-template.html` — the reusable vault page template (NCR / T — Transaction Pipeline as sample content)

After generating each page, confirm the file name and ask for any changes before continuing to the next.

**What not to do:**
- No animated gradients or heavy visual effects on technical pages
- No placeholder text (`Lorem ipsum`, `[coming soon]`, `TBD`)
- No icon libraries (Font Awesome, Heroicons) — use inline SVG or omit icons entirely
- No external CSS frameworks (Tailwind, Bootstrap)
- No React, Vue, or any JS framework
- No `<img>` tags for diagrams — use CSS/SVG
- Do not replicate the dark green full-page cover from the old Armstrong proposal
- The pitch deck pages (store-2030, armstrong) break the doc layout — do not apply the doc nav to them

**File naming:** Each file is named exactly as shown in the site map. The `<title>` tag follows the pattern `[Page Title] — Canary RapidPOS`.

**Shared `<style>` block:** After generating page 1, extract the complete CSS into a comment block at the top of each subsequent page so the design system is visible and copyable for any page generated independently.
