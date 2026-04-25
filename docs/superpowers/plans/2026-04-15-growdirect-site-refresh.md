---
classification: confidential
owner: GrowDirect LLC
---

# GrowDirect.io Site Package Refresh — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Consolidate all growdirect.io static site assets into a deployable `site/` directory with accurate content matching the April 2026 codebase state.

**Architecture:** Static HTML files organized in `site/` with shared CSS extracted for consistency. Files sourced from repo root, Brain raw inbox, and iCloud archive. Content updated to match current rule counts (37/10), Goose credit model, and honest built-vs-roadmap status. Manifesto V.3 rewritten.

**Tech Stack:** Static HTML/CSS, OpenAPI 3.0 YAML, Redoc CLI for API reference generation.

**Spec:** `docs/superpowers/specs/2026-04-15-growdirect-site-refresh-design.md`

---

## Chunk 1: Scaffold and File Migration

Create the directory structure and move/copy all source files to their final locations before any content editing. This establishes the working set.

### Task 1: Create `site/` Directory Structure

**Files:**
- Create: `site/`, `site/canary/`, `site/docs/`, `site/investor/`, `site/css/`, `site/legal/`

- [ ] **Step 1: Create directories**

```bash
mkdir -p ~/GrowDirect/site/{canary,docs,investor,css,legal}
```

- [ ] **Step 2: Verify structure**

```bash
find ~/GrowDirect/site -type d | sort
```

Expected:
```
site/
site/canary
site/css
site/docs
site/investor
site/legal
```

### Task 2: Move Repo Root Files to `site/`

**Files:**
- Move: `growdirect-hub.html` → `site/index.html`
- Move: `canary.growdirect.io.html` → `site/canary/index.html`

- [ ] **Step 1: Move hub**

```bash
mv ~/GrowDirect/growdirect-hub.html ~/GrowDirect/site/index.html
```

- [ ] **Step 2: Move canary site**

```bash
mv ~/GrowDirect/canary.growdirect.io.html ~/GrowDirect/site/canary/index.html
```

- [ ] **Step 3: Verify both files exist in new locations**

```bash
ls -la ~/GrowDirect/site/index.html ~/GrowDirect/site/canary/index.html
```

### Task 3: Move Technical Library to `site/docs/`

**Files:**
- Move: `Canary Technical Library/Canary Data Model.html` → `site/docs/canary-data-model.html`
- Move: `Canary Technical Library/Canary Platform Architecture.html` → `site/docs/canary-platform-architecture.html`
- Move: `Canary Technical Library/Canary Technical Roadshow.html` → `site/docs/canary-technical-roadshow.html`
- Move: `Canary Technical Library/Canary Factory Process.html` → `site/docs/canary-factory-process.html`
- Move: `Canary Technical Library/Canary elJeffe Protocol.html` → `site/docs/canary-eljeffe-protocol.html`

- [ ] **Step 1: Move all 5 docs (rename to kebab-case, no spaces)**

```bash
mv ~/GrowDirect/"Canary Technical Library/Canary Data Model.html" ~/GrowDirect/site/docs/canary-data-model.html
mv ~/GrowDirect/"Canary Technical Library/Canary Platform Architecture.html" ~/GrowDirect/site/docs/canary-platform-architecture.html
mv ~/GrowDirect/"Canary Technical Library/Canary Technical Roadshow.html" ~/GrowDirect/site/docs/canary-technical-roadshow.html
mv ~/GrowDirect/"Canary Technical Library/Canary Factory Process.html" ~/GrowDirect/site/docs/canary-factory-process.html
mv ~/GrowDirect/"Canary Technical Library/Canary elJeffe Protocol.html" ~/GrowDirect/site/docs/canary-eljeffe-protocol.html
```

- [ ] **Step 2: Move the shared CSS**

```bash
mv ~/GrowDirect/"Canary Technical Library/canary docs.css" ~/GrowDirect/site/css/canary-docs.css
```

- [ ] **Step 3: Remove empty directory**

```bash
rmdir ~/GrowDirect/"Canary Technical Library" 2>/dev/null || echo "Directory not empty — check for leftover files"
```

- [ ] **Step 4: Verify all docs landed**

```bash
ls -la ~/GrowDirect/site/docs/
```

Expected: 5 HTML files

### Task 4: Move Brain Inbox Files to `site/investor/`

**Files:**
- Move: `Brain/raw/inbox/growdirect_investor.html` → `site/investor/index.html`
- Move: `Brain/raw/inbox/02-eljeffe-v3.html` → `site/investor/eljeffe.html`

- [ ] **Step 1: Move investor briefing**

```bash
mv ~/GrowDirect/Brain/raw/inbox/growdirect_investor.html ~/GrowDirect/site/investor/index.html
```

- [ ] **Step 2: Move elJeffe orbital diagram**

```bash
mv ~/GrowDirect/Brain/raw/inbox/02-eljeffe-v3.html ~/GrowDirect/site/investor/eljeffe.html
```

- [ ] **Step 3: Verify**

```bash
ls -la ~/GrowDirect/site/investor/
```

### Task 5: Copy iCloud Archive Files to `site/docs/`

**Files:**
- Copy: iCloud `Product_Sites/Canary_LP_Magazine_Article.html` → `site/docs/canary-magazine-article.html`
- Copy: iCloud `Product_Sites/Canary_JSONB_Forensic_Analysis_v1.0.html` → `site/docs/canary-jsonb-forensic.html`
- Copy: iCloud `Product_Sites/Canary_CRDM_v2.0.html` → `site/docs/canary-crdm-mapping.html`
- Copy: iCloud `Product_Sites/Fox_Module_Technical_Specification_v1.0.html` → `site/docs/canary-fox-spec.html`
- Copy: iCloud `Jeremy_gLog_Swagger_v1.0.yaml` → `site/docs/eljeffe-swagger.yaml`

- [ ] **Step 1: Copy Product_Sites files**

```bash
ICLOUD="$HOME/Library/Mobile Documents/com~apple~CloudDocs/GrowDirect.archived"
cp "$ICLOUD/Canary_IP/Documents/Product_Sites/Canary_LP_Magazine_Article.html" ~/GrowDirect/site/docs/canary-magazine-article.html
cp "$ICLOUD/Canary_IP/Documents/Product_Sites/Canary_JSONB_Forensic_Analysis_v1.0.html" ~/GrowDirect/site/docs/canary-jsonb-forensic.html
cp "$ICLOUD/Canary_IP/Documents/Product_Sites/Canary_CRDM_v2.0.html" ~/GrowDirect/site/docs/canary-crdm-mapping.html
cp "$ICLOUD/Canary_IP/Documents/Product_Sites/Fox_Module_Technical_Specification_v1.0.html" ~/GrowDirect/site/docs/canary-fox-spec.html
```

- [ ] **Step 2: Copy Swagger YAML**

```bash
cp "$ICLOUD/_ALX/WorkOrders/output/Jeremy/Jeremy_gLog_Swagger_v1.0.yaml" ~/GrowDirect/site/docs/eljeffe-swagger.yaml
```

- [ ] **Step 3: Verify all files**

```bash
ls -la ~/GrowDirect/site/docs/
```

Expected: 10 HTML files + 1 YAML + 1 CSS

### Task 6: Copy Legal Files

**Files:**
- Copy: `docs/legal/terms-of-use.html` → `site/legal/terms.html`
- Copy: `docs/legal/privacy-policy.html` → `site/legal/privacy.html`
- Copy: `docs/legal/legal-disclaimer.html` → `site/legal/disclaimer.html`

- [ ] **Step 1: Copy legal files**

```bash
cp ~/GrowDirect/docs/legal/terms-of-use.html ~/GrowDirect/site/legal/terms.html
cp ~/GrowDirect/docs/legal/privacy-policy.html ~/GrowDirect/site/legal/privacy.html
cp ~/GrowDirect/docs/legal/legal-disclaimer.html ~/GrowDirect/site/legal/disclaimer.html
```

- [ ] **Step 2: Verify**

```bash
ls -la ~/GrowDirect/site/legal/
```

### Task 7: Clean Up Old Locations

- [ ] **Step 1: Archive loose root files**

```bash
mv ~/GrowDirect/knowledge-architecture.html ~/GrowDirect/docs/_archive/knowledge-architecture.html
```

- [ ] **Step 2: Commit the full scaffold**

```bash
cd ~/GrowDirect
git add site/
git add docs/_archive/knowledge-architecture.html
git commit -m "chore: scaffold site/ directory and migrate all source files

Move hub, canary site, Technical Library, investor assets, and legal
files into site/ directory structure. Copy iCloud archive sources
(magazine, JSONB forensic, CRDM, Fox spec, Swagger YAML). No content
changes yet — this is the file migration only."
```

---

## Chunk 2: Shared CSS Extraction

Extract common CSS patterns into `site/css/shared.css` before editing individual files, so all subsequent content updates can reference the shared stylesheet.

### Task 8: Create Shared CSS

**Files:**
- Create: `site/css/shared.css`
- Reference: `site/index.html` (source of CSS variables and patterns)

Read the existing inline `<style>` blocks in `site/index.html` and `site/canary/index.html` to extract shared patterns. The shared CSS should include:

- [ ] **Step 1: Read both site files to identify shared CSS patterns**

Read `site/index.html` lines 10-230 and `site/canary/index.html` lines 10-365 to identify the common CSS custom properties, nav, footer, gate, typography, and section patterns.

- [ ] **Step 2: Create `site/css/shared.css`**

Extract into `site/css/shared.css`:
- `:root` custom properties (color palette — use the Canary dark theme as canonical: `--ink`, `--card`, `--border`, `--canary`/`--btc`, `--text`, `--text2`, `--text3`, `--green`, `--blue`, `--red`)
- Reset (`*, *::before, *::after`, `html`, `body`, `a`)
- Grain overlay (`body::after`)
- Nav bar (`.nav-*` classes)
- Footer (`.site-footer`, `.footer-left`, `.footer-right`)
- Section structure (`.section`, `.section-label`, `.section-title`, `.section-intro`)
- Gate pattern (`.gate-*` classes, `#gated-content`)
- Typography families (Inter body, Space Grotesk headings, Space Mono mono)
- Doc nav for `site/docs/` pages (back-link bar)

Keep the shared CSS focused on structural patterns. Page-specific styles (hero, portfolio grid, pricing cards, pipeline diagram) stay inline in each file.

- [ ] **Step 3: Verify the file renders**

Open `site/css/shared.css` and confirm it's valid CSS with no syntax errors.

- [ ] **Step 4: Commit**

```bash
cd ~/GrowDirect
git add site/css/shared.css
git commit -m "feat(site): extract shared CSS variables and patterns"
```

---

## Chunk 3: Hub Content Updates (`site/index.html`)

Update all content in the main growdirect.io page.

### Task 9: Update Hub — Numbers and Goose Card

**Files:**
- Modify: `site/index.html`

- [ ] **Step 1: Update hero stat**

Find: `29` in the hero stats section (around line 1143-1144)
Replace the detection rules stat with `37`

- [ ] **Step 2: Update Chirp platform card**

Find the Detection Engine card (around line 1193-1196)
Replace "29 detection rules across 8 categories" with "37 detection rules across 10 categories"

- [ ] **Step 3: Rewrite Goose platform card**

Find the Bitcoin & Lightning card (around line 1203-1208). Replace the entire card content:
- Title: keep "Bitcoin & Lightning"
- Codename: keep "GOOSE"
- Badge: change from `Phase 2` to `Building`
- Description: "Sat-denominated credit system powered by the Strike Lightning API. Every metered operation — transaction processing, detection alerts, case management, AI analysis — draws from a single credit balance. Treasury-funded onboarding gives every merchant free credits at signup. Self-service refills via any Lightning wallet. Gold list alerts are always free. L402 macaroon tokens handle authentication. The billing infrastructure that makes the product self-sustaining without subscription tiers."

- [ ] **Step 4: Update pipeline diagram**

Find "29 rules · 3 tiers" in the pipeline section (around line 1239)
Replace with "37 rules · 3 tiers"

- [ ] **Step 5: Update Portfolio Canary card**

Find the Canary portfolio card (around line 1306-1347):
- Change "29 detection rules across 8 fraud categories" → "37 detection rules across 10 fraud categories" in the narrative
- Change the stat `29` → `37` for "Detection Rules"
- Remove the "536 Tests Passing" stat entirely (volatile)
- Change "Bitcoin-anchored audit trail via Ordinal inscription" → "INSERT-only evidence chain with SHA-256 hash linking and database-enforced immutability"

- [ ] **Step 6: Verify no remaining "29" references**

Search for any remaining `29` in the file that refers to rules. Also search for `536` and `8 categories`.

### Task 10: Update Hub — Gated Investor Section Links

**Files:**
- Modify: `site/index.html`

- [ ] **Step 1: Fix gated content card links**

Find the gated content section (around line 1508-1557). Update each card:

The Manifesto card (line ~1516): change `onclick="window.open('Brain/raw/inbox/growdirect_investor.html','_blank')"` to `onclick="window.open('investor/','_blank')"`

The elJeffe card (line ~1521): change `onclick="window.open('Brain/raw/inbox/02-eljeffe-v3.html','_blank')"` to `onclick="window.open('investor/eljeffe.html','_blank')"`

The CRDM card (line ~1536-1540): wrap in `<a>` tag linking to `docs/canary-data-model.html` (or add onclick)

The JSONB Forensic card (line ~1547-1550): wrap in `<a>` tag linking to `docs/canary-jsonb-forensic.html`

The Magazine Article card (line ~1552-1555): wrap in `<a>` tag linking to `docs/canary-magazine-article.html`

- [ ] **Step 2: Remove dead cards**

Remove these cards that have no backing files:
- "War Chest — Strategic Briefing" (no standalone file exists)
- "Component Business Model" (Dog, Bull, Heron, Hawk don't exist)
- "Patent Visualizations" (no standalone file exists)

- [ ] **Step 3: Add new cards**

Add cards for the newly included docs:
- **Fox Case Management** → `docs/canary-fox-spec.html` — "Structured incident reporting built to evidentiary standards. Evidence locker, case timeline, resolution tracking. INSERT-only with SHA-256 hash chain."
- **CRDM Schema Mapping** → `docs/canary-crdm-mapping.html` — "How Square webhook payloads map to the Canonical Retail Data Model. Field extraction, schema normalization, evidence-grade storage."
- **API Reference** → `docs/canary-api-reference.html` — "OpenAPI specification for the elJeffe notarization protocol. gLog queries, event validation, L402 payment gate. Roadmap — architecture spec, not live endpoints."

- [ ] **Step 4: Update the gate contents list**

Update the `<ul class="gate-contents">` list (around line 1488-1496) to match the actual cards now present.

- [ ] **Step 5: Commit**

```bash
cd ~/GrowDirect
git add site/index.html
git commit -m "feat(site): update hub content — numbers, Goose card, gated links

- 29→37 rules, 8→10 categories everywhere
- Rewrite Goose card: Strike credit system, not BTCPay subscriptions
- Fix gated section: real links to investor/ and docs/
- Remove dead cards (War Chest, CBM, Patent Viz)
- Add Fox, CRDM Mapping, API Reference cards
- Remove volatile '536 tests' stat"
```

---

## Chunk 4: Canary Site Content Updates (`site/canary/index.html`)

### Task 11: Update Canary Site — Numbers

**Files:**
- Modify: `site/canary/index.html`

- [ ] **Step 1: Update detection section**

Find the detection section (around line 1098-1101). Update:
- "29 Rules. 8 Categories. 3 Tiers." → "37 Rules. 10 Categories. 3 Tiers."
- Update the section intro to mention the 10 categories

- [ ] **Step 2: Update rule catalog table**

Find the gated rules table (around line 1356-1382). This table currently shows 12 rules. Update it to include all 37 rules across 10 categories. The categories are:

1. Fraud (Post-Void, Refund-to-Different-Card is REMOVED — doesn't exist in code)
2. Employee (Off-Clock Activity)
3. Timing (After-Hours Activity)
4. Refund (High Refund Velocity, Large Refund)
5. Velocity (Rapid Refund Sequence)
6. Pricing (Excessive Discount)
7. Register (No-Sale Abuse, Untendered Order)
8. Card (Manual Entry Spike)
9. Evasion (Split Transaction)
10. Gift Card (Gift Card Load Velocity, Gift Card Drain)
11. Dispute (Dispute Created, Dispute Lost, Dispute Velocity)
12. Invoice (Invoice Overdue, Invoice Charge Failed, High-Value Unpaid Invoice)
13. Loyalty (Point Accumulation, Bulk Redemption, Cross-Location, Enrollment Fraud)
14. Composite (SRA Threshold Breach)

**To get the exact list:** Read `Canary/canary/chirp/rule_definitions.py` and extract all rule names, categories, triggers, default severities, and tiers. Build the table from the actual code.

- [ ] **Step 3: Verify no remaining "29" or "8 categories"**

Search the file for stale numbers.

### Task 12: Rewrite Canary Site — Pricing Section

**Files:**
- Modify: `site/canary/index.html`

- [ ] **Step 1: Replace the pricing section**

Find the pricing section (around lines 1246-1294). Replace the three-tier cards (Starter $49 / Professional $99 / Enterprise $199) with content describing the Goose credit model:

Section title: "Start Free. Pay As You Grow."
Section intro: "Connect your Square account and start receiving alerts immediately. GrowDirect funds your account with free credits at signup. Gold list alerts — the ones that catch real theft — are always free. Premium features like case management and deep analysis draw from your credit balance. Top up anytime from any Lightning wallet."

Content should cover:
- **Free onboarding** — treasury-funded credits, no credit card required
- **Gold list alerts always free** — Post-Void, Off-Clock, Untendered Order — the hooks
- **Usage-based** — premium features (Fox cases, Owl analysis, health checks) metered by credits
- **Easy refills** — scan a QR with Cash App, Strike, or any Lightning wallet
- **No tiers, no contracts** — one account, one balance, pay for what you use
- **Soft degradation** — if credits run low, alerts keep flowing; premium features pause until you top up

Do NOT include specific sat amounts or dollar prices (these are tunable and not finalized).

Do NOT push Bitcoin/Lightning as a feature — frame refills as "add credits" with Lightning as the mechanism, not the selling point.

- [ ] **Step 2: Commit**

```bash
cd ~/GrowDirect
git add site/canary/index.html
git commit -m "feat(site): update canary site — 37 rules, full catalog, credit pricing

- Update detection section: 37 rules, 10 categories
- Replace 3-tier pricing fiction with Goose credit model
- Expand rule catalog table to all 37 rules from rule_definitions.py
- Remove Refund-to-Different-Card (doesn't exist in code)"
```

---

## Chunk 5: Technical Library Doc Updates (`site/docs/`)

Each doc needs: (a) internal link updates (paths changed), (b) number corrections, (c) content accuracy updates. These tasks can be parallelized — each doc is independent.

### Task 13: Update `canary-data-model.html`

**Files:**
- Modify: `site/docs/canary-data-model.html`

- [ ] **Step 1: Update internal nav links**

Update any `href` or `onclick` links pointing to old paths:
- `../canary.growdirect.io.html` → `../canary/`
- `Canary Technical Library/` references → `./` (same directory)
- Any `canary docs.css` reference → `../css/canary-docs.css`

- [ ] **Step 2: Update rule counts if mentioned**

Search for "26" or "29" rule references. Update to 37.

- [ ] **Step 3: Add `<link>` to shared CSS**

Add `<link rel="stylesheet" href="../css/shared.css">` in the `<head>` if not already present. Keep page-specific styles inline.

### Task 14: Update `canary-platform-architecture.html`

**Files:**
- Modify: `site/docs/canary-platform-architecture.html`

- [ ] **Step 1: Update internal nav links** (same pattern as Task 13)
- [ ] **Step 2: Update rule counts** (same pattern)
- [ ] **Step 3: Add shared CSS link**

### Task 15: Update `canary-technical-roadshow.html`

**Files:**
- Modify: `site/docs/canary-technical-roadshow.html`

- [ ] **Step 1: Update internal nav links**
- [ ] **Step 2: Update rule counts** — 26/29 → 37
- [ ] **Step 3: Mark L402 as roadmap**

Find any section describing L402 validation gate as live/current. Add a clear status marker: "(Roadmap — architecture designed, implementation planned for Sprint 7+)"

- [ ] **Step 4: Add shared CSS link**

### Task 16: Update `canary-factory-process.html`

**Files:**
- Modify: `site/docs/canary-factory-process.html`

- [ ] **Step 1: Update internal nav links**
- [ ] **Step 2: Add shared CSS link**

Content is accurate — no other changes needed.

### Task 17: Rewrite `canary-eljeffe-protocol.html`

**Files:**
- Modify: `site/docs/canary-eljeffe-protocol.html`

This is the biggest content change in the Technical Library.

- [ ] **Step 1: Update internal nav links and add shared CSS**

- [ ] **Step 2: Reposition the document**

The current framing pushes elJeffe as a revenue engine and selling point. Reframe as a technical architecture reference:

**What's built (mark as "Live"):**
- `evidence_records` table with INSERT-only enforcement and database triggers
- SHA-256 hash chain linking every record to its predecessor
- `inscription_pool` table with `bitcoin_txid` and `bitcoin_block` columns
- Merkle tree batching schema
- Three-schema architecture (app, sales, metrics) with immutability at the PostgreSQL level

**What's designed but not implemented (mark as "Roadmap"):**
- Genesis Pool minting via OrdinalsBot API
- Merchant self-minting and treasury systems
- L402 validation gate (Strike + macaroons — designed in Goose spec)
- Perpetual royalty revenue from validation requests
- Self-custody evaluation
- Avalanche private subnet (status: under review — may be dropped)

- [ ] **Step 3: Remove or qualify aspirational claims**

Remove or clearly label claims like:
- "10 million ordinal inscriptions as Genesis Pool"
- "Merchants build their own treasuries and mint Ordinals"
- "Treasury earns revenue perpetually via L402"

Replace with honest descriptions of the infrastructure that exists and the design that's planned.

- [ ] **Step 4: Frame Bitcoin as infrastructure, not feature**

The narrative should be: "We use Bitcoin's proof-of-work as an immutability anchor for evidence records. This is infrastructure — the merchant never sees it. They see tamper-proof records. The Bitcoin layer is why those records are trustworthy."

### Task 18: Update `canary-magazine-article.html`

**Files:**
- Modify: `site/docs/canary-magazine-article.html`

- [ ] **Step 1: Update numbers**

Search for "26" and "29" (rules) and "8" (categories). Update to 37 and 10.

- [ ] **Step 2: Update internal nav**

Add consistent nav bar: "← Canary" link to `../canary/`, "GrowDirect" link to `../`

- [ ] **Step 3: Add shared CSS link** (if compatible with existing styles)

### Task 19: Update `canary-jsonb-forensic.html`

**Files:**
- Modify: `site/docs/canary-jsonb-forensic.html`
- Reference: `Canary/canary/chirp/rule_definitions.py` (for current rule list)

- [ ] **Step 1: Add nav and shared CSS link**

- [ ] **Step 2: Update for new rule categories**

Read `Canary/canary/chirp/rule_definitions.py` to identify all field mappings for the new categories: Gift Card, Dispute, Invoice, Loyalty, Composite. Add JSONB field extraction mappings for these categories if the document covers per-rule field analysis.

- [ ] **Step 3: Update rule count references**

### Task 20: Update `canary-crdm-mapping.html`

**Files:**
- Modify: `site/docs/canary-crdm-mapping.html`
- Reference: `Canary/canary/models/` (for current schema)

- [ ] **Step 1: Add nav and shared CSS link**

- [ ] **Step 2: Check schema against current models**

Read `Canary/canary/models/app/` and `Canary/canary/models/sales/` to verify the CRDM mapping matches current tables. Note any new tables added since February 2026.

- [ ] **Step 3: Add Goose tables if appropriate**

If the document covers the full schema, add the Goose tables: `merchant_wallets`, `wallet_transactions`, `gas_schedule`, `macaroon_tokens`, `strike_invoices`. Reference the Goose spec for column details.

### Task 21: Update `canary-fox-spec.html`

**Files:**
- Modify: `site/docs/canary-fox-spec.html`
- Reference: `Canary/canary/fox/` (for current code)

- [ ] **Step 1: Add nav and shared CSS link**

- [ ] **Step 2: Check against current Fox code**

Read `Canary/canary/fox/` (models, routes, services) and verify the spec matches what's implemented. Update any stale specifics (field names, routes, behavior).

### Task 22: Update Swagger YAML and Generate Redoc

**Files:**
- Modify: `site/docs/eljeffe-swagger.yaml`
- Create: `site/docs/canary-api-reference.html`

- [ ] **Step 1: Update Swagger metadata**

In `site/docs/eljeffe-swagger.yaml`:
- Add to description: "Note: This is an architecture specification. These endpoints are not yet live. See the elJeffe Protocol document for implementation status."
- Update server URL from `https://jeffe.io` to `https://api.growdirect.io` (or remove if no live server)
- Update contact URL from `https://jeffe.io` to `https://growdirect.io`

- [ ] **Step 2: Generate Redoc HTML**

```bash
cd ~/GrowDirect
npx @redocly/cli build-docs site/docs/eljeffe-swagger.yaml -o site/docs/canary-api-reference.html
```

If `@redocly/cli` is not available, install it:
```bash
npx @redocly/cli build-docs site/docs/eljeffe-swagger.yaml -o site/docs/canary-api-reference.html
```

- [ ] **Step 3: Verify the generated HTML opens correctly**

Open `site/docs/canary-api-reference.html` in a browser and confirm it renders the API spec.

### Task 23: Commit All Doc Updates

- [ ] **Step 1: Commit Technical Library updates**

```bash
cd ~/GrowDirect
git add site/docs/ site/css/
git commit -m "feat(site): update all Technical Library docs — numbers, links, content

- All docs: 37 rules, 10 categories, nav links fixed
- elJeffe protocol: rewritten as infrastructure reference, built vs roadmap
- JSONB forensic: new rule categories added
- CRDM mapping: checked against current schema
- Fox spec: checked against current code
- Swagger: metadata updated, Redoc HTML generated
- Magazine article: number pass
- All docs: consistent nav (← Canary, GrowDirect) and shared CSS"
```

---

## Chunk 6: Investor Assets and Canary Doc Links

### Task 24: Update Investor Briefing (`site/investor/index.html`)

**Files:**
- Modify: `site/investor/index.html`

- [ ] **Step 1: Update rule counts**

Search for "26" and "29" references to detection rules. Update to 37.

- [ ] **Step 2: Update any internal links**

Fix any links that pointed to Brain paths or other old locations.

- [ ] **Step 3: Verify the password gate still works**

The file has a JS gate. Confirm the unlock code is `eljeffe2026` and the gate JS functions correctly after the file move.

### Task 25: Update Canary Site Gated Section Links

**Files:**
- Modify: `site/canary/index.html`

- [ ] **Step 1: Fix doc card links**

The gated section doc cards (around line 1328-1353) currently link to `Canary Technical Library/*.html`. Update all links:
- `Canary Technical Library/Canary Data Model.html` → `../docs/canary-data-model.html`
- `Canary Technical Library/Canary Platform Architecture.html` → `../docs/canary-platform-architecture.html`
- `Canary Technical Library/Canary Technical Roadshow.html` → `../docs/canary-technical-roadshow.html`
- `Canary Technical Library/Canary Factory Process.html` → `../docs/canary-factory-process.html`
- `Canary Technical Library/Canary elJeffe Protocol.html` → `../docs/canary-eljeffe-protocol.html`

- [ ] **Step 2: Add cards for new docs**

Add doc cards for:
- Magazine Article → `../docs/canary-magazine-article.html`
- JSONB Forensic → `../docs/canary-jsonb-forensic.html`
- Fox Case Management → `../docs/canary-fox-spec.html`
- API Reference → `../docs/canary-api-reference.html`

- [ ] **Step 3: Update footer link**

Change `growdirect-hub.html` → `../` in the footer.

- [ ] **Step 4: Commit**

```bash
cd ~/GrowDirect
git add site/canary/index.html site/investor/
git commit -m "feat(site): fix canary doc links and update investor assets

- Canary gated section: all links point to ../docs/
- Added cards for magazine, JSONB forensic, Fox spec, API reference
- Investor briefing: updated rule counts, fixed internal links
- Footer: updated cross-site nav links"
```

---

## Chunk 7: Manifesto V.3 Rewrite

### Task 26: Rewrite Manifesto Section V.3

**Files:**
- Modify: `Brain/raw/inbox/GrowDirect_Manifesto_v1.2.md`
- Reference: `docs/superpowers/specs/2026-04-15-canary-account-credit-system-design.md`

- [ ] **Step 1: Read current V.3 section**

Read `Brain/raw/inbox/GrowDirect_Manifesto_v1.2.md` lines 699-738 (Section V.3 — The Subscription Model).

- [ ] **Step 2: Rewrite V.3 to describe Goose credit system**

Replace the Basic/Treasury/Full Node tier descriptions with:

**Title:** "V.3 — The Credit Model"

Content should describe:
- Sat-denominated credit wallets (custodial, GrowDirect holds keys)
- Treasury-funded onboarding (100,000 sats default per merchant)
- Tunable gas schedule — every metered operation has a sat cost
- Three meter categories: transactions processed, detection events, compute
- Gold list alerts always free (the hook)
- Soft degradation on credit exhaustion (dashboard stays, premium gates)
- Self-service Lightning refills via Strike API
- L402 macaroon authentication/authorization
- Break-even recalculated: at N merchants with average daily operations of X, gas revenue covers infrastructure at Y sats/month

- [ ] **Step 3: Update other stale sections**

In the same file, update:
- III.1: "26 detection rules across 8 categories" → "37 detection rules across 10 categories" (line ~190)
- III.3: "Twenty-six rules across eight categories" → "Thirty-seven rules across ten categories" (line ~228)
- V.4 Protocol Pipe Mermaid: "26 Chirp rules" → "37 Chirp rules" (line ~786)

- [ ] **Step 4: Update Appendix C status map**

Read current Appendix C (lines 1870-1927). Update to reflect April 2026 state:

**LIVE TODAY:** Square OAuth, webhook HMAC verification, TSP pipeline (4 stream consumers, 37 rules), evidence seal layer, Chirp detection across 10 categories, Fox case management, Owl AI analysis, dashboard, alert pipeline, risk scoring

**BUILDING NOW:** Goose credit system (merchant wallets, gas schedule, Strike integration, L402 macaroons, treasury funding)

**DESIGNED (ROADMAP):** OrdinalsBot inscription bridge, L402 validation gate (public API), Genesis Pool minting

**FUTURE ARCHITECTURE:** DAO governance, Kubernetes auto-purchase, cross-vertical expansion, heartbeat network

- [ ] **Step 5: Commit**

```bash
cd ~/GrowDirect
git add "Brain/raw/inbox/GrowDirect_Manifesto_v1.2.md"
git commit -m "docs: update manifesto V.3 to Goose credit model, refresh numbers

- V.3: replace Basic/Treasury/Full Node tiers with credit system
- III.1, III.3, V.4: 26→37 rules, 8→10 categories
- Appendix C: update status map to April 2026 state
- Reflects Goose spec (account-credit-system-design)"
```

---

## Chunk 8: Final Verification and Cleanup

### Task 27: Cross-Link Verification

- [ ] **Step 1: Verify all links resolve**

```bash
cd ~/GrowDirect/site
# Check that every href/onclick target exists as a file
grep -roh 'href="[^"]*"' *.html canary/*.html docs/*.html investor/*.html | \
  sort -u | \
  sed 's/href="//;s/"//' | \
  grep -v '^#' | grep -v '^http' | grep -v '^mailto' | \
  while read f; do
    # Resolve relative paths
    test -f "$f" || echo "BROKEN: $f"
  done
```

Fix any broken links found.

- [ ] **Step 2: Verify no old paths remain**

```bash
grep -r "Canary Technical Library" ~/GrowDirect/site/ || echo "Clean"
grep -r "Brain/raw/inbox" ~/GrowDirect/site/ || echo "Clean"
grep -r "growdirect-hub.html" ~/GrowDirect/site/ || echo "Clean"
grep -r "canary.growdirect.io.html" ~/GrowDirect/site/ || echo "Clean"
```

All should return "Clean". Fix any remaining old path references.

- [ ] **Step 3: Verify no stale numbers remain**

```bash
# Search for "29 detection" or "29 rules" or "26 rules" or "8 categories"
grep -rn "29 detection\|29 rules\|26 rules\|26 detection\|8 categories\|536 test" ~/GrowDirect/site/ || echo "Clean"
```

### Task 28: Full Package Inventory

- [ ] **Step 1: List final package contents**

```bash
find ~/GrowDirect/site -type f | sort
```

Verify the complete set matches the spec:
- `site/index.html`
- `site/canary/index.html`
- `site/css/shared.css`
- `site/css/canary-docs.css`
- `site/docs/canary-data-model.html`
- `site/docs/canary-platform-architecture.html`
- `site/docs/canary-technical-roadshow.html`
- `site/docs/canary-factory-process.html`
- `site/docs/canary-eljeffe-protocol.html`
- `site/docs/canary-magazine-article.html`
- `site/docs/canary-jsonb-forensic.html`
- `site/docs/canary-crdm-mapping.html`
- `site/docs/canary-fox-spec.html`
- `site/docs/canary-api-reference.html`
- `site/docs/eljeffe-swagger.yaml`
- `site/investor/index.html`
- `site/investor/eljeffe.html`
- `site/legal/terms.html`
- `site/legal/privacy.html`
- `site/legal/disclaimer.html`

Total: 20 files

- [ ] **Step 2: Final commit**

```bash
cd ~/GrowDirect
git add site/
git commit -m "feat(site): complete growdirect.io site package refresh

20-file deployable package in site/:
- Hub: updated numbers, Goose credit card, fixed investor links
- Canary: 37-rule catalog, credit pricing, doc links
- 11 technical docs: consistent nav, accurate content, shared CSS
- Investor briefing + elJeffe orbital diagram
- API reference generated from OpenAPI spec
- Legal pages
- Manifesto V.3 updated to Goose credit model

All content verified against April 2026 codebase state."
```
