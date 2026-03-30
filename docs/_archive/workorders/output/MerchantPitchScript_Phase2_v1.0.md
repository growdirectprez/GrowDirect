---
type: workorder
domain: business
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Merchant Pitch Script — Phase 2 Onboarding

**Version:** 1.0
**Date:** February 26, 2026
**Author:** ALX (Chief of Staff)
**Classification:** CONFIDENTIAL — Internal use only
**Purpose:** What Jeffe says at Offset Coffee (or any Phase 2 friendly merchant)
**Prerequisites:** Phase 1 (GrowDirect Lab) complete. Jeffe has done the full flow himself.

---

## Before You Walk In

**Carry with you:**
- Phone with Canary running (showing GrowDirect Lab results — real Chirps on your own data)
- Syd's Scouting Checklist (printed or on phone): `_ALX/WorkOrders/output/Syd/branded/GD_ScoutingChecklist_v1.0.docx`
- Syd's merchant pack ready to email or AirDrop: NDA, Beta Tester Agreement, DPA
- Business cards if you have them (GrowDirect, not Canary — product name stays quiet)

**Mindset:**
- You are not pitching software. You are showing something you built and offering a free look.
- You are not asking questions. You already know how this works because you did it yourself.
- You are not selling. You are recruiting a co-development partner.
- If the vibe isn't right, you leave with coffee and good intel. No pressure. Ever.

---

## The Conversation

### Opening (2 minutes)

You're at the counter. You've ordered. You're a regular or becoming one. The conversation is natural — not rehearsed.

**If the owner is there and it opens up:**

> "I'm building something for businesses like yours — small retailers who use Square. I'm local, I'm in [Torrance / your neighborhood]. Can I show you something on my phone? It'll take 60 seconds."

**If they say yes, show your phone:**

> "This is what I built. It watches my Square account and tells me when something looks off — a drawer came up short, a refund pattern that doesn't look right, someone opening the register when they shouldn't be. See this one? My test drawer was short $18 last Tuesday. It caught it and walked me through what to do about it."

**Let them look. Let them ask questions. Don't explain everything. Let the screen do the work.**

### The Ask (2 minutes)

> "Here's why I'm here. I've been testing this on my own account, but I need to see if the alerts make sense for a real business — not a test store. I'm looking for one local merchant who'd let me connect to their Square account for a couple weeks. I'd see your transaction data — same stuff that's already in your Square dashboard — and the system would tell you what it finds."

> "You wouldn't need to do anything different. You run your business. Canary watches in the background. If it spots something, you'll see it on your phone."

> "I'm not charging anything. This is co-development. You'd be helping me make the product better, and in return you get a free look at what's happening in your business that you can't see today."

### Handling Objections

**"What data would you see?"**
> "Same data that's in your Square dashboard — transactions, refunds, cash drawer open/close, timecards. Nothing new gets collected. I'm just watching what Square already records and looking for patterns."

**"Is it safe?"**
> "Square controls the permissions. When you connect, Square shows you exactly what you're sharing — you approve it on Square's own page, not mine. And I have an NDA and a data agreement I'd want us both to sign before anything connects. This is real — I'm building a real business here."

**"How long would it take?"**
> "About 15 minutes to connect. You log into your Square account, approve the permissions, and it starts working. I'd want to check in with you after a week to see what it found and whether the alerts made sense to you."

**"What if I don't like it?"**
> "You disconnect anytime. One tap in your Square dashboard under 'Connected Apps.' Your data stays in your Square account — I delete everything on my end. No strings."

**"What does it cost?"**
> "Nothing right now. You're helping me build this. When it's ready for market, I'll offer you a founder's rate — but that's down the road. Right now I just need to know if the alerts are useful to a real merchant."

### If They're Interested (5 minutes)

> "Great. Here's what happens next. I'll send you two short documents — a mutual NDA and a beta tester agreement. They basically say: I'll protect your data, you'll protect my product details, and either of us can walk away anytime. My legal counsel wrote them in plain English — no surprises."

> "Once those are signed, I'll send you a link. You tap it, log into Square, approve the connection, and we're live. The system will pull your last week of data and start looking for patterns. I'll check in with you [next week / in a few days] to walk you through what it found."

**Do NOT connect on the spot during the first visit unless the merchant is enthusiastic and the vibe is right. The better play is usually: leave the docs, connect on a follow-up visit.**

### Closing (1 minute)

> "I appreciate your time. I'll send those docs over today. And seriously — the coffee is great. I'll be back regardless."

**Leave your contact info. Don't linger. Let them think about it.**

---

## After the Visit

**Same day:**
1. Send Syd's merchant pack via email (NDA + Beta Tester Agreement + DPA)
2. Include a one-paragraph email recap: "Great meeting you. Here are the docs I mentioned. Take your time reviewing — no rush. When you're ready, I'll send the connection link and we'll be up and running in 15 minutes."
3. Update TRIAGE.md and HANDOFF.md with recon results
4. Brief Jim — he'll handle logistics from here if merchant says yes

**When merchant signs:**
1. Jim reaches out to schedule the connection (Jeffe can do this too — keep it personal)
2. Jeremy confirms pipeline is ready (webhook URL live, backfill working)
3. Jeffe sends the OAuth connection link
4. Jeffe walks merchant through the first Today's View load (in person if possible)

**If merchant says no or goes quiet:**
- No follow-up pressure. One gentle check-in after 5 days, max.
- Move to next candidate. The lead database has 5 more options.
- Adjust the pitch based on what didn't land.

---

## What NOT to Say

- Don't say "AI." Don't say "machine learning." Don't say "algorithm." Say "it watches for patterns."
- Don't say "data warehouse" or "CRDM" or any technical term. Say "it connects to your Square account."
- Don't name the product. Say "something I'm building" or "my system." The product name is confidential until Phase 3.
- Don't promise features that don't exist yet. Show what's working today.
- Don't bad-mouth Square. Square is the platform you're building on. Say "Square is great for payments — I'm adding the piece that watches for problems."
- Don't mention the team. It's "I'm building" not "we have a team of 15 agents." The merchant is talking to the founder.
- Don't quote shrink statistics. The merchant knows they lose money — they don't need a lecture. Show them, don't tell them.

---

## The One Thing That Matters

The merchant sees a real Chirp from their own data and says: **"I didn't know that was happening."**

That's the sale. Everything else is logistics.

---

*GrowDirect | CONFIDENTIAL*
*February 26, 2026*
