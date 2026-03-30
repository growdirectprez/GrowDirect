---
type: research
domain: protocol
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Investor Site Copy — Brief 5: From tLog to gLog
*PhD Research Framework | B-058 Deliverable | February 27, 2026*
*Classification: MAXIMUM CONFIDENTIAL — Investor-Facing Copy*
*Supersedes: PhD_B054_Brief5_TlogToGlog_v1.0.md*
*Routes to: Jess (Section 03b build), Syd (legal review before any external use)*

---

## Brief 5: From tLog to gLog — The Permanent Transaction Log

**Pull quote:** *"IBM had the tLog. Geoffrey built the gLog."*

For thirty years, every retailer on earth ran on the transaction log. The IBM 4690 tLog was the industry standard — the atomic record of every sale, refund, void, and cash event. It was also mutable, deletable, and controlled by whoever owned the server. Non-journal mode dropped records without detection. Integration failures corrupted payloads silently. Loss Prevention accused employees of fraud based on data the system itself had destroyed.

The gLog is the permanent successor. Every POS event is hashed to strip personal data, then inscribed as a Bitcoin Ordinal through the elJeffe API at jeffe.io. Block height provides a global timestamp no one controls. Each inscription chains to the prior entry, creating a complete, replayable merchant history on the most secure ledger ever created.

The founder built the transaction processing infrastructure for the world's largest retailers. He co-founded the SaaS platform that aggregated more private retail transaction data than any system in the industry. He witnessed the tLog's failures firsthand — spent sleepless nights under accusation for data the system had dropped.

Now he is making the transaction log permanent. Not by trusting better institutions, but by removing the need for trust entirely. The record lives on Bitcoin. Forever.

---

## Integration Notes for Jess (B-058 Build)

**Section 03b layout:** Brief 5 anchors the thesis section — the "why this founder, why now" argument. Recommended as the first card in the sequence, framing the four investment thesis briefs that follow.

**Card-ready elements:**
- Pull quote: prominent display
- tLog → gLog lineage: IBM 4690 (1986–2017) → elJeffe gLog (2026–∞)
- Career arc: Big Four consulting → IBM enterprise systems → SaaS pioneer → Bitcoin-native

**Voice:** Same as Briefs 1–4. Confident. Sparse. The mechanism is the pitch.

---

*PhD Research Framework | February 27, 2026*
*Output: `_ALX/WorkOrders/output/PhD/PhD_B054_Brief5_TlogToGlog_v2.0.md`*
*Sequential gate: This copy → Syd reviews → Jess builds Section 03b*
