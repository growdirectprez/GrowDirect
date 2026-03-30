---
name: canary-tdd
description: |
  Test-driven development for Canary. Use when implementing any feature or bugfix,
  before writing implementation code. RED-GREEN-REFACTOR with data integrity
  principles, Python/pytest examples, and retail-aware test philosophy.
  Replaces superpowers:test-driven-development.
allowed-tools:
  - Read
  - Bash
  - Edit
  - Write
  - Grep
  - Glob
---

# Canary TDD — Test-Driven Development

> "At the end of the day we are generating metrics and serving up dashboards —
> they have to be accurate. We can't have any hallucinating data."
> — Jeffe, March 9, 2026

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests
the right thing.

**Why it matters here:** This platform analyzes people's livelihoods. A false
positive accuses someone of theft. A false negative lets real loss bleed through.
Every test we write is a guardrail against both.

**Announce at start:** "I'm using canary-tdd for test-first implementation."

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over.
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Delete means delete

## Red-Green-Refactor

### RED — Write Failing Test

Write one minimal test showing what should happen.

```python
# tests/unit/test_drawer_variance.py
import pytest
from canary.services.chirp.rules.cash_drawer import evaluate_drawer_variance

class TestDrawerVariance:
    def test_flags_variance_above_threshold(self):
        """Drawer short $18 on morning shift should trigger alert."""
        result = evaluate_drawer_variance(
            expected=500.00,
            actual=482.00,
            threshold=10.00
        )
        assert result.triggered is True
        assert result.variance == -18.00

    def test_ignores_variance_within_threshold(self):
        """Drawer short $3 with $10 threshold should not trigger."""
        result = evaluate_drawer_variance(
            expected=500.00,
            actual=497.00,
            threshold=10.00
        )
        assert result.triggered is False
```

**Requirements:**
- One behavior per test. "and" in the name? Split it.
- Clear name that describes the business behavior, not the implementation
- Real code paths — mocks only for external services (Square API, etc.)

### Verify RED — Watch It Fail

**MANDATORY. Never skip.**

```bash
python3 -m pytest tests/unit/test_drawer_variance.py -v
```

Confirm:
- Test fails (not errors from bad syntax)
- Failure message matches expectation (feature missing, not typo)
- If test passes immediately -> you're testing existing behavior. Fix the test.

### GREEN — Minimal Code

Write the simplest code that passes the test.

```python
# canary/services/chirp/rules/cash_drawer.py
from dataclasses import dataclass

@dataclass
class VarianceResult:
    triggered: bool
    variance: float

def evaluate_drawer_variance(
    expected: float,
    actual: float,
    threshold: float
) -> VarianceResult:
    variance = actual - expected
    return VarianceResult(
        triggered=abs(variance) > threshold,
        variance=variance
    )
```

Don't add features. Don't refactor other code. Don't "improve" beyond the test.

### Verify GREEN — Watch It Pass

**MANDATORY.**

```bash
python3 -m pytest tests/unit/test_drawer_variance.py -v
```

Then run smoke tests to catch regressions:

```bash
python3 -m pytest tests/smoke/ -v --timeout=30
```

Confirm:
- New test passes
- Existing tests still pass
- No warnings or errors in output

### REFACTOR — Clean Up

After green only:
- Remove duplication
- Improve names
- Extract helpers

Keep tests green. Don't add behavior.

### Repeat

Next failing test for next behavior.

---

## Pipeline Flow Tests

When touching any node in the six-node pipeline, prove data flows through —
not just within the service.

```python
class TestPipelineFlow:
    def test_webhook_reaches_structured_store(self, db_session):
        """A valid webhook should flow from receipt (Node 1) to parsed record (Node 3)."""
        result = process_webhook(SAMPLE_PAYMENT)
        assert result.status_code == 200

        txn = db_session.query(Transaction).filter_by(
            external_id=SAMPLE_PAYMENT["id"]
        ).first()
        assert txn is not None
        assert txn.merchant_id == expected_merchant_uuid  # UUID, not Square ID

    def test_detection_fires_on_threshold(self, db_session):
        """A transaction above threshold should flow from Node 3 to Node 4 (alert)."""
        insert_test_transaction(db_session, amount=999.99)
        alerts = run_detection_rules(merchant_id=test_merchant_uuid)
        assert len(alerts) >= 1
```

Unit tests prove the function works. Pipeline tests prove the data moves.
Both are required for any feature touching the pipeline.

---

## Data Integrity Tests

When touching `canary_sales` schema, always include immutability tests:

```python
class TestSalesImmutability:
    def test_insert_only_on_payments(self, db_session):
        """canary_sales tables reject UPDATE operations."""
        payment = create_test_payment(db_session)
        db_session.commit()

        payment.amount = 999.99  # attempt mutation
        with pytest.raises(Exception):  # trigger should block
            db_session.commit()

    def test_no_delete_on_transactions(self, db_session):
        """canary_sales tables reject DELETE operations."""
        txn = create_test_transaction(db_session)
        db_session.commit()

        db_session.delete(txn)
        with pytest.raises(Exception):
            db_session.commit()
```

> "We treat data integrity with the utmost seriousness. This is people's lives
> and jobs we are analyzing. If we accuse someone, we have to be sure and have
> the facts."

---

## Webhook Tests

When touching the TSP pipeline or Square integration:

```python
class TestWebhookIntegrity:
    def test_rejects_invalid_hmac(self):
        """Unsigned or tampered webhooks must be rejected."""
        response = process_webhook(
            payload=SAMPLE_PAYMENT,
            signature="bad-signature"
        )
        assert response.status_code == 401

    def test_processes_valid_webhook(self):
        """Properly signed webhook flows through TSP pipeline."""
        response = process_webhook(
            payload=SAMPLE_PAYMENT,
            signature=compute_hmac(SAMPLE_PAYMENT)
        )
        assert response.status_code == 200
```

---

## Pytest Markers

Tag tests with markers from `pytest.ini`:

```python
@pytest.mark.chirp
def test_chirp_rule_evaluation():
    ...

@pytest.mark.fox
def test_case_evidence_chain():
    ...

@pytest.mark.smoke
def test_health_endpoint():
    ...
```

Available: `unit`, `smoke`, `chirp`, `fox`, `owl`, `square`, `raas`,
`healthcheck`, `browser`, `postgres`, `critical`

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "TDD will slow me down" | TDD is faster than debugging in production. |
| "Need to explore first" | Fine. Throw away exploration. Start with TDD. |
| "Test hard = design unclear" | Listen to the test. Hard to test = hard to use. |
| "Existing code has no tests" | You're improving it. Add tests for what you touch. |
| "Already manually tested" | Ad-hoc != systematic. No record, can't re-run. |
| "Deleting X hours of work is wasteful" | Sunk cost. Keeping untested code is tech debt. |

## Red Flags — STOP and Start Over

- Code before test
- Test passes immediately
- Can't explain why test failed
- "Just this once"
- "Keep as reference"
- "It's about spirit not ritual"

**All of these mean: Delete code. Start over with TDD.**

---

## Debugging Integration

Bug found? Write failing test reproducing it. Follow TDD cycle.
The test proves the fix AND prevents regression. Never fix bugs without a test.

For complex bugs, use `canary-debug` first to find root cause,
then return here for the fix.

---

*Canary TDD v1.0 — Test-Driven Development*
*Replaces: superpowers:test-driven-development*
