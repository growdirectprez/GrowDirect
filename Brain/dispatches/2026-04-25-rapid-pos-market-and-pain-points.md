---
type: dispatch
status: ready-for-execution
date: 2026-04-25
target: laptop-side Claude Code (background agent)
priority: medium
unblocks: Canary positioning for SMB specialty retailers on Counterpoint; Bart Monday call prep selling material; Module L/W native-build product strategy
inputs:
  - Public web (forums, Reddit, review platforms, trade publications, government / association data)
  - Existing wikis at Brain/wiki/ncr-counterpoint-* (anchor for what's already known)
tags: [research, market-analysis, rapid-pos, counterpoint, garden-center, pain-points, tam]
---

# Dispatch — Rapid POS / NCR Counterpoint user pain points + market research / TAM

Two-objective research dispatch. Public sources only. Outputs are synthesis wikis the engagement planner + GTM use; no Canary code modification.

## Operational discipline

Executes on the laptop as a background agent. Read-only on existing files; web research via WebSearch + WebFetch. No git commits — founder reviews the output wikis and commits.

## Objective A — User pain points + FAQs

Build a pain-point map from public-community discussion of Rapid POS, Rapid Garden POS, and NCR Counterpoint deployments. Target sources:

- Reddit subs likely to discuss SMB POS: r/retail, r/smallbusiness, r/POS, r/Cashier, r/garden, r/gardening, r/landscaping (light coverage expected), r/Aquariums (specialty retail discussion), r/sysadmin (when Counterpoint deployment issues surface)
- Review platforms: Capterra, G2, Software Advice, GetApp, Trustpilot — search "NCR Counterpoint" + "Rapid Garden POS" + "Rapid POS"
- NCR / Counterpoint community forums (if public — many vendor forums require login)
- Vendor blogs that respond to user questions: AMS Retail blog, RCS blog, Mariner Business Solutions blog, Counterpoint University, POS Highway, Nationwide Payment Systems blog
- Trade publications with comment sections / reader Q&A: Garden Center Magazine, Nursery Management, IGC Magazine, Greenhouse Grower
- YouTube comment sections on Counterpoint / Rapid POS demo videos (often surface real complaints)

Synthesize into recurring themes:
- Top 5 most frequently surfaced pain points
- Top 5 most frequently asked questions
- Identified gaps in current platform that Canary could fill (cross-reference Module L / W native-build opportunity per memory `project_canary_native_labor_module_opportunity.md`)
- Workarounds users have built (sometimes the gap is bigger than the official feature list suggests)
- Quotes (sanitized — no user-identifying detail) for selling material

## Objective B — Market research / TAM

Quantify the addressable market for "Counterpoint-running SMB specialty retailer interested in a back-office analytics + LP layer." Target sources:

- AmericanHort — green-industry size data (number of garden centers, average revenue, employment)
- NRF research — small-business retail data
- IBISWorld — industry reports (often paywalled; gather what's free)
- Statista — POS market sizing, garden-center sizing
- NCR Voyix investor materials (NCR Voyix is public — 10-K, investor presentations)
- Rapid POS press releases / website claims about customer count
- Trade publications' annual "state of the industry" reports
- US Census Bureau retail trade data (NAICS codes for nurseries/garden centers, gun stores, specialty food, wine, feed-and-tack)
- Software market sizes for adjacent categories (workforce management TAM as proxy for Module L native-build opportunity sizing)

Synthesize into:
- TAM estimate: # of US garden centers running Counterpoint (with confidence interval + source notes)
- TAM estimate: # of US specialty retailers running Counterpoint across all VAR-served verticals (garden, gun, food, wine, feed-and-tack)
- Revenue per store (median + range)
- Adjacent-vertical sizing (gun stores, specialty food, etc.) for Phase 6+ horizontal-expansion view
- Competitive landscape: Counterpoint vs alternatives (Lightspeed, Shopify POS, Square for Retail, Clover, etc.) — relative SMB market share where data exists
- Module L / W external-vendor TAM: Homebase + Deputy + When I Work etc. customer counts in retail SMB (sanity-check Canary native-build opportunity sizing)
- "Why customers leave Counterpoint" — pain that drives churn (informs displacement opportunity vs ride-along positioning)

## Sources of caution

Public web research surfaces conflicting numbers. Per `feedback_no_hype_copy` (direct, serious, tangible), every quantitative claim in the output must:

- Cite a specific source with link
- Note confidence (high — multiple corroborating sources / medium — single reputable source / low — extrapolated or single weak source)
- Flag where numbers conflict and which to trust

Per `feedback_iterate_with_what_you_have`, do NOT pause to ask for better sources. Grind through what's public; mark gaps as gaps in the output rather than blocking.

## Outputs

Two synthesis wiki articles in `Brain/wiki/`:

### 1. `Brain/wiki/rapid-pos-counterpoint-user-pain-points.md`

Sections:
- Executive summary (one paragraph — top pains + top opportunities)
- Methodology (sources scanned, # of distinct discussions reviewed, time range)
- Top pain points (5–10, ranked by frequency × severity)
- Top FAQs (5–10, with the answers users converge on — including "the official answer doesn't work, here's what people actually do")
- Gap-to-opportunity mapping (for each pain, which Canary module / capability could resolve it)
- Sanitized user quotes (~5–10, attribution scrubbed but with platform of origin)
- Open questions (what wasn't answerable from public sources alone)

### 2. `Brain/wiki/rapid-pos-counterpoint-market-research-tam.md`

Sections:
- Executive summary (TAM headline number with confidence + key competitive positioning)
- Methodology (sources, dates, confidence framework)
- TAM estimate — primary (US garden centers on Counterpoint)
- TAM estimate — extended (all SMB verticals served by Counterpoint VARs)
- Revenue-per-store ranges
- Competitive landscape (Counterpoint vs alternatives, with rough share where data permits)
- Module L / W external-vendor adjacent TAM (Homebase / Deputy / When I Work / Beekeeper / YOOBIC etc.)
- Churn drivers ("why customers leave Counterpoint")
- Source-quality table (every quantitative claim → source link → confidence)
- Open questions / data gaps

Both articles use the standard frontmatter:

```yaml
---
classification: internal
type: wiki
date: 2026-04-25
last-compiled: 2026-04-25
needs-review: 2026-05-09
source: public-web research; methodology section in body
---
```

## Brand voice (every output)

- Direct, serious, tangible. No hype copy. No sales-pitch language.
- Evidence-first. Every claim sourced or marked "no source found, inference only."
- Numbers always with context (range / confidence / source date).
- Customer-respecting. If a pain is identified, frame it as a real-world challenge people are working through — not "users hate X."

## Scrub rules

- No naming a specific user / retailer / business in the output. If a quote ties to a specific retailer, abstract.
- Per `feedback_scrub_client_names`, abstract named retailers into archetypes (e.g., "a Midwest garden center" → "a regional specialty retailer").
- No proprietary information / leaked screenshots / paywalled content reproduced verbatim. Cite + summarize, never copy.
- No personally identifying user info from forum discussions.

## Acceptance criteria

- Both wiki articles produced at the specified paths
- Each article has the standard frontmatter
- Top pain points + top FAQs grounded in citable public sources
- TAM headline number with explicit confidence + source notes
- Source-quality table for every quantitative claim
- Open questions / data gaps explicitly listed
- One-paragraph closing summary at session end: what's defensible, what's gappy, what would need NCR / Rapid-POS internal data to resolve

## Reporting

Single one-page status at completion:
- Sources scanned (count + types)
- Pain themes surfaced (count + top 3)
- TAM headline + confidence
- Identified gaps that need primary research (customer interviews, vendor data requests)

## Out of scope

- Do NOT contact Rapid POS, NCR, or any specific retailer. Public web only.
- Do NOT fabricate numbers. If sources are weak, mark them weak.
- Do NOT scrape paywalled content or violate site ToS.
- Do NOT produce sales material. The outputs are research artifacts; sales positioning is a downstream consumer.
- Do NOT modify Canary code or any non-output files.
- Do NOT git commit. Founder reviews outputs and commits.

## Related

- `Brain/wiki/ncr-counterpoint-api-reference.md` — what Counterpoint actually does (defines what gaps exist)
- `Brain/wiki/ncr-counterpoint-rapid-pos-relationship.md` — VAR relationship clarification (why this dispatch targets Rapid POS specifically AND Counterpoint generally)
- `docs/sdds/canary/ncr-counterpoint-retail-spine-integration.md` — integration SDD informing what Canary already covers
- Memory: `project_canary_native_labor_module_opportunity.md` — Module L / W native-build framing this research helps size

---

**Dispatch author:** Senior ALX (laptop), 2026-04-25
**Executor:** Background agent on the laptop
**Review gate:** Founder reviews both wiki articles before they merge
