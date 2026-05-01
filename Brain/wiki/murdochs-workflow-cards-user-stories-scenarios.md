---
date: 2026-04-30
type: wiki
status: active
tags: [canary, murdochs, catz, crb, hawk, cove, user-stories, workflows, farm-ranch, firearms, live-animals, bopis, agentic]
sources:
  - Brain/raw/inbox/murdochs/_manifest.md
  - Brain/wiki/murdochs-ranch-home-supply-proof-case.md
  - Brain/wiki/catz-method.md
  - Brain/process-decomp/CRB-PROCESS-MAP.md
  - docs/sdds/go-handoff/hawk-case-management.md
method-role: Writer
method-stage: design
last-compiled: 2026-04-30
needs-review: 2026-05-14
---

**Wiki:** [[Brain/Home|Home]] → [[Brain/projects/Canary|Canary]] → [[Brain/wiki/murdochs-ranch-home-supply-proof-case|Murdoch's Proof Case]]

# Murdoch's Ranch & Home Supply — In-Store Workflow Cards, User Stories & Scenarios

## Governing Thesis

Murdoch's operates 47 stores across six Western states with a catalog of 40,774 SKUs spanning twelve departments — from firearms and agricultural chemicals to live poultry and camping gear. The compliance surface is not incidental to the business; it is the business. Every department carries a distinct regulatory regime. Every state draw from the 47-store footprint modifies that regime in a different direction. Today, the operational response to this complexity is a combination of printed compliance binders, cashier training, manager discretion, and institutional memory that retires whenever a long-tenure employee does.

The platform's answer is not a database. It is an agent-native operating layer that resolves the "Can I sell this here, to this customer, right now?" question at the moment of transaction — and captures every exception, deviation, and compliance event as a structured case record the organization can actually use. The work cards below map Murdoch's in-store workflow families to CRB process modules, Hawk incident types, and the Cove governance surface. They are the Phase I As-Is inventory and the Phase II To-Be design brief in a single artifact.

---

## Workflow Inventory — Department × Compliance Regime × CRB Module

The crawl confirms that Murdoch's brand identity as a "farm and ranch" store understates the catalog's actual shape. Farm & Ranch is 1,025 URLs — the *smallest* of the eight major departments. The real volume lives in Clothing/Footwear (9,349), Pets/Livestock (6,963), Sporting Goods (5,356, of which 3,016 are Shooting SKUs), and Tools/Hardware (5,353). The highest regulatory density, however, sits in the smallest departments. Firearms, ag chemicals, and live animals each carry compliance obligations that dwarf their catalog footprint.

| Work Card | Workflow Family | Dept | SKU Count | Compliance Class | CRB Modules | Priority |
|---|---|---|---:|---|---|:---:|
| WC-01 | Firearms Counter | Sporting Goods → Shooting | 3,016 | Federal + multi-state | T, S, N, Q, Hawk | P1 |
| WC-02 | Agricultural Chemicals | Farm/Ranch → Ag Chemicals | 29 | Federal + state EPA | S, N, Hawk | P1 |
| WC-03 | Live Animal & Poultry | Pets/Livestock → Poultry (569) / Livestock (952) | 1,521 | State ag + biosecurity | S, N, T, Hawk | P1 |
| WC-04 | Outdoor Power Equipment Service | Lawn/Garden → OPE | 1,029 | Warranty + MAP | S, T, Q | P2 |
| WC-05 | BOPIS Fulfillment | Cross-department | ~40,774 | Age gate + ID at pickup | T, R, S, Q | P1 |
| WC-06 | Seeds & Plant Quarantine | Lawn/Garden → plants-bulbs-seeds | 1,304 | State ag quarantine | S, N | P2 |
| WC-07 | Feed & Livestock Nutrition | Pets/Livestock → Horse (2,298) + Cattle (952) | 3,250 | Medicated feed + feed store license | S, N, T | P2 |
| WC-08 | Workwear & PPE Sales | Clothing/Footwear/Accessories | 9,349 | OSHA attributes (informational) | S | P3 |
| WC-09 | Cashier Exception Handling | Transaction layer | All | Internal policy + state | T, Q, Hawk | P1 |
| WC-10 | Store Opening / Manager Compliance Sweep | Operations | All stores | Multi-regime daily | N, Q, Hawk, Cove | P1 |

---

## Functional Work Cards

Each card is structured as: actor(s) · trigger · workflow steps · compliance gates · CRB L2 mapping · Hawk incident types · automation posture.

---

### WC-01 · Firearms Counter Compliance

**Actors:** Firearms associate, store manager, customer, ATF (as regulatory authority)  
**Trigger:** Customer requests a firearm, ammunition with legal restrictions, or magazine/accessory subject to state ordinance.

**Workflow steps:**
1. Associate identifies SKU and pulls item authorization record — federal classification, state restriction overlay for store location, magazine capacity ordinance if applicable.
2. Age verification: 18+ for long guns, 21+ for handguns, state-specific elevations where enacted.
3. NICS check initiation (federal): associate confirms ATF Form 4473 capture.
4. State-level checks: Colorado and Montana each carry distinct magazine capacity and feature-test rules. Wyoming and Idaho follow federal baseline. Texas has no additional state overlay. Nebraska: single-store footprint (Scottsbluff), federal baseline.
5. NICS proceed / delay / deny outcome logged as a hash-verified event.
6. ATF Form 4473 retention obligation created with 20-year due date.

**Compliance gates:**
- Item authorization contract: `item_eligibility × site_regulatory_zone × operational_blocks`
- Magazine capacity: CO counties (Denver, Boulder, others) have specific ordinances overlaying state law
- MAP pricing: ~9% of catalog hides price until clerk action (confirmed in crawl); firearms likely in this bucket

**CRB L2 mapping:** S.3 (item authorization), N.4 (site regulatory zone config), T.2 (sealing + integrity), T.4 (SALE event publication), Q.4 (alert trigger), Q.5 (alert delivery)

**Hawk incident types triggered by failure:** `procedural_non_compliance` (PV track), `register_manipulation` (if price override), `external` class if denied customer becomes confrontational

**Automation posture:** Agent answers "Can I sell this here?" in real time at the POS terminal. NICS workflow is associate-assisted (ATF requires a human to administer Form 4473); the platform captures, seals, and anchors the record, but does not automate the check itself. Compliance obligation (20-year retention) created automatically on Form 4473 capture.

---

### WC-02 · Agricultural Chemicals

**Actors:** Ag department associate, customer (potentially requires pesticide applicator license), state EPA (regulatory)  
**Trigger:** Customer requests a restricted-use pesticide, herbicide, or ag chemical.

**Workflow steps:**
1. Associate scans SKU → platform queries restriction class: general use, restricted use, or state-specific (e.g., Grazon Next HL is EPA-restricted; Ranger Pro requires applicator license in some states).
2. If restricted-use: verify current pesticide applicator license (state-issued, expiry tracked).
3. Restricted-use sale requires customer ID and license number captured to transaction record.
4. Cross-state check: MT, WY, CO, ID, TX, NE each have distinct ag chemical registration requirements. The same product may be registered in four states but not a fifth.
5. Sale completed or blocked. If blocked, Hawk case created with compliance obligation to document the refusal.

**CRB L2 mapping:** S.3 (item authorization), S.5 (item lifecycle / restriction flag), N.4 (site regulatory zone), Q.3 (case intake via Fox/Hawk)

**Hawk incident types:** `procedural_non_compliance` (failure to verify license), `safety_violation` (sale completed without verification)

**Automation posture:** Full agent resolution at point of inquiry. Restriction lookup is a platform query against the item authorization record. License verification is associate-executed (physical document); platform captures and anchors the record. Expiry-date tracking on customer's applicator license creates a Cove-managed obligation that surfaces on renewal.

---

### WC-03 · Live Animal & Poultry Sales

**Actors:** Livestock associate, store manager, customer, state veterinarian (regulatory)  
**Trigger:** Spring chick days, livestock purchase event, beekeeping nuc sale, or any live animal transaction.

**Workflow steps:**
1. Seasonal listing state check: live birds are active-status only during the seasonal window (March–May typically). Platform gate prevents sale outside the window.
2. Biosecurity protocol delivery: associate provides customer with species-specific biosecurity card at transaction time. Montana and Wyoming have distinct bird flu response protocols (2025–2026 active).
3. Interstate transport check: customer shipping live animals across state lines requires USDA health certificate in most combinations. Platform flags the restriction; associate completes the physical paperwork.
4. Quantity limits: some state veterinarians set minimum flock sizes for small-scale purchases. Platform enforces at transaction.
5. Live animal transaction logged as a species-typed event — distinct from general merchandise transactions for reporting purposes.

**CRB L2 mapping:** S.4 (seasonal listing state), S.3 (item authorization + species flag), N.4 (site regulatory zone), T.3 (provider-keyed parsing — species attribute extraction), T.4 (SALE event with species payload)

**Hawk incident types:** `safety_violation` (biosecurity breach), `procedural_non_compliance` (sale outside seasonal window or without biosecurity delivery), `incident` class (animal health event in store)

**Automation posture:** Seasonal window gate is fully automated — the platform activates and deactivates the SKU class on the configured dates. Biosecurity card delivery is associate-executed; the platform generates the current-state card from the knowledge base rather than a printed binder. Interstate transport flag is agent-surfaced at POS; associate completes the physical USDA paperwork.

---

### WC-04 · Outdoor Power Equipment Service Counter

**Actors:** OPE associate, service technician, customer  
**Trigger:** Customer brings in a STIHL chainsaw, Husqvarna mower, or other OPE for service; or purchases and registers a new unit.

**Workflow steps:**
1. Serial number captured → item linked to customer account → warranty status queried against manufacturer records.
2. Service intake form created (Hawk case, `incident` class, equipment type coded in wizard template).
3. Parts order initiated if out-of-stock — cross-referenced against item master using dual-key (SKU + MPN) confirmed in crawl.
4. MAP pricing gate: new OPE units are in the MAP-gated segment (~9% of catalog). Associate triggers "click to view price" equivalent for floor pricing; quote is recorded.
5. Loaner/rental program (if active): separate transaction type, distinct from sale.
6. Service complete → customer notification via platform alert. Case closed with resolution summary → card generated.

**CRB L2 mapping:** S.2 (item master, dual-key lookup), S.5 (warranty lifecycle flag), T.3 (service transaction parsing), Q.7 (MCP investigator tools for service follow-up)

**Hawk incident types:** `incident` class (equipment damage on service intake), `procedural_non_compliance` (MAP pricing breach)

**Automation posture:** Serial number lookup and warranty status are agent-resolved at the service counter. Service case creation and card generation are automated on case close. MAP price visibility requires associate-confirmed trigger (by design — MAP is a manufacturer rule, not a platform decision).

---

### WC-05 · BOPIS Fulfillment

**Actors:** Online customer, pick associate, customer service associate at pickup counter  
**Trigger:** Customer places BOPIS order online; inventory is committed; customer arrives for pickup.

**Workflow steps:**
1. Order received → item authorization re-run at fulfillment time (age-gated or restricted items must clear the same gate at pickup as at online order). Crawl confirmed the "Find in a Murdoch's store" path is a parallel UI track on every PDP.
2. Pick associate locates item against on-hand inventory (BOPIS inventory XHR is the highest-priority open question from the crawl — contract not yet captured).
3. Substitution logic: if inventory changes between order and pickup, platform surfaces approved substitutions against the same item hierarchy.
4. Age-gated items (firearms, ammunition, OTC pharmaceuticals, agricultural chemicals): customer presents ID at pickup counter. Platform verifies age gate at handoff — second authorization event.
5. Pickup confirmed → transaction sealed → Merkle leaf written.

**CRB L2 mapping:** T.1 (adapter ingress — BOPIS order event), T.3 (BOPIS-typed document parsing), T.4 (BOPIS SALE event), C.2 (customer identity at pickup), S.3 (item authorization at fulfillment), Q.2 (BOPIS shrink detection rules)

**Hawk incident types:** `procedural_non_compliance` (age gate bypassed at pickup), `grab_and_run` (BOPIS used to stage pick and skip the counter)

**Automation posture:** Age gate re-verification at pickup is fully automated — the platform fires the item authorization contract a second time. Inventory commitment and substitution logic require the BOPIS inventory XHR contract (open question). Shrink detection runs the same rules on BOPIS transactions as in-store.

---

### WC-06 · Seed & Plant Quarantine

**Actors:** Garden center associate, customer, state department of agriculture  
**Trigger:** Customer selects seeds or plants from the garden center; item may carry a state quarantine restriction.

**Workflow steps:**
1. SKU carries quarantine flag: species × state matrix determines whether the item can be sold at this store's state location.
2. Associate is surfaced: "This item is restricted for sale in Montana. It is available for shipment to Wyoming." (Equivalent to the ag chemical restriction but at species level.)
3. Quarantine-aware replenishment: the platform prevents cross-state transfer of restricted species before the sale event — the item should not be on the shelf in Montana if it carries a MT prohibition.

**CRB L2 mapping:** S.3 (item authorization, quarantine flag), N.4 (site regulatory zone — quarantine zone config), S.4 (seasonal listing state — seasonal seed activation)

**Hawk incident types:** `procedural_non_compliance` (quarantine-restricted item sold), `safety_violation` (restricted species shipped across state lines)

**Automation posture:** Quarantine gate is fully automated at POS and at replenishment. The species × state matrix lives in the item authorization knowledge base, not in a printed list.

---

### WC-09 · Cashier Exception Handling

**Actors:** Cashier, floor supervisor, loss prevention manager  
**Trigger:** Void request, discount override, return without receipt, post-transaction price adjustment, MAP price inquiry from customer.

**Workflow steps:**
1. Exception initiated at POS → platform fires exception type classification.
2. Void: if post-tender, supervisor authorization required. Void reason code captured. Platform checks against configured allow-list (Q-VO-01).
3. Discount: percent-off against configured cap (Q-DR-01). Override above cap requires manager PIN + reason code.
4. Return without receipt: platform cross-references customer identity (if known) against prior transaction history. High-risk returns (high-value item, short interval, no receipt) auto-create a Hawk case of type `register_discrepancies`.
5. All exception events flow through the Merkle anchoring pipeline (T.5) — every cashier exception has a hash-verified timestamp.

**CRB L2 mapping:** T.3.7 (audit log flattening), T.4.3 (VOID event), T.4.6 (AUDIT-LOG event), Q.2 (detection rules: Q-VO-01, Q-DR-01, Q-DC-01), Q.3 (case management), Q.4 (alert trigger), Q.5 (alert delivery)

**Hawk incident types:** `register_discrepancies` (PV track), `cash_theft` (DE track if internal), `procedural_non_compliance`

**Automation posture:** Detection is fully automated — the Q detection rules fire on every exception event. Alert delivery is real-time. Case creation is triggered automatically when a threshold is crossed. Supervisor authorization workflows (PIN capture, reason code) are human-executed; the platform captures and anchors the record.

---

### WC-10 · Store Opening / Manager Compliance Sweep

**Actors:** Store manager, department leads, district manager (review surface)  
**Trigger:** Daily store opening; weekly district compliance review; regulatory inspection arrival.

**Workflow steps:**
1. Daily checklist: temperature logs for live animal areas, regulatory posting verification (firearms, pesticide applicator requirements, labor law postings), drawer baseline confirmation.
2. Seasonal calendar: platform surfaces the current seasonal activation state — which live animal SKUs are active, which seed varieties have quarantine flags updated since last week, which state has issued a new ag chemical restriction.
3. Training compliance: associate certifications tracked against expiry (firearms sales authorization, pesticide sales training, OSHA-required PPE training). Expiry approaching → Cove notification to manager.
4. Regulatory inspection: if an ATF, state EPA, or state ag inspector arrives, the manager pulls the Hawk compliance obligation record — every Form 4473, every restricted-use sale, every biosecurity event — as a hash-verified export.
5. Compliance sweep complete → summary card generated and routed to district manager via Cove communication thread.

**CRB L2 mapping:** N.4 (store config baseline), N.5 (device health alerts), Q.6 (allow-list management), Q.7 (MCP investigator tools)

**Hawk incident types:** `safety_violation`, `procedural_non_compliance`, `incident` (inspection event)

**Cove governance mapping:** Each store is a governed entity in Cove's model — analogous to a parcel in the HOA framework. Obligations (regulatory postings, training expiries, inspection deadlines) are Cove obligations with due dates and responsible parties. SOPs (the compliance binders that today live in three-ring binders behind the service counter) are Cove documents, versioned, searchable, and accessible from the POS terminal. District manager review is a Cove communication thread, not an email chain.

**Automation posture:** Calendar-driven seasonal updates are fully automated. Training expiry notifications are Cove-generated on a configurable lead-time. Hash-verified compliance export for inspectors is a single MCP tool call — `hawk_compliance_export(store_id, date_range, obligation_class)`. The daily checklist is agent-assisted: the manager confirms completion, the platform records and seals the confirmation event.

---

## User Stories

### WC-01 — Firearms Counter

> **As a firearms associate at the Fort Collins store**, I want to ask the agent "Can I sell a 20-round magazine for a Ruger 10/22 to this customer?" and receive a definitive answer with the applicable Colorado ordinance citation — so I don't have to call the manager or guess.

> **As a store manager**, I want every NICS outcome and Form 4473 reference automatically attached to the transaction record and retained for 20 years — so an ATF inspection can be satisfied without a manual records search.

> **As a district manager**, I want a cross-store view of firearms compliance events (denied sales, Form 4473 volumes, ordinance-blocked transactions by location) in a single dashboard — so I can identify stores that need additional associate training before the next inspection.

---

### WC-03 — Live Animal & Poultry

> **As a livestock associate during spring chick days**, I want the platform to prevent sale of live birds outside the active seasonal window and surface the current biosecurity card for Montana's bird flu protocol — so I never accidentally violate the state ag department's current order.

> **As a customer buying live chicks in Wyoming**, I want to know at the point of sale which states I can legally transport them to and what documentation I need — so I don't discover a compliance issue at a state line.

---

### WC-05 — BOPIS Fulfillment

> **As a BOPIS pick associate**, I want the system to flag any age-gated item in the pickup queue before the customer arrives — so I can stage the ID verification step rather than discovering the issue at the counter with a line behind the customer.

> **As a loss prevention manager**, I want BOPIS transactions to run the same shrink detection rules as in-store transactions — so grab-and-run patterns that route through the BOPIS queue are visible in the same alert surface as floor events.

---

### WC-09 — Cashier Exception Handling

> **As a cashier**, I want the system to tell me whether a void requires supervisor authorization *before* I initiate it — not after — so I'm not left waiting with a customer while I track down a floor manager.

> **As a loss prevention investigator**, I want a return-without-receipt transaction that triggers my configured risk threshold to automatically create a Hawk case — so the event is documented before the customer leaves the store, not reconstructed from video three days later.

---

## Scenarios

### Scenario A — Magazine Capacity Ordinance, Fort Collins CO

A customer at the Fort Collins store is looking at a 30-round magazine for a Ruger 10/22. She has a valid Colorado driver's license and is over 21. The associate asks the agent at the POS terminal.

**Without the platform:** The associate checks a laminated card from 2023 that lists "Colorado magazine restrictions" generically. Fort Collins is in Larimer County, which follows Colorado's 2023 magazine capacity law (15-round limit). The associate isn't sure if the county ordinance supersedes the state. He calls the manager. The manager isn't sure either. They decline the sale to be safe. The customer buys the magazine online from a Montana retailer who ships to Wyoming and drives down. The store loses the sale. The compliance event is undocumented.

**With the platform:** Associate's query resolves: *"Restricted at this store. Colorado HB23-1230 limits magazine capacity to 15 rounds. This item (30-round) may not be sold in Colorado. Item is available at your Laramie WY store (43 min). Customer may also order for shipment to a WY address."* Associate explains the restriction with a citation. Customer is directed to the Laramie option. The declined-sale event is logged as a `procedural_non_compliance` case (resolved: blocked by regulation) with the Colorado statute reference. The compliance record exists before the customer leaves the counter.

---

### Scenario B — Spring Chick Days, Billings MT

It is February 15th. A customer wants to buy six chicks from the seasonal livestock area. The store's spring chick program is scheduled to activate March 1st per the state ag calendar.

**Without the platform:** A new associate doesn't know the activation date. Live birds are on the shelf (a delivery arrived early). She completes the sale. The Montana Department of Livestock's current biosecurity order requires a minimum of 6 chicks with an accompanying biosecurity acknowledgment, and the sale window is March 1 through May 31. The sale was technically in violation. No record exists.

**With the platform:** The SKU carries a seasonal listing state of `inactive` until March 1. The POS blocks the sale and surfaces: *"Live bird sales activate March 1 per Montana ag calendar. Earliest available: 13 days."* The customer is offered a pre-order hold. The early delivery is flagged to the store manager as an inventory discrepancy (live birds received outside active window) — a `procedural_non_compliance` Hawk case auto-created from the receiving event.

---

### Scenario C — Restricted-Use Herbicide, Laramie WY

A rancher asks for Corteva Grazon Next HL for pasture weed control. Wyoming requires a valid pesticide applicator license for restricted-use product sales. He says he has one but doesn't have his card.

**Without the platform:** The associate isn't sure whether Grazon Next HL is restricted-use in Wyoming (it is). She checks a physical restricted-use list posted at the service counter. The list was last updated in 2024. She makes a judgment call and completes the sale without capturing the license number. Six months later, a state EPA audit flags the transaction as a restricted-use sale without applicator license verification. The store receives a notice of violation.

**With the platform:** Associate scans the SKU. Platform responds: *"Restricted-use pesticide. Wyoming requires current pesticide applicator license. License number and expiry required before sale can proceed."* Associate captures license number verbally (platform creates a compliance obligation tied to the transaction pending verification of expiry date). If the rancher can provide the license number, the sale completes with the obligation noted. If not, sale is blocked and a Hawk case is created: `procedural_non_compliance`, status `open`, obligation `verify applicator license within 48 hours or void transaction`. The rancher's license is verified the next day via the state ag database; the obligation is closed and the case resolves. The audit trail is hash-chained.

---

### Scenario D — BOPIS Pickup with Age-Gated Items, College Station TX

A customer has placed a BOPIS order that includes a case of Winchester .308 ammunition and a Traeger grill. The customer who picks up is under 21 (the .308 is handgun-caliber ammunition; Texas follows the federal 21+ age requirement for handgun ammunition).

**Without the platform:** The pick associate bags both items. The counter associate checks the ID at pickup, sees the customer is 19, and is unsure whether the .308 falls under the handgun-ammunition rule. She bags it anyway because "it's for a rifle." The transaction completes. The age gate was bypassed; the event is invisible.

**With the platform:** The BOPIS order is flagged at pick time: *"Order contains age-gated item: Winchester .308 Rem 150gr — federal handgun ammunition classification, 21+ required at pickup."* The pick associate sets the item aside with a flag. At the counter, the ID check triggers the platform's age verification: customer is 19 → item authorization returns `blocked`. Counter associate explains the restriction, removes the item from the order, and issues a partial refund. The blocked pickup event is logged as a `procedural_non_compliance` case (resolved: blocked by regulation) with the customer ID noted (redacted). LP alert is triggered per Q-configured threshold for age-gated BOPIS blocks.

---

## Hawk + Cove as the Solution Surface

### Hawk: From Compliance Binder to Living Case Record

The 63 incident types in Hawk's reference seed map across all ten work cards. The critical design insight is that Murdoch's compliance complexity — firearms, ag chemicals, live animals, BOPIS exceptions, cashier exceptions — is not ten separate problems. It is one problem: *an event occurred that requires a structured record, a compliance obligation, and an institutional knowledge output.* Hawk's wizard-driven intake ensures the right fields are captured for each incident class. The `hawk_compliance_obligations` table tracks every regulatory deadline (Form 4473 retention, license verification due dates, inspection response windows) with machine-enforced status.

The card factory (Hawk's `hawk_cards` table, pgvector-embedded) is where institutional knowledge crystallizes. Every resolved case generates a card. Cards seed the memory bus. The agent's answer to "Can I sell this here?" improves with every case resolved — not because someone updates a binder, but because the knowledge graph grows from live operational events.

| Murdoch's Compliance Problem | Hawk Mechanism |
|---|---|
| Firearms compliance record | `hawk_compliance_obligations` — Form 4473 retention + NICS outcome log |
| Ag chemical license verification | `hawk_compliance_obligations` — applicator license expiry per customer |
| Live animal biosecurity breach | `hawk_cases` — `safety_violation` class, wizard captures species and state |
| Cashier exception investigation | `hawk_cases` — `register_discrepancies` PV track, hash-chained timeline |
| ATF/EPA inspection readiness | `hawk_compliance_export` — hash-verified audit package in one tool call |
| Associate training failures | `procedural_non_compliance` cases → Cove obligation routing |

### Cove: Store as Governed Entity

The Cove governance engine's core model — a governed entity with a document library, a set of obligations, a roster of responsible parties, and a structured communication surface — maps onto the store compliance administration problem without modification. The HOA parcel becomes the retail store. The governing documents (bylaws, CC&Rs) become the SOPs and compliance playbooks. The assessment schedule becomes the training expiry calendar. The board communication thread becomes the district manager review loop.

| Cove HOA Concept | Murdoch's Store Application |
|---|---|
| Parcel / lot | Individual store (1 of 47) |
| Governing documents | Compliance SOPs, state-specific playbooks, firearms binder |
| Assessment obligations | Training certification renewals (pesticide, firearms, OSHA) |
| Violation notice | Hawk case routed to manager + DM when threshold crossed |
| Board communication | District manager review thread, compliance sweep summary |
| Meeting minutes | Inspection outcome records, audit response documentation |
| Vote / resolution | Manager sign-off on daily compliance sweep confirmation |

The Cove integration point is the compliance sweep workflow (WC-10): every morning, the store manager's platform surface is a Cove-governed checklist. Completion is a Cove resolution. Outstanding items are Cove obligations with due dates. The district manager sees a Cove-generated summary across all stores in their territory — not an email inbox.

---

## CATz Alignment Map

These work cards feed two Phase I workstreams and two Phase II workstreams simultaneously.

| CATz Workstream | What These Cards Feed |
|---|---|
| **Phase I WS2 — Field Visits** | WC-01 through WC-10 are the field observation inventory — what an associate in each department actually does, what the compliance friction points are, where the binder gets pulled out |
| **Phase I WS3 — As-Is Workshops (Store Ops domain)** | The workflow steps in each card are the as-is process documentation. The gaps (no structured record, no hash-chained audit trail, institutional knowledge in one person's head) are the diagnostic finding |
| **Phase II WS1 — To-Be Workshops (Store Ops + Technology domains)** | Each card's Automation Posture section is the to-be state — what the agent resolves, what the associate executes, what the platform anchors |
| **Phase II WS4 — IT Architecture (Target state)** | Hawk case management + Cove governance engine + item authorization contract + CRB modules T/S/N/Q/R = the architecture that runs all ten workflows on a single platform |

The Phase I exit gate requires a signed business case. The quantification target for Murdoch's: current cost of manual compliance management (binder maintenance, manager escalation rate, LP investigation time, audit preparation cost, lost sales from over-refusal) versus platform cost. The items in WC-01 (Scenario A — Fort Collins magazine refusal), WC-03 (Scenario B — early chick sale violation), and WC-02 (Scenario C — restricted-use herbicide) are each independently quantifiable as annual cost exposures.

---

## Open Questions for Next Session

1. **BOPIS inventory XHR contract** — highest-priority gap from the crawl. The store-locator dialog inventory query is the last unobserved first-party endpoint. Resolve before building the BOPIS item authorization gate.
2. **Firearms platform: is there an existing agent or POS-integrated tool?** Murdoch's may already have a third-party firearms compliance tool (many Counterpoint-on-firearm chains use Bound Book software). If so, WC-01's To-Be posture is integration/replacement analysis, not greenfield.
3. **Counterpoint VAR identification** — which VAR currently serves Murdoch's determines the channel motion for the pilot proposal.
4. **Laramie pilot scope** — WC-01 (firearms), WC-02 (ag chemicals), and WC-09 (cashier exceptions) are the three highest-ROI workflows for a 90-day Laramie pilot. WC-03 (live animals) adds if the pilot runs March–May.

## Related

- [[Brain/wiki/murdochs-ranch-home-supply-proof-case|Murdoch's Proof Case]]
- [[Brain/wiki/catz-method|CATz Method]]
- [[Brain/process-decomp/CRB-PROCESS-MAP|CRB Process Map]]
- [[docs/sdds/go-handoff/hawk-case-management|Hawk SDD]]
- [[Brain/wiki/canary-mcp-stack-architecture|MCP Stack Architecture]]
