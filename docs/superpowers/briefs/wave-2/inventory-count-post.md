---
screen: /inventory/count/:id/post
title: Count Review + Post
role: MGR
wave: W2
origin: N
cp_equivalent: "frmimphysicalcount post — Windows-only, no variance drill-down, no LP linkage"
---

# Count Review + Post

**URL:** `/inventory/count/:id/post`  
**Primary role:** MGR  
**Entry points:** Count entry screen → Complete Count; Count list → Completed count row action

## Layout

| Zone | Content | Notes |
|---|---|---|
| Header | "Post Count: [Count ID] — [Store], [Date]", count type badge | |
| Summary banner | Total variance value ($), variance line count, shrink % | Color-coded: green = near-zero, orange = moderate, red = high |
| Main content | Variance review table | All non-zero-variance lines |
| LP flag section | High-variance items flagged for LP review | Below variance table |
| Action bar | Post Adjustments, Discard Count, Export | |

## Key Elements

### Summary Banner
Three KPIs displayed prominently before posting:
- **Total Variance ($):** Sum of all variance values (absolute). Not net — both shortages and overages counted.
- **Variance Lines:** Count of lines with non-zero variance out of total lines.
- **Shrink %:** Total shortage value ÷ total expected inventory value at cost. The KPI the finance team and LP want to know.

If all variances are zero, the banner shows "No variances — clean count" in green. Post is a one-click confirmation.

### Variance Review Table
Shows only non-zero-variance lines. Columns: Item #, Description, Expected Qty, Entered Qty, Variance Qty, Variance Value ($), Notes (from counter flags).

Sorted by Variance Value descending (largest variances first). MGR reviews before posting. Any line can be expanded to see the counter who entered it and the timestamp of the entry.

### LP Flag Section
Items with Variance Value > configured LP threshold (e.g., $50 shortage on a single line) are surfaced here with a callout: "These variances exceed the LP alert threshold. Posting will generate LP alerts for the following items."

LP is not notified automatically — the section gives MGR visibility that LP notification will happen, so there are no surprises. MGR can add a note before posting ("count discrepancy confirmed, LP investigation already open for this item").

### Post Adjustments Action
Applies inventory adjustments: the perpetual ledger is updated for every line with a non-zero variance. For shortage lines: inventory decreases. For overage lines: inventory increases.

Each adjustment is recorded with a reference to the count ID, so inventory history shows "Physical Count #C-0047" as the reason for the adjustment.

**This action cannot be undone.** A confirmation dialog appears: "Post this count and apply [N] inventory adjustments? This cannot be reversed." MGR must confirm.

After posting, status transitions: Completed → Posted. LP alerts are generated for flagged items.

### Discard Count
Discards the count without applying adjustments. Used if the count is believed to be invalid (e.g., incorrect items scanned, process failure mid-count). Requires reason. Status transitions: Completed → Discarded. A new count must be initiated.

**Empty state:** Not applicable — count exists before reaching this screen.

## Interaction Flows

1. **Clean post:** MGR reviews count → all variances < $5 → no LP flags → clicks Post → confirms → adjustments applied → status = Posted
2. **High-variance review:** Count shows −18 on item #7734 ($216 shortage) → LP flag section highlights it → MGR adds note "LP case #C-0044 already open for this item" → Posts → LP alert generated and links to existing note
3. **Discard bad count:** Counter accidentally scanned items from wrong store location → variance numbers are anomalous → MGR clicks Discard → enters reason "wrong location scanned" → count discarded → new count initiated

## UX Callout

In CP, posting a physical count applies the adjustments in bulk with no pre-post variance summary. The manager clicks Finalize, adjustments are applied, and they find out later (if at all) that a $1,400 shrinkage event was embedded in the count. Canary surfaces the variance summary explicitly before posting — the shrink % and LP flag callout are the moment a manager understands what happened in the count before committing to the ledger. The LP flag section closes the loop between inventory operations and loss prevention: an LP investigator doesn't have to discover the shortage from a report three days later; the alert fires the moment the count is posted.

## Navigation Exits

- `/inventory/count/:id` — back to count entry
- `/inventory/count` — after posting
- `/cases/hawk/new` — from LP flag section if MGR creates case directly

## Open Questions

None.
