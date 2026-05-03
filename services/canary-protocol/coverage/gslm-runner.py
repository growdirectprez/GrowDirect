"""
GSLM 9-domain coverage runner.

Compares the Canary Go canonical schema (deploy/schema/*.sql) against
the Global Store Logical Model (GSLM) — the 9-domain canonical-model
exemplar the founder's team defined for Walmart International's 2009
banner-rollout work and re-used in 2023 for the Dollar Tree integration.

GSLM domains:
    Item · Customer · Employee · Vendor · Location · Pricing ·
    Inventory · Transaction · Operations

The runner is intentionally a static analysis of SQL DDL (no DB
connection required). It produces:

    1. A per-domain coverage table (canonical tables present, GSLM
       entities mapped, gaps in either direction)
    2. A top-N cross-domain prioritized gap list

Usage:

    python3 services/canary-protocol/coverage/gslm-runner.py \\
        --schema-dir CanaryGo/deploy/schema \\
        --report-out Brain/wiki/cards/gslm-coverage-report-2026-05-03.md

Authority: GRO-722 + GRO-763 Phase B.1.
Provenance: memory project_gslm_provenance.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Iterable

# ──────────────────────────────────────────────────────────────────────
# GSLM 9-domain canonical-entity registry
# ──────────────────────────────────────────────────────────────────────
#
# Each entity carries:
#   - name            human-readable label (matches Walmart 2009 spec)
#   - kind            "core" (must-have for SMB retail) | "extension"
#                     (large-format / compliance / specialized)
#   - canonical_match list of regex patterns matched against
#                     "schema.table" — any match counts as covered
#
# When adding a new GSLM entity, supply one or more match patterns. The
# patterns are intentionally permissive — schemas may name entities with
# tenant-specific prefixes or suffixes, and we want the runner to
# catch reasonable equivalents.

GSLM: dict[str, list[dict]] = {
    "Item": [
        {"name": "Item", "kind": "core", "match": [r"^m\.items$"]},
        {"name": "ItemHierarchy/Category", "kind": "core", "match": [r"^m\.product_categories$", r"^m\.item_categories$"]},
        {"name": "Barcode/GTIN", "kind": "core", "match": [r"^m\.item_barcodes$"]},
        {"name": "Pack/UOM", "kind": "core", "match": [r"^m\.item_packs$", r"^m\.item_units$"]},
        {"name": "ItemVendor (sourcing)", "kind": "core", "match": [r"^m\.item_vendors$"]},
        {"name": "Brand", "kind": "extension", "match": [r"^m\.brands$"]},
        {"name": "ItemAttribute (extensible)", "kind": "extension", "match": [r"^m\.item_attributes$", r"^m\.item_attribute_values$"]},
        {"name": "AssortmentList", "kind": "core", "match": [r"^l\.location_assortment$", r"^m\.assortments$"]},
        {"name": "ItemImage/MediaAsset", "kind": "extension", "match": [r"^m\.item_images$", r"^m\.item_media$"]},
        {"name": "ItemSubstitute/CrossRef", "kind": "extension", "match": [r"^m\.item_substitutes$", r"^m\.item_cross_references$"]},
    ],
    "Customer": [
        {"name": "Customer", "kind": "core", "match": [r"^c\.customers$"]},
        {"name": "CustomerAddress", "kind": "core", "match": [r"^c\.customer_addresses$"]},
        {"name": "LoyaltyMember", "kind": "core", "match": [r"^c\.loyalty_memberships$"]},
        {"name": "CustomerSegment", "kind": "extension", "match": [r"^c\.customer_segments$"]},
        {"name": "CustomerEvent (lifecycle)", "kind": "extension", "match": [r"^c\.customer_events$"]},
        {"name": "Party (canonical identity)", "kind": "core", "match": [r"^party\.parties$"]},
        {"name": "Household (decisioning unit)", "kind": "core", "match": [r"^party\.households$"]},
    ],
    "Employee": [
        {"name": "Employee", "kind": "core", "match": [r"^e\.employees$"]},
        {"name": "EmployeeRole/Assignment", "kind": "core", "match": [r"^e\.employee_role_assignments$", r"^app\.user_roles$"]},
        {"name": "User (auth-side)", "kind": "core", "match": [r"^app\.users$"]},
        {"name": "User-Employee link", "kind": "core", "match": [r"^app\.user_employee_links$"]},
        {"name": "EmployeeLocationAssignment", "kind": "core", "match": [r"^e\.employee_location_assignments$", r"^app\.employee_location_assignments$"]},
        {"name": "Shift", "kind": "core", "match": [r"^t\.shift_events$", r"^e\.shifts$"]},
        {"name": "TimeClock/Punch", "kind": "core", "match": [r"^e\.time_clock$", r"^e\.time_punches$", r"^t\.cashier_actions$"]},
        {"name": "EmployeeAvailability", "kind": "extension", "match": [r"^e\.employee_availability$"]},
        {"name": "Compensation", "kind": "extension", "match": [r"^e\.compensation$", r"^e\.pay_rates$"]},
    ],
    "Vendor": [
        {"name": "Vendor", "kind": "core", "match": [r"^m\.vendors$"]},
        {"name": "VendorContact", "kind": "extension", "match": [r"^m\.vendor_contacts$"]},
        {"name": "VendorTerm (payment terms)", "kind": "core", "match": [r"^m\.vendor_terms$", r"^f\.vendor_payment_terms$"]},
        {"name": "SupplierInvoice", "kind": "core", "match": [r"^f\.supplier_invoices$"]},
        {"name": "SupplierInvoiceLine", "kind": "core", "match": [r"^f\.supplier_invoice_lines$"]},
        {"name": "VendorPayment", "kind": "core", "match": [r"^f\.payments$", r"^f\.payment_invoice_applications$"]},
        {"name": "VendorPerformance/Scorecard", "kind": "extension", "match": [r"^m\.vendor_performance$"]},
    ],
    "Location": [
        {"name": "Location/Site", "kind": "core", "match": [r"^l\.locations$"]},
        {"name": "LocationHierarchy", "kind": "core", "match": [r"^l\.location_hierarchy$", r"^l\.location_hierarchy_assignments$"]},
        {"name": "LocationZone (back-of-house)", "kind": "core", "match": [r"^l\.location_zones$"]},
        {"name": "Planogram", "kind": "core", "match": [r"^s\.planograms$"]},
        {"name": "PlanogramAssignment", "kind": "core", "match": [r"^s\.planogram_assignments$"]},
        {"name": "PlanogramPosition (slot)", "kind": "core", "match": [r"^s\.planogram_positions$"]},
        {"name": "Department/Aisle/Bay/Shelf", "kind": "extension", "match": [r"^l\.location_zones$", r"^l\.fixtures$"]},
        {"name": "ServiceArea (delivery zone)", "kind": "extension", "match": [r"^l\.service_areas$", r"^l\.delivery_zones$"]},
    ],
    "Pricing": [
        {"name": "ItemPrice (per item × location)", "kind": "core", "match": [r"^p\.item_prices$"]},
        {"name": "Promotion", "kind": "core", "match": [r"^p\.promotions$"]},
        {"name": "PromotionRule", "kind": "core", "match": [r"^p\.promotion_rules$"]},
        {"name": "Markdown", "kind": "core", "match": [r"^p\.markdowns$"]},
        {"name": "TaxRate", "kind": "core", "match": [r"^p\.tax_rates$"]},
        {"name": "TaxClass", "kind": "core", "match": [r"^p\.tax_classes$"]},
        {"name": "Coupon", "kind": "extension", "match": [r"^p\.coupons$"]},
        {"name": "PriceTier (cost-plus envelope)", "kind": "core", "match": [r"^f\.markup_envelope_tiers$"]},
        {"name": "TenderType (config)", "kind": "core", "match": [r"^f\.tender_types$"]},
    ],
    "Inventory": [
        {"name": "InventoryPosition (on-hand)", "kind": "core", "match": [r"^i\.inventory_positions$"]},
        {"name": "InventoryMovement (audit trail)", "kind": "core", "match": [r"^i\.inventory_movements$"]},
        {"name": "InventoryDocument (count/RTV)", "kind": "core", "match": [r"^i\.inventory_documents$"]},
        {"name": "InventoryDocumentLine", "kind": "core", "match": [r"^i\.inventory_document_lines$"]},
        {"name": "Lot", "kind": "core", "match": [r"^i\.inventory_lots$"]},
        {"name": "SerialUnit", "kind": "extension", "match": [r"^i\.serial_units$", r"^i\.inventory_serials$"]},
        {"name": "Reservation/Allocation", "kind": "core", "match": [r"^o\.allocations$"]},
        {"name": "CycleCount (campaign)", "kind": "core", "match": [r"^i\.cycle_counts$", r"^i\.inventory_documents$"]},
        {"name": "StockLedgerEntry (financial)", "kind": "core", "match": [r"^ledger\.stock_ledger_entries$"]},
    ],
    "Transaction": [
        {"name": "Transaction (sale/return/exchange)", "kind": "core", "match": [r"^t\.transactions$"]},
        {"name": "TransactionLineItem", "kind": "core", "match": [r"^t\.transaction_line_items$"]},
        {"name": "TransactionTender", "kind": "core", "match": [r"^t\.transaction_tenders$"]},
        {"name": "TransactionDiscount", "kind": "core", "match": [r"^t\.transaction_discounts$"]},
        {"name": "CashDrawerEvent", "kind": "core", "match": [r"^t\.cash_drawer_events$"]},
        {"name": "CashierAction (audit)", "kind": "core", "match": [r"^t\.cashier_actions$"]},
        {"name": "GiftCardEvent", "kind": "core", "match": [r"^t\.gift_card_events$"]},
        {"name": "LoyaltyEvent", "kind": "core", "match": [r"^t\.loyalty_events$"]},
        {"name": "ShiftEvent", "kind": "core", "match": [r"^t\.shift_events$"]},
        {"name": "Return/Void/Refund (subtypes)", "kind": "core", "match": [r"^t\.returns$", r"^t\.transactions$"]},  # subtype of transactions
    ],
    "Operations": [
        {"name": "PurchaseOrder", "kind": "core", "match": [r"^o\.purchase_orders$"]},
        {"name": "PurchaseOrderLine", "kind": "core", "match": [r"^o\.purchase_order_lines$"]},
        {"name": "SalesOrder", "kind": "core", "match": [r"^o\.sales_orders$"]},
        {"name": "SalesOrderLine", "kind": "core", "match": [r"^o\.sales_order_lines$"]},
        {"name": "Fulfillment (pick/pack/ship)", "kind": "core", "match": [r"^o\.fulfillments$", r"^o\.fulfillment_lines$"]},
        {"name": "Allocation (soft-reserve)", "kind": "core", "match": [r"^o\.allocations$"]},
        {"name": "ShippingDocument (BOL/manifest)", "kind": "core", "match": [r"^o\.shipping_documents$"]},
        {"name": "ReceivingDoc (ASN)", "kind": "core", "match": [r"^o\.receiving_documents$", r"^i\.inventory_documents$"]},
        {"name": "PutAway", "kind": "extension", "match": [r"^o\.putaway$", r"^i\.inventory_movements$"]},
        {"name": "ReturnToVendor (RTV)", "kind": "core", "match": [r"^o\.rtv$", r"^i\.inventory_documents$"]},
        {"name": "Replenishment", "kind": "extension", "match": [r"^o\.replenishment$"]},
        {"name": "Workflow (cross-cutting orchestration)", "kind": "extension", "match": [r"^app\.workflow_executions$", r"^app\.workflow_definitions$"]},
    ],
}


# Tables we don't expect to map to a GSLM domain (platform plumbing).
PLATFORM_PASSTHROUGH = {
    "app.organizations",
    "app.tenants",
    "app.merchants",
    "app.merchant_settings",
    "app.merchant_sources",
    "app.source_systems",
    "app.external_identities",
    "app.audit_log",
    "app.interest_signups",
    "app.hawk_oauth_tokens",
    "app.bull_api_credentials",
    "app.bull_event_log",
    "app.bull_merchant_config",
    "app.bull_poll_watermarks",
    "app.api_keys",
    "app.workflow_definitions",
    "app.workflow_executions",
    "app.roles",
    "app.location_hierarchy",  # superseded by l.* counterparts
    "app.locations",  # superseded
    "app.employees",  # superseded by e.employees
    "app.employee_location_assignments",  # superseded
    "ledger.blockchain_anchors",
    "ledger.ildwac_positions",
    "ledger.l402_otb_budgets",
    "ledger.rib_batches",
    "f.gl_accounts",
    "protocol.evidence",
    "protocol.source_secrets",
    "q.detection_rules",
    "q.detections",
    "q.subjects",
    "q.cases",
    "q.case_actions",
    "q.case_evidence",
    "party.identifiers",
    "party.identifier_links",
    "party.resolution_events",
    "party.household_memberships",
    "party.household_evidence",
    "party.decisioning_facts",
}


@dataclass
class CanonicalTable:
    schema: str
    name: str

    @property
    def qualified(self) -> str:
        return f"{self.schema}.{self.name}"


@dataclass
class GslmEntity:
    name: str
    kind: str
    matches: list[str] = field(default_factory=list)


@dataclass
class DomainResult:
    domain: str
    canonical_tables: list[str] = field(default_factory=list)
    entities_present: list[GslmEntity] = field(default_factory=list)
    entities_missing: list[GslmEntity] = field(default_factory=list)


CREATE_TABLE_RE = re.compile(
    r"^\s*CREATE\s+TABLE(?:\s+IF\s+NOT\s+EXISTS)?\s+([a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)\s*\(",
    re.IGNORECASE,
)


def parse_canonical_tables(schema_dir: Path) -> list[CanonicalTable]:
    """Walk schema_dir/*.sql; yield (schema, table) for every CREATE TABLE."""
    tables: list[CanonicalTable] = []
    for sql_file in sorted(schema_dir.glob("*.sql")):
        with sql_file.open() as f:
            for line in f:
                m = CREATE_TABLE_RE.match(line)
                if m:
                    tables.append(CanonicalTable(schema=m.group(1), name=m.group(2)))
    return tables


def coverage_for_domain(
    domain: str, gslm_entities: list[dict], canonical_tables: list[CanonicalTable]
) -> DomainResult:
    """Match each GSLM entity against the canonical table set."""
    qualified = {t.qualified for t in canonical_tables}
    present: list[GslmEntity] = []
    missing: list[GslmEntity] = []
    domain_canonical_tables: set[str] = set()

    for ent in gslm_entities:
        matches = [
            q for q in qualified if any(re.match(pat, q) for pat in ent["match"])
        ]
        if matches:
            present.append(GslmEntity(name=ent["name"], kind=ent["kind"], matches=matches))
            domain_canonical_tables.update(matches)
        else:
            missing.append(GslmEntity(name=ent["name"], kind=ent["kind"]))

    return DomainResult(
        domain=domain,
        canonical_tables=sorted(domain_canonical_tables),
        entities_present=present,
        entities_missing=missing,
    )


def find_unmapped_tables(
    canonical_tables: list[CanonicalTable], domain_results: list[DomainResult]
) -> list[str]:
    """Tables that didn't match any GSLM entity AND aren't platform passthrough."""
    mapped: set[str] = set()
    for r in domain_results:
        mapped.update(r.canonical_tables)
    unmapped: list[str] = []
    for t in canonical_tables:
        q = t.qualified
        if q in mapped or q in PLATFORM_PASSTHROUGH:
            continue
        unmapped.append(q)
    return sorted(unmapped)


def render_report(
    domain_results: list[DomainResult],
    canonical_tables: list[CanonicalTable],
    unmapped: list[str],
) -> str:
    """Markdown report — Brain wiki card format."""
    today = date.today().isoformat()
    total_canonical = len(canonical_tables)
    total_platform = sum(1 for t in canonical_tables if t.qualified in PLATFORM_PASSTHROUGH)
    domain_total = sum(len(r.entities_present) + len(r.entities_missing) for r in domain_results)
    domain_present = sum(len(r.entities_present) for r in domain_results)

    out: list[str] = []
    out.append("---")
    out.append(f"title: GSLM 9-domain Coverage Report — {today}")
    out.append("type: coverage-report")
    out.append("status: active")
    out.append(f"date: {today}")
    out.append("linear: GRO-722")
    out.append("parent: GRO-763")
    out.append("authority: GSLM Walmart-International 2009 canonical-model exemplar")
    out.append("provenance: memory project_gslm_provenance")
    out.append(f"last-compiled: {today}")
    out.append(f"needs-review: 2026-08-03")
    out.append("---")
    out.append("")
    out.append("# GSLM 9-domain Coverage Report")
    out.append("")
    out.append(
        "Static analysis of `CanaryGo/deploy/schema/*.sql` against the "
        "Global Store Logical Model (GSLM) — the 9-domain canonical-model "
        "exemplar the founder's team defined for Walmart International's "
        "2009 banner-rollout work. GSLM is used here as a **completeness "
        "checklist**, not a schema source. Entities listed in GSLM but "
        "missing from canonical schema flag potential gaps; entities "
        "present in canonical but absent from GSLM are documented as "
        "one-way differences (Canary's accountability rails are intentionally "
        "richer than the 2009 spec)."
    )
    out.append("")
    out.append("## Summary")
    out.append("")
    out.append(f"- **Canonical tables analyzed:** {total_canonical}")
    out.append(f"- **Platform plumbing (passthrough):** {total_platform}")
    out.append(f"- **GSLM entities checked:** {domain_total}")
    out.append(f"- **GSLM entities mapped:** {domain_present} ({domain_present * 100 // domain_total}%)")
    out.append(
        f"- **Domains with full core coverage:** "
        f"{sum(1 for r in domain_results if not [e for e in r.entities_missing if e.kind == 'core'])}/9"
    )
    out.append("")

    out.append("| Domain | Tables | Core entities | Core mapped | Extension mapped | Gaps (core) |")
    out.append("|---|---|---|---|---|---|")
    for r in domain_results:
        core_total = sum(1 for e in r.entities_present + r.entities_missing if e.kind == "core")
        core_present = sum(1 for e in r.entities_present if e.kind == "core")
        ext_total = sum(1 for e in r.entities_present + r.entities_missing if e.kind == "extension")
        ext_present = sum(1 for e in r.entities_present if e.kind == "extension")
        core_gaps = ", ".join(e.name for e in r.entities_missing if e.kind == "core") or "—"
        out.append(
            f"| {r.domain} | {len(r.canonical_tables)} | {core_total} | "
            f"{core_present}/{core_total} | {ext_present}/{ext_total} | {core_gaps} |"
        )
    out.append("")

    for r in domain_results:
        out.append(f"## {r.domain}")
        out.append("")
        if r.canonical_tables:
            out.append("**Canonical tables:**")
            out.append("")
            for t in r.canonical_tables:
                out.append(f"- `{t}`")
            out.append("")
        else:
            out.append("**Canonical tables:** _(none mapped)_")
            out.append("")

        out.append("**Entities mapped:**")
        out.append("")
        if r.entities_present:
            for e in r.entities_present:
                tag = "" if e.kind == "core" else " _(extension)_"
                covers = ", ".join(f"`{m}`" for m in e.matches)
                out.append(f"- {e.name}{tag} → {covers}")
        else:
            out.append("- _(none)_")
        out.append("")

        out.append("**Gaps:**")
        out.append("")
        if r.entities_missing:
            for e in r.entities_missing:
                tag = "**core**" if e.kind == "core" else "extension"
                out.append(f"- {e.name} ({tag})")
        else:
            out.append("- _(none — full coverage)_")
        out.append("")

    out.append("## Top cross-domain gaps (prioritized)")
    out.append("")
    out.append(
        "Ranked by impact on the platform mission (operational / financial "
        "/ evidentiary accountability). Core gaps surface here before "
        "extension gaps."
    )
    out.append("")
    core_gaps_flat: list[tuple[str, str]] = []
    ext_gaps_flat: list[tuple[str, str]] = []
    for r in domain_results:
        for e in r.entities_missing:
            (core_gaps_flat if e.kind == "core" else ext_gaps_flat).append(
                (r.domain, e.name)
            )
    rank = 1
    for domain, name in core_gaps_flat[:10]:
        out.append(f"{rank}. **{domain} · {name}** (core)")
        rank += 1
    for domain, name in ext_gaps_flat[: max(0, 10 - rank + 1)]:
        out.append(f"{rank}. {domain} · {name} (extension)")
        rank += 1
    out.append("")

    if unmapped:
        out.append("## Canonical tables not mapped to a GSLM entity")
        out.append("")
        out.append(
            "These tables exist in the canonical schema but don't match any "
            "GSLM 9-domain entity pattern AND aren't on the platform-passthrough "
            "allowlist. They likely represent intentional Canary extensions "
            "(accountability rails, LP detection, evidentiary substrate) — "
            "review and either add to GSLM patterns above (if they map to "
            "an existing entity by another name) or to PLATFORM_PASSTHROUGH "
            "(if they're plumbing)."
        )
        out.append("")
        for q in unmapped:
            out.append(f"- `{q}`")
        out.append("")

    out.append("## Cross-references")
    out.append("")
    out.append(
        "- Memory `project_gslm_provenance` — origin of GSLM as canonical-"
        "model exemplar"
    )
    out.append(
        "- [`docs/sdds/go-handoff/canonical-data-model.md`]"
        "(../../../docs/sdds/go-handoff/canonical-data-model.md) — schema source of truth"
    )
    out.append(
        "- [`docs/sdds/go-handoff/canonical-data-model-party-edits.md`]"
        "(../../../docs/sdds/go-handoff/canonical-data-model-party-edits.md) — party schema (lands GRO-763 Phase B.5)"
    )
    out.append(
        "- [`services/canary-protocol/coverage/gslm-runner.py`]"
        "(../../../services/canary-protocol/coverage/gslm-runner.py) — the runner that produced this report"
    )
    out.append("")

    return "\n".join(out)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--schema-dir",
        default="CanaryGo/deploy/schema",
        help="Directory holding *.sql files (default: CanaryGo/deploy/schema)",
    )
    parser.add_argument(
        "--report-out",
        default="-",
        help="Output path for the report (default: stdout)",
    )
    args = parser.parse_args(argv)

    schema_dir = Path(args.schema_dir)
    if not schema_dir.is_dir():
        print(f"error: schema dir not found: {schema_dir}", file=sys.stderr)
        return 2

    canonical = parse_canonical_tables(schema_dir)
    if not canonical:
        print(f"error: no CREATE TABLE statements found under {schema_dir}", file=sys.stderr)
        return 3

    domain_results = [
        coverage_for_domain(domain, entities, canonical)
        for domain, entities in GSLM.items()
    ]
    unmapped = find_unmapped_tables(canonical, domain_results)
    report = render_report(domain_results, canonical, unmapped)

    if args.report_out == "-":
        print(report)
    else:
        out_path = Path(args.report_out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report)
        print(f"wrote {out_path} ({len(report.splitlines())} lines)", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
