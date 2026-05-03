# A4 — DNS Configuration and Position Paper Publication Scope

**Dispatch:** A4 in `outputs/session-summary-and-company-formation-epic.md` (Category A — Foundation)
**Status:** Ready for execution
**Owner:** Founder + technical contributor (founder may execute solo for the minimal site)
**Target completion:** Phase A week 4-6 (parallel to A1 Wyoming formation; independent of A2/A3 Genesis inscription except for the block-height anchor mechanic)
**Block-height anchor:** First publication moment

---

## Mission

Configure DNS for the `eljeffe.io` domain portfolio and supporting domains; stand up a minimal site at the canonical namespace identifier with the position paper at `/position`; embed a block-height anchor in the page footer (mechanism: published-as-of-block-NNNNN line in footer + corresponding ordinal-inscription txid for the position paper's content hash). The first-mover claim is established publicly the moment the page is live.

## Deliverables

1. **DNS configuration for the canonical namespace identifier.** Per epic open decision #3 (`jefe.io` vs `eljeffe.io` as primary), configure A/AAAA/CNAME records for the chosen primary plus 301-redirect from the secondary. Configure the supporting domains in the portfolio (per the founder's secured list — `eljeffe.io / .org / .wtf / .xyz / jeffe.io / eljeffebtc.com / growdirect.app / growdirect.io / abalonecove.org / ownpalosverdes.com`) per the role each plays:
   - `[primary]` — main site; position paper at `/position`; eljeffe Hash and Seal Protocol page at `/protocol`
   - `[secondary]` — 301-redirect to primary; reserves the namespace
   - `eljeffebtc.com` — Bitcoin-specific landing for crypto-native audience; can defer to Phase B
   - `growdirect.app` — partner-network OpenAPI/Swagger documentation site (per epic dispatch D3); defer to Phase B
   - `growdirect.io` — operating company surface; defer to Phase B
   - `abalonecove.org` — Cove proposal-engine surface (continues as WPBCA HOA governance + future namespace expansion); coordinate with Cove maintainers
   - `ownpalosverdes.com` — namespace-adjacent geographic positioning; defer to Phase B
2. **Minimal site stand-up at the primary domain.** Single-page site with: index page (one-paragraph thesis + link to `/position`); `/position` page rendering `outputs/position-paper-eljeffe-io.md` cleanly; `/protocol` placeholder page (links to position paper; notes the formal protocol specification per epic dispatch C2 is forthcoming); favicon (the eljeffe wallet's signature symbol or a minimal King Harbor anchor). No JavaScript heavier than a static-site analytics snippet. No tracking pixels. No third-party trackers. The site renders in 200ms on a slow connection.
3. **Block-height anchor in footer.** Every page footer contains:
   - `Published as of Bitcoin block height [BLOCK_NNNNNN]`
   - `Position paper content hash: [hex_hash]`
   - `Inscribed at txid: [tx_id]` (links to mempool.space or another block explorer)
   - `King Harbor — Redondo Beach — pier`
4. **TLS configuration.** Let's Encrypt or equivalent; auto-renewal configured. Strict-Transport-Security header. No mixed content. HTTP/2 enabled. (PCI-related — keeps the site from being a soft target.)
5. **Email forwarding configuration.** Set up `[role]@[primary-domain]` forwarding for the principal roles (founder@, governance@, ops@, compliance-architecture@) to the appropriate humans during Phase A. Defer migration to a managed email service to Phase B once the team is larger than three.
6. **Robots.txt and sitemap.** Crawlable; no noindex directives on the position paper or the protocol page. We want this content discovered.

## Hosting choice — open decision

Two viable options. Founder picks; both work; the choice affects ongoing-cost shape and operational ownership.

**Option A — Cloudflare Pages.**
- Free tier covers the minimal site comfortably
- Integrated TLS, edge caching, DDoS protection
- Git-based deployment (push to main → live)
- Zero ongoing cost at the minimal-site scale; ~$5-20/month if the site grows beyond free-tier limits
- Operational owner: founder (push to repo; site updates)
- Trade-off: third-party dependency (Cloudflare); their TOS apply

**Option B — GCP Cloud Storage + Cloud Load Balancer.**
- ~$5-10/month for storage + load balancer + Cloud CDN
- Integrates cleanly with the eventual Canary.GO GCP infrastructure (per `crb-skills/saas-acquisition-diligence/Brain/diligence/rapidpos/03-gcp-onramp-architecture.md`)
- Single-vendor operational model (GCP everywhere)
- Operational owner: founder + technical contributor
- Trade-off: more configuration overhead than Cloudflare Pages; slightly higher ongoing cost

Recommendation: **Option A for Phase A** (minimal cost, fastest stand-up). Migrate to Option B in Phase B once the broader GCP footprint is being deployed and consolidating to one vendor reduces operational overhead.

## Block-height anchor mechanic — specific instructions

The position paper's content hash gets inscribed onto the Bitcoin chain as part of the publication moment. This is a substrate consistency requirement, not a marketing flourish. The mechanism:

1. Founder finalizes the position paper content
2. Compute SHA-256 hash of the position paper file (`outputs/position-paper-eljeffe-io.md`)
3. Inscribe the hash + a brief metadata line ("eljeffe Hash and Seal Protocol — Position Paper v1") into a Bitcoin transaction's witness data per the Ordinals protocol
4. Wait for the transaction to confirm; record the block height + txid
5. Update the page footer with the actual block height and txid
6. Publish the page

This produces a permanent on-chain record that the position paper as published at this exact content hash existed at this exact block height. Any subsequent edit to the published page that doesn't carry a new inscription is detectable by hash mismatch; any future claim that "this page was published earlier" is refutable by the block-height anchor; the substrate's first-mover position is established by the chain itself.

For the founder's eventual Wyoming-counsel review (per `outputs/dispatches/A1-wyoming-counsel-scope.md`): this inscription does not create a regulatory reporting trigger. It is a statement of fact about the content hash, not a transaction in the regulated sense. Counsel confirms this in Phase 1 of the A1 engagement.

## Cost estimates

| Line item | Phase A | Phase B+ |
| --- | --- | --- |
| Domain renewals (per the portfolio) | $200/year initial; $200-300/year ongoing | Same |
| TLS certificates | $0 (Let's Encrypt) | $0 |
| Hosting (Option A — Cloudflare Pages) | $0 | $0-20/month |
| CDN | Included in hosting | Included |
| Email forwarding (basic) | $0-5/month | Migrate to managed service ~$30-100/month |
| First inscription transaction fee | ~200-500 sat ($0.20-0.50 at $85K/BTC) | Per-publication-event same |
| **Total Phase A** | **~$250 + ~$0.50 inscription** | **~$300/year + per-publication inscription** |

The total is small. The substrate's posture: don't over-spend on infrastructure that isn't yet load-bearing; the minimal site is enough to establish position.

## Time estimates

| Step | Estimated time |
| --- | --- |
| DNS configuration | 30 min |
| Static-site setup (Option A) | 60-90 min |
| Position paper rendering check | 30 min |
| Inscription mechanic (compute hash, build tx, broadcast, confirm) | 30-90 min depending on fee market |
| Footer update with actual block height + txid | 15 min |
| TLS + headers verification | 15 min |
| Email forwarding configuration | 30 min |
| **Total** | **~3-5 hours of founder time** |

## Open items requiring resolution

1. **Primary canonical domain choice** (per epic open decision #3). Affects the DNS configuration centrally. Decision needed before week 4.
2. **Hosting choice** (Option A vs Option B). Defer-to-founder choice. Recommendation: Option A.
3. **Email-forwarding role names** (founder@, governance@, ops@, compliance-architecture@, or different naming). Founder confirms.
4. **Inscription wallet** (the founder's eljeffe wallet — confirm the inscription transaction comes from the principal-stake wallet so the provenance chain reads cleanly: F2Pool reward → founder wallet → first protocol inscription → first publication inscription).

## Cross-references

- `outputs/session-summary-and-company-formation-epic.md` — Category A dispatches (A4 this dispatch; A5 position paper drafting completed; A1 entity formation parallel; A2 Genesis block inscription separate from but related to publication inscription)
- `outputs/position-paper-eljeffe-io.md` — the content being published
- `outputs/investor-brief-eljeffe-io.md` — companion content (publish at `/investor-brief` or similar in Phase B; not the Phase A publication target)
- `outputs/dispatches/A1-wyoming-counsel-scope.md` — counsel confirms inscription is not a regulatory-reporting trigger
- Domain portfolio per the founder's secured list (in the company-formation epic Section "What the session added — Personal commitment + operational frame")

---

*DNS and publication scope. Ready for execution.*
*Block-height anchor recorded at first publication.*
