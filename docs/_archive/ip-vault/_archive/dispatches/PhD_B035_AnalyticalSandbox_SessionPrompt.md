---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# PhD Session Prompt — B-035 Analytical Sandbox + Query Governor Brief
*Dispatch: ALX | February 26, 2026*

---

PhD — two documents to read before you start. Both are required context.

**Read first:**
1. `Canary_IP/Markdown/Strategy/Canary_Data_Strategy_NorthStar_v1.1.md` — the full document, particularly the new section **"The Standardization Paradox"** and the updated Layer C+ architecture.
2. `_ALX/WorkOrders/B035_Addendum_TemporalPartition_QueryGovernor.md` — the full architecture brief.

---

## The Core Insight You're Validating

> *All retail is the same. It is how merchants want to spin their data that makes them unique — and makes standardization hard. If we start correctly, we can do both.*

The CRDM schema is canonical and fixed across every merchant. What varies is the analytical lens — the temporal grain, the retention window, the comparison period that matches how each merchant type thinks about their business. Your job is to validate and extend this framework theoretically, then define the analytical sandbox that will generate the industry benchmarks only GrowDirect can produce.

---

## Deliverable 1: Spectrum Validation — Do Three Grains Cover All of Retail?

The proposed temporal grain options are: **hour / day / week.**

These map to:
- Hour → QSR, coffee, high-volume food service (daypart thinking)
- Day → general SMB retail (daily shrink review, days-of-supply)
- Week (NRF 4-5-4) → seasonal retail, fashion, grocery (sell week thinking)

**Your question:** Does this three-grain system cover the full SMB merchant spectrum accessible through Square without meaningful gaps? Are there merchant archetypes that think in a grain this system cannot serve? (Consider: salons, service businesses, event-driven retail, market stalls, food trucks.)

If gaps exist: recommend whether they are served by an existing grain with different retention windows, or whether a fourth grain is warranted and what the operational cost is.

Produce: one-page spectrum assessment. Merchant archetypes mapped to grain. Gap analysis. Recommendation.

---

## Deliverable 2: The Query Governor as Economic Mechanism

Tom is designing the query governor as a **technical constraint** — Superset dataset permissions, mandatory time bounds, row limits. This prevents unbounded queries (`SELECT *.*`) from degrading system performance.

Your question: can this also function as an **economic constraint** consistent with the Dome architecture?

The framing: an unbounded query is a form of resource debasement — it consumes shared infrastructure without proportional value exchange, exactly as monetary inflation consumes purchasing power without proportional economic output. The technical limit addresses the symptom. The economic limit addresses the incentive.

**Assess the L402 model:** API calls within the base tier (bounded, materialized views, standard windows) are free. Calls beyond the base tier — wider time windows, higher row counts, raw partition access under enterprise contract — cost sats via L402 micropayment. This creates:
- A natural tier structure aligned with the Dome philosophy
- Economic irrationality for unbounded queries (they cost money)
- A revenue stream from heavy API users (third-party developers building on the CRDM)

**What you need to produce:**
- One-page economic governor assessment: does L402 tiering work as complement or alternative to the technical constraint model?
- Proposed tier structure: what does the free tier include, what does the paid tier unlock, what does enterprise unlock?
- Revenue model sketch: at 1,000 merchants with 10 third-party apps each making 100 API calls/day above the free tier at 10 sats/call — what does that look like annually at current BTC price?

---

## Deliverable 3: Layer C Anonymization Boundary

The materialized view tier (Layer C) is computed from Layer A (raw merchant partitions) by Airflow/dbt. The rule: no PII, no card fingerprints, no employee names, no merchant-identifiable detail crosses this boundary.

**Your question:** is the proposed anonymization boundary sufficient, or are there aggregation attacks that could re-identify merchants or individuals from Layer C data?

Specifically:
- Can `mv_daily_summary` at the merchant level be reverse-engineered to identify individual transactions or employees? (Small merchant with 2 employees and 30 transactions/day is not statistically anonymous.)
- At what merchant size / transaction volume does aggregated data become genuinely anonymous?
- What additional suppression rules are needed? (Minimum cohort size before a metric is reported? Differential privacy noise injection? K-anonymity threshold?)

Produce: anonymization boundary specification. What fields are stripped/hashed before Layer A → Layer C. Suppression rules. Minimum cohort thresholds for Layer C+ benchmark reporting.

---

## Deliverable 4: Layer C+ Sandbox Scope Definition

You are the primary user of the Layer C+ analytical sandbox. Before Syd can draft the consent language that gates merchant participation, she needs to know what questions you intend to answer with it.

**Define the research agenda:**
- What industry benchmarks does GrowDirect need to produce to be credible with investors, enterprise buyers, and press? (e.g., "SMB cash variance rates by vertical," "Chirp signal-to-noise by merchant type," "shrink rates by geography and season")
- What is the minimum merchant cohort size to produce statistically meaningful benchmarks in each category?
- What is the data you need access to — which Layer C materialized views, what time windows, what aggregation grain?
- What are you explicitly NOT doing with the sandbox? (This feeds Syd's consent language — the scope must be bounded.)

Produce: Layer C+ sandbox scope document. Research agenda. Minimum cohort requirements. Data access specification. Explicit exclusions. This feeds directly into Syd's consent language drafting — be precise.

---

## Output Files

1. `_ALX/WorkOrders/output/PhD/PhD_B035_SpectrumValidation.md` — three-grain coverage assessment
2. `_ALX/WorkOrders/output/PhD/PhD_B035_QueryGovernor_Economic_Assessment.md` — L402 economic governor model
3. `_ALX/WorkOrders/output/PhD/PhD_B035_AnonymizationBoundary.md` — Layer C anonymization spec
4. `_ALX/WorkOrders/output/PhD/PhD_B035_SandboxScope.md` — Layer C+ research agenda (feeds Syd)

---

## Deliverable 5: The Timestamp Layer — Theoretical Framework

Read the North Star v1.1 section **"The Timestamp Layer"** before writing this deliverable. The architecture is defined there. Your job is the theoretical framing that makes it investable, legally credible, and philosophically coherent.

**Jeffe's directive, February 26, 2026:**
> *"We are giving the little guy FBI level evidence. We don't have to even be involved. We are just helping them timestamp their network."*

This is the product vision. Everything below serves it.

**Three things PhD produces:**

**1. The protocol framing**
This is not a Layer 2 solution. Not a sidechain. Not a token. It is Bitcoin L1 used for exactly what the whitepaper describes: a timestamp server that proves a piece of data existed at a specific time, secured by proof-of-work. Every layer beyond L1 introduces a trust assumption an attorney can challenge. L1 introduces none. Write the one-page explanation that a non-technical investor, a federal attorney, and a skeptical Bitcoin maximalist all find credible. They have different objections. Address all three.

**2. The evidentiary argument**
When a merchant's records are anchored to Bitcoin via Ordinals inscription, what exactly is proven? Walk through the verification chain: raw event hash → Merkle tree → Merkle root → on-chain inscription → block timestamp → proof-of-work chain. What legal standard does this satisfy? What does it exceed? What does it not prove (Canary still asserts the hash was computed correctly — the inscription proves it hasn't changed since, not that it was correct to begin with)? Be precise. Syd will build on this.

**3. The justice framing for investors**
Satoshi built trustless verification of events in time. Every major use case since has been about money. Canary applies it to something older than money — evidence. The record of what happened, when it happened, that no one can dispute. Not a crypto product. A justice product. Available to a coffee shop owner for pennies a day. Write the 200-word investor narrative that opens with this framing and closes with the Gucci/LVMH enterprise implication. This goes in the pitch deck.

**Output:** `_ALX/WorkOrders/output/PhD/PhD_B035_TimestampLayer_Framework.md`

---

## Coordination Notes

- **Tom** is running in parallel on the partition DDL and Superset/dbt stack. You are not blocked on Tom and Tom is not blocked on you. ALX converges both outputs.
- **Syd** will receive your Sandbox Scope document as input for consent language drafting. PhD scope → Syd consent → sandbox goes live. That is the sequence.
- **The Standardization Paradox section** in the North Star v1.1 is yours to challenge if the theoretical framing is wrong. If the three-grain model has gaps, say so now before Tom writes DDL.

---

## Deadline

Sprint 6 architecture decision. Not a Phase 1 blocker. Must resolve before Phase 2 (first real merchant) so the partition template and consent framework are correct before real data flows.

---

*ALX | Chief of Staff | February 26, 2026*
