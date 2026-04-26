---
title: Tesco Technical Library — The Third Canonical Layer at F&E
type: validation-memo
status: v0.1
tags: [ttl, creations, redsky-it, fresh-and-easy, tesco-us, private-label, product-specification, nutrition-facts, allergen, pack-copy, tpnb, upc, canonical-validation, third-canonical-layer, canary, smb-grocer, founder-operator-era, founder-authored]
created: 2026-04-24
updated: 2026-04-24
related:
  - "[[third-branch]]"
  - "[[intactix-canonical-validation]]"
  - "[[srd-shelf-edge-label]]"
  - "[[retail-integration-spine]]"
  - "[[Brain/projects/Canary|Canary MOC]]"
sources:
  - Brain/raw/inbox/tesco-technical-library-corpus.md  (the raw intake for this article)
  - Brain/raw/inbox/Technical Library/TTL_Functional_Spec_V1.2.doc  (founder-authored, V1.0 18 July 2006, V1.2 19 July 2006)
  - Brain/raw/inbox/Technical Library/Tesco US Proposal V1.0.doc  (RedSky IT, 3 August 2006)
  - Brain/raw/inbox/Technical Library/Tesco CR TTL043 Tesco US Enhancements v1.1.doc  (11 October 2006)
  - Brain/raw/inbox/Technical Library/Service Definition - Tesco US.doc
last-compiled: 2026-04-24
needs-review: 2026-05-08
---

# Tesco Technical Library — The Third Canonical Layer at F&E

> **Provenance boundary.** This article carries founder-operator lineage from
> Fresh & Easy (2006–2007) — specifically the founder's authorship of the US
> Technical Library functional specification on 18 July 2006, predating the
> SRD interface specs by ~10 months. That lineage is private provenance. It
> **does not** carry forward to CATz or any customer-facing blueprint. Public
> artifacts present the third-canonical-layer claim on its engineering merits.

**Governing thesis.** Private-label fresh-prep retail does not run on two
canonicals (merchandising + planogram). It runs on **three**. The third is
the **specification canonical** — the lifecycle-aware, supplier-collaborative,
regulator-facing object that owns ingredient recipe, nutrition calculation,
allergen matrix, and the compile of pack-copy text. At Fresh & Easy this was
instantiated as the **Tesco Technical Library** (TTL) — the US clone of the
UK RedSky IT Creations platform, authored by the founder on 18 July 2006 and
approved by the F&E Regulatory Lead (Breda Mitchell), Commercial Lead
(Charlotte Maxwell), Technical Manager (Helen Mottram), and IT Director
(Doug Rutledge). Without this third canonical, the shelf-edge label cannot
compile for private-label product, and the supply chain cannot regulate
itself to packaging discipline. RetailSpine's current catalog does not yet
carry this surface explicitly. This memo argues it must.

## Executive summary

| Canonical layer | Master of record at F&E | RetailSpine family | What it owns |
|---|---|---|---|
| **Merchandising** | RMS / Oracle Retail | C-prefix (product master, price, range status) | *Who* the product is |
| **Planogram / Range / Display** | SRD (Space, Range & Display) | S-prefix (planogram ID, capacity, facings, reason codes) | *Where* the product is |
| **Specification / Regulatory** | **TTL / RedSky Creations** | *Not yet canonical in RetailSpine — proposed C090 family* | *What* the product is |

The three canonicals compile at one physical target: the **shelf-edge label**
(see `[[srd-shelf-edge-label]]`). Merchandising supplies identity, price, and
range. Planogram supplies location, capacity, and facings. Specification
supplies Statement of Identity, Nutrition Facts, ingredient declaration (with
US compound-nesting rules), allergen statements, pack copy, and date-code
text. Omit any one and the rail tag cannot legally print.

## I. Why a third canonical is load-bearing

The merchandising master and the planogram master are sufficient for
**branded** product — where the manufacturer owns the specification, the
label is fixed at the factory, and the retailer consumes the UPC as a
pointer into a data pool it does not author. Private-label inverts this:
the retailer is the legal manufacturer, the spec is authored collaboratively
with the supplier, and the printed label is a compile target that must
reconcile legal identity, nutrition math, allergen declarations, and pack
copy every time the recipe, pack configuration, or regulatory rule changes.

TTL's functional spec (V1.0, 18 July 2006, author G. Lyle) names the
requirements directly:

- *"Suppliers are required to create all product specification data, there is
  no data entry requirement on the part of the commercial team."*
- *"TTL must be modified to generate a TPNB for each product size ... when
  the product specification status changes from collaboration draft to pack
  copy sent."*
- *"The Number generation functionality will need to be turned off when Tesco
  goes into production with RMS in the US."*
- *"The Recipe calculation module must be modified to support US regulations
  and measures."*
- *"The nutrition label must be modified to meet US regulations."*

Three properties of the specification canonical are named in those
requirements:

1. **It is supplier-authored** (not commercial-team-authored). The third
   canonical brings the vendor inside the retailer's data plane as a
   co-author, not just a counter-party.

2. **It has a lifecycle state machine** whose transitions trigger
   identifier generation. `{supplier-draft, collaborative-draft,
   pack-copy-sent, approved, live}` is the state set; *pack-copy-sent* is
   the transition that requests a TPNB and a UPC from the master-of-record
   (TTL in the interim, RMS once in production). This is the same
   lifecycle discipline JDA Intactix encoded as
   `{Live, Pending, Historic}` for planogram objects (see
   `[[intactix-canonical-validation]] §II.D`). The specification canonical
   needs its own.

3. **It has a kill-switch posture against the master of record.** TTL
   generates numbers only until RMS is in production; after that, numbers
   come *from* RMS. The third canonical is deliberately subordinate when
   the merchandising master is online — an inversion of authority the
   planogram master also respects (see the SRD ordering gate,
   `[[intactix-canonical-validation]] §III.4`).

## II. What the specification canonical contains

### Product header (identifier and hierarchy)

- Product Number (TPNB) — Tesco internal identifier
- UPC — 8 or 13 digits, with check-digit validation (added in TTL043)
- Product Name / **Fanciful Name** / **Descriptive Name** /
  **Statement of Identity** — four distinct fields with different legal
  roles. TTL043 (11 Oct 2006) clarified that "Fanciful Name" at the header
  and "Fanciful Name / Descriptive Name" at pack-copy are separately
  editable, and "Statement of Identity" is independently editable at pack
  copy vs supplier details
- Size (per declared quantity), Category, Sub Group
- Buying Manager, Technical Manager (responsibility assignment)
- Versioning — multiple iterations of a single food spec can coexist

### Recipe and nutrition

- Compound recipe management in both metric and imperial units of measure
- Ingredient supplier tracking (each ingredient in the recipe ties back to
  its own supplier)
- Automatic ingredient-list assembly with **US compound-nesting notation**:
  - Tier 1: `( )` round brackets — *Beef Stew (Beef, Water, Potato, Salt, MSG)*
  - Tier 2: `[ ( ) ]` — *Beef Stew [Beef, Vegetable Stock (Water, Potato, Flavouring), salt, MSG]*
  - Tier 3: `{ [ ( ) ] }` — full nesting
  - No emboldening; terminal full stop
- US Nutrition Facts panel:
  - Servings Per Container allows text (e.g. "Approx 10"), not numeric-only
  - Serving Size Text / Serving Quantity / Servings Per Container as
    stacked layout
  - RDA validation disabled (UK rule that warns at <1/6 RDA does not apply
    in US)
  - Nutrient indent as constituent (configurable variable for indent size)
  - GDA rename to "2500 kcal diet" / "2000 kcal diet"

### Allergen matrix

US-reduced from the UK set to **8 retained statements**:

- 6 existing: Milk, Wheat, Egg, Fish, Shellfish, Soy
- 2 added: Tree Nuts, Peanuts

With **sub-type drop-downs** (Tree Nuts → nut types; Fish → fish types;
Shellfish → shellfish types) and a **cross-contact statement** —
*"This product is made in a factory that processes ..."* — driven by a
multi-select of the 8 major US allergens.

### Pack copy

Pack copy is the **compiled output** of the specification canonical that
feeds the label printer. Pack-copy-level fields are editable **separately**
from header-level equivalents (a post-launch TTL043 change):

- Fanciful Name / Descriptive Name — editable at pack copy, independent
  of header
- Statement of Identity — editable at pack copy, independent of supplier
  details
- Marketing Romance Copy — 3-line display field
- Brand Guidelines — US-tuned variant of UK original
- Ingredient Information — with compound nesting
- **Allergen Information as sub-section under Ingredient Information**
  (structural US requirement)
- Raw meat & poultry statement (added for US)
- Date code text
- *"This product is made in a factory that processes ..."* pulled from
  the allergen matrix selections via TTL043 Mod 20

### Product storage and packaging

- Storage: Date Code and Delivery Destination, Minimum Shelf Life
  (Short Life Product < 30 days), Minimum Life in Tesco DC or Store
- Packaging: Primary/Transit radio, component weights mandatory,
  pallet math using US standard **Tie** (crates per layer) and **Hi**
  (layers per pallet)
- Finished Product Standards: Quantitative Micro standards, Maximum
  value, Report-to-Tesco flag, Method column

## III. How the three canonicals compile

The shelf-edge label is the compile target. The two-latency reconciliation
in SRD (`S039` daily batch + `S101` near-real-time emergency facings)
carries the *planogram* inputs. The RMS feed carries the *merchandising*
inputs. The TTL pack-copy feed carries the *specification* inputs.

```
                   THE PRIVATE-LABEL LABEL COMPILE
                 ───────────────────────────────────

   TTL (Creations / spec canonical)
       │
       │  Pack Copy export:
       │    · Statement of Identity
       │    · Ingredient list (compound-nested)
       │    · Nutrition Facts (US format)
       │    · Allergen statements + factory-processes clause
       │    · Marketing Romance Copy
       │    · Date code text
       ▼
   ┌──────────────────────────────────────┐
   │                                      │
   │   PACK-COPY MASTER                   │
   │   (compiled artifact per TPNB)       │◀──── RMS / Oracle Retail
   │                                      │      · UPC
   │                                      │      · Retail price
   │                                      │      · Range status
   │                                      │      · Product description
   │                                      │
   └────────────────┬─────────────────────┘
                    │
                    │                       ◀──── SRD / IDS / Storeline
                    │                              · Planogram ID
                    │                              · Capacity, Facings
                    │                              · Range / Display reason
                    │                              · RPP overrides
                    ▼
            ┌───────────────┐
            │  Storeline    │
            │    ↓          │
            │   CRDM        │─── SEL printer ─── rail tag
            │  (Sysrepublic)│
            └───────────────┘
```

**Three masters, one compile.** Each is kill-switched against the others
(TTL yields to RMS for numbers; SRD yields to RMS for item enrollment; RMS
yields to SRD for ordering activation). The shelf-edge label is the only
physical artifact that reconciles all three — and that is why, at F&E, the
label was the physical test the full canonical stack had to pass every
night before store open.

## IV. What RetailSpine is missing

RetailSpine v0.5 has C-prefix master data (C001 Product, C010 Price, etc.)
and S-prefix planogram data. It does not have an explicit **specification
canonical** surface. The current assumption is that C001 Product carries
enough attribute structure to cover regulatory needs. TTL disproves this
for private-label fresh-prep:

- **A specification is a collaborative object, not a static record.** It
  has a versioning history, a supplier-side authoring plane, a commercial-
  and technical- and regulatory-review plane, a pack-copy compile
  artifact, and a kill-switch transition to the master of record. A flat
  C001 leaf set cannot carry this shape.

- **A specification has a recipe sub-object.** Recipe is its own typed
  object with ingredients (each tied to an ingredient supplier), compound
  structure (supporting 1–3+ tiers of nesting), and metric/imperial
  calculation — none of which RetailSpine currently codifies.

- **A specification has a nutrition sub-object.** Nutrition is its own
  typed object with serving-size semantics, nutrient config, RDA handling
  (US/UK-switchable), and indent behavior — again, not in RetailSpine.

- **A specification has an allergen sub-object.** Allergen is an 8-row
  retained set (US) plus sub-type drop-downs plus a cross-contact clause.
  The cross-contact clause has a multi-select provenance rule: the values
  that appear in the pack copy are pulled directly from the allergen
  matrix selections (TTL043 Mod 20). This is typed provenance across the
  spec canonical into the pack-copy compile.

### Proposed RetailSpine v0.7 addition

A new **C090 Product Specification** family under the C-prefix, with
canonical sub-surfaces:

- **C091 Specification Lifecycle** — state machine
  `{supplier-draft, collaborative-draft, pack-copy-sent, approved, live,
  superseded}`, transitions, and the identifier-generation hook
- **C092 Recipe** — ingredient tree (tier 1–3 compound structure),
  metric/imperial UoM, ingredient-supplier pointer, regulator-flagged
  ingredients
- **C093 Nutrition** — serving-size text, serving quantity, servings
  per container (text-tolerant), nutrient configuration (with RDA
  handling switch), nutrient indent-as-constituent
- **C094 Allergen Matrix** — 8 retained allergens (US set), sub-type
  drop-downs, cross-contact multi-select, provenance rule into pack
  copy
- **C095 Pack Copy** — compiled artifact, editable at compile level
  (independent of header-level equivalents for the fields named in
  TTL043 §2), with strict provenance back to C091 + C092 + C093 + C094
- **C096 Finished Product Standards** — Quantitative Micro, Method,
  Report-to-retailer flag
- **C097 Storage & Packaging** — Tie/Hi, short-life flag (<30 days),
  storage temperature range, primary/transit

Each sub-surface is a first-class object with versioning, authority-level
(analogous to JDA's planogram Authority Level —
see `[[intactix-canonical-validation]] §II.D`), and a kill-switch rule
against C001 once the merchandising master is of record.

## V. Why Canary should care

Canary's ICP today is Square-tier SMB grocery. The largest missed category
in SMB grocery is **fresh-prep / private-label** — deli, bakery, salad bar,
sandwich station, hot food bar, prepared-foods counter. Every one of those
categories carries the full regulatory footprint TTL was built to discharge.
Most small grocers discharge them by hand: printed binders of SOPs,
pre-formatted spec templates, laminated allergen cards at the case, and a
manager's memory for the last recipe change.

The third canonical is the capability wedge nobody has packaged for SMB.
A Canary-era specification canonical — agent-authored from a recipe entry,
auto-compiling nutrition and allergen matrix, emitting pack-copy-ready
text into the POS and into a printer — is the exact ambient-spec surface
that lets a neighborhood grocer:

1. **Add a recipe to the deli counter and instantly get the Nutrition
   Facts panel, ingredient list with US compound nesting, and allergen
   statement.** Today this is a three-day exercise with a lab or a
   spreadsheet.

2. **Close cross-contact risk.** The factory-processes clause is where
   most SMB fresh-prep programs fail compliance — they either omit it
   or over-declare it. An agent-authored specification canonical closes
   both failure modes by construction.

3. **Shelf-edge label at SMB tier.** Today, private-label-at-scale retailers
   use CRDM or its descendants. SMB retailers use laser printers and
   clipboards. A specification canonical that compiles to a pack-copy
   output — even if the "printer" is a QR code on a label strip — brings
   the discipline of the three-canonical stack to the Canary ICP without
   demanding enterprise print infrastructure.

4. **LP wedge relevance.** Fresh-prep shrink is the highest-margin,
   highest-waste category in most SMB grocers and is invisible in most
   POS journal analysis because the items are scale-priced, in-house
   coded, and often recorded under generic departmental PLUs. A
   specification canonical is the only surface on which *"what is this
   product"* can be asserted rigorously enough to attribute fresh-prep
   shrink at item level.

**Bluntly: TTL is the Canary fresh-prep module waiting to be rebuilt on
2026 substrate.** The spec exists. The lifecycle is known. The US
regulatory rules are the same. The only thing missing is the agent layer
to do the authoring the supplier was required to do in 2006.

## VI. Founder operator-era context

The founder is the named author of the TTL Functional Specification V1.0
(18 July 2006) and V1.2 (edits accepted from Helen Mottram, 19 July 2006).
Approvers: Breda Mitchell (Regulatory Lead), Charlotte Maxwell (Commercial
Lead), Helen Mottram (Technical Manager), Doug Rutledge (IT Director);
Document Owner: John O'Brien; follow-up contact Debra K.W. Topham
(Product Information Manager, Tesco US, El Segundo CA).

**This predates the SRD interface specs by ~10 months.** S039 v1.2 is
dated 22 May 2007. S101 v0.2 is dated 14 Sep 2007. The founder's F&E role
began in senior solution/product capacity in mid-2006, authoring the
regulatory and specification backbone before the planogram-execution
interface layer was drafted. The sequencing matters: at F&E, the
specification canonical was built *first*, the planogram-execution
canonical *second*, and both were built against an RMS / Oracle Retail
master that was still coming online through 2007–2008.

The RedSky IT relationship (UK, Nottingham; US operation in South
Plainfield, NJ) was the first in a sequence of UK retail-tech specialist
vendor relationships that would later include Sysrepublic at F&E (CRDM,
2007+), Sysrepublic at Secure (xBR replacement era, 2010s), Appriss and
IBM at the LP tier. The pattern is consistent: **UK retail-tech
specialist consumes the retailer's canonical and delivers a capability
the store physically feels.** RedSky's capability was the TTL itself
(authoring + lifecycle + compile). Sysrepublic's was CRDM (SEL delivery)
and later xBR (LP analytics). The founder's operator trajectory runs
through all of them.

## VII. Next steps

1. Promote this article's canonical proposals (C090 family) into a
   formal RetailSpine v0.7 patch. Cross-reference to
   `[[intactix-canonical-validation]] §III` (Object Versioning, Authority
   Level) — the lifecycle and authority semantics TTL needs are exactly
   the ones that memo already proposes.
2. Add a "Specification / Regulatory" row to the executive-summary table
   in `[[third-branch]] §IV` under *What GrowDirect actually is* — TTL
   is a sibling of the spine (RetailSpine), the bubble (Canary), the
   agents (MCP), and the accounting primitive (sats). It is a **fourth**
   load-bearing surface for the private-label / fresh-prep slice of the
   market.
3. Thread TTL into the Canary MOC as a named post-v1 capability under
   the fresh-prep / private-label expansion. The current Canary wedge
   (Square merchant + LP) does not yet reach fresh-prep; TTL-on-Canary
   is the path that opens the deli/bakery/hot-food case.
4. Read the remaining TTL corpus artifacts: the January 2007 snapshot
   zip and the `DV Private Label Food Setup v3/v4` training decks.
   Likely contains the operator-side flow (supplier onboarding → spec
   authoring → review → pack-copy-sent → TPNB/UPC generation) and
   the specific US regulatory screens (nutrition panel, allergen matrix,
   pack copy) that ship with the US TTL clone. Those would strengthen
   the C090 proposal with concrete field-level detail.

---

*Source: `[[Brain/raw/inbox/tesco-technical-library-corpus|Tesco Technical
Library Corpus]]` — founder-authored TTL Functional Spec V1.0 (18 July 2006)
and V1.2 (19 July 2006); RedSky IT proposal (3 August 2006, Paul Woodward);
Change Request TTL043 (11 October 2006, Paul Raynor); Service Definition
Tesco US; January 2007 snapshot (zip, still to extract); DV Private Label
Food Setup v3/v4 training decks (still to read). Approvers at Tesco US /
F&E: Breda Mitchell (Regulatory Lead), Charlotte Maxwell (Commercial Lead),
Helen Mottram (Technical Manager), Doug Rutledge (IT Director); Document
Owner John O'Brien. Product-information contact: Debra K.W. Topham.
Companion memos: `[[third-branch]]`, `[[intactix-canonical-validation]]`,
`[[srd-shelf-edge-label]]`. Operator-era: founder authored the US Technical
Library functional specification at F&E, 18 July 2006 — ~10 months before
the earliest SRD interface specs.*
