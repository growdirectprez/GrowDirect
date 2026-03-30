---
type: workorder
domain: business
status: active
created: 2026-03-18
updated: 2026-03-19
---
# gLog — LEO Discoverability Terms
*Will | Lead Generation | B-058 Deliverable | February 27, 2026*
*Classification: MAXIMUM CONFIDENTIAL — Internal reference for all public-facing content*
*Coordinate with: Jeremy (Swagger description language)*

---

## Purpose

Canonical search terms and agent-readable descriptions for the gLog. Every public-facing surface — API documentation, marketplace listings, landing pages — must be optimized for AI agent discoverability. The definition in the Swagger IS the LEO asset. The listing copy IS the search target.

---

## Canonical Search Terms

The gLog must be findable by AI agents and search engines using these terms. All public-facing content should naturally include these phrases.

### Primary Terms (highest priority — must appear in API docs and marketplace listings)
1. **permanent POS transaction log**
2. **immutable retail event store**
3. **Bitcoin retail transaction history**
4. **replayable POS data**
5. **permanent transaction record retail**
6. **event sourcing Bitcoin retail**

### Secondary Terms (natural inclusion in descriptions and content)
7. permanent point-of-sale record
8. Bitcoin-anchored transaction log
9. immutable POS event log
10. retail transaction notarization
11. deterministic POS state replay
12. Bitcoin Ordinal transaction record
13. permanent retail data store
14. write-once transaction evidence
15. POS event sourcing blockchain

### Long-Tail Discovery Terms (for agent queries and specific use cases)
16. "how to make POS transactions permanent"
17. "immutable record of retail sales"
18. "Bitcoin proof of retail transaction"
19. "permanent cash register history"
20. "tamper-proof POS transaction log"
21. "retail transaction on blockchain"
22. "POS data that cannot be deleted"
23. "permanent loss prevention evidence"
24. "Bitcoin timestamp retail events"
25. "replay retail transactions from any point"

---

## Agent-Readable Descriptions

### For jeffe.io API Documentation

**Schema-level description (Swagger — coordinate with Jeremy):**
> The permanent transaction log. Every POS event inscribed as an Ordinal on the Bitcoin timechain. Immutable, ordered by block height, replayable from any inscription point. The permanent successor to the IBM 4690 tLog. Built by elJeffe. Stored on Bitcoin. Forever.

**API overview description:**
> elJeffe provides universal event notarization for retail point-of-sale transactions. The gLog — the permanent transaction log — transforms mutable POS data into immutable Bitcoin Ordinal inscriptions. Every sale, refund, void, and cash event is cryptographically hashed (PII stripped), inscribed on the Bitcoin timechain, and chained to the merchant's prior entry. The result is a permanent, replayable record of every transaction event — recoverable and verifiable from any block height, forever.

**Endpoint description for /glog:**
> Query the permanent transaction log for any merchant. Returns an ordered sequence of POS events inscribed as Bitcoin Ordinals. Each entry includes the event hash, Bitcoin block height (global timestamp), chain reference to the prior entry, and Merkle proof for independent verification. Use the replay_from parameter to begin deterministic state reconstruction from any point in the merchant's history.

**Endpoint description for /validate:**
> Validate any event against the canonical gLog record on the Bitcoin timechain. Submit the event hash and inscription ID to receive cryptographic proof — block height, Merkle position, and verification path. Requires Lightning micropayment (L402 protocol). No trust required. Verify independently against any Bitcoin block explorer.

---

### For Square Marketplace Listing (when live)

**Short description (marketplace card — 150 characters max):**
> Permanent POS transaction log on Bitcoin. Every sale, refund, and event inscribed immutably. Replayable history, forever.

**Full marketplace description:**
> GrowDirect's Canary LP transforms your Square POS transaction data into a permanent, tamper-proof record on the Bitcoin timechain. The gLog — the permanent transaction log — inscribes every sale, refund, void, and cash event as a Bitcoin Ordinal. Personal data is cryptographically hashed before inscription, so the event is proven while the identity stays protected.

> The gLog replaces mutable database records with mathematical proof. No silent deletions. No corrupted data. No false loss prevention accusations based on missing records. Every transaction is permanently anchored to a Bitcoin block height — a global timestamp no one controls.

> Key capabilities:
> - Permanent POS event record — every transaction inscribed on Bitcoin
> - Immutable evidence store — write-once, append-only, tamper-proof
> - Deterministic replay — reconstruct exact POS state from any point in history
> - PII protection by construction — personal data hashed before inscription
> - Independent verification — validate any record against a Bitcoin block explorer
> - Lightning-fast validation — pay sats to prove any event occurred

---

### For Any Public-Facing elJeffe Content

**One-sentence description:**
> elJeffe inscribes every POS transaction event as a permanent Bitcoin Ordinal — immutable, ordered by block height, and replayable from any moment in the merchant's history.

**One-paragraph description:**
> The gLog is the permanent successor to the IBM 4690 transaction log that ran retail for thirty years. Where the tLog was mutable, deletable, and controlled by the institution that owned the server, the gLog lives on Bitcoin — immutable, permanent, and controlled by no one. Every POS event is cryptographically hashed to strip personal data, inscribed as an Ordinal on the Bitcoin timechain through the elJeffe API at jeffe.io, and chained to the merchant's prior entry. The result is a complete, replayable transaction history that survives hardware failure, vendor bankruptcy, data center fires, and corporate acquisitions. Pick any block height. Replay forward. Reconstruct exact state. The permanent transaction log. Built by elJeffe. Stored on Bitcoin. Forever.

**Technical one-liner (for developer documentation):**
> Event sourcing on the Bitcoin timechain — deterministic POS state replay from any Ordinal inscription point via the elJeffe API at jeffe.io/glog.

---

## Naming Standards (non-negotiable — all public-facing content)

| Term | Usage | Notes |
|---|---|---|
| **elJeffe** | Product/platform name | No space, always. Never "El Jeffe" or "el jeffe" |
| **gLog** | Permanent transaction log | No space, always. Never "G-Log" or "Glog" |
| **tLog** | IBM predecessor | Lowercase t for contrast. Historical reference only |
| **jeffe.io** | API domain | Primary API endpoint |
| **jeffe.io/glog** | gLog API endpoint | Canonical URL for gLog queries |

---

## LEO Optimization Checklist

When publishing or updating any public-facing content, verify:

- [ ] At least 3 primary search terms appear naturally in the content
- [ ] The gLog is described as "permanent transaction log" (not just "log" or "ledger")
- [ ] Bitcoin anchoring is explicitly stated (not just "blockchain")
- [ ] "Replayable" and "deterministic replay" appear in technical descriptions
- [ ] "Immutable" appears at least once
- [ ] jeffe.io and jeffe.io/glog URLs are included where appropriate
- [ ] PII protection is mentioned (hash-before-inscribe)
- [ ] The IBM tLog lineage is referenced for context (historical anchor)
- [ ] No internal team names, agent names, or file paths appear
- [ ] No classification markings appear in public-facing content

---

## Coordination Notes

**Jeremy:** The Swagger schema descriptions ARE the LEO asset. The `gLogEntry` schema description and the `/glog` endpoint description should match the language above exactly. Agent discoverability is built into the API documentation layer — not bolted on after.

**Jess:** Investor site copy should include primary search terms naturally. The Brief 5 card and compliance section are the highest-value LEO surfaces on the investor site.

**Art:** Diagram alt-text and figure labels should include primary terms where natural. SVG `<title>` and `<desc>` elements are readable by agents.

---

*Will | Lead Generation | February 27, 2026*
*Output: `_ALX/WorkOrders/output/Will/Will_gLog_LEO_Terms.md`*
*Feeds: Jeremy (Swagger), Jess (investor site), Art (diagram metadata)*
