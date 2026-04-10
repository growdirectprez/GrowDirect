# Playbook: Neighborhood Content Hub

**Purpose:** Repeatable process for building a neighborhood hub page for TheHillPV.com, from source crawl to published content in Angelique's voice.

**Pilot:** Lunada Bay, PVE (April 2026)
**Output locations:**
- Raw content pool: `Angel/knowledge/content-pools/{neighborhood}-raw.md`
- Hub page draft: `Angel/knowledge/content-pools/{neighborhood}-hub.md`
- Published page: TheHillPV.com `/neighborhoods/{slug}` (when Flask content engine is live)

---

## Step 0: Read Context First

Before doing anything, load these files:

| File | Why |
|------|-----|
| `Brain/projects/Angel.md` | Project MOC — what Angel is, who Angelique is |
| `Angel/knowledge/agentic-profile.md` | Voice rules — the non-negotiable tone guide |
| `Angel/knowledge/community-intelligence.md` | Source registry — all crawlable sources by tier |
| `Angel/knowledge/market-knowledge.md` | Neighborhood descriptions, median prices, character |
| `Brain/wiki/south-bay-wiki-architecture.md` | Content spine — what categories each hub covers |
| `Brain/raw/processed/angel/` | Angelique's original printed guide (2 pages) — seed voice samples |

If the neighborhood already has a content pool, read that too before re-crawling.

---

## Step 1: Crawl Sources

### What to Crawl

Pull from the Source Registry (`Angel/knowledge/community-intelligence.md`), filtering for the target neighborhood. Priority order:

**Tier 1 — RSS Feeds (daily):**
- Patch PV: `patch.com/california/palosverdes/feed`
- Easy Reader: `easyreadernews.com/feed/`
- Daily Breeze: `dailybreeze.com/feed/`

**Tier 2 — Structured Calendars (weekly):**
- City of RPV: `rpvca.gov/Calendar.aspx`
- PVPUSD: `pvpusd.net/apps/events/`
- PVPLC: `pvplc.org/events`
- South Coast Botanic Garden: `southcoastbotanicgarden.org/events`
- PV Chamber: `palosverdeschamber.com/events`
- Terranea: `terranea.com/events` (often blocks direct fetch — use search instead)

**Tier 3 — Community Content Sites (weekly):**
- South Bay by Jackie: `southbaybyjackie.com` (weekend guides, event roundups)
- Palos Verdes Pulse: `palosverdespulse.com` (peninsula lifestyle, business openings)
- OurSouthBay / Southbay Magazine: `oursouthbay.com` (lifestyle features)
- Rachel Ezra calendar: `rachelezra.com/south-bay-calendar` (competitor reference)

**Also search for:**
- `"{neighborhood} Palos Verdes events {current month} {year}"`
- `"{neighborhood} restaurants"` / `"{neighborhood} dining"`
- `"{neighborhood} real estate market {year}"`
- `"{neighborhood} schools ratings"`
- GreatSchools for the specific elementary + feeder pattern

### How to Crawl

**Tool priority:** Firecrawl MCP (if available) > WebFetch > WebSearch

In the Lunada Bay pilot, Firecrawl MCP was configured (`.mcp.json`) but tools weren't exposed at runtime. WebSearch worked reliably for search-based discovery. WebFetch was blocked on some sites (PV Pulse, South Bay by Jackie, Terranea) but worked on others.

**Parallel agent strategy:** Dispatch 3 background agents simultaneously:
1. **Events agent** — crawls calendars, event sites, Patch
2. **Dining/lifestyle agent** — crawls restaurant sources, lifestyle articles, shopping
3. **Schools/community agent** — crawls GreatSchools, PVPUSD, news sites, real estate data

Each agent returns structured results by category with source URLs.

### What to Capture Per Category

**Events:** name, date/time, location, description, source URL, recurring flag
**Dining:** name, cuisine, location, what's notable, hours, source URL
**Schools:** name, grades, rating, test scores, feeder pattern, programs, source URL
**Real estate:** median price, price/sqft, sales volume, DOM, trends, source URL
**Community news:** headline, date, summary, source URL
**Shopping:** tenant name, category, tenure notes

---

## Step 2: Build the Content Pool

Write to `Angel/knowledge/content-pools/{neighborhood}-raw.md`.

Structure:
1. **Neighborhood Facts** — character, identity, real estate data
2. **Schools** — feeder pattern, ratings, district context
3. **Dining & Coffee** — organized by proximity (at the plaza, nearby, destination)
4. **Shopping** — current tenant mix
5. **Events** — current month, recurring, coming up
6. **Community News** — recent developments
7. **Lifestyle Articles** — external coverage (title, source, date, URL)
8. **Seasonal Calendar** — annual events for content planning

Every data point gets a source URL. Every price gets a date. Flag anything that's closed or changed.

---

## Step 3: Write the Hub Page

Write to `Angel/knowledge/content-pools/{neighborhood}-hub.md`.

### Voice Rules (from `agentic-profile.md`)

| Do | Don't |
|----|-------|
| First person ("I"), warm, confident, grounded | Third person, corporate voice |
| Lead with empathy — acknowledge the stress of moving | Open with credentials |
| Specific local knowledge — street names, school campuses | Be vague about locations |
| Opinionated: have favorites, explain why | Use "stunning," "boasts," "vibrant" |
| Lifestyle framing: connect to living here | Write like a wiki or brochure |
| Active voice: "everyone knows" not "is known for" | Use passive voice |
| Natural sentences, conversational flow | Bullet points in client-facing copy |
| End with soft call to action | Aggressive urgency |

### Hub Page Structure

1. **Voice-written intro** — Angelique's personal take on the neighborhood (2-3 paragraphs). Why she loves it, what makes it different. Reference her own experience living on the Hill.

2. **The Neighborhood** — Character, housing stock, price range, who lives here. Data woven into narrative, not a data table.

3. **Schools** — The feeder pattern explained by someone who put two kids through it. Ratings included but framed as context, not the whole story.

4. **The Plaza / Village Center** — Walk through what's there now. Name specific businesses, give opinions. Mention recent openings and closings.

5. **Where to Eat Nearby** — Opinionated picks beyond the plaza. Connect each to a use case ("where I take clients," "weeknight family dinner," "date night").

6. **What's Happening Right Now** — Current month events, recurring activities, coming-up previews. This section makes the page alive, not static.

7. **Community Pulse** — Recent news, city updates, HOA activity. Things a prospective resident would want to know.

8. **Further Reading** — Curated external links with context.

9. **Closing paragraph** — Brief, warm, personal. Signature block with contact info and DRE#.

10. **Source attribution** — List sources crawled and date, small text at bottom.

### Freshness Signals

The hub page should feel current. Include:
- "Updated April 2026" in the header
- "This month" callouts in the events section
- "New" or "Just opened" flags on recent businesses
- "Closed" notes on departed tenants
- "Last crawled" date at the bottom

---

## Step 4: Quality Check

Before considering the hub page done:

- [ ] Voice check: Read the intro aloud. Does it sound like Angelique or a brochure?
- [ ] No cliches: Search for "nestled," "boasts," "vibrant," "prestigious," "world-class," "turn-key"
- [ ] No passive voice: Search for "is known for," "is located," "is situated"
- [ ] Data dated: Every price, rating, or stat has a source and date
- [ ] Links work: Every "Further Reading" URL is real
- [ ] Compliance: DRE# present, no steering, no appreciation guarantees
- [ ] Freshness: At least 3 things that are specific to the current month
- [ ] Opinions: At least 5 places where Angelique has a specific recommendation, not just a list

---

## Step 5: Distribution

Once the Flask content engine is live, the hub page becomes a template-rendered page at `TheHillPV.com/neighborhoods/{slug}`. Until then, the markdown serves as:
- Draft content for the website build
- Source material for social media posts
- Newsletter content (the events section feeds "This Week on the Hill")
- RSS feed items once published

---

## Session Log

### 2026-04-10 — Lunada Bay Pilot

**Session type:** Content crawl + hub page creation
**Agents dispatched:** 3 (events, dining/lifestyle, schools/community)
**Tools used:** WebSearch (primary), WebFetch (blocked on some sites), Firecrawl MCP (configured but not exposed)
**Sources crawled:** 15+ (Patch, Easy Reader, PV Pulse, OurSouthBay, SB by Jackie, RPV Calendar, PVPLC, SCBG, PV Chamber, GreatSchools, PVPUSD, Redfin, PV Source, LBHOA, Yelp, TripAdvisor)
**Output:**
- `Angel/knowledge/content-pools/lunada-bay-raw.md` — structured content pool (8 categories)
- `Angel/knowledge/content-pools/lunada-bay-hub.md` — voice-written hub page
**Gaps noted:**
- Firecrawl MCP tools need to be verified at runtime (configured in `.mcp.json` but not available)
- Terranea, PV Pulse, SB by Jackie block direct WebFetch — use search or RSS instead
- May 2026 events were sparse (calendars not yet updated)
- Lunada BayHouse closed — no replacement tenant confirmed
**Next neighborhood candidate:** Malaga Cove (has seed data in wiki)
