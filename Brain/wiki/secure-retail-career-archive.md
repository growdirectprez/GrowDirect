---
date: 2026-04-21
type: wiki
tags: [secure, retail-career, ibm-consulting, pwc, appriss, archive-stub, nas-indexing-future]
sources:
  - /Users/gclyle/secure/PROJECTS/ (local enumeration)
  - /Users/gclyle/mnt/nas-archive/Work/ (NAS — not indexed yet)
last-compiled: 2026-04-21
needs-review: 2026-05-05
---

**Wiki:** [[Brain/Home|Home]]

# Pre-Secure Retail Career Archive

## Summary

Index of client folders in `/Users/gclyle/secure/PROJECTS/` and their era classification. Sprint 1 does **not** ingest these — content is either pre-Secure (IBM / PwC / JDA / Retek consulting, 2001–2009) or duplicated on the NAS (Secure-era clients other than Kroger). This article is a **stub**: captures what exists, defers extraction to a future NAS indexing sprint.

## Details

### Populated locally (pre-Secure IBM / consulting era)

These folders have real content at `/Users/gclyle/secure/PROJECTS/`. All are pre-Secure — the IBM consulting / retail-partner era before Appriss Retail.

| Folder | Files | Era / nature | Notes |
|---|---|---|---|
| `FM-JDA` | 1,856 | 2004–2005 JDA / PMM consulting | Biggest folder; Project Management artifacts, Allocation + Configuration workplans, BPA, CWRVW contract extension |
| `Circuit City` | 234 | 2002+ IBM retail consulting | Largest non-JDA client folder |
| `Fresh&Easy` | 85 | 2008 GMIS replacement / JDA | GMIS Replacement, JDA, RMS Replen Training, RPAS Client, Reclass, SRD |
| `CEO Study` | 23 | 2006 IBM Global CEO Study | Retail POV drafts (v0.3b through v0.9a), summary slides, HBR supporting material |
| `Dumoulin` | 14 | Canadian retailer | |
| `CBM` | 7 | IBM Component Business Model | IBM strategy framework, pre-Secure |
| `D&G` | 6 | | Small — light context |
| `CIRCUIT CITY WPC` | 6 | Circuit City Work Product Center | Related to main Circuit City folder |

### Empty locally — content lives on NAS (Secure-era clients)

These `PROJECTS/` folders exist as directory stubs only; actual content is at `~/mnt/nas-archive/Work/Clients/<FOLDER>` or `~/mnt/nas-archive/Work/Projects/<FOLDER>`. Not in Sprint 1 scope beyond Kroger.

- **Wal-Mart** — Secure 3.2 client (referenced in Secure Lite docs)
- **Harrods** — non-US Secure client
- **Staples** — Secure Store Management Reports SOW referenced in NAS Unsorted/Downloads
- **Toys** + **Toys 'R' Us** — Secure client (pre-bankruptcy era)
- **Heartbeat** — Secure adjacent
- **TSA** (The Sports Authority) — Secure client (pre-bankruptcy)
- **Retek** — pre-Secure partner (merchandising system implementations)
- **SAP** + **SAP Retail** — pre-Secure partner
- **Kroger CRP** — Secure 3.5 client, covered in [[Brain/wiki/secure-client-kroger|Kroger deep-dive]] (2017 engagement)
- **Weston** — George Weston Ltd (Loblaws parent, Canadian grocery)
- **PA LCB** — Pennsylvania Liquor Control Board
- **PB** — Pitney Bowes (?) or other
- **SWINDON** — Swindon (UK location — likely a retailer HQ)
- **TODAYMAN** — unclear
- **MCS Better Business** + **MCS Project Assessment** — MCS consulting
- **GAP** — 2002-era IBM retail consulting (pre-Secure)
- **IBM Method Web** — IBM internal methodology
- **NOTES** — generic; content unclear
- **RETAIL** — generic; likely cross-cutting
- **CBM** (populated), **D&G** (populated) — see above

### Where NAS content actually lives

The larger archive at `~/mnt/nas-archive/` contains:

- `Work/Clients/<CLIENT>/` — engagement folders for Secure + pre-Secure clients (KROGER, SECURE 5, BELK referenced, others not yet enumerated)
- `Work/Projects/<PROJECT>/` — project folders (Kroger CRP seen)
- `Work/Recovered/Secure Files/` — small (16K), possibly fragments
- `Email/CLIENTS/SECURE 5/` — email context, small
- `Reference/` — mixed: retail LP reference PDFs (Appriss Retail Data Spec v1.2, CRDM Deployment Guide, Secure Store Feature Sheet for Cashier Coaching, Baseline Case Resource Plan, Belk Resource Plan, Delivery Framework 2013, LPMS Open Interface) interleaved with a lot of non-retail personal content
- `Unsorted/` + `Unsorted/Downloads/` — large, mixed (SysRepublic SOWs, Walmart Secure 3.2 Quick Start Guide, RadioShack Secure Store SOW, Crime Bulletins)

## Future Work — NAS Indexing Sprint

The broader NAS archive holds high-value material that's worth extracting with proper triage. Candidates flagged during Sprint 1 (from incidental discovery):

**SDD source material** (retail LP product documentation):
- Appriss Retail Data Specification **v1.2** (newer than v1.1 we already have)
- Appriss Retail Hosted Application Overview v1.2
- Appriss Retail Support Model
- CRDM Deployment Guide
- Secure Store Feature Sheets (Cashier Coaching seen)

**FR / requirements material:**
- `5.1 Requirements.xlsx` (already covered in [[Brain/wiki/secure-omnichannel|Omnichannel]])
- Belk Resource Plan
- Baseline Case Resource Plan
- Cashier Perf Baseline Plan
- Limited Secure 3 Resource Plan

**Methodology / agent-team playbook material:**
- Delivery Framework v1.2 2013
- Delivery Resources Oct 2016
- Consultant Certification in BCS (120905)
- Efficient Item Assortment 2003.5 Road Map

**Client-specific content** (beyond Kroger):
- **Belk** — Resource Plan, full engagement content
- **Walmart** — Secure 3.2 Quick Start Guide
- **RadioShack** — Secure Store Management Reports SOW
- **CVS** — Secure Order Form 09-30-18
- **Kroger** — additional content (Appriss Order Form for Secure Store EBR Core, encrypted)

### Why deferred to a future sprint

Sprint 1 scope is the curated `~/secure/` content (Secure product docs + Kroger as first client). The broader NAS is:

1. **Much larger** — hundreds to thousands of files
2. **Less curated** — mixed with personal content (real estate, financial, family)
3. **Requires PII gate** — a clean extraction needs per-file PII classification before anything reaches `Brain/raw/inbox/`. Sprint 1 hit a PII incident where a bulk-extract leak captured a personal credit report and closing disclosure into the scratch dir before they were caught and deleted. The future NAS sprint needs this gate built into the `extract` command by default, not as a post-hoc manual review.
4. **Separate deliverables** — treasures here become SDDs, FR docs, agent-team playbooks, methodology guides (see [[Brain/projects/Secure|Secure MOC]] "Future Work" section)

## Related

- [[Brain/projects/Secure|Secure]] MOC
- [[Brain/wiki/secure-client-kroger|Kroger Deep-Dive]] — the one Secure-era client covered in Sprint 1
- [[Brain/wiki/secure-platform-overview|Secure Platform Overview]] — product line this career built

## Sources

- `/Users/gclyle/secure/PROJECTS/` — local enumeration via `find ... -type f | wc -l`
- `/Users/gclyle/mnt/nas-archive/Work/`, `Reference/`, `Unsorted/` — NAS structure observed during Kroger extraction (not ingested)
