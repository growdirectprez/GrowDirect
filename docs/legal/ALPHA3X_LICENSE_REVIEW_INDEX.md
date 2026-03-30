---
type: legal
domain: business
status: active
created: 2026-03-19
updated: 2026-03-19
---
# Canary LP / GrowDirect
## Alpha 3X Stack License Review — Complete Package

**DATE:** February 21, 2026
**PREPARED FOR:** Syd (Legal Counsel), Jeremy (Developer Quant)
**TOTAL DOCUMENTS:** 3
**TOTAL PAGES:** ~45 (equivalent)

---

## DOCUMENT INDEX

### 1. **Executive Summary** (For Quick Decision-Making)
**FILE:** `Canary_Alpha3X_License_Executive_Summary.md` (6.4 KB)

**AUDIENCE:** Syd, Jeffe, Eva (decision-makers)

**CONTENTS:**
- Three-item risk summary table
- Yellow/Red risk breakdown for each component
- One-page action items for Syd and Jeremy
- Open-source license decision framework (GPL-3.0 vs. Apache-2.0)
- To-do list by deadline

**READ TIME:** 5 minutes

**KEY TAKEAWAY:** Redis is RED risk (must fix). Directus and Grafana are YELLOW (manageable).

---

### 2. **Legal Brief (Detailed Analysis)**
**FILE:** `Canary_Alpha3X_License_Review_Brief_Syd_v1.0.md` (27 KB, 522 lines)

**AUDIENCE:** Syd (primary), legal review, compliance team

**CONTENTS:**
- Executive summary with risk ratings
- Item 1: Directus BSL-1.1 analysis (revenue thresholds, GPL conversion, open-source implications)
- Item 2: Redis RSALv2/SSPLv1 analysis (SaaS restrictions, Valkey alternative, drop-in replacement)
- Item 3: Grafana AGPL-3.0 analysis (network use clause, unmodified use compliance, alternatives)
- Overall platform architecture license summary
- Implications for Canary's open-source strategy
- Legal review checklist
- Risk summary table
- Next steps by owner
- Full appendices with license text references

**READ TIME:** 20-30 minutes

**LEGAL STANDARD:** Attorney-client privileged communication; suitable for external legal counsel review if needed

**KEY DETAILS:**
- Directus $5M revenue threshold explained
- RSALv2/SSPLv1 ambiguity for SaaS detailed with court precedent discussion
- AGPL-3.0 "viral" license risk explained with mitigation strategies
- Complete references to source licenses and FAQs

---

### 3. **Technical Migration Guide**
**FILE:** `Canary_Redis_to_Valkey_Migration_Guide.md` (10 KB)

**AUDIENCE:** Jeremy (Developer Quant), ops team

**CONTENTS:**
- Why migrate (license risk explained in technical terms)
- Step-by-step migration checklist (8 steps, 4-5 hours total effort)
- Specific code changes for each component (requirements.txt, Docker Compose, etc.)
- Verification procedures (test suite, Celery verification, CLI tests)
- Compatibility matrix (100% API-compatible)
- Testing scenarios with expected results
- Rollback plan (if issues arise)
- Signoff checklist
- Q&A section
- Implementation timeline

**READ TIME:** 15-20 minutes (implementation-focused)

**TECHNICAL STANDARD:** Ready for immediate engineering action

**KEY POINTS:**
- Zero code changes required (Valkey is 100% Redis-compatible)
- 2-4 hours effort
- All existing data works without migration
- Full test suite expected to pass unchanged

---

## HOW TO USE THIS PACKAGE

### Scenario A: Syd Needs to Approve Alpha 3X Platform Rehydration

1. **Read:** Executive Summary (5 min)
2. **Decide:** Approve or request changes on the three components
3. **Action:** Forward Executive Summary to Jeffe with your recommendation
4. **Refer to:** Legal Brief (27 KB) if Jeffe asks detailed questions

### Scenario B: Jeremy Needs to Fix Redis Risk Immediately

1. **Read:** Migration Guide (15 min)
2. **Do:** Follow the 8-step checklist (4-5 hours)
3. **Verify:** Run test suite; confirm Celery works
4. **Commit:** Push changes to GitHub
5. **Notify:** Syd that risk is now GREEN

### Scenario C: Syd Needs to Brief Legal Team (External Counsel)

1. **Provide:** Legal Brief (Canary_Alpha3X_License_Review_Brief_Syd_v1.0.md)
2. **Note:** Attorney-client privileged communication
3. **Include:** Risk ratings and recommendations
4. **Question focus:** Directus April 2026 conversion; Redis SaaS enforceability; Grafana modification risk

### Scenario D: Jeffe Needs to Decide Open-Source License (Critical Path)

1. **Read:** Executive Summary section "CRITICAL DECISION FOR JEFFE + SYD"
2. **Options:** GPL-3.0 (aligns with stack) vs. Apache-2.0 (requires component replacement)
3. **Timeline:** Decide by March 31, 2026
4. **Refer to:** Legal Brief sections on each component's open-source implications

---

## RISK SUMMARY (ONE PAGE)

| Item | Component | Risk | Action | Owner | Deadline |
|------|-----------|------|--------|-------|----------|
| 1 | Directus 11 Admin Panel | 🟨 YELLOW | Approve; decide open-source license | Syd + Jeffe | Mar 31, 2026 |
| 2 | Redis Cache/Broker | 🔴 RED | Replace with Valkey (BSD-3) | Jeremy | Feb 28, 2026 |
| 3 | Grafana Monitoring | 🟨 YELLOW | Approve (unmodified); document safeguards | Syd | Before alpha sign-off |

**Status:** Two items approved with conditions. One item (Redis) requires immediate fix before Alpha 3X can proceed.

---

## KEY DATES & DEADLINES

| Date | Action | Owner | Document |
|------|--------|-------|----------|
| **Feb 28, 2026** | Redis → Valkey migration complete | Jeremy | Migration Guide |
| **Mar 31, 2026** | Directus open-source license decision | Jeffe + Syd | Legal Brief + Exec Summary |
| **Apr 26, 2026** | Directus BSL → GPL-3.0 automatic conversion | (Monitoring) | Legal Brief |
| **Before Alpha Sign-Off** | Grafana governance rules documented | Syd | Executive Summary |

---

## RECOMMENDATIONS AT A GLANCE

✅ **APPROVE IMMEDIATELY:**
- Directus 11 (internal admin use, <$5M threshold)
- Grafana (unmodified deployment, internal monitoring)

❌ **BLOCK ALPHA 3X SIGN-OFF UNTIL FIXED:**
- Redis 7.2 (replace with Valkey 8.0; effort: 4-5 hours)

⏰ **DECIDE BY MARCH 31:**
- Canary's intended open-source license (GPL-3.0 vs. Apache-2.0) — drives Directus/Grafana strategy

---

## SUPPORTING RESEARCH

All claims are sourced from:
- Official license texts and FAQs
- Vendor documentation (Directus, Redis, Grafana)
- Linux Foundation Valkey project
- OSI Open Source License definitions
- Legal precedent on AGPL enforceability (where applicable)

**Full citations:** See Legal Brief appendices and inline source links

---

## QUESTIONS?

**For Syd:**
- Directus revenue threshold interpretation?
- AGPL modification risk?
- Open-source license implications?
→ See Legal Brief sections 1-3 and appendices

**For Jeremy:**
- How do I migrate Redis to Valkey?
- Will my tests pass unchanged?
- What's the rollback plan?
→ See Migration Guide (step-by-step)

**For Jeffe:**
- What's the legal impact of my "completely open source" commitment?
- Which open-source license should Canary use?
- Do I need to budget for commercial licenses?
→ See Executive Summary "Critical Decision" section + Legal Brief "Implications for Canary's Open-Source Strategy"

---

## DOCUMENT VERSIONS

| Document | Version | Date | Status |
|----------|---------|------|--------|
| Executive Summary | v1.0 | Feb 21, 2026 | Ready for use |
| Legal Brief | v1.0 | Feb 21, 2026 | Ready for legal review |
| Migration Guide | v1.0 | Feb 21, 2026 | Ready for engineering |

**All documents are confidential — Canary LP / GrowDirect internal use only.**

---

## NEXT STEPS

1. **Syd:** Read Executive Summary (5 min); forward to Jeffe with recommendation
2. **Jeffe:** Decide open-source license (GPL-3.0 vs. Apache-2.0) by March 31
3. **Jeremy:** Begin Redis → Valkey migration immediately (Est. 4-5 hours; deadline Feb 28)
4. **Team:** No coding on other Alpha 3X features until Redis risk is mitigated (GREEN)
5. **All:** Update project documentation once decisions are final

---

*For questions about this package, contact Syd (Legal Counsel).*

*Confidential — Canary LP / GrowDirect. All rights reserved.*
