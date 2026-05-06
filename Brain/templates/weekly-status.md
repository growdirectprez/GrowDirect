---
date: <% tp.date.now("YYYY-MM-DD") %>
type: weekly-status
week: <% tp.date.now("GGGG") %>-W<% tp.date.now("WW") %>
week-start: <% tp.date.now("YYYY-MM-DD", -6) %>
week-end: <% tp.date.now("YYYY-MM-DD") %>
author: Alejandro
status: draft
last-compiled: <% tp.date.now("YYYY-MM-DD") %>
needs-review: <% tp.date.now("YYYY-MM-DD", 14) %>
tags: [weekly-status, status-report]
---

# Weekly Status — <% tp.date.now("GGGG") %>-W<% tp.date.now("WW") %>

> ABCD — Accomplishments · Benefits · Concerns · Do Next. The four-box is
> the narrative layer. The auto-rails below are the inventory layer. If
> the box at the top reads as a duplicate of the rails, the box failed.

## Governing thesis
<!-- One paragraph. The single most important thing about this week.
     What moved? What changed? What's the headline a partner would care about? -->


## A · Accomplishments
<!-- What got done. Concrete, verifiable, one bullet per item.
     Each bullet links to a Linear issue, commit SHA, or wiki article. -->



## B · Benefits
<!-- Why it mattered. Outcomes, not activities. The "so what" against
     each accomplishment. If you can't write a benefit, the accomplishment
     was busywork — flag it. -->



## C · Concerns
<!-- Risks, blockers, drift, things slipping. One bullet per concern,
     with severity (LOW/MED/HIGH) and what would unblock it.
     Be honest. Future-self needs the truth. -->



## D · Do Next
<!-- Top 3-5 priorities for next week, ranked. If you ship none of these,
     the week was a failure. Each item points at a Linear issue. -->

1.
2.
3.

---

## Auto-rails
<!-- Populated by `engine.py weekly` on Friday. Don't edit by hand —
     re-run the command if these are stale. -->

### Dispatches closed this week
<!-- Linear: Done in Dispatch project, closed-at within week range -->


### Wiki cards added or updated
<!-- git log --since=Mon --until=Sun -- Brain/wiki/ -->


### Commits of substance
<!-- git log filtered to non-trivial commits (not formatting/typo-only) -->


---

## Cross-week thread
<!-- What from last week's "Do Next" landed? What slipped? Patterns over time
     show up here. If "blocker X" is in the Concerns box for the third week
     running, that's its own emergency. -->

