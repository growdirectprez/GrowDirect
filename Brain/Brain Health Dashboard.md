---
type: dashboard
tags: [brain, health, dataview, maintenance]
---

# Brain Health Dashboard

Live queries powered by Dataview. Open this note in Obsidian to see auto-updating tables.

---

## Overdue Reviews

Articles past their `needs-review` date:

```dataview
TABLE needs-review AS "Review Due", status, type
FROM "Brain/wiki"
WHERE needs-review AND needs-review < date(today)
SORT needs-review ASC
```

---

## Recently Updated (Last 14 Days)

```dataview
TABLE last-compiled AS "Compiled", status, type
FROM "Brain/wiki"
WHERE last-compiled
SORT last-compiled DESC
LIMIT 15
```

---

## Missing Frontmatter

### No `last-compiled` date

```dataview
TABLE date AS "Created", type, status
FROM "Brain/wiki"
WHERE !last-compiled
SORT file.name ASC
```

### No `status` field

```dataview
TABLE date AS "Created", type
FROM "Brain/wiki"
WHERE !status
SORT file.name ASC
```

---

## Stale Articles (No Update in 30+ Days)

```dataview
TABLE last-compiled AS "Last Compiled", status
FROM "Brain/wiki"
WHERE last-compiled AND (date(today) - last-compiled).days > 30
SORT last-compiled ASC
```

---

## Articles by Project

### Cove
```dataview
TABLE status, last-compiled AS "Compiled"
FROM "Brain/wiki"
WHERE contains(tags, "cove")
SORT file.name ASC
```

### Angel
```dataview
TABLE status, last-compiled AS "Compiled"
FROM "Brain/wiki"
WHERE contains(tags, "angel")
SORT file.name ASC
```

### Canary
```dataview
TABLE status, last-compiled AS "Compiled"
FROM "Brain/wiki"
WHERE contains(tags, "canary")
SORT file.name ASC
```

### Seacove
```dataview
TABLE status, last-compiled AS "Compiled"
FROM "Brain/wiki"
WHERE contains(tags, "seacove")
SORT file.name ASC
```

---

## Orphan Check

Notes in `Brain/wiki/` with zero incoming links:

```dataview
LIST
FROM "Brain/wiki"
WHERE length(file.inlinks) = 0
SORT file.name ASC
```

---

## Inbox Status

```dataview
LIST
FROM "Brain/raw/inbox"
SORT file.name ASC
```

---

## Stats

- **Total wiki articles:** `$= dv.pages('"Brain/wiki"').length`
- **Total project MOCs:** `$= dv.pages('"Brain/projects"').length`
- **Articles with needs-review:** `$= dv.pages('"Brain/wiki"').where(p => p["needs-review"]).length`
- **Articles missing last-compiled:** `$= dv.pages('"Brain/wiki"').where(p => !p["last-compiled"]).length`
