---
type: workorder
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# Coffee-Shop Seed Data Spec — Level B Demo
**Author:** Jim (QA Manager & CSM)
**Date:** February 26, 2026
**Demo Date:** Monday, March 3, 2026
**Purpose:** Seed data for guided demo with one specialty coffee merchant. This is what the merchant will see on screen Monday.

> **NAMING RULE:** Merchant is "Lighthouse Coffee" — NOT Offset Coffee. All data uses the fictional name.
> **GOAL:** The merchant looks at the screen and thinks "that's my Tuesday."

---

## 1. Merchant Record

**Table: `merchants`** (or equivalent top-level merchant identity)

| Field | Value | Notes |
|-------|-------|-------|
| merchant_id | `demo_merch_lighthouse_001` | Use consistent ID across all tables |
| business_name | `Lighthouse Coffee` | Fictional — do NOT use Offset Coffee |
| square_merchant_id | `SQ_DEMO_LH_001` | Sandbox value |
| business_type | `specialty_coffee` | |
| state | `CA` | |
| city | `Torrance` | |
| timezone | `America/Los_Angeles` | Critical for time-of-day Chirp logic |
| owner_employee_id | `emp_001` | Alex Navarro |
| demo_flag | `true` | Mark as demo/seed data |

---

## 2. Location Record

**Table: `locations`**

One location for the demo. Do not add a second — we want single-location simplicity.

| Field | Value |
|-------|-------|
| location_id | `demo_loc_lighthouse_pch` |
| merchant_id | `demo_merch_lighthouse_001` |
| location_name | `Lighthouse Coffee — PCH` |
| address_line1 | `2240 Pacific Coast Hwy` |
| city | `Torrance` |
| state | `CA` |
| zip | `90505` |
| square_location_id | `SQ_LOC_LH_PCH` |
| is_primary | `true` |

---

## 3. Employee Roster

**Table: `employees`** (or `users` with role field)

7 employees. Roles map to Canary RBAC: OWNER (full permissions), SHIFT_LEAD (Store Manager — restricted), BARISTA (Barista/part-timer — restricted).

| employee_id | full_name | role | employment_type | hire_notes | demo_login |
|---|---|---|---|---|---|
| `emp_001` | Alex Navarro | OWNER | Full-time | Owner-operator. Runs daily ops, manages all staff. | `alex@lighthouse.demo` |
| `emp_002` | Rosa Medina | SHIFT_LEAD | Full-time | 5 years at the shop. Opens most weekday mornings. Trusted. | `rosa@lighthouse.demo` |
| `emp_003` | Diego Chen | BARISTA | Full-time | Regular closer. 2 years. Recent performance concern (see Chirps). | `diego@lighthouse.demo` |
| `emp_004` | Priya Patel | BARISTA | Full-time | Morning specialist. Reliable, accurate counts. | `priya@lighthouse.demo` |
| `emp_005` | Cody Walsh | BARISTA | Part-time | College student. Afternoon/closing shifts. 3+ no-sale drawer opens Thu. | `cody@lighthouse.demo` |
| `emp_006` | Marisol Torres | BARISTA | Part-time | Opens 2-3x/week. Dependable, quiet. | `marisol@lighthouse.demo` |
| `emp_007` | Jake Rivera | BARISTA | Part-time | Weekends + some weekday closes. | `jake@lighthouse.demo` |

**Demo login for walkthrough:** Alex Navarro (`emp_001`, OWNER role). This is the persona the merchant will see — full permissions, sees all Chirps, can escalate to Fox.

---

## 4. Employee Timecards

**Table: `employee_timecards`**

Required for Process 4 Step 2 ("Who touched it last?" — pre-fills the closer list from timecard data).

### Thursday, February 26

| employee_id | clock_in | clock_out | shift_type |
|---|---|---|---|
| `emp_002` (Rosa) | 2026-02-26 06:30 | 2026-02-26 14:30 | OPEN/AM |
| `emp_004` (Priya) | 2026-02-26 07:00 | 2026-02-26 13:00 | AM |
| `emp_005` (Cody) | 2026-02-26 13:30 | 2026-02-26 21:15 | PM/CLOSE |

### Friday, February 27

| employee_id | clock_in | clock_out | shift_type |
|---|---|---|---|
| `emp_002` (Rosa) | 2026-02-27 06:30 | 2026-02-27 14:30 | OPEN/AM |
| `emp_004` (Priya) | 2026-02-27 07:00 | 2026-02-27 12:00 | AM |
| `emp_003` (Diego) | 2026-02-27 14:00 | 2026-02-27 21:30 | PM/CLOSE |

### Saturday, February 28

| employee_id | clock_in | clock_out | shift_type |
|---|---|---|---|
| `emp_002` (Rosa) | 2026-02-28 06:30 | 2026-02-28 15:00 | OPEN |
| `emp_001` (Alex) | 2026-02-28 07:00 | 2026-02-28 12:00 | OWNER_FLOOR |
| `emp_007` (Jake) | 2026-02-28 10:00 | 2026-02-28 16:00 | MID |
| `emp_003` (Diego) | 2026-02-28 15:00 | 2026-02-28 21:45 | PM/CLOSE |

### Sunday, March 1

| employee_id | clock_in | clock_out | shift_type |
|---|---|---|---|
| `emp_006` (Marisol) | 2026-03-01 07:30 | 2026-03-01 13:30 | OPEN/AM |
| `emp_001` (Alex) | 2026-03-01 08:00 | 2026-03-01 14:00 | OWNER_FLOOR |
| `emp_007` (Jake) | 2026-03-01 08:00 | 2026-03-01 16:00 | MID/CLOSE |

### Monday, March 3 (Demo Day — morning only)

| employee_id | clock_in | clock_out | shift_type |
|---|---|---|---|
| `emp_002` (Rosa) | 2026-03-03 06:30 | (ongoing) | OPEN/AM |
| `emp_004` (Priya) | 2026-03-03 07:00 | (ongoing) | AM |

---

## 5. Cash Drawer Shifts

**Table: `cash_drawer_shifts`**

Five shifts. The Saturday close is the one with variance that fires the hero Chirp.

| shift_id | date | opened_by | opened_at | opening_cash_cents | closed_by | closed_at | closed_cash_cents | expected_cash_cents | cash_variance_cents | status | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `CDS-001` | 2026-02-26 | `emp_002` | 06:30 | 20000 | `emp_005` | 21:00 | 18750 | 18325 | +425 | CLOSED | Over by $4.25 — no Chirp |
| `CDS-002` | 2026-02-27 | `emp_002` | 06:30 | 20000 | `emp_003` | 21:30 | 21575 | 21850 | -275 | CLOSED | Short $2.75 — under threshold, no Chirp |
| `CDS-003` | 2026-02-28 | `emp_002` | 06:30 | 22500 | `emp_003` | 21:45 | 21260 | 23000 | **-1740** | CLOSED | **⚠️ SHORT $17.40 → CASH_VARIANCE_THRESHOLD FIRES** |
| `CDS-004` | 2026-03-01 | `emp_006` | 07:30 | 20000 | `emp_001` | 13:45 | 23400 | 23300 | +100 | CLOSED | Over $1.00 — essentially balanced |
| `CDS-005` | 2026-03-03 | `emp_002` | 06:45 | 20000 | (open) | — | — | — | — | OPEN | Demo day active drawer |

**Note for Jeremy:** `expected_cash_cents` = `opening_cash_cents` + total cash sales during shift – cash refunds – paid out. The -$17.40 on CDS-003 is what triggers alert ALC-003. Seed this as the computed value; the system derives it from transaction records if Square sync is wired.

### Cash Drawer Events

**Table: `cash_drawer_events`** (individual events inside a shift)

| event_id | shift_id | event_type | employee_id | timestamp | amount_cents | notes |
|---|---|---|---|---|---|---|
| `CDE-001` | `CDS-001` | OPEN | `emp_002` | 2026-02-26 06:30 | 20000 | Opening count |
| `CDE-002` | `CDS-001` | NO_SALE | `emp_005` | 2026-02-26 15:30 | 0 | No-sale #1 (Cody) |
| `CDE-003` | `CDS-001` | NO_SALE | `emp_005` | 2026-02-26 16:45 | 0 | No-sale #2 (Cody) |
| `CDE-004` | `CDS-001` | NO_SALE | `emp_005` | 2026-02-26 17:45 | 0 | No-sale #3 (Cody) |
| `CDE-005` | `CDS-001` | NO_SALE | `emp_005` | 2026-02-26 19:00 | 0 | No-sale #4 (Cody) — HIGH_NO_SALE_FREQUENCY FIRES |
| `CDE-006` | `CDS-001` | CLOSE | `emp_005` | 2026-02-26 21:00 | 18750 | Closing count |
| `CDE-007` | `CDS-003` | OPEN | `emp_002` | 2026-02-28 06:30 | 22500 | Opening count |
| `CDE-008` | `CDS-003` | CLOSE | `emp_003` | 2026-02-28 21:45 | 21260 | Closing count — short $17.40 |

---

## 6. Transaction History

**Table: `transactions`** + **`transaction_line_items`**

49 records total across 5 days: 39 SALE, 5 RETURN, 1 VOID, 4 NO_SALE.

> **Pricing reference (specialty coffee, South Bay market):**
> Drip Coffee $3.75–4.25 | Latte $6.25–6.75 | Cappuccino $5.75 | Flat White $6.00 | Cold Brew $5.75 | Americano $4.50 | Espresso $3.50 | Matcha Latte $6.50 | Croissant $4.25 | Muffin $3.75 | Avocado Toast $11.50 | Breakfast Sandwich $9.75 | Retail Beans 12oz $22.00

**Field key:** All `amount_cents` values include card tip where noted. Cash transactions have no tip.

---

### Thursday, February 26

| txn_id | time | type | employee_id | items | amount_cents | tender | tip_cents | notes |
|---|---|---|---|---|---|---|---|---|
| `TXN-001` | 07:02 | SALE | `emp_002` | 2x Drip Coffee, 1x Croissant | 1400 | CARD | 200 | Morning rush |
| `TXN-002` | 07:08 | SALE | `emp_004` | 1x Latte (L), 1x Espresso | 1175 | CARD | 150 | |
| `TXN-003` | 07:31 | SALE | `emp_002` | 1x Cappuccino, 1x Avocado Toast | 2050 | CARD | 300 | |
| `TXN-004` | 08:05 | SALE | `emp_004` | 1x Matcha Latte, 1x Croissant | 1075 | CASH | 0 | |
| `TXN-005` | 08:22 | SALE | `emp_002` | 3x Drip Coffee, 2x Breakfast Sandwich | 3650 | CARD | 500 | Group order |
| `TXN-006` | 09:15 | SALE | `emp_004` | 1x Flat White | 700 | CARD | 100 | |
| `TXN-007` | 10:30 | SALE | `emp_002` | 1x Retail Beans (12oz) | 2200 | CARD | 0 | |
| `TXN-008` | 11:15 | SALE | `emp_004` | 1x Latte, 1x Muffin | 1025 | CARD | 0 | |
| `TXN-009` | 14:05 | SALE | `emp_005` | 1x Cold Brew, 1x Avocado Toast | 1925 | CARD | 200 | Cody starts PM |
| `TXN-010` | 15:30 | NO_SALE | `emp_005` | — | 0 | — | 0 | **No-sale #1** |
| `TXN-011` | 16:15 | SALE | `emp_005` | 1x Latte | 675 | CASH | 0 | |
| `TXN-012` | 16:45 | NO_SALE | `emp_005` | — | 0 | — | 0 | **No-sale #2** |
| `TXN-013` | 17:30 | SALE | `emp_005` | 1x Americano | 550 | CARD | 100 | |
| `TXN-014` | 17:45 | NO_SALE | `emp_005` | — | 0 | — | 0 | **No-sale #3** |
| `TXN-015` | 18:15 | SALE | `emp_005` | 1x Drip Coffee, 1x Croissant | 800 | CARD | 0 | |
| `TXN-016` | 19:00 | NO_SALE | `emp_005` | — | 0 | — | 0 | **No-sale #4 → HIGH_NO_SALE_FREQUENCY FIRES** |
| `TXN-017` | 20:30 | SALE | `emp_005` | 1x Cold Brew | 575 | CARD | 0 | |

---

### Friday, February 27

| txn_id | time | type | employee_id | items | amount_cents | tender | tip_cents | notes |
|---|---|---|---|---|---|---|---|---|
| `TXN-018` | 07:05 | SALE | `emp_002` | 1x Latte, 1x Croissant | 1250 | CARD | 200 | |
| `TXN-019` | 07:18 | SALE | `emp_004` | 1x Espresso, 1x Muffin | 850 | CARD | 100 | |
| `TXN-020` | 07:35 | SALE | `emp_002` | 1x Cold Brew | 575 | CARD | 0 | |
| `TXN-021` | 08:10 | SALE | `emp_004` | 2x Cappuccino, 1x Avocado Toast | 2725 | CARD | 400 | |
| `TXN-022` | 08:45 | SALE | `emp_002` | 1x Retail Beans (12oz) | 2200 | CARD | 0 | |
| `TXN-023` | 09:20 | SALE | `emp_004` | 1x Flat White | 600 | CASH | 0 | |
| `TXN-024` | 10:00 | SALE | `emp_002` | 1x Matcha Latte, 1x Breakfast Sandwich | 2125 | CARD | 300 | |
| `TXN-025` | 14:30 | SALE | `emp_003` | 1x Americano, 1x Croissant | 875 | CARD | 0 | Diego starts PM |
| `TXN-026` | 15:45 | RETURN | `emp_003` | 1x Retail Beans (12oz) | -2200 | CARD | 0 | Customer: wrong grind size. Return receipt present. |
| `TXN-027` | 16:15 | SALE | `emp_003` | 1x Latte | 725 | CARD | 100 | |
| `TXN-028` | 16:30 | VOID | `emp_003` | 2x Drip Coffee | -850 | VOID | 0 | Customer said wrong order. Voided before close. |
| `TXN-029` | 19:30 | SALE | `emp_003` | 1x Cold Brew, 1x Muffin | 1100 | CARD | 150 | |

---

### Saturday, February 28

| txn_id | time | type | employee_id | items | amount_cents | tender | tip_cents | notes |
|---|---|---|---|---|---|---|---|---|
| `TXN-030` | 06:35 | SALE | `emp_002` | 2x Latte, 1x Avocado Toast | 2900 | CARD | 400 | Rosa opens |
| `TXN-031` | 07:00 | SALE | `emp_001` | 1x Drip Coffee, 2x Croissant | 1175 | CASH | 0 | Alex on floor |
| `TXN-032` | 07:22 | SALE | `emp_007` | 1x Cold Brew, 1x Breakfast Sandwich | 1850 | CARD | 300 | Jake starts |
| `TXN-033` | 08:10 | SALE | `emp_002` | 2x Cappuccino | 1350 | CARD | 200 | |
| `TXN-034` | 08:30 | SALE | `emp_007` | 1x Matcha Latte, 1x Muffin | 1025 | CARD | 0 | |
| `TXN-035` | 09:00 | SALE | `emp_001` | 1x Retail Beans (12oz) | 2200 | CARD | 0 | Alex sells beans |
| `TXN-036` | 09:30 | SALE | `emp_002` | 1x Flat White, 1x Croissant | 1025 | CASH | 0 | |
| `TXN-037` | 10:15 | SALE | `emp_007` | 1x Americano, 1x Avocado Toast | 1900 | CARD | 300 | |
| `TXN-038` | 15:30 | SALE | `emp_003` | 1x Latte | 775 | CARD | 100 | Diego takes over |
| `TXN-039` | 17:00 | RETURN | `emp_003` | 1x Americano | -450 | CARD | 0 | ⚠️ No manager present. Customer: wrong size. No receipt. Refund #1 of 4. |
| `TXN-040` | 17:15 | SALE | `emp_003` | 1x Cold Brew, 1x Retail Beans | 3175 | CARD | 400 | |
| `TXN-041` | 18:15 | RETURN | `emp_003` | 1x Drip Coffee | -375 | CARD | 0 | ⚠️ No manager. Customer "changed mind" — no receipt. Refund #2 of 4. |
| `TXN-042` | 18:45 | RETURN | `emp_003` | 1x Latte | -675 | CARD | 0 | ⚠️ No manager. "Drink was wrong." No receipt. Refund #3 of 4. |
| `TXN-043` | 19:45 | RETURN | `emp_003` | 1x Cold Brew | -575 | CARD | 0 | ⚠️ No manager. "Wrong drink." No receipt. Refund #4 → **HIGH_REFUND_FREQUENCY FIRES** |
| `TXN-044` | 20:00 | SALE | `emp_003` | 1x Americano | 450 | CASH | 0 | |
| `TXN-045` | 20:30 | SALE | `emp_003` | 2x Drip Coffee | 850 | CARD | 0 | |

> **Sat close note:** Diego counts drawer at 21:45. Expected $230.00. Actual $212.60. Short $17.40. See CDS-003.

---

### Sunday, March 1

| txn_id | time | type | employee_id | items | amount_cents | tender | tip_cents | notes |
|---|---|---|---|---|---|---|---|---|
| `TXN-046` | 08:15 | SALE | `emp_006` | 1x Latte, 1x Croissant | 1250 | CARD | 200 | Marisol opens |
| `TXN-047` | 09:00 | SALE | `emp_001` | 1x Flat White, 1x Retail Beans | 2800 | CARD | 0 | Alex on floor |
| `TXN-048` | 10:30 | SALE | `emp_007` | 1x Cold Brew, 1x Muffin | 950 | CARD | 0 | |
| `TXN-049` | 11:15 | SALE | `emp_001` | 2x Cappuccino, 2x Breakfast Sandwich | 3650 | CARD | 500 | Family group |
| `TXN-050` | 12:00 | SALE | `emp_007` | 1x Drip Coffee | 375 | CASH | 0 | |
| `TXN-051` | 13:00 | SALE | `emp_001` | 1x Americano, 1x Croissant | 875 | CARD | 0 | Alex's last sale |

> **Sunday Chirp action:** Alex resolves HIGH_REFUND_FREQUENCY Chirp at 10:15am via Process 3 wizard. Resolution note: "Reviewed all 4 refunds from Diego's Sat shift. 3 are customer complaint-plausible. 1 unclear. Spoke with Diego — coaching conversation scheduled for Tuesday. Not flagging to Fox at this time." Chirp status → RESOLVED.

---

### Monday, March 3 (Demo Day — Morning)

| txn_id | time | type | employee_id | items | amount_cents | tender | tip_cents | notes |
|---|---|---|---|---|---|---|---|---|
| `TXN-052` | 06:55 | SALE | `emp_002` | 1x Drip Coffee, 1x Croissant | 900 | CARD | 100 | Rosa's first sale |
| `TXN-053` | 07:10 | SALE | `emp_004` | 2x Latte | 1600 | CARD | 250 | Priya starts |
| `TXN-054` | 07:25 | SALE | `emp_002` | 1x Cold Brew, 1x Breakfast Sandwich | 1750 | CARD | 200 | |

---

## 7. Active Chirps (Today's View — Monday, March 3)

**Table: `alerts`** (Chirps are alerts in the CRDM)

These are what the merchant sees when they open Today's View on Monday morning.

### Chirp 1 — HERO (🔴 Red)

| Field | Value |
|-------|-------|
| alert_id | `ALC-003` |
| merchant_id | `demo_merch_lighthouse_001` |
| location_id | `demo_loc_lighthouse_pch` |
| chirp_code | `CASH_VARIANCE_THRESHOLD` |
| severity | RED |
| fired_at | 2026-02-28 21:50 |
| linked_employee_id | `emp_003` (Diego Chen — closer) |
| linked_shift_id | `CDS-003` |
| variance_amount_cents | -1740 |
| status | ACTIVE |
| resolved_at | NULL |
| resolved_by | NULL |

> **UI copy (hero banner):** "Drawer short $17.40 at Lighthouse Coffee — 4 min wizard"
> **Demo narrative:** Diego closed Saturday's drawer $17.40 short. Alex hasn't addressed it yet. This is the one we walk through with Process 4.

---

### Chirp 2 — SECONDARY (🟡 Yellow)

| Field | Value |
|-------|-------|
| alert_id | `ALC-001` |
| merchant_id | `demo_merch_lighthouse_001` |
| location_id | `demo_loc_lighthouse_pch` |
| chirp_code | `HIGH_NO_SALE_FREQUENCY` |
| severity | YELLOW |
| fired_at | 2026-02-26 19:05 |
| linked_employee_id | `emp_005` (Cody Walsh) |
| no_sale_count | 4 |
| shift_id | `CDS-001` |
| status | ACTIVE |
| resolved_at | NULL |
| resolved_by | NULL |

> **UI copy (Chirp peek):** "+1 more: High no-sale frequency — Cody Walsh, Thu shift"
> **Demo narrative:** Cody opened the drawer 4 times without a transaction on Thursday afternoon. Alex noticed but hasn't resolved it yet.

---

### Chirp 3 — RESOLVED (🟢 Green, from yesterday)

| Field | Value |
|-------|-------|
| alert_id | `ALC-002` |
| merchant_id | `demo_merch_lighthouse_001` |
| location_id | `demo_loc_lighthouse_pch` |
| chirp_code | `HIGH_REFUND_FREQUENCY` |
| severity | YELLOW |
| fired_at | 2026-02-28 19:55 |
| linked_employee_id | `emp_003` (Diego Chen) |
| refund_count | 4 |
| status | RESOLVED |
| resolved_at | 2026-03-01 10:15 |
| resolved_by | `emp_001` (Alex Navarro) |
| resolution_note | `Reviewed all 4 refunds from Diego's Saturday shift. 3 plausible customer complaints. 1 unclear — flagged for coaching. Not escalating to Fox at this time.` |

> **Demo narrative:** This was yesterday's alert. Alex handled it. The green checkmark shows the system works — it catches things AND lets you close them out.

---

## 8. Scorecard Data

**Minimal placeholder — enough to show the health bar isn't empty.**

**Table: `daily_shrink_scores`** (or equivalent scorecard table)

| date | merchant_id | location_id | shrink_score | trend | open_alerts | resolved_alerts | notes |
|---|---|---|---|---|---|---|---|
| 2026-02-26 | demo | demo_loc | 82 | neutral | 1 | 0 | No-sale Chirp active |
| 2026-02-27 | demo | demo_loc | 79 | down | 1 | 0 | Refund + void logged |
| 2026-02-28 | demo | demo_loc | 58 | down | 3 | 0 | Bad Saturday — variance + high refunds |
| 2026-03-01 | demo | demo_loc | 88 | up | 2 | 1 | Sunday clean. High_refund resolved. |
| 2026-03-03 | demo | demo_loc | 71 | neutral | 2 | 0 | Demo day AM — 2 active Chirps remain |

**Health bar target for demo:** Score of 71 with upward trend since Saturday. Merchant should feel like "things are getting better, but there's still work to do." That's a real feeling.

---

## 9. Product Reference Map (for Today's View)

What Today's View should display when Alex opens the app Monday morning:

| Element | Value | Source |
|---------|-------|--------|
| Greeting | "Good morning, Alex — 2 Chirps need you" | `emp_001.first_name` + active alert count |
| Canary avatar | Green idle pulse | 0 critical issues from THIS morning (drawer is open and balanced so far) |
| Hero Chirp banner | "Drawer short $17.40 at Lighthouse Coffee — 4 min wizard" | ALC-003 |
| Chirp peek | "+1 more: High no-sale frequency — Cody Walsh, Thu shift ›" | ALC-001 |
| Health bar | ~71/100, upward trend arrow | Daily shrink score |
| Action cards (max 3) | "Count the Drawer" (Bull) · "Check Today's Shrink" (Canary) · "Review Cody's Shift" (Rooster) | AM Monday, owner context |
| Resolved Chirp visibility | ALC-002 visible in Chirps tab as resolved (green checkmark, timestamp) | Yesterday's resolution |

> **Section label:** "Your morning" (AM time-of-day awareness)

---

## 10. SQL / JSON Notes for Jeremy

1. **Timestamps:** All times are PT (America/Los_Angeles). Store as UTC in the database, display in PT for the demo.
2. **Amount fields:** All monetary values are in **cents** (integer). The UI converts to dollars. `cash_variance_cents = -1740` = short $17.40.
3. **Chirp fire logic:** If using seed data only (no live Chirp engine), insert the alert records directly with `status = 'ACTIVE'`. The Today's View reads from the `alerts` table, so this will work without the engine.
4. **NO_SALE transactions:** Can be seeded as `transaction_type = 'NO_SALE'` with `amount_cents = 0`. These are the records that power the HIGH_NO_SALE_FREQUENCY Chirp.
5. **Resolved Chirp:** ALC-002 should have `status = 'RESOLVED'`, `resolved_at` timestamp, and `resolved_by = emp_001`. It should appear in the Chirps tab history with a green state, not in the hero.
6. **Demo flag:** Consider adding a `is_demo_seed = true` column or a separate `demo_merchants` table so this data can be cleared cleanly post-Monday.
7. **Tip amounts:** For simplicity, `tip_cents` can be included in `total_amount_cents` OR tracked separately depending on your schema. The CRDM has both tenders and line items — clarify with the tender fields.

---

*Jim — QA Manager & CSM*
*Canary LP | Confidential*
*February 26, 2026*
