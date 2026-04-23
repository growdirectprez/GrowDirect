---
date: 2026-04-22
type: wiki
tags: [growdirect, warchest, founder-story, ibm, lanehawk, tlog]
sources:
  - docs/_archive/ip-vault/warchest/sources/01-founders-case.md
last-compiled: 2026-04-22
needs-review: 2026-05-06
---

**Wiki:** [[Brain/Home|Home]]

# The Founder's Case
*Spine: ACT 2A–2C | Manifesto: I.1, I.2, I.3*

**Status:** 📝 DRAFT — Extracted from PhD tLogToGlog Founder Case v1.0 + Manifesto I.1-I.3. Partial — awaiting B-056 evidence (IBM emails, LaneHawk docs, Palisades photos).

---

## The tLog Problem

IBM created the transaction log — the tLog — as the universal record of everything that happened at a point-of-sale terminal. For thirty years, the IBM 4690 format defined retail. Every sale, refund, void, and cash event began as a line in the tLog. IBM held more than 70% of grocery, drug, and mass merchant POS infrastructure throughout the 1990s. The tLog was the industry standard payload. It was also fundamentally broken.

The IBM 4690 operating system included a configuration that dropped sequential transaction records without detection. In normal operation, the system produced gaps in the transaction sequence — records that simply vanished. No error. No alert. No trace. The data was gone, and nobody could tell it had ever existed.

The consequences were human. Loss Prevention departments relied on the tLog as the source of truth for employee activity. When records went missing — due to system configuration, hardware failures, or integration errors — LP interpreted the gaps as evidence of fraud. Employees were accused of stealing based on corrupted data. Careers were damaged. Livelihoods were threatened. The accusations were wrong, but the system provided no way to prove it.

The problem was never the people. The problem was the log.

## The LaneHawk Incident

One of the most damaging failures occurred when under-basket scanning technology was integrated into the 4690 platform. The integration created field length overflows in the packed hexadecimal BCD format — the encoding the tLog used for transaction data. Fields silently truncated. Records corrupted. Transactions vanished from the log. Loss Prevention flagged the missing records as theft. It was not theft. It was a crashed field length in a fragile binary format that had never been designed for third-party integration.

The founder lived this. He built the enterprise systems that processed the tLog. He defended himself and others against accusations based on data the system itself had corrupted. He spent sleepless nights proving that the gaps were engineering failures, not human failures.

*[B-056: Evidence pending — IBM accusation/resolution emails, LaneHawk integration incident docs. These primary sources will strengthen this section when recovered.]*

## The Thirty-Year Through-Line

The founder trained at IBM's Advanced Business Institute in Palisades, New York, where the corridor from lobby to classroom traced the arc from the Dayton Scale Company meat slicer to the Apollo mission control mainframe to the personal computer. He then went on to build enterprise retail systems — the transaction processing infrastructure that handled millions of daily events for the largest retailers on the planet.

His career spans the entire evolution of retail technology. Strategy consulting at a Big Four firm in the mid-1990s, writing industry-defining research on where retail technology was headed. Enterprise systems integration at the world's largest technology company, building the Oracle, EDI, and POS infrastructure that processed the transaction stream. Then co-founding the SaaS platform that aggregated more private retail transaction data than any system in the industry — running exception-based reporting across billions of transactions before cloud computing had a name.

He watched that data get locked in silos. He watched it get disputed in courtrooms. He watched it vanish when companies changed hands and servers were decommissioned.

The gLog — Geoffrey's Log — is the permanent successor to the tLog. Where the tLog lived on institutional servers — mutable, deletable, and controlled by whoever owned the hardware — the gLog lives on Bitcoin. The record cannot be altered. Cannot be deleted. Cannot be silently dropped and blamed on an employee.

This is not a pivot. It is a culmination. Thirty years from the meat slicer museum to the permanent ledger.

---

**Source:** PhD tLogToGlog Founder Case v1.0 + Manifesto I.1, I.2, I.3
**Blocked by:** B-056 (evidence hunt — IBM emails, LaneHawk docs, Palisades photos)
**Manifesto tag:** `Manifesto: I.1, I.2, I.3`
**Filled:** February 27, 2026 — ALX (B-059 Phase 1)

## Related

- [[Brain/projects/GrowDirect|GrowDirect MOC]]
- [[Brain/wiki/growdirect-working-papers|Working Papers Structure]]

## Sources

- `docs/_archive/ip-vault/warchest/sources/01-founders-case.md` — the war-chest source this card summarizes
