---
type: legal
domain: business
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Pre-Demo IP Checklist: El Jeffe

**DISCLAIMER: INTERNAL FOUNDER PREPARATION — NOT LEGAL ADVICE**

This checklist is an internal guide to help the founder prepare for the merchant demo on Monday, March 3. It does NOT constitute legal advice. Before the demo, the founder MUST review this checklist with a qualified patent attorney and legal counsel. This is a preparation aide only and should not be relied upon without professional legal guidance.

---

## EXECUTIVE SUMMARY

The merchant demo on Monday, March 3 begins a public disclosure clock under the America Invents Act (AIA). Once disclosed, a 12-month deadline starts counting down to file a provisional patent application. The current memo recommends filing a provisional BEFORE the demo to establish priority date before the clock starts. This checklist ensures that the demo can proceed safely while protecting IP.

**Critical timing:** Provisional must be filed before Monday 11:59 PM PT or the AIA clock starts running.

---

## PRE-DEMO CHECKLIST

- [ ] **Provisional patent filed with USPTO** (or explicit decision made not to file, with founder approval and documented rationale)
  - *If not yet filed:* Patent attorney must file by Sunday, March 2, 11:59 PM PT
  - *Confirmation:* Founder receives USPTO acknowledgment with filing number and date stamp

- [ ] **Merchant has signed NDA before any technical discussion**
  - *Template includes:* Confidentiality clause, IP acknowledgment, restricted use clause, term (typically 3-5 years)
  - *Specific clause:* "Merchant acknowledges pending patent application. Merchant agrees not to disclose technical architecture details to third parties without written permission."
  - *Confirmation:* Signed PDF in founder's file before demo kickoff

- [ ] **Founder briefed on what CAN be shown during demo**
  - ✓ End-to-end workflow: webhook in → database record + Bitcoin inscription out
  - ✓ Demo merchant transaction with actual Bitcoin inscription ID + block explorer link
  - ✓ Query API (showing structured application store results)
  - ✓ Bilateral verification: merchant's send log vs. El Jeffe's received payload (byte-for-byte match)
  - ✓ Merchant's own keys in action: inspecting their inscription on Bitcoin blockchain
  - ✓ Use cases: retail, healthcare, supply chain, legal, insurance, government

- [ ] **Founder briefed on what CANNOT be shown during demo**
  - ✗ Subscription isolation architecture (evidence store → application store → inscription service separation)
  - ✗ Message queue structure or tuning parameters
  - ✗ Key custody procedures or key backup/rotation logic
  - ✗ Database schema or table structures
  - ✗ Internal worker deployment (Kubernetes, scaling, concurrency)
  - ✗ Merkle tree construction or batching intervals
  - ✗ Satoshi denomination for L402 validation calls
  - ✗ Cost analysis or margin estimates
  - ✗ Competitive intelligence (polling architecture argument)

- [ ] **Founder briefed on what CAN be said about the architecture**
  - ✓ "We receive your webhook, compute a cryptographic hash of the raw payload, store it permanently, and inscribe proof on Bitcoin."
  - ✓ "Your merchant record is available in two forms: queryable (instant, our database) and verifiable (permanent, on Bitcoin)."
  - ✓ "Bilateral verification: you retain your send log, we retain the received payload and hash. We can prove byte-for-byte matching without you trusting us."
  - ✓ "Bitcoin Ordinal inscription gives you a permanent, independently auditable record that exists outside our infrastructure."
  - ✓ "The inscription ID is public. You can verify it yourself on any Bitcoin block explorer, now and 50 years from now."

- [ ] **Founder briefed on what CANNOT be said about the architecture**
  - ✗ "We use triple subscriber pattern..." (reveals internal architecture)
  - ✗ "Evidence store is write-once..." (reveals design decision, potential licensing concern)
  - ✗ "We batch events into Merkle trees..." (reveals cost optimization, potential competitor insight)
  - ✗ "Ordinal inscription pool is owned by GrowDirect..." (reveals custody model, potential regulatory concern)
  - ✗ Any discussion of key custody, rotation, or backup procedures
  - ✗ Any discussion of database technology, server infrastructure, or deployment
  - ✗ Any discussion of operational cost per inscription or pricing strategy
  - ✗ Any claim of "we're the first to..." or competitive superiority

- [ ] **Founder prepared for the question: "How does this work technically?"**
  - *Approved response:* "We receive your event, hash it to preserve evidence, store the hash permanently on Bitcoin via Ordinal inscription, and make the record queryable through our API. The Bitcoin record is independently verifiable without any intermediary. Happy to walk you through the flow on this transaction we just processed."
  - *Follow-up to redirect:* "The detailed architecture is in our pending patent application. Our technical team can walk you through the workflow without diving into implementation details."
  - *Boundary:* Do not describe internal subscriber isolation, Merkle batching, or key custody.

- [ ] **Founder prepared for the question: "Can I see the code?"**
  - *Approved response:* "Our code is proprietary pending patent filing. We're happy to walk you through the product workflow and answer questions about how it meets your business needs."
  - *Alternative if code sharing is acceptable:* "We can review a code walkthrough under NDA as part of our evaluation process. Let's discuss that separately."
  - *Firm boundary:* Code repository access or source code review should NOT happen on Monday demo call.

- [ ] **Founder reminded: The 12-month AIA clock starts at demo**
  - *Implication:* If provisional NOT filed before Monday, one-year deadline to file begins counting down Monday 11:59 PM PT.
  - *Risk:* Provisional filing cost ($1,500-$5,000) is trivial compared to losing patent priority. If not filed before Monday, file within 12 months or lose patent rights.
  - *Recommendation:* File before Monday to start fresh.

---

## POST-DEMO IP ACTIONS

- [ ] **Document what was disclosed at the demo**
  - *Include:* Date, attendees, what technical details were shown, any questions asked about the architecture
  - *File:* In founder's IP folder for later reference if patent office asks for timeline of public disclosure

- [ ] **If merchant requests code access or technical deep-dive**
  - *Action:* Schedule separate call with merchant's technical team under expanded NDA
  - *Boundary:* Code walkthrough should not reveal key custody, Merkle batching, or internal subscriber architecture (these are Crown Jewels)
  - *Approval required:* Patent attorney approval before sharing any code or technical documentation

- [ ] **If merchant asks "when can we go live?"**
  - *Check:* Has provisional been filed? Is the patent attorney prepared to discuss continuation-to-utility timeline?
  - *Approved response:* "We're targeting [launch date]. We're ensuring our IP is properly protected before scaling. Our legal team will provide a timeline."
  - *Reality:* Provisional is filed. Utility application can be prepared over the next 12 months. No product timeline should be delayed by patent strategy.

- [ ] **Follow-up with patent attorney**
  - *Task:* Provide attorney with any new competitive intelligence or merchant feedback from demo
  - *Task:* Confirm timeline for continuation-to-utility application (typically filed before 12-month provisional anniversary)
  - *Task:* Begin prior art search if not already complete

---

## STANDING RULES FOR DEMO

1. **NDA must be signed BEFORE technical discussion.** No exceptions. No "we'll send it over after." The merchant signs, the founder confirms receipt, and only then does the technical demo begin.

2. **No company names.** Do not name the polling architecture company, competing platforms, or any other company. Avoid specific competitive references.

3. **No internal team names.** Do not mention team member roles or names (developers, engineers, architects).

4. **Bilateral verification is the crown jewel.** This is the single most defensible and novel aspect of the architecture. Emphasize it in the demo: the merchant's send log vs. our received payload, byte-for-byte match, no intermediary required.

5. **Bitcoin inscription ID is the proof.** Every transaction shown should include the actual inscription ID and a link to the block explorer. This is the most concrete, impressive part of the demo. Let the merchant look it up themselves.

6. **If asked "is this patented?"** approved response: "We have a patent application pending for this technology. Our legal team can discuss the details."

7. **If merchant wants to see the patent application.** Response: "The patent application is confidential during prosecution. Once issued, it will be public. We're happy to discuss the general innovation areas our team is protecting."

8. **Do not discuss money transmitter or regulatory risk.** If merchant asks about compliance or regulation, response: "Our legal team is reviewing regulatory requirements. We'll have a full compliance briefing before we move forward."

9. **Do not discuss pricing.** If merchant asks about cost per notarization or per validation call, response: "We're still optimizing our pricing model. We'll share a detailed pricing proposal as we move toward integration."

10. **Document everything.** Founder should record (with permission) or take detailed notes on:
    - What the merchant asked about
    - What was disclosed (beyond the demo walkthrough)
    - Any indication of competitive interest
    - Any indication of merchant's technical sophistication (may affect future disclosures)

---

## RED FLAGS DURING DEMO

**If merchant says any of these, pause and escalate to counsel:**

- "Can I license this technology?" — Licensing agreement would need IP counsel review
- "Can we co-develop this?" — Co-ownership agreement would need IP counsel review
- "Can you integrate with our system?" — Integration may expose Crown Jewels; needs NDA scope review
- "How do you scale this to billions of events?" — Do not discuss Merkle batching, pool scaling, or Kubernetes elasticity
- "What if you get hacked?" — Do not discuss key custody or backup procedures
- "How do you prevent fraud in the timestamp?" — Do not discuss bilateral verification beyond what's in the demo

---

## AFTER MONDAY: CRITICAL PATH

1. **File utility patent application within 12 months of provisional filing date.** Patent attorney will advise on timeline; typically within 6-9 months.

2. **Maintain strict confidentiality of Crown Jewels:** Merkle batching, key custody procedures, internal subscriber isolation, queue tuning, Chirp parameters.

3. **Expand NDA if merchant requests code access.** Do not share code without attorney review.

4. **Monitor for competitive references.** If merchant discloses (in violation of NDA), document and report to counsel.

5. **File trademark application for "El Jeffe"** if not already filed. Class 42 (SaaS), Class 35 (Business Services).

6. **Clarify legal structure** (GrowDirect product vs. separate entity) with tax and business attorney. Impacts future licensing and equity treatment.

---

## REMINDERS FOR THE FOUNDER

**The demo is an opportunity, not a risk**, provided:
- Provisional is filed before Monday (priority date is locked in)
- Merchant signs NDA before technical discussion
- Founder sticks to the talking points (what CAN be shown/said)
- Founder captures evidence of disclosure for the patent record

**The merchant wants to see that the thing works.** Show them:
1. A real webhook triggering a notarization
2. The database record (queryable, instant)
3. The Bitcoin inscription (permanent, verifiable)
4. The bilateral verification (their send log vs. our received payload)
5. The block explorer link (independent verification, no intermediary)

**That is enough.** You do not need to explain Merkle trees, key custody, or Kubernetes. Those are the Crown Jewels. They stay secret. The innovation is in the six-node architecture, and the demo proves that the six-node architecture delivers the outcome. The merchant will be impressed.

**If the merchant asks "how do you build a cryptographically verifiable permanent record?" the answer is:**
"That's exactly what we're protecting with a pending patent. What I can tell you is: we capture your webhook, we hash it, we store it permanently on Bitcoin, and you can verify it yourself. That's what you're seeing in this demo."

---

**Prepared by:** Syd, Legal Research — GrowDirect  
**Date:** February 26, 2026  
**For:** Founder preparation before merchant demo  
**Confidentiality:** Internal guide — do not share with merchant or external parties  
**Review with:** Patent attorney and legal counsel before Monday demo

---

## QUICK REFERENCE: What to Say

| Question | Approved Response |
|---|---|
| "How does this work?" | "We receive your event, hash it, inscribe on Bitcoin. Two artifacts: queryable database + permanent Bitcoin record. You can verify independently." |
| "Can I see the technical architecture?" | "Patent application pending. I can walk you through the workflow without implementation details." |
| "Can I see the code?" | "Proprietary. Happy to do a code walkthrough under NDA as a separate conversation." |
| "Is this patented?" | "Patent application pending. Legal team is handling details." |
| "How do you prove authenticity?" | "Bilateral verification: your send log vs. our received payload, byte-for-byte match. Plus: Bitcoin inscription, independently verifiable." |
| "Can you guarantee this works forever?" | "Bitcoin Ordinals are permanent and independently verifiable. No company infrastructure required. You can verify in 50 years." |

---

**FINAL REMINDER:** This is a checklist for preparation. Before the demo, review this with your patent attorney and legal counsel. This is not a substitute for legal advice.
