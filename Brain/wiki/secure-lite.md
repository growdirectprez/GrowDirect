---
date: 2026-04-21
type: wiki
tags: [secure, secure-lite, appriss, smb, product-variant, canary-lineage]
sources:
  - Brain/raw/inbox/secure-lite-overview-docx.md
  - Brain/raw/inbox/secure-lite-config-docx.md
last-compiled: 2026-04-21
needs-review: 2026-05-05
---

**Wiki:** [[Brain/Home|Home]]

# Secure Lite

## Summary

Secure Lite (Oct 2018, proposed by Geoff Lyle) was a **simplified configuration** of Secure Store — not a separate codebase. Same engine, stripped config surface, pre-baked risk dictionary + Instant Analytics, three fixed roles, no SSO, no designer access, no developer mode, no file app. The goal: turn-key deployment for SMB retailers without the client-services engagement overhead that Secure 5 required. The variant exists because enterprise-grade configurability had become the enemy of fast SMB onboarding.

## Details

### Why Lite existed

Secure 5 assumed an enterprise retail IT organization and a multi-week client-services engagement to stand it up. For smaller merchants this was unworkable: the product was capable, the onboarding was not proportional. Secure Lite removes configuration surface until what's left is a usable installation that can be handed to an SMB with minimal hand-holding.

The Lite solution reused:
- The existing Executive / Analyst / Investigator role definitions from Secure 5
- A standard risk dictionary (common LP detection patterns)
- Pre-configured Instant Analytics targeting known areas of risk in the standard retail operating model

### What's removed vs Secure 5

| Capability | Secure 5 | Secure Lite |
|---|---|---|
| SSO | SAML 2.0 / OIDC | Manual credentials only |
| CRDM field aliases / enumerations | Resourceable | Out-of-box SDL only, no resourcing |
| Calendar | Multiple fiscal + Gregorian | One calendar at setup, no change |
| Report / Dashboard designer | Full access | Not included — new reports = consulting |
| Search composer | Full access | Ad-hoc composer only (Analyst), Quick Start only (Investigator) |
| Work Item Composer | Full configurable analytics | Predefined set, enable/disable only |
| Metric Manager | Full access | Metric search only, no manager |
| User tasks | Included | Not included |
| Teams | Included | Not included |
| Permission Groups | Configurable | Not included |
| Data Policy | Configurable | Set at initial deployment, changes via hierarchy |
| Export Manager | Included | Not included |
| Developer mode / Job system / Service Manager | Included | Not included |
| Data Management menu | Full | Not included |
| Files app | Included | Not included |
| Designer access | Included | Consulting engagement required |
| EBR Dashboard | Custom | Out-of-box only (asterisk indicates dev work to unlock) |
| Case Results Dashboard | Custom | Out-of-box only |

Items marked with an asterisk (\*) in the source doc indicate capabilities that **would need dedicated engineering to deliver** — they were on the roadmap at document time, not yet shipped.

### Three-role capability sheet

**Executive (Lite):**
- EBR Dashboard (out of box)
- Store Model Outlier (out of box SRA metrics)
- Case Results Dashboard
- Key Actor Profile lookups (Store / Cashier)
- Quick Start questions

**Analyst (Lite):**
- CRDM out of the box via SDL — no field aliasing or enumeration resourcing after setup
- Single calendar set at setup
- Analyst Dashboard
- Store Model Outlier access
- Manual user management, manual data policies + permission groups
- User data uploads
- Predefined Risk Dictionary searches
- Ad-hoc search composer
- Work Item Composer with predefined analytics (enable/disable + parameter tuning)
- Metric search (no Metric Manager)
- Factboard access
- Internal EBR Case Management
- Data Load Console

**Investigator (Lite):**
- Work items module
- Investigator EBR + Case dashboards
- Quick Start questions (no search composer)
- Case Management access
- Key actor profile lookups
- Receive notifications, view reports

### What this teaches Canary

- **"Configuration surface is the enemy of onboarding."** The Lite framing — take a capable product, remove config knobs until it onboards in hours — is directly applicable to Canary. Each flag, each preference, each optional step is onboarding friction. Canary's merchant tier strategy should be Lite-first, Advanced-opt-in, not the reverse.
- **Pre-baked risk dictionary + Instant Analytics as the default.** Secure Lite's answer to "how does an SMB tune detection" is **"they don't — we pre-tune it using patterns that work for most merchants."** This is Canary's Chirp pack model in spirit. Strengthen the defaults; reserve tuning for merchants who demand it.
- **"New reports = consulting" as a pricing boundary.** Lite set an explicit line: the designer surface is out of scope; customer reports need a consulting engagement. Canary's version: most merchants use defaults; Atlas-driven custom reporting is an upsell or partner enablement.
- **Roles don't change across variants.** Executive / Analyst / Investigator is the same model across Secure 5, Lite, and Omnichannel. Keep the user mental model stable across pricing tiers; vary features and config surface, not roles.

## Related

- [[Brain/projects/Secure|Secure]] MOC
- [[Brain/wiki/secure-platform-overview|Secure Platform Overview]] — product line context
- [[Brain/wiki/secure-architecture|Secure Architecture]] — full architecture Lite runs on
- [[Brain/projects/Canary|Canary]] — forward project
- [[docs/superpowers/briefs/2026-04-secure-to-canary-handoff|Secure → Canary Handoff]]

## Sources

- `/Users/gclyle/secure/Secure Lite Overview.docx` — role capability sheet (Geoff Lyle, Oct 2018)
- `/Users/gclyle/secure/Secure Lite Config.docx` — config detail (intake at `Brain/raw/inbox/secure-lite-config-docx.md`)
