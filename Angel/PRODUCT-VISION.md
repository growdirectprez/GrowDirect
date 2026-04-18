# Angel — Product Vision

**What it is:** A web presence and content platform for Angelique Lyle's Palos Verdes real estate practice.

**What it is not:** A CRM. An AI chatbot. A lead pipeline system. Those come later, if ever.

## The Problem

Angelique has 20 years of local expertise and no web presence that reflects it. Her Luxury Presence site is a brochure. Her printed neighborhood guide is two pages. Her market knowledge lives in her head. None of it is findable, shareable, or generating inbound leads.

## The Product

A content website — TheHillPV.com — that turns Angelique's knowledge into searchable, shareable, SEO-optimized content written in her voice. When someone googles "best neighborhoods in Palos Verdes" or "PVPUSD school ratings" or "Lunada Bay homes," they find Angelique's take — not Zillow's.

## What Ships

**Neighborhood guides** — one page per PV neighborhood. Character, pricing, who lives there, insider perspective. Written in Angelique's voice, updated quarterly with fresh market data.

**School guide** — PVPUSD schools with ratings, programs, feeder patterns, parent perspective. Updated annually.

**Market content** — monthly snapshots. What sold, what's sitting, what's trending. Data-driven but voice-wrapped.

**Lifestyle content** — dining, coffee, events, parks. The South Bay Wiki content, curated and opinionated. Seasonal updates.

**SEO foundation** — schema.org markup, sitemap, meta descriptions, internal linking. The boring stuff that makes content findable.

## What Doesn't Ship (Yet)

- AI chatbot / agent sidecar
- Lead pipeline with stages
- Twilio SMS notifications
- Compass CRM sync
- Webhook integrations
- APN-based property database
- Market analysis engine

These are real ideas. They're not v1. V1 is: does Angelique's content show up when people search, and does it make them want to call her?

## How It's Built

Flask app. Server-rendered pages. Tailwind CSS. Good typography. Fast. No SPA, no React, no widget framework. Content lives in the database so it can be queried and updated programmatically, but the site reads like a magazine, not an app.

The data layer (parcels, listings, market snapshots) exists to feed the content. It's infrastructure, not product. Nobody sees the database — they see the articles it generates.

## How It's Different from What Was Planned

The 7 SDDs and 16 Linear issues describe a platform: AI agent, CRM pipeline, webhook ingestion, multi-domain strategy, Compass sync. That was architecture for a product that doesn't have its first user yet.

This vision is smaller and more honest: make a website that's good enough that people find it, read it, and call Angelique. If that works, everything else follows. If it doesn't, the pipeline doesn't matter.

## Relationship to Cove

None, at the code level. Angel is its own Flask app, its own database, its own docker-compose. They share a founder and some PV peninsula knowledge in Brain. That's it.

Cove is an HOA governance prototype for the WPBCA board. Angel is a real estate content platform for Angelique. Different users, different products, different codebases.

## Relationship to Brain

Brain wiki articles about PV (community history, geology, neighborhoods, declaration scheme) are shared knowledge. Angel's content team (currently: you and Claude) can draw on Brain research when writing neighborhood guides or market content. But Angel doesn't import from Brain programmatically — it's a knowledge reference, not a data source.

## Success Metric

Someone googles a Palos Verdes real estate question and finds TheHillPV.com. They read something useful. They call Angelique. That's it.
