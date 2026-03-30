---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Condor Wave 2 Session — PRD Addenda + B-048 C-005 Chirp Confirmation
**Work Orders:** B-066 follow-up (PRD addenda) + B-048 C-005 architectural confirmation
**Date:** February 28, 2026 (queued — fires after Condor Wave 1 delivers)
**Dispatched by:** ALX
**Priority:** 🟡 HIGH — keeps PRDs current for Jeremy's build. Closes B-048 for Tom.
**Session type:** Documentation + Architecture Review

---

## Context — What You Just Delivered in Wave 1

In your B-066 + B-067-A combined session, you produced:
1. `Condor_B066_Questions_v1.0.md` — questions for Jeffe/ALX resolution
2. `B067_SquareCapabilityMap_v1.0.md` — 16-family capability map
3. `Square_TSP_CodingStandards_v1.0.md` — Jeremy's coding bible

**Section 10 of the coding standards** lists PRD addenda required — TSP PRDs that need updating based on your SDK review findings. That list is your input for this session.

---

## Task 1: PRD Addenda (from B-066 Section 10)

### Read First
```
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Condor/Square_TSP_CodingStandards_v1.0.md  (Section 10)
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Condor/Condor_B066_Questions_v1.0.md
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Condor/PRD_TripleSubscriberPipeline/
```

### What to Do

For each PRD flagged in Section 10 of the coding standards:
1. Open the PRD at v1.2
2. Write a formal addendum section at the bottom (do NOT modify the v1.2 body — append only)
3. Format:
   ```
   ---
   ## Addendum v1.2.1 — Post-SDK Review (Feb 28, 2026)
   **Source:** B-066 Square SDK Review
   **Change:** [what changed and why]
   **Impact:** [what Jeremy needs to do differently]
   **Approved:** [ALX / pending Jeffe]
   ```
4. Bump the PRD version to v1.2.1 in the header

### Output
Updated PRDs in place at:
```
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Condor/PRD_TripleSubscriberPipeline/
```

### If No Addenda Were Flagged
Section 10 may contain zero flags — meaning the SDK review found no material gaps against the PRDs. In that case, write a one-page confirmation memo:
```
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Condor/B066_PRDConfirmation_v1.0.md
```
Confirming: "All TSP PRDs at v1.2 remain accurate post-SDK review. No addenda required."

---

## Task 2: B-048 — C-005 Chirp Logic Confirmation

### Context
Tom flagged this: `card_fingerprint` is **network-universal by design**. Merchant isolation comes from `merchant_id` + `location_id` context — not from the fingerprint itself.

C-005 Chirp: "Detect refunds issued to the same card from multiple merchants." This Chirp works as designed and is **stronger** than originally spec'd because the fingerprint IS the cross-merchant signal.

### What to Do

1. Read the C-005 Chirp definition in the TSP PRDs (likely TSP-02 or the Consolidated Review)
2. Read Tom's B-048 note in HANDOFF.md (lines ~488-493)
3. Confirm or flag: does the C-005 evaluation logic correctly use `card_fingerprint` as join key across merchant partitions?
4. Specifically: the query pattern should be `WHERE card_fingerprint = X AND merchant_id != current_merchant`

### Deliverable
```
/Users/geofflyle/GrowDirect/_ALX/WorkOrders/output/Condor/B048_C005_Confirmation_v1.0.md
```

Short (1 page max):
- C-005 logic: CONFIRMED CORRECT or ISSUE FOUND
- `card_fingerprint` cross-merchant query pattern: verified or needs revision
- Any impact on Tom's partition design (partition-crossing query considerations)
- Sign-off line: "B-048 C-005 Chirp: CONFIRMED" or "B-048 C-005 Chirp: REVISION NEEDED — [details]"

---

## Task 3 (if time): Resolve Jeffe Questions from B-066

If your B-066 Questions doc flagged items as "needs Jeffe resolution," those may have been answered by now (ALX routes them during the Wave 1→Wave 2 gap). Check HANDOFF.md or TRIAGE.md for any ALX notes on resolved questions. If resolved, fold the answers into the coding standards doc as an addendum.

---

## Standing Directives

- Append only on PRDs — never modify v1.2 body text
- B-064: Everything traces to the heartbeat. If a PRD addendum changes the heartbeat path, flag it RED.
- IP safety: no detection algorithms, no CRDM internals, no patent language in any output

---

## Session Close

Update HANDOFF.md:
- PRD addenda: which PRDs updated (or confirmation memo if none needed)
- B-048 C-005: confirmed or revision needed
- Any remaining unresolved B-066 questions

Log timelog per TRIAGE Step 0.

---

*ALX | February 28, 2026 | Wave 2 — Condor PRD Addenda + B-048*
*Keeps PRDs current. Closes out B-048 for Tom.*
