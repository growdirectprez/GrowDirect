---
date: 2026-04-26
type: dispatch
status: ready
session: code
priority: critical
tags: [deploy, cloudflare, pages, proposal, quartz, github-pages, dns, armstrong]
due: 2026-04-27
---

# Dispatch — Deploy proposal.growdirect.io + Wire Vault Domains

## Mission

Three deliverables before Monday April 28 1pm (Armstrong meeting):

1. **proposal.growdirect.io** — serve Armstrong_Proposal_v2.html as a live URL
2. **brain.growdirect.io** — wire Canary Retail Brain Quartz vault to custom domain
3. **catz.growdirect.io** — wire CATz Quartz vault to custom domain

---

## Context

- Cloudflare account: Gclyle@growdirect.io (ID: 27bee2623caee5415d031b6281923983)
- Vercel team: growdirectprezs-projects (ID: team_tPcgVcQMZo0OkQOYH39lBxz5) — no projects yet
- No Workers or Pages deployed yet — clean slate
- Proposal file: /Users/gclyle/Desktop/Armstrong_Proposal_v2.html (85,576 bytes)
- Quartz vaults currently on GitHub Pages:
  - Canary Retail Brain → https://growdirect-llc.github.io/canary-retail-brain/
  - CATz → https://growdirect-llc.github.io/catz/
- Cloudflare MCP available via Cowork: Workers, D1, KV, R2 — no DNS zone tool in MCP, use dashboard or wrangler CLI
- Cloudflare Access already configured on both vaults (whitelist: gclyle@growdirect.io, bart@rapidpos.com, tim.mooney@maonach.com) — custom domain wiring is the prerequisite for Access enforcement to activate

---

## Deliverable 1 — proposal.growdirect.io

### Recommended: Cloudflare Pages (static deploy via wrangler)

```bash
# 1. Install wrangler if not present
npm install -g wrangler

# 2. Auth with growdirect Cloudflare account
wrangler login

# 3. Stage the proposal as index.html
mkdir -p /tmp/proposal-site
cp /Users/gclyle/Desktop/Armstrong_Proposal_v2.html /tmp/proposal-site/index.html

# 4. Deploy to Cloudflare Pages
cd /tmp/proposal-site
npx wrangler pages deploy . --project-name=armstrong-proposal
```

This gives `armstrong-proposal.pages.dev` immediately — shareable as a fallback URL if DNS is not ready before Monday.

### Custom domain
Cloudflare dashboard → Pages → armstrong-proposal → Custom domains → Add proposal.growdirect.io

Cloudflare auto-wires the CNAME if growdirect.io is already a zone in this account.

### Access gate decision
- If proposal is public-facing for Monday: leave open, no Access gate
- If confidential: Cloudflare Access → Applications → Self-hosted → proposal.growdirect.io → Email allow-list

---

## Deliverable 2 — brain.growdirect.io (Canary Retail Brain)

Currently at: https://growdirect-llc.github.io/canary-retail-brain/

### Step A — GitHub Pages custom domain
Repo growdirect-llc/canary-retail-brain → Settings → Pages → Custom domain → brain.growdirect.io
Tick "Enforce HTTPS" after DNS propagates. GitHub will create CNAME file in repo root.

### Step B — Cloudflare DNS
In growdirect.io zone, add:

  Type:   CNAME
  Name:   brain
  Target: growdirect-llc.github.io
  Proxy:  DNS only (grey cloud — required for GitHub Pages SSL cert validation)

### Access enforcement
Per Brain/projects/CanaryRetailBrain.md: Cloudflare Access is configured but not enforced — custom domain wiring is the prerequisite. Once brain.growdirect.io is live the Access gate activates on the existing whitelist.

---

## Deliverable 3 — catz.growdirect.io (CATz Method Vault)

Currently at: https://growdirect-llc.github.io/catz/

### Step A — GitHub Pages custom domain
Repo growdirect-llc/catz → Settings → Pages → Custom domain → catz.growdirect.io
Tick "Enforce HTTPS" after DNS propagates.

### Step B — Cloudflare DNS

  Type:   CNAME
  Name:   catz
  Target: growdirect-llc.github.io
  Proxy:  DNS only (grey cloud)

---

## Critical path check — is growdirect.io on Cloudflare DNS?

Check in Cloudflare dashboard → Websites. If growdirect.io is NOT there:
- Option A: Add site to Cloudflare, update nameservers at registrar — propagation 24-48h, risky for Monday
- Option B: Deploy proposal to Vercel (gets vercel.app URL immediately), add CNAME at registrar pointing to cname.vercel-dns.com. Share the vercel.app URL for Monday and wire the custom domain after.
- Option C: Share the pages.dev URL directly for Monday — no custom domain needed to run the demo

**Fastest path for Monday if DNS is uncertain: share armstrong-proposal.pages.dev — it works immediately.**

---

## Wrangler quick reference

```bash
wrangler whoami                      # confirm auth + account
wrangler pages list                  # list Pages projects
wrangler pages deploy /tmp/proposal-site --project-name=armstrong-proposal
wrangler pages deployment list --project-name=armstrong-proposal
```

---

## Verification checklist

- [ ] proposal.growdirect.io (or .pages.dev fallback) loads Armstrong_Proposal_v2.html — five plays visible, Canary Lawn & Garden OS, Play 4 VSM Goes Live
- [ ] brain.growdirect.io loads Canary Retail Brain Quartz site (13-module spine, platform articles, case studies)
- [ ] catz.growdirect.io loads CATz Method Vault (Phase I/II methodology, CBM v2, proof cases)
- [ ] All three HTTPS green
- [ ] brain + catz Cloudflare Access gates active (tim.mooney@maonach.com can auth through)
- [ ] Proposal URL ready to share to Armstrong contacts before Monday 1pm

---

## Related

- [[Brain/dispatches/2026-04-26-three-vault-jekyll-pages-architecture]] — three-vault architecture decision
- [[Brain/projects/CanaryRetailBrain]] — brain vault MOC (Access config, Cloudflare Access whitelist)
- [[Brain/projects/CATz]] — CATz vault MOC (Access config)
- Proposal source: /Users/gclyle/Desktop/Armstrong_Proposal_v2.html
