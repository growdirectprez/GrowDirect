# SEO Mining Playbook — Transaction Data → Content Authority → Leads

## The Core Insight

Most agents create content based on what they *think* people want to read.
Angelique creates content based on what she's *actually sold* — backed by
20 years of CRMLS transaction data. Every closed deal is a proof point.
Every neighborhood she's worked becomes a content authority zone.

The pipeline: **Mine → Map → Write → Rank → Convert**

---

## Stage 1: MINE — Extract Intelligence from Transaction History

### Data Source
CRMLS RESO Web API → Property resource filtered by Angelique's MLS Agent ID
(both `ListAgentMlsId` and `BuyerAgentMlsId` for listing-side and buy-side deals).

### What We Extract per Transaction

| Field | SEO/Marketing Use |
|-------|-------------------|
| Address + APN | Geo-target for neighborhood content |
| City / Zip / Neighborhood | Power zone identification |
| ClosePrice | Price band authority |
| ListPrice → ClosePrice delta | Negotiation story (list-to-sale ratio) |
| DaysOnMarket | Speed-of-sale story |
| PropertyType | Content vertical (SFR, condo, townhome, land) |
| Beds / Baths / SqFt | Buyer profile matching |
| CloseDate | Recency weighting, seasonal patterns |
| Side (list vs. buy) | Listing authority vs. buyer knowledge |
| OriginalListPrice → ClosePrice | Full pricing narrative |

### Derived Intelligence

**Power Zones** — neighborhoods where she has 3+ closed transactions:
- These are her highest-authority content targets
- Every blog post about these neighborhoods can reference "I've sold X homes here"
- Example: "Lunada Bay" with 12 closed deals = she IS the Lunada Bay expert

**Price Bands** — her transaction distribution by price:
- Identifies her sweet spot (where she closes most deals)
- Reveals growth opportunities (price bands she wants to break into)
- Drives ad targeting (match buyer search to her proven range)

**Seasonal Patterns** — close dates mapped by month/quarter:
- When does inventory move in each neighborhood?
- Drives content calendar (publish school content in Jan-Mar for fall enrollment)
- Drives listing acquisition timing (contact likely sellers 3 months before peak)

**Property Type Mix** — what she's sold by type:
- SFR dominance = lean into family/school content
- Condo experience = first-time buyer content angle
- Land/estate = luxury/custom build content

**Trend Lines** — how her market footprint has evolved:
- Expanding into new neighborhoods? Create content to establish authority there
- Average price climbing? Update messaging for move-up buyers
- More buy-side deals? She knows what buyers want — use that in listing pitches

---

## Stage 2: MAP — Connect Transaction Authority to SEO Targets

### The Authority Matrix

For each neighborhood in her power zones, cross-reference:

| Dimension | Data Source | Output |
|-----------|------------|--------|
| Her closed deals | CRMLS transaction history | Authority score (# deals, recency, volume) |
| Search volume | Google Keyword Planner / SEMrush / Ahrefs | Demand signal |
| Competition | SERP analysis | Difficulty score |
| Content gap | Competitor blog analysis | Opportunity score |
| Conversion potential | Lead value × conversion rate | Revenue score |

### Priority Score Formula

```
Priority = (Authority × 0.3) + (Search Volume × 0.25) +
           (Content Gap × 0.25) + (Conversion Potential × 0.2)
```

### Target Keyword Categories

**Tier 1: Neighborhood + Intent** (highest conversion)
- "homes for sale in Lunada Bay" → she's sold 12 there, write the definitive guide
- "Rancho Palos Verdes real estate agent" → her home turf
- "buy a home in Rolling Hills Estates" → transactional intent

**Tier 2: Neighborhood + Life Decision** (relocation families)
- "best schools Palos Verdes" (720/mo) → school guide anchored to neighborhoods she knows
- "moving to Palos Verdes with kids" (170/mo) → relocation guide with her personal story
- "Palos Verdes vs Manhattan Beach families" (210/mo) → comparison she can write authoritatively

**Tier 3: Neighborhood + Local Knowledge** (long-tail authority)
- "Lunada Bay neighborhood review" → she lives this
- "PVPHS vs PVHS which is better" → she raised kids through both feeders
- "Portuguese Bend horse property" → if she has deals there, she's the expert
- "Hollywood Riviera Torrance hidden gem" → if she has buy-side deals there

**Tier 4: Market Intelligence** (newsletter/social content)
- "Palos Verdes home prices 2026" → she has the actual data from her deals
- "how long do homes take to sell in PVE" → her DOM data answers this
- "is it a good time to sell in Rancho Palos Verdes" → market analysis backed by deals

### Content Authority Signals

For every piece of content, we embed real transaction proof:

**Weak (generic agent):** "Lunada Bay is a beautiful neighborhood."

**Strong (data-backed Angelique):** "I've helped 12 families find their home in
Lunada Bay over the past 8 years. The median price I've closed at is $3.1M,
and the average time from listing to sold is 28 days — well below the
Peninsula average. Here's what I tell every family considering the Bay..."

This is the difference between commodity content and authority content.

---

## Stage 3: WRITE — Content Briefs Powered by Transaction Data

### Blog Post Formula (OwnPalosVerdes.com)

Every blog post follows this structure:

1. **Hook** — the question a relocating mom is Googling at 11pm
2. **Authority** — "I've sold X homes in this neighborhood / I raised my kids here"
3. **Substance** — real data, real street names, real school experiences
4. **Proof** — transaction-backed claims (DOM, pricing, trends she's seen)
5. **CTA** — soft, warm, low-pressure ("When you're ready, I'm here")

### Content Brief Template

```
TARGET KEYWORD: [keyword] ([search volume]/mo)
AUTHORITY SCORE: [# deals in this zone] deals, $[volume] closed
CONTENT TYPE: [blog / guide / comparison / market report]
WORD COUNT: [800-1500]
COMPETITOR CONTENT: [top 3 ranking URLs — what they cover, what they miss]

ANGLE: What can Angelique say that NO other agent can?
- Personal experience: [specific anecdote]
- Transaction proof: [X deals, $Y volume, Z avg DOM]
- Local knowledge: [street-level detail competitors don't have]

OUTLINE:
1. [Hook — the reader's question]
2. [Answer with authority]
3. [Deep detail — neighborhoods, schools, specific streets]
4. [Data — pricing, DOM, trends from her transactions]
5. [Personal touch — her own experience]
6. [Soft CTA]

INTERNAL LINKS: [other OwnPalosVerdes pages to link to]
SCHEMA MARKUP: LocalBusiness, RealEstateAgent, FAQPage
```

---

## Stage 4: RANK — Technical SEO + Content Distribution

### On-Page SEO (OwnPalosVerdes.com)

- **Schema markup:** RealEstateAgent, LocalBusiness, FAQPage on every guide
- **Geo-targeted pages:** One definitive page per neighborhood in her power zones
- **Internal linking:** Neighborhood pages → school guide → market reports → contact
- **Fresh content signals:** Monthly market updates (automated from transaction data)
- **E-E-A-T signals:** Transaction proof = Experience + Expertise + Authority + Trust

### Content Distribution (Real-World Marketing Tie-In)

| Channel | Content Type | Transaction Data Use |
|---------|-------------|---------------------|
| OwnPalosVerdes.com | Neighborhood guides, school guide, market reports | Authority proof in every article |
| Instagram | Just Listed / Just Sold, neighborhood moments | "Just closed in Lunada Bay — my 12th sale here" |
| Facebook | Community content, market updates | Share blog posts with personal commentary |
| Email newsletter | Monthly market update | "Here's what I'm seeing based on my recent closings" |
| YouTube (future) | Neighborhood video tours | Walk the streets she's sold on |
| Google Business Profile | Posts, reviews, Q&A | Transaction count in business description |
| Farming mailers | Neighborhood-specific postcards | "I've sold X homes on your street / in your community" |
| Open house follow-up | Personalized email | "Based on what I've seen in this neighborhood..." |

---

## Stage 5: CONVERT — From Content to Client

### The Funnel

```
Google Search → OwnPalosVerdes.com (SEO content)
                ↓
         Read school guide / neighborhood guide (5+ minutes)
                ↓
         Retarget on Instagram/Facebook (Meta Pixel)
                ↓
         See "I've sold 12 homes in Lunada Bay" social proof
                ↓
         Return to site → download relocation guide (lead capture)
                ↓
         Email sequence begins (Angel voice, empathy-first)
                ↓
         Angelique calls → appointment → client
```

### Key Metrics

| Metric | Target | How Transaction Data Helps |
|--------|--------|--------------------------|
| Organic traffic to OwnPalosVerdes | 2,000+ monthly | Authority content ranks higher |
| Time on page (guides) | 4+ minutes | Real data keeps readers engaged |
| Lead capture rate | 3-5% of visitors | Social proof increases trust |
| Email open rate | 35%+ | Personalized, data-backed subject lines |
| Lead-to-appointment | 15-20% | "She knows this neighborhood" confidence |
| Appointment-to-client | 50%+ | Transaction proof closes the trust gap |

---

## Real-World Marketing Integration

### Farming Mailers (Neighborhood-Specific)

For each power zone, create quarterly postcards:

> **LUNADA BAY MARKET UPDATE**
> I've helped 12 families buy or sell in Lunada Bay since 2018.
> Here's what I'm seeing right now:
> • Median sale price: $3.1M (up 8% YoY)
> • Average days on market: 28 days
> • Homes listed in the last 90 days: 4
>
> Thinking about selling? I'd love to give you a no-pressure market
> assessment. I know this neighborhood — I've walked every street.
>
> — Angelique
> angelique.lyle@compass.com | OwnPalosVerdes.com
> CA DRE# 01475592 | Compass

### Open House Strategy

Hold open houses in her power zones — neighborhoods where she has the most
closed deals. The conversation advantage: "I've sold the house three doors
down, and the one on the corner. I know what buyers pay here."

### Sphere of Influence Nurture

For past clients (from transaction database):
- Annual home value update: "You bought at $X in 2019 — here's where you stand"
- Neighborhood changes: "Two new listings on your street — market's moving"
- Referral ask: "Know anyone thinking about the Peninsula?"

### Compass Private Exclusive Advantage

Her transaction data proves the PE strategy works:
- Filter her sales to PE vs. direct MLS
- Calculate the actual premium she's achieved
- Use that data in listing pitches: "My Private Exclusive listings close X% higher"
