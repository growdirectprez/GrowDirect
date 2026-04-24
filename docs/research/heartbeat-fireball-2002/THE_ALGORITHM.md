# THE_ALGORITHM — the core OOS detection method

The intellectual centre of the 2002 system. A statistical algorithm
that **learns normal item velocity from POS transaction history under
varying merchandising conditions, then detects statistical variances
from that learned velocity** to flag a small set of named event types.
Branded as the Consumer Demand Signal Service / Item Velocity Monitor.

## What it computes

Five named event types per (store, SKU):

| Event type | Meaning |
|---|---|
| OOS | Out of stock — observed velocity has dropped to a level inconsistent with the learned model |
| Too Fast | Item moving above its normal turn rate (typically signals a sudden popularity shift, a misprice, or a competitor outage) |
| Too Slow | Item moving below its normal turn rate (without yet being OOS — leading indicator) |
| New Item | Item now appearing in the data with no prior history — first-time observation flag |
| Dropped Item | Item that previously had a learned velocity has stopped appearing — possible delist / discontinue |

## What it operates on

| Input | Description |
|---|---|
| Transaction stream | Trickled TLOG: per-basket-checkout, with timestamp, sequence of item codes (UPCs), per-item quantity, net price per item (regular price + applicable discounts) |
| Item master | Daily Item Tables: PLU / item code, description, attributes, hierarchy, current promotional flag |
| Merchandising-condition context | Current price, time of day, day of week, store identifier, current store traffic, current promotions, in-store competition, seasonality |

The model does *not* receive an inventory feed. OOS is **inferred from
sales velocity dropping below the model's expectation**, not from an
inventory-on-hand count crossing zero. This is the most consequential
design choice in the system.

## How it learns

A statistical model per (monitored item, monitored store, merchandising
condition). The training is described in the source as transforming
historical item-movement data into a series of "event observations
whose arrival times behave in a random, statistically independent way
called a **Poisson process**." The transformation specifics were
proprietary to the algorithm vendor and not disclosed in the available
artifacts.

What is disclosed:

- The model accounts for **price, time of day, day of week, store name,
  current store traffic, current promotions, in-store competition,
  and seasonality**. Eight covariates.
- The model is **first trained, then used to detect events, then
  retrained using the events-adjusted historical data** (a feedback
  loop). The events themselves filter the training data — observations
  during a known OOS event are not allowed to corrupt the velocity
  learning.
- The model is **automatically rebuilt every 15 minutes to 24 hours**
  depending on installation. The 15-minute end is the live-pilot
  cadence; the 24-hour end is for less time-sensitive deployments.

## How it detects

For each new transaction, the model is queried: *"What is the
probability of the newly observed transaction data given the normal
velocity model?"* "Normal velocity" already accounts for current
conditions (price, promotion, traffic, etc.). If the probability of
the observation, or of one more extreme (slower or faster), is small,
an anomaly event is generated. The kind of event (OOS / Too Fast /
Too Slow / New Item / Dropped Item) depends on the transaction
data and a set of **model rules adapted per installation**.

This is a **likelihood-ratio anomaly detector against a learned
Poisson model with merchandising-context covariates**. It's not
threshold-based on raw counts. It's not Bayesian in the Bayesian-
network sense. It's a parametric statistical model with a per-event-
type classification overlay tuned per deployment.

## Output handling

Detected events are:

1. **Immediately stored into the events cache** (in-memory, fast
   lookup) so they're available to the events server.
2. **Cached alongside select velocity-model details** — expected item
   velocities and historical item sales — so a downstream client
   can query "what was expected vs what was observed" for a given
   item without recomputing.
3. **Updated every 15 minutes** in the cache (for the live-pilot
   cadence).
4. **Streamed out via the XML events formatter** to the integration
   bus, which routes them to the notification subsystem.

## False-positive / false-negative control

The source artifacts are explicit that the algorithm's accuracy was
tunable and *was tuned* per installation. Specific control points:

- **Per-store training** — the model is per-(item, store) so a SKU
  that turns slowly in one location and fast in another is modeled
  separately.
- **Promotional-status awareness** — explicit covariate so a sudden
  velocity spike during a known promotion does not register as Too
  Fast.
- **Event-feedback retraining** — events themselves filter the
  training data so a learned OOS period doesn't subsequently get
  re-learned as "normal slow velocity."
- **Independent audit** — the southeastern-chain pilot conducted an
  independent audit of algorithm accuracy via the browser-based
  reports. Audits of this kind appear to have been routine pre-
  deployment.

## What "out for restocking" vs "really OOS" detection looked like

The source doesn't directly answer this — but the "Too Slow" event
type plus the per-(item, store) Poisson model implies that the
algorithm's semantics treat OOS as a continuum, not a binary. A SKU
moving below its expected rate is "Too Slow"; one that has dropped
to ~zero observation against expected non-zero is "OOS." There is
no documented "out for restocking" exclusion — operationally, it
appears that the operator receiving the OOS alert was expected to
disambiguate (visit the shelf, check the back room) rather than the
algorithm.

## Operator tunability

| Tunable | Where the operator could intervene |
|---|---|
| Threshold sensitivity | Per-installation tuning by the algorithm vendor; not described as customer-facing |
| Subscription / filtering | Per-user via subscription system (see THE_NOTIFICATION_SYSTEM.md). Operators couldn't tune the algorithm but they could tune what they received |
| Retraining cadence | Set per installation (15-min to 24-hour) |
| Per-event-type classification rules | Adapted per installation by the vendor |

The model was *not* designed for end-user threshold tuning. Operators
got knobs over delivery, not detection.

## Knowledge gaps in the available artifacts

- The exact transformation from raw POS to Poisson event observations
  is proprietary and not disclosed.
- The specific likelihood threshold for event generation is not stated.
- The classification logic for OOS-vs-Too Slow is not disclosed in
  closed form.
- Performance characteristics under high-traffic conditions (the
  Phase-I retrospective notes scalability and tuning time as risks)
  are not documented in the algorithm collateral itself.

## Canary analogue

Canary's Chirp module is a **multi-rule deterministic detection
engine** rather than a single statistical model:

- 27+ named detection rules, each with explicit threshold parameters
  configurable per merchant
- Severity-based scoring + dollar-impact attribution per alert
- No Poisson-velocity learning (yet); rules are deterministic against
  POS event shape
- Per-merchant threshold overrides via `merchant_rule_configs`
- Future work: a statistical-anomaly layer (the Bayesian / KAP
  scoring referenced in Canary's data-strategy NorthStar) would be
  the direct descendent of the 2002 OOS algorithm — broadened from
  one detection question to many, but the per-(merchant, signal)
  learned-baseline pattern is identical.

The 2002 design picked **one flagship algorithm, very tunable, applied
narrowly**. Canary picks **many simpler rules, tunable individually,
applied broadly**. Both shapes solve the same shape of problem; the
2002 work proved the per-store-per-SKU baseline was viable.
