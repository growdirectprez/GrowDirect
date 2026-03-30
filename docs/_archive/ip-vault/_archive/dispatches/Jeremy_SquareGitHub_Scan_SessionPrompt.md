---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Jeremy Session Prompt — Square GitHub Repository Scan
**Work Order:** B-065-A
**Date:** February 28, 2026
**Dispatched by:** ALX
**Priority:** Medium
**Session type:** Research + Asset Acquisition

---

## Mission

Clone every relevant Square GitHub repository into a new `square/` directory on the local filesystem. Catalog everything. No analysis yet — acquisition first, then Jeremy knows exactly what Square has available when building TSP integrations.

---

## Target Directory

```
/Users/geofflyle/GrowDirect/Canary/square/
```

Create this directory. Everything goes here.

---

## Repositories to Clone

Clone ALL of the following. These are Square's official public repos relevant to our stack:

### Priority 1 — Clone immediately (directly relevant to TSP build)

```bash
cd /Users/geofflyle/GrowDirect/Canary/square

# Active Python SDK (what we use)
git clone https://github.com/square/square-python-sdk.git

# OAuth + webhook + payment code examples (Python OAuth flow is here)
git clone https://github.com/square/connect-api-examples.git

# OpenAPI spec — machine-readable schema for all Square APIs
git clone https://github.com/square/connect-api-specification.git
```

### Priority 2 — Clone for reference

```bash
# Deprecated Python SDK — keep for migration reference only
git clone https://github.com/square/connect-python-sdk.git

# Square's web payments SDK samples
git clone https://github.com/square/web-payments-quickstart.git

# Point of Sale SDK (iOS + Android — reference only)
git clone https://github.com/square/point-of-sale-ios-sdk.git
git clone https://github.com/square/point-of-sale-android-sdk.git
```

---

## After Cloning — Catalog

Once all repos are cloned, run this to generate a directory tree for ALX:

```bash
find /Users/geofflyle/GrowDirect/Canary/square -type f \
  \( -name "*.py" -o -name "*.md" -o -name "*.yaml" -o -name "*.json" \) \
  | sort > /Users/geofflyle/GrowDirect/Canary/square/SQUARE_ASSET_INDEX.txt

echo "Total files:" >> /Users/geofflyle/GrowDirect/Canary/square/SQUARE_ASSET_INDEX.txt
wc -l /Users/geofflyle/GrowDirect/Canary/square/SQUARE_ASSET_INDEX.txt >> \
  /Users/geofflyle/GrowDirect/Canary/square/SQUARE_ASSET_INDEX.txt
```

---

## Key Files to Note (Read These — Don't Implement Yet)

After cloning, open and read the following. Note anything relevant to TSP in your session log:

### OAuth flow (Python)
```
connect-api-examples/connect-examples/oauth/python/oauth-flow.py
```
This is Square's reference implementation for the OAuth authorization code flow in Python. This is the foundation for B-065-B (OAuth work order). Read it fully.

### Webhook validation (Python — v2)
```
square-python-sdk/README.md
```
Specifically the `verify_signature` section — this is the current SDK method we should be using in TSP-01 instead of manual HMAC computation.

### Templates directory
```
connect-api-examples/templates/
```
Square provides reusable code blocks here. Scan all of them. List any that apply to payments, webhooks, OAuth, or refunds.

---

## Deliverable

Create this file when done:

```
/Users/geofflyle/GrowDirect/Canary/square/SQUARE_SCAN_NOTES.md
```

Contents:
1. List of every repo cloned with clone status (success/failed)
2. Notable files relevant to TSP-01 through TSP-06
3. Notable files relevant to OAuth (for B-065-B)
4. Anything surprising — Square features, SDK capabilities, or patterns we aren't currently using
5. Any SDK version discrepancies vs. what's in `requirements.txt`

---

## Standing Directives

- Do NOT modify any existing Canary code during this session
- Do NOT import or integrate anything yet — acquisition and cataloging only
- B-063 reminder: confirm `squareup` SDK version in `requirements.txt` vs. latest in cloned repo
- Flag any deprecated patterns we're currently using in Canary vs. the current SDK

---

## Session Close

Update HANDOFF.md: Square scan complete, SQUARE_ASSET_INDEX.txt and SQUARE_SCAN_NOTES.md written to `/Canary/square/`. Flag any SDK version gaps for ALX review.

---

*ALX | February 28, 2026 | B-065-A*
