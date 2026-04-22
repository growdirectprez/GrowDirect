---
name: cove-qa
roles-primary:[Compliance]
roles-assist:[QA]
stage: qa
description: |
  QA testing for Cove. Use when asked to test, verify a branch, or before
  shipping. Diff-aware route testing with governance checks and structured reports.
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
---

# Cove QA — Quality Assurance

> Delegates to: `factory-qa` for standard QA workflow.

Run the factory-qa skill, then apply the Cove-specific QA checks below.

**Announce:** "I'm using cove-qa to test [scope]."

## Cove-Specific QA Checks

### Template Discovery Warning

Templates live in **blueprint-local** folders, NOT just `cove/templates/`.

```bash
# CORRECT — finds all templates
find cove -name "*.html" -not -path "*/.claude/*" -not -path "*/static/*"

# WRONG — only finds archive + base
find cove/templates -name "*.html"
```

Always use the first form when auditing templates.

### Governance QA Checks

If the diff touches governance files:

```bash
# Confirm ballot table has no member_id
docker exec devops-cove-db-1 psql -U cove -d cove -c \
  "SELECT column_name FROM information_schema.columns WHERE table_name = 'ballots';"

# Confirm RLS is enabled on ballot_envelopes
docker exec devops-cove-db-1 psql -U cove -d cove -c \
  "SELECT relrowsecurity FROM pg_class WHERE relname = 'ballot_envelopes';"
```

### Security Checklist

- Missing `@login_required` on non-public routes?
- Missing CSRF token in forms (`{{ form.hidden_tag() }}`)?
- SQL injection via string interpolation?
- Broken template inheritance?
- IDOR: entity fetches scoped to `current_user.organization_id`?
- Privacy consent gate bypassed on member routes?

### Report Format

```markdown
## QA Report — [Branch/Feature]

**Tested:** [date]
**Mode:** [quick/diff-aware/full]

### Routes Tested
| Route | Expected | Actual | Pass |

### Governance Checks
[ballot integrity, quorum, RLS — or "N/A"]

### Issues Found
[list or "None"]
```

---

*Cove QA v1.0 — Quality Assurance*
*Delegates to: factory-qa*
