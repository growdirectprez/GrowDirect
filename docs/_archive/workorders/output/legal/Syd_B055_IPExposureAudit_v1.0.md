---
type: legal
domain: business
status: active
created: 2026-03-18
updated: 2026-03-19
---
# IP Exposure Audit — Summary Report
*Prepared by: Syd (Legal Counsel) | February 27, 2026*
*Classification: Attorney-Client Privileged*
*Triggered by: Jeffe directive — "I am afraid I have too much exposed on the GrowDirect web"*
*Reference: DISPATCH_Syd_IPExposureAudit.md (B-055)*

---

## EXECUTIVE SUMMARY

**Bottom line: GrowDirect's public exposure is minimal.** The IP is largely safe. The public-facing landing page is well-constructed — it describes WHAT the system does without disclosing HOW it does it. The password-gated investor site is more detailed but behind a gate. The primary risks are the password gate mechanism (client-side JS — easily bypassed) and one area of the landing page that approaches technical specificity. No emergency takedown required, but two items need attention before the attorney call.

---

## 1. PUBLIC WEB PRESENCE — WHAT'S EXPOSED

### 1.1 growdirect.io Landing Page

**Source:** `_ALX/WorkOrders/output/Art/growdirect-site/index.html`
**Deployment status:** In git repo (`growdirectprez/growdirect.io`). Domain is on Cloudflare. Whether actually deployed and live is unconfirmed — web search returns zero results for "growdirect.io" and the domain may not yet be resolving to content.

**Content review:**

| Content Element | IP Risk | Rating |
|---|---|---|
| Company name "GrowDirect" + "Universal Event Notarization on Bitcoin" tagline | Generic — describes what, not how | 🟢 GREEN |
| "Capture. Seal. Inscribe." messaging | Marketing language — no implementation detail | 🟢 GREEN |
| 6-node pipeline visual (Event → Gateway → Queue → Seal → Route → Inscribe) | **Describes the pipeline structure.** Names 6 stages with timing ("T+0ms", "T+15ms"). This mirrors the patent claim architecture. | 🟡 YELLOW |
| Three Guarantees (Real-Time Capture, Cryptographic Seal, Bitcoin Inscription) | High-level descriptions. Mentions "write-once evidence store" and "Merkle trees" and "Ordinals." | 🟡 YELLOW |
| Stats (536 tests, 0 failures, 9 patent claims, 22 immutability triggers) | The "9 patent claims" number is fine (public in the patent itself). "22 immutability triggers" is specific enough to signal architecture sophistication but not exploitable. | 🟢 GREEN |
| Why Bitcoin section (17+ years uptime, etc.) | Generic Bitcoin advocacy — no IP exposure | 🟢 GREEN |
| Industries section (Retail, Healthcare, Supply Chain, Legal, Insurance, Government) | Use case list — no IP exposure. Mentions "Canary LP" as beachhead. | 🟢 GREEN |
| Patent Pending badge ("Application 63/991,596") | **Correct practice.** Patent number is public record. Claiming "Patent Pending" is legally appropriate and encouraged. | 🟢 GREEN |
| "hello@growdirect.io" contact email | Low risk — standard practice | 🟢 GREEN |
| Founder quote — "If it happened, you should be able to prove when." | No IP exposure | 🟢 GREEN |
| Animated Canary bird with chirp sound + health-wave animation | Brand asset — no IP exposure. Detailed SVG animation code is visible in source but is creative expression, not trade secret. | 🟢 GREEN |

**Assessment:** The landing page is well-crafted. It communicates value without exposing mechanism. **Two YELLOW items:**

1. **Pipeline visual** — The 6-node pipeline (Event → Gateway → Queue → Seal → Route → Inscribe) with timing annotations ("T+0ms", "T+15ms") mirrors the six-node architecture described in the patent provisional. While the patent is filed and this creates no *patent* risk (you WANT to describe the invention), it does expose the pipeline structure to anyone viewing the page. A competitor could see the architecture pattern without reading the patent filing.

   **Recommendation:** KEEP as-is. The pipeline visual is intentional marketing. The patent is filed (63/991,596). The 12-month provisional window is running. Disclosing the architecture on the landing page is consistent with the business strategy of establishing first-mover recognition. The landing page does NOT disclose thresholds, Chirp rules, CRDM schema, or implementation details.

2. **"Merkle trees" + "Ordinals" mention** — The Three Guarantees section mentions "batched into Merkle trees" and "inscribed as Ordinals." These are accurate but technical. They tell a sophisticated reader how the inscription batching works.

   **Recommendation:** KEEP. These are established Bitcoin concepts. The novelty is in the combination (covered by patent), not in using Merkle trees per se.

### 1.2 GitHub Repository

**Repo:** `github.com/growdirectprez/growdirect.io`
**Status: NOT PUBLICLY ACCESSIBLE.** Returns 404 to unauthenticated requests. Either the repo is set to PRIVATE or the account/repo path has changed.

| Check | Result | Rating |
|---|---|---|
| Repo publicly visible? | NO — 404 | 🟢 GREEN |
| Source code exposed? | NO | 🟢 GREEN |
| README/docs visible? | NO | 🟢 GREEN |

**Recommendation:** Confirm repo is explicitly set to PRIVATE in GitHub settings (not just "not found"). If there are any other repos under the `growdirectprez` account, verify ALL are private. The `growdirectprez` GitHub profile page also returns 404 — meaning the account may be set to private entirely.

### 1.3 Domain Registrations (Cloudflare)

**Domains secured (per B-038):**
1. eljeffe.io (primary API)
2. eljeffe.org
3. eljeffe.wtf
4. eljeffe.dev
5. eljeffebtc.com (foundation umbrella)
6. jeffe.io (personal brand / short-form)
7. growdirect.app (parent company)

**WHOIS Privacy:**

Cloudflare Registrar automatically enables WHOIS privacy (redacted contact data) for all domains registered through their service. This is default behavior — no manual configuration required. Cloudflare replaces registrant name, address, email, and phone with redacted placeholders in WHOIS records.

| Check | Result | Rating |
|---|---|---|
| WHOIS privacy enabled (Cloudflare default)? | YES (automatic) | 🟢 GREEN |
| Registrant name exposed? | NO (Cloudflare redacts) | 🟢 GREEN |
| Personal email/phone exposed? | NO | 🟢 GREEN |

**Recommendation:** No action needed. Cloudflare's default WHOIS privacy is sufficient.

### 1.4 Google Index — What's Discoverable?

**Searches performed:**
- `"GrowDirect"` — No relevant results
- `"Canary LP"` — No relevant results (unrelated canary/warrant discussion on BitcoinTalk from 2015)
- `"growdirect.io"` — No results
- `"El Jeffe" notarization Bitcoin` — No relevant results

| Check | Result | Rating |
|---|---|---|
| GrowDirect indexed by Google? | NO | 🟢 GREEN |
| Any investor materials indexed? | NO | 🟢 GREEN |
| Any technical content indexed? | NO | 🟢 GREEN |
| Internal team member names indexed? | NO | 🟢 GREEN |

**Assessment:** Zero public footprint. If growdirect.io is deployed, Google has not yet crawled it (or it is too new to be indexed). This is ideal from an IP perspective.

---

## 2. PASSWORD-GATED CONTENT — WHAT'S BEHIND THE GATE

### 2.1 `growdirect_investor_1.html`

**Gate type:** Client-side JavaScript password check
**Password:** `eljeffe2026`
**Gate mechanism:** JavaScript compares user input to hardcoded string. Content div is hidden behind `display:none` and revealed on correct password.

**Content behind the gate:**

| Section | Content | IP Sensitivity |
|---|---|---|
| 01 — The Problem | "The Record Is Broken" — Polling gaps, mutable records, trust required | LOW — general industry critique |
| 02 — The Solution | "Capture. Seal. Inscribe." — 6-node pipeline + 4 competitive moat cards | MEDIUM — pipeline architecture + moat framing |
| 03 — The Economy | Closed-loop SVG diagram + 4 ownership tiers | HIGH — business model specifics |
| 04 — The Market | Beachhead stats + competitive comparison | MEDIUM — market positioning |
| 05 — The Vision | 6 use cases (universal protocol) | LOW — general vision |
| 06 — What's Built | Metrics + checklist + protection cards | MEDIUM — specific product metrics |

**Gate assessment:**

| Risk | Severity | Detail |
|---|---|---|
| Password visible in source code | 🔴 HIGH | Anyone can View Source → search for password comparison → find `eljeffe2026` |
| Content accessible without password | 🔴 HIGH | The full HTML content is in the DOM (just hidden). Browser DevTools → Elements → change `display:none` to `display:block`. No password needed. |
| No server-side protection | 🔴 HIGH | There is no server validating the password. The "gate" is cosmetic only. |
| Password shared across all viewers | 🟡 MEDIUM | Single password for all investors. No tracking of who accessed. No revocation capability. |

**Risk Rating: 🔴 RED for gate sufficiency. 🟡 YELLOW for content sensitivity.**

The content behind the gate is investor-facing summary material. It does NOT contain:
- Chirp rule thresholds or detection logic
- CRDM schema specifics
- Lightning/L402 fee architecture implementation details
- Internal team member names or agent roles
- SysRepublic, Appriss, or former employer references
- Patent claim details beyond "Patent Pending"

**However:** The economy section describes the business model (closed-loop ownership tiers), and the competitive moat cards describe the strategic positioning in enough detail that a competitor could learn the strategy.

### 2.2 Expanded Investor Site (B-054, planned)

**Status:** Not yet built. Work order written. Will use same client-side JS gate mechanism unless upgraded.

**Planned content sensitivity:** HIGHER than v1. Will include:
- PhD investment thesis briefs (Block Space Moat, Genesis Pool, VeriSign Parallel, Vertical Integration)
- Compliance by Construction section (B-053)
- Protection section (patent pending + IP layers)

**This content is MAXIMUM CONFIDENTIAL.** Client-side JS password gate is insufficient for this material.

---

## 3. INTERNAL ONLY — CROSS-REFERENCE CHECK

Cross-referenced against IP Protection Strategy v1.0 and patent assessment:

| Protected Item | Exposed Publicly? | Exposed Behind Gate? | Action Required? |
|---|---|---|---|
| Chirp rule thresholds / detection logic | NO | NO | None |
| CRDM schema specifics | NO | NO | None |
| Lightning/L402 fee architecture details | NO | NO (economy section is high-level only) | None |
| Internal team member names / agent roles | NO | NO | None |
| SysRepublic / Appriss / former employer references | NO | NO | None |
| Patent claims beyond "Patent Pending" | NO (patent # is public record) | NO | None |
| 6-node pipeline architecture | YES (landing page) | YES (investor site) | Acceptable — patent filed |
| Business model (ownership tiers, closed-loop) | NO | YES (behind gate) | Gate upgrade recommended |
| Competitive moat framing | NO | YES (behind gate) | Acceptable — investor context |

---

## 4. OVERALL RISK RATINGS

| Asset | Risk Rating | Action |
|---|---|---|
| growdirect.io landing page | 🟢 GREEN | Keep as-is. Well-crafted. No IP leakage. |
| GitHub repos | 🟢 GREEN | Confirm all repos set to PRIVATE explicitly. |
| Domain WHOIS | 🟢 GREEN | Cloudflare privacy is automatic. No action. |
| Google index | 🟢 GREEN | Nothing indexed. Ideal. |
| Investor site v1 (gate) | 🔴 RED (gate) / 🟡 YELLOW (content) | Gate is trivially bypassable. Content is moderate sensitivity. Upgrade gate before sharing with anyone outside trusted circle. |
| Investor site v2 (planned) | 🔴 RED (gate) | MUST upgrade gate before deployment. Client-side JS is insufficient for MAXIMUM CONFIDENTIAL content. |

---

## 5. IMMEDIATE RECOMMENDATIONS

### Before the Attorney Call Today

1. **No emergency takedown needed.** The landing page is clean. Nothing needs to come down.

2. **Tell the attorney:** The provisional patent (63/991,596) was filed Feb 26, 2026. The landing page describes the system at a marketing level consistent with establishing first-mover recognition. No implementation details are exposed. The 6-node pipeline visual matches the patent architecture but does not disclose the novel combination elements (triple subscriber isolation, bilateral verification, raw payload hashing, Merkle batching specifics).

3. **Tell the attorney about the gate:** The investor briefing site uses client-side JavaScript password protection. It is trivially bypassable. Ask whether this matters for prior art analysis if the URL is shared with investors under NDA.

### Before Any Investor Sees B-054

4. **Upgrade the password gate.** See Deliverable 3 (Password Gate Recommendation) for options.

5. **Every investor who receives the URL must sign the Merchant NDA first.** The NDA is already delivered (Syd_MerchantNDA_v1.0.md). This provides contractual protection even if the technical gate is weak.

---

*Syd | Legal Counsel | GrowDirect*
*February 27, 2026*
*Attorney-Client Privileged — Do Not Distribute*
