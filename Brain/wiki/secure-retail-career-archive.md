---
date: 2026-04-21
type: wiki
tags: [secure, retail-career, ibm-consulting, pwc, appriss, archive-stub, nas-indexing-future]
sources:
  - /Users/gclyle/secure/PROJECTS/ (local enumeration)
  - /Users/gclyle/mnt/nas-archive/Work/ (NAS — not indexed yet)
last-compiled: 2026-04-23
needs-review: 2026-05-07
---

**Wiki:** [[Brain/Home|Home]]

# Pre-Secure Retail Career Archive

## Summary

Index of client folders in `/Users/gclyle/secure/PROJECTS/` and their era classification. Sprint 1 did **not** ingest these — content is either pre-Secure (IBM / PwC / JDA / Retek consulting, 2001–2009) or duplicated on the NAS (Secure-era clients other than the one top-5 US grocery chain covered in [[Brain/wiki/secure-client-top5-grocery-chain|Secure Client: Top-5 Grocery Chain]]). This article is a **stub**: captures what exists, defers extraction to a future NAS indexing sprint.

Per `feedback_scrub_client_names.md`, client identities below are abstracted to deployment archetypes. **Folder paths retain original client folder names** — paths are source-of-record references (like Sources sections elsewhere in the Brain). The narrative descriptions use archetypes.

## Details

### Populated locally (pre-Secure IBM / consulting era)

These folders have real content at `/Users/gclyle/secure/PROJECTS/`. All are pre-Secure — the IBM consulting / retail-partner era before Appriss Retail.

| Folder (path) | Files | Era / archetype |
|---|---|---|
| `FM-JDA` | 1,856 | 2004–2005 JDA / PMM consulting — Project Management artifacts, Allocation + Configuration workplans, BPA, contract extension material (largest folder in the archive) |
| `Circuit City` | 234 | 2002+ IBM retail consulting — US consumer-electronics big-box retailer (pre-bankruptcy) |
| `Fresh&Easy` | 85 | 2008 GMIS replacement / JDA — US grocery chain (short-lived US expansion of UK grocer, pre-2013 closure). GMIS Replacement, JDA, RMS Replen Training, RPAS Client, Reclass, SRD |
| `CEO Study` | 23 | 2006 IBM Global CEO Study — retail POV drafts (v0.3b through v0.9a), summary slides, HBR supporting material |
| `Dumoulin` | 14 | Canadian regional retailer |
| `CBM` | 7 | IBM Component Business Model — IBM strategy framework, pre-Secure |
| `D&G` | 6 | Regional retailer — small folder, light context |
| `CIRCUIT CITY WPC` | 6 | Work Product Center — related to main Circuit City folder |

### Empty locally — content lives on NAS (Secure-era clients)

These `PROJECTS/` folders exist as directory stubs only; actual content is at `~/mnt/nas-archive/Work/Clients/<FOLDER>` or `~/mnt/nas-archive/Work/Projects/<FOLDER>`. Not in Sprint 1 scope beyond the one top-5 grocery chain.

Archetype summary of the folders found:

- **Big-box US general-merchandise retailer** — Secure 3.2 client (referenced in Secure Lite docs)
- **UK luxury department-store flagship** — non-US Secure client
- **US office-supply chain** — Secure Store Management Reports SOW referenced in NAS Unsorted/Downloads
- **US toy-retail chain** (+ related sister folder) — Secure client (pre-bankruptcy era)
- **Heartbeat / Fireball 2002** — Secure-adjacent prior-art product; full deep-dive planned per `docs/playbooks/playbook-heartbeat-blueprint.md`
- **US sporting-goods retailer (sports specialty)** — Secure client (pre-bankruptcy)
- **Retek** — pre-Secure partner (merchandising system implementations — product vendor, not client per se)
- **SAP** + **SAP Retail** — pre-Secure partner (product vendor)
- **Top-5 US grocery chain** — Secure 3.5 client; covered in [[Brain/wiki/secure-client-top5-grocery-chain|Secure Client: Top-5 Grocery Chain]] (2017 engagement)
- **Canadian grocery conglomerate** — multi-brand Canadian grocery group
- **US state liquor control board** — public-sector beverage retailer
- **PB** — unclear abbreviation (possibly Pitney Bowes or other)
- **UK town engagement codename** — regional engagement, UK retailer HQ location
- **TODAYMAN** — unclear codename
- **MCS Better Business** + **MCS Project Assessment** — MCS consulting partner
- **US specialty apparel chain** — 2002-era IBM retail consulting (pre-Secure)
- **IBM Method Web** — IBM internal methodology
- **NOTES**, **RETAIL** — generic cross-cutting folders

### Where NAS content actually lives

The larger archive at `~/mnt/nas-archive/` contains:

- `Work/Clients/<CLIENT>/` — engagement folders for Secure + pre-Secure clients (top-5 grocery chain, Secure 5 archetype, other referenced but not yet enumerated)
- `Work/Projects/<PROJECT>/` — project folders (top-5 grocery-chain procurement project seen)
- `Work/Recovered/Secure Files/` — small (16K), possibly fragments
- `Email/CLIENTS/SECURE 5/` — email context, small
- `Reference/` — mixed: retail LP reference PDFs (Appriss Retail Data Spec v1.2, CRDM Deployment Guide, Secure Store Feature Sheet for Cashier Coaching, Baseline Case Resource Plan, a Southeastern US department-store chain Resource Plan, Delivery Framework 2013, LPMS Open Interface) interleaved with a lot of non-retail personal content
- `Unsorted/` + `Unsorted/Downloads/` — large, mixed (Sysrepublic SOWs, big-box-retailer Secure 3.2 Quick Start Guide, specialty-electronics-chain Secure Store SOW, Crime Bulletins)

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
- Southeastern US dept-store Resource Plan
- Baseline Case Resource Plan
- Cashier Perf Baseline Plan
- Limited Secure 3 Resource Plan

**Methodology / agent-team playbook material:**

- Delivery Framework v1.2 2013
- Delivery Resources Oct 2016
- Consultant Certification in BCS (120905)
- Efficient Item Assortment 2003.5 Road Map

**Client-specific content** (beyond the top-5 grocery chain):

- **Southeastern US dept-store chain** — Resource Plan, full engagement content
- **Big-box US general-merchandise retailer** — Secure 3.2 Quick Start Guide
- **US consumer-electronics chain** — Secure Store Management Reports SOW
- **US drug-store chain** — Secure Order Form 09-30-18
- **Top-5 US grocery chain** — additional content (Appriss Order Form for Secure Store EBR Core, encrypted)

### Why deferred to a future sprint

Sprint 1 scope is the curated `~/secure/` content (Secure product docs + top-5 grocery chain as first client). The broader NAS is:

1. **Much larger** — hundreds to thousands of files
2. **Less curated** — mixed with personal content (real estate, financial, family)
3. **Requires PII gate** — a clean extraction needs per-file PII classification before anything reaches `Brain/raw/inbox/`. Sprint 1 hit a PII incident where a bulk-extract leak captured a personal credit report and closing disclosure into the scratch dir before they were caught and deleted. The future NAS sprint needs this gate built into the `extract` command by default, not as a post-hoc manual review.
4. **Separate deliverables** — treasures here become SDDs, FR docs, agent-team playbooks, methodology guides (see [[Brain/projects/Secure|Secure MOC]] "Future Work" section)

## Related

- [[Brain/projects/Secure|Secure]] MOC
- [[Brain/wiki/secure-client-top5-grocery-chain|Top-5 Grocery Chain Deep-Dive]] — the one Secure-era client covered in Sprint 1
- [[Brain/wiki/secure-platform-overview|Secure Platform Overview]] — product line this career built
- [[Brain/wiki/secure-retail-operating-model-2006|Retail Operating Model 2006]] — sibling IBM-era engagement (UK global grocer)
- [[Brain/wiki/secure-property-services-operating-model-2002|Property Services Operating Model 2002]] — sibling IBM-era engagement (UK dept-store + grocery group)

## Sources

Folder paths retain original client-folder names as source-of-record per `feedback_scrub_client_names.md`.

- `/Users/gclyle/secure/PROJECTS/` — local enumeration via `find ... -type f | wc -l`
- `/Users/gclyle/mnt/nas-archive/Work/`, `Reference/`, `Unsorted/` — NAS structure observed during top-5 grocery-chain extraction (not ingested)
