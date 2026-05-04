---
last-compiled: 2026-05-04
needs-review: false
type: reference
status: active
tags: [canary, item-master, catalog, sku, product-dimensions, e-catalog, mobile, functional-requirements]
created: 2026-05-04
---
last-compiled: 2026-05-04
needs-review: false

# Canary — Item Master & Catalog Setup

The item master is the foundation of everything in Canary. Replenishment parameters are stored against items. Planograms are built from items. SOH tracks items. Orders are for items. The quality of the item master determines the quality of everything downstream.

Enterprise retailers solved this with heavyweight systems: Gap's "Item Master" was a 30-step process involving 6 systems, 3 months of PLM lead time, and a dedicated IT team to manage the interfaces. Oracle RMS used a 3-level item hierarchy (Style → SKU → Barcode) that required a specific creation sequence enforced by API validation.

SMB retailers have a barcode, a name, and a price in the POS back-office. That's their item master. The Canary item master replaces that with a real product data model — but populated the modern way: scan a barcode, let the system do the work.

---
last-compiled: 2026-05-04
needs-review: false

## The Item Hierarchy — What Enterprise Got Right

Every retail system from Oracle to SAP to JDA uses a 3-level item hierarchy. The levels vary in name but the concept is universal and correct:

```
Level 1 — Style / Product
  The generic product concept, independent of variant.
  "Men's Black Oxford Shoe" or "Organic Whole Milk" or "Ball-Peen Hammer 16oz"
  Attributes: description, brand, category, subcategory, images

Level 2 — SKU (Stock Keeping Unit)
  A specific, orderable variant. Each SKU has its own barcode.
  Attributes: all Level 1 attributes PLUS variant dimensions (size, color, flavor, etc.)
  This is where replenishment parameters live.

Level 3 — Barcode / Scannable Unit
  The physical barcode on the item (UPC/EAN/PLU).
  One SKU may have multiple barcodes (different market codes, supplier-specific codes).
  This is what the POS scans.
```

**Why this matters for Canary:**

An "organic whole milk, half-gallon" is one SKU (one replenishment record, one SOH counter). It may have three barcodes: the manufacturer UPC, a store-specific PLU, and a weight-based barcode for catch-weight units. All three should resolve to the same SKU in Canary.

A "men's oxford shirt in blue" and the same shirt in white are two SKUs (different SOH, different replenishment, different planogram positions) but one Style (same ordering logic, same supplier, same case pack). The Style level exists so you can view and manage at the product level without duplicating configuration across every color/size variant.

**Canary's implementation stance:** the full 3-level hierarchy is in the data model from day one. The UI exposes it progressively — a grocery SMB sees flat SKUs (no style level needed for canned goods). An apparel retailer sees the style/SKU matrix. The model supports both; the UI adapts.

---
last-compiled: 2026-05-04
needs-review: false

## The Three Item Creation Flows

Modern item setup happens one of three ways. Canary should support all three from launch.

---
last-compiled: 2026-05-04
needs-review: false

### Flow 1: Scan-to-Lookup (Primary for Grocery/CPG)

The fastest path. The operator or associate scans the item's barcode. Canary queries a product content API. If found, the item record is pre-populated. The operator confirms and optionally adjusts.

**Product content APIs available today:**

| Source | Coverage | Cost | Notes |
|---|---|---|---|
| Open Food Facts | 3M+ food products globally | Free / open | Community-maintained; depth varies by brand |
| UPC Item DB | 1.5M+ general merchandise | Free tier + paid | Good for non-food CPG |
| Digit-Eyes | 150M+ barcodes | Paid | Broadest coverage; enterprise tier |
| GS1 US Registry | Official GS1 database | Free lookup | Brand-managed; authoritative for major brands |
| Amazon Product API | Very broad | Paid | Good as fallback; ToS restrictions |

**Scan-to-lookup flow:**

```
Screen 1 — Scan
[ Camera / Bluetooth scanner view ]
Scan the item's barcode or enter manually.

─── barcode scanned: 0 12345 67890 5 ───

Screen 2 — Review auto-filled record
╔══════════════════════════════════════╗
║ Found: Open Food Facts               ║
║                                      ║
║ Name:     Organic Whole Milk         ║
║ Brand:    Horizon                    ║
║ Category: Dairy > Milk               ║
║ Pack:     Half Gallon (64 fl oz)     ║
║ Weight:   2.07 lbs                   ║
║                                      ║
║ [Looks right — continue]             ║
║ [Edit before saving]                 ║
╚══════════════════════════════════════╝

Screen 3 — Operational fields (auto-fill doesn't know these)
Supplier:         [ Select ▼ ]
Case pack size:   [ 4 ] units
Unit cost:        $ [ _____ ]
Selling price:    $ [ _____ ]
Zone / Location:  [ Select ▼ ]
Display min/max:  [ 2 ] / [ 8 ]
```

The product content API fills in the "what is this thing" fields. The operator fills in the "how do we sell this" fields. The split is deliberate — Canary should never ask the operator to re-type a product name that a barcode lookup can provide.

**Lookup failure handling:** if the barcode is not found in any source, the operator enters the product name manually. Canary logs the barcode as "unknown" — over time, the aggregate of unknown barcodes from all Canary merchants builds a private catalog that improves lookup rates for the next operator who scans the same item.

---
last-compiled: 2026-05-04
needs-review: false

### Flow 2: Supplier E-Catalog (Modern EDI Replacement)

The enterprise equivalent was a one-way interface from the supplier's system to the retailer's item master. Today's equivalent is a product content network or supplier portal.

**What exists today:**

| Platform | How it works |
|---|---|
| **GS1 DataSync** | Supplier publishes item data to GS1's 1WorldSync platform; retailer subscribes and receives item records with full attribute data |
| **Salsify / Akeneo** | Product Information Management (PIM) platforms; suppliers maintain item records and share with retailers via API |
| **Supplier catalog CSV/Excel** | The most common SMB reality — a supplier emails a spreadsheet with their product list; the retailer manually enters items |
| **NuOrder / Faire** | B2B wholesale platforms where items are ordered and item data comes with the order |
| **Shopify B2B** | Supplier's Shopify wholesale channel; item data available via Shopify Admin API |

**For Canary's SMB audience, the realistic e-catalog integrations in Phase 1:**

1. **Faire / NuOrder import:** these platforms are widely used by independent retailers and their suppliers. A Faire order import would pull item data (name, brand, description, barcode, case pack, unit cost) from the order automatically. This is the closest thing SMB has to EDI.

2. **Supplier CSV import:** simple but effective. Canary provides a CSV template; the supplier fills it in; the operator uploads it. Field mapping is configurable. Canary validates, shows a preview, and the operator confirms. A supplier with 200 items can be set up in 5 minutes this way.

3. **GS1 DataSync (Phase 2):** when Canary is serving larger SMB operators or chains, GS1 integration provides automated item master maintenance — when a supplier changes a product (new UPC, reformulation, size change), Canary receives the update automatically. This is the full e-catalog vision. Not Phase 1.

**Supplier catalog import flow (CSV):**

```
Supplier Profile → Import Items

1. Download template: [ Download CSV template ]

2. Upload completed file: [ Choose file ]

3. Preview:
   ┌──────────────────────────────────────────────────────┐
   │ 47 items found in file                               │
   │                                                      │
   │ ✓ 44 items ready to import                          │
   │ ⚠  3 items need attention:                          │
   │    Row 12: missing barcode                           │
   │    Row 31: duplicate barcode (already in Canary)     │
   │    Row 38: case pack = 0 (invalid)                  │
   │                                                      │
   │ [ Fix issues ]   [ Import 44 and skip 3 ]            │
   └──────────────────────────────────────────────────────┘

4. Set defaults for all imported items:
   Location: [ Unassigned — I'll slot them manually ]
   Replenishment: [ Min/Max — I'll set parameters per item ]
   Status: [ Active / Trial ]
```

After import, the 44 items appear in the item list with a "needs configuration" flag on the operational fields (location, min/max, price). The product identity fields (name, barcode, case pack, cost) are populated from the supplier file.

---
last-compiled: 2026-05-04
needs-review: false

### Flow 3: Manual Entry (For Local, Artisan, Private Label)

When there's no barcode and no supplier catalog — the farmer's market vendor, the local bakery, the house brand — the operator enters everything manually.

The form should be minimal but complete:

```
New Item — Manual Entry

Required:
  Item name:     [ _________________ ]
  Category:      [ Select ▼ ]
  Barcode:       [ Scan or enter, or generate PLU ]
  Supplier:      [ Select ▼ ]
  Unit cost:     $ [ _____ ]
  Selling price: $ [ _____ ]
  Case pack:     [ ___ ] units

Optional (add later):
  Brand, description, image, dimensions, weight
  Allergens, nutrition, country of origin

[ Save and set location ]
```

**PLU generation:** for items without barcodes (bulk produce, local items), Canary generates a store-assigned PLU code in the 4-digit or 5-digit PLU range. The PLU prints as a barcode label that the associate applies to the item or to the shelf edge. The POS then scans it like any other barcode.

**Private label items:** items the store sells under their own brand (e.g., "Joe's Market Granola"). These are entered manually with the store as the "supplier." Cost is the production cost; the selling price is the retail price. Same data model as any other item — just no external supplier to reference.

---
last-compiled: 2026-05-04
needs-review: false

## Product Dimension Types — What Canary Supports

The "product dimensions" question is about which variant axes an item can have. A size-color matrix (apparel) is very different from a weight-grade matrix (produce). Canary needs to support multiple dimension types without requiring every operator to configure attributes they don't use.

**Dimension Type 1: No variants (simplest)**

One SKU = one product. Grocery, hardware, most general merchandise. No size, no color, no flavor variant. The barcode IS the SKU.

```
Organic Whole Milk (64 fl oz)   ← one SKU, one barcode
```

**Dimension Type 2: Single-axis variants**

One product exists in multiple variants along one dimension — typically pack size or flavor.

```
Horizon Organic Milk:
  Half Gallon (64 fl oz) — SKU A
  Quart (32 fl oz)        — SKU B
  Pint (16 fl oz)         — SKU C
```

Each variant is a separate SKU with its own barcode, SOH, and replenishment record. They share the Style (Horizon Organic Milk) so they can be grouped in the item list and ranged together.

**Dimension Type 3: Two-axis variants (apparel)**

Size × Color matrix. Each combination is a distinct SKU.

```
Men's Oxford Shirt:
  Blue / S    Blue / M    Blue / L    Blue / XL
  White / S   White / M   White / L   White / XL
  Navy / S    Navy / M    Navy / L    Navy / XL
  = 12 SKUs, one Style
```

**Size run / size model** (from GAP doc): when a new style is created, the operator selects a size run (e.g., XS/S/M/L/XL or 28/30/32/34/36 for denim) rather than creating each size manually. The size run is a template. This is the Gap's "size model defaulted at Department/Class level" — for Canary, it means the operator selects a size template (already configured for their apparel category) and all variant SKUs are generated automatically.

```
New Apparel Item:
  Style name: Men's Oxford Shirt
  Category: Tops > Dress Shirts
  Colors available: [ Blue ] [ White ] [ Navy ] [ + Add color ]
  Size run: [ Standard Men's XS-XL ▼ ]
  
  → Generates 12 SKUs automatically (3 colors × 4 sizes)
  → Each SKU gets a unique barcode placeholder (filled from supplier catalog or manual entry)
  → Each SKU gets its own SOH record and replenishment config
```

**Dimension Type 4: Catch weight / weight-variable**

Produce, deli, butcher. The SKU is the product; the price is computed from the weight at sale. No fixed price per unit.

```
Ribeye Steak:
  PLU: 3141
  Priced by: weight (per lb)
  Price: $18.99/lb
  
  At POS: cashier places on scale → weight captured → price calculated
```

For Canary's SOH, catch-weight items are tracked in units received (number of steaks / packages) but the POS returns a weight per sale. Canary must handle the unit-to-weight conversion for SOH tracking: "I received 12 packages averaging 1.4 lbs each; I sold 3 transactions totaling 4.2 lbs — approximately 3 packages."

**Dimension Type 5: Case-pack / inner-pack hierarchy**

The pack item from the GAP doc — a pre-configured assortment of variants in fixed ratios. In grocery terms: a case pack. In apparel terms: a pre-packed assortment.

```
Case Pack — Horizon Organic Milk:
  12 units of Half Gallon (64 fl oz)
  Ordering unit: 1 case = 12 units

Pre-pack — Men's Oxford Shirt Assortment:
  2× S + 4× M + 4× L + 2× XL = 1 assortment pack
  Ordering unit: 1 pack = 12 units (mixed sizes)
```

**Case pack handling in Canary:**

Every item has a Supplier Case Pack (the minimum orderable quantity from the supplier). Canary uses this for order quantity rounding. When the operator enters a quantity, Canary shows the case-rounded result: "You need 47 units → 4 cases of 12 = 48 units."

Pre-packs (mixed-SKU assortments) are a separate entity: the assortment is ordered as one unit but received as components. When a pre-pack arrives, Canary splits it into its component SKUs during receiving — each size/color gets its quantity credited. The operator doesn't need to count sizes separately; the pre-pack definition does the split automatically.

---
last-compiled: 2026-05-04
needs-review: false

## Item Status Lifecycle

Connecting item setup to range management:

```
Draft → Active → On Trial → Phase-Out → Inactive
```

| Status | What it means | Replenishment behavior |
|---|---|---|
| **Draft** | Being set up; not yet in POS item master | None — item not yet live |
| **Active** | On the shelf; being sold and replenished | Full replenishment enabled |
| **On Trial** | Recently added; under evaluation | Min/Max only; 8-week evaluation window |
| **Phase-Out** | Selling down; no new orders | No new POs generated; existing stock depletes |
| **Inactive** | Not carried; historical record preserved | No replenishment; hidden from operational views |

**Draft → Active transition:** triggered by first receiving confirmation. Until the item is physically received and confirmed, it remains in Draft. This prevents ghost items from appearing in SOH reports and POS lookups before the product is actually in the store.

---
last-compiled: 2026-05-04
needs-review: false

## The E-Catalog Vision — What Doesn't Exist Yet

The user's question — "receive a SKU via e-catalog" — points at a capability that doesn't fully exist in the SMB market today. Enterprise retailers have GS1 DataSync. Mid-market has NuOrder and Faire. SMB has a PDF linesheet and an email.

**The Canary catalog play (long-term):**

When Canary has enough merchants, it becomes its own product content network. Every time a merchant sets up an item in Canary (via scan lookup, supplier import, or manual entry), the item record is contributed to a shared catalog (opt-in, anonymized supplier attribution). The next merchant who scans the same barcode gets the record pre-filled not just from Open Food Facts, but from Canary's own item master — enriched with operational data that Open Food Facts doesn't have (case pack, supplier code, typical display minimum, planogram category).

This is the network effect applied to item setup: every item set up anywhere on the Canary network makes item setup easier for every other merchant. A barcode scanned at 1,000 stores is a fully-configured item; a barcode scanned for the first time is a lookup call to Open Food Facts. Over time, the private catalog coverage rate approaches 100% for the item types Canary merchants sell.

**The supplier side:** suppliers who participate (think of it as a free item data service for their retail customers) can push catalog updates to all Canary merchants who carry their products simultaneously. A reformulation, a packaging change, a new UPC — the update flows automatically to every merchant's item master instead of requiring each operator to manually update their POS back-office. This is full GS1 DataSync functionality, but built for SMB, priced at zero for the supplier, and funded by Canary's satoshi billing model.

---
last-compiled: 2026-05-04
needs-review: false

## Build Priority

1. **Scan-to-lookup** (Open Food Facts + UPC Item DB) — day one; eliminates manual item name entry for 70%+ of items
2. **3-level item hierarchy** (Style → SKU → Barcode) in data model — day one; enables apparel and multi-variant items
3. **Dimension type support** (no-variant, single-axis, two-axis/apparel, catch-weight, case-pack) — day one for no-variant and case-pack; apparel in Phase 1 if Bart's stores include apparel
4. **Supplier CSV import** — day one; fastest path to getting a full supplier's catalog into Canary
5. **Item status lifecycle** (Draft → Active → Phase-Out → Inactive) — day one; required for range management
6. **PLU generation** for barcodes-less items — day one; required for produce and local items
7. **Pre-pack / assortment split at receiving** — Phase 1 for apparel VAR; later for general merchandise
8. **Faire / NuOrder import** — Phase 2; valuable for boutique/gift operators on those platforms
9. **Canary network catalog** — Phase 3; requires merchant scale to be useful

[[Brain/wiki/cards/store-ops-capability-model]] · [[Brain/wiki/cards/canary-mobile-task-ux-flows]] · [[Brain/wiki/cards/canary-space-range-display-on-floor]] · [[Brain/wiki/cards/canary-purchase-order-lifecycle]] · [[Brain/projects/Canary]]
