---
type: spec
domain: canary
status: active
created: 2026-03-18
updated: 2026-03-19
---
# B-068 Token Registry v1.0
## Complete Token Key Inventory — Canary Generic Frontend Blueprint

**Work Order:** B-068, Lane B
**Date:** February 28, 2026
**Author:** Condor (IP Sanitization)
**Supervised by:** PhD
**Purpose:** Flat registry of every token key in Blueprint v2.0. Input for Lane C (JSON locale/vocabulary packs) and Lane D (Tom's `merchant_vocabulary` DB schema).

---

## Registry Format

| Token Key | Category | Vocabulary-Overridable | Description | Example en-US |
|---|---|---|---|---|

---

## 1. Business-Term Tokens (Vocabulary-Overridable)

These tokens appear in the Settings → Language & Labels page. Merchants can rename them.

| Token Key | Category | Vocab-Overridable | Description | Example en-US |
|---|---|---|---|---|
| `employee.label.singular` | business-term | YES | Singular form of employee entity | Employee |
| `employee.label.plural` | business-term | YES | Plural form of employee entity | Employees |
| `location.label.singular` | business-term | YES | Singular form of location entity | Location |
| `location.label.plural` | business-term | YES | Plural form of location entity | Locations |
| `cash_drawer.label.singular` | business-term | YES | Singular form of cash drawer entity | Cash Drawer |
| `cash_drawer.label.plural` | business-term | YES | Plural form of cash drawer entity | Cash Drawers |
| `transaction.label.singular` | business-term | YES | Singular form of transaction entity | Transaction |
| `transaction.label.plural` | business-term | YES | Plural form of transaction entity | Transactions |
| `void.label.singular` | business-term | YES | Singular form of void entity | Void |
| `void.label.plural` | business-term | YES | Plural form of void entity | Voids |
| `refund.label.singular` | business-term | YES | Singular form of refund entity | Refund |
| `refund.label.plural` | business-term | YES | Plural form of refund entity | Refunds |
| `case.label.singular` | business-term | YES | Singular form of investigation case entity | Case |
| `case.label.plural` | business-term | YES | Plural form of investigation case entity | Cases |
| `chirp.label.singular` | business-term | YES | Singular form of alert entity (default: Alert, not Chirp) | Alert |
| `chirp.label.plural` | business-term | YES | Plural form of alert entity | Alerts |
| `shift.label.singular` | business-term | YES | Singular form of shift entity | Shift |
| `shift.label.plural` | business-term | YES | Plural form of shift entity | Shifts |
| `tender.label.singular` | business-term | YES | Singular form of tender/payment entity | Tender |
| `tender.label.plural` | business-term | YES | Plural form of tender/payment entity | Tenders |
| `store.label.singular` | business-term | YES | Singular form of store reference | Store |
| `store.label.plural` | business-term | YES | Plural form of store reference | Stores |
| `drawer.label.singular` | business-term | YES | Short form of cash drawer | Drawer |
| `drawer.label.plural` | business-term | YES | Short form of cash drawer plural | Drawers |
| `discount.label.singular` | business-term | YES | Singular form of discount entity | Discount |
| `discount.label.plural` | business-term | YES | Plural form of discount entity | Discounts |
| `exchange.label.singular` | business-term | YES | Singular form of exchange entity | Exchange |
| `exchange.label.plural` | business-term | YES | Plural form of exchange entity | Exchanges |
| `variance.label.singular` | business-term | YES | Singular form of variance | Variance |
| `shrink.label.singular` | business-term | YES | Singular form of shrinkage | Shrink |
| `investigation.label.singular` | business-term | YES | Singular form of investigation | Investigation |
| `investigation.label.plural` | business-term | YES | Plural form of investigation | Investigations |

---

## 2. Companion / Today's View Tokens

| Token Key | Category | Vocab-Overridable | Description | Example en-US |
|---|---|---|---|---|
| `companion.today.greeting.morning` | companion-ui | NO | Morning greeting prefix | Good morning |
| `companion.today.greeting.afternoon` | companion-ui | NO | Afternoon greeting prefix | Good afternoon |
| `companion.today.greeting.evening` | companion-ui | NO | Evening greeting prefix | Good evening |
| `companion.today.chirp_count.singular` | companion-ui | NO | Chirp count label (singular) | {count} {chirp.label.singular} needs you |
| `companion.today.chirp_count.plural` | companion-ui | NO | Chirp count label (plural) | {count} {chirp.label.plural} need you |
| `companion.today.chirp_count.zero` | companion-ui | NO | Zero chirps message | Nothing needs your attention right now. |
| `companion.today.section.morning` | companion-ui | NO | Morning action section label | Your morning |
| `companion.today.section.afternoon` | companion-ui | NO | Afternoon action section label | Your afternoon |
| `companion.today.section.evening` | companion-ui | NO | Evening action section label | Your evening |
| `companion.today.section.week` | companion-ui | NO | Friday/weekly section label | This week |

---

## 3. Chirp UI Tokens

| Token Key | Category | Vocab-Overridable | Description | Example en-US |
|---|---|---|---|---|
| `chirp.severity.critical.label` | chirp-ui | NO | Critical severity display label | Critical |
| `chirp.severity.high.label` | chirp-ui | NO | High severity display label | Urgent |
| `chirp.severity.medium.label` | chirp-ui | NO | Medium severity display label | Attention |
| `chirp.severity.low.label` | chirp-ui | NO | Low severity display label | Notice |
| `chirp.hero.cta.label` | chirp-ui | NO | Hero banner call-to-action button | Fix this → |
| `chirp.hero.time.label` | chirp-ui | NO | Wizard time estimate label | {minutes} min wizard |
| `chirp.peek.more.label` | chirp-ui | NO | Chirp peek indicator prefix | +{count} more: |
| `chirp.list.active.heading` | chirp-ui | NO | Active chirps list heading | Active |
| `chirp.list.resolved.heading` | chirp-ui | NO | Resolved chirps list heading | Resolved |

---

## 4. Navigation Tokens

| Token Key | Category | Vocab-Overridable | Description | Example en-US |
|---|---|---|---|---|
| `nav.tab.home.label` | nav-ui | NO | Home tab label | Home |
| `nav.tab.insights.label` | nav-ui | NO | Insights tab label (owner only) | Insights |
| `nav.tab.investigate.label` | nav-ui | NO | Investigate tab label (owner only) | Investigate |
| `nav.tab.inventory.label` | nav-ui | NO | Inventory tab label | Inventory |
| `nav.tab.daily.label` | nav-ui | NO | Daily operations tab label | Daily |
| `nav.tab.money.label` | nav-ui | NO | Money tab label (owner + manager) | Money |

---

## 5. Wizard — Shared Tokens

| Token Key | Category | Vocab-Overridable | Description | Example en-US |
|---|---|---|---|---|
| `wizard.progress.label` | wizard-ui | NO | Step progress indicator | Step {current} of {total} |
| `wizard.nav.back.label` | wizard-ui | NO | Back button label | Back |
| `wizard.nav.next.label` | wizard-ui | NO | Next button label | Next |
| `wizard.nav.confirm.label` | wizard-ui | NO | Confirm button label | Confirm |
| `wizard.nav.skip.label` | wizard-ui | NO | Skip button label | Skip |
| `wizard.nav.done.label` | wizard-ui | NO | Done button label | Done |

---

## 6. Process 1 — Open the Store

| Token Key | Category | Vocab-Overridable | Description | Example en-US |
|---|---|---|---|---|
| `process.open_store.title` | process-ui | NO | Process title | Open the Store |
| `process.open_store.step1.title` | process-ui | NO | Step 1 title | Verify Store Ready |
| `process.open_store.step1.description` | process-ui | NO | Step 1 instruction text | Check each item to confirm readiness. |
| `process.open_store.step1.item.lights` | process-ui | NO | Checklist item: lights | Lights on |
| `process.open_store.step1.item.register` | process-ui | NO | Checklist item: register | Register powered |
| `process.open_store.step1.item.signage` | process-ui | NO | Checklist item: signage | Signage visible |
| `process.open_store.step2.title` | process-ui | NO | Step 2 title | Open Cash Drawer |
| `process.open_store.step2.prompt` | process-ui | NO | Step 2 prompt | Count your starting cash |
| `process.open_store.step2.validation.zero_warning` | process-ui | NO | Zero amount warning | Starting with $0.00 — are you sure? |
| `process.open_store.step3.title` | process-ui | NO | Step 3 title | Confirm Opening |
| `process.open_store.step3.summary` | process-ui | NO | Step 3 summary template | {location.label.singular} opening with {amount} in {drawer.label.singular} |
| `process.open_store.step4.title` | process-ui | NO | Step 4 title | Done |
| `process.open_store.step4.message` | process-ui | NO | Completion message | Store is open! |
| `process.open_store.error.already_open` | process-ui | NO | Already-open error | {location.label.singular} is already open |

---

## 7. Process 2 — Count the Drawer

| Token Key | Category | Vocab-Overridable | Description | Example en-US |
|---|---|---|---|---|
| `process.count_drawer.title` | process-ui | NO | Process title | Count the Drawer |
| `process.count_drawer.step1.title` | process-ui | NO | Step 1 title | Select Drawer |
| `process.count_drawer.step1.expected_label` | process-ui | NO | Expected cash label | Expected cash |
| `process.count_drawer.step2.title` | process-ui | NO | Step 2 title | Enter Actual Count |
| `process.count_drawer.step3.title` | process-ui | NO | Step 3 title | Variance Check |
| `process.count_drawer.step3.balanced` | process-ui | NO | Balanced confirmation | Balanced — no variance detected. |
| `process.count_drawer.step3.variance.warning` | process-ui | NO | Moderate variance warning | Variance detected — review recommended. |
| `process.count_drawer.step3.variance.critical` | process-ui | NO | Severe variance warning | Significant variance — investigate. |
| `process.count_drawer.step4.title` | process-ui | NO | Step 4 title | Document & Close |
| `process.count_drawer.step4.notes_prompt` | process-ui | NO | Notes field prompt | Explain the variance |
| `process.count_drawer.step4.photo_prompt` | process-ui | NO | Photo upload prompt | Attach count sheet photo (optional) |
| `process.count_drawer.step5.title` | process-ui | NO | Step 5 title | Done |
| `process.count_drawer.step5.balanced` | process-ui | NO | Balanced completion | Perfect count! Drawer balanced. |
| `process.count_drawer.step5.variance` | process-ui | NO | Variance completion | Variance noted. Keep an eye on it. |
| `process.count_drawer.step5.critical` | process-ui | NO | Critical variance completion | Significant variance — consider investigating. |
| `process.count_drawer.error.no_open` | process-ui | NO | No open drawers message | No open drawers to count |
| `process.count_drawer.error.already_closed` | process-ui | NO | Already closed message | This drawer was closed by {employee_name} at {time} |

---

## 8. Process 3 — Resolve Refund Alert

| Token Key | Category | Vocab-Overridable | Description | Example en-US |
|---|---|---|---|---|
| `process.refund_alert.title` | process-ui | NO | Process title | Resolve Refund Alert |
| `process.refund_alert.step1.title` | process-ui | NO | Step 1 title | Review the Facts |
| `process.refund_alert.step2.title` | process-ui | NO | Step 2 title | Examine Individual Refunds |
| `process.refund_alert.step3.title` | process-ui | NO | Step 3 title | Assess the Situation |
| `process.refund_alert.step3.option.legitimate` | process-ui | NO | Legitimate assessment option | All legitimate — busy day with returns |
| `process.refund_alert.step3.option.questionable` | process-ui | NO | Questionable assessment option | Some look questionable |
| `process.refund_alert.step3.option.suspicious` | process-ui | NO | Suspicious assessment option | This is suspicious — investigate further |
| `process.refund_alert.step3.option.escalate` | process-ui | NO | Escalation button (owner only) | Escalate for formal investigation |
| `process.refund_alert.step3.manager_guidance` | process-ui | NO | Manager guidance for suspicious | Talk to the store owner about this. |
| `process.refund_alert.step4.title` | process-ui | NO | Step 4 title | Take Action |
| `process.refund_alert.step5.title` | process-ui | NO | Step 5 title | Done |
| `process.refund_alert.step5.legitimate` | process-ui | NO | Legitimate completion | All clear — refund pattern explained. |
| `process.refund_alert.step5.escalated` | process-ui | NO | Escalated completion | Flagged for investigation. |

---

## 9. Process 4 — Resolve Cash Drawer Shortage

| Token Key | Category | Vocab-Overridable | Description | Example en-US |
|---|---|---|---|---|
| `process.shortage.title` | process-ui | NO | Process title | Resolve Cash Drawer Shortage |
| `process.shortage.step1.title` | process-ui | NO | Step 1 title | Confirm the Fact |
| `process.shortage.step1.prompt` | process-ui | NO | Step 1 prompt template | Was the drawer actually short {amount}? |
| `process.shortage.step1.option.yes` | process-ui | NO | Yes option | Yes, the drawer was short |
| `process.shortage.step1.option.no` | process-ui | NO | No option | No, it was a false alarm |
| `process.shortage.step2.title` | process-ui | NO | Step 2 title | Who Touched It Last? |
| `process.shortage.step2.prompt` | process-ui | NO | Step 2 prompt | Select who last worked this drawer |
| `process.shortage.step2.no_data` | process-ui | NO | No timecard data fallback | No timecard data available — you can enter a name manually |
| `process.shortage.step3.title` | process-ui | NO | Step 3 title | What Might Have Happened? |
| `process.shortage.step3.prompt` | process-ui | NO | Step 3 prompt | Select the most likely cause |
| `process.shortage.step3.cause.refund` | process-ui | NO | Cause: missed refund | Forgot to ring up a refund |
| `process.shortage.step3.cause.math` | process-ui | NO | Cause: math error | Math error during count |
| `process.shortage.step3.cause.theft` | process-ui | NO | Cause: suspected theft | Suspected theft |
| `process.shortage.step3.cause.other` | process-ui | NO | Cause: other | Something else |
| `process.shortage.step3.option.escalate` | process-ui | NO | Escalation button (owner only) | Escalate for formal investigation |
| `process.shortage.step4.title` | process-ui | NO | Step 4 title | Fix It Now |
| `process.shortage.step5.title` | process-ui | NO | Step 5 title | Learn & Prevent |
| `process.shortage.step5.playbook_toggle` | process-ui | NO | Playbook toggle label | Add to team playbook |
| `process.shortage.step6.title` | process-ui | NO | Step 6 title | Done |
| `process.shortage.step6.resolved` | process-ui | NO | Resolved completion | Great job — shrink prevented. |
| `process.shortage.step6.false_alarm` | process-ui | NO | False alarm completion | False alarm — glad to hear it! |
| `process.shortage.step6.escalated` | process-ui | NO | Escalated completion | Case opened — investigation started. |

---

## 10. Scorecard Tokens

| Token Key | Category | Vocab-Overridable | Description | Example en-US |
|---|---|---|---|---|
| `scorecard.shrink.headline_label` | scorecard-ui | NO | Daily shrink score label | Today's estimated shrinkage |
| `scorecard.shrink.action.label` | scorecard-ui | NO | Shrink scorecard action button | See details |
| `scorecard.alerts.headline_label` | scorecard-ui | NO | Alert heatmap label | this week |
| `scorecard.team.headline_label` | scorecard-ui | NO | Team performance label | Team performance |
| `scorecard.inventory.headline_label` | scorecard-ui | NO | Inventory health label | Inventory health |
| `scorecard.treasury.headline_label` | scorecard-ui | NO | Treasury snapshot label | Treasury snapshot |
| `scorecard.trend.up` | scorecard-ui | NO | Trend direction: up | ↑ |
| `scorecard.trend.down` | scorecard-ui | NO | Trend direction: down | ↓ |
| `scorecard.trend.stable` | scorecard-ui | NO | Trend direction: stable | → |
| `scorecard.trend.comparison` | scorecard-ui | NO | Trend comparison template | vs. {period} |

---

## 11. Error State Tokens

| Token Key | Category | Vocab-Overridable | Description | Example en-US |
|---|---|---|---|---|
| `error.offline.message` | error-ui | NO | Network offline message | You're offline — we'll refresh when you're back. |
| `error.server.message` | error-ui | NO | Server error message | Taking a moment. Try again shortly. |
| `error.wizard_step.message` | error-ui | NO | Wizard step load failure | This step couldn't load. Tap to retry. |
| `error.photo_upload.message` | error-ui | NO | Photo upload failure | Photo didn't upload. You can try again or skip for now. |
| `error.permission.message` | error-ui | NO | Role permission denied | This area is for store owners. Talk to {owner_name} if you need access. |
| `error.session.message` | error-ui | NO | Session expired | Please log in again to continue. |
| `error.missing_data.message` | error-ui | NO | Missing data fallback | We don't have {data_type} data for today. You can still complete this step manually. |
| `error.retry.label` | error-ui | NO | Retry button label | Try again |

---

## 12. Shared / Brand Tokens

| Token Key | Category | Vocab-Overridable | Description | Example en-US |
|---|---|---|---|---|
| `brand.wordmark` | brand | NO | Application wordmark | CANARY |
| `shared.action.fix` | shared-ui | NO | Generic fix action | Fix this |
| `shared.action.details` | shared-ui | NO | Generic details action | See details |
| `shared.action.retry` | shared-ui | NO | Generic retry action | Try again |
| `shared.action.cancel` | shared-ui | NO | Generic cancel action | Cancel |
| `shared.action.confirm` | shared-ui | NO | Generic confirm action | Confirm |
| `shared.status.loading` | shared-ui | NO | Loading indicator text | Loading... |
| `shared.photo.optional` | shared-ui | NO | Optional photo label | Optional |

---

## 13. Theme Tokens (Design System)

These tokens replace hardcoded hex colors and font names in v2.0. Not vocabulary-overridable — they belong to the Theme Pack JSON.

| Token Key | Category | Vocab-Overridable | Description | v1.0 Default |
|---|---|---|---|---|
| `theme.color.ink` | theme | NO | Primary background | #0D1117 |
| `theme.color.card` | theme | NO | Card surface | #161B22 |
| `theme.color.border` | theme | NO | Card/divider border | #21262D |
| `theme.color.signal_yellow` | theme | NO | Primary accent, CTA buttons | #FBBF24 |
| `theme.color.accent_gold` | theme | NO | CTA hover, mascot wing | #F59E0B |
| `theme.color.deep_amber` | theme | NO | Mascot depth detail | #D97706 |
| `theme.color.beak_gold` | theme | NO | Mascot beak accent | #E8A317 |
| `theme.color.health_green` | theme | NO | All-clear / positive | #059669 |
| `theme.color.health_yellow` | theme | NO | Caution / mid-severity | #FBBF24 |
| `theme.color.health_red` | theme | NO | Critical / urgent | #EF4444 |
| `theme.color.text_primary` | theme | NO | Primary text on dark | #E5E7EB |
| `theme.color.text_muted` | theme | NO | Secondary text | #6B7280 |
| `theme.color.text_dim` | theme | NO | Tertiary text, inactive nav | #4B5563 |
| `theme.color.module.rooster` | theme | NO | Rooster module tint | rgba(251, 191, 36, 0.12) |
| `theme.color.module.bull` | theme | NO | Bull module tint | rgba(5, 150, 105, 0.12) |
| `theme.color.module.fox` | theme | NO | Fox module tint | rgba(239, 68, 68, 0.12) |
| `theme.color.module.canary` | theme | NO | Canary module tint | rgba(245, 158, 11, 0.12) |
| `theme.color.module.owl` | theme | NO | Owl module tint | rgba(99, 102, 241, 0.12) |
| `theme.color.module.goose` | theme | NO | Goose module tint | rgba(6, 182, 212, 0.12) |
| `theme.font.display` | theme | NO | Display / wordmark font | Space Grotesk |
| `theme.font.heading` | theme | NO | Heading / card title font | Space Grotesk |
| `theme.font.body` | theme | NO | Body text font | Inter |
| `theme.font.label` | theme | NO | Label / tag font | Inter |

---

## Registry Summary

| Category | Token Count | Vocabulary-Overridable |
|---|---|---|
| Business-term | 32 | ALL YES |
| Companion-ui | 10 | ALL NO |
| Chirp-ui | 9 | ALL NO |
| Nav-ui | 6 | ALL NO |
| Wizard-ui | 6 | ALL NO |
| Process-ui (P1) | 14 | ALL NO |
| Process-ui (P2) | 17 | ALL NO |
| Process-ui (P3) | 13 | ALL NO |
| Process-ui (P4) | 22 | ALL NO |
| Scorecard-ui | 10 | ALL NO |
| Error-ui | 8 | ALL NO |
| Shared-ui / Brand | 8 | ALL NO |
| Theme | 23 | ALL NO |
| **TOTAL** | **178** | **32 YES / 146 NO** |

---

## Lane C Input Notes

- Lane C produces two JSON outputs per locale: a **Locale Pack** (all non-overridable tokens) and a **Vocabulary Pack** (all 32 vocabulary-overridable tokens with merchant-configurable defaults).
- Token keys in this registry map 1:1 to JSON keys. The namespace dot-separates into nested objects: `chirp.severity.critical.label` → `{ "chirp": { "severity": { "critical": { "label": "Critical" } } } }`.
- Theme tokens produce a separate **Theme Pack** JSON. Theme tokens do NOT appear in locale or vocabulary packs.
- Resolution order (backend): Vocabulary Pack → Locale Pack → en-US default. Frontend receives resolved strings. No frontend resolution logic.

## Lane D Input Notes (Tom)

- The 32 vocabulary-overridable tokens map to rows in Tom's `merchant_vocabulary` table.
- Schema reference: `merchant_id` + `token_key` + `display_value` + `updated_at`.
- Default values for each token_key come from the en-US Locale Pack fallback.

---

*Condor | B-068-B | February 28, 2026*
*"The Blueprint describes structure. The JSON describes language. Never mix them."*
