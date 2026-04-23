---
date: 2026-04-23
type: wiki
tags: [secure, lpms, case-management, sporting-goods, firearms-regulated, taxonomy, reference-data, 2015]
sources:
  - Brain/raw/inbox/actions.md
  - Brain/raw/inbox/incident-types.md
  - Brain/raw/inbox/source-of-info.md
  - Brain/raw/inbox/open-analyst-investigations--7-17-15.md
  - Brain/raw/inbox/weekly-recap-2015-week-24.md
  - Brain/raw/inbox/ytd-errors-in-lpms-reporting-2015.md
  - Brain/raw/inbox/yearly-case-extract---sample.md
last-compiled: 2026-04-23
needs-review: 2026-05-07
---

**Wiki:** [[Brain/Home|Home]]

# LPMS Case Management — Sporting-Goods Chain Deployment (2015)

## Summary

Seven intakes from a 2015 LPMS (Loss Prevention Management System) deployment at a **US sporting-goods chain with ~1,100+ stores operating across a firearms-regulated segment**. A complete operational snapshot of how a mid-to-large US multi-brand retailer ran its LP function: the taxonomies used to classify incidents and outcomes, the regional org structure, a weekly operational recap showing audit performance and shrink tiers, a YTD data-quality errors tracker, and a sample yearly case extract with real case records.

**Deployment archetype:** US sporting-goods chain, 1,100+ stores, multi-brand portfolio including a specialty-golf sub-brand, firearms-regulated (FFL compliance surface), seven named LP regions with Regional LP Director + District LP Manager cascade, Analyst + Field Investigator tiers.

## The Reference Data Model

### Action Taxonomy (Actions.xlsx)

The set of closing actions a case can take, split between Internal (employee) and External (customer/shoplifter) classes. Current taxonomy + mapping to the future historical-conversion target.

**Internal action codes:**

- Closed Unfounded
- Corrective Action *(formerly "Final Warning / Corrective Action")*
- Interviewed-No Case
- Phone Interview variants (Final Warning, Quit During Interview, Resigned, Terminated-Prosecuted, Terminated-Released) — note added to merge non-phone + phone via a phone-interview boolean
- Quit During Interview
- Quit Before Interview
- Reported to ATF *(firearms-compliance incidents)*
- Terminated - Prosecuted
- Terminated - Released
- Under Investigation

**External action codes:**

- Closed Unfounded
- Prosecuted
- Released - Adult
- Released - To Guardian *(formerly "To Parent")*
- Released - To Police *(pending addition in the reform)*
- Under Investigation

The Actions sheet has a reform-delta column ("Changes if applicable" + "Convert Historical to") — this is a *working document for a taxonomy consolidation sprint* that was in progress when the snapshot was taken.

### Incident Type Taxonomy (Incident Types.xlsx)

Three-level classification: **Class** (Critical Smart Alert / External / Internal) × **Type** × **Definition**. Each row tagged Active/Inactive and with a **Visability** flag (LP / All / Admin).

**Critical Smart Alerts** (LP visibility only, triggers escalation):

- Accidental Firearm Discharge
- Bomb Threat
- Burglary
- Civil Disturbance
- Fire
- Incident General (catch-all)
- Inspection: Firearms *(compliance audits)*
- Inspection: Other *(non-firearm compliance)*
- Missing F4473 *(firearms paperwork compliance)*
- Non-Productive Detainment *(shoplifter stopped but no merch recovered)*
- Robbery
- Serious Workplace Accident
- Shooting: Active In or Around a Store Location
- Shooting: Potentially Linked to a Store Purchase *(media-sensitive)*
- Straw Purchase *(firearms fraud)*
- Unaccounted for Firearm
- Weather Related Business Disruption *(Inactive)*
- Workplace Violence or Assault

**External incidents:**

- External Apprehension
- Known Theft
- Organized Retail Crime
- Refunder *(systematic refund exploitation)*
- Shoplifting / Grab and Run / Prevention-Recovery

**Internal incidents** (employee-related):

- Analyst Investigation (AI) / Field Investigation (FI)
- Cash Refund Fraud / Cash Theft / Credit Card Fraud
- Commission Fraud
- Coupon Abuse / Coupon Fraud (merge target)
- Destruction of Company Property
- Employee Discount Abuse
- Gift/Merchandise Card Fraud
- Merchandise Theft
- Passing Merchandise *(colluding with an external party)*
- Scorecard Abuse
- Unauthorized Markdowns
- Violation of Company Policy
- Falsification of Company Document

The firearms-heavy Critical Smart Alert list is distinctive to the firearms-regulated segment — the regulatory surface around firearms sales (ATF Form 4473, reporting, straw purchase detection, unaccounted-for firearm traceability) drives a specialised alert taxonomy that generic retailers wouldn't need.

### Source of Info Taxonomy (Source of Info.xlsx)

The sources that can feed a case or lead. Split Internal / External. Also includes a reform-delta column showing renames (e.g., "CCTV → LPTV", "Aspect Automind → SysRepublic Secure Alerts", "Anonymous → Tip - Anonymous").

Notable internal sources: Analyst Generated EBR, DLPM Generated EBR, Super User Generated EBR, **SysRepublic Secure Alerts** (the product feed), LPTV, Covert Camera, Tip (Associate/Customer/Hotline/Manager), Observation, Alarm Report/Data, Implication.

## Operational Snapshots

### Open Analyst Investigations — 7/17/2015

Weekly snapshot by Region, showing **Open** (current) vs **Last Week**. Seven numbered LP regions, each owned by a Regional LP Director (RLPD):

| Region | Open | Last Week |
|---:|---:|---:|
| 1 | 20 | 13 |
| 2 | 16 | 19 |
| 3 | 9 | 9 |
| 4 | 5 | 8 |
| 6 | 7 | 5 |
| 7 | 9 | 9 |
| 9 | 7 | 6 |
| Misc (DC / F&S / Corp) | 0 | 0 |
| **Total** | **73** | **69** |

**Aged leads breakdown:**

- Compliant Investigations (0–30 days): 61 current, 15 last week
- Director Intervention Investigations (31–99 days): 12 current, 54 last week *(big swing — suggests a major sweep of aged leads happened in the prior week)*
- Brand Risk Investigations (100+ days): 0, 0

### Weekly LP Recap — Week 24, July 2–8, 2015

Store assessment performance snapshot. Stores scoring ≥90% or <80% are highlighted. Each row: Region / District / Store Name / Store # / Score % / Audit Date / Type (**2015 LP Audit** or **2015 Specialty-Golf Audit**, reflecting the main-brand vs sub-brand audit program split) / **Shrink Tier** (G/Y/R/New) / Cost Shrink % most recent / Cost Shrink Goal %.

The **Shrink Tier** classification (G/Y/R) is a shrink-performance signal; **G** = on target, **Y** = cautionary, **R** = missing target by material margin. Typical per-week audit volume in the extract spans store counts across Midwest, Mid-Atlantic, Southeast, Southwest, Ohio Valley, Northeast regions.

### YTD Errors in LPMS Reporting (2015)

A data-quality tracker across 12 months (Jan–Dec) with consistent column set per month: **Narrative / Date of Incident / Case Complete / Stage / Case Status / AssignedTo / CaseOwner / Case / Action / SourceofInfo / IncidentType / Position / Civil / Restitution**.

Each month lists the *types* of LPMS data-quality errors the LP Operations team was finding during audit. The header row is a tongue-in-cheek "the fields below are required for reporting and documentation in LPMS" — what follows is the recurring pattern of errors:

- "Missing — Is it a case or not?" (Narrative blank)
- "All should be completed stating YES not NO" (Case Complete)
- "Is it a case, under investigation? What stage?" (Stage)
- "All should be CLOSED. Pending Approval need to be reviewed, approved and flags changed for civil/rest and close out" (Case Status)
- "Directors Name should be showing" with DLPM approval-routing notes
- "Is it coded correctly in the proper field? DE or PV or FW?" (Case) — **DE** = Dishonest Employee, **PV** = Policy Violation, **FW** = Final Warning (also **SL** referenced)

This is the kind of artefact you only get from an active LP ops function — a living document tracking how field LP staff were mis-coding cases and what the correct pattern should be. Every month has the same error categories, which says either (a) the errors were chronic, or (b) the document is a template re-filed each month rather than a live tracker.

### Yearly Case Extract — 2015 Sample

Real case records with columns: Date/Time · Region # · District # · Store # · Case # · Associate Name · Case Type · Regional Director · DLPM · Source · Case $ · Stage · Action · Associate Position · Complete · Created by.

Case ID format: **{DE|PV|FW}-{YY}-{STORE#}-{SEQ}** e.g. `DE-15-00092-1` (Dishonest Employee, 2015, Store 92, sequence 1).

Sample case types observed in the extract:

- Unauthorized Markdowns (Cashier)
- Gift/Merchandise Card Fraud (Customer Service Specialist)
- Violation of Company Policy
- Falsification of Company Document
- Merchandise Theft (Cashier)
- Passing Merchandise (Sales Associate/Cashier — high-$ cases typically got Phone Interview outcome)
- Scorecard Abuse
- Employee Discount Abuse

Positions involved: Cashier, Customer Service Specialist, Sales Associate/Cashier, Operations Associate, specialty-technician roles. Virtually all 2015 cases in the extract closed with **Terminated - Released** or similar; Phone Interview used for the higher-value prosecutable cases.

## Why This Matters

- **Taxonomy archaeology.** LP case management is a taxonomy discipline — the Action / Incident Type / Source of Info enums ARE the system. The 2015 taxonomies from this deployment are a masterclass in how a mature mid-market LP function structures its classification hierarchy, and a direct reference for how Canary's Fox module should shape its case taxonomies for multi-vertical Square merchants.
- **Real shrink-tier example.** The Green/Yellow/Red shrink-tier classification mapped against per-store shrink vs. goal is the exact pattern Canary's Chirps + merchant dashboard want to surface.
- **Regional org structure.** Seven numbered regions × ~60+ districts × ~1,100+ stores → RLPD → DLPM → Analyst roles. Clean precedent for how the LP management layer cascades. Canary's tenant model has to support that scale eventually.
- **Firearms-vertical alerts.** The Critical Smart Alert list captures firearms-compliance signals (F4473, ATF, straw purchase, unaccounted firearm) that are real-retail, real-regulatory — worth preserving as a reference for any future Canary vertical module targeting firearms retailers.
- **Data-quality error tracker.** The YTD Errors workbook is the off-system process for when the system lets bad data in. Maps directly to Canary's dashboard validation + case-completeness checks.

## Related

- [[Brain/projects/Secure|Secure MOC]]
- [[Brain/wiki/secure-sysrepublic-xbr-2016|Sysrepublic xBR Response (2016)]] — the SysRepublic Secure Alerts feed referenced in this deployment's Source-of-Info
- [[Brain/wiki/secure-eagle-eye-fnr-2018|Eagle Eye FR/NFR (2018)]] — follow-on product requirements work
- [[Brain/wiki/secure-platform-overview|Secure Platform Overview]]
- [[Brain/projects/Canary|Canary]] — forward lineage (Fox module case management)

## Sources

- `Brain/raw/inbox/Case Management Documentation/Actions.xlsx` — Action taxonomy (Internal + External) with reform-delta
- `Brain/raw/inbox/Case Management Documentation/Incident Types.xlsx` — Incident taxonomy (Critical Smart Alert / External / Internal) with definitions
- `Brain/raw/inbox/Case Management Documentation/Source of Info.xlsx` — Source-of-Info enum with rename reform notes
- `Brain/raw/inbox/Case Management Documentation/Reports/Open Analyst Investigations  7-17-15.xlsx` — Weekly open-investigations snapshot by region, 17 July 2015
- `Brain/raw/inbox/Case Management Documentation/Reports/Weekly Recap 2015 Week 24.xlsx` — Weekly LP recap with store audit scores + shrink tier, July 2–8 2015
- `Brain/raw/inbox/Case Management Documentation/Reports/YTD Errors in LPMS Reporting 2015.xlsx` — Monthly YTD data-quality error tracker for LPMS
- `Brain/raw/inbox/Case Management Documentation/Reports/Yearly Case Extract - Sample.xls` — Sample case extract with real case records (Feb 2015 onwards)

Extraction path: `.xls` / `.xlsx` → markitdown.
