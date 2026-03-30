---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Work Order: Push GrowDirect Site to GitHub Pages

**From:** ALX
**To:** Jeremy (Code Tab)
**Priority:** URGENT — Jeffe wants to check from his phone NOW
**Date:** 2026-02-26
**Status:** READY TO EXECUTE

---

## TL;DR

Deploy package is fully staged at `growdirect-deploy/` in the workspace root. Everything is built — favicons, social cards, CNAME, meta tags, .gitignore, README. Just push it.

## Deploy Package Location

```
GrowDirect/growdirect-deploy/
├── index.html              ← landing page (bird + soundtrack + Jeffe's quote)
├── favicon.svg             ← bird icon
├── CNAME                   ← growdirect.io
├── README.md               ← patent-pending notice only
├── .gitignore              ← clean repo hygiene
└── assets/
    ├── brand/
    │   ├── apple-touch-icon.png
    │   ├── favicon-32.png
    │   └── favicon-192.png
    └── social/
        └── og-1200x630.png ← OpenGraph social share card
```

## Commands — Execute in Order

### Step 1: Init and push

```bash
cd growdirect-deploy
git init
git add -A
git commit -m "Initial site launch — patent pending, Feb 2026"
git branch -M main
git remote add origin https://github.com/growdirectprez/growdirectprez.github.io.git
git push -u origin main
```

If the repo `growdirectprez.github.io` doesn't exist yet, create it first:
- Go to github.com/new
- Repo name: `growdirectprez.github.io`
- Public
- No README (we have one)
- Create repository

### Step 2: Enable GitHub Pages

In repo Settings → Pages:
- Source: **Deploy from a branch**
- Branch: `main` / `/ (root)`
- Save

### Step 3: Verify

Site should be live within 60 seconds at:
**https://growdirectprez.github.io**

### Step 4: Custom Domain (GoDaddy DNS)

In GoDaddy DNS settings for growdirect.io:
- Delete existing A records pointing to GoDaddy hosting
- Add 4 A records:
  ```
  185.199.108.153
  185.199.109.153
  185.199.110.153
  185.199.111.153
  ```
- Add CNAME: `www` → `growdirectprez.github.io`
- **Do NOT touch MX records** — email stays on GoDaddy

Then in GitHub Pages settings:
- Custom domain: `growdirect.io`
- Enforce HTTPS: enable (after DNS propagates)

## What NOT to Push

- Nothing from `_ALX/`, `Canary/`, or `Canary_IP/`
- No internal team names in commits or files
- No `.env`, credentials, or API keys

## Audit Checklist

The deploy package has already been audited:
- [x] No internal agent names
- [x] No `_ALX/` references
- [x] No Canary IP leaks
- [x] og:image meta tags point to hosted assets
- [x] apple-touch-icon and favicon PNGs included
- [x] CNAME file set to growdirect.io
- [x] .gitignore blocks .DS_Store and node_modules

## Deliverables

1. ✅ Repo live at `github.com/growdirectprez/growdirectprez.github.io`
2. ✅ Site live at `growdirectprez.github.io`
3. ✅ Jeffe can view from phone
4. DNS instructions handed to Jeffe for GoDaddy custom domain step
