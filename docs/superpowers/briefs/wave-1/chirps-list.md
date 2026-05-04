---
screen: /chirps
title: Chirp Feed (Live Transaction Feed)
role: LP | MGR
wave: W1
origin: O
cp_equivalent: "Z-Tape (post-close only) — no real-time equivalent"
---

# Chirp Feed

**URL:** `/chirps`  
**Primary role:** LP; secondary: MGR  
**Entry points:** Primary sidebar nav (Surveillance section); alert detail → "View source chirp"

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | Page title "Live Feed", store selector, auto-refresh status, Pause button | Pause stops feed update; useful for reviewing a specific transaction cluster |
| Filter bar | Chirp type, Store, Cashier, Time window (last 1h / 4h / 8h / today) | Filters apply to the live window |
| Main content | Reverse-chronological feed — newest at top | Auto-scrolls unless Paused; user-scroll pauses auto-refresh |
| Feed controls | "Auto-refresh: ON", "Resume live" button (when paused), update frequency display | Top-right of feed |

## Key Elements

### Chirp Feed Rows
Each row: Chirp type badge (SALE / RETURN / VOID / DISCOUNT / COMP / EOD), Store indicator, Terminal ID, Cashier name, Transaction amount, Item count, Timestamp (relative, updating live: "just now" / "2 min ago"). Rows are compact — 2-line height. Click → `/chirps/:id`.

Color-coding on type badge: VOID and COMP rows have a subtle yellow tint to draw LP attention without triggering a full alert. RETURN rows have blue tint. EOD rows have grey tint.

**Empty state:** "No transactions in the selected time window for the selected filters." For stores not yet sending events: "No transactions received from [Store] in the past hour — adapter may be offline."

### Store Selector
Multi-select dropdown. LP can watch all stores simultaneously or focus on one location. Store selector state persists in session. For LP investigators assigned to a subset of stores, only their assigned stores appear in this list.

### Pause / Resume
Pause button stops feed from prepending new rows. LP can scroll the frozen feed without new rows pushing their view. "Resume Live" button returns to top and re-enables live updates. A badge counts new chirps received while paused: "14 new transactions while paused."

### Flag for Review
Each row has a flag icon (appears on hover). Click → marks the chirp for follow-up review without opening the detail. Flags are session-local (not persisted). LP can flag a cluster of suspicious transactions and then investigate them in sequence.

## Interaction Flows

1. **Pre-rule situational awareness:** LP monitors feed → notices cashier J. Martinez has had 3 VOID chirps in 15 minutes → these haven't triggered a rule yet → LP pauses feed → clicks each void chirp → reviews line items → identifies a pattern → opens a case manually from `/cases/hawk`
2. **System health check:** MGR opens chirp feed for their store → confirms transactions are flowing → checks that the chirp count matches expected traffic for the time of day → satisfied that the system is alive
3. **Filter to a specific cashier:** LP is investigating a subject → filters feed to Cashier = [subject] → sees all their transactions for today in real-time → flags suspicious ones for deeper review

## UX Callout

The chirp feed is Canary's fundamental departure from Counterpoint's observability model. CP operators are blind until the Z-tape prints at end of day. Canary operators see every transaction as it posts — before any rule fires, before any alert generates. This is pre-rule situational awareness: the ability to see a pattern forming before it becomes an alert. For experienced LP investigators, this early visibility is often where the best catches come from — a human eye detecting intent before the algorithm catches the pattern.

## Navigation Exits

- `/chirps/:id` — chirp detail for any row
- `/cases/hawk` — if LP opens a case from a chirp pattern
- `/rules` — to check if a pattern should have triggered a rule but didn't

## Open Questions

None.
