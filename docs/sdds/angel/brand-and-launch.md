# Angel Brand & Launch Plan

> **Type:** Reference Document (not a deployable service)
> **Status:** Proposed — concept spec, pending Angelique approval
> **Namespace:** angel
> **Date:** 2026-04-06 (ops upgrade 2026-04-13)
> **Author:** ALX (COO) / Jeffe (CEO)
> **Audience:** Internal (GrowDirect) + Angelique Lyle pitch

**Wiki:** [[Brain/wiki/south-bay-wiki-architecture|South Bay Wiki Architecture]] · [[Brain/wiki/angel-brand-and-team|Angel Brand & Team]] · [[Brain/wiki/angel-voice-training|Angel Voice Training]] · [[Brain/projects/Angel|Angel MOC]]
**Parent:** [[docs/sdds/angel/angel-overview|Angel Overview]]

---

## Purpose

Defines the Angel brand identity, voice specification, and launch strategy for
pitching to Angelique Lyle. This is a reference document — it describes brand
guidelines and rollout plans, not a running service.

---

## The Brand Concept

### Why "Angel"

1. **Personal** — Angelique -> Angel. Her name, shortened the way locals would.
2. **AI assistant** — "Meet Angel" bridges the human and the technology naturally.
3. **Positioning** — Warm, approachable, and memorable on a prestige-driven peninsula.

### Brand Voice

Angel inherits Angelique's actual voice — not a corporate version of it.

**Tone:** Warm, confident, grounded. Leads with empathy. Knows the Hill because
she lives on it.

**Signature language:**
- "Life above the Pacific" — the tagline
- "The Hill" — locals' name for the peninsula
- First person, always. Never corporate third-person.

**What we kill:** "Abalone Shore" and all prior sub-brand attempts. Disjointed
visual identities. Generic luxury agent language. Third-person corporate voice.

### Brand Independence

Angel is Angelique's brand, not Compass's. If she moves brokerages, the brand
moves with her.

```
Primary:     Angel | Angelique Lyle
Secondary:   Compass · Accardo Real Estate Associates
Required:    DRE# 01475592
```

---

## Visual Identity (Direction)

| Role | Direction | Rationale |
|------|-----------|-----------|
| Primary | Deep ocean blue-green | The Pacific view that defines PV |
| Secondary | Warm sandstone / terracotta | Rancho-era architecture, earth |
| Accent | Coastal sage green | Native landscaping, trails |
| Neutral | Fog gray / warm white | The marine layer, softness |

**Typography:** Modern serif headlines (warmth + authority), clean sans-serif body.
**Photography:** Real PV locations, not stock. Angelique in environment, not studio.

---

## The Pitch to Angelique

**Framework:** Open with the problem she feels (scattered brand) -> introduce
Angel as her knowledge available 24/7 -> ground it in verifiable data (2,368
listings, 5,514 parcels) -> small ask (voice calibration + website blessing).

### Objection Handling

| Objection | Response |
|-----------|----------|
| "I don't want to be replaced by AI" | Angel extends you. Handles 10pm questions, routes to your phone. |
| "My clients want a human" | They get you. Angel qualifies and warms the lead first. |
| "Tech tools are expensive" | Built on existing infrastructure. Cost is time for voice calibration. |
| "Compass has their own tools" | Angel integrates with Compass tools. Makes them more effective. |
| "What if I leave Compass?" | Angel is your brand. Data, website, chatbot — all goes with you. |

---

## Phased Rollout

| Phase | Weeks | Goal | Exit Criteria |
|-------|-------|------|---------------|
| **0 — Foundation** | 1-2 | Data loaded, brand approved | Angelique says yes. Listings in DB. |
| **1 — Agent MVP** | 3-6 | Working chatbot on TheHillPV | Visitor -> Angel -> SMS to Angelique |
| **2 — Content & Integration** | 7-10 | TheHillPV live + LP integrated | 20+ pages indexed, widget on both, CRM sync |
| **4 — Optimization** | Ongoing | Growth and refinement | Leads/month growing, SEO ranking |

---

## Success Metrics

### 90-Day Targets

| Metric | Target |
|--------|--------|
| TheHillPV.com pages indexed | 50+ |
| Monthly organic impressions | 1,000+ |
| Angel conversations/month | 100+ |
| Leads captured/month | 10+ |
| Listing appointments from Angel leads | 2+ per month |

### 12-Month Vision

| Metric | Target |
|--------|--------|
| Monthly organic traffic (all domains) | 5,000+ visits |
| Leads captured/month | 50+ |
| Closed transactions attributed to Angel | 3-5 per year |
| Revenue impact | $150K-250K/year |

---

## Budget Estimate

### Ongoing

| Item | Monthly Cost |
|------|-------------|
| Anthropic API | $50-200 |
| ATTOM API | $0-200 |
| Cloudflare | $0-20 |
| Twilio | $5-20 |
| **Total** | **$85-440/month** |

### One-Time

| Item | Cost |
|------|------|
| Photography | $500-1,500 |
| Logo / visual design | $500-2,000 |
| **Total** | **$1,000-3,500** |

---

## Risk Register

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Angelique says no | Project stops | Ground pitch in her voice, data, brand. Small ask. |
| LP blocks widget embed | No chat on flagship | Bridge CTA to TheHillPV. Subdomain fallback. |
| OwnPV domain unrecoverable | Lose secondary SEO | Redirect to TheHillPV. Not critical. |
| CRMLS API access denied | Manual export only | Continue Top Producer CSV. Works fine. |
| Low organic traffic initially | Slow lead gen | Expected. SEO takes 3-6 months. |
| Compass compliance concerns | Must add disclosures | Pre-build DRE/Fair Housing disclosures. |

---

## Operations (Minimal — Reference Document)

This document does not describe a running service. No deployment, health checks,
or monitoring apply. Brand assets (when created) will be stored in:
- `Angel/brand/` — logos, color specs, photography
- `Angel/knowledge/content-pools/` — voice content, neighborhood copy

---

## Code Review Findings

No code review findings — this is a reference document, not a service.

---

## Production Readiness Checklist

N/A — reference document. Brand deliverables tracked in Linear (GRO-460).

---

*Angel Brand & Launch Plan SDD — GrowDirect Inc.*
