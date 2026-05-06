---
date: 2026-05-03
type: index
last-compiled: 2026-05-03
needs-review: 2026-08-03
tags: [weekly-status, index]
---

# Weekly Status — index

Friday-cadence ABCD reports. One file per ISO week, named
`YYYY-Www-status.md`. Source of the narrative layer over Linear's
inventory layer.

## Why this exists

Linear tells you which dispatches closed. The weekly status tells you what
those closes *meant* — patterns, slippage, the headline a partner would
care about. If a weekly report reads as a duplicate of last week's Linear
filter, the report failed.

## ABCD format

| Box | Question | Failure mode |
|---|---|---|
| **A — Accomplishments** | What got done? | Activity list with no link to outcome |
| **B — Benefits** | Why did it matter? | Empty boxes — busywork in disguise |
| **C — Concerns** | What's slipping or at risk? | Sandbagging — concerns suppressed |
| **D — Do Next** | Top 3-5 priorities for next week | Wishlist instead of ranked priorities |

## Cadence

- **Friday afternoon (target):** run `python3 content-engine/engine.py weekly`
  to scaffold the file with auto-populated rails (closed dispatches, wiki
  adds, commits). Fill in the four boxes by hand. 15 minutes if the rails
  are doing their job.
- **Same sitting:** tick any SDLC stage transitions on the module entity
  cards in `Brain/modules/`. The [SDLC Tracker.base](../SDLC Tracker.base)
  re-renders automatically.
- **Monday morning:** re-read the prior week's ABCD before opening Linear.
  This is the "what was I doing" anchor that closes the loop.

## Cross-references

- [[../SDLC Tracker]] — module × SDLC stage matrix (live Bases view)
- [[../NFR Matrix]] — subsystem × NFR concern matrix (live Bases view)
- [[../templates/weekly-status]] — Templater scaffold for new weeks
- [[../templates/module]] — module entity template (feeds the trackers)

## Related

- [[../projects/Method|Method MOC]] — platform method
- [`engine.py weekly`](../../content-engine/engine.py) — auto-rail generator
