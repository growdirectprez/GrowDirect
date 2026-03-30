---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Work Order: DNS Consolidation to Cloudflare

**Agent:** Jeremy (Dev / Infra)
**Issued by:** ALX on behalf of Jeffe
**Date:** February 26, 2026
**Priority:** 🟡 HIGH
**Triage Ref:** B-038

---

## Outcome

All seven GrowDirect domains route through Cloudflare DNS. One dashboard, one place to manage records. GoDaddy stays as registrar for growdirect.app and hosting provider for the growdirect.io website + email. Nothing breaks during the switch.

## Current State

| Domain | Registrar | DNS Currently | Purpose |
|---|---|---|---|
| eljeffe.io | Cloudflare | Cloudflare | Primary — Canary API |
| eljeffe.org | Cloudflare | Cloudflare | Redirect / reserve |
| eljeffe.wtf | Cloudflare | Cloudflare | Redirect / reserve |
| eljeffe.dev | Cloudflare | Cloudflare | Redirect / reserve |
| eljeffebtc.com | Cloudflare | Cloudflare | Foundation umbrella |
| jeffe.io | Cloudflare | Cloudflare | Short-form / personal brand |
| growdirect.app | GoDaddy | GoDaddy | Parent company web presence |

## Tasks

### 1. Migrate growdirect.app DNS to Cloudflare
- Add growdirect.app as a site in Cloudflare (free plan)
- Cloudflare will provide two nameservers (e.g. `ada.ns.cloudflare.com`, `bob.ns.cloudflare.com`)
- Log into GoDaddy → growdirect.app → DNS Management → Change nameservers to the Cloudflare pair
- Wait for propagation (usually < 1 hour, can take up to 48)

### 2. Preserve GoDaddy Email (growdirect.io)
- Before touching growdirect.io DNS (if/when it moves to Cloudflare later): capture ALL existing MX records from GoDaddy
- Recreate MX records in Cloudflare pointing to GoDaddy's mail servers
- Also capture any SPF, DKIM, DMARC TXT records and recreate them
- **Test email send/receive before declaring done**

### 3. Preserve GoDaddy Website Hosting (growdirect.io)
- The growdirect.io website builder site stays on GoDaddy hosting
- If/when growdirect.io DNS moves to Cloudflare: set an A record or CNAME pointing to GoDaddy's hosting IP
- Verify the site loads through Cloudflare proxy

### 4. DNS Record Plan (all seven domains)
Draft a record map for Jeffe's approval:

| Domain | Record Type | Points To | Purpose |
|---|---|---|---|
| eljeffe.io | A / CNAME | [Canary API host] | Primary API |
| growdirect.app | A / CNAME | [TBD — company landing] | Parent company site |
| growdirect.io | A / CNAME | GoDaddy hosting IP | Existing website + CRM |
| jeffe.io | Redirect rule | [TBD] | Short links / personal |
| Others | Redirect rule | eljeffe.io or growdirect.app | Parked / redirect |

### 5. Validation
- All seven domains resolve correctly
- Email send/receive works on growdirect.io
- growdirect.io website loads normally
- No DNS propagation issues after 48 hours

## Constraints
- **Do NOT touch email MX records without testing first**
- **growdirect.io website must stay live throughout migration**
- Zero downtime is the goal — if propagation creates a gap, schedule for low-traffic window
- No cloud API spend — Cloudflare free tier only

## Dependency
- Jeffe approves the DNS record plan (Task 4) before Jeremy implements
- Worm takes over growdirect.io site content after DNS is stable

## Done When
- All seven domains managed in Cloudflare DNS dashboard
- Email works
- Website works
- Record plan approved and implemented
- B-038 updated to RESOLVED
