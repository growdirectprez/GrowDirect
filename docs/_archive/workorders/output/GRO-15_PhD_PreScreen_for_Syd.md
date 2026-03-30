---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# GRO-15 — PhD Research Files Pre-Screen for Syd

**Prepared By:** ALX (Chief of Staff)
**Date:** March 2, 2026
**Purpose:** Accelerate Syd's legal review of PhD's research output (41 files in `_ALX/Workorders/output/PhD/`)
**Gate:** Syd must review and sign off before any file is shared externally or integrated into investor materials.

---

## Priority 1 — Must Read (6 files)

| File | Summary | Legal Flags | Action |
|------|---------|-------------|--------|
| **B077_PhD_ReviewPackage_Jeffe_Syd.docx** | Word doc explicitly prepared for Jeffe + Syd review. Contains the B-077 work order package. | Primary legal review package. Contains 6 flagged legal questions from RaaS section. | **READ FIRST** — This is Syd's named deliverable. |
| **PhD_B077_RaaS_ManifestoSection_IV3.1.md** | Receipt-as-a-Service manifesto section. Defines `POST /verify` and `GET /receipt` API endpoints gated by L402 micropayments. | **Regulatory classification**: Is RaaS a notary service? Money transmitter? Data processor? API serves auditors, insurers, regulators, law enforcement. | **READ IMMEDIATELY** — 6 legal questions explicitly routed to Syd in routing section. |
| **PhD_B053_ComplianceByConstruction_Brief.md** | Claims Bitcoin layer "eliminates the HIPAA/PCI-DSS attack surface." Positions compliance as architectural rather than procedural. | Investor-facing compliance claims need legal vetting. "Eliminates attack surface" ≠ "HIPAA compliant." Routing says "Syd (legal review — approve language before any external use)." | **READ SECOND** — Reframe language before Jess integrates into investor site. |
| **PhD_StagedImmutability_PatentSchematic_v1.0.md** | Patent schematic for universal webhook notarization. Claims 7 novel elements. References provisional patent 63/991,596. | Non-obviousness claims, patent-eligible subject matter under 35 U.S.C. § 101, prior art positioning. | **READ FOR IP** — Coordinate with patent counsel before finalizing. |
| **PhD_B071_GrowDirectProtocol_PositionPaper_v1.0.md** | Wrapped BTC treasury, DAO governance (3-phase), Avalanche sidechain architecture. Claims "7 novel patent claims extending provisional filing." | DAO token = potential security under SEC guidance. Bridge custody risk (Avalanche Bridge, THORChain, Wormhole). Routes to Syd for patent claims + DAO compliance. | **READ FOR TREASURY + DAO** — Securities classification and bridge risk. |
| **GrowDirect_Manifesto_v1.1_FINAL.md** | Master manifesto for investors. All architectural, regulatory, and moat claims in one document. | Multiple claims: "courts begin requiring cryptographic timestamps," "compliance by construction," "regulatory moat." All need qualification. | **SKIM FOR REGULATORY CLAIMS** — Focus on Part II.3 (Trust Collapse) and Part VI (The Moat). |

---

## Priority 2 — Skim (4 files)

| File | Summary | Legal Flags | Action |
|------|---------|-------------|--------|
| **PhD_StagedImmutability_BitcoinFrame_v1.0.md** | Investment thesis: "Bitcoin solved money; this solves events." Capital allocation thesis, perpetual revenue claims. | Investor-facing claims about asset appreciation and regulatory moat ("governments will prefer immutable records"). Needs qualification. | Skim for investor claim language. |
| **PhD_BitcoinProtocol_PositionPaper_v1.0.md** | Strategic positioning on Bitcoin's regulatory resilience. Ordinals legitimacy within consensus. | Claims about government pressure resistance and Bitcoin's "uncapturability." Verify no sanctions evasion territory. | Skim Section 5 ("Why It Has To Be Bitcoin"). |
| **PhD_B054_InvestorSiteCopy_v1.0.md** | Condensed investor briefs for website. VeriSign parallel, block space moat, perpetual revenue. | Routes to Syd: "Syd reviews → Jess builds Section 03b." Antitrust risk in block space monopoly claims. | Skim before Jess integrates. |
| **PhD_VeriSign_Analogy_InvestorBrief.md** | Compares GrowDirect to VeriSign. Claims about 2010 breach, DigiNotar, $21B valuation. | Factual claims need verification. VeriSign trademark/IP exposure if analogy overreaches. Routes to Syd for fact-check. | Fact-check financial figures and dates. |

---

## Priority 3 — Skip (31 files)

These are technical theses, economic models, alignment audits, or narrative content with no direct legal exposure. Syd can reference on demand.

Key categories:
- **PhD_Layer5_*.md** (6 files) — Economic theses on block space, fee windows, genesis pool capital. Technical, not regulatory.
- **PhD_B069_*.md** (2 files) — Hybrid chain economics, validator compensation. Reference only if DAO/token review needed.
- **PhD_B076_*.md** (3 files) — Metcalfe's Law, convergence analysis, position paper drafts. Technical foundation.
- **PhD_B054_Brief5_TlogToGlog_*.md** (2 files) — Transaction-to-global-log narrative. Historical.
- **PhD_Alignment_Brief.md** — Product audit, not legal content.
- **Patent visualization HTMLs** (4 files) — Visual aids for patent filing. IP-adjacent but no new claims.
- **GrowDirect_TechAssessment_*.md/.html/.docx** — Technical assessment, not legal.
- **PhD_MerchantWeapon_Brief_v1.0.md** — Merchant positioning narrative.
- **PhD_tLogToGlog_FounderCase_v1.0.md** — Founder narrative.
- **GrowDirect_Manifesto_Investor.html** — HTML render of manifesto (same content as FINAL.md).
- **GrowDirect_MermaidAtlas_v1.0.md** — Diagram atlas.
- **GrowDirect_ResearchPaperRoadmap_v1.0.md** — Research planning doc.

---

## Top 7 Legal Concerns (for Syd's Triage)

1. **RaaS Regulatory Classification** — Is `POST /verify` a notary service, money transmitter, or data processor? Serves auditors, insurers, regulators. Clarify before external positioning.

2. **"Compliance by Construction" Language** — B053 claims Bitcoin layer eliminates HIPAA/PCI attack surface. Technically defensible but legally risky if claimed as full compliance. Reframe to "eliminates on-chain attack surface."

3. **Patent Non-Obviousness** — 7 novel elements claimed in staged immutability patent. Provisional 63/991,596 filed. Coordinate with patent counsel on examiner risk.

4. **DAO Tokens as Securities** — B071 describes governance tokens with voting + economic rights. Likely securities under SEC guidance. Get formal opinion.

5. **Wrapped BTC Bridge Risk** — Treasury uses Avalanche Bridge (BTC.b). Who holds keys? What if bridge is hacked? Legal review of custody + insurance.

6. **Regulatory Moat Claims** — Multiple docs state "regulators will prefer immutable records" as fact. Must qualify with "as regulatory frameworks evolve" language.

7. **VeriSign Analogy Accuracy** — Investor brief makes specific claims about 2010 breach, DigiNotar, $21B valuation. All must be fact-checked before external use.

---

## Files Explicitly Routed to Syd in PhD Work Orders

- B077 RaaS Section — 6 legal questions flagged
- B053 Compliance by Construction — Approve language before external use
- B054 Investor Site Copy — Syd reviews → Jess builds
- B071 Protocol Position Paper — Patent claims + DAO governance
- VeriSign Analogy Brief — Fact-check before external use

---

*ALX | GRO-15 | March 2, 2026*
