---
date: 2026-04-24
type: raw
source:
  - Brain/raw/inbox/Technical Library/TTL_Functional_Spec_V1.2.doc
  - Brain/raw/inbox/Technical Library/ICIX_TTL_Functional_Spec_V1.0.doc
  - Brain/raw/inbox/Technical Library/Tesco_Technical_Library_Modification_Functional_Specification.doc
  - Brain/raw/inbox/Technical Library/Tesco US Proposal V1.0.doc
  - Brain/raw/inbox/Technical Library/Service Definition - Tesco US.doc
  - Brain/raw/inbox/Technical Library/Tesco CR TTL043 Tesco US Enhancements v1.1.doc
  - Brain/raw/inbox/Technical Library/DV Private Label Food Setup v4.ppt
  - Brain/raw/inbox/Technical Library/Tesco Technical Library 01 09 2007.zip
original_source: Fresh & Easy / Tesco US — Product Specification and Regulatory platform, 2006–2007
authors:
  - Geoff Lyle (document author, TTL Functional Spec V1.0 and V1.2)
  - Helen Mottram (edits accepted into V1.1 / V1.2)
  - John O'Brien (document owner)
  - Paul Woodward (RedSky IT Sales & Marketing Director, proposal author)
  - Paul Raynor (change request originator, TTL043)
dates:
  - 2006-07-18 (TTL Functional Spec V1.0, G. Lyle)
  - 2006-07-19 (V1.1 — Mottram edits)
  - 2006-08-03 (RedSky IT Proposal, Paul Woodward)
  - 2006-08-15 (planned production go-live date in scope)
  - 2006-10-11 (Change Request TTL043, Paul Raynor)
  - 2007-01-09 (Tesco Technical Library 01 09 2007.zip snapshot)
project: third-branch
tags: [ttl, tesco-technical-library, creations, redsky-it, fresh-and-easy, tesco-us, private-label, product-specification, recipe, nutrition-facts, allergen, pack-copy, tpnb, upc, icix, founder-authored, canonical-validation]
status: unprocessed
---

# Tesco Technical Library Corpus — F&E Private-Label Product Specification Platform

## Source

Eight working files from `Brain/raw/inbox/Technical Library/`, captured during the
F&E launch prep of the US Technical Library (TTL), summer 2006 through January 2007.
The corpus is the product-specification layer of the F&E operating model — the
counterpart to the SRD (Space, Range & Display) corpus under `Brain/raw/inbox/SRD/`
but addressing a different canonical question: *what is the product?* rather than
*where does it live on the shelf?*

The founder is the named author of the originating functional specification.

## Context for intake

TTL ("Tesco Technical Library") is the Tesco-branded SKU of **Creations**, the
product-lifecycle and specification-management platform built by **RedSky IT**
(UK, Nottingham; US operation set up in South Plainfield, NJ during 2006). The
UK Technical Library was deployed across 1,700+ sites supplying own-label to
Tesco UK by 2006; the 2006–2007 work captured in this corpus is the US clone,
modified for US regulatory requirements and for the F&E operating model.

The TTL *is* the regulatory and specification backbone of private-label food
retail. Every row of private-label product in a Fresh & Easy store — sandwiches,
salads, ready-meals, bakery, prepared foods — was authored in TTL by the
supplier, reviewed in TTL by the Tesco US regulatory and commercial teams, and
promoted through TTL's lifecycle into pack-copy output that drove artwork, label
print, and Oracle Retail item set-up.

TTL is the *third canonical layer* of the F&E operating stack, distinct from and
complementary to:
- **RMS / Oracle Retail** (merchandising master) — C-prefix canonical
- **SRD** (planogram / range / display) — S-prefix canonical
- **TTL / Creations** (specification / regulatory) — the *specification* canonical

Without TTL, the shelf-edge label cannot compile for private-label — because the
legally required text (Statement of Identity, Nutrition Facts, ingredient
declaration with US compound-nesting rules, allergen statements, pack copy,
storage instructions, date code, Tie/Hi pallet math) does not exist anywhere
else in the stack.

## Founder authorship

**TTL Functional Spec V1.0**, dated **18 July 2006**, lists the Document Author
as **Geoff Lyle**. V1.1 (19 July 2006) accepts edits from Helen Mottram. V1.2
carries forward as the production spec for RedSky IT's development work.
Document Owner is **John O'Brien**. The original (V1.0, titled
`Tesco_Technical_Library_Modification_Functional_Specification`) and the
later edit-accepted version (`TTL_Functional_Spec_V1.2`) both carry the
founder as author.

Approvers named on the spec (Tesco US / F&E):

| Role | Name |
|---|---|
| Regulatory Lead | Breda Mitchell |
| Commercial Lead | Charlotte Maxwell |
| Technical Manager | Helen Mottram |
| IT Director | Doug Rutledge |
| Document Owner | John O'Brien |

Product Information Manager at Tesco US (El Segundo, CA) cited in follow-up
correspondence: **Debra K.W. Topham**.

**This matters for the third-branch thesis.** The founder's arrival at F&E was
not operator-side in 2007. It was author of the US Technical Library functional
specification on 18 July 2006 — approximately one year *before* the SRD interface
specs (S039 at v1.2 dated 22 May 2007; S101 at v0.2 dated 14 Sep 2007). The
founder was at F&E in a senior solution / product role from the earliest phase
of the US venture, authoring the spec that the UK's long-standing RedSky IT
relationship consumed for the US clone.

## Corpus inventory

| File | Type | Date | Author / Owner | Role in corpus |
|---|---|---|---|---|
| `Tesco_Technical_Library_Modification_Functional_Specification.doc` | spec V1.0 | 2006-07-18 | Geoff Lyle | Originating functional spec |
| `ICIX_TTL_Functional_Spec_V1.0.doc` | spec V1.0 alt | 2006-07-18 | Geoff Lyle | Functional-requirements-list variant (ICIX-era snapshot) |
| `TTL_Functional_Spec_V1.2.doc` | spec V1.2 | 2006-07-19 (edits) | Geoff Lyle / H. Mottram | Production spec for RedSky dev work |
| `Tesco US Proposal V1.0.doc` | vendor proposal | 2006-08-03 | Paul Woodward (RedSky IT) | RedSky's commercial response — £277,607.50 year 1, £133,407.50 year 2+, 5-year |
| `Service Definition - Tesco US.doc` | service contract | 2006 | RedSky IT | Hosting and ITIL support terms |
| `Tesco CR TTL043 Tesco US Enhancements v1.1.doc` | change request | 2006-10-11 | Paul Raynor | Post-launch US-ization polish (US registration fields, compound-ingredient nesting, barcode check-digit, Tie/Hi) |
| `DV Private Label Food Setup v4.ppt` | training deck | 2006–2007 | F&E Private Label team | Operator training for private-label food setup on TTL |
| `Tesco Technical Library 01 09 2007.zip` | snapshot | 2007-01-09 | F&E | Working snapshot during US implementation |

## What TTL does (extracted from the functional spec)

### Required capabilities (TTL Functional Spec V1.0–V1.2)

1. Clone of UK TTL as starting point for US development
2. Hosted in RedSky IT data centers; secure web access for Tesco US and suppliers
3. **Automatic TPNB generation** per declared product size when spec status
   transitions from *collaboration draft* to *pack copy sent* — algorithm supplied
   by Tesco
4. **Automatic UPC generation** per declared product size, same status transition
   — algorithm supplied by Tesco
5. Number-generation functionality must be **switchable off** when Tesco goes
   into production with RMS in the US (the kill-switch — TTL stops generating
   numbers once Oracle Retail/RMS becomes the master of record)
6. Flat-file export of product data for data migration
7. Recipe calculation module modified for US imperial measures and US rounding
   rules
8. Nutrition label module replaced with US-regulation version (Nutrition Facts,
   RDA handling, serving-size text)
9. US English spelling, MM/DD/YYYY date formats, field-label US-ization
   (Fanciful Name, Statement of Identity, Depot → Tesco DC)

### Product header data model

The spec captures and stores, per product:

- Product Number (TPNB) — Tesco's internal product identifier
- UPC — 8- or 13-digit barcode with check-digit validation
- Product Name / Fanciful Name / Descriptive Name / Statement of Identity
  (multiple nuanced fields; TTL043 clarified their distinct use)
- Size, Category, Sub Group
- Buying Manager, Technical Manager (responsibility assignment)
- Versioning of specifications

### Domain sections of the specification (TTL043 reveals)

- **Registration** (supplier onboarding) — US fields: State/Province, ZIP,
  Federal Tax ID; hidden fields for UK-specific items (VAT Number, Tesco NPD
  contact, cost-categorization-visible-to-supplier)
- **Supplier Details** — site details, multiple supplier contacts
- **Recipe** — compound recipe management in both metric and imperial; ingredient
  supplier tracking
- **Nutrition Facts** — US-regulation label with Servings Per Container (text,
  not numeric — e.g. "Approx 10"), Serving Size Text, Serving Quantity, nutrient
  indent-as-constituent, RDA validation turned off per US rules
- **Ingredients** — **compound-breakdown nesting rule** (US regulatory):
  - Tier 1 compound: `( )` round brackets — *Beef Stew (Beef, Water, Potato, Salt, MSG)*
  - Tier 2 (compound-in-compound): `[ ( ) ]` — *Beef Stew [Beef, Vegetable Stock (Water, Potato, Flavouring), salt, MSG]*
  - Tier 3: `{ [ ( ) ] }` — full curly/square/round nesting
  - No emboldening (US: illegal); terminal full stop
- **Dietary and Allergy Data** — US-reduced to 6 retained statements (Milk,
  Wheat, Egg, Fish, Shellfish, Soy) + 2 new (Tree Nuts, Peanuts); all other UK
  statements removed. Drop-downs added for nut types, fish types, shellfish
  types. "This product is made in a factory that processes ..." statement with
  multi-select dropdown of the 8 major US allergens
- **Finished Product Standards** — Quantitative Micro standards, Maximum /
  Report to Tesco, Method column
- **Product Storage** — Serve Before Date → Date Code and Delivery Destination;
  Minimum Life into Depot → Minimum Life in Tesco DC or Store; Short Life
  Product < 30 days
- **Packaging** — Primary/Transit radio; component weights mandatory; Pallet
  details with US standard **Tie** (crates per pallet layer) and **Hi**
  (layers per pallet)
- **Pack Copy** — compiled output for the printed label; Brand Guidelines,
  Allergen as sub-section under Ingredient Information, raw meat & poultry
  statement, editable Fanciful Name / Statement of Identity at pack-copy
  level (distinct from header values)

### Operational lifecycle

Spec status machine progressing through:
1. *Supplier draft* (supplier authoring, no TPNB required yet)
2. *Collaborative draft* (review, no TPNB required yet)
3. *Pack copy sent* → **TPNB and UPC auto-generated at this transition**
4. (Subsequent live / approved states with pack-copy lock)

The kill-switch on number generation ties TTL to the RMS / Oracle Retail master
handoff — TTL generates interim numbers only until RMS is in production,
after which TTL consumes numbers from RMS rather than producing them. This is
the same inversion pattern the SRD ordering gate enforces on the planogram
side: *TTL is subordinate to the master of record once the master of record
exists.*

## Vendor context (from RedSky IT proposal, 3 Aug 2006)

- **Creations** is RedSky IT's product brand; "Tesco Technical Library" is
  Tesco's internal naming
- 2005 Tesco UK committed to an international global licence of £100,000, of
  which 50% was already paid. US adoption triggered the remaining 50%.
- 40 days professional services + 56.5 days development quoted for the US clone
- Target go-live: end of October 2006 (6-week development, UAT mid-September,
  training October, supplier marketing/registration in parallel)
- RedSky IT setting up US operation (1 Cragwood Road Suite 202, South
  Plainfield, NJ 07080) during 2006; sales executed from UK + NJ
- Platform: Lotus Domino R6.5 as both application server and database server;
  Windows Server 2003; primary/backup clustered + reporting server; Telehouse
  London data centre (live) + Nottingham (test/UAT + dev)
- Customer base quoted in 2006: ASDA Wal\*Mart, Tesco, J Sainsbury,
  Somerfield, Iceland, Woodwards, Waitrose, Booker Cash & Carry, The Body
  Shop International — 2,300 companies, 17,000 users, 27,000 own-brand
  products managed on the platform
- UK industry collaboration: Provisions Trade Federation, Institute of Grocery
  Distribution, Bodycote Laboratories

## Synthesis notes (for wiki)

1. **TTL is the third canonical layer at F&E** — specification / regulatory,
   distinct from merchandising (RMS / Oracle Retail) and planogram (SRD). Each
   of the three has a master of record and a kill-switch posture relative to
   the others.

2. **The shelf-edge label is the compile point of all three canonicals for
   private-label.** Statement of Identity, Nutrition Facts, Ingredients (with
   US compound nesting), Allergens, and Pack Copy come from TTL. Product
   identity, price, range status come from RMS. Facings, capacity, planogram
   assignment come from SRD. All three land on the same rail tag via the
   Storeline → CRDM path (see `[[srd-shelf-edge-label]]`).

3. **TTL043 (11 Oct 2006) is the post-launch regulatory patch corpus** — the
   compound-ingredient nesting rules (curly/square/round brackets by tier),
   RDA-validation disable, barcode check-digit, US pallet math (Tie/Hi), and
   the Fanciful Name / Statement of Identity / Descriptive Name field
   triangulation are all documented here as the US-vs-UK delta at the
   operator level, two-ish months after the spec was written.

4. **The founder-authorship predates the SRD interface specs by ~10 months.**
   TTL V1.0 is 18 July 2006. S039 v1.2 is 22 May 2007. S101 v0.2 is 14 Sep
   2007. The founder was the original US Technical Library spec author at F&E
   before the SRD interface layer was drafted. This adjusts the third-branch
   narrative: the founder's F&E role began in senior solution/product
   capacity in mid-2006, authoring the TTL functional spec with Regulatory,
   Commercial, Technical, and IT Director approvers at Tesco US.

5. **Small-grocer / Canary relevance.** Every small grocer that operates a
   deli, bakery, salad bar, sandwich station, hot food bar, or prepared-foods
   program has every regulatory obligation TTL was built to discharge —
   Statement of Identity, Nutrition Facts, ingredient list with US compound
   rules, allergen statements including cross-contact, pack copy compile.
   Most small grocers discharge these obligations by hand (printed binder,
   pre-formatted templates, laminated cards at the case) because no vendor
   has packaged them at SMB price. A Canary-era TTL — the *same spec canonical*
   rebuilt with agents doing the authoring, nutrition calculation, allergen
   matrix, and compound nesting automatically from recipe entry — is a
   capability wedge the founder has pre-authored. It is exactly the kind of
   ambient-spec surface that closes the fresh-prep gap at the SMB tier.

6. **RedSky IT / Creations / Sysrepublic parallel.** RedSky IT (UK, Nottingham)
   played the same role in TTL that Sysrepublic would later play in CRDM
   (shelf-edge label delivery) and xBR / Secure (LP analytics): UK-based
   retail-tech specialist selling a productized canonical into Tesco and the
   broader UK supermarket cohort. The founder's 2006 RedSky IT engagement
   is the first in a sequence of UK retail-tech vendor relationships that
   later include Sysrepublic-at-F&E (CRDM, 2007+), Sysrepublic-at-Secure
   (xBR replacement era, 2010s), Appriss and IBM at the LP tier. The
   relational pattern is consistent: **UK retail-tech specialist consumes
   the canonical and delivers a capability the store physically feels.**

7. **Third-canonical implication for RetailSpine.** RetailSpine's current
   catalog does not have an explicit Product Specification / Regulatory
   surface. The implicit assumption has been that `C001 Product Master`
   carries enough attribute structure to cover the regulatory footprint. TTL
   disproves that assumption for private-label fresh-prep food: *the
   specification is a lifecycle object with versioning, supplier
   collaboration, recipe calculation, nutrition calculation, allergen
   matrix, and pack-copy compile, distinct from the master-data item
   record.* RetailSpine v0.7 should add a fourth canonical surface under
   the C-prefix (something like **C090 Product Specification** with a
   lifecycle state machine echoing TTL's {supplier-draft, collaborative-draft,
   pack-copy-sent, approved, live}) as the private-label / fresh-prep
   canonical complement to C001.

## Still to read / extract

- `Tesco Technical Library 01 09 2007.zip` — January 2007 snapshot; not yet
  extracted
- `DV Private Label Food Setup v4.pdf` — operator training deck; converted to
  PDF but not yet read
