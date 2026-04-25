---
title: Intactix 2006 — Canonical Validation of RetailSpine
type: validation-memo
status: v0.1
tags: [retailspine, intactix, jda, canonical-validation, interface-design, ikb, planogram, assortment, fred-meyer, founder-operator-era]
created: 2026-04-24
updated: 2026-04-24
related:
  - "[[retail-integration-spine]]"
  - "[[Brain/projects/RetailSpine|RetailSpine MOC]]"
  - "[[third-branch]]"
  - "[[academic-frame-1999-hbs]]"
sources:
  - Brain/raw/inbox/Intactix Enterprise Suite 2006.2.0 Integration Guide.pdf  (master, 31pp)
  - Brain/raw/inbox/ASR 2006.1.0_IKB 2006.2.0 Integ Guide.pdf  (24pp)
  - Brain/raw/inbox/IKB 2006.2.0 - PRO 2005.3.0 Integ. Guide.pdf  (17pp)
  - Brain/raw/inbox/MMS 2005.1.0_IKB 2006.2.0 Integ Guide.pdf  (30pp)
  - Brain/raw/inbox/PMM 2005.2.0_IKB 2006.2.0 Integ. Guide.pdf  (44pp)
last-compiled: 2026-04-24
needs-review: 2026-05-08
---

# Intactix 2006 — Canonical Validation of RetailSpine

> **Provenance boundary.** This memo cites founder-operator experience at Fred Meyer / F&E as the validation basis for RetailSpine's canonical shape. That operator lineage is private provenance and **does not** carry forward to CATz or any customer-facing blueprint. Public materials present RetailSpine as the canonical it is — not as the retained shape of any specific prior deployment.

**Governing thesis.** The five JDA Intactix Enterprise Suite 2006.2.0 integration guides are ground truth for the canonical retail-integration nouns that RetailSpine abstracts. Every interface object, field, file, and activity named in the guides maps onto a RetailSpine canonical — and where the map has gaps, the gaps are surgical, not structural. The founder operated inside this suite at Fred Meyer Superstores (Kroger) circa 2003–2005. RetailSpine's architectural posture — an item knowledge base as hub, capability modules as spokes, planogram-capacity-replenishment as a first-class triangle, static-vs-performance as the dimension-vs-fact axis — is not a theoretical reconstruction. It is the retained shape of an enterprise suite the operator deployed, reclaimed vendor-neutral.

This memo validates that claim interface by interface, noun by noun. Where Intactix is richer than current RetailSpine, the memo names the patch. Where RetailSpine is richer than Intactix, the memo names the expansion. Both lists are short.

## Executive summary

The 2006 Intactix suite is a **hub-and-spoke** architecture in which **IKB (Intactix Knowledge Base)** is the item/planogram/store/floorplan object store, and every other module (Space Planning, Floor Planning, EIA, Shelf Assortment, ASR, PRO, MMS, PMM, Space Automation) integrates *to* IKB rather than to each other. This is the same hub-and-spoke shape RetailSpine carries forward, with IKB carried forward *by the same acronym*.

| JDA 2006 module | JDA expansion | RetailSpine canonical |
|---|---|---|
| **IKB** | Intactix Knowledge Base | **IKB — Item Knowledge Base** (already in RetailSpine System Glossary as vendor-neutral; now validated as the *original* naming) |
| **Space Planning** | Planogram authoring (shelf-level) | **GPM — Planogram Management** |
| **Floor Planning** | Store layout / macro planogram | **GPM — Planogram Management** (macro-level) |
| **Space Automation** | Rule-driven planogram generation | *(new RetailSpine surface — GPM-automation sub-capability)* |
| **EIA** | Efficient Item Assortment | **CRDB — Catalog / Range Database** (assortment master) |
| **Shelf Assortment** | Shelf-level assortment | **CRDB + SR** (catalog feeds range execution) |
| **ASR** (Advanced Store Replenishment by E3) | Store-level replenishment engine | **GFO — Forecasting + Allocation + Ordering** (J017 PBS Stock Order + J010 SOH + replenishment parameters) |
| **PRO** (ProSpace) | Replenishment engine (Portfolio Enablement Services variant) | **GFO** (same surface, different vendor lineage — J017 family) |
| **PMM** (Portfolio Merchandise Management) | Merch master + assortment plans + performance feedback | **RMS + CRDB** (merch master + assortment authoring) |
| **MMS** (Merchandise Management System, AS/400) | Legacy merch master on DB2/400 | **RMS — Merchandising System** (C-prefix master data; F012 supplier master) |

**One-line validation:** every module in the Intactix 2006 suite collapses cleanly onto an existing RetailSpine canonical. The suite is the historical realization of the abstract spine, with IKB preserved *by name* and the rest renamed to vendor-neutral canonical roles.

---

## I. The module graph, drawn from the master integration guide

The Intactix Enterprise Suite 2006.2.0 master guide documents sixteen integration chapters. The topology they describe is a hub-and-spoke with bidirectional flows:

```
                                  ┌────────────────────┐
                                  │   PMM (merch +     │
                                  │   assortment plans)│
                                  └─────────┬──────────┘
                                            │
        ┌─────────────────┐                 │                  ┌────────────────┐
        │   MMS (AS/400   │                 │                  │  ASR / PRO     │
        │   legacy merch) │                 │                  │  (replen       │
        └────────┬────────┘                 │                  │   engines)     │
                 │                          │                  └───────┬────────┘
                 │ XML product import       │                          │
                 │ XML location import      │                          │
                 │ Min/Max export           │                          │
                 ▼                          ▼                          ▼
                              ┌────────────────────────┐
                              │                        │
                              │   IKB                  │
                              │   (Intactix            │
                              │   Knowledge Base)      │
                              │                        │
                              │   Products             │
                              │   Planograms           │
                              │   Stores               │
                              │   Floorplans           │
                              │   Performance Data     │
                              │                        │
                              └─────┬──────────────┬───┘
                                    │              │
                     ┌──────────────┼──────────────┼───────────────┐
                     ▼              ▼              ▼               ▼
              ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌─────────────┐
              │  Space     │ │  Floor     │ │  EIA       │ │  Shelf      │
              │  Planning  │ │  Planning  │ │            │ │  Assortment │
              └────────────┘ └────────────┘ └────────────┘ └─────────────┘
                     │              │              │               │
                     └──────────────┴──────┬───────┴───────────────┘
                                           ▼
                                    ┌────────────┐
                                    │   Space    │
                                    │ Automation │
                                    │  (rules)   │
                                    └────────────┘
```

Three characteristics of this topology map directly onto RetailSpine:

1. **IKB is the only canonical hub.** No module integrates to another module's native store. All master-data and performance-data flow through IKB. RetailSpine carries this forward — IDS/IKB in the current catalog are the same pattern under two vendor-neutral names.
2. **Static data and performance data are distinguished at the schema layer.** JDA names them explicitly ("Static Data" vs "Performance Data"). RetailSpine carries this forward as the dimension/fact split in the canonical interface catalog.
3. **Integration is bidirectional by default.** Master data flows into IKB; planogram/floorplan/assortment objects flow back out; replenishment Min/Max flow out to the order engines; sales history flows back in. RetailSpine's C/D/F/J/S prefixes preserve this bidirectionality.

---

## II. Noun inventory — every defined term in the five guides

Below is the canonical noun extraction from the five integration guides. Each row is a term JDA explicitly defined (Terminology sections) or treated as a first-class object (file names, activity names, interface names, field names). The *Canonical map* column names the RetailSpine surface it maps to, or flags *NEW* for surgical gaps.

### II.A — Identifier and hierarchy nouns

| Intactix 2006 noun | JDA definition / usage | Canonical map |
|---|---|---|
| **SKU ID** | "The sellable unit, or stock keeping unit. In IKB, this field is referred to as ID." | RetailSpine **Product ID** (C001 payload) |
| **UPC** | Universal product code, MMS `/CommonProduct/UPC` | RetailSpine **UPC** (C023/C027/C045/C054 PLU family) |
| **Check Digit (ICHECK)** | MMS field, DB2/400 record format | RetailSpine C001 payload leaf |
| **SKU Number (INUMBR)** | MMS field code | Same as Product ID |
| **Store ID / Location ID** | Store master object | RetailSpine **Store** (C012 payload) |
| **Organization (store)** | PMM term — store grouping for org creation/maintenance | RetailSpine **Store Hierarchy** (C012) |
| **Department / Sub-Department / Class / Style** | MMS download hierarchy levels | RetailSpine **Item Hierarchy** (C002/C003) |
| **Section** | Planogram / hierarchy level | RetailSpine C002 (Item Section) |
| **Planogram ID** | Core planogram identifier (addressed in master guide CH 5/6) | RetailSpine **Planogram ID** (S-prefix; S059 mod number) |
| **Modular (Mod) Number** | Alternate planogram identifier ("Valid Mod Number Range") | RetailSpine S059 |
| **Floorplan ID** | Floor Planning identifier | RetailSpine **Floorplan ID** (new leaf under GPM — macro layout) |
| **Object ID** | Generic IKB business-object identifier | RetailSpine canonical object ID across all S-prefix |

### II.B — Dimensional (Static Data) nouns

| Intactix 2006 noun | JDA definition / usage | Canonical map |
|---|---|---|
| **Product Information (Static)** | Dimensions, descriptions, UPCs; "data that does not change or changes infrequently" | RetailSpine C001 / S036 / S058 |
| **Location Information (Static)** | Store numbers, addresses, store attributes | RetailSpine C012 / S035 / S074 / S008 |
| **Address Line** | MMS field family | RetailSpine C012 leaf |
| **Case Depth / Case Height / Case Width / Case Pack / Case Number Deep/High/Wide / Case Total Number** | MMS case-dimension family | RetailSpine **Product Case Dimensions** (C001 leaf family — currently abstract, this names 8 concrete leaves) |
| **Alternate Depth / Alternate Height / Alternate Width / Alternate Max High / Alternate Number Deep/High/Wide / Alternate Total Number** | MMS alt-packaging family | RetailSpine **Product Alt-Pack Dimensions** (C001 leaf family — validates the need for a dual dimension set) |
| **Volume Unit of Measure (IXUOM)** | Volume UoM code | RetailSpine **UoM** (C001 leaf) |
| **Activity Master** | MMS activity-name registry ("STR_MSTUPD — STORE MASTER UPDATE") | RetailSpine — *NEW surface*: "Activity Master" as a first-class audit/ops dimension is not currently explicit in RetailSpine; it's the DB2/400 analog of change-data-capture event naming |

### II.C — Factual (Performance Data) nouns

| Intactix 2006 noun | JDA definition / usage | Canonical map |
|---|---|---|
| **Unit Sales** | Performance measure — "Space Planning and IKB performance measures include Unit Sales, Retail Price, and Unit or Case Cost" | RetailSpine **Sales from Till** (J004) — summarized to SKU-store-time |
| **Unit Movement** | PMM synonym for Unit Sales History | Same — J004 aggregated |
| **Retail Price** | Price-at-sale, performance-level | RetailSpine **C010** — price master that feeds J004 sales attribution |
| **Unit Cost / Case Cost** | Unit and case cost of goods, performance-level | RetailSpine **C010** cost leaf (same interface carries cost) |
| **Sales History (by time frame)** | PMM retrieves and summarizes for specified time range | RetailSpine J035 (actual sales feedback) |
| **Capacity** | "Field stored at various levels in IKB to indicate the number of merchandised units for each product. At the Performance level, the field indicates the total number of units of a product on a specified planogram." | RetailSpine **S075 Capacity Information** — *exact direct match by noun and by semantics* |
| **Backroom Stock** | Formula input for Replenishment Max | RetailSpine — *NEW leaf under J010 SOH* (currently J010 is single-valued; this validates the need to distinguish front-of-store vs back-of-store) |
| **Presentation Minimum (IPRES)** | "Minimum shelf quantity for presentation purposes if demand forecast is too low to protect presentation requirements" | RetailSpine **Planogram Presentation Min** — *NEW leaf*; intersects S075 capacity with J017 replenishment |
| **Buyer Max (IPMAXI)** | "Soft OUTL maximum, as long as service is not jeopardized — limits the SKU cycle within source line" | RetailSpine **Replenishment Ceiling** — *NEW leaf under J017*; distinct from Replenishment Max |
| **Replenishment Min (formula)** | Formula: Horizontal facings · H×V facings · % of Capacity · case/tray multiple | RetailSpine **Replenishment Min** (J017 parameter) |
| **Replenishment Max (formula)** | Formula: Capacity · Capacity + Backroom Stock · Capacity × safety factor | RetailSpine **Replenishment Max** (J017 parameter) |

### II.D — Object-lifecycle nouns (NEW RetailSpine surface)

This cluster names semantics RetailSpine does not currently codify as first-class.

| Intactix 2006 noun | JDA definition / usage | Canonical map |
|---|---|---|
| **Object Versioning** | "Within IKB, all business objects (products, planograms, floorplans, stores) can have multiple versions that move through an object life cycle" | RetailSpine — **NEW**: first-class temporal-versioning surface |
| **Live** | Current authoritative version of any business object | NEW — object status value |
| **Pending** | Future authoritative version ("will replace the Live version at a future date") | NEW — object status value |
| **Historic** | Prior authoritative version (former Live after a Pending promotion) | NEW — object status value |
| **Allow Live Planogram Updates / Allow Live Store Updates** | Config flag controlling whether Add on an existing Live record overwrites or creates Pending | NEW — object-lifecycle policy |
| **Authority Level** | Planogram / floorplan authorization field (CH 13 "Saving Shelf Assortment projects" + CH 15 "EIA / Shelf Assortment / IKB Integration") | RetailSpine — **NEW**: planogram provenance / authorization lineage surface |

**Implication for RetailSpine.** The abstract canonical catalog has no explicit object-status state machine. JDA did in 2006. This is a straightforward expansion of RetailSpine to include a *versioning sub-surface* — every canonical object gets `status ∈ {Live, Pending, Historic}` plus a promotion/demotion rule set. This is the surgical patch the validation exposes.

### II.E — Integration-file and interface nouns

| Intactix 2006 noun | JDA definition / usage | Canonical map |
|---|---|---|
| **XML Product Import Interface** | MMS → IKB product data path | RetailSpine C001 realization |
| **XML Location Import Interface** | MMS → IKB store data path | RetailSpine C012 realization |
| **PMM Direct Product Import Interface** | PMM → IKB product path | Same as C001 via PMM |
| **PMM Direct Location Import Interface** | PMM → IKB store path | Same as C012 via PMM |
| **PMM Min/Max Export Interface** | IKB → PMM replenishment parameters | RetailSpine J017 parameters |
| **PMM Performance Update Interface** | PMM → IKB performance refresh | RetailSpine J035 |
| **PMM Assortment Export Interface** | IKB → PMM: "gather information for all listed objects that have a Live status" | RetailSpine — validates that assortment-export is a first-class S-prefix leaf (S047/S057 family) |
| **E3SXIKB file** | ASR ↔ IKB FTP exchange payload (Min/Max/Start Date/End Date) | RetailSpine J017 transport |
| **E3SITM / E3SHSTA / E3SWHSE** | ASR DB files: items, history, warehouse | RetailSpine J052/J057/J100 analog |
| **E3INFLST / E3INXFR** | ASR inbound control and transfer files | RetailSpine — interface control plane; matches the pattern of J023 (ASN) + J076 (supply authority) |
| **Portfolio Enablement Services database tables** | PRO's IKB-facing data plane | RetailSpine canonical data-plane abstraction |
| **Data Manager** | "IKB component that allows users to view and modify data for objects stored in the Intactix database" | RetailSpine — operator layer for IKB/CRDB (analogous to RMS Foundation Data Mgmt) |
| **Intactix Console** | "IKB component that allows users to configure the Intactix database and the interfaces between IKB and external applications" | RetailSpine — *admin plane* (the Console is the meta-interface over the interface catalog) |

### II.F — Planogram-authoring nouns (GPM deepening)

| Intactix 2006 noun | JDA definition / usage | Canonical map |
|---|---|---|
| **Horizontal facings / Vertical facings** | Formula inputs for Replenishment Min | RetailSpine — *NEW leaves under S075*: planogram facing geometry |
| **Performance object** | IKB object type capturing Unit Sales + Retail Price + Unit/Case Cost at planogram level | RetailSpine canonical **Planogram Performance Object** (new surface: facts bound to the planogram dimension, not the store-product-time dimension) |
| **Assortment Plan** | PMM-owned plan object | RetailSpine CRDB object |
| **Assortment Format** | PMM clustering object (similar stores grouped by format) | RetailSpine — intersects C012 (Store Format) with CRDB |
| **Assortment Changes view** | Space Planning view on EIA assortment diffs (CH 12 / CH 13) | RetailSpine — *NEW surface*: diff-as-view over CRDB objects |
| **Current Assortment / Do Not Save Planogram / Assortment Action** | Space Planning assortment-change vocabulary | NEW — decision-action leaves under CRDB |
| **Cluster (store cluster, product cluster)** | EIA clustering primitives | RetailSpine **Channel Clustering** (C012 derived) / **Product Cluster** (CRDB derived) |
| **Business Rule Validation** | Space Automation CH 16 — rule engine for planogram compliance | RetailSpine — **NEW surface**: rule engine bound to S-prefix with validation outcomes as facts |

### II.G — Integration-control nouns (the operator plane)

| Intactix 2006 noun | JDA definition / usage | Canonical map |
|---|---|---|
| **BATCH** / **Batch file** | Batch execution path | RetailSpine — interface-control plane |
| **ExportTo / ExportType / ExecuteApplication** | INI file directives | RetailSpine — interface metadata (manifest) |
| **OverwriteDeleteErrors / OverwritePreviousExport** | Error-handling policy flags | RetailSpine — interface-level SLO policy |
| **ErrorFile / ErrorPrefix** | Error logging config | RetailSpine — observability layer on the interface |
| **INIFile** | INI config pointer | RetailSpine — manifest binding |
| **Interface (the configured binding)** | Intactix-Console-registered binding between IKB and an external system | RetailSpine **Interface** canonical — exactly the sense this article catalogs |

---

## III. What JDA had that RetailSpine should now codify

Three surgical patches to RetailSpine fall out of the validation:

**1. Object Versioning as a first-class temporal surface.**
Every canonical object in RetailSpine (Product, Store, Planogram, Floorplan, Assortment Plan, Assortment Format) should carry `status ∈ {Live, Pending, Historic}`, a `valid_from` / `valid_to` pair, and a per-object-type policy for promotion and demotion. JDA's "Allow Live Updates" vs "Allow Live Updates Restricted" branching is the simplest statement of that policy; it should be preserved as-is in RetailSpine canonical semantics.

**2. Authority Level as a provenance / authorization surface.**
Planograms and floorplans in IKB carry an Authority Level field distinguishing who can modify an object at what stage. This is not currently represented in RetailSpine. The 2026 analog is clean: Authority Level collapses into a capability grant ("which agent or human role is authorized to mutate this object in which lifecycle state?"). This is the bridge between RetailSpine canonicals and the agent-operator layer of the Third Branch.

**3. Business Rule Validation (Space Automation) as a fact-generating process.**
JDA's Space Automation evaluates business rules against planograms and emits validation outcomes. These outcomes are themselves facts — they should be addressable as S-prefix observables. RetailSpine can codify this as a canonical "rule-outcome" leaf under GPM with deterministic, machine-parseable payloads.

**4. The Ordering Gate — planogram assignment as a precondition for item activation.**
This is the one canonical rule JDA 2006 *enabled* but did not *enforce*, and the one F&E's SRD implementation *did* enforce — and it is the rule that closes the substrate loop. At Fresh & Easy, no item could be enrolled as orderable in the Oracle Retail item master until it had (a) a location-level planogram assignment, (b) a known shelf capacity, and (c) a known pack configuration. The ordering activation flag was derived, not asserted: it flipped only when the S-prefix record for a given Product × Store had a valid Capacity and a valid Planogram ID, and the C001 Product master had a pack configuration that reconciled to the shelf geometry. This inverted the industry-default sequence (buy first, shelve later) and forced merchandising upstream into packaging specifications with the vendor — the supply chain bending to the shelf rather than the shelf bending to the supply chain. RetailSpine should codify this as a canonical derived attribute: **`Product.orderable_at_location[store_id]` = Boolean, derived from `Planogram(product_id, store_id) != null AND Capacity(product_id, store_id) > 0 AND Product.pack_config reconciles shelf geometry`.** This is the operator-side closure of the canonical — and it is the discipline that made F&E's store-of-the-future labor economics work.

**5. The Shelf-Edge Label Compile Gate — label-compilability as the exit symmetric of the ordering gate.**
The same F&E discipline that used planogram assignment as the *entry* gate for items used the shelf-edge label as the *exit* reconciliation. An item cannot hang on a rail without a label; a label cannot compile without planogram + capacity + pack + price + description + UoM + range status reconciling for that product × store. The SRD interfaces `S039` (daily batch — SEL Range and Display, author Prasanth Dukaram, 22 May 2007 v1.2) and `S101` (near-real-time emergency facings, author Andy Barker, 14 Sep 2007 v0.2) implemented this as a two-latency reconciliation event landing in IDS table `SKUItemInStore` with a reason enum `SRDSEL_Trans.UpdateType ∈ {FULL, RANGE, FACINGS, EMERGENCY}`. Physical label delivery was the Sysrepublic product **CRDM** — which is the first engagement point in the decade-plus Sysrepublic relationship that later produced the xBR / Secure-era LP platforms. RetailSpine should codify three additions from this analysis: (a) `Product.label_compilable[store_id]` as a derived Boolean symmetric to `orderable_at_location`, (b) the `{FULL, RANGE, FACINGS, EMERGENCY}` enum as the canonical SEL Reconciliation Reason set, and (c) `latency ∈ {batch, real-time}` as a canonical property of reconciliation events. See `[[srd-shelf-edge-label]]` for the end-to-end data path and the IDS schema. Noting also that S039 v1.2 specifies *"This interface is for US and Turkey implementation"* — dual-national portability was a design property of the canonical at the interface-spec layer, not a post-hoc port.

Each patch is small. Together they bring RetailSpine from static canonical model to lifecycle-aware, ordering-gate-entering, label-compiling canonical model — which is what the agent layer needs, and what the Third Branch substrate loop requires to actually close.

---

## IV. What RetailSpine has that Intactix 2006 did not

Two load-bearing expansions RetailSpine inherits from the post-Intactix era:

**1. Explicit Customer domain.**
JDA 2006 does not have a Customer master. The suite is entirely product/store/planogram/assortment/replenishment. RetailSpine's C-prefix (Commercial) and the reverse crosswalk to RBIS BSTs carry a first-class Customer Management domain (Purchase Profiles, Customer Profiles, RFQ, Cross Purchase Behavior, Market Basket, LTV, Attrition, Loyalty). This is the post-2006 substrate arriving — the same substrate that failed Branch C in 1999 now being integrated into the full spine.

**2. Explicit Loss Prevention as a Store Operations BST fed by D-prefix events.**
JDA's ASR and PMM know about shrink only through Min/Max-and-SOH reconciliation. RetailSpine makes **LP** a first-class BST fed by D019/D020/D033 (inventory adjustments), D021/D022/D029 (stock takes), J010 (SOH baseline), and J004 (cashier-attributed transactions). This is the commercial wedge of the Third Branch — the LP department reading the same D-prefix events Intactix treated as quiet reconciliation traffic, now being read as a first-class loss-attribution stream.

The JDA suite ended at the shelf. RetailSpine runs past the shelf into the customer and into the shrink attribution layer. That is the post-1999-substrate expansion, consistent with the Third Branch thesis.

**3. The F&E operational closure — the ordering gate as enforced canonical rule.**
The deepest post-Intactix expansion is operator-side, not model-side. At Fresh & Easy the same JDA canonical was deployed against Oracle Retail as the system-of-record item master, and the SRD (Space, Range & Display) layer was built as the *enforcement* plane over that canonical. The rule JDA 2006 enabled — *an item has a location, a capacity, and a pack before it has a purchase order* — was made a hard gate at F&E. This turned planogram discipline into supply-chain discipline, which turned pack configuration into a vendor negotiation, which minimized store labor to the point where the substrate paid for itself on operating cost alone, independent of the customer-side value the BroadVision-era promised but couldn't deliver. RetailSpine inherits this gate as canonical semantics (see III.4); any merchant-facing agent in GrowDirect that touches procurement should honor the gate as a precondition, not a suggestion. This is the operator discipline the Third Branch recovers alongside the observation substrate.

**4. The specification canonical — TTL as the third leg of the F&E operating model.**
JDA 2006 is entirely product/store/planogram/assortment/replenishment. It does not carry a specification or regulatory object. At Fresh & Easy that gap was filled by a **third canonical** — the **Tesco Technical Library** (TTL), a US clone of RedSky IT's Creations platform, authored at F&E by the founder as the originating Functional Specification V1.0 (18 July 2006, ~10 months before the S-prefix interface specs were drafted). TTL owns the lifecycle object *Specification* — with supplier-authored recipe, nutrition calculation, US allergen matrix, US compound-ingredient nesting, and pack-copy compile — and it kill-switches against RMS / Oracle Retail exactly the way SRD does on the planogram side: TTL generates TPNB and UPC during pre-RMS interim, then yields number generation to RMS once the merchandising master is in production. This makes the F&E operating model a **three-canonical** stack: *who the product is* (RMS), *where the product is* (SRD), *what the product is* (TTL). All three compile at one physical target — the shelf-edge label. RetailSpine currently codifies the first two (C-prefix + S-prefix). The third — a C090 Product Specification family with C091 Lifecycle, C092 Recipe, C093 Nutrition, C094 Allergen Matrix, C095 Pack Copy, C096 Finished Product Standards, C097 Storage & Packaging — is the v0.7 patch the private-label / fresh-prep slice of retail requires. See `[[tesco-technical-library]]` for the full canonical proposal and the founder-operator provenance. This is the load-bearing expansion for the Canary fresh-prep module: every SMB grocer running a deli, bakery, salad bar, or prepared-foods counter has the same regulatory footprint the TTL was built to discharge, and the 2006 spec is the authored-once ancestor of the 2026 agent-authored instantiation.

---

## V. Implications

**A. The RetailSpine thesis is not invented — it is reclaimed.** The entity model, the hub-and-spoke shape, the static/performance distinction, the Min/Max formula family, the planogram-capacity triangle, and the IKB naming are all directly inherited from a 2006 enterprise suite the founder operated. This is defensible against any CIO who deployed JDA, Retek, or an equivalent 2000s-era space-and-replenishment stack — which is most Tier-1 retailers.

**B. RetailSpine gets three surgical patches for agent-era fitness.** Object Versioning (Live/Pending/Historic), Authority Level (provenance + authorization), and Business Rule Validation (rule outcomes as observable facts) are the three first-class surfaces the agent layer needs that the abstract canonical model currently treats as implicit. The patches are small and each one is directly named by JDA.

**C. The Intactix guides are the training corpus for agent-facing interface documentation.** The five guides are, in aggregate, a complete specification of how a 2006 enterprise retail suite exposed its surface to integrators. That shape is exactly what the agent layer needs to consume. Future RetailSpine interface docs should lift the guides' structural conventions (Terminology · Integration Overview · Installation · Chapter-per-module-pair integration · Object Versioning table · Interface control objects) as the format agents read.

**D. The LP wedge is validated at the interface layer.** Every D-prefix interface JDA treated as replenishment plumbing is, from LP's budget line, a shrink-detection observable. RetailSpine's decision to make LP a first-class BST over D019/D020/D021/D022/D033/J010 is consistent with JDA's data model but commercially orthogonal to how JDA sold the suite. That commercial orthogonality is the Third Branch commercial motion.

**E. SRD meets MCP is where the loop closes.** The SRD canonical has always been a grammar operators could read. What it has never been is a grammar *agents* could read. Model Context Protocol is the first interface protocol in which the 30 S-prefix interfaces, the object-versioning state machine, the Authority Level provenance, the Business Rule Validation outcome facts, and — critically — the ordering gate itself can be exposed as typed, discoverable, callable surfaces that an agent honors by construction. Every S-prefix record becomes an MCP resource; every F-prefix movement event becomes an MCP event stream; every J-prefix replenishment parameter becomes an MCP tool; the ordering gate becomes an MCP-enforced precondition that no procurement agent can bypass. The canonical *was* the discipline; MCP makes the discipline native to the operator layer. This is the specific architectural claim the Third Branch reduces to: **the SRD grammar, exposed over MCP, is the substrate that BroadVision tried to build, that Auto-ID tried to instantiate, and that JDA + F&E operated one slice of.** When SRD meets MCP the loop closes for the first time since 1999.

---

## VI. Next steps

1. Promote the five PDFs to proper raw intakes in `Brain/raw/inbox/` with frontmatter per the intake protocol (the files are currently still under `uploads/`).
2. Patch RetailSpine v0.6 to include Object Versioning, Authority Level, and Business Rule Validation as first-class canonical surfaces (one section per patch).
3. Add an explicit "Case dimension family" and "Alt-pack dimension family" sub-spec to C001 product master, lifting the eight JDA leaves as the canonical leaf set.
4. Add Backroom Stock as a distinct leaf under J010 SOH (front-of-store vs back-of-store).
5. Add Presentation Minimum as a leaf under S075 capacity, bridged to J017 replenishment.
6. Document the "Live Updates Allowed" vs "Live Updates Restricted" policy as the default object-lifecycle policy set.

---

*Source: five JDA Intactix Enterprise Suite 2006.2.0 integration guides (master + ASR/IKB, IKB/PRO, MMS/IKB, PMM/IKB), 146 pages total, extracted via `pdftotext -layout` on 2026-04-24. Companion: `[[retail-integration-spine]]` (the canonical catalog being validated) and `[[third-branch]]` (the thesis these canonicals serve). Operator-era: founder deployment of JDA Intactix at Fred Meyer Superstores, ~2003–2005.*
