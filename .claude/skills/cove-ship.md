---
name: cove-ship
roles-primary: [Jeremy]
roles-assist: [DevOps]
stage: ship
description: |
  Ship a development branch for Cove. Use when implementation is complete,
  tests pass, and you need to commit, PR, or deploy.
allowed-tools:
  - Read
  - Bash
  - Grep
---

# Cove Ship — Finishing a Development Branch

> Delegates to: `factory-ship` for standard ship workflow.

Run the factory-ship skill, then apply the Cove-specific additions below.

**Announce:** "I'm using cove-ship to land [feature]."

## Cove-Specific Additions

### Pre-Ship Checklist

- [ ] Ballot integrity verified (if governance feature): no `member_id` in `ballots`
- [ ] GRO issue referenced in all commits (`GRO-XXX: ...`)
- [ ] Docker stack healthy: `docker compose -f devops/docker-compose.yml ps`

### Commit Convention

```bash
git commit -m "GRO-XXX: [imperative verb] [what and why]"
```

Branch naming: `feature/GRO-XXX-short-description`

### PR Template

```bash
gh pr create --title "GRO-XXX: [title]" --body "$(cat <<'EOF'
## Summary
- [what changed]

## Evidence
- Tests: [count] passing
- Routes: [tested]
- Ballot integrity: [verified / N/A]
- Davis-Stirling: [compliant / N/A]

## GRO Issue
GRO-XXX
EOF
)"
```

### Post-Ship

1. Mark GRO issue as Done in Linear
2. Run smoke test: `curl -s http://localhost:5002/`
3. Note follow-up items as new Linear issues

---

*Cove Ship v1.0 — Finishing a Development Branch*
*Delegates to: factory-ship*
