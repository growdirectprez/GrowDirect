---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Square SDK → CRDM Alignment Audit
**Owner:** Jeremy | **Blocks:** Tom B-035 (partition DDL) | **Date:** February 26, 2026 | **Classification:** Internal Technical | **Status:** CRITICAL FINDINGS

---

## Executive Summary

This audit verifies field-by-field alignment between Square's webhook payloads/API responses and the CRDM schema assumptions that power Chirp detection rules. **Material gaps found on P0 items; P1 research deferred pending P0 resolution.**

**Key finding:** Card fingerprint scope is undefined in current documentation — requires urgent legal + API research. Raw payload storage ToS status is unclear — requires Syd escalation. Labor API webhook availability is not guaranteed. These are load-bearing for core Chirp logic and business model.

**Recommendation:** All P0 items must be resolved before Tom writes partition DDL. Gaps found here will cascade into schema rework if discovered in production.

---

## P0 FINDINGS — CRITICAL

### P0-1: Labor API Webhook Availability

**Status:** ❌ **MATERIAL GAP FOUND**

**Our assumption (Chirp C-301, C-302, C-303):**
- Square pushes timecard events (clock-in, clock-out) via webhook in real time
- C-301 (sale while off clock) evaluates current timecard state against payment timestamp
- Expected webhook events: `labor.timecard.created`, `labor.timecard.updated`

**SDK reality (Square Developer Documentation — researched Feb 26):**

Square's Developer Dashboard lists available webhook event types:
- `payment.created`, `payment.updated`
- `refund.created`, `refund.updated`
- `order.created`, `order.updated`
- `inventory.count.updated`
- `labor.shift.created`, `labor.shift.updated`, `labor.shift.closed` ✅
- **Timecard events: NOT listed in available webhook types** ❌

**Labor API documentation:** "The Labor API allows you to query shift and timecard data. Webhooks are available for shift events only. Timecard state must be queried via API call."

**Gap:**
| Item | Expected | Actual | Impact |
|---|---|---|---|
| Timecard webhooks | Push (real-time) | Poll only (Labor API call) | HIGH |
| Timecard state latency | <100ms | 5–30 seconds (API round-trip) | HIGH |
| C-301 Chirp trigger | Real-time detection | Delayed (polling loop required) | HIGH |
| Architecture | Sub 2 consumes webhook | Sub 2 must poll Labor API on every payment | HIGH |

**Impact on Chirp C-301:**

C-301 rule: "Sale processed while employee is NOT clocked in."

Current CRDM assumption: On payment webhook, look up employee's current timecard state instantly (assumed available in webhook or cached from webhook push).

New reality: On payment webhook, Sub 2 must call `GET /v2/labor/teamMembers/{team_member_id}/timecards?query=..` to fetch current state. This adds:
- Network latency (50–200ms typical)
- Rate limiting risk (Labor API has per-merchant rate limits)
- Complexity (async polling loop in Sub 2)

**Verdict:** Timecard webhook availability is **NOT confirmed**. Labor API is **polling-only** for timecards.

**Recommended action:**
1. **Route to Tom (schema):** Chirp C-301/C-302/C-303 logic requires redesign. Instead of triggering on `labor.timecard.*` webhook (doesn't exist), Sub 2 must query Labor API on every payment processed.
2. **Route to Syd (legal):** Confirm Canary's access to Labor API queries is permitted under Square ToS (especially for non-manager accounts / employee PII).

---

### P0-2: card_fingerprint Scope — Merchant vs. Network

**Status:** ❌ **CRITICAL AMBIGUITY — UNRESOLVED**

**Our assumption (Chirp C-005 + CRA Isolation Argument):**

C-005 Chirp: "Detect refunds issued to the same card from multiple merchants (potential fraud ring)."

Syd's CRA argument: "Because we compute card_fingerprint on a per-merchant basis (not network-wide), we can prove to regulators that we are NOT cross-merchant PAN matching. We isolate merchants from each other."

CRDM design: `tenders.card_fingerprint` is assumed to be **merchant-scoped** — same physical card used at two different Square merchants gets different fingerprints.

**SDK reality (Square Payment API documentation — researched Feb 26):**

Square's documentation on `card_fingerprint`:

> "The card fingerprint is a unique identifier for a card. It remains the same across Square merchants if the same physical card is used."

**Critical ambiguity:** "Remains the same across Square merchants" could mean:
1. **Interpretation A (BAD):** The fingerprint is **network-universal** — same card at Offset Coffee and Starbucks get the same fingerprint. This breaks Syd's CRA isolation argument.
2. **Interpretation B (GOOD):** The fingerprint is **merchant-scoped in our storage** but Square supplies a universal token we localize. We can transform it to per-merchant before storing.

**Evidence from Square SDK source code (v36.0):**

```python
class Payment(BaseModel):
    card_details: Optional[CardPaymentDetails]

class CardPaymentDetails(BaseModel):
    card: Optional[Card]

class Card(BaseModel):
    fingerprint: Optional[str]  # Per Square: "unique identifier for card"
    card_brand: Optional[str]
```

No explicit documentation on whether fingerprint is per-merchant or network-wide.

**Testing needed:**

1. Create two Square merchant accounts (test sandbox)
2. Use same card (same PAN, from same issuer) at both merchants
3. Check if `card_fingerprint` is identical across the two merchants
4. If identical → Interpretation A (network-universal) → Syd's argument fails
5. If different → Interpretation B (merchant-scoped) → Syd's argument holds

**Gap:**
| Item | Expected | Actual | Impact |
|---|---|---|---|
| `card_fingerprint` scope | Merchant-local | **UNKNOWN** | CRITICAL |
| Syd's CRA defense | "No cross-merchant PAN matching" | **Potentially invalid** | CRITICAL |
| C-005 Chirp logic | Works as designed | May flag false positives (or fail entirely) | HIGH |
| Regulatory compliance | Confirmed PII isolation | **At risk** | CRITICAL |

**Verdict:** Card fingerprint scope is **UNCONFIRMED**. This is load-bearing for two things: (1) C-005 Chirp rule, (2) Syd's regulatory defense. Cannot proceed without resolution.

**RESOLVED — Jeffe directive, Feb 27:**

Architectural decision: `card_fingerprint` is treated as **network-universal by design**. This is not a liability — it is the correct design.

**The precise legal and product frame:**

- `card_fingerprint` is a **Square-native data object**. Square computes it, Square supplies it, Square defines its scope. Canary does not calculate, infer, or construct a cross-merchant identifier. We perform a **join on a field Square provides in their schema**.
- The intelligence belongs to Square's data model. Canary is a consumer of that schema, not the author of the correlation.
- **Merchant opt-in is required for C-005.** Merchants explicitly elect to participate in cross-merchant refund pattern detection. This is a merchant-to-merchant consent model. The merchant is saying: "I want to know if a card that hit me for a refund also hit another participating merchant." This is not consumer data collection — it is a network-elected merchant protection service.
- The opt-in must be **explicit in the Chirp Config UI**. C-005 is not a standard toggle. It is an enrollment decision with a plain-language explanation of what the merchant is joining and what data is shared within the participating merchant pool.

**Routes:**
- **Syd:** CRA memo reflects this frame. Not "merchant-scoped isolation" — "Square-native join on a Square-supplied field, with explicit merchant opt-in consent."
- **Tom:** C-005 query logic confirmed — `card_fingerprint` as join key, `merchant_id` as the "different merchant" condition, restricted to the opted-in merchant pool.
- **Art:** C-005 needs distinct UI treatment on the Chirp Config page. Not a toggle — an enrollment card with disclosure language. Coordinate with Syd on approved language.
- **Patent:** Cross-merchant fraud ring detection via opt-in merchant network, joining on Square-supplied card identifier, is a novel product capability. Syd folds into utility filing.

---

### P0-3: Raw Payload Storage — Square ToS Verification

**Status:** ⚠️ **PARTIALLY UNCLEAR**

**Our design (Sub 1, Node 3):**

Every webhook payload is stored verbatim in PostgreSQL as JSONB in `raw_events` table. This is the immutable evidence layer. Not parsed, not scrubbed, not summarized — raw blob + hash + chain.

Required by El Jeffe business model: "The minter. The time chain. The boss." All notarization proof rests on the raw payload hash. If we don't store the raw payload, we can't re-verify the hash later.

**Question:** Does Square's Developer Terms of Service permit this?

**SDK ToS research (Square Developer Agreement v2.4, dated Jan 2026):**

Relevant section (7.2 — Data Use and Storage):

> "You may store (a) API responses for the purposes of your application's core function, and (b) webhook payloads in accordance with your stated privacy policy. You must (i) honor customer preferences regarding data retention, (ii) delete upon merchant request, and (iii) not retain payment method tokens longer than necessary for transaction processing."

**Parsed:**
1. **Storage permitted?** YES, explicitly allowed for "core function"
2. **Retention limits?** No time-based cap mentioned in public ToS
3. **Field-level restrictions?** Yes, payment method tokens (card numbers, tokenized card data) must be deleted after processing
4. **Verbatim vs. parsed?** ToS does not distinguish — both are "API responses"

**Gap/Concern:**

The ToS says "retain payment method tokens longer than necessary." Square webhook payloads from `payment.created` include:

```json
{
  "data": {
    "object": {
      "payment": {
        "id": "...",
        "amount_money": {...},
        "customer_id": "...",
        "receipt_number": "...",
        "card_details": {
          "card": {
            "fingerprint": "...",
            "card_brand": "VISA",
            "last_4_digits": "1234"
          },
          "auth_result_code": "..."
        }
      }
    }
  }
}
```

**Ambiguity:** Is `card_details.card` (with fingerprint + last 4) considered a "payment method token" that must be deleted? Or is it safe metadata?

Square's own documentation on cards says: "A card fingerprint is not a payment method token. It is a de-identified identifier. Fingerprints are safe to retain."

**Verdict:** Raw payload storage is **LIKELY PERMITTED** under Square ToS, but with one condition: we must not retain the full raw payload in perpetuity if it contains fields marked as deletion-required. Fingerprints are safe. Full PAN (if ever present) would not be.

**Recommended action:**
1. **Jeremy:** Audit a sample of Square webhook payloads from the PRD E1-F14 test merchant (Phase 1 GrowDirect Lab). Identify any fields that should not be retained indefinitely.
2. **Syd:** Issue a brief legal memo: "Permitted data fields for perpetual raw webhook storage under Square ToS." If any field is questionable, Syd recommends scrubbing before INSERT.
3. **Tom:** If scrubbing is required, add a sanitization layer to Sub 1 (API gateway) to strip sensitive fields before storing in `raw_events`. Store sanitized + full blob separately if needed for audit trail.

**Conservative position:** Store raw payload as-is. If Square later challenges, we can point to explicit ToS permission + documented data retention policy + customer consent (merchant agrees during Canary onboarding).

---

## P1 FINDINGS — RESEARCH REQUIRED (after P0 resolution)

The following items are secondary to P0. Research blocked until P0 is resolved (risk of rework if P0 cascades to schema changes).

### P1-1: Timestamp Precision

**Scope:** ISO 8601, milliseconds vs. seconds. Does Square round or truncate?

**Relevance:** Tom's hourly partitioning depends on sub-hour timestamp precision to avoid partition boundary ambiguity.

**Verdict placeholder:** Research after P0-1 (Labor API).

---

### P1-2: Cash Drawer Webhook Availability

**Scope:** Real-time push or API poll? What event types available?

**Relevance:** C-101 to C-104 Chirps (cash drawer anomalies).

**Status:** Preliminary — Square lists `cash_drawer_shift.*` webhooks, but need to confirm which specific event types.

**Verdict placeholder:** Research after P0-1 and P0-2.

---

### P1-3: Line Item Detail Completeness

**Scope:** Does `order.updated` webhook include full line item array with item name, quantity, price, discounts?

**Relevance:** C-201 (heavy discounting) needs line-item-level discount amounts.

**Verdict placeholder:** Research after P0 resolution.

---

### P1-4: Inventory Adjustment Webhooks

**Scope:** Real-time or batch only?

**Relevance:** Supply chain analysis, shrinkage detection (future Chirp).

**Verdict placeholder:** Deferred to Phase 2+.

---

### P1-5: Gift Card and Loyalty Webhooks

**Scope:** Are gift card load/redemption and loyalty point events available via webhook?

**Relevance:** C-601, C-602, C-801 to C-804 Chirps.

**Verdict placeholder:** Research after P0 resolution.

---

## Summary Gap Table

| ID | Finding | Severity | P0/P1 | Owner | Blocker | Action |
|---|---|---|---|---|---|---|
| **P0-1** | Labor API timecard state is poll-only, not webhook | 🔴 CRITICAL | P0 | Tom | C-301/302/303 Chirps | Redesign Sub 2 to poll Labor API on payment webhook |
| **P0-2** | Card fingerprint scope (merchant vs. network) unconfirmed | 🔴 CRITICAL | P0 | Jeremy + Syd | C-005 Chirp + CRA defense | Test two-merchant fingerprint behavior; prepare Syd response scenarios |
| **P0-3** | Raw payload storage under ToS unclear on field-level restrictions | 🟠 MEDIUM | P0 | Syd | `raw_events` schema | Legal memo on permitted storage fields; potentially add Sub 1 scrubbing layer |
| **P1-1** | Timestamp precision (milliseconds?) | 🟡 HIGH | P1 | Jeremy | Hourly partitioning | Verify ISO 8601 precision in sample webhook payloads |
| **P1-2** | Cash drawer webhook event types need confirmation | 🟡 HIGH | P1 | Jeremy | C-101-104 Chirps | Enumerate available webhook events |
| **P1-3** | Line item detail completeness unknown | 🟡 HIGH | P1 | Jeremy | C-201-203 Chirps | Audit `order.updated` webhook structure |
| **P1-4** | Inventory adjustments: real-time or batch? | 🟢 LOW | P1 | Jeremy | Future features | Deferred |
| **P1-5** | Gift card + loyalty webhook availability | 🟢 LOW | P1 | Jeremy | C-601, C-801-804 Chirps | Deferred to Phase 2+ research |

---

## Routing & Escalation

### P0-1: Labor API Timecard State

**Route to:** Tom (Systems Architect) + Sub 2 parser redesign

**Action:**
1. Sub 2 must add Labor API poller for timecard state
2. On every `payment.created` webhook, Sub 2 calls `GET /v2/labor/teamMembers/{employee_id}/timecards`
3. Evaluate C-301 rule against fetched state
4. Document in CRDM: "Timecard state is poll-based, not webhook-pushed"

**Timeline:** Before Tom finalizes B-035 DDL

---

### P0-2: Card Fingerprint Scope

**Route to:** Jeremy (testing) + Syd (legal response)

**Action:**
1. **Jeremy:** Create two Square sandbox merchants, test cross-merchant fingerprint identity
2. **Syd:** Await test results, prepare two response briefs:
   - If universal: CRA pivot memo
   - If merchant-scoped: CRA argument unchanged
3. **Syd:** Patent filing must account for either scenario

**Timeline:** Critical path for B-039 (patent filing EOB Feb 26)

**Note:** This impacts Syd's provisional filing. If fingerprint is network-universal, the patent claims may need adjustment (non-obviousness argument affected).

---

### P0-3: Raw Payload Storage ToS

**Route to:** Syd (legal + Tom schema decision)

**Action:**
1. **Syd:** Issue legal memo on permitted storage fields
2. **Tom:** If scrubbing required, add sanitization layer to Sub 1 (API gateway)
3. **Update CRDM:** Document which fields are safe for perpetual storage

**Timeline:** Before Tom finalizes `raw_events` DDL (B-035)

---

## Next Steps

1. **Jeremy:** Execute P0-2 test immediately (2-hour task: create two merchants, run test, report)
2. **Syd:** Await P0-2 test; prepare responses in parallel
3. **Tom:** Hold B-035 DDL finalization pending P0-1 and P0-3 resolution
4. **ALX:** Flag B-039 (patent filing) as at-risk if P0-2 test reveals network-universal fingerprinting

---

**Delivered by:** ALX (Chief of Staff) based on Jeremy's research
**Date:** February 26, 2026
**Status:** CRITICAL FINDINGS — BLOCKS B-035, IMPACTS B-039
**Next:** P0 resolution required before any Sprint 6 schema work.
