---
name: cove-preflight
roles-primary:[ALX]
roles-assist:[ProgramManager]
stage: preflight
description: |
  Session bootstrap for Cove development. Run at the start of every session.
  Delegates to factory-preflight for shared infrastructure, then adds Cove-specific
  checks: template integrity, archive integrity, blueprint count, security docs,
  Davis-Stirling context. Use when: starting a session, 'cove preflight', 'check in',
  'status', 'where are we'.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
---

# Cove Preflight — Session Bootstrap

> Delegates to: `factory-preflight` for shared infrastructure checks.

Run factory-preflight first, then apply the Cove-specific checks below.

**Announce at start:** "I'm using cove-preflight to bootstrap this session."

## Cove Builder Identity

You are the **Cove builder** — a headless factory executor. No persona, no greeting. Run the pipeline.

Shorthand triggers:
| Command | Action |
|---------|--------|
| `cove preflight` | Run this preflight |
| `check in` / `status` / `where are we` | Run this preflight |
| `>>north star` | "This community owns something rare: private ocean access on the California coast. Cove exists to organize, fund, and defend that asset." |

## Cove-Specific Health Checks

After factory-preflight passes, run:

```bash
cd ~/GrowDirect/Cove

# Template integrity (blueprint-local — NOT just cove/templates/)
echo "=== Templates (blueprint-local + shared) ===" && find cove -name "*.html" -not -path "*/.claude/*" -not -path "*/static/*" | wc -l
echo "=== Real templates (>10 lines) ===" && find cove -name "*.html" -not -path "*/.claude/*" -not -path "*/static/*" -exec sh -c 'test $(wc -l < "$1") -gt 10' _ {} \; -print | wc -l
echo "=== Stub templates (<=10 lines) ===" && find cove -name "*.html" -not -path "*/.claude/*" -not -path "*/static/*" -exec sh -c 'test $(wc -l < "$1") -le 10' _ {} \; -print | wc -l

# Archive integrity
echo "=== Archive docs ===" && find docs/archive -name "*.md" -not -path "*/originals/*" | wc -l
echo "=== Originals ===" && find docs/archive/originals -type f | wc -l

# Security & blueprints
echo "=== Security docs ===" && ls docs/security/*.md 2>/dev/null | wc -l
echo "=== Expected: 3 (data-retention, encryption, breach) ==="
echo "=== Blueprints ===" && grep -c "register_blueprint" cove/__init__.py
echo "=== Expected: 14 ==="
```

**IMPORTANT:** Templates live in **blueprint-local** folders (`cove/*/templates/*/`),
NOT just `cove/templates/`. Always search with `find cove -name "*.html"`.

### Flags

- Any `docs/knowledge/` references = RED (old directory structure leaked back)
- Security docs < 3 = RED (compliance gap)
- Blueprint count != 14 = YELLOW (module added/removed without updating CLAUDE.md)
- Stub count increasing = YELLOW (new routes without real templates)

### Cove Health Report Extension

```
| Templates  | [status] | X real, Y stubs (blueprint-local) |
| Archive    | [status] | X docs, Y originals |
| Security   | [status] | X docs (expected 3) |
| Blueprints | [status] | X registered (expected 14) |
```

### Davis-Stirling Context

Before starting governance-related work, verify familiarity with:
- Civil Code §5100-5145 (elections, secret ballots)
- Corp Code §7512 (quorum rules)
- AB 2159 (2024) — electronic secret ballot voting
- AB 2460 (2024) — reconvened election quorum reduced to 20%

### Linear Status

Pull current state from Linear project **Cove** (GRO-prefixed issues).

---

*Cove Preflight v1.0 — Session Bootstrap*
*Delegates to: factory-preflight (shared infra)*
*Replaces: cove-startup*
