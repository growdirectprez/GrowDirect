---
name: cove-tdd
roles-primary:[Engineer]
stage: tdd
description: |
  Test-driven development for Cove governance platform. Use when implementing
  any feature or bugfix, before writing implementation code. RED-GREEN-REFACTOR
  with ballot integrity tests, quorum verification, and APN chain validation.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Write
  - Edit
---

# Cove TDD — Test-Driven Development

> Delegates to: `factory-tdd` for standard RED-GREEN-REFACTOR.

Run the factory-tdd skill, then apply the Cove-specific test patterns below.

**Announce:** "I'm using cove-tdd for [feature]."

## Cove-Specific Required Tests

### Ballot Separation Test (Required for any governance feature)

```python
def test_ballot_has_no_member_id(self):
    """Secret ballot: ballot table must NOT have member_id column."""
    from cove.models.governance import Ballot
    columns = [c.name for c in Ballot.__table__.columns]
    assert "member_id" not in columns
```

### One Vote Per Member Test

```python
def test_cannot_vote_twice(self, app_ctx, member, proposal):
    from cove.governance.services import cast_vote
    cast_vote(proposal.id, member, "yes", "test")
    with pytest.raises(ValueError, match="already voted"):
        cast_vote(proposal.id, member, "no", "test")
```

### Quorum Calculation Tests

```python
def test_quorum_general_business(self, app_ctx, org):
    """1/3 of 81 members = 27 needed."""
    quorum = calculate_quorum(proposal, eligible_count=81)
    assert quorum.required == 27

def test_no_quorum_for_secret_ballot(self, app_ctx, org):
    """Secret ballot votes have no quorum requirement per §5.9."""
    proposal.requires_secret_ballot = True
    quorum = calculate_quorum(proposal, eligible_count=81)
    assert quorum.required == 0
```

### APN Chain Test

```python
def test_member_resolves_to_parcel(self, app_ctx, member):
    """Every member connects back to a parcel via APN."""
    assert member.parcel is not None
    assert member.parcel.apn is not None
```

### Route Access Tests

```python
def test_board_route_requires_board_role(self, client, member_login):
    """Non-board members get 403 on board routes."""
    resp = client.get("/board/")
    assert resp.status_code == 403

def test_protected_route_redirects_anonymous(self, client):
    """Anonymous users redirect to login."""
    resp = client.get("/member/dashboard")
    assert resp.status_code == 302
    assert "/auth/login" in resp.headers["Location"]
```

## Test Locations

| Layer | Directory | What it tests |
|-------|-----------|---------------|
| Unit | `tests/unit/` | Services, quorum math, ballot separation, model logic |
| Integration | `tests/integration/` | Routes -> services -> DB full cycle |
| Smoke | `tests/smoke/` | Endpoints exist and respond (200/302) |

---

*Cove TDD v1.0 — Test-Driven Development*
*Delegates to: factory-tdd*
