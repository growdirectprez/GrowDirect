---
classification: internal
type: wiki
status: active
date: 2026-04-25
last-compiled: 2026-04-25
needs-review: 2026-05-09
source: public-web research; methodology section in body
----

# Rapid POS / NCR Counterpoint — User Pain Points + FAQs

Synthesis of public-community discussion on Rapid POS, Rapid Garden POS, and
NCR Counterpoint (now NCR Voyix Counterpoint). Built from review platforms
(Capterra, G2, Software Advice, SoftwareConnect, TrustRadius, Software
Reviews / Info-Tech, GetApp), vendor-blog and trade-publication content,
the standing Counterpoint Users Group forum, and the public-web reference
material listed in `Brain/wiki/ncr-counterpoint-*.md`.

## Executive summary

The dominant pain in the public record is **support-and-bug fatigue**: users
across multiple verticals consistently report that recent versions ship
buggy, that NCR Voyix routes them to their VAR for resolution, and that
the customization layer they paid for is expensive to maintain because
every change requires a paid dealer engagement. Layer two is **functional
gaps not on the official feature list** — labor and scheduling, eCommerce
sync reliability, modern reporting discoverability, and modern web/mobile
UX. Layer three is **upgrade and end-of-life pressure** — perpetual-license
customers facing forced migrations to current versions, new payment
hardware, TLS requirements, and Secure Pay gateway transitions.

For a back-office analytics + LP layer like Canary, the implication is
clear: customers are not asking for a Counterpoint replacement — they are
asking for things Counterpoint does not natively do, layered on top of the
data Counterpoint already captures. Specifically: better reporting
discoverability, native labor/scheduling that lives next to sales data,
fraud / loss-prevention monitoring that uses the audit log Counterpoint
already writes, and a modern web/mobile surface for managers who do not
want to RDP into a Windows workstation to read a Crystal Report.

## Methodology

- **Time range:** primary focus on reviews and discussion 2022–2026, with
  contextual material older where it remained the most authoritative
  reference (e.g., 2017 forum activity reports, 2018 economic impact
  data).
- **Sources scanned:** ~25 distinct public sources across review
  platforms, vendor blogs, trade publications, NCR Voyix investor
  materials, the Counterpoint Users Group forum, and Garden Center
  Magazine state-of-industry coverage.
- **Distinct discussions reviewed:** ~90 user reviews aggregated across
  Capterra (NCR Voyix Counterpoint, 90+ reviews; Rapid Garden POS, 11
  reviews), G2 (352 reviews across NCR Voyix products), Software Advice,
  SoftwareConnect (5 reviews), TrustRadius, Software Reviews
  (Info-Tech), and SoftwareFinder. Reddit yielded no on-topic threads
  for "NCR Counterpoint POS" within search reach — the public Counterpoint
  conversation lives on review platforms and the (now-quiet) CPUSER.ORG
  forum, not on Reddit.
- **Confidence framework:** every theme below has at least two
  corroborating sources unless explicitly flagged as single-source.
- **Sanitization:** named retailers and reviewers are abstracted to
  archetype (vertical + size + role). Quotes are paraphrased where
  needed to remove identifying detail.

## Top pain points (ranked by frequency × severity)

### 1. Support has migrated entirely to the VAR channel — and customers feel abandoned

Across every public review platform, the single most-cited complaint is
that NCR Voyix itself does not provide direct end-user support and routes
all issues to the dealer / VAR who deployed the system. For customers on
older versions, on smaller dealers, or with dealers who don't specialize
in their vertical, this becomes a multi-hop, paid-by-the-hour escalation
path for problems they expect to be patched as bugs.

> "There is no technical support and the technical team does not care."
> — gift / novelty retailer, recent Capterra review
>
> "NCR will only advise to see a dealer." — multi-source aggregation
> across G2, Capterra, SoftwareConnect
>
> "Customer support is inconsistent — some reps are helpful, others
> create delays and extra charges." — retail, mid-size, Capterra

Confidence: **high** (multi-source, multi-vertical, recent).

### 2. New versions ship with bugs; patches are slow

Multiple recent (2024–2025) reviews report that releases on the current
8.6.x line introduce new instability. The most-cited symptom is the POS
UI crashing when the application is minimized or backgrounded, with the
in-progress ticket lost and unrecoverable.

> "New versions are full of bugs and there is no technical support."
> — consumer-goods retailer, October 2025 Capterra review
>
> "NCR Counterpoint will crash when minimized or hidden, and you would
> immediately lose the ticket … unable to be recovered at all."
> — computer-retail vertical, Capterra
>
> "There always seems to be something going wrong with it and constantly
> having to do patches or NCR does not fix things in a timely fashion."
> — G2 review

Confidence: **high** (multi-source, recent).

### 3. Customization is the value-add — and the lock-in

Counterpoint is praised for being deeply customizable (custom fields,
custom tables, custom Crystal Reports, dealer-built UI extensions). The
same depth is the most expensive ongoing cost in the system: every
custom field needs paid dealer support to maintain, every database-schema
upgrade can break custom columns, and customers who have invested heavily
in customization describe themselves as locked in.

> "We have so much money invested in customization that it's very
> difficult to part with." — retailer, multi-year Capterra review
>
> "Customization requires support with every aspect of custom fields,
> at high costs." — gift / novelty / tobacco retailer, Capterra
>
> "Crystal Reports has a long and very steep learning curve … advanced
> work benefits significantly from a certified NCR Counterpoint partner."
> — VAR-blog technical guidance (CCS Retail Systems)

Confidence: **high** (multi-source).

### 4. Reporting discoverability and accessibility

Counterpoint ships with 2,000+ canned reports plus a Crystal Reports
custom-builder. The repeated complaint is not that the system lacks
reporting — it's that users can't find the report they want, can't
modify it without dealer help, and can't access it from outside the
Windows workstation it was installed on.

> "No easy way to find reports that are available." — Rapid Garden POS
> retailer, 2+ years of use
>
> "Not good reporting in purchasing module. No open PO report, no
> expected delivery report." — Rapid Garden POS IT manager
>
> "Reports … require many workarounds to pull any type of reporting."
> — TrustRadius / SoftwareConnect aggregation

Confidence: **high**.

### 5. Labor / scheduling / timeclock is not in the product

Counterpoint exposes API users and roles, not employees, schedules, or
timeclocks. Customers who want labor data alongside sales must integrate
a third-party workforce-management product — TimeForge is the most
commonly mentioned integration partner. This gap is rarely surfaced as
a complaint per se because most users have learned to treat it as
"that's not what Counterpoint does," but it materially shapes what
managers see (or don't see) when they ask "what was payroll doing
during the slow hour on Tuesday?"

Confidence: **high** for the gap; **medium** for the framing as pain
(users have largely adapted around it).

Cross-references: `Brain/wiki/ncr-counterpoint-api-reference.md` Module L,
`Brain/wiki/ncr-counterpoint-endpoint-spine-map.md` "Spine modules with
no coverage."

### 6. eCommerce synchronization is brittle

Counterpoint syncs to Shopify, WooCommerce, BigCommerce, and Magento
through third-party middleware (Modern Retail / RDi, OctopusBridge by
24sevencommerce, POS Highway's sync app, etc.) — there is no
NCR-native eCommerce store. Public reviews routinely describe sync
breakage: prices not flowing from Counterpoint to the website, orders
arriving but not appearing in Counterpoint, manual import workarounds
becoming the daily norm.

> "Pricing not moving from Counterpoint to website; manual imports
> required. Orders being lost and irretrievable." — health/wellness
> retailer, Capterra
>
> "Lacks Facebook Shop or Instagram integration capabilities."
> — apparel retailer, Capterra

Confidence: **high**.

### 7. Hardware and payment terminal compatibility friction

Recent reviews of Rapid Garden POS specifically call out hardware
upgrades degrading the user experience — new printers and terminals
performing worse than the equipment they replaced — and Ingenico chip
readers being "slow, expensive, and not user friendly." This intersects
with the NCR Secure Pay gateway transition (a forced migration NCR has
been rolling out; older CP Gateway customers are required to upgrade
hardware and CounterPoint version together).

> "Updates cause problems EVERY time including printing, slow use."
> — garden center owner, 2+ years of use, Rapid Garden POS Capterra
>
> "Ingenico chip readers are a disaster — slow, expensive and not user
> friendly." — garden center owner, Rapid Garden POS Capterra

Confidence: **medium-high** (multiple Rapid Garden POS reviews;
narrower vertical exposure on the broader Counterpoint side).

### 8. Compliance gaps in regulated verticals

Sporting-goods reviewers flag ATF compliance violations introduced by
patches and not fixed in subsequent releases. Tobacco / novelty
reviewers flag tax-code implementation conflicts with state Department
of Revenue standards. These are vertical-specific but represent a
real risk surface for licensed retailers.

> "Routinely updates push violations with ATF, rarely gets fixed."
> — sporting goods retailer, Capterra
>
> "Tax codes conflict with Department of Revenue standards; unfixable
> design flaw." — gift / novelty / tobacco retailer, Capterra

Confidence: **medium** (single-source per vertical, but corroborated
by the existence of vertical-specific competitors — Bravo Store
Systems, Gearfire AXIS, Orchid Advisors, Trident 1 — each of which
positions ATF / state-compliance as their own primary differentiator
versus generic POS).

### 9. End-of-life and forced upgrade pressure

NCR ended support for all Counterpoint versions prior to 8.5.7.x on
2023-12-31, and as of 2024 supports only the current production
version plus the previous two releases. Customers running older
deployments face a forced migration that often pulls in new POS
hardware, new payment terminals, new TLS configuration, and a Secure
Pay gateway transition simultaneously. The migration is paid work
through the VAR.

> "The system would remain usable, but had a limited life expectancy
> with support continuing for 2-3 years." — VAR-blog summary of the
> v7.5 EOL announcement (Skurlas)
>
> "Continuing with outdated software poses risks; when support is
> needed, the system is no longer supported by regularly released
> patches." — Retail Control Systems blog

Confidence: **high**.

### 10. Pricing rules and complex price logic require expertise

Both Counterpoint generally and Rapid Garden POS specifically draw
complaints about the pricing-rules surface being more complex than
tutorials suggest. For verticals with multi-tier pricing (retail vs.
landscaper vs. commercial in garden centers; bulk-vs-unit in feed and
tack), the pricing engine is genuinely powerful but genuinely difficult
to use without dealer assistance.

> "Price rules function not as user friendly as tutorials suggest."
> — garden center manager, less than 6 months of use, Rapid Garden POS
>
> "Some users struggle with the price rules function … isn't as easy
> as tutorials make it seem." — Rapid Garden POS / SoftwareFinder
> aggregation

Confidence: **medium-high**.

## Top FAQs (and the answers users converge on)

### Q1. Is NCR Voyix still investing in Counterpoint?

**Public answer (vendor):** yes — Counterpoint is in the current
"specialty retail" lineup at NCR Voyix, with v8.6.x releases shipping
into 2026.

**What users converge on:** the perception across multiple recent
reviews is that NCR is investing less in Counterpoint than in its
larger Voyix Commerce Platform / DSR / Aloha lines. NCR Voyix's own
2025 investor materials describe an SMB segment that "was impacted by
headwinds related to market dynamics and the legacy nature of the
current SMB offering" — language the user community reads as
confirmation that Counterpoint's modernization budget is constrained.
The Aloha Next refresh is the announced SMB modernization vehicle on
the restaurant side; there is no announced Counterpoint Next on the
retail side as of Q1 2026.

### Q2. What's the difference between Counterpoint and Rapid Garden POS?

**Public answer:** Rapid Garden POS is NCR Counterpoint deployed by
Rapid POS LLC as an authorized VAR, with garden-center-tailored
configuration and Rapid-built customizations on top. Same database,
same REST API, same runtime — different vertical packaging.

This is the most asked structural question on vendor blogs and
buyer-guide sites. Most independent garden center buyers do not know
that "Rapid Garden POS" is Counterpoint until they ask, which means
purchase decisions are sometimes made under a misconception about
what the underlying platform is.

Cross-reference: `Brain/wiki/ncr-counterpoint-rapid-pos-relationship.md`.

### Q3. How do I integrate Counterpoint with Shopify / WooCommerce?

**Public answer:** through third-party middleware. The most-cited
integration vendors are Modern Retail / RDi (WooCommerce, Magento),
24sevencommerce / OctopusBridge (Shopify, Magento, BigCommerce), POS
Highway sync, and Retail Dimensions. None of these are NCR products.

**What users converge on:** the integrations work, but they are
brittle. Inventory and price flow Counterpoint → web reasonably well;
order flow web → Counterpoint is where most failure happens. Larger
retailers ultimately build their own integration glue.

### Q4. Does Counterpoint have employee scheduling or timeclock?

**Public answer:** no. The User / Role surface on the API is for API
access management, not for employee records, schedules, or timeclock.

**What users converge on:** integrate TimeForge, or accept that labor
data lives outside Counterpoint and reconcile manually.

### Q5. Why does my POS crash when I minimize the window?

**Public answer:** known behavior in current 8.6.x versions; the
in-progress ticket cannot be recovered.

**What users converge on:** train staff to never minimize the
Counterpoint window during a transaction. This is a workaround, not
a fix; recent reviews (October 2025 Capterra) still cite it.

### Q6. How much does Counterpoint actually cost?

**Public answer:** not published publicly. Public starting points
(via VAR pricing pages):
- Counterpoint Cloud: ~$149/month per license
- Counterpoint perpetual license: from ~$1,190 starting point
- Traditional subscription: ~$125/month single user, +$50/month per
  additional user
- VAR implementation: $2,000–$10,000 typical range; one Capterra
  review described paying $7,500 and still not going live
- Hardware: separate, on top of license

Total cost of ownership in the public review record clusters around
$5,000–$25,000 first-year for a single-store independent retailer
with mid-complexity customization, plus ongoing $2,000–$10,000/year
in dealer support and customization maintenance.

Confidence: **medium** — pricing is the hardest dimension to verify
publicly; the numbers above are aggregated from VAR pricing pages
that are themselves indicative, not contractual.

### Q7. What's the path off Counterpoint when we outgrow it?

**Public answer:** the most-cited public migration paths are Shopify
POS, Lightspeed Retail, and (for verticals with compliance needs)
vertical-specific replacements (Bravo for firearms / pawn, Gearfire
AXIS for firearms, Trident 1 for licensed verticals).

**What users converge on:** migration is painful because so much
business logic lives in customization and Crystal Reports. The
customers who do migrate are typically the ones who never invested
heavily in customization in the first place.

### Q8. Can I get my data out of Counterpoint?

**Public answer:** yes — the REST API exposes the bulk of the
domain (Document, Customer, Item, Inventory, etc.); direct ODBC
to the underlying SQL Server is also a documented path. The
Counterpoint Users Group historically provided community-built tools
for export.

**What users converge on:** the API is real, but the API is also a
paid Counterpoint license add-on (`registration.ini` API option) and
the rate-limiting / caching policy makes it less useful for
real-time analytics than for incremental batch sync. The path most
back-office tools take is direct database read.

### Q9. How do I track shrinkage / dead-count for live goods?

**Public answer:** Counterpoint's standard shrinkage workflow is
inventory adjustments + return-to-vendor (RTV) Documents.
Garden-center-specific dead-count workflows are vendor-built on
top, not native.

**What users converge on:** most independent garden centers either
build a custom Counterpoint workflow (paid dealer engagement) or
track dead-count outside the system entirely. The 78% of shrinkage
attributable to spoilage in garden-center retail (per AMS Retail
trade-pub citation) is a cost center that is often invisible to the
POS.

### Q10. Where do I find other Counterpoint users to ask questions?

**Public answer:** historically the CPUSER.ORG independent users
group; the founder Gordon Gelrod ran free open-forum support since
2003. The forum closed after his passing (per a 2021 POS Pondering
notice). The remaining option is vendor-run knowledge bases (CPSQL
Knowledge Base) and the small forum at counterpointapp.org.

**What users converge on:** the Counterpoint independent community
is materially smaller than it was in 2015–2018. New customers
typically rely on their VAR's knowledge base and ticketing; they do
not have a peer community to triangulate against.

## Gap-to-opportunity mapping (Canary modules)

| Pain | Canary module that addresses it | How |
|---|---|---|
| Support migrated to VAR channel | All modules | Canary as a self-serve back-office layer reduces the share of issues that have to go through a paid dealer call |
| New-version bug fatigue | Q (Loss Prevention monitoring) | Canary detects anomalous behavior (lost tickets, drawer-session breaks) without requiring fixes inside Counterpoint |
| Customization lock-in | Module surface (read-only) | Canary reads what Counterpoint already captures (Document, audit log, pricing decisions) — no schema change inside Counterpoint, no new dealer engagement |
| Reporting discoverability | T + R + F (Transactions, Customer, Finance) — modern web UI on top of CRDM | Cloud-accessible web dashboards replace "RDP into the workstation to find a Crystal Report" |
| **Labor / scheduling gap** | **Module L native build** — opportunity | Counterpoint has no native L; if Canary builds Module L from store-level timeclock data sources, this is greenfield, not displacement |
| eCommerce sync brittleness | Q + T monitoring | Canary monitors order flow web → Counterpoint and alerts on backlog / mismatch instead of replacing the integration |
| Hardware / payment friction | Out of scope for Canary | Canary doesn't replace POS hardware or payment processors; this is a Rapid POS / NCR concern |
| Compliance gaps (vertical) | Q (LP rules per vertical) | Canary's rules engine can encode vertical-specific compliance checks (ATF, tax-code reconciliation) without modifying Counterpoint itself |
| End-of-life pressure | Adapter neutrality | Canary's CRDM abstracts the upstream; if a customer eventually migrates to a different POS, Canary's L/Q/reporting layer doesn't have to be rebuilt |
| Pricing rules complexity | P (derived) | Canary observes pricing decisions per line (PS_DOC_LIN_PRICE) — managers see what rules actually fire without having to read the rule definitions |

The strongest opportunity surface is the convergence of: (a) gap not in
Counterpoint at all (L), (b) pain Counterpoint causes that customers
have learned to live with (reporting discoverability, eCommerce sync
visibility), and (c) anomaly detection that Counterpoint's own audit
log already captures but doesn't surface (Q).

## Workarounds users have built

These show up across reviews and forum threads:

1. **Don't minimize the POS window.** Train staff to leave the POS
   foreground always; lock the workstation rather than minimizing.
2. **Daily manual eCommerce reconciliation.** Some health/wellness and
   apparel retailers reconcile web orders to Counterpoint by
   spreadsheet every morning rather than relying on the integration.
3. **Pay dealer for every custom field.** Customers normalize the cost
   of every schema change as a paid line item.
4. **Track special orders on a clipboard.** Multiple garden-center
   reviews describe special-order tracking happening on paper or in a
   spreadsheet because the in-system workflow is too slow.
5. **Crystal-report exports as the only reliable reporting surface.**
   Managers run a saved Crystal report nightly, export to PDF or
   Excel, and read in Excel rather than in the Counterpoint UI.
6. **Use TimeForge for labor.** The dominant integration when
   Counterpoint customers want labor data alongside sales.
7. **Direct ODBC for ad-hoc reporting.** Power users skip Crystal
   Reports and go directly against the SQL Server with their own
   queries — accepting the risk that schema changes will break their
   queries on upgrade.

## Sanitized user quotes (selected, ~10)

1. "There is no technical support and the technical team does not care."
   — gift / novelty retailer, Capterra (recent)
2. "New versions are full of bugs and there is no technical support."
   — consumer-goods retailer, Capterra (October 2025)
3. "We have so much money invested in customization that it's very
   difficult to part with." — retailer, Capterra
4. "NCR Counterpoint will crash when minimized or hidden, and you would
   immediately lose the ticket … unable to be recovered at all."
   — computer-retail vertical, Capterra
5. "Updates cause problems EVERY time including printing, slow use."
   — garden center owner, Rapid Garden POS Capterra (2+ years use)
6. "Seemingly constant replication problems create distrust in our
   numbers." — garden center owner, Rapid Garden POS Capterra
7. "Routinely updates push violations with ATF, rarely gets fixed."
   — sporting goods retailer, Capterra
8. "Pricing not moving from Counterpoint to website; manual imports
   required. Orders being lost and irretrievable."
   — health / wellness retailer, Capterra
9. "Price rules function not as user friendly as tutorials suggest."
   — garden center manager, Rapid Garden POS Capterra (<6 months use)
10. "More focused on solving problems than preventing them." — VP at
    20-year garden-supply Rapid Garden POS customer, Capterra

## Open questions (not answerable from public sources alone)

1. **Actual Counterpoint installed base.** Public-record floor: one VAR
   (CCS Retail Systems) cites ~2,000 supported users; total Voyix
   "platform sites" across all products is 80,000 (Q4 2025) but is
   not Counterpoint-specific. Real number requires NCR Voyix internal
   data.
2. **Rapid POS customer count by vertical.** Rapid markets garden,
   gun, feed-and-tack, food, and wine separately under sub-brands;
   no public count by vertical.
3. **VAR channel concentration.** How much of the Counterpoint
   installed base is concentrated in the top 5–10 VARs (Rapid POS,
   AMS Retail, RCS, Mariner, POS Highway, C&K Systems, NCC, RBMS,
   Retail Dimensions, CCS Retail Systems) vs. long-tail dealers?
   This shapes Canary's go-to-market: VAR partner deals vs. direct
   to retailer.
4. **Churn rate.** Public reviews surface dissatisfaction but not how
   many customers actually leave per year. Counterpoint customers
   describe themselves as locked in by customization, suggesting low
   churn — but anecdote, not data.
5. **Per-customer customization spend.** Reviews mention "thousands"
   and "tens of thousands" but no aggregate. Canary's pricing power
   is bounded by what customers already spend on the dealer; we
   don't know that ceiling.
6. **Real adoption rate of the Counterpoint REST API.** The API is a
   paid add-on (registration.ini option). What percentage of the
   installed base has it enabled? If it's low, Canary's adapter
   strategy may need a direct-DB fallback as primary, not secondary.
7. **Ratio of Rapid Garden POS customers running with Rapid-specific
   custom tables vs. stock Counterpoint.** Affects how much of
   Canary's adapter has to handle Rapid-proprietary surfaces vs.
   standard API.
8. **Customer attitudes toward "yet another vendor in the stack."**
   Counterpoint customers already pay NCR + VAR + integration
   middleware vendors + payment processor + (sometimes) workforce
   vendor. Adding Canary is the Nth contract; how price-sensitive is
   that decision?

## Sources

### Review platforms

- Capterra — NCR Voyix Counterpoint reviews (90+):
  [capterra.com/p/7227](https://www.capterra.com/p/7227/NCR-Counterpoint/reviews/)
- Capterra — Rapid Garden POS reviews (11):
  [capterra.com/p/151139](https://www.capterra.com/p/151139/Rapid-Garden-POS/reviews/)
- G2 — NCR Voyix Counterpoint reviews:
  [g2.com/products/ncr-counterpoint-pos](https://www.g2.com/products/ncr-counterpoint-pos/reviews)
- Software Advice — NCR Voyix:
  [softwareadvice.com/product/1058](https://www.softwareadvice.com/product/1058-NCR-Counterpoint/reviews/)
- Software Advice — Rapid Garden POS:
  [softwareadvice.com/retail/rapid-garden-profile](https://www.softwareadvice.com/retail/rapid-garden-profile/)
- SoftwareConnect — NCR Counterpoint:
  [softwareconnect.com/reviews/ncr-counterpoint](https://softwareconnect.com/reviews/ncr-counterpoint/)
- TrustRadius — NCR Voyix Counterpoint:
  [trustradius.com/products/ncr-voyix-counterpoint](https://www.trustradius.com/products/ncr-voyix-counterpoint/reviews)
- GetApp — NCR Voyix:
  [getapp.com/.../ncr-counterpoint](https://www.getapp.com/customer-management-software/a/ncr-counterpoint/reviews/)
- Software Reviews / Info-Tech — NCR Voyix Counterpoint:
  [infotech.com/.../ncr-voyix-counterpoint](https://www.infotech.com/software-reviews/products/ncr-voyix-counterpoint?c_id=6)
- SoftwareFinder — Rapid Garden POS:
  [softwarefinder.com/retail/rapid-garden-pos](https://softwarefinder.com/retail/rapid-garden-pos)

### VAR / vendor / community

- Counterpoint Users Group (CPUSER.ORG, historical, now closed):
  [cpuser.org](http://cpuser.org/)
- POS Pondering — CPUSER.ORG closure notice (2021):
  [pospondering.com — closed forum](http://www.pospondering.com/2021/06/nrc-counterpoint-users-group-and-forum.html)
- counterpointapp.org forum:
  [counterpointapp.org/forum](https://www.counterpointapp.org/forum/)
- CCS Retail Systems blog — Crystal Reports guidance (2013):
  [ccsretailsystems.com/.../ncr-counterpoint-and-crystal-report-writer](https://ccsretailsystems.com/2013/01/12/ncr-counterpoint-and-crystal-report-writer/)
- Skurlas — CP Gateway end-of-life:
  [skurlas.com/.../cp-gateway-end-of-life](https://www.skurlas.com/counterpoint-news/ncr-counterpoint-cp-gateway-end-of-life-0-0-0)
- AMS Retail — Counterpoint customization guide:
  [amsretail.com/.../customizing-ncr-counterpoint-software](https://amsretail.com/feeds/blog/customizing-ncr-counterpoint-software)
- AMS Retail — Counterpoint for garden centers:
  [amsretail.com/.../ncr-counterpoint-garden-center](https://amsretail.com/feeds/blog/ncr-counterpoint-garden-center)
- RCS — outdated hardware risks:
  [retailcontrolsystems.com/.../the-hidden-risks-of-outdated-hardware](https://www.retailcontrolsystems.com/blog/the-hidden-risks-of-outdated-hardware-in-retail-why-its-time-for-an-upgrade/)
- POS Highway — Shopify-to-Counterpoint integration:
  [poshighway.com/integrations/shopify-to-counterpoint](https://www.poshighway.com/integrations/shopify-to-counterpoint/)
- TimeForge — NCR Counterpoint integration:
  [timeforge.com/integrations/ncr-counterpoint](https://timeforge.com/integrations/ncr-counterpoint/)
- 24sevencommerce — Counterpoint-eCommerce integration:
  [24sevencommerce.com/counterpoint-pos-ecommerce-integration](https://www.24sevencommerce.com/counterpoint-pos-ecommerce-integration.html)

### Trade publications

- Garden Center Magazine — 2024 State of the Industry:
  [gardencentermag.com/.../2024-state-independent-garden-centers-industry-report](https://www.gardencentermag.com/article/2024-state-independent-garden-centers-industry-report/)
- Greenhouse Grower — POS buying guide:
  [greenhousegrower.com/.../how-to-pick-the-best-pos-for-your-garden-store](https://www.greenhousegrower.com/management/retailing/how-to-pick-the-best-pos-for-your-garden-store/)

## Closing summary

Defensible: the support / VAR-routing complaint, the bug-fatigue
complaint, the customization lock-in pattern, the labor / scheduling
gap, and the eCommerce sync brittleness are all corroborated across
multiple recent reviews and multiple platforms. The end-of-life
pressure and Secure Pay migration timeline are corroborated by VAR
publications and NCR's own announcements.

Gappy: the actual installed-base count, the per-customer customization
spend, and the churn rate. Public sources do not produce defensible
numbers for any of these.

Would need NCR / Rapid POS internal data to resolve: the count of
active customers per VAR per vertical, the actual API enablement rate
across the installed base, and the dollar value of dealer-supported
customization across the customer base. These are the questions that
would let Canary size pricing and channel strategy precisely; today
the public web supports a posture, not a precise plan.

## Related

- [[Brain/wiki/ncr-counterpoint-api-reference|NCR Counterpoint API Reference]]
- [[Brain/wiki/ncr-counterpoint-document-model|NCR Counterpoint Document Model]]
- [[Brain/wiki/ncr-counterpoint-rapid-pos-relationship|Counterpoint vs Rapid Garden POS — Relationship]]
- [[Brain/wiki/ncr-counterpoint-endpoint-spine-map|NCR Counterpoint Endpoint × CRDM × Spine Map]]
- [[Brain/wiki/rapid-pos-counterpoint-market-research-tam|Rapid POS / Counterpoint — Market Research + TAM]]
- `docs/sdds/canary/ncr-counterpoint-retail-spine-integration.md`
