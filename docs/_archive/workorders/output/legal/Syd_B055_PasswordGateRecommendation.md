---
type: legal
domain: business
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Password Gate — Recommendation Memo
*Prepared by: Syd (Legal Counsel) | February 27, 2026*
*Classification: Attorney-Client Privileged*
*Reference: DISPATCH_Syd_IPExposureAudit.md (B-055)*

---

## Current State

The investor briefing site (`growdirect_investor_1.html`) uses client-side JavaScript password protection:

```javascript
// Simplified version of what's in the file:
if (input === 'eljeffe2026') {
  gate.style.display = 'none';
  content.style.display = 'block';
}
```

**Vulnerabilities:**
1. Password is a plaintext string in the source code — visible via View Source
2. The protected content is in the DOM (hidden with CSS `display:none`) — accessible via browser DevTools without any password
3. No server-side validation — the "gate" is entirely cosmetic
4. No access logging — no way to know who accessed, when, or how many times
5. Single shared password — no per-investor credentials, no revocation

---

## Recommendation

### For the Current Investor Site (v1) — ACCEPTABLE with NDA

The current content behind the gate is moderate sensitivity (business model summary, competitive positioning). It does NOT contain MAXIMUM CONFIDENTIAL material (Chirp rules, CRDM schema, implementation details).

**Recommendation:** Keep the current JS gate for v1, BUT:
- Every person who receives the URL MUST sign the Merchant NDA first
- The NDA provides the actual protection, not the password gate
- The gate's purpose is to prevent casual browsing, not to resist determined access
- This is sufficient for the current content level

### For the Expanded Investor Site (v2 / B-054) — UPGRADE REQUIRED

B-054 will contain PhD investment thesis briefs, business model details, IP protection strategy summaries, and compliance positioning. This is MAXIMUM CONFIDENTIAL material.

**Client-side JS gate is NOT sufficient for this content.**

### Gate Options (Ranked)

| Option | Mechanism | Cost | Complexity | Security Level |
|---|---|---|---|---|
| **A. Cloudflare Access** | Cloudflare's Access product — email-based authentication. Visitor enters email, receives one-time code, gains access. No password to share or leak. Per-user access control. Audit log built in. | Free tier (up to 50 users) or $7/user/mo | LOW — Cloudflare already manages our domains. 15-minute setup. | 🟢 HIGH |
| **B. HTTP Basic Auth (server-side)** | Cloudflare Worker or Pages function validates credentials server-side before serving content. Password never in client code. | Free (Cloudflare Workers free tier) | MEDIUM — requires writing a small Cloudflare Worker function | 🟡 MEDIUM |
| **C. Unique URL tokens** | Generate per-investor unique URL (e.g., `investor.growdirect.io/abc123xyz`). Token mapped to investor identity. Track access. Revocable. | Free (Cloudflare Workers) | MEDIUM — requires token management code | 🟡 MEDIUM |
| **D. Netlify/Vercel password protection** | Built-in site-level password protection. Server-side. | Netlify Pro ($19/mo) or Vercel Pro ($20/mo) | LOW — one setting toggle | 🟡 MEDIUM |
| **E. Keep JS gate + NDA** | Status quo. Rely on contractual protection (NDA) rather than technical protection. | $0 | ZERO | 🔴 LOW |

### Syd's Recommendation: Option A — Cloudflare Access

**Why:**
1. **Already on Cloudflare.** All 7 domains are managed there. No new vendor relationship.
2. **Free tier covers our use case.** Up to 50 authenticated users at no cost.
3. **Email-based auth.** No passwords to share, leak, or find in source code. The investor receives an email with a one-time code. The code expires.
4. **Per-user access control.** We can add/remove individual investors. Revocation is instant.
5. **Audit trail.** Cloudflare logs every access — who, when, from where. This is evidence if we ever need to prove an investor violated their NDA.
6. **15-minute setup.** Jeremy or even Jeffe can configure this in the Cloudflare dashboard.
7. **The site stays as a single HTML file.** No backend changes. Cloudflare Access sits in front of the URL and authenticates before the content loads.

**Implementation:**
1. Deploy `growdirect_investor_v2.0.html` to Cloudflare Pages (or as a static file on any Cloudflare-proxied domain)
2. In Cloudflare dashboard → Zero Trust → Access → Create Application
3. Set policy: "Allow — emails ending in [specific investor emails]" or "Allow — one-time pin to any email"
4. Done. The content is now behind server-side authentication with per-user audit trail.

---

## Additional Recommendations

### Should growdirect.io Landing Page Content Be Reduced?

**No.** The landing page is well-crafted and discloses no trade secrets. The patent is filed. The content supports market recognition and first-mover positioning. Reducing it would hurt the business without improving IP protection.

### Should Any GitHub Repos Be Made Private?

**They already are.** The `growdirectprez/growdirect.io` repo returns 404 to unauthenticated requests. Confirm in GitHub settings that all repos under this account are explicitly set to PRIVATE (not just "internal" or "visible to organization").

**Action item:** Jeffe or Jeremy — log into GitHub, go to Settings → Repositories, confirm every repo shows "Private."

### WHOIS Privacy

**Already handled.** Cloudflare Registrar enables WHOIS privacy by default for all domains. No action required.

### Immediate Actions Before Attorney Call

1. **None required for takedown.** Nothing needs to come down.
2. **Confirm GitHub is private.** 2-minute check in GitHub dashboard.
3. **Read the IP Exposure Summary** (Deliverable 1) for full context.
4. **Read the Attorney Call Talking Points** (Deliverable 2) — use as your script on the call.

---

*Syd | Legal Counsel | GrowDirect*
*February 27, 2026*
*Attorney-Client Privileged*
