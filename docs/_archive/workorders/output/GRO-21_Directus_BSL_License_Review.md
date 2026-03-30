---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# GRO-21 — Directus BSL 1.1 License Review

**Issue:** GRO-21 (B-005)
**Prepared By:** ALX (Chief of Staff) — draft for Syd's legal opinion
**Date:** March 2, 2026
**Classification:** Internal — Legal Analysis Draft
**Gate:** Syd delivers formal opinion.
**Done When:** Legal opinion delivered — use or don't use.

---

## 1. Summary

Directus is a headless CMS and backend-as-a-service platform licensed under the **Business Source License 1.1 (BSL 1.1)**. It was relicensed from GPL v3 to BSL 1.1 in 2023. Canary LP is evaluating Directus as a potential admin panel / content management layer. This memo analyzes whether BSL 1.1 is compatible with GrowDirect's current and projected business profile.

---

## 2. BSL 1.1 — Key Terms

### 2.1 What BSL 1.1 Is

The Business Source License is a source-available (not open source) license created by MariaDB. Key characteristics:

- **Source code is publicly available** on GitHub — anyone can read, fork, and contribute
- **Production use requires a commercial license** for organizations above the revenue threshold
- **Time-based conversion:** On the Change Date (or 4th anniversary of each release, whichever is first), the code automatically converts to **GPL v2.0 or later** — becoming fully open source
- **Non-production use is unrestricted** — development, testing, evaluation, debugging are always free

### 2.2 The Revenue Threshold

Directus's "Additional Use Grant" in the BSL specifies:

> You may make production use of the Licensed Work, provided Your organization (including affiliates) has less than **$5,000,000 USD in total annual revenue and funding** in the prior fiscal year.

**Key definitions:**
- **"Total annual revenue and funding"** = all revenue streams + any investment/grant funding received
- **"Production use"** = any use other than development, debugging, testing, or evaluation
- **"Affiliates"** = entities that control, are controlled by, or under common control with your organization

### 2.3 What Requires a Commercial License

If your organization has **>$5M in total annual revenue + funding** AND is using Directus **in production**, you need a commercial license from Directus.

### 2.4 What Does NOT Require a Commercial License

- Organizations under $5M revenue+funding — fully free for all use including production
- Non-production use at any revenue level (dev, test, evaluation)
- Using unmodified object code (facilitating installation, updating, hosting)
- Academic and research use

---

## 3. GrowDirect Applicability

### 3.1 Current State

| Factor | GrowDirect Status |
|--------|------------------|
| Annual revenue | Pre-revenue (Canary LP not yet launched) |
| Total funding | Seed stage — **well under $5M** |
| Combined revenue + funding | **Under $5M threshold** |
| Planned use | Production (admin panel for Canary LP) |

**Current assessment: GrowDirect qualifies for the free production use grant.** No commercial license needed today.

### 3.2 Future State — When Does This Change?

The $5M threshold includes **funding**, not just revenue. This means:

| Scenario | Threshold Impact |
|----------|-----------------|
| Seed round closes at $2M | Still under $5M — no license needed |
| Series A at $5M+ | **Exceeds threshold** — commercial license required |
| Revenue reaches $5M+ (no funding) | **Exceeds threshold** — commercial license required |
| Revenue + funding combined exceed $5M | **Exceeds threshold** — commercial license required |

**Critical risk:** A successful fundraise could push GrowDirect over the $5M threshold immediately, requiring a commercial license for any Directus production use the next fiscal year.

### 3.3 Commercial License Cost

Directus's self-hosted pricing for organizations over $5M is not publicly listed — it requires contacting their Enterprise team. Based on market comparables for headless CMS enterprise licenses, expect $10,000-$50,000/year depending on usage scale.

---

## 4. Risk Analysis

### 4.1 Risks of Adopting Directus

| Risk | Severity | Likelihood | Notes |
|------|----------|------------|-------|
| **Fundraise triggers license obligation** | HIGH | HIGH | Series A will almost certainly exceed $5M threshold |
| **License terms change** | MEDIUM | LOW | BSL allows Directus to modify terms for future versions; existing versions are locked |
| **Vendor lock-in** | MEDIUM | MEDIUM | Migrating away from Directus after building admin panel on it is costly |
| **GPL conversion uncertainty** | LOW | LOW | Code converts to GPL v2+ after 4 years — but you'd be running on a 4-year-old version |
| **Audit/compliance burden** | LOW | LOW | Must track revenue + funding annually against threshold |

### 4.2 The Series A Problem

This is the core issue. GrowDirect's trajectory assumes a Series A raise. If that raise is $5M+ (which is typical), Directus production use immediately requires a commercial license. This creates a forced cost at exactly the moment you're deploying capital toward growth — not ideal.

**Mitigation options:**
1. Budget the commercial license into Series A planning
2. Choose a permissively-licensed alternative now (avoid the dependency entirely)
3. Use Directus for non-production only (dev/admin tooling, not merchant-facing)

---

## 5. Alternatives Comparison

| Tool | License | Production Use | Cost at Scale | Notes |
|------|---------|---------------|---------------|-------|
| **Directus** | BSL 1.1 | Free <$5M, paid above | $10-50K/yr est. | Best DX, but license risk |
| **Strapi** | MIT (Community) | Free, unlimited | $0 (self-hosted) | Permissive license, large community |
| **Payload CMS** | MIT | Free, unlimited | $0 (self-hosted) | TypeScript-first, newer but growing |
| **KeystoneJS** | MIT | Free, unlimited | $0 (self-hosted) | GraphQL-native, Prisma-based |
| **Nocodb** | AGPL v3 | Free with copyleft obligations | $0 (if compliant) | Same AGPL concerns as Grafana (GRO-22) |
| **Custom admin panel** | N/A | No license dependency | Dev cost only | Maximum control, maximum effort |

---

## 6. Recommendation

**For Syd's formal opinion, ALX recommends:**

1. **Do not adopt Directus for production use.** The BSL 1.1 $5M threshold is a ticking clock. GrowDirect will almost certainly exceed it at Series A, creating a forced commercial license obligation at a critical growth moment.

2. **If Directus is used at all**, restrict to non-production environments (internal dev tooling, prototyping). This is explicitly free under BSL regardless of revenue.

3. **Prefer MIT-licensed alternatives** for the admin panel / CMS layer. Strapi (MIT) or Payload CMS (MIT) provide similar functionality without license risk at any revenue level.

4. **If the team strongly prefers Directus**, budget $25-50K/year for the commercial license in Series A planning and negotiate terms before the raise closes.

---

## 7. Open Questions for Syd

1. **Does the $5M threshold include convertible notes and SAFEs?** The BSL says "revenue and funding" — does uncommitted/unconverted investment count?

2. **When exactly does the threshold apply?** "Prior fiscal year" — if GrowDirect raises $5M in Q1 2027, is the obligation triggered immediately or in FY2028?

3. **Is there risk in using Directus pre-threshold and migrating away post-threshold?** Could Directus claim ongoing production use if data/schemas created under the free grant persist in the production system?

4. **GPL v2 conversion clause** — after 4 years, BSL converts to GPL. Does this create a viable long-term strategy (wait for conversion), or is running a 4-year-old CMS version impractical?

---

## 8. Routing

- **Syd:** Deliver formal opinion — use or don't use. Focus on the fundraise trigger
- **Tom:** Assess Strapi vs Payload as alternatives if Directus is rejected
- **Jeremy:** Do not begin production Directus integration until Syd signs off

---

*ALX | GRO-21 | March 2, 2026*
