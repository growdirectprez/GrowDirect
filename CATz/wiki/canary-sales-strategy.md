---
date: 2026-04-10
type: wiki
status: active
tags: [canary, sales, strategy, detection-rules, merchants, go-to-market]
sources: [docs/_archive/ip-vault/Canary/Strategy/Gold List — Top 8 Detection Rules.md]
last-compiled: 2026-04-10
needs-review: 2026-07-10
----

# Canary Sales Strategy

## Summary

Canary's go-to-market is built around 8 "gold list" detection rules that produce undeniable, merchant-friendly alerts. The strategy is to sell outcomes ("here's the $200 your cashier walked out with"), not technology. The adoption ladder moves merchants from proof → monitoring → tuning → prediction, with each step feeling natural and never requiring the word "AI."

## The Gold List — 8 Rules That Sell Themselves

These are the rules where a single confirmed hit proves Canary's value. Each one tells a story a merchant instantly understands:

**C-502 POST_VOID** — "Your cashier voided a $200 sale after the customer left with the merchandise." Undeniable. Timestamp proves it. The longer the gap between sale and void, the more suspicious.

**C-301 OFF_CLOCK_TRANSACTION** — "Someone ran a $150 payment and they weren't even clocked in." Ghost employee. No legitimate explanation.

**C-004 AFTER_HOURS_TRANSACTION** — "A $300 sale at 2 AM. You close at 10 PM." One question answers it: "Were you open?"

**C-201 EXCESSIVE_DISCOUNT** — "This employee averages 40% discounts. Everyone else averages 8%." Sweethearting — giving product away to friends and family. The peer comparison makes it obvious.

**C-001 RAPID_REFUND** — "Refund issued 3 minutes after the sale, same cashier." Classic cash-out scheme. Ring it up, pocket the cash, refund the card.

**C-101 NO_SALE_ABUSE** — "Cash drawer opened 12 times with no sale in one shift." Skimming. The drawer shouldn't open without a transaction.

**C-008 MANUAL_ENTRY_SPIKE** — "15 keyed-in card numbers in one shift. Store average is 2." Card-not-present fraud. Someone's typing in stolen card numbers.

**C-204 UNTENDERED_ORDER** — "Order created, items rung up, never paid for. 3 hours ago." Merchandise walked out the door.

## Adoption Ladder

Each stage feels like a natural next step. None require the word "AI":

Stage 1 (Prove): "Here's what we found" — the gold list hits, undeniable. Stage 2 (Watch): "Want us to keep watching?" — always-on monitoring, subscription starts. Stage 3 (Tune): "Let us tune it for your business" — LLM-assisted config per merchant, lock-in. Stage 4 (Predict): "Here's what's coming before it happens" — predictive analytics, the moat.

## Signal Over Noise

Too many alerts = they turn it off. Too few = they forget it exists. The sensitivity tuning per merchant is the product. A $500 transaction at a farmers market is a five-alarm fire. At a jewelry store it's Tuesday. The ThresholdManager feeds 30 days of merchant data to calibrate thresholds to THEIR business. The signal-to-noise ratio IS the product.

## Mobile-First Alert Design

The merchant is at the register, driving between locations. The alert hits their phone: "POST_VOID $200 — Steve Chen, Torrance, 4:47 PM." Tap → see the transaction → see the pattern → tap to escalate or dismiss. Done in 10 seconds. The ops console is back office. The phone is every day. That's where trust gets built.

## Validation Hunting List

When real merchant data flows, these confirmed patterns prove value for demos, case studies, and investors: first real POST_VOID with >15min gap, first OFF_CLOCK transaction, first AFTER_HOURS hit, first EXCESSIVE_DISCOUNT outlier, first RAPID_REFUND under 5 minutes, first NO_SALE cluster (5+ in shift), first MANUAL_ENTRY spike (3x average), first UNTENDERED_ORDER over 2 hours.

## Related

- [[Brain/wiki/canary-detection|Canary Detection Engine]] — Technical details on all 37 Chirp rules
- [[Brain/wiki/canary-architecture|Canary Architecture]] — System design and data flow
- [[Brain/projects/Canary|Canary MOC]] — Project hub

## Sources

- `docs/_archive/ip-vault/Canary/Strategy/Gold List — Top 8 Detection Rules.md` — Original strategy document (March 2026)
