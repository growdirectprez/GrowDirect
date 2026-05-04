---
screen: /settings/catalog
title: Catalog Settings
role: ADM | MGR
wave: W2
origin: O
cp_equivalent: "frmcategory + frmtaxcodes + frmvendors (three separate screens — no unified catalog config)"
---

# Catalog Settings

**URL:** `/settings/catalog`  
**Primary role:** ADM; MGR (read; limited edit)  
**Entry points:** Settings → Catalog section

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Catalog Settings", tab bar | |
| Tab content | Tab-dependent | |

## Tabs

### Departments Tab
Lists all departments (categories) defined in the system. Source: synced from CP's department/category table via adapter. Fields: Department ID, Department Name, Parent Department (for nested categories), Item Count, Active.

**CP crosswalk:** CP's `frmcategory` manages this. Canary syncs rather than owns — ADM edits are advisory; the CP database is authoritative. Changes in CP propagate to Canary on next sync. If ADM edits department names in Canary without corresponding CP changes, the records will re-sync from CP and overwrite.

**Read vs Edit:** MGR: read only. ADM: can add descriptive metadata (display name overrides, department aliases for reports). Cannot add or delete departments from Canary — those operations must happen in CP.

**LP context:** Department breakdown in the Category Performance report uses these department records. If a department has no items assigned (Item Count = 0), it will produce empty rows in the category report — an operational cleanup signal.

### Tax Codes Tab
Lists all tax codes defined in the system. Source: synced from CP's tax code table. Fields: Tax Code ID, Description, Rate (%), Applies To.

**Read-only in Canary:** Tax code management is a CP function. Canary displays tax codes for reference — transaction records are tagged with the tax code from CP; reports use these definitions to break down tax collected. No editing in Canary.

### Unit of Measure Tab
Lists UOM codes used in item records. Source: synced from CP. Fields: UOM Code, Description, Base Unit flag.

**Read-only in Canary:** Same pattern as tax codes — CP is authoritative. UOM codes appear in item detail, transfer records, and purchase orders. Ensuring consistency between CP and Canary requires managing the source in CP.

### Price Levels Tab
Lists price levels (e.g., Retail, Wholesale, Contractor, Employee). Source: synced from CP's price level table.

**Important for LP:** Price levels are the legitimate discount pathway. When Canary's discount detection rules evaluate a transaction, they compare the discount against the customer's assigned price level. An employee price level on a non-employee customer account is a potential red flag. This tab gives LP visibility into what price levels exist so they can validate rule configurations against legitimate pricing structures.

**Read-only in Canary.** Price level creation and assignment happen in CP.

**Empty state per tab:** "No [departments/tax codes/UOM codes/price levels] synced from CP. Check the adapter sync status in admin → config."

## Interaction Flows

1. **Audit before category report:** BYR checks Departments tab → sees 3 departments with Item Count = 0 → these are legacy CP categories from a discontinued product line → flags for ADM to clean up in CP → will clean up in Canary on next sync
2. **LP price level audit:** LP investigator sees a discount alert referencing Price Level = Wholesale → opens Catalog Settings → Price Levels tab → confirms Wholesale = 30% discount off retail → intended for B2B accounts only → checks customer record to verify B2B status
3. **ADM sync verification:** After a CP category structure change, ADM opens Catalog Settings → Departments tab → confirms new departments appear → if not, checks adapter sync status in admin → config

## UX Callout

CP splits catalog configuration across three separate Windows forms (`frmcategory`, `frmtaxcodes`, `frmvendors` plus others). Canary consolidates the reference view in one screen because the goal is different: where CP's forms are the editing surfaces for these structures, Canary's Catalog Settings tab is a read surface for agents and managers who need to understand what exists without navigating CP's form architecture. The LP use case — price level validation during alert investigation — is the case where having this in Canary saves the most time: an investigator can verify a discount is legitimate without leaving Canary to query CP.

## Navigation Exits

- `/settings/store/locations` — neighboring settings section
- `/admin/config` — if sync issues are suspected

## Open Questions

None.
