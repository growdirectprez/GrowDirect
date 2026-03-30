---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# DISPATCH: Syd — Same-Day IP Exposure Audit
*Issued by: ALX | February 27, 2026 | Priority: 🔴 URGENT — Same Day*
*Classification: Attorney-Client Privileged*
*Triggered by: Jeffe directive — "I am afraid I have too much exposed on the GrowDirect web"*

---

## Directive

Jeffe wants to call the patent attorney TODAY. Before that call, he needs a clear picture of what's currently exposed publicly vs. what's behind gates. Syd delivers talking points for the attorney call.

---

## Audit Scope

### 1. Public Web Presence — What's Exposed?

Audit these assets for IP exposure:

| Asset | Location | Status |
|---|---|---|
| growdirect.io landing page | `_ALX/WorkOrders/output/Art/growdirect-site/index.html` (in git, potentially deployed) | Review for any trade secret or architecture disclosure |
| GitHub repos | `github.com/growdirectprez/growdirect.io` | Audit: is repo public or private? What's visible? |
| Domain registrations | 7 domains on Cloudflare (see B-038) | WHOIS privacy enabled? |
| Any other public content | Google "GrowDirect" + "Canary LP" + "El Jeffe" | What's indexed? |

### 2. Password-Gated Content — What's Behind the Gate?

| Asset | Gate Type | Risk Assessment |
|---|---|---|
| `growdirect_investor_1.html` | Client-side JS password (`eljeffe2026`) | Syd assesses: is this sufficient? Anyone can view-source to bypass. |
| Expanded investor site (B-054, planned) | Same gate mechanism | Recommend: keep or upgrade? |

### 3. Internal Only — What Must NEVER Be Public?

Cross-reference against Syd's existing IP Protection Strategy (v1.0) and flag anything that:
- Exposes Chirp rule thresholds or detection logic
- Reveals CRDM schema specifics
- Describes the Lightning/L402 fee architecture in implementation detail
- Names internal team members or agent roles
- References SysRepublic, Appriss, or former employer lineage
- Exposes patent claims beyond "Patent Pending"

---

## Deliverables

### Deliverable 1: IP Exposure Summary (1 page)
**Format:** Markdown → Jeffe reads it before the attorney call
**Content:**
- What's currently exposed publicly (with URLs)
- What's behind password gates
- What needs to come down immediately (if anything)
- What's safe to keep up
- Risk rating: RED / YELLOW / GREEN for each asset

### Deliverable 2: Attorney Call Talking Points (half page)
**Format:** Bullet list — Jeffe reads from this on the call
**Content:**
- Patent provisional status (63/991,596, filed Feb 26 2026)
- What's been publicly disclosed (from Deliverable 1)
- Questions for attorney:
  - Does our public landing page create prior art issues?
  - Is client-side password protection sufficient for gated investor content?
  - Timeline recommendation for utility filing given current public exposure
  - Any immediate takedown recommendations?
- What we're building next (expanded investor site behind password gate)
- What we need from counsel (scope of engagement, retainer, timeline)

### Deliverable 3: Recommendation Memo
**Format:** Short legal memo
**Content:**
- Should the growdirect.io landing page content be reduced?
- Should any GitHub repos be made private (if public)?
- Password gate: client-side JS vs. server-side auth — recommendation
- WHOIS privacy audit results
- Any immediate actions before the attorney call

---

## Output Location

All deliverables to: `_ALX/WorkOrders/output/Syd/`
- `Syd_B054_IPExposureAudit_v1.0.md`
- `Syd_B054_AttorneyCallTalkingPoints.md`
- `Syd_B054_PasswordGateRecommendation.md`

---

## Context Files (Syd reads these first)

1. `_ALX/WorkOrders/output/Syd/Syd_IP_Protection_Strategy_v1.0.md` — existing IP strategy
2. `_ALX/WorkOrders/output/Syd/Syd_PatentAssessment_StagedImmutability_v1.0.md` — patent assessment
3. `_ALX/WorkOrders/output/Art/growdirect-site/index.html` — current public landing page
4. `/mnt/uploads/growdirect_investor_1.html` — current password-gated investor site
5. `_ALX/WorkOrders/WORKORDER_B054_InvestorBriefingSite.md` — expanded site plan

---

## Timeline

**TODAY.** Jeffe wants to call the attorney. Syd delivers before that call happens.

---

*ALX | Chief of Staff | February 27, 2026*
*This is a same-day dispatch. Do not queue behind B-053 sequential gate.*
