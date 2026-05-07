#!/usr/bin/env python3
"""Build the RapidPOS cost-model.xlsx — 8 named tabs, real formulas, three scenarios."""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

OUT = "/sessions/lucid-peaceful-tesla/mnt/GrowDirect/outputs/diligence/rapidpos/cost-model-output.xlsx"

NAVY = "21295C"
SAND = "F5F1E8"
TEAL = "1C7293"
WHITE = "FFFFFF"

wb = openpyxl.Workbook()
wb.remove(wb.active)

def style_header(ws, row=1, last_col="Z"):
    for cell in ws[row]:
        cell.font = Font(bold=True, color=WHITE, size=11)
        cell.fill = PatternFill("solid", fgColor=NAVY)
        cell.alignment = Alignment(horizontal="left", vertical="center")

def style_input(cell):
    cell.fill = PatternFill("solid", fgColor="FFF8E1")  # editable yellow
    cell.font = Font(bold=True)

def style_calc(cell):
    cell.fill = PatternFill("solid", fgColor=SAND)
    cell.font = Font(italic=True, color="555555")

def style_section(ws, row):
    for cell in ws[row]:
        cell.font = Font(bold=True, size=11)
        cell.fill = PatternFill("solid", fgColor="E0E0E0")

def autosize(ws, widths):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w

# ============================================================================
# 1. TARGET
# ============================================================================
ws = wb.create_sheet("target")
ws["A1"] = "Field"; ws["B1"] = "Value"; ws["C1"] = "Confidence"; ws["D1"] = "Notes"
style_header(ws)
rows = [
    ("Target name", "RapidPOS LLC", "confirmed", ""),
    ("Type", "Counterpoint VAR", "confirmed", ""),
    ("Customer count", 50, "guess", "Founder verification needed"),
    ("Aggregate ARR ($)", 2700000, "guess", "Target-profile midpoint $3-6M; midpoint $4.5M flagged elsewhere"),
    ("Stores aggregate", 1500, "guess", "Range 500-2,500"),
    ("Team headcount", 9, "guess", "Range 6-12"),
    ("Senior engineers", 3, "guess", "Range 2-5; 1-2 are flight-risk-critical"),
    ("Verticals served", "garden / gun / wine / specialty food / feed-and-tack", "confirmed", ""),
    ("Open ticket count", 115, "guess", "Range 80-150"),
    ("Weekly inflow tickets", 40, "guess", "Range 30-50"),
    ("% repeat-cause", 0.65, "guess", "Range 60-70%; load-bearing for A1+A2 sizing"),
    ("Customer-bespoke %", 0.30, "guess", "Range 30%; 70% silently-repeating"),
    ("Modernization appetite", "moderate", "guess", "Conservative team; needs to be sold on cloud narrative"),
    ("Suitor landscape", "1-2 PE rollup interest likely", "guess", "Implicit clock 6-12 months"),
]
for i, (k, v, c, n) in enumerate(rows, start=2):
    ws.cell(row=i, column=1, value=k)
    cell = ws.cell(row=i, column=2, value=v); style_input(cell)
    ws.cell(row=i, column=3, value=c)
    ws.cell(row=i, column=4, value=n)
autosize(ws, [22, 50, 12, 50])

# ============================================================================
# 2. CUSTOMERS — cohort segmentation
# ============================================================================
ws = wb.create_sheet("customers")
ws["A1"] = "Cohort"; ws["B1"] = "Customer count"; ws["C1"] = "% of total"; ws["D1"] = "ARR per customer ($)"; ws["E1"] = "Cohort ARR ($)"; ws["F1"] = "Notes"
style_header(ws)
ws["A2"] = "Eager (compliance-pressured / multi-store)"
ws["A3"] = "Steady (single/small-multi location)"
ws["A4"] = "Laggard (will not modernize)"
ws["A5"] = "TOTAL"
ws["B2"] = 12; ws["B3"] = 28; ws["B4"] = 10
ws["B5"] = "=SUM(B2:B4)"
for r in (2, 3, 4):
    ws.cell(row=r, column=2).font = Font(bold=True)
    style_input(ws.cell(row=r, column=2))
ws["C2"] = "=B2/$B$5"; ws["C3"] = "=B3/$B$5"; ws["C4"] = "=B4/$B$5"; ws["C5"] = "=SUM(C2:C4)"
ws["D2"] = 75000; ws["D3"] = 45000; ws["D4"] = 35000
for r in (2, 3, 4):
    style_input(ws.cell(row=r, column=4))
ws["E2"] = "=B2*D2"; ws["E3"] = "=B3*D3"; ws["E4"] = "=B4*D4"; ws["E5"] = "=SUM(E2:E4)"
for r in (2, 3, 4, 5):
    style_calc(ws.cell(row=r, column=3))
    style_calc(ws.cell(row=r, column=5))
ws["F2"] = "Migrate Phase B (M6-18)"; ws["F3"] = "Migrate Phase C (M18-36)"; ws["F4"] = "Stay on Counterpoint; founder-team supports"
for c in ("C", "C5"):
    pass
# % format
for r in (2, 3, 4, 5):
    ws.cell(row=r, column=3).number_format = "0%"
    ws.cell(row=r, column=4).number_format = "$#,##0"
    ws.cell(row=r, column=5).number_format = "$#,##0"
autosize(ws, [40, 16, 12, 22, 18, 36])

# ============================================================================
# 3. ILDWAC LIFT
# ============================================================================
ws = wb.create_sheet("ildwac_lift")
ws["A1"] = "Cohort"; ws["B1"] = "Customers"; ws["C1"] = "Avg devices"; ws["D1"] = "Conversion difficulty"; ws["E1"] = "Hours per customer"; ws["F1"] = "Total hours"; ws["G1"] = "$ at $200/hr"
style_header(ws)
rows_ildwac = [
    ("Eager", "=customers!B2", 8, 1.2, "=C2*40*D2"),
    ("Steady", "=customers!B3", 4, 1.0, "=C3*40*D3"),
    ("Laggard", "=customers!B4", 3, 0.8, "=C4*40*D4"),
]
for i, (cohort, count, devices, diff, hours) in enumerate(rows_ildwac, start=2):
    ws.cell(row=i, column=1, value=cohort)
    ws.cell(row=i, column=2, value=count)
    style_calc(ws.cell(row=i, column=2))
    style_input(ws.cell(row=i, column=3, value=devices))
    style_input(ws.cell(row=i, column=4, value=diff))
    ws.cell(row=i, column=5, value=hours)
    ws.cell(row=i, column=6, value=f"=B{i}*E{i}")
    ws.cell(row=i, column=7, value=f"=F{i}*200")
ws["A5"] = "TOTAL"; ws["A5"].font = Font(bold=True)
ws["F5"] = "=SUM(F2:F4)"; ws["G5"] = "=SUM(G2:G4)"
for r in (2, 3, 4, 5):
    ws.cell(row=r, column=7).number_format = "$#,##0"
ws["A8"] = "Note:"; ws["A8"].font = Font(bold=True, italic=True)
ws["B8"] = "ILDWAC = Item × Location × Device × MCP × Port × Weighted-Average-Cost (patent #63/991,596). Conversion difficulty multiplier > 1 for serialized inventory; > 1.5 for multi-vendor port mix."
ws.merge_cells("B8:G8")
ws["B8"].alignment = Alignment(wrap_text=True, vertical="top")
ws.row_dimensions[8].height = 40
autosize(ws, [12, 12, 14, 22, 18, 14, 14])

# ============================================================================
# 4. CRDM LIFT
# ============================================================================
ws = wb.create_sheet("crdm_lift")
ws["A1"] = "Cohort"; ws["B1"] = "Customers"; ws["C1"] = "Custom tables/customer"; ws["D1"] = "Hours per table"; ws["E1"] = "Hours per customer"; ws["F1"] = "Total hours"; ws["G1"] = "$ at $200/hr"
style_header(ws)
rows_crdm = [
    ("Eager", "=customers!B2", 12, 8),
    ("Steady", "=customers!B3", 8, 8),
    ("Laggard", "=customers!B4", 5, 8),
]
for i, (cohort, count, tables, hpt) in enumerate(rows_crdm, start=2):
    ws.cell(row=i, column=1, value=cohort)
    ws.cell(row=i, column=2, value=count)
    style_calc(ws.cell(row=i, column=2))
    style_input(ws.cell(row=i, column=3, value=tables))
    style_input(ws.cell(row=i, column=4, value=hpt))
    ws.cell(row=i, column=5, value=f"=C{i}*D{i}")
    ws.cell(row=i, column=6, value=f"=B{i}*E{i}")
    ws.cell(row=i, column=7, value=f"=F{i}*200")
ws["A5"] = "TOTAL"; ws["A5"].font = Font(bold=True)
ws["F5"] = "=SUM(F2:F4)"; ws["G5"] = "=SUM(G2:G4)"
for r in (2, 3, 4, 5):
    ws.cell(row=r, column=7).number_format = "$#,##0"
ws["A8"] = "Note:"; ws["A8"].font = Font(bold=True, italic=True)
ws["B8"] = "CRDM = Canary Retail Data Model, anchored on GSLM (Walmart Intl 2009). Mapping each customer's Counterpoint tables + VAR-proprietary extensions onto CRDM. Hours/table covers schema mapping, adapter dev, validation."
ws.merge_cells("B8:G8")
ws["B8"].alignment = Alignment(wrap_text=True, vertical="top")
ws.row_dimensions[8].height = 40
autosize(ws, [12, 12, 22, 16, 18, 14, 14])

# ============================================================================
# 5. GCP INFRA — 18-workload blueprint at 4 tiers
# ============================================================================
ws = wb.create_sheet("gcp_infra")
ws["A1"] = "Workload"; ws["B1"] = "T0 (today, $/mo)"; ws["C1"] = "T1 (eager-cohort, $/mo)"; ws["D1"] = "T2 (steady + new-logo, $/mo)"; ws["E1"] = "T3 (Global-50 anchor, $/mo)"
style_header(ws)
workloads = [
    ("1. POS adapter ingress", 0, 1500, 6000, 25000),
    ("2. TSP transaction streaming", 0, 1200, 5000, 20000),
    ("3. CRDM canonical store (Cloud SQL → AlloyDB)", 0, 3500, 12000, 60000),
    ("4. ILDWAC service", 0, 1000, 4000, 18000),
    ("5. RIB batch + blockchain anchor", 100, 600, 1800, 6000),
    ("6. Hawk case management", 0, 900, 3000, 12000),
    ("7. Owl search + RAG", 0, 1500, 5000, 22000),
    ("8. LLM inference (Vertex AI)", 200, 20000, 60000, 250000),
    ("9. Edge agent (per-store)", 0, 5000, 18000, 80000),
    ("10. Identity / auth", 0, 700, 2200, 8000),
    ("11. Notifications (SendGrid + Twilio)", 100, 1500, 5500, 22000),
    ("12. Reporting / BI (BigQuery + Looker)", 0, 3000, 9000, 35000),
    ("13. Object / evidence storage", 50, 500, 2000, 10000),
    ("14. Security & audit (SCC Premium + Chronicle)", 0, 2500, 6000, 18000),
    ("15. DR / backup / cross-region", 0, 1000, 3500, 14000),
    ("16. Networking / Cloud Armor", 0, 1500, 5500, 30000),
    ("17. Tax & regulatory compliance", 0, 1800, 1800, 1800),  # constant-cost dominated
    ("18. Agentic ops fabric (A1-A5)", 0, 8000, 20000, 60000),
]
for i, (name, t0, t1, t2, t3) in enumerate(workloads, start=2):
    ws.cell(row=i, column=1, value=name)
    style_input(ws.cell(row=i, column=2, value=t0))
    style_input(ws.cell(row=i, column=3, value=t1))
    style_input(ws.cell(row=i, column=4, value=t2))
    style_input(ws.cell(row=i, column=5, value=t3))
total_row = len(workloads) + 2
ws.cell(row=total_row, column=1, value="TOTAL monthly").font = Font(bold=True)
for col in range(2, 6):
    L = get_column_letter(col)
    ws.cell(row=total_row, column=col, value=f"=SUM({L}2:{L}{total_row-1})").font = Font(bold=True)
ws.cell(row=total_row+1, column=1, value="ANNUALIZED").font = Font(bold=True, italic=True)
for col in range(2, 6):
    L = get_column_letter(col)
    ws.cell(row=total_row+1, column=col, value=f"={L}{total_row}*12").font = Font(bold=True, italic=True)
for r in range(2, total_row+2):
    for col in range(2, 6):
        ws.cell(row=r, column=col).number_format = "$#,##0"
autosize(ws, [44, 18, 22, 24, 24])

# ============================================================================
# 6. PROGRAM COST — three scenarios
# ============================================================================
ws = wb.create_sheet("program_cost")
ws["A1"] = "Component"; ws["B1"] = "Best ($)"; ws["C1"] = "Expected ($)"; ws["D1"] = "Worst ($)"; ws["E1"] = "Source"
style_header(ws)
rows_pc = [
    # (label, best, expected, worst, source)
    ("ISO 27001 — 15 critical-mass controls remediation", 80000, 104000, 140000, "diligence/rapidpos/02; 520 hrs × $200, ±35%"),
    ("ISO 27001 — remaining 78 controls remediation", 180000, 233000, 310000, "diligence/rapidpos/02; ~1,164 hrs"),
    ("ISMS framework (policy + governance)", 30000, 60000, 100000, "200-400 hrs"),
    ("Stage 1 + Stage 2 audit fees", 20000, 35000, 50000, "industry range"),
    ("Surveillance audit (Y2-3 ongoing)", 20000, 30000, 40000, "annual × 2 yrs"),
    ("ILDWAC conversion (across cohorts)", "=ildwac_lift!G5*0.7", "=ildwac_lift!G5", "=ildwac_lift!G5*1.4", "ildwac_lift sheet"),
    ("CRDM mapping (across cohorts)", "=crdm_lift!G5*0.7", "=crdm_lift!G5", "=crdm_lift!G5*1.4", "crdm_lift sheet"),
    ("GCP infra (T1 annualized × 18 months)", "=gcp_infra!C22*1.5", "=gcp_infra!C22*1.5", "=gcp_infra!C22*1.5", "gcp_infra sheet T1 col"),
    ("Day-1 agentic ops compute (Phase A)", 36000, 48000, 72000, "$8k/mo × 6 mo"),
    ("Wyoming counsel (entity formation + ongoing)", 25000, 45000, 80000, "Phase 1 + Phase 2 hourly"),
    ("Compliance-architecture lead role (Y1)", 80000, 120000, 180000, "cash component for runway"),
    ("Engineering team retention pool (RapidPOS senior eng)", 100000, 200000, 350000, "retention-package estimate"),
]
for i, (label, b, e, w, src) in enumerate(rows_pc, start=2):
    ws.cell(row=i, column=1, value=label)
    ws.cell(row=i, column=2, value=b)
    ws.cell(row=i, column=3, value=e)
    ws.cell(row=i, column=4, value=w)
    ws.cell(row=i, column=5, value=src)
total_row = len(rows_pc) + 2
ws.cell(row=total_row, column=1, value="TOTAL Phase A+B (18mo program)").font = Font(bold=True)
for col in range(2, 5):
    L = get_column_letter(col)
    cell = ws.cell(row=total_row, column=col, value=f"=SUM({L}2:{L}{total_row-1})")
    cell.font = Font(bold=True)
    cell.fill = PatternFill("solid", fgColor=NAVY)
    cell.font = Font(bold=True, color=WHITE)
for r in range(2, total_row+1):
    for col in range(2, 5):
        ws.cell(row=r, column=col).number_format = "$#,##0"
autosize(ws, [44, 14, 16, 14, 36])

# ============================================================================
# 7. GLIDE PATH — 24-month sequence
# ============================================================================
ws = wb.create_sheet("glide_path")
ws["A1"] = "Month"; ws["B1"] = "Phase"; ws["C1"] = "Milestone"; ws["D1"] = "Cohort wave"; ws["E1"] = "Compliance gate"
style_header(ws)
glide = [
    (1, "A", "Acquisition close OR channel-partnership executed", "—", "Day-1 agentic ops deployed"),
    (3, "A", "8 of 15 critical-mass controls remediated; sandbox infra live", "—", "Internal review"),
    (6, "A", "All 15 critical-mass controls remediated; sandbox DriftPOS live", "Eager cohort identified", "Pre-Stage-1 dry run"),
    (9, "B", "ISO Stage 1 audit clean; first eager-cohort customer in sandbox", "Eager wave 1 begins", "Stage 1 sign-off"),
    (12, "B", "DriftPOS GA; eager-cohort wave 1 in production", "Eager wave 1 in prod", "Stage 2 observation triggered"),
    (15, "B", "Eager-cohort wave 2 underway; steady cohort begins", "Steady cohort begins", "Stage 2 observation in progress"),
    (18, "B", "ISO 27001 certified; eager-cohort fully migrated", "Steady cohort migrating", "Certificate issued"),
    (24, "C", "Steady cohort migration complete; new-logo wins", "New-logo wave begins", "SOC 2 Type II observation start"),
]
for i, (mo, ph, ms, cw, cg) in enumerate(glide, start=2):
    ws.cell(row=i, column=1, value=f"M{mo}")
    ws.cell(row=i, column=2, value=ph)
    ws.cell(row=i, column=3, value=ms)
    ws.cell(row=i, column=4, value=cw)
    ws.cell(row=i, column=5, value=cg)
autosize(ws, [8, 8, 50, 30, 32])

# ============================================================================
# 8. ASSUMPTIONS
# ============================================================================
ws = wb.create_sheet("assumptions")
ws["A1"] = "Assumption"; ws["B1"] = "Value"; ws["C1"] = "Used in"; ws["D1"] = "Notes"
style_header(ws)
assumps = [
    ("Engineering hourly rate", 200, "ildwac_lift, crdm_lift, program_cost", "Internal blended"),
    ("Compliance-pressure factor (gap-to-discount)", 0.7, "valuation contexts", "Range 0.5 (theoretical) - 1.0 (acute)"),
    ("Lineage-decay coefficient α (substrate)", 0.5, "substrate governance", "Per namespace; default 0.5"),
    ("Phase 1 founder-mint duration (months)", 18, "substrate phase mechanics", "Per bylaws"),
    ("Eager-cohort fraction of customer base", "=customers!C2", "cost-model sizing", "Live link to customers tab"),
    ("Steady-cohort fraction", "=customers!C3", "cost-model sizing", "Live link"),
    ("Laggard fraction", "=customers!C4", "cost-model sizing", "Live link"),
    ("ISO 27001 critical-mass control count", 15, "DriftPOS-blocking gate", "Per saas-acquisition-diligence skill ref/07"),
    ("ISO 27001 total Annex A control count", 93, "full audit scope", "ISO 27001:2022 standard"),
    ("Hours per critical-mass ISO control (avg)", 35, "remediation sizing", "520 / 15"),
    ("GCP T1 monthly aggregate ($)", "=gcp_infra!C22", "annualized run-rate", "Live from gcp_infra"),
    ("Program duration Phase A+B (months)", 18, "program_cost summation", ""),
]
for i, (k, v, used, note) in enumerate(assumps, start=2):
    ws.cell(row=i, column=1, value=k)
    cell = ws.cell(row=i, column=2, value=v)
    style_input(cell)
    if isinstance(v, (int, float)) and 0 < v <= 1:
        cell.number_format = "0.0%"
    elif isinstance(v, (int, float)) and v >= 1000:
        cell.number_format = "$#,##0"
    ws.cell(row=i, column=3, value=used)
    ws.cell(row=i, column=4, value=note)
autosize(ws, [44, 14, 32, 36])

wb.save(OUT)
print(f"WROTE: {OUT}")
print(f"Tabs: {len(wb.sheetnames)} — {wb.sheetnames}")
