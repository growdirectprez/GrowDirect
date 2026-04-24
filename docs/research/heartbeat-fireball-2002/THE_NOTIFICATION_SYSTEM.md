# THE_NOTIFICATION_SYSTEM — the Chirp ancestor

The single most directly Canary-parallel artifact in the 2002 archive.
Where the algorithm was the intellectual centre of the system, the
notification subsystem was the **operational centre** — the surface
through which the OOS detection actually reached a human who could do
something about it. This is the document set the Chirp module's
behavior most closely traces to.

## Trigger model — what fired a notification

Three event categories triggered notifications, each routed
separately:

1. **OOS Report** — package of OOS events (items that have transitioned
   to out-of-stock), Too Fast events (above-normal turn rate), Too Slow
   events (below-normal turn rate). Generated each reporting period.
2. **Threshold Alarm** — separate email when OOS-loss-value crossed a
   configured dollar threshold (e.g. "$996.36 in OOS losses since last
   check"). Sent independently of the OOS report so it didn't get lost
   in a long event list. Some users (e.g. one of the pilot retailers)
   explicitly suppressed Threshold Alarms.
3. **Data Flow Interrupted Alarm** — fires whenever the trickle POS
   feed pauses, signaling that downstream OOS reports may be unreliable.
   **All personnel received this; suppression was not allowed.** This
   is the trust-the-pipeline alarm — without it, an operator can't tell
   whether "no OOS events" means "everything's fine" or "we lost
   visibility."

> *Canary analogue.* Same three trigger categories. Chirp alerts =
> OOS Report. Severity-based thresholding = Threshold Alarm.
> TSP heartbeat / pipeline-health alerts = Data Flow Interrupted
> Alarm.

## Subscription model — who got what

Every user had a **per-user subscription** that controlled:

| Subscription dimension | Options |
|---|---|
| Report types received | OOS Report (yes/no) · Threshold Alarm (yes/no) · Data Flow Alarm (yes — non-suppressible) |
| Report period | 15-minute, hourly, every 4 hours, every 8 hours, daily — configurable per user, not per retailer (multi-day frequencies explicitly not supported) |
| Summary vs Periodic | **Summary** = current full OOS position (cumulative — same item across periods appears repeatedly). **Periodic** = changes since last report (transitions only). Mix-and-match supported (e.g., one summary per day at 6:00, periodic every 15 min during operating hours) |
| Time windows | Operator-defined — e.g., "every 15 minutes from 7:00 a.m. until 7:00 p.m." |
| Event-type filter | OOS · Too Fast · Too Slow — any subset. Operators routinely suppressed Too Fast / Too Slow when focused on stockouts |
| Promotional-status filter | Only items currently on promotion (yes/no) |
| Future filters (post-pilot) | Merchandise hierarchy (department / category) · Top-N selling items |
| Sort order | Two named profiles for pilot: **Stocker** (Event Type → Department → Category → Promotional Status → Item Code) and **Store Manager** (Event Type → Promotional Status → Department → Category → Item Code) |
| Report cap | Configurable; pilot default 100 events per report (handheld device constraint) |

User ↔ device was 1:1 in the system but devices could be shared
between humans operationally (the system didn't enforce; users
coordinated subscriptions among themselves).

> *Canary analogue.* The subscription model survives 1:1 in Chirp's
> alert routing — per-user notification preferences, channel selection
> (SMS / email / in-app / push), severity filter, quiet-hours
> suppression, daily rate caps, digest batching (realtime / hourly /
> daily / weekly). The 2002 sort-by-role pattern is recognizable in
> Canary's role-based dashboard views.

## Delivery channels

| Channel | Detail |
|---|---|
| Wireless pager / handheld | Primary. Two device families evaluated — handheld push-email devices and traditional alphanumeric pagers. Both received via SMTP. |
| Browser-based reports | Secondary. Operators with browser access could use a richer report (no character-cap constraint). Used for fuller summaries and audits. |
| Future channels (post-pilot) | Symbol/Telxon-class in-store handhelds, store digital phone systems |

The pilot UX was deliberately constrained: **8 lines × 25 characters**
per report (the lowest-common-denominator handheld display). Reports
were padded with spaces to make the larger device visually match the
smaller. This is the kind of detail that signals how seriously the
team took the operator's actual receiving context — they designed
to the hardware, not against it.

> *Canary analogue.* Modern channel set: SMS, email, in-app, web push,
> mobile push. Browser-based dashboard is the spiritual successor to
> the 2002 browser report. The "design to the receiving device"
> discipline carries forward — Canary's mobile alert detail page
> respects mobile read patterns, not desktop ones.

## Report format — the pager UX

The OOS Report wireframe, reconstructed from the spec:

```
        1         2
123456789012345678901234567
1 OOS mm/dd/yyyy hh:mm     ← report header (event type + timestamp)
2
3 O 004151132001 123456 P  ← event line: type | UPC | item | promo
4 ROMAN MEAL ROUND TOP BREA← description (40-char wrap)
5 D
6
7 O 001820000801 123456    ← next event
8 BUSH LIGHT 12 PACK /CANS
9
0
1
2
3
```

The convention:

- **One letter for event type** (`O`=OOS, `F`=Too Fast, `S`=Too Slow)
- **UPC + item code + promotional flag** on one line
- **Description** wrapped to ~40 chars on subsequent lines (no word-
  break formatting — character-cap was hard)
- **Three lines per event + blank** spacer

Threshold Alarm format was even tighter:

```
1 02/23/2001 15:49
2 THRESHOLD $   996.36
```

Data Flow Interrupted Alarm:

```
1 02/23/2001 15:49
2 DATA FLOW INTERRUPTED
```

> *Canary analogue.* SMS-format chirp messages follow the same
> philosophy: short, character-conscious, structured for fast scanning
> on a small screen. The "type letter + identifiers + description"
> pattern survives in Chirp alert summaries.

## Event schema — XML envelope and its evolution

The notification subsystem received its inputs as XML messages from
the OOS algorithm cluster's XML events formatter. Two schema versions
exist in the archive:

- **August schema** (Project-Heartbeat XMLschema 6 Aug)
- **January schema** (Project-Heartbeat XMLschema 15 Jan)

The 5-month delta (~Aug 2001 → Jan 2002) reflects production-experience
learning. The available materials carry both side by side; the
specific deltas are extractable from the schema docs as a forensic
exercise but the pattern is the more valuable signal.

Pattern observations:

- The XML envelope carried the data needed for routing **inside the
  body**, not just in headers (this is what enabled the integration
  bus's "Open Channels" pattern — destination derived from message
  content).
- The message identified retailer + store + event-type + item +
  timing inline.
- The schema's evolution between Aug and Jan is the kind of artifact
  that signals *the production deployment surfaced things the design
  hadn't predicted* — a healthy sign in any near-real-time messaging
  system.

> *Canary analogue.* Square webhook payload + Canary's normalized
> event records (the CRDM in `sales` schema). Same role: a wire-
> format event that carries enough context for routing and downstream
> action without external lookup. JSON over HTTPS rather than XML
> over EAI bus, but the design choice (self-contained event with
> routing context) is identical.

## Failure modes — what happened when things went wrong

The notification subsystem's failure modes get attention in the spec:

- **Trickle interruption** → Data Flow Interrupted Alarm fires (see
  trigger model above). Non-suppressible.
- **Notification delivery failure** to a specific device → not directly
  documented in the available artifacts, but the architecture's use of
  SMTP transport means the standard SMTP retry / queueing semantics
  applied. There is no documented store-and-forward queue at the
  notification subsystem level.
- **Subscription mismatch** (user's subscription requested a filter or
  hierarchy that wasn't yet supported) → handled at subscription-
  configuration time, not at delivery time.

The Phase-I Pilot Assessment's risk list flagged "delivery of a
notification system for the OOS algorithm does not yet represent a
significant opportunity to recoup investment" — interesting because
it underlines that the notification subsystem was perceived
internally as the *finished, working* part of the system. The risks
were business-model risks, not delivery-quality risks. The
notification subsystem worked.

> *Canary analogue.* Delivery failure handling is more sophisticated
> in modern Canary — explicit notification dispatch records, retry
> with backoff, dead-letter queue, per-channel circuit breakers. The
> 2002 notification subsystem worked; modern infrastructure makes the
> same role more robust under failure.

## Operator workflow — what the human did with the alert

The 2002 spec is explicit that the user wearing the pager was
expected to:

1. Be notified by vibration or audible tone
2. Open the report email
3. Browse the events
4. Take physical action at the shelf (the spec doesn't enumerate this
   — it's the implicit endpoint)
5. Delete the email when handled

There is no documented in-pager acknowledge / dismiss / escalate
workflow. The system did not track *whether the operator had acted on
an alert* — that was an out-of-band human-process responsibility.

> *Canary analogue.* This is a deliberate **expansion** in Canary.
> Chirp alerts have a full lifecycle (`new` → `investigating` /
> `escalated` / `resolved` / `dismissed` / `case_opened` /
> `archived`) tracked in `alert_history`. The 2002 design left the
> "did the operator act?" question to the operating environment;
> Canary brings it inside the system. This is one of the largest
> single deltas between the two designs.

## Why this is the most Canary-parallel artifact

The notification subsystem is where the 2002 system most closely
matches what Chirp does today. Trigger model · subscription model ·
delivery channels · report format · event schema · failure modes ·
operator workflow — every dimension has a Canary analogue, mostly
1:1 conceptually with substrate-and-sophistication updates.

The architectural shape — *near-real-time detection produces an event,
event flows through an integration layer, subscription subsystem
determines who and how, message renders for the receiving channel and
context, operator acts at the physical point* — is unchanged in 25
years. The 2002 design got this shape right, and Canary inherits it
without significant alteration.
