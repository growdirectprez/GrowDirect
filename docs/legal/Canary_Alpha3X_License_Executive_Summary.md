---
type: legal
domain: business
status: active
created: 2026-03-19
updated: 2026-03-19
---
# CANARY LP / GROWDIRECT
## Alpha 3X Stack License Review — Executive Summary

**DATE:** February 21, 2026
**PREPARED FOR:** Syd (Legal Counsel)
**STATUS:** Ready for approval

---

## THREE-ITEM LICENSE REVIEW: QUICK SUMMARY

| # | Component | License | Risk | Action | Timeline |
|---|-----------|---------|------|--------|----------|
| **1** | Directus 11 Admin Panel | BSL-1.1 → GPL-3.0 | 🟨 YELLOW | Approve; decide open-source license by Mar 31 | Before public launch |
| **2** | Redis Cache/Broker | RSALv2/SSPLv1 | 🔴 RED | Replace with Valkey (BSD-3) | By Feb 28, 2026 |
| **3** | Grafana Monitoring | AGPL-3.0 | 🟨 YELLOW | Approve (unmodified only); implement safeguards | Before alpha sign-off |

---

## DIRECTUS (Item 1) — 🟨 YELLOW RISK

**The Issue:** BSL-1.1 converts to GPL-3.0 automatically on April 26, 2026.

**Why It's Yellow, Not Red:**
- ✅ Directus is internal-only (ops team, not merchants)
- ✅ BSL 1.1 explicitly permits SaaS internal use <$5M revenue
- ✅ Merchant-facing exposure: zero

**The Catch:** If Canary exceeds $5M in annual revenues (all sources), a commercial license becomes required. If Canary open-sources under Apache-2.0 or MIT, GPL-3.0 dependencies create legal friction.

**What Syd Needs to Do:**
1. Confirm GrowDirect is <$5M (likely yes, but verify)
2. Decide by March 31: Is Canary's open-source license GPL-3.0 or Apache-2.0?
   - If GPL-3.0: No action needed; April conversion is seamless
   - If Apache-2.0: Must replace Directus before April 2026

**Bottom Line:** ✅ **APPROVED for Alpha 3X**. Add calendar reminder for March 31 decision.

---

## REDIS (Item 2) — 🔴 RED RISK

**The Issue:** Redis 7.2 licenses changed in March 2024 to RSALv2 + SSPLv1 (not OSI-approved; ambiguous for SaaS).

**Why It's Red:**
- ❌ RSALv2 restricts commercialization; unclear if SaaS qualifies
- ❌ SSPLv1 requires releasing "management layers" if offered as service; ambiguous what that means
- ❌ No court precedent; license enforceability is untested
- ❌ Linux distributions dropped Redis; industry consensus: these licenses are problematic
- ❌ If Canary open-sources, Redis licensing ambiguity creates legal liability

**The Fix:** Replace with **Valkey** (Linux Foundation fork, BSD-3-Clause license)
- ✅ 100% API-compatible drop-in replacement
- ✅ Backed by AWS, Google Cloud, Oracle, Ericsson
- ✅ Zero code changes needed; configuration only
- ✅ Same performance, same reliability, zero risk
- ✅ Clear BSD-3 licensing; no ambiguity

**What Jeremy Needs to Do:**
1. Update `requirements.txt`: `redis` → `valkey`
2. Update Docker Compose: `redis:7.2` → `valkey:8.0`
3. Run tests (should pass; no code changes needed)
4. Verify Celery works with Valkey (it does)

**Effort:** 2-4 hours. No risk.

**Bottom Line:** ❌ **DO NOT PROCEED WITH REDIS**. 🟢 **Replace with Valkey immediately**. This is a blocker for Alpha 3X sign-off.

---

## GRAFANA (Item 3) — 🟨 YELLOW RISK

**The Issue:** Grafana is AGPL-3.0 (copyleft license); copyleft licenses have "viral" restrictions.

**Why It's Yellow, Not Red:**
- ✅ Grafana is deployed **unmodified** (no code changes to core)
- ✅ Custom dashboards are not AGPL-affected (they're proprietary)
- ✅ Internal ops team use doesn't expose merchants to AGPL
- ✅ Unmodified AGPL deployment is compliant; source is public

**The Catch:** If Canary modifies Grafana core code (unlikely) or open-sources with Grafana as a dependency, AGPL obligations become substantive.

**What Syd Needs to Do:**
1. Add governance rule: "Grafana core modifications prohibited without legal review"
2. Document: "Custom dashboards are Canary proprietary IP; unmodified Grafana deployment is AGPL-3.0 compliant"
3. If open-sourcing Canary: Include license disclaimer about AGPL-3.0 Grafana dependency

**Alternatives (If AGPL Becomes Strategic Blocker):**
- Perses (Apache-2.0; direct Grafana replacement; CNCF project)
- However, no urgency; unmodified Grafana is widely used in SaaS and is AGPL-compliant

**Bottom Line:** ✅ **APPROVED for Alpha 3X**. Add safeguards to governance manual.

---

## CRITICAL DECISION FOR JEFFE + SYD: OPEN-SOURCE LICENSE

This brief assumes Canary will be open-sourced (per Jeffe's Feb 17 statement: "completely open source").

**Decision Point:** Is Canary's open-source license **GPL-3.0 or Apache-2.0/MIT?**

| Choice | Directus | Grafana/Hasura | Effort | Trade-off |
|--------|----------|---------|--------|-----------|
| **GPL-3.0** | ✅ Compatible | ✅ Compatible | Zero | Derivative works must also be GPL |
| **Apache-2.0** | ❌ Conflict | ⚠️ Conflict | High (migrate components) | Permissive; allows proprietary derivatives |

**Recommendation:** GPL-3.0 aligns naturally with the stack. Apache-2.0 requires Directus (and possibly Grafana) replacement.

**Timeline:** Decide by March 31, 2026.

---

## SYD'S TO-DO LIST

### Before Alpha 3X Sign-Off (Feb 28 – Mar 15):
- [ ] Confirm this brief is correct (ask questions)
- [ ] Coordinate with Jeremy on Valkey migration
- [ ] Confirm GrowDirect is <$5M revenue (for Directus compliance)
- [ ] Add Grafana governance rule to compliance manual

### By March 31, 2026:
- [ ] Finalize open-source license decision with Jeffe (GPL-3.0 vs. Apache-2.0)
- [ ] If Apache-2.0 chosen: Plan Directus + Grafana replacement Q2 2026

### Ongoing:
- [ ] Monitor Grafana licensing (unlikely to change, but track)
- [ ] Monitor Directus commercialization as GrowDirect scales
- [ ] Update project documentation with final license strategy

---

## RISK MITIGATION SUMMARY

| Item | Pre-Mitigation Risk | Post-Mitigation Risk | Owner |
|------|------------------|-------------------|-------|
| Directus | 🟨 YELLOW | 🟨 YELLOW (controlled) | Syd + Jeffe |
| Redis → Valkey | 🔴 RED | 🟢 GREEN | Jeremy (2-4 hrs) |
| Grafana | 🟨 YELLOW | 🟨 YELLOW (controlled) | Syd + governance |

**Overall Alpha 3X Readiness:** Approve after Valkey migration (single blocker).

---

## SOURCES & REFERENCES

- [Directus License](https://directus.io/bsl)
- [Directus BSL FAQ](https://directus.io/bsl-faq)
- [Redis Licensing](https://redis.io/legal/licenses/)
- [Valkey (Linux Foundation)](https://valkey.io/)
- [Grafana Licensing](https://grafana.com/licensing/)
- [AGPL-3.0 Specification](https://www.gnu.org/licenses/agpl-3.0.html)

---

*For detailed analysis, legal precedent, and alternative options, see: `Canary_Alpha3X_License_Review_Brief_Syd_v1.0.md`*

*Confidential — Canary LP / GrowDirect*
