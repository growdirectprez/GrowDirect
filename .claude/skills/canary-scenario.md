---
name: canary-scenario
roles-primary: [Jim]
roles-assist: [Art]
description: |
  Use when adding a new test scenario to the Test Lab. Enforces fully-populated
  payloads, proper scenario structure, and end-to-end verification for Chirp
  rule testing.
allowed-tools:
  - Read
  - Bash
  - Edit
  - Write
  - Grep
  - Glob
---

# Canary Scenario — Adding Test Scenarios to the Lab

## When to Use

- Adding a new Chirp rule scenario to the Test Lab
- Extending an existing scenario with new steps
- Creating scenarios for a new domain (gift cards, loyalty, timecards, etc.)

## Hard Rules

1. **Every payload field populated.** Use `payload_factory.py` builders. No hand-built sparse payloads.
2. **No direct SQL.** Data enters through the lab -> Square SDK -> webhook -> TSP.
3. **One system.** Scenarios live in `SCENARIO_REGISTRY` in `scenario_fire.py`.

## Process

### Step 1: Identify the Chirp Rule

Read `canary/services/chirp/rule_engine.py` to understand trigger conditions,
detection_type, alert severity and category.

### Step 2: Design the Trigger Pattern

| Rule Type | Pattern |
|-----------|---------|
| Rapid refund (C-001) | Order -> immediate refund (within 15 min) |
| Round amount (C-003) | Order totaling exact $X.00 |
| Card velocity (C-005) | 5+ orders on same card within 60 min |
| After hours (C-004) | Order with timestamp outside 6am-10pm |
| Excessive discount (C-201) | Order with discount > 50% of gross |
| Sweethearting (C-203) | Single item discount >= $20 |
| Post void (C-502) | Order -> payment -> cancel |

### Step 3: Define the Scenario

Add to `SCENARIO_REGISTRY` in `canary/services/scenario_fire.py` with name,
description, tests_rules, steps (action, label, line_items, tip_cents, nonce),
expected_rules, and verification_queries.

### Step 4: Update Test Lab UI

Add the new scenario to the table in `templates/ops/test_lab.html`.

### Step 5: Fire and Verify

```bash
python3 devops/scripts/seed_sandbox.py --scenario your_scenario_key
```

Check Chirps page for expected alerts, verify evidence chain, run Owl verification.

### Step 6: Commit

```bash
git add canary/services/scenario_fire.py templates/ops/test_lab.html
git commit -m "feat(GRO-XXX): add <scenario_name> test scenario"
```

## Checklist

- [ ] Chirp rule trigger conditions understood
- [ ] Scenario defined in SCENARIO_REGISTRY
- [ ] All line items use product names from payload_factory.CATALOG
- [ ] All payloads fully populated (no sparse fields)
- [ ] Expected rules listed
- [ ] Scenario row added to test_lab.html
- [ ] Scenario fired successfully
- [ ] Expected Chirp alert(s) appeared
- [ ] Evidence chain verified

---

*Canary Scenario v1.0 — Test Lab Scenario Addition*
