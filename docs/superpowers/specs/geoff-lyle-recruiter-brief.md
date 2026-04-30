---
date: 2026-04-30
type: recruiter-brief
status: draft-v0.1
classification: confidential
audience: executive-recruiter
purpose: Profile build for consulting firm placement, strategic partnership, or advisory engagement
---

# Geoff Lyle — Executive Profile Brief

## Who He Is

Geoff Lyle is a retail technology architect and practitioner with 25+ years of hands-on delivery across the full retail technology stack — from the integration backbone to the analytics layer to the loss prevention platform. He has built and sold packaged software, written the functional specifications that became production systems at global grocery chains, led enterprise retail transformation programs across the US and UK, and is now building the next generation of the platform from the ground up.

He is not a generalist technology executive. He is a retail domain expert who also writes code.

---

## The Method

Lyle developed a retail transformation methodology — now formalized as **CATz** (the Canary Analytical Transformation methodology) — through two decades of engagements spanning grocery, fashion, specialty, home improvement, and pharmacy. The method addresses the recurring failure mode in retail technology programs: the gap between what a system is designed to do and what a retail operator can actually use.

CATz is structured around three accountability rails that every retail operation must close:
- **Operational** — no unknown inventory loss
- **Financial** — authorized spend only, constrained by open-to-buy
- **Evidentiary** — every record is hashed, traceable, and portable

The methodology is documented in a living knowledge base of 385+ embedded documents — the Canary Retail Brain — covering the full retail module spine (13 modules from Item through Finance), integration patterns, prior-art case studies, and deployment playbooks.

---

## The Platform He Built

**RTI — Real Time Integrator.** A BizTalk-based retail integration backbone built and sold through **Sysrepublic Ltd** (Nottingham, UK), Lyle's trans-Atlantic technology partner. RTI connected POS systems, merchandising platforms, and analytics layers in real time — the integration substrate that made loss prevention analytics operational rather than batch.

RTI is the predecessor to what Lyle is building today: **Canary Go**, a Go/GCP implementation of the same architectural principles, rebuilt for the cloud-native era with a 13-module retail spine, Lightning Network payment rails, and a Bitcoin-standard cost model.

**The platform in production:**
- RTI processed live POS data feeds from multiple retail formats simultaneously
- The exception-based reporting (EBR) layer surfaced loss events in real time
- Sysrepublic's xBR (exception-based reporting) platform, deployed at US and UK retailers, was the commercial expression of RTI's integration and analytics architecture

---

## Grocery Client Roster

### United States

| Client | Nature of engagement |
|---|---|
| **Kroger** | LP influence across all Kroger divisions — Secure Store EBR and RTI rolled out division-wide for near-real-time POS data analysis; RFP, architecture, SOW, POS baseline, DSD requirements; Retek project. Engagement was LP-scoped (not enterprise IT), but divisional coverage was complete. |
| **Safeway** | Secure Store SOW; implementation planning |
| **Albertsons / Fred Meyer** | Analytics and LP engagement |
| **Southeastern Grocers (SEG) / BI-LO** | Secure Store implementation — LP program designed with SEG LP leadership; Beck Total Retail Loss framework operationalized in production |
| **Schnucks** | CCTV-integrated LP analytics (Salient CCTV SOW) |
| **The Fresh Market (TFM)** | Secure Store implementation — RFP, SOW, implementation schedule |
| **WinCo Foods** | LP analytics engagement |
| **Wegmans** | Encryption and data security design |
| **Save Mart** | LP analytics |
| **Fresh & Easy (Tesco US)** | Oracle Retail implementation; Tesco Technical Library (TTL) functional specification — **founder is named document author** |

### United Kingdom and International

| Client | Nature of engagement |
|---|---|
| **Tesco UK** | Tesco Technical Library (TTL) — private-label product specification platform deployed across 1,700+ UK supplier sites and 4,000+ stores |
| **Marks & Spencer** | Fireball / Heartbeat — the major M&S loss prevention program; the largest UK LP engagement in the portfolio |
| **Sainsbury's** | LP analytics engagement |
| **Morrisons** | Retail operating model engagement (Swindon project) |
| **Waitrose** | LP analytics |
| **Delhaize** | Belgian grocery group |
| **Coles** | Australian grocery |
| **Jumbo** | Netherlands grocery |
| **ICA** | Swedish grocery |

**The grocery client roster spans Tier-1 grocery in the US, UK, Europe, and Australia — built over two decades of integrated platform delivery, not advisory work.**

---

## Broader Retail Client Roster (Selected)

The grocery practice sits inside a broader retail technology portfolio spanning:

- **Fashion / Apparel**: Gap, H&M, C&A, Zeeman, Laura Ashley, Belk, Limited, Zales, Zumiez
- **Home / DIY**: Lowe's, Floor & Decor, Orchard Supply (Lowe's), BCF
- **Specialty**: PetCo, Shoe Sensation, RadioShack, T-Mobile, Best Buy, Hallmark
- **Department**: JCPenney, C. & J. Clark (Clarks UK)
- **Food Service / Travel**: SSP (airport food)
- **International**: Alshaya (Middle East franchise), Lulu (UAE hypermarket), Selco (UK builders merchant)
- **Public Sector**: Pennsylvania Liquor Control Board

---

## Scale — What the Platform Processes

**Tesco UK:** The Technical Library platform Lyle specified (2006) underpinned private-label product compliance for 1,700+ UK supplier sites and is deployed across Tesco's 4,000+ store estate. Tesco UK processes approximately 40 million customer transactions per week — roughly 800 million per year, 8+ billion over the last decade in UK alone. The TTL platform sits in the specification chain behind every private-label item in every transaction.

**US grocery:** Kroger alone operates 2,700+ stores processing approximately 9 million daily transactions. The Secure Store / RTI integration layer Lyle architected processes the exception-based reporting stream from those POS systems — every transaction is a candidate event for the detection model.

*Precise lifetime transaction volumes to be confirmed from Tesco and Kroger annual reports. Working estimate: the platform's integration and analytics surface has touched 10+ billion retail transactions across its deployment history.*

---

## What He Is Building Now

**GrowDirect / Canary Go** — a Go/GCP implementation of the same retail spine, rebuilt cloud-native, with:

- 13-module retail architecture (Item, Organization, Transaction, Distribution, Value, Merchandising, Space, Finance, Customer, Loss Prevention, Labor, Device, Work Execution)
- Lightning Network (L402) payment rails — open-to-buy as a provenance-stamped wallet constraint
- Bitcoin-standard cost accounting — IL(Device/MCP/Port/)WAC, the first retail cost model with agent, device, and POS-connector provenance dimensions
- RaaS (Resolution as a Service) — portable merchant identity across POS systems
- EJ Spine (Electronic Journal) — immutable, hash-chained transaction record

**The thesis:** the same algorithms that IBM is building for Tier-1 retailers at $2-5M per-store investment — running on the POS data the SMB retailer already generates. No sensors. No enterprise OMS. Just the Square webhook and the method.

---

## What a Consulting Firm Acquires

A firm that acquires Lyle and the GrowDirect portfolio gets:

| Asset | What it is |
|---|---|
| **The person** | 25 years of hands-on retail technology delivery at the largest grocery chains in the US and UK. Not an advisor. A builder who has shipped. |
| **The method** | CATz — a documented, agent-queryable transformation methodology. Not a deck. A living knowledge base. |
| **The prior art** | 20 years of engagement artifacts — functional specs, SOWs, implementation plans, RFP responses — across every major retail format. |
| **The platform** | Canary Go — a production-ready retail spine with LP, OTB, EJ Spine, and Bitcoin-standard cost accounting. No competitor has this combination. |
| **The agent infrastructure** | ALX (Canary Retail Ops Agent) — an AI-native delivery model that runs the methodology at 10x the efficiency of a traditional consulting engagement. |

---

## Contact

**Geoff Lyle**
GrowDirect LLC
bonsallprotea@gmail.com

---

*Draft v0.1 — 2026-04-30. Volume figures to be confirmed from public annual reports. Client list compiled from MyPassport archive and NAS engagement records. Subject to PII review before external distribution.*
