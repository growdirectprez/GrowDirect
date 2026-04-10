# Angel Brand & Launch Plan

> **Status:** Proposed — concept spec, pending Angelique approval
> **Namespace:** angel
> **Date:** 2026-04-06
> **Author:** ALX (COO) / Jeffe (CEO)
> **Audience:** Internal (GrowDirect) + Angelique Lyle pitch

---

## 1. The Brand Concept

### Why "Angel"

The name works on three levels:

1. **Personal** — Angelique → Angel. It's her name, shortened the way locals
   would. It's authentic, not manufactured.
2. **AI assistant** — "Meet Angel" is how we introduce the chatbot. The name
   bridges the human and the technology naturally.
3. **Positioning** — On a peninsula where agents compete on prestige and
   luxury branding, "Angel" is warm, approachable, and memorable.

### Brand Voice

Angel (the brand) inherits Angelique's actual voice — not a corporate version
of it. The voice was defined in the agentic profile and distilled through
conversations about how she actually talks to clients:

**Tone:** Warm, confident, grounded. She leads with empathy. She knows the Hill
because she lives on it. She figured things out the hard way and shares what
she learned without pretense.

**Signature language:**
- "Life above the Pacific" — the tagline
- "The Hill" — locals' name for the peninsula
- "I figured it out the hard way" — authenticity marker
- First person, always. Never corporate third-person.

**What we kill from the old brand:**
- "Abalone Shore" and all prior sub-brand attempts
- Disjointed visual identities across different materials
- Generic luxury agent language ("stunning," "prestigious," "dream home")
- Third-person corporate voice
- Any branding that she couldn't take with her if she left Compass

### Brand Independence

Critical design constraint: Angel is Angelique's brand, not Compass's. If she
moves brokerages, the brand moves with her. Compass and Accardo Real Estate
Associates appear as supporting credits (as required by DRE), not as the
primary identity.

```
Primary:     Angel | Angelique Lyle
Secondary:   Compass · Accardo Real Estate Associates
Required:    DRE# 01475592
```

---

## 2. Visual Identity (Direction)

Final visual design requires a designer. These are strategic directions, not
finished assets.

### Color Palette

Inspired by the PV peninsula itself — ocean, fog, sandstone, native sage.
Not gold-and-black "luxury." Not Compass navy.

| Role | Direction | Rationale |
|------|-----------|-----------|
| Primary | Deep ocean blue-green | The Pacific view that defines PV |
| Secondary | Warm sandstone / terracotta | Rancho-era architecture, earth |
| Accent | Coastal sage green | Native landscaping, trails, nature |
| Neutral | Fog gray / warm white | The marine layer, softness |

### Typography Direction

- Headline: modern serif (warmth + authority — not cold sans-serif tech branding)
- Body: clean sans-serif (readable, contemporary)
- No script fonts, no all-caps luxury display type

### Photography Direction

- Real PV locations, not stock (Lunada Bay, Trump National cliffs, Malaga Cove plaza, Portuguese Bend trails)
- Angelique in environment, not studio headshots
- Properties shot at golden hour with ocean backdrop
- Community moments: school events, farmers market, trail walks

---

## 3. The Pitch to Angelique

Angelique will be hesitant. She's seen agent tech tools come and go. The
pitch needs to be grounded, specific, and about her — not about the technology.

### Pitch Framework

**Open with the problem she already feels:**

"Your brand is scattered right now. Abalone Shore, the Compass template, the
various one-off materials — they don't tell one story. And your website is
beautiful but it's the same IDX search that 50,000 other LP agents have.
Meanwhile you have 20 years of knowledge about this peninsula that no other
agent can match."

**Introduce Angel as HER knowledge, available 24/7:**

"What if we took everything you know — every street, every school feeder
pattern, every neighborhood quirk — and made it available to people searching
at 10pm on a Tuesday when you're at dinner? Not a chatbot that says 'an agent
will call you back.' An AI that actually knows Lunada Bay from Miraleste, knows
the difference between PVPUSD and PVUSD, and can pull real transaction data for
any property on the Hill."

**Ground it in data she can verify:**

"We've already loaded 2,368 MLS listings and mapped them to 5,514 county
parcels. We know every APN, every assessed value, every transaction since
July 2023. This is your data, working for you."

**The ask is small:**

"All we need from you right now is a few hours for voice calibration — making
sure Angel sounds like you, not like a tech company. And your blessing to
refresh the website content. We build everything else."

### Objection Handling

| Objection | Response |
|-----------|----------|
| "I don't want to be replaced by AI" | Angel doesn't replace you — it extends you. It handles the 10pm question so you can have dinner. When someone's ready to act, it routes to YOUR phone. |
| "My clients want a human" | They do, and they'll get you. Angel qualifies and warms the lead before you ever pick up the phone. By the time they call, they already trust you because Angel spoke in your voice. |
| "Tech tools are expensive and never work" | We're building this on infrastructure that's already running. Your cost is time for voice calibration, not a $500/month subscription. |
| "Compass has their own tools" | Compass tools are great and we integrate with them — Private Exclusives, Concierge, the Redfin syndication. Angel makes those tools more effective by driving qualified traffic to you. |
| "What if I leave Compass?" | Angel is your brand, not Compass's. The data, the website, the chatbot — it all goes with you. |

---

## 4. Phased Rollout

### Phase 0 — Foundation (Weeks 1–2)

**Goal:** Data platform live, brand concept approved.

| Task | Owner | Deliverable |
|------|-------|------------|
| Import CRMLS data to Angel DB | Builder | 2,368 listings in `listings` table |
| Activate ATTOM enrichment (free trial) | ALX | Deed history, AVM for priority APNs |
| Brand concept presentation | Jeffe | Pitch deck for Angelique |
| Voice calibration session with Angelique | Jeffe + ALX | Validated agentic profile |
| LP account audit | Angelique | Confirm admin access, custom code options |

**Exit criteria:** Angelique says yes. Data platform has listings loaded.

### Phase 1 — Angel Agent MVP (Weeks 3–6)

**Goal:** Working chatbot with core tools, deployed on TheHillPV.com.

| Task | Owner | Deliverable |
|------|-------|------------|
| Angel Agent sidecar (server.py, tools.py) | Builder | Sidecar on port 8004 |
| Core tools: parcel_lookup, listing_search, market_stats | Builder | 3 working tools |
| System prompt with Angelique's voice | ALX | Validated prompt |
| Chat widget (JS embed) | Builder | Embeddable widget |
| TheHillPV.com skeleton (Flask app) | Builder | Home, /ask, /api/chat routes |
| Lead capture → SMS notification | Builder | capture_lead tool → Twilio SMS |
| DNS setup (Cloudflare) | ALX | thehillpv.com pointing to stack |

**Exit criteria:** Visitor can chat with Angel on TheHillPV.com, ask about a
property, and get routed to Angelique's phone via SMS.

### Phase 2 — Content Engine (Weeks 7–10)

**Goal:** TheHillPV.com has enough content to rank for target keywords.

| Task | Owner | Deliverable |
|------|-------|------------|
| Neighborhood pages (5 areas) | Builder + Angel Voice | /neighborhoods/{slug} |
| School guide | Builder + Angel Voice | /schools |
| Market report auto-generation | Builder | /market/{area}/{month} |
| Blog posts (initial batch of 8) | Angel Voice + editorial | /blog/{slug} |
| SEO technical setup (sitemap, schema, meta) | Builder | Crawlable, indexed |
| Google Search Console + Analytics | ALX | Tracking live |

**Exit criteria:** TheHillPV.com indexed by Google with 20+ pages. First
organic impressions appearing.

### Phase 3 — LP Integration + OwnPV Cleanup (Weeks 11–14)

**Goal:** AngeliqueLyle.com refreshed, OwnPalosVerdes.com cleaned up.

| Task | Owner | Deliverable |
|------|-------|------------|
| LP content refresh (bio, neighborhoods, voice) | Angelique + ALX | Updated AngeliqueLyle.com |
| LP chat widget investigation | Builder | Confirmed: embed works or bridge needed |
| Widget embed or bridge CTA on LP | Builder | Angel accessible from LP site |
| OwnPalosVerdes.com spam cleanup | ALX | Clean domain, holding page |
| OwnPV Google reconsideration request | ALX | Penalty removal (if applicable) |
| Compass CRM sync (async lead pipeline) | Builder | Leads auto-sync to Compass |

**Exit criteria:** All three domains active with Angel widget. Leads flowing
to Compass CRM.

### Phase 4 — Optimization (Ongoing)

| Activity | Cadence | Owner |
|----------|---------|-------|
| Market report generation | Monthly | Automated + editorial review |
| Blog content | 2–4 posts/month | Angel Voice + editorial |
| Lead funnel analysis | Weekly | ALX |
| Chat conversation review | Weekly | ALX + Angelique |
| CRMLS data refresh | Weekly | Manual export → automated API (future) |
| ATTOM enrichment runs | Weekly | Automated script |
| SEO keyword tracking | Monthly | ALX |

---

## 5. Success Metrics

### 90-Day Targets (End of Phase 3)

| Metric | Target | Measurement |
|--------|--------|-------------|
| TheHillPV.com pages indexed | 50+ | Google Search Console |
| Monthly organic impressions | 1,000+ | Google Search Console |
| Angel conversations/month | 100+ | Valkey counters |
| Leads captured/month | 10+ | Angel DB leads table |
| Leads → Angelique callback | 80% within 4 hours | Lead stage timestamps |
| Listing appointments from Angel leads | 2+ per month | Manual tracking |

### 12-Month Vision

| Metric | Target |
|--------|--------|
| Monthly organic traffic (all domains) | 5,000+ visits |
| Angel conversations/month | 500+ |
| Leads captured/month | 50+ |
| Closed transactions attributed to Angel | 3–5 per year |
| Revenue impact (at ~$50K avg commission) | $150K–250K/year |

---

## 6. Budget Estimate

### Ongoing Costs

| Item | Monthly Cost | Notes |
|------|-------------|-------|
| Anthropic API (Angel Agent) | $50–200 | ~500 conversations × ~$0.20 avg |
| ATTOM API | $0–200 | Free trial first, then subscription |
| Cloudflare (DNS + CDN) | $0–20 | Free tier likely sufficient |
| Twilio (SMS notifications) | $5–20 | ~50 leads/month × $0.01/SMS |
| Domain renewals | $30/year | TheHillPV.com |
| **Total ongoing** | **$85–440/month** | |

### One-Time Costs

| Item | Cost | Notes |
|------|------|-------|
| Professional photography | $500–1,500 | PV locations, Angelique portraits |
| Logo / visual identity design | $500–2,000 | Freelance designer |
| LP content refresh (copywriting) | $0 | Angel Voice skill generates |
| **Total one-time** | **$1,000–3,500** | |

### What's Free (GrowDirect Infrastructure)

- PostgreSQL, Valkey, Ollama — shared infrastructure, already running
- Flask hosting — Docker container on existing stack
- Development — GrowDirect builder time (factory pipeline)
- Content generation — Angel Voice skill + LLM
- CRMLS data — included with Jeffe's member access

---

## 7. Risk Register

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Angelique says no | Project stops | Ground pitch in her voice, her data, her brand. Small initial ask. |
| LP blocks widget embed | No chat on flagship site | Bridge CTA strategy (link to TheHillPV/ask). Subdomain fallback. |
| OwnPV domain authority unrecoverable | Lose secondary SEO domain | Redirect to TheHillPV. Not critical — TheHillPV is primary. |
| CRMLS API access denied | Manual export only | Continue Top Producer CSV exports (current process). Works fine. |
| ATTOM free trial expires before value proven | Lose enrichment data | Prioritize high-value APN enrichment during trial. Budget for subscription if ROI proven. |
| Low organic traffic initially | Slow lead generation | Expected — SEO takes 3–6 months. Chat widget provides value to direct/referral visitors immediately. |
| Compass compliance concerns about AI chat | Must add disclosures | Pre-build DRE/Fair Housing disclosures into widget footer. Review with broker if needed. |

---

*Angel Brand & Launch Plan SDD — GrowDirect Inc.*
