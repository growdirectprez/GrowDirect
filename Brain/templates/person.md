---
type: person
status: active   # active | inactive
person-id: <slug>
role: <e.g. founder, agent-ALX, agent-Tom, partner-VAR-principal>
kind: <human|agent|partner>
modules-owned: []  # spine letters this person/agent has primary responsibility for
services-owned: []
on-call: <schedule-link-or-null>
contact-public: <email-or-null>   # null for confidential
relationships: []  # var_partner, customer, vendor — links to those entities
last-compiled: <YYYY-MM-DD>
tags: [person, org]
---

# <Name or agent identity>

Short bio / role description. For agents, the system prompt's intent.

## Responsibilities

- <responsibility>
- <responsibility>

## How to reach

For humans: see frontmatter `contact-public` (if set). Internal contact info lives in private notes.

For agents: invocation pattern, where they run.

## Related

- Services owned: [[]]
- Modules owned: [[]]
- Active dispatches / projects: (Bases query)
