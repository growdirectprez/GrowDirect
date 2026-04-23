---
date: 2026-04-23
type: wiki
tags: [canary, user-guide, alerts, library]
sources:
  - Canary/canary/services/chirp/rule_definitions.py
  - Canary/canary/services/alert_config.py
  - Canary/canary/services/notification_dispatcher.py
authors: [Writer]
reviewers: [PhD, QA]
related:
  - "[[Brain/wiki/canary-detection|Canary Detection Engine (architecture)]]"
  - "[[Brain/projects/Canary|Canary MOC]]"
last-compiled: 2026-04-23
needs-review: 2026-05-07
---

# Canary Alerts — A Plain-English Guide

Canary watches your Square data and flags things that look wrong. Here is every alert it can send, what each one actually means, and how to tune the system so you don't drown in notifications.

## How it works, in thirty seconds

Canary has 37 rules. Each one watches for one specific pattern — a fast refund, a drawer opening after hours, an employee ringing up a sale while clocked out. When a rule sees what it is watching for, it creates an alert. You decide which alerts actually notify you.

**Firing and notifying are two different things.** Every alert is recorded whether or not anyone gets pinged. You can review quietly-recorded alerts in the dashboard anytime. That matters, because the right move for a noisy rule is almost always to silence its notifications — not to turn the rule off. Off-rule means no data; silent rule means data you can look at on your own schedule.

## The rules

### Payment

- **C-001 Rapid Refund** — A sale got refunded within 15 minutes. Classic cash-pocketing pattern.
- **C-002 Excessive Refund Rate** — One employee is refunding a lot more sales than their coworkers.
- **C-003 Round Amount Pattern** — Multiple round-dollar sales back to back. Can signal structuring.
- **C-004 After-Hours Transaction** — A sale went through when the store should have been closed.
- **C-005 Card Velocity** — The same card was used five or more times in an hour. Usually card testing.
- **C-006 Split Tender Pattern** — Sales keep getting split across multiple payment methods.
- **C-007 High-Value Refund** — A single refund over $100.
- **C-008 Manual Entry Spike** — An employee is typing card numbers in by hand more than they should be.
- **C-009 Square Delay Hold** — Square itself flagged this payment as suspicious.
- **C-010 Partial Authorization** — The card was only approved for part of the amount charged.
- **C-011 No-Sale Detected** — Square flagged the payment as a no-sale.

### Cash Drawer

- **C-101 No-Sale Abuse** — The register keeps opening without anyone ringing up a sale.
- **C-102 Cash Variance** — End-of-shift cash was off by more than $20.
- **C-103 Paid-Out Anomaly** — More than $50 paid out of the register without manager approval.
- **C-104 After-Hours Drawer** — Cash drawer opened when the store should have been closed. Critical.

### Orders & Discounts

- **C-201 Excessive Discount Rate** — Average discounts are running over 50%. Sweethearting pattern.
- **C-202 Line-Item Void Rate** — Too many individual items are being removed from orders.
- **C-203 Sweethearting** — An unapproved discount over $20 on a pricier item.
- **C-204 Untendered Order** — An order sat open for a full day with no payment. Critical.

### Timecard

- **C-301 Off-Clock Transaction** — An employee rang up a sale while not clocked in. Critical. Only useful if your timecard data is clean.
- **C-302 Break Transaction** — An employee rang up a sale during their declared break.
- **C-303 Wrong Location** — Employee clocked in at one store but rang up a sale at another.

### Voids

- **C-501 High Void Rate** — Someone voided five or more sales during a shift.
- **C-502 Post-Void** — A completed sale got canceled after the fact. The single most common way retail theft gets hidden. Severity scales with how long after the sale — a cancel 30 seconds later is usually a real correction; a cancel three hours later almost never is.

### Gift Cards

- **C-601 Gift Card Load Velocity** — Several gift cards loaded in a short window. Money-laundering signal.
- **C-602 Gift Card Drain** — A gift card was drained of its full value within 30 minutes of being loaded. Critical.

### Loyalty

- **C-801 Rapid Point Accumulation** — Loyalty points piling up on one account too fast.
- **C-802 Bulk Redemption** — Someone cashed in more than 5,000 points in a single transaction.
- **C-803 Cross-Location Velocity** — Loyalty activity bouncing between three or more locations in two hours.
- **C-804 Enrollment Fraud** — One employee signed up ten or more new members in a single day.

### Chargebacks

- **C-D01 Dispute Created** — A customer filed a chargeback.
- **C-D02 Dispute Lost** — The chargeback ruled against you. The money is going back. Critical.
- **C-D03 Dispute Velocity** — Three or more chargebacks at one location in the last 30 days.

### Invoices

- **C-I01 Invoice Overdue** — An invoice is past its due date.
- **C-I02 Invoice Charge Failed** — A scheduled invoice charge didn't go through.
- **C-I03 High-Value Invoice Unpaid** — An invoice over $500 is unpaid.

### Shrink Summary

- **C-901 Shrink Risk Assessment** — Your estimated shrink is over 3% of sales for the period. A lagging indicator — useful for trends, not for single-case investigations.

## Tuning without drowning

### Three dials, from coarse to fine

1. **Sensitivity preset.** One setting for all rules: Strict, Default, Relaxed, or Minimal. Most new merchants should start on Relaxed.
2. **Rule template.** Pick the one that matches your business: Retail Standard, Food & Beverage, High-Value Retail, High-Volume / Quick Service, or Learning Mode.
3. **Per-rule overrides.** When one rule is noisier or quieter than the rest, adjust just that rule.

### Four ways to control notification volume

- **Daily and hourly caps.** Default 100 per day, 50 per hour. Anything over that lands in the dashboard, not in your pocket.
- **Quiet hours.** Set them to your off-shift window. Critical alerts still record; they just don't interrupt.
- **Severity routing.** Critical and high go real-time. Medium and low go to the daily digest. Adjustable by category.
- **Per-rule notification toggle.** Keep the rule firing; silence the notifications.

## How to onboard without regretting it

Don't turn on all 37 rules on day one. Here is the sequence that works:

- **Week 1.** Relaxed preset, Learning Mode template. Turn on the three refund rules (C-001, C-002, C-007), the after-hours drawer (C-104), and post-void (C-502). Daily digest.
- **Week 2.** Review the week's alerts. If a rule produced too many false positives, raise its threshold or silence its notifications. Add after-hours transactions (C-004) and card velocity (C-005).
- **Week 3.** If your timecard data is clean, turn on off-clock transaction (C-301). Skip it if your timecards are messy — it will produce nothing but false alarms.
- **Weeks 4–6.** Add the structuring rules (C-003, C-006, C-008), discount rules (C-201, C-203), and void rate (C-501), one at a time. One rule per week.
- **After six weeks.** You have enough of your own history to tune the five or six rules that matter most for your shop.

## Rule of thumb

The tool that catches theft is the tool whose alerts you actually read. The tool whose alerts you read is the tool whose alerts are few enough to read. Start narrow. Add one rule at a time. When a rule gets noisy, silence the notification — don't kill the rule.
