---
type: research
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Tesco Operating Model (TOM) — Extraction Index

> **Source:** `~/GrowDirect/ALX_SYS/ALX/Tom/PROCESSES/`
> **Period:** 2001-2007 (Tesco IT Change Programme)
> **Context:** "The other Tom" — Tesco Operating Model, documented by Jeffe

---

## File Inventory

| File | Topic | Lines | Key Content |
|------|-------|-------|-------------|
| `OM Map v24 Powerpoint DRAFT - UK Exec 070125.ppt` | Complete Operating Model v1.24 | 223 | ~100 Level 1 processes across entire retail value chain |
| `TOM Top Down Design - Property pack template Jul 06 V5_1.ppt` | Property Services | 449 | ~20 L1/L2 processes for store development, construction, maintenance |

---

## The Operating Model v1.24 (OM Map)

Issued January 25, 2007. Tesco's complete retail operating model organized as a value chain:

### Value Chain Categories

| # | Category | Scope |
|---|----------|-------|
| 1 | **DEFINE THE OFFER** | Customer understanding, category planning, ranging, space rules, pricing strategy, promotions strategy |
| 2 | **ACQUIRE, MANUFACTURE** | Sourcing, supplier management, international sourcing, seasonal buys, purchase orders |
| 3 | **FORECAST & ORDER** | Demand forecasting, stock ordering (stores + DCs), allocation, replenishment |
| 4 | **PRIMARY DISTRIBUTION** | Transport, DC operations, network volumes, DC labour scheduling |
| 5 | **STORE DISTRIBUTION** | Receiving, warehouse layout, stock transfers, shelf replenishment |
| 6 | **STORE OPERATIONS** | Space/range/display execution, promotions, stock take, price integrity, production, waste |
| 7 | **STORE OPERATIONS (SELLING)** | Checkout, counters, local marketing, catering, petrol, concessions, **minimise shrink** |
| 8 | **FINANCIAL CONTROL** | Budget, fixed assets, **sales & tender validation**, invoice matching, payroll, ledgers, treasury |
| 9 | **IT/OPERATIONS** | Architecture, development, deployment, support |
| 10 | **PEOPLE** | Recruiting, training, values, rewards, performance, attendance, leavers |
| 11 | **STRATEGIC OPERATIONS** | Commercial strategy, price strategy, distribution network, brand/format |
| 12 | **MANAGEMENT INFORMATION** | Marketing, supply chain, property, SRD, commercial, store, finance, executive reports |
| 13 | **OPERATIONS DEVELOPMENT** | Operational insight, solution generation, trial & test, implement change |

### Space, Range & Display (SRD) Team

The OM Map includes a detailed team structure for the International Operations Division (IOD) Space, Range & Display function:
- IOD Director: Janet Smith
- Best Practice Development, Capability Management, Implementation (Turkey/US)
- Systems: JDA Floor Planning, JDA Space Planning, Retek Assort, custom .NET ranging tools

### Systems Architecture (2007)

| System | Vendor/Type |
|--------|------------|
| Floor Planning | JDA |
| Space Planning | JDA |
| Assortment | Retek Assort |
| Planogram | JDA + custom generators |
| Ranging Controls | In-house .NET |
| Store Communication | In-house |
| Reporting | In-house |

---

## TOM Property Services (Top-Down Design)

Property pack template from the Tesco IT Change Programme. Created 2001, last updated July 2006. 836 revisions.

### Property Services Principles
- Maximise return on investment by optimising site usage
- Create new trading space (new stores + extensions)
- Refit stores for like-for-like growth
- Year-on-year reduction in standard build costs
- Challenge design specifications (off-the-shelf vs bespoke)
- Reduce energy costs; track consumption at store level
- Enable growth sustainably

### Level 1 Processes (Property)

| # | Process | Governance |
|---|---------|-----------|
| 1 | Create Format Blueprints for Store Types | RDG Approval |
| 2 | Set the Store and DC Development Programme | RDG Approval |
| 3 | Set Engineering and Fire Safety Standards | RDG Approval |
| 4 | Set Store Design Standards | RDG Approval |
| 5 | Create Feasibility Site Plans for Stores | RDG + PAC Approval |
| 6 | Set Standard Build Costs | — |
| 7 | Implement Design Standards to Development Plans | RDG Approval |
| 8 | Create Development Budgets | PAC Approval |
| 9 | Develop Store Construction Plans | RDG Approval |
| 10 | Develop DC Construction Plans | IODG Approval |
| 11 | Build for Less | PAG/PAC Approval |
| 12 | Tender for Construction, Agree and Sign Contracts | — |
| 13 | Build Facilities (Stores, DCs, HO) | Building Permit |
| 14 | Pay for Construction and Maintenance | Budget Control |
| 15 | Maintain Facilities (Stores, DCs, HO) | SLA + CQT |
| 16 | Reduce Energy Use | CR Targets |
| 17 | Refit Stores | CIA + CQT |

### Process Documentation Standard

Each TOM process follows a consistent 4-question framework:
1. **What we do** (short description of Level 1 Process)
2. **What does that mean?** (more detailed description)
3. **Why do we do it** (what value does this process deliver to the business)
4. **How do we measure it** (e.g. contribution to availability, customer promises)

Plus Level 2 sub-processes for each.

### Open Decisions (at time of documentation)

| Question | Status |
|----------|--------|
| Who has the A for Loss Prevention in TOM? | Unresolved |
| Who has the A for Corporate Purchasing in TOM? | Unresolved |
| Who has the A for New Store Opening in TOM? | Retail - Richard Dodd? |
| Who has the A for concession space allocation? | Commercial? |
| Who has the A for DC Blueprints in TOM? | Clarify |
| Who has the A for Site Research in TOM? | Best practice not in TOM |
| Who has the A for Site Acquisition in TOM? | Best practice not in TOM |
| International governance for Property Services TOM? | Unclear |

---

## Extraction Notes

- PPT format: OLE2 binary (PowerPoint 97-2003)
- Extraction method: `strings -n 8` with noise filtering
- OM Map is a single-slide process map — the slide IS the model (visual layout lost, process names preserved)
- Property Services is a multi-slide deck with full L1/L2 documentation per process
- Some binary artifacts remain in raw extraction — cleaned in the mapping document

---

*Extracted 2026-03-09 | GrowDirect Inc.*
