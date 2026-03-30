---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# B-068 — Foundation Layer: Presentation + Localization + Partitioning Architecture
## Master Dispatch — Five-Lane Parallel Build

**Work Order:** B-068
**Date:** February 28, 2026
**Dispatched by:** ALX
**Priority:** 🔴 CRITICAL — Foundation. Everything else is built on this.
**Directive:** Jeffe — "If this is right we can make any app. We need a white paper so we
don't lose the intellectual provenance."

---

## The Unified Principle

Read this before any lane executes:

```
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/PhD/
  GrowDirect_UnifiedArchitectureThesis_v1.0.md
```

This is the primary source document. It establishes that the five lanes of this work order are
not five separate decisions. They are one decision — merchant-first isolation — expressed
simultaneously at the Bitcoin layer (patent), the Postgres layer (partitioning), and the
presentation layer (vocabulary packs).

**The central claim:**
The partition is the hash chain is the vocabulary pack. Each merchant's state is bounded,
independent, and portable at every layer. Get this right and any app can be built on top of it.
That is the precise technical meaning of Jeffe's phrase.

---

## Five Lanes

| Lane | Agent | Task | Depends on |
|---|---|---|---|
| **E** | PhD | White paper — unified architecture thesis | Nothing — write first |
| **A** | Tom | Postgres partition architecture + gLog investor paragraph | Lane E brief |
| **D** | Tom | `merchant_vocabulary` DB schema + resolution function | Lane E brief |
| **B** | Condor | Blueprint v2.0 — strip display strings, replace with token keys | Lane E brief |
| **C** | Condor | en-US.json + vocabulary JSON files | Lane B token registry |

**Lane E is complete.** White paper written and on disk. Tom reads it before Lane A or D.
Condor reads it before Lane B. Lane C waits on Lane B's token registry.

---

## LANE E — PhD: Unified Architecture White Paper ✅ COMPLETE

**Output:** `_ALX/WorkOrders/output/PhD/GrowDirect_UnifiedArchitectureThesis_v1.0.md`
**Status:** Written February 28, 2026 by ALX (ALX wrote this directly — intellectual
provenance required immediate capture before execution fragmented the threads).

**What it establishes:**
- The five claims that constitute the unified thesis
- The multithreaded development provenance (four parallel threads, convergence Feb 28)
- The tLog failure analysis as the problem statement
- The UTXO parallel as the mathematical foundation
- The VeriSign frame as the investor argument
- The "any app" claim grounded in three independent proofs
- The primary source document index for patent counsel and investors

---

## LANE A — Tom: Partition Architecture

**Session prompt:** `Tom_B068A_PartitionArchitecture_SessionPrompt.md`
**Read first:** `GrowDirect_UnifiedArchitectureThesis_v1.0.md` — specifically Section 3.2

**The framing Tom must hold:**
The partition is not a performance optimization. It is the Postgres expression of the
hash chain principle. The same mathematical property that makes the Bitcoin pipeline
scale linearly — per-merchant independence of state — must be expressed in the SQL
layer for the same reason: damage boundedness, archival precision, and horizontal
scaling without global lock contention.

**Decisions Tom must make and document:**

1. **Composite partition key:** Evaluate and decide between:
   - Period only (current spec — insufficient, all merchants share partition)
   - Merchant × Period (recommended — true isolation)
   - With flexible granularity: monthly (SMB default) vs quarterly (enterprise override)
     stored in `merchants.partition_config JSONB`

2. **Naming convention:** `txn_{merchant_id}_{year}_{period}` — establish the standard

3. **DDL:** Complete `CREATE TABLE` with child partition definitions

4. **Scope extension:** Apply same decision to new tables from E1-F6 through E1-F11:
   `cash_drawer_shifts`, `transaction_line_items`, `transaction_tenders`,
   `gift_card_activities`, `inventory_adjustments`, `employee_timecards`

5. **Archive path:** DROP PARTITION strategy for cold storage. S3/Glacier path.

6. **Hash chain alignment:** Confirm partition boundary aligns with Sub 1 evidence store
   — each merchant's hash chain lives within their partitions, never crossing boundaries

7. **The gLog investor paragraph:** One paragraph explaining the partition-per-merchant
   strategy as a scaling story. Not technical. See white paper Section 3.2 for framing.

**Output:** `Canary_IP/Markdown/Specs/B068_PartitionArchitecture_v1.0.md`

---

## LANE B — Condor: Blueprint v2.0 Tokenization

**Session prompt:** `Condor_B068B_BlueprintRefactor_SessionPrompt.md`
**Read first:** `GrowDirect_UnifiedArchitectureThesis_v1.0.md` — specifically Section 3.3

**The framing Condor must hold:**
The vocabulary pack is the presentation expression of merchant-first isolation. The token
key naming convention must be consistent with the CRDM canonical field names. A
token key is not a display label — it is a bounded identifier whose resolution is
per-merchant, per-locale, with a guaranteed fallback chain.

**Deliverables:**

1. `Canary_Generic_Frontend_Blueprint_v2.0.md` — every display string replaced with
   `{{token.key}}` in `{{module.screen.element.variant}}` format. No hex codes. No font
   names. Structure only.

2. `B068_TokenRegistry_v1.0.md` — flat registry of every token key:
   - Key name
   - Category (chirp / companion / nav / scorecard / fox / goose / owl / shared)
   - Vocabulary-overridable: yes/no (flag terms merchants can rename)
   - Description
   - Example en-US resolution

**Vocabulary-overridable tokens** (the merchant-facing business terms):
`employee.label.*`, `location.label.*`, `cash_drawer.label.*`, `transaction.label.*`,
`chirp.label.*` (note: merchants see "Alert" not "Chirp" by default), `case.label.*`,
`void.label.*`, `refund.label.*`

**Output:**
```
_ALX/WorkOrders/output/Triangulation/Canary_Generic_Frontend_Blueprint_v2.0.md
_ALX/WorkOrders/output/Condor/B068_TokenRegistry_v1.0.md
```

---

## LANE C — Condor: Locale and Vocabulary JSON Files

**Depends on:** Lane B token registry
**Session prompt:** `Condor_B068C_LocaleVocabulary_SessionPrompt.md`

**Deliverables:**

1. `en-US.json` — every token key from the registry resolved to English default

2. `default_vocabulary.json` — Canary standard merchant-facing terms. Note: `chirp` → 
   `Alert` in default vocabulary (merchants don't see internal codename "Chirp")

3. `vocabulary_template.json` — blank with all vocabulary-overridable keys. Merchant
   fills this in via Settings → Language & Labels.

**Vertical reference examples** (document but do not ship as defaults):
- Restaurant: transaction → "Check", employee → "Server", cash_drawer → "Register"
- Coffee: employee → "Barista", location → "Café"
- Cannabis: employee → "Budtender", transaction → "Receipt", void → "Cancellation"
- Franchise: employee → "Associate", location → "Store"

**Output:**
```
_ALX/WorkOrders/output/Triangulation/LocalePacks/en-US.json
_ALX/WorkOrders/output/Triangulation/VocabularyPacks/default_vocabulary.json
_ALX/WorkOrders/output/Triangulation/VocabularyPacks/vocabulary_template.json
```

---

## LANE D — Tom: Merchant Vocabulary DB Schema

**Session prompt:** `Tom_B068D_VocabularySchema_SessionPrompt.md`
**Read first:** `GrowDirect_UnifiedArchitectureThesis_v1.0.md` — Sections 3.2 and 3.3 together

**The framing Tom must hold:**
The `merchant_vocabulary` table is the database expression of the same isolation principle
as the partition. One row per merchant per token per locale. No global vocabulary state.
The schema must make the resolution function trivial: lookup by `(merchant_id, token_key,
locale)`, fallback to locale pack JSON loaded at startup, fallback to en-US.

**Deliverables:**

1. `merchant_vocabulary` table DDL with indexes
2. `merchants.locale` and `merchants.vocabulary_enabled` field additions
3. Resolution function design — PostgreSQL function or application-layer service pattern
   implementing: Vocabulary → Locale → en-US fallback chain
4. Settings UI data model — what the Sprint 7+ vocabulary editor reads and writes

**Output:** `Canary_IP/Markdown/Specs/B068_VocabularySchema_v1.0.md`

---

## B-067 Connection

Condor's B-067-A capability map must use token keys for LP Signals, phase labels, and
section headers. Before Condor writes the capability map, they read the token registry from
Lane B. The capability map HTML (Qwen B-067-C) renders resolved strings from the API —
never hardcoded English.

B-067 runs in parallel. B-068-B token registry gates B-067-A for any user-facing strings.

---

## Deliverables Summary

| File | Owner | Lane | Status |
|---|---|---|---|
| `GrowDirect_UnifiedArchitectureThesis_v1.0.md` | ALX/PhD | E | ✅ COMPLETE |
| `B068_PartitionArchitecture_v1.0.md` | Tom | A | Pending |
| `B068_VocabularySchema_v1.0.md` | Tom | D | Pending |
| `Canary_Generic_Frontend_Blueprint_v2.0.md` | Condor | B | Pending |
| `B068_TokenRegistry_v1.0.md` | Condor | B | Pending |
| `en-US.json` | Condor | C | Pending (gates on B) |
| `default_vocabulary.json` | Condor | C | Pending (gates on B) |
| `vocabulary_template.json` | Condor | C | Pending (gates on B) |

---

*ALX | February 28, 2026 | B-068*
*Foundation. If this is right, we can make any app.*
