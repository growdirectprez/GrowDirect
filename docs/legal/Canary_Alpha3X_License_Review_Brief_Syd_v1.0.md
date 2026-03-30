---
type: legal
domain: business
status: active
created: 2026-03-19
updated: 2026-03-19
---
# CANARY LP / GROWDIRECT
## Legal Brief: Alpha 3X Stack License Review

**TO:** Syd, Legal Counsel & PR
**FROM:** Internal Legal Review
**DATE:** February 21, 2026
**RE:** Three License Items Requiring Review Before Alpha 3X Platform Rehydration Sign-Off
**CLASSIFICATION:** Confidential — Legal Review

---

## EXECUTIVE SUMMARY

Three open-source dependencies in the Alpha 3X stack present licensing considerations that require legal review and approval before the platform architecture can be finalized. This brief provides detailed analysis of each license, identifies risks, and recommends resolution paths.

| Item | Component | License | Risk Level | Recommendation |
|------|-----------|---------|------------|-----------------|
| 1 | Directus 11 (Admin Panel) | BSL 1.1 + GPL-3.0 Conversion | YELLOW | Approved with conditions; monitor conversion date |
| 2 | Redis (Cache/Message Broker) | RSALv2 + SSPLv1 | RED | Replace with Valkey (BSD-3) immediately |
| 3 | Grafana (Monitoring) | AGPL-3.0 | YELLOW | Approved if unmodified; evaluate alternatives |

**Bottom Line:** Two items (Directus, Grafana) are manageable with conditions. Redis requires immediate replacement due to SaaS restrictions.

---

## ITEM 1: DIRECTUS BSL 1.1 — ADMIN PANEL

### Current Situation

**Component:** Directus 11 — used as internal admin control panel for Canary operators (loss prevention analysts, system administrators). Not exposed to merchants; merchants do not access Directus.

**License:** Business Source License 1.1 (BSL 1.1) with Additional Use Grant

**Change Date:** April 2026 (3-year conversion period from April 2023 initial release)

### License Analysis

#### What the BSL 1.1 Allows

The BSL 1.1 grants anyone the right to:
- Copy, modify, and create derivative works
- Use the software in production for free **if company "Total Finances" do not exceed $5,000,000**
- Use the software non-productively without financial restrictions (development, testing, debugging)

**Definition of "Total Finances":** The largest of your aggregate gross revenues, entire budget, and/or funding (no matter the source). This includes all revenue streams, not revenue specifically from Directus.

**Automatic Conversion:** On April 26, 2026, Directus 10.0.0 (released April 2023) automatically converts to GPL-3.0 or later. Subsequent releases follow their own 3-year timers independently.

#### Obligations Under BSL 1.1

1. **For SaaS Use (Internal Admin):** The BSL is explicitly designed to allow SaaS use internally without triggering commercial license requirements, *provided the $5M threshold is not exceeded*.

2. **Distribution Restriction:** You cannot commercialize or offer the software as a managed service to customers.

3. **Revenue Threshold:** If GrowDirect's combined revenues (all products, all funding) exceed $5M in any fiscal year, a commercial license is required going forward.

#### Does Internal-Only Admin Use Avoid Restrictions?

**Answer: Yes, with conditions.**

- BSL 1.1 explicitly permits production use of BSL-licensed software internally for companies under $5M
- Directus admin panels used only by Canary operators are **not exposed to merchants**, so there is no "offering to customers as a service"
- The $5M threshold is the only financial gate for internal use

**However:** If GrowDirect's total finances exceed $5M at any point, BSL 1.1 **requires** a commercial license from Directus Ltd. for continued production use.

#### Implications for Square Marketplace Certification

Square's Partner Program Agreement does not explicitly restrict components using BSL licenses, provided:
- The component is internal (not distributed to end-users)
- The component does not trigger license violations
- Compliance with the component's license terms is maintained

Directus on the Square Marketplace is not a violation per se — many merchants run Directus installations. However, **listing a merchant-facing app that internally depends on BSL code requires that you maintain compliance with BSL terms**.

#### Implications for Open-Sourcing Canary

This is the critical juncture. **When Directus converts to GPL-3.0 in April 2026, if Canary's codebase includes Directus as a dependency and is open-sourced, Canary's codebase becomes subject to GPL-3.0 obligations.**

**Specifically:**
- If Canary open-sources its code, any GPL-licensed component (including Directus after April 2026) triggers GPL-3.0 on the entire project
- The GPL-3.0 conversion is automatic — Directus Ltd. will offer no exceptions or relicensing windows
- Releasing Canary under GPL-3.0 is not problematic *if Canary's chosen open-source license is GPL-3.0 or compatible*
- Releasing Canary under a non-copyleft license (Apache 2.0, MIT, BSD) **after April 2026 while depending on GPL-licensed Directus is not legally sustainable**

### Risk Rating: YELLOW

**Rationale:**
- ✅ Directus BSL 1.1 is explicitly designed to allow internal SaaS use
- ✅ Merchant-facing use is not a concern (admin use only)
- ✅ <$5M revenue threshold is not an immediate blocker
- ⚠️ April 2026 GPL conversion requires architectural decision on open-source licensing
- ⚠️ If GrowDirect exceeds $5M in revenue, commercial license becomes mandatory

### Recommendations

**1. Immediate (Now — February 2026):**
- ✅ **APPROVED for use in Alpha 3X** — Directus BSL 1.1 is compliant for internal admin use
- Add compliance clause to Canary operational manual: "Directus must be used only for internal administration. No merchant-facing use."
- Track GrowDirect revenue; if approaching $5M, request Directus commercial license quote in Q3/Q4 2026

**2. By April 2026 (Before Conversion):**
- Make a formal decision on Canary's intended open-source license (GPL-3.0 vs. non-copyleft)
- If choosing GPL-3.0: No action needed; GPL-to-GPL compatibility is seamless
- If choosing Apache 2.0, MIT, or other non-copyleft: You must **replace Directus before April 2026** with a non-copyleft-licensed alternative

**3. Alternative Admin Panels (If GPL-3.0 is Unacceptable):**

| Alternative | License | Notes |
|-----------|---------|-------|
| **NocoDB** | AGPL-3.0 (transitioning to Sustainable Use License) | SaaS-friendly; similar feature set to Directus; unmodified use is safe |
| **Budibase** | GPL-3.0 | Low-code admin tool; built for internal tools |
| **AdminJS** | MIT | Lightweight; limited feature set vs. Directus |
| **Rowy** | AGPL-3.0 | Spreadsheet-like admin interface; similar GPL caveat |

**Risk of Alternatives:** NocoDB and Rowy both use AGPL-3.0, which has its own April 2026 conversion concerns. AdminJS is MIT but significantly less feature-rich. If open-source flexibility is a priority, Budibase (GPL-3.0) is the closest comparable to Directus.

**Recommendation:** **Approve Directus for Alpha 3X. Decide on Canary's open-source license by March 2026. If non-GPL is chosen, begin migration to AdminJS or Budibase in Q2 2026.**

---

## ITEM 2: REDIS RSALv2 / SSPLv1 — CACHE & MESSAGE BROKER

### Current Situation

**Component:** Redis 7.2.x — used as:
- **Cache layer** for merchant session state and fraud alert caching
- **Celery message broker** for asynchronous task processing (Chirp rule evaluation, email alerts)

**License:** Dual-licensed RSALv2 (Redis Source Available License v2) and SSPLv1 (Server Side Public License v1) as of March 2024

**Previous License:** BSD-3-Clause (until March 2024)

### License Analysis

#### Why Redis Changed Licenses

In March 2024, Redis Inc. moved away from the permissive BSD-3-Clause open-source license to restrictive source-available licenses in response to managed service providers (AWS ElastiCache, Google Cloud Memorystore, Azure Cache) using Redis 7.2 under BSD-3 but not contributing back to the project.

#### What RSALv2 Restricts

RSALv2 permits:
- Free use, copying, modification
- Private/internal use without restrictions

RSALv2 **prohibits:**
- **Commercializing the software** (charging money for Redis itself)
- **Offering Redis as a managed service** to others (e.g., "Redis-as-a-Service" offering)

**Translation for Canary:** If Canary operates Redis internally as a cache/message broker and does not offer Redis services to merchants, RSALv2 is not violated. However:

#### What SSPLv1 Restricts

SSPLv1 permits:
- Free use, modification, redistribution, including for SaaS use

SSPLv1 **requires:**
- If you offer the software as a service to others, you must **publicly release all management layers and modifications** under SSPLv1

**Translation for Canary:** If Canary is a SaaS merchant loss-prevention platform that internally depends on Redis, SSPLv1 could be interpreted as:
- Redis is a backend service dependency; merchants don't directly interact with Redis
- But the "service" Canary offers to merchants (loss prevention via AI analysis) is powered by Redis
- SSPLv1 interpretation is ambiguous — does it require releasing your fraud detection logic? Your Chirp rules? Your case management system?

#### The Real Problem: License Ambiguity + Community Rejection

Redis's RSALv2/SSPLv1 licenses are **not OSI-approved** and are widely considered legally unclear. Major Linux distributions (Ubuntu, Debian, Fedora) dropped Redis from their repositories. Cloud providers deprecated Redis. The developer community forked Redis under a clearer license.

**Key Court Precedent:** These licenses have not been tested in court. Their enforceability for SaaS use is uncertain.

#### Implications for Canary

**Scenario 1: Internal Redis Use Only**
- Canary uses Redis as internal cache/message broker
- Merchants do not access Redis directly
- Canary does not offer Redis as a managed service
- **Risk Level:** UNCLEAR — RSALv2 probably doesn't restrict this; SSPLv1 interpretation is murky

**Scenario 2: If Canary Offers Advanced Analytics Requiring Real-Time Redis Data**
- If Canary exposes any merchant-facing feature that directly depends on Redis (e.g., real-time fraud score, live dashboard)
- SSPLv1 could be interpreted as requiring release of management layers
- **Risk Level:** AMBIGUOUS AND DANGEROUS

**Scenario 3: Open-Sourcing Canary**
- If Canary's codebase is open-sourced, and the code includes Redis dependency configuration, the Redis components fall under RSALv2/SSPLv1
- Open-source release does not exempt you from SSPLv1 "service" obligations
- **Risk Level:** VERY HIGH — mixing open-source code with SSPLv1 dependencies creates legal ambiguity

### The Linux Foundation Alternative: Valkey

In response to Redis's license change, a consortium of major tech companies (AWS, Google Cloud, Oracle, Ericsson, others) and former Redis maintainers forked Redis 7.2.4 under the **BSD-3-Clause license** as **Valkey**, backed by the Linux Foundation.

**Valkey Key Facts:**
- **License:** BSD-3-Clause (fully open-source, no restrictions on commercial use)
- **API Compatibility:** 100% compatible with Redis 7.2 and earlier versions — drop-in replacement
- **Long-Term Support:** Backed by Linux Foundation; no single vendor can change the license
- **Community:** Endorsed by AWS, Google Cloud, Oracle, Homebrew, Debian, Ubuntu, and major observability platforms
- **Status:** Production-ready; widely deployed in enterprises as Redis replacement

**Migration Effort:** For Canary's use case (simple cache + Celery broker), migration from Redis to Valkey is typically **zero code changes** — configuration only. Valkey CLI commands are identical to Redis.

### Risk Rating: RED

**Rationale:**
- 🔴 RSALv2/SSPLv1 are not OSI-approved and have unclear SaaS implications
- 🔴 SSPLv1 interpretation is ambiguous for a SaaS product; legal enforceability is untested
- 🔴 Open-sourcing Canary creates complex questions about Redis dependency licensing
- 🔴 Redis Inc. can change license terms further; vendor lock-in risk is high
- ✅ Valkey drop-in replacement exists and is production-ready
- ✅ Valkey has no license ambiguity; BSD-3 is industry-standard permissive

### Recommendations

**REPLACE REDIS WITH VALKEY IMMEDIATELY**

**1. Before Alpha 3X Sign-Off (Next 2 Weeks):**

```
Migration Checklist:
[ ] Verify Valkey 8.0+ supports Celery (it does; Celery broker >= 5.0 is compatible)
[ ] Update requirements.txt: redis → valkey
[ ] Update .env.template and Docker Compose: redis:7.2 → valkey:8.0
[ ] Run existing test suite against Valkey (no code changes needed)
[ ] Verify Celery broker communication (should be identical)
[ ] Update project dependencies audit to reflect Valkey BSD-3 license
[ ] Update Alpha_Infrastructure_Setup_v1.0.md with Valkey instead of Redis
```

**2. Documentation:**
- Add to `Markdown/Specs/Canary_Technology_Blueprint_v1.0.md`: "Redis 7.2 replaced with Valkey 8.0 (BSD-3-Clause, Linux Foundation) to ensure open-source licensing clarity and eliminate RSALv2/SSPLv1 ambiguity."
- Add to compliance manual: "Canary uses Valkey (not Redis) to maintain BSD-3 licensing compatibility and avoid SaaS license ambiguity."

**3. Cost/Benefit:**
- **Cost:** ~2-4 hours engineering effort; near-zero risk
- **Benefit:** Eliminates Red-level license risk; improves open-source credibility; aligns with Linux Foundation backing

**4. If Not Feasible (Unlikely):**
If for some reason Valkey is not compatible with your use case, explore:
- **KeyDB** (BSD-3 license; Redis-compatible fork)
- **DragonflyDB** (BSL → open-source; Redis-compatible but newer, less battle-tested)
- However, neither is necessary — Valkey is a direct drop-in

**Recommendation:** **Do not proceed to Alpha 3X with Redis. Replace with Valkey in next sprint. Risk is too high given clear, zero-effort alternative exists.**

---

## ITEM 3: GRAFANA AGPL-3.0 — MONITORING DASHBOARDS

### Current Situation

**Component:** Grafana 10.x — used for internal monitoring and observability:
- System metrics (CPU, memory, disk, network)
- Application performance monitoring (API response times, database query performance)
- Alerting dashboard
- Log aggregation display (Loki integration)

**Audience:** Internal Canary ops team only; not exposed to merchants

**License:** AGPL-3.0-only (changed from Apache-2.0 in April 2021)

### License Analysis

#### What AGPL-3.0 Requires

AGPL-3.0 is a **copyleft license** that extends GPL-3.0 with a "network use" clause.

**AGPL Core Obligation:** If you use, modify, or serve AGPL software over a network, and users interact with it over a network, you must provide users with the source code of that software and any modifications.

**Specifically for Grafana:**

1. **Unmodified Use:** If you deploy Grafana exactly as-is (no code changes), AGPL is satisfied by:
   - Disclosing to users that the software is AGPL-licensed
   - Providing access to Grafana's source code (already public on GitHub)
   - No obligation to disclose your own monitoring code or dashboard configurations

2. **Modified Grafana Core:** If you modify Grafana's core code (not plugins, not dashboards), you must:
   - Release those modifications under AGPL-3.0
   - Make the modified source available to all users who interact with it over the network

3. **Custom Dashboards & Plugins:**
   - Creating custom dashboards in Grafana is not "modification" of Grafana code
   - Grafana plugins remain Apache-2.0 licensed and do not trigger AGPL
   - Custom dashboards are your proprietary content; no disclosure required

4. **Network Service Clause:** Because Grafana runs as a web service (port 3000, accessed over HTTP), AGPL's network clause applies. However:
   - The obligation is to disclose Grafana source, not your data or configurations
   - Grafana Inc. treats unmodified Grafana as AGPL-compliant without additional disclosure

### Does Internal-Only Monitoring Avoid AGPL Obligations?

**Answer: Yes, largely.**

- Unmodified Grafana used internally with custom dashboards is AGPL-compliant
- AGPL obligations trigger when you **modify Grafana source code and make it available over a network**
- Monitoring dashboards you create are your proprietary content; they are not Grafana modifications
- Internal ops team access over HTTPS is covered by AGPL compliance (source is available)

### Implications for Canary

**Current Use is Low-Risk:**
- ✅ Canary deploys Grafana unmodified
- ✅ Custom dashboards are proprietary (not AGPL-affected)
- ✅ Internal ops use does not expose merchants to AGPL
- ✅ Grafana source is publicly available on GitHub; AGPL requirements are met

**Risk Emerges If:**
- ❌ Canary modifies Grafana core code (e.g., custom authentication, custom visualizations in core)
- ❌ Canary open-sources its codebase and includes Grafana configuration as deployable infrastructure
- ❌ Canary develops custom Grafana plugins with AGPL-incompatible licenses

**Open-Sourcing Concern:**
- If Canary's infrastructure-as-code (Docker Compose, Kubernetes manifests) includes `grafana/grafana:10.0` as a dependency, that does not trigger AGPL obligations on Canary's code
- The Grafana container remains AGPL-licensed; Canary's orchestration remains under Canary's chosen license
- However, **if Canary includes Grafana in a single monolithic deployment**, the line becomes blurred and Syd should advise

### Alternatives to Grafana

If AGPL is a strategic blocker (unlikely, but considered):

| Alternative | License | Pros | Cons |
|-----------|---------|------|------|
| **Perses** | Apache-2.0 | Direct Grafana replacement; CNCF Sandbox project; Prometheus-native | Newer; smaller community |
| **Kibana** | SSPL-like (ELB license) | Elasticsearch-native; powerful | Elasticsearch is also restricted; full-stack lock-in |
| **Apache Superset** | Apache-2.0 | Multi-source dashboards; SQL Lab | Less focused on metrics monitoring; more BI-oriented |
| **Prometheus + Custom** | Apache-2.0 | Use Prometheus metrics export; build custom dashboards | Engineering effort required |

### Risk Rating: YELLOW

**Rationale:**
- ✅ Unmodified Grafana with custom dashboards is AGPL-compliant
- ✅ Internal-only ops use is low-risk
- ✅ Custom dashboards are proprietary; no disclosure required
- ⚠️ If Grafana core is modified, AGPL obligations become substantive
- ⚠️ Open-sourcing Canary's infrastructure code requires careful handling of Grafana dependency
- ⚠️ AGPL has "viral" nature — any code that integrates tightly with Grafana is at risk

### Recommendations

**APPROVED FOR USE IN ALPHA 3X WITH SAFEGUARDS**

**1. Immediate (Now):**
- ✅ Continue using unmodified Grafana 10.x
- Add governance rule: "Grafana core code modifications are prohibited without legal review. Dashboard and plugin development is permitted."
- Document that custom monitoring dashboards are Canary proprietary IP

**2. Before Alpha 3X Sign-Off:**
- Audit any Grafana plugins Canary uses; ensure they are Apache-2.0 or compatible
- Verify Docker Compose includes `grafana/grafana:latest` (unmodified image)
- Add to `Markdown/Specs/Canary_Technology_Blueprint_v1.0.md`: "Grafana is deployed unmodified (AGPL-3.0 compliance) for internal monitoring only. Custom dashboards and plugins remain Canary proprietary."

**3. If Canary Open-Sources Its Infrastructure:**
- Document explicitly: "Grafana is a third-party AGPL-3.0 component. Canary's orchestration and configuration remain under [chosen license]. Grafana source is available at https://github.com/grafana/grafana."
- Do not attempt to relicense Grafana; treat it as a licensed dependency
- Syd should review final license compatibility before public release

**4. If Grafana's AGPL Becomes Strategically Unacceptable:**
- **Transition Plan:** Move to Perses (Apache-2.0) in Q3 2026
- Perses is production-ready and CNCF-backed; migration effort is moderate
- However, this is not urgent — unmodified Grafana is AGPL-compliant and widely used in SaaS products

**5. Monitor:**
- Grafana Inc.'s licensing; they have not changed since April 2021 and are unlikely to change
- Community sentiment on AGPL; if sentiment shifts and Grafana relicenses, Canary can reassess

---

## OVERALL PLATFORM ARCHITECTURE — LICENSE SUMMARY

Assuming the three recommendations above are adopted:

| Component | License | Risk | Status |
|-----------|---------|------|--------|
| **Directus 11** | BSL-1.1 → GPL-3.0 (Apr 2026) | YELLOW | Approved; decide open-source license by Mar 2026 |
| **Valkey** | BSD-3-Clause | GREEN | Recommended; replace Redis immediately |
| **Grafana** | AGPL-3.0 | YELLOW | Approved; unmodified use only |
| **Flask** | BSD-3-Clause | GREEN | Core framework |
| **PostgreSQL** | PostgreSQL License (Apache-2.0 compatible) | GREEN | Database |
| **Hasura** | AGPL-3.0 (Community) | YELLOW | Internal GraphQL API gateway; same safeguards as Grafana |
| **Airflow** | Apache-2.0 | GREEN | Orchestration |
| **Superset** | Apache-2.0 | GREEN | Merchant-facing dashboards |
| **Keycloak** | Apache-2.0 | GREEN | Authentication/OAuth |

**Overall License Posture:** Defensible for SaaS use. If Canary chooses GPL-3.0 as its open-source license, all components are compatible. If Canary chooses Apache-2.0 or MIT, Directus and Grafana/Hasura will require mitigation (migration or commercial licensing).

---

## IMPLICATIONS FOR CANARY'S OPEN-SOURCE STRATEGY

This is critical context for Syd's eventual IP strategy decision.

### Scenario A: Canary Open-Sources Under GPL-3.0

**Compatibility:**
- ✅ Directus (GPL-3.0 after April 2026)
- ✅ Grafana (AGPL-3.0; GPL-3.0 is compatible)
- ✅ Hasura Community (AGPL-3.0)
- ✅ All other components

**Implications:**
- Canary's code, once released under GPL-3.0, cannot be relicensed to proprietary or non-copyleft licenses
- Merchants receiving Canary's code receive GPL-3.0 rights
- This aligns with Jeffe's stated "completely open source" positioning (Feb 17 session)
- **This is viable and coherent.**

### Scenario B: Canary Open-Sources Under Apache-2.0 or MIT

**Compatibility:**
- ❌ Directus (GPL-3.0 after April 2026) — copyleft conflict
- ⚠️ Grafana (AGPL-3.0) — copyleft conflict (mitigated if unmodified)
- ⚠️ Hasura Community (AGPL-3.0) — copyleft conflict

**Implications:**
- Canary's code released under Apache-2.0 would still depend on GPL-3.0/AGPL-3.0 components
- This is legal but creates "license stack" complexity — users of Canary would need to understand GPL-3.0 obligations from transitive dependencies
- Releases would require careful documentation of which components are GPL-covered
- Not recommended; too much friction for open-source adoption

**Action Needed:** Syd should clarify with Jeffe whether Canary's intended open-source license is GPL-3.0 (yes, aligns with components) or Apache-2.0 (requires component migration).

---

## LEGAL REVIEW CHECKLIST FOR SYD

Before Alpha 3X sign-off, Syd should complete:

- [ ] **Directus BSL-1.1:** Confirm understanding of $5M revenue threshold; if <$5M at all times, BSL use is compliant
- [ ] **Directus April 2026 Conversion:** Make go/no-go decision on open-source license (GPL-3.0 vs. non-copyleft) by March 31, 2026
- [ ] **Redis → Valkey Migration:** Approve immediate replacement; coordinate with Jeremy for implementation
- [ ] **Grafana AGPL Compliance:** Confirm unmodified deployment; document in governance manual
- [ ] **Open-Source Strategy:** Clarify with Jeffe: Is Canary's intended license GPL-3.0 (yes, aligns with stack) or Apache-2.0 (requires component migration)
- [ ] **Square Marketplace Implications:** Verify that dependent open-source components do not violate Square Partner Program Agreement (unlikely, but review)
- [ ] **Commercial Licensing:** Obtain quotes for Directus commercial license (in case $5M threshold is approached) and Grafana enterprise license (in case AGPL becomes unacceptable)
- [ ] **Compliance Documentation:** Update project manual, deployment guides, and open-source license acknowledgments to reflect final decision

---

## RISK SUMMARY TABLE

| Item | Current Risk | After Recommendations | Owner | Deadline |
|------|-----------|-------------|-------|----------|
| **Directus** | YELLOW | YELLOW (mitigated) | Syd, Jeffe | Mar 31, 2026 (license decision) |
| **Redis/Valkey** | RED | GREEN | Jeremy | Feb 28, 2026 (migration) |
| **Grafana** | YELLOW | YELLOW (mitigated) | Syd | Ongoing (governance) |
| **Open-Source License** | PENDING | PENDING | Jeffe, Syd | Mar 31, 2026 |

---

## NEXT STEPS

**For Syd:**
1. Review this brief and confirm understanding
2. Coordinate with Jeremy on Redis → Valkey migration timeline
3. Schedule call with Jeffe to finalize open-source license decision (GPL-3.0 vs. Apache-2.0) — this drives Directus and Grafana strategy
4. Update `Canary_Technology_Blueprint_v1.0.md` and compliance documentation

**For Jeremy:**
1. Migrate Redis to Valkey before Alpha 3X QA gate (est. 2-4 hours effort)

**For Eva:**
1. Update Attack Plan and Sprint 2 task list to include Valkey migration

**For Team (All):**
1. Be aware that three components have licensing considerations; no secrets, no surprises in external communications

---

## APPENDICES

### Appendix A: Directus BSL-1.1 Full Text Reference

**Source:** [Directus License Overview](https://directus.io/bsl)

Key provisions:
- **Free Use:** Any company <$5M "Total Finances" may use in production
- **Change Date:** April 26, 2026 (3-year mark for v10.0.0)
- **Change License:** GPL-3.0 or compatible
- **Commercial License:** Available for >$5M organizations at [Directus Commercial License](https://directus.io/commercial-license)

### Appendix B: Redis RSALv2 vs. SSPLv1

**Source:** [Redis Licensing](https://redis.io/legal/licenses/)

- **RSALv2:** Prohibits commercialization and managed service offerings
- **SSPLv1:** Requires release of management layers if offered as a service
- **Key Issue:** Not OSI-approved; legal ambiguity for SaaS use cases
- **Community Response:** [Valkey Linux Foundation Fork](https://valkey.io/)

### Appendix C: Grafana AGPL-3.0 Compliance

**Source:** [Grafana Licensing](https://grafana.com/licensing/)

- **Core License:** AGPL-3.0 (as of April 2021)
- **Plugins:** Apache-2.0 (not AGPL-affected)
- **Unmodified Use:** Compliant with public source disclosure
- **Modified Use:** Requires source release under AGPL-3.0
- **Commercial License:** Available at [Grafana Labs](https://grafana.com/licensing/) for modified deployments

### Appendix D: Valkey BSD-3-Clause License

**Source:** [Valkey](https://valkey.io/)

- **License:** Berkeley Software Distribution 3-Clause (BSD-3)
- **Backing:** Linux Foundation (ensures perpetual open-source status)
- **API Compatibility:** 100% with Redis 7.2.x
- **Endorsement:** AWS, Google Cloud, Oracle, Ericsson, others
- **Deployment:** Production-ready; drop-in replacement

---

## SIGN-OFF

**Prepared by:** Internal Legal Review
**Date:** February 21, 2026
**Status:** READY FOR SYD REVIEW AND APPROVAL

**Next Review:** Post-Alpha 3X sign-off; Directus conversion monitoring (April 2026)

---

*This brief is attorney-client privileged communication. Do not distribute outside the team without Syd's explicit approval.*

*Confidential — Canary LP / GrowDirect. All rights reserved.*
