---
classification: HIDE-scope
type: design-briefs
date: 2026-04-26
audience: Claude Design (web app) — paste each brief directly
purpose: visual artifact production for Bart Monday 1pm PST call (2026-04-27) and downstream Canary asset library
constraints:
  - Hero Bird is locked (canary-icon-512.png) — never generate a replacement
  - Direct + serious + tangible voice — no AI-shimmer, no corny garden-center clichés, no hype
  - Match existing Canary brand identity (find Hero Bird in Canary/ repo for reference)
  - No emoji
---

# Claude Design Briefs — Monday Bart Call + Canary Asset Library

## How to use

Each brief below is paste-ready for Claude Design. Order by priority:

1. **Brief 1** — run first, today. Live constraint: Bart 1pm PST Monday 2026-04-27.
2. **Briefs 2-4** — queued. Run when bandwidth allows; each compounds in value as the asset library grows.

When pasting into Claude Design, also attach the Hero Bird logo file (`canary-icon-512.png` — find in `Canary/` repo, likely under `Canary/canary/static/img/` or similar). Brief 1 references it explicitly; Briefs 2-4 should match its visual register.

---

## Brief 1 — Bart-call leave-behind one-pager (RUN FIRST)

**Purpose:** A single 8.5×11 PDF Bart can hand to the L&G chain prospect, or use himself in a follow-up email. Visualizes Canary's canonical positioning. Read in 30 seconds; prompt one good question.

**Prompt for Claude Design:**

> Design a one-page (8.5×11 portrait, print-ready PDF) leave-behind document titled "Canary on NCR Counterpoint — operating platform for specialty retail." The Hero Bird logo (attached) goes top-left. The page is divided into three horizontal bands of equal weight, each labeled with a single word in a strong sans-serif: WHAT, WHO, HOW.
>
> **WHAT band:** "Multi-store merchandising and store operations for SMB retail running NCR Counterpoint." Below, a thin row of 13 small monogram tiles (one per Canary spine module — letters T R N A Q C D F J S P L W). Below the tiles, one line: "Thirteen modules. One spine. Counterpoint as the source of truth, Canary as the operating layer."
>
> **WHO band:** "Delivered through Rapid POS — the VAR partner who already knows your install." Below, three short labeled callouts in a row: "Counterpoint expertise" / "On-site delivery" / "Long-term partnership."
>
> **HOW band:** "CATz method — Counterpoint Architecture & Transformation. Two-phase engagement: Assess and design first, select and implement second. No vaporware, no rip-and-replace."
>
> **Footer band (small):** Three labeled metrics in a row — "Phase 1 ships in 60 days · 10 of 13 modules covered by Counterpoint substrate · 24 detection rules calibrated for L&G operating reality."
>
> **Visual treatment:** Clean, serious, IBM-Big-Four register. No stock photography. No emoji. No gradients. Tight typographic hierarchy. Single accent color picked from the Hero Bird palette (likely a warm yellow). Black text on warm off-white, accent yellow used sparingly. Print-safe margins.
>
> **Tone:** "We have a real product, real method, real partner channel" — confident, factual, declarative. No marketing copy. Treat this like a McKinsey one-pager, not a startup landing page.

**Where it goes after generation:** save as `Brain/raw/inbox/bart-monday-leave-behind.pdf` (HIDE-scope; not committed). Bart receives via email or in-person hand-off Monday.

---

## Brief 2 — Sell / Plan / Move / Buy L1 quadrant visual

**Purpose:** Replaces what we'd otherwise render as a mermaid diagram. Becomes the single image that explains Canary in 30 seconds — usable in slides, the L&G playbook, future pitch decks, partner onboarding.

**Prompt for Claude Design:**

> Design a 16:9 landscape diagram titled "Canary value chain — the four operating quadrants of specialty retail." Below the title, a single descriptor line: "Mapped to the Canary 13-module spine."
>
> The main visual is a 2×2 grid of four equal quadrants:
>
> - **Top-left: SELL** — "POS transactions, returns, voids, exceptions." Below, a row of monograms: T A Q F.
> - **Top-right: PLAN** — "Assortment, pricing, OTB, promotions." Below: S P C.
> - **Bottom-left: MOVE** — "Inventory transfers, receiving, fulfillment, shrink." Below: D J L F.
> - **Bottom-right: BUY** — "Supplier, PO, receiving, cost updates." Below: C J F.
>
> Around the four quadrants, a thin border band labeled "cross-cutting" containing three more monograms with single-word labels: N (Where) · W (Who) · R (Audit).
>
> The Hero Bird logo (attached) sits in the top-right corner of the title bar, small.
>
> **Visual treatment:** Same register as Brief 1 — clean, serious, typographic. Each quadrant has a single accent color (consider four muted complementary tones — not bright). Monograms are ALL CAPS, monospace or strong geometric sans, in small filled circles or squares. No icons, no illustrations, no decoration. The diagram should look like it could appear in an IBM Architecture Options document.
>
> **Tone:** Frame, not infographic. The reader should be able to point at any quadrant and ask a real question.

**Where it goes:** `Brain/raw/inbox/canary-l1-quadrant.pdf` + `.png` (HIDE-scope until reviewed; can promote to `Brain/wiki/` assets afterward).

---

## Brief 3 — 13-module spine monogram icon set

**Purpose:** Build-once-reuse-forever. Every L2 swimlane diagram, every dashboard mockup, every slide that references the spine uses the same iconography. Pays compounding interest across every subsequent visual artifact.

**Prompt for Claude Design:**

> Design a sheet of 13 module-monogram icons for the Canary retail spine. Each icon is a single uppercase letter inside a filled geometric mark, sized 256×256px PNG with transparent background, plus an SVG version. The 13 letters and their module names:
>
> - **T** — Transactions
> - **R** — Customer (Relationship)
> - **N** — Device (places)
> - **A** — Asset Management
> - **Q** — Loss Prevention (Quality)
> - **C** — Commercial
> - **D** — Distribution
> - **F** — Finance
> - **J** — Forecast / Order
> - **S** — Space, Range, Display
> - **P** — Pricing / Promotion
> - **L** — Labor / Workforce
> - **W** — Work Execution
>
> **Treatment:** All 13 share the same geometric container (filled circle is the safest default), the same typeface (strong geometric sans, ALL CAPS, single letter centered). Differentiation between modules is by **color only** — pick a distinct hue for each from a coherent 13-color palette that reads as one set, not a rainbow. Avoid pure red and pure green (color-blindness). The Hero Bird's accent yellow should be reserved as a meta-color (used to highlight the active module in interfaces, not assigned to a specific module).
>
> Below the icon grid on the same sheet, render a one-line key: "Letter-coded modules. Color is identity; letter is universal."
>
> **Deliverables:** one combined sheet (PDF), and individual files per module (256×256 PNG + SVG, named `module-T.png`, `module-T.svg`, etc.).

**Where it goes:** `Canary/canary/static/img/modules/` (when promoted) — these become real product assets.

---

## Brief 4 — Canary product UI mockups (low-fidelity, exploratory)

**Purpose:** Pre-build mockups of three Canary surfaces. Useful for partner conversations, recruiting, and locking design intent before engineering ships. Lower priority than 1-3 because it's not externally constrained by Monday — but high cumulative value.

**Prompt for Claude Design:**

> Generate three 16:9 desktop UI mockups for Canary, each a separate frame. Treat as low-fidelity wireframes with brand color applied — not pixel-perfect production designs. Use the Hero Bird logo (attached) in the top-left of each frame's chrome. Same typographic register as Briefs 1-3.
>
> **Mockup A — Owl conversational interface.** A two-pane layout. Left pane (narrow, ~25%): a list of recent agent conversations with timestamps and one-line summaries. Right pane (wide, ~75%): an active conversation thread between the user and "Owl" (Canary's analytical agent). Conversation shows the user asking "show me last week's voids over $50 by store" and Owl responding with a compact bar chart inline plus a paragraph of analysis. Below the chart, three small follow-up prompt suggestions as clickable chips.
>
> **Mockup B — Loss-prevention alert console.** A three-pane layout. Top bar: store filter, date range, severity filter. Left pane (narrow): list of active alerts grouped by Q-rule (e.g., "Q-DM-01 · Discount-cap exceeded · 7 today"). Center pane (wide): selected alert detail — transaction summary, the rule that fired, the employee, store, time, and a "Mark as resolved / Send to investigation" action row. Right pane (narrow): "Related alerts" — same employee, same rule, same store across the past 30 days.
>
> **Mockup C — Multi-store rebalance dashboard.** A map-and-grid layout. Map pane (top, ~40%): pinpoints for the chain's stores with color-coded inventory health indicators. Grid pane (bottom, ~60%): a transfer-flow matrix — rows are source stores, columns are destination stores, cells show pending transfer count and total value. One row highlighted as "selected"; below the matrix, a transfer detail strip showing line items.
>
> **Treatment:** Each mockup is annotated with thin callout lines pointing to key elements with one-word labels (no marketing copy). The visual register stays serious — this is what an L&G ops director sees, not what the marketing site shows. Use real-looking data (numbers, store names like "Store 03 · Northgate"); avoid Lorem Ipsum.

**Where it goes:** `Brain/raw/inbox/canary-ui-mockups/` initially (HIDE-scope); promote to `docs/design/` if reviewed and kept.

---

## Notes on running these

- Pasting the brief verbatim is fine — Claude Design will ask for the Hero Bird attachment when needed.
- If a generation comes back too marketing-y or too AI-shimmer, push back with: "Strip all decoration. Make this look like an IBM Architecture Options document, not a startup landing page."
- Save outputs to the paths noted above so they're discoverable for the next session that needs them.
- If anything generated includes a real client name (Boutique H&G chain, named landscaper accounts, etc.), regenerate with abstracted placeholders — per memory `feedback_scrub_client_names.md`, synthesis-layer artifacts use NFR deployment archetypes, not named clients.
