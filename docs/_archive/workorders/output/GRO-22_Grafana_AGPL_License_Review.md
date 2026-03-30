---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# GRO-22 — Grafana AGPL v3 License Review

**Issue:** GRO-22 (B-006)
**Prepared By:** ALX (Chief of Staff) — draft for Syd's legal opinion
**Date:** March 2, 2026
**Classification:** Internal — Legal Analysis Draft
**Gate:** Syd delivers formal opinion.
**Done When:** Legal opinion delivered — use or don't use.

---

## 1. Summary

Grafana, Grafana Loki, and Grafana Tempo are licensed under the **GNU Affero General Public License v3 (AGPL-3.0)**. This license was adopted in April 2021, replacing the previous Apache 2.0 license. Grafana plugins, agents, and certain libraries remain Apache-licensed.

Canary LP is evaluating Grafana OSS for internal metrics dashboards (merchant analytics, Chirp detection visualization, operational monitoring). This memo analyzes whether AGPL v3 is compatible with Canary LP's deployment model.

---

## 2. AGPL v3 — Key Obligations

### 2.1 What AGPL Adds Over GPL v3

The AGPL is identical to GPL v3 except for **Section 13 (Remote Network Interaction)**, which closes the "SaaS loophole." Under GPL v3, providing software as a hosted service (without distributing binaries) does not trigger copyleft. AGPL v3 changes this:

> If you modify the Program and make it available to users interacting with it remotely through a computer network, you must provide those users access to the Corresponding Source of your modified version.

### 2.2 Trigger Conditions

The AGPL copyleft obligation triggers when **ALL** of the following are true:

1. You **modify** the AGPL-licensed code (not just configure/deploy it)
2. Users **interact with the modified software over a network**
3. Those users are **outside your organization**

### 2.3 What Does NOT Trigger Copyleft

- **Running unmodified Grafana** — No source code disclosure required even if exposed to external users
- **Internal-only use** — Even modified Grafana used only by your own employees does not trigger Section 13
- **Configuration and theming** — Changing dashboards, data sources, and visual configuration is not "modification" of the software
- **Connecting via API/iframe** — Grafana running as a separate process, embedded via iframe in your application, generally does not create a derivative work of your application (process boundary doctrine)

---

## 3. Canary LP Use Case Analysis

### 3.1 Planned Usage

| Use Case | Description | External Users? |
|----------|-------------|-----------------|
| **Internal ops dashboard** | Team monitoring of system health, sync status, error rates | No — internal only |
| **Merchant-facing analytics** | Embedded Grafana panels showing transaction metrics, Chirp alerts, loss trends | **Yes — merchants access via Canary web app** |
| **Admin analytics** | Cross-merchant aggregate views for GrowDirect team | No — internal only |

### 3.2 Risk Assessment by Use Case

**Internal ops dashboard — LOW RISK**
- Internal-only use never triggers AGPL Section 13, even with modifications
- No action required

**Merchant-facing analytics — MEDIUM-HIGH RISK**
- If Grafana panels are embedded (via iframe) in the Canary LP merchant dashboard, merchants are "users interacting remotely through a computer network"
- **If Grafana is unmodified:** No copyleft trigger. Merchants see Grafana output, but Canary has no obligation to share source
- **If Grafana is modified** (custom plugins, forked rendering, API modifications): AGPL Section 13 triggers. Canary must provide modified Grafana source to merchants. Canary's own application code is NOT affected (separate process boundary), but the modified Grafana code must be disclosed
- **The gray zone:** Custom Grafana plugins are Apache-licensed per Grafana Labs' policy. But if modifications touch core Grafana code (not plugins), the AGPL applies to those modifications

**Admin analytics — LOW RISK**
- Internal use only. No AGPL trigger regardless of modifications

### 3.3 Embedding Architecture Matters

The copyleft "infection" question depends on how Grafana integrates with Canary:

| Integration Model | AGPL Risk | Notes |
|------------------|-----------|-------|
| **Iframe embed** (separate Grafana process) | Low | Process boundary generally prevents copyleft from reaching Canary app code. Only modified Grafana code is affected |
| **Grafana as API** (Canary fetches data from Grafana API, renders in own UI) | Low | REST API interaction is not a derivative work |
| **Linked library** (Grafana code compiled into Canary app) | **HIGH** | Creates derivative work — entire linked application may be AGPL-encumbered |
| **Forked/modified Grafana** served to merchants | **MEDIUM** | Must share modified Grafana source, but Canary app code is separate |

---

## 4. Mitigation Options

### Option 1: Use Unmodified Grafana OSS (Recommended for MVP)

- Deploy stock Grafana OSS
- Configure dashboards, data sources, and panels — this is configuration, not modification
- Embed via iframe for merchant-facing views
- Custom logic lives in Canary's application layer, not in Grafana
- **Risk:** Minimal. No AGPL obligations triggered

### Option 2: Use Grafana Enterprise (Free Tier)

- Grafana Labs offers a free-to-use Enterprise binary under a proprietary license
- Same features as OSS but no AGPL obligations
- **Risk:** Zero copyleft risk. Dependency on Grafana Labs' licensing terms (they could change)
- **Trade-off:** Proprietary license — cannot inspect or modify source

### Option 3: Commercial License from Grafana Labs

- Contact Grafana Labs for a commercial license that removes AGPL obligations
- Allows modifications without source disclosure
- **Risk:** Cost. Likely $thousands/year for a startup
- **When:** Only if Canary needs deep Grafana modifications that touch core code

### Option 4: Alternative Tool (Metabase, Apache Superset)

- **Metabase:** AGPL-licensed (same issue)
- **Apache Superset:** Apache 2.0 license — no copyleft, fully permissive
- **Redash:** BSD 2-Clause — no copyleft
- If AGPL is a dealbreaker, Superset or Redash are permissive alternatives
- **Trade-off:** Feature set, community size, plugin ecosystem differ

---

## 5. Recommendation

**For Syd's formal opinion, ALX recommends:**

1. **Use unmodified Grafana OSS for MVP** — embed via iframe, no core modifications. This is the lowest-risk path and is consistent with how most SaaS companies use Grafana internally and for customer-facing dashboards.

2. **Establish a "no modification" policy** — Any Grafana customization must be done through dashboards, data sources, and Apache-licensed plugins. No forking or modifying Grafana core code without legal review.

3. **If deep customization is needed later**, evaluate:
   - Grafana Enterprise (free tier, proprietary license)
   - Commercial license from Grafana Labs
   - Migration to Apache Superset (permissive license)

4. **Document the deployment model** — Record that Grafana runs as a separate, unmodified process connected to Canary's PostgreSQL databases. This documentation protects against future audit claims.

---

## 6. Open Questions for Syd

1. **Does iframe embedding of unmodified AGPL software in a SaaS product create any risk under GrowDirect's specific deployment model?** Community consensus says no, but no court has definitively ruled on AGPL Section 13 + iframe embedding.

2. **Should GrowDirect adopt a blanket policy against AGPL-licensed dependencies?** Some enterprise companies (Google, Apple) ban AGPL entirely. Is this appropriate for our stage?

3. **If we later need to modify Grafana core, should we pursue the commercial license proactively** (before the modification), or is the Enterprise free tier sufficient?

4. **Does the AGPL create any risk for investor due diligence?** Some VCs flag AGPL dependencies as a concern. Should this be disclosed or addressed preemptively?

---

## 7. Routing

- **Syd:** Deliver formal legal opinion — approve unmodified Grafana OSS use, or recommend alternative
- **Tom:** Confirm Grafana deployment will be iframe-embed (separate process), not linked library
- **Jeremy:** Do not modify Grafana core code until Syd signs off on AGPL implications

---

*ALX | GRO-22 | March 2, 2026*
