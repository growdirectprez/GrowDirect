# CRM Pipeline & Lead Management

## Pipeline Stages

Angel tracks leads through a pipeline that maps to real estate milestones,
not arbitrary CRM states. Each stage is triggered by an APN event or a
client action.

### Seller Pipeline

| Stage | Trigger | Action |
|-------|---------|--------|
| **Prospect** | APN flagged (likely to sell, DOM threshold, price reduction) | Add to watch list, research property |
| **Contacted** | First outreach sent (email, call, door knock) | Log activity in Compass CRM |
| **Listing Appointment** | Meeting scheduled | Prep CMA, Concierge assessment, Private Exclusive pitch |
| **Listed — Private** | Listing agreement signed, PE live | Launch Phase 1 (Private Exclusive) |
| **Listed — MLS** | MLS entry | Launch Phase 3+ (full marketing) |
| **Under Contract** | Offer accepted | Transaction Coordinator handoff |
| **Closed** | Grant deed recorded | Post-close follow-up, referral request |

### Buyer Pipeline

| Stage | Trigger | Action |
|-------|---------|--------|
| **Lead** | Inquiry received (website, referral, open house) | Qualify: timeline, budget, area preference |
| **Qualified** | Budget confirmed, timeline under 12 months | Set up Compass Collections, saved search |
| **Active Search** | Showings scheduled | Send matching listings, neighborhood guides |
| **Offer Submitted** | Offer written | Negotiate, track competing offers |
| **Under Contract** | Offer accepted | Transaction Coordinator handoff |
| **Closed** | Grant deed recorded | Welcome package, check-in sequence |

---

## Lead Sources

### Organic / Content
- OwnPalosVerdes.com (SEO — school guides, neighborhood content)
- angeliquelyle.com (Luxury Presence agent site)
- Social media (Instagram, Facebook)
- Blog posts and market updates

### Referral
- Past client referrals (highest conversion rate)
- Compass agent-to-agent referrals
- Relocation companies

### Data-Driven (Angel Lead Engine)
- APN monitoring (new listings, price reductions, grant deeds)
- Likely-to-sell predictions (Compass + SmartZip)
- Employer relocation feeds (aerospace/tech hiring surges)
- Behavioral signals (out-of-state visitors on OwnPalosVerdes.com)

### Paid
- Google Ads (targeted search terms)
- Meta Ads (retargeting out-of-state school guide readers)
- Compass Marketing Center campaigns

---

## Follow-Up Cadences

### New Relocation Lead
- Day 0: Personal email (empathy-first, neighborhood guide offer)
- Day 2: Text/call if no response
- Day 5: Follow-up email with school guide link
- Day 14: Market snapshot for their target neighborhoods
- Day 30: Check-in email ("still looking?")
- Monthly: Market update newsletter (ongoing until unsubscribe)

### Post-Open House
- Day 0: Thank you email (reference specific property)
- Day 2: Send comparable listings
- Day 7: "Any questions about the neighborhood?"
- Day 14: New listing alert if matching criteria

### Sphere of Influence (Past Clients)
- Quarterly: Market update with local relevance
- Annual: Home anniversary note
- Ongoing: Social media engagement
- Event-triggered: "Thinking of selling?" when market conditions favor

---

## Compass CRM Integration Points

| Angel Action | Compass CRM Effect |
|-------------|-------------------|
| New lead captured | Create contact with tags, source, notes |
| Pipeline stage change | Update deal stage in pipeline |
| Activity logged | Record call/meeting/note on contact |
| Email sent | Log communication in contact timeline |
| Listing launched | Update listing status, link to contact |
| Collection created | Share curated property list with buyer |

---

## Key Metrics

- **Lead-to-close conversion rate** — target: 2-3% (industry avg ~1.5%)
- **Average response time** — target: under 5 minutes for web leads
- **Touches to appointment** — typically 5-8 for cold, 2-3 for referral
- **Pipeline value** — total potential commission in active pipeline
- **Days in stage** — flag leads stuck in any stage over threshold
