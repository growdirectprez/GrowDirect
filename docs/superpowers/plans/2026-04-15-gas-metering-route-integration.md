# Gas Metering Route Integration — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Wire a `@gas_metered` decorator to 9 intelligence endpoints so merchant wallet usage is tracked with fictitious sat balances.

**Architecture:** New `@gas_metered(operation_key)` decorator uses JWT merchant_id, looks up cost via `GasMeter.get_cost()`, debits via `WalletService.debit()` directly (bypassing `GasMeter.charge()` balance check for soft-gate). Auto-provisions wallets for merchants who predate Goose. Receipt endpoints gain `@jwt_required` + merchant scoping.

**Tech Stack:** Flask decorators, SQLAlchemy (existing GasMeter/WalletService/TreasuryService), pytest

**Spec:** `docs/superpowers/specs/2026-04-15-gas-metering-route-integration-design.md`

---

## File Structure

| File | Action | Responsibility |
|------|--------|----------------|
| `canary/services/goose/gas_metered.py` | Create | `@gas_metered` decorator |
| `canary/blueprints/owl_api.py` | Modify | Add `@gas_metered` to 5 routes |
| `canary/blueprints/fox_wired.py` | Modify | Add `@gas_metered` to 2 routes |
| `canary/blueprints/receipt_tsp.py` | Modify | Add `@jwt_required` + `@gas_metered` to 2 routes, merchant scoping on queries |
| `tests/unit/test_gas_metered.py` | Create | 8 unit tests for decorator |
| `tests/integration/test_gas_metered_routes.py` | Create | 3 integration tests for route wiring |

---

## Chunk 1: `@gas_metered` Decorator

### Task 1: Write decorator unit tests

**Files:**
- Create: `tests/unit/test_gas_metered.py`

- [ ] **Step 1: Create test file with all 8 unit tests**

```python
"""Unit tests for @gas_metered decorator."""

import uuid
from unittest.mock import MagicMock, patch

import pytest
from flask import Flask, g, jsonify


@pytest.fixture
def app():
    """Minimal Flask app for testing decorators."""
    app = Flask(__name__)
    app.config["TESTING"] = True
    return app


@pytest.fixture
def mock_session():
    return MagicMock()


class TestGasMetered:
    """Tests for the @gas_metered decorator."""

    def test_charges_wallet_with_correct_amount(self, app, mock_session):
        """Metered request with existing wallet charges the correct amount."""
        from canary.services.goose.gas_metered import gas_metered

        mock_wallet = MagicMock()
        mock_wallet.id = "wallet-123"
        mock_wallet.status = "active"
        mock_wallet.balance_sats = 100000

        mock_tx = MagicMock()
        mock_tx.balance_after_sats = 99975

        with app.test_request_context("/test"):
            with patch("canary.services.goose.gas_metered.get_session", return_value=mock_session):
                with patch("canary.services.goose.gas_metered.GasMeter") as MockGM:
                    with patch("canary.services.goose.gas_metered.WalletService") as MockWS:
                        MockGM.return_value.get_cost.return_value = 25
                        MockWS.return_value.get_wallet.return_value = mock_wallet
                        MockWS.return_value.debit.return_value = mock_tx

                        g.merchant_id = "merchant-abc"

                        @gas_metered("owl.query.basic")
                        def dummy_route():
                            return jsonify({"ok": True})

                        response = dummy_route()
                        MockWS.return_value.debit.assert_called_once_with(
                            wallet_id="wallet-123",
                            merchant_id="merchant-abc",
                            amount_sats=25,
                            operation_type="owl.query.basic",
                            reference_id=MockWS.return_value.debit.call_args.kwargs["reference_id"],
                            reference_type="http_request",
                        )

    def test_auto_provisions_wallet_when_none_exists(self, app, mock_session):
        """Metered request with no wallet auto-provisions wallet + funds, then charges."""
        from canary.services.goose.gas_metered import gas_metered

        new_wallet = MagicMock()
        new_wallet.id = "new-wallet"
        new_wallet.status = "active"
        new_wallet.balance_sats = 100000

        mock_tx = MagicMock()
        mock_tx.balance_after_sats = 99975

        with app.test_request_context("/test"):
            with patch("canary.services.goose.gas_metered.get_session", return_value=mock_session):
                with patch("canary.services.goose.gas_metered.GasMeter") as MockGM:
                    with patch("canary.services.goose.gas_metered.WalletService") as MockWS:
                        with patch("canary.services.goose.gas_metered.TreasuryService") as MockTS:
                            MockGM.return_value.get_cost.return_value = 25
                            # First call returns None (no wallet), second returns new wallet
                            MockWS.return_value.get_wallet.side_effect = [None, new_wallet]
                            MockWS.return_value.debit.return_value = mock_tx

                            g.merchant_id = "merchant-new"

                            @gas_metered("owl.query.basic")
                            def dummy_route():
                                return jsonify({"ok": True})

                            response = dummy_route()
                            # Verify wallet was created via session.add
                            assert mock_session.add.called
                            # Verify treasury funded it
                            MockTS.return_value.fund_merchant.assert_called_once()

    def test_allows_negative_balance_soft_gate(self, app, mock_session):
        """Metered request with depleted wallet debits into negative, passes through."""
        from canary.services.goose.gas_metered import gas_metered

        mock_wallet = MagicMock()
        mock_wallet.id = "wallet-broke"
        mock_wallet.status = "depleted"
        mock_wallet.balance_sats = 0

        mock_tx = MagicMock()
        mock_tx.balance_after_sats = -25

        with app.test_request_context("/test"):
            with patch("canary.services.goose.gas_metered.get_session", return_value=mock_session):
                with patch("canary.services.goose.gas_metered.GasMeter") as MockGM:
                    with patch("canary.services.goose.gas_metered.WalletService") as MockWS:
                        MockGM.return_value.get_cost.return_value = 25
                        MockWS.return_value.get_wallet.return_value = mock_wallet
                        MockWS.return_value.debit.return_value = mock_tx

                        g.merchant_id = "merchant-broke"

                        @gas_metered("owl.query.basic")
                        def dummy_route():
                            return jsonify({"ok": True})

                        response = dummy_route()
                        # Debit was called (not blocked)
                        MockWS.return_value.debit.assert_called_once()
                        # Route executed (soft gate)
                        assert response.status_code == 200

    def test_skips_when_no_merchant_id(self, app, mock_session):
        """Metered request with no JWT context skips metering, passes through."""
        from canary.services.goose.gas_metered import gas_metered

        with app.test_request_context("/test"):
            # g.merchant_id not set
            with patch("canary.services.goose.gas_metered.get_session", return_value=mock_session):
                with patch("canary.services.goose.gas_metered.WalletService") as MockWS:

                    @gas_metered("owl.query.basic")
                    def dummy_route():
                        return jsonify({"ok": True})

                    response = dummy_route()
                    MockWS.return_value.get_wallet.assert_not_called()
                    assert response.status_code == 200

    def test_skips_when_zero_cost_operation(self, app, mock_session):
        """Metered request with unknown/free operation skips charge, passes through."""
        from canary.services.goose.gas_metered import gas_metered

        with app.test_request_context("/test"):
            with patch("canary.services.goose.gas_metered.get_session", return_value=mock_session):
                with patch("canary.services.goose.gas_metered.GasMeter") as MockGM:
                    with patch("canary.services.goose.gas_metered.WalletService") as MockWS:
                        MockGM.return_value.get_cost.return_value = 0

                        g.merchant_id = "merchant-abc"

                        @gas_metered("chirp.gold_list.fired")
                        def dummy_route():
                            return jsonify({"ok": True})

                        response = dummy_route()
                        MockWS.return_value.debit.assert_not_called()
                        assert response.status_code == 200

    def test_passes_through_on_db_error(self, app, mock_session):
        """DB error during charge logs error, passes through (never blocks)."""
        from canary.services.goose.gas_metered import gas_metered

        with app.test_request_context("/test"):
            with patch("canary.services.goose.gas_metered.get_session", return_value=mock_session):
                with patch("canary.services.goose.gas_metered.GasMeter") as MockGM:
                    with patch("canary.services.goose.gas_metered.WalletService") as MockWS:
                        MockGM.return_value.get_cost.return_value = 25
                        MockWS.return_value.get_wallet.side_effect = Exception("DB down")

                        g.merchant_id = "merchant-abc"

                        @gas_metered("owl.query.basic")
                        def dummy_route():
                            return jsonify({"ok": True})

                        response = dummy_route()
                        assert response.status_code == 200

    def test_sets_gas_context_on_request(self, app, mock_session):
        """Verify g.gas_cost and g.gas_wallet_status set on request context."""
        from canary.services.goose.gas_metered import gas_metered

        mock_wallet = MagicMock()
        mock_wallet.id = "wallet-123"
        mock_wallet.status = "warning"
        mock_wallet.balance_sats = 5000

        mock_tx = MagicMock()
        mock_tx.balance_after_sats = 4975

        with app.test_request_context("/test"):
            with patch("canary.services.goose.gas_metered.get_session", return_value=mock_session):
                with patch("canary.services.goose.gas_metered.GasMeter") as MockGM:
                    with patch("canary.services.goose.gas_metered.WalletService") as MockWS:
                        MockGM.return_value.get_cost.return_value = 25
                        MockWS.return_value.get_wallet.return_value = mock_wallet
                        MockWS.return_value.debit.return_value = mock_tx

                        g.merchant_id = "merchant-abc"

                        captured = {}

                        @gas_metered("owl.query.basic")
                        def dummy_route():
                            captured["cost"] = g.gas_cost
                            captured["status"] = g.gas_wallet_status
                            return jsonify({"ok": True})

                        dummy_route()
                        assert captured["cost"] == 25
                        assert captured["status"] == "warning"

    def test_auto_provision_does_not_mint_macaroon(self, app, mock_session):
        """Auto-provisioning creates wallet + funds but does NOT mint macaroon."""
        from canary.services.goose.gas_metered import gas_metered

        new_wallet = MagicMock()
        new_wallet.id = "new-wallet"
        new_wallet.status = "active"
        new_wallet.balance_sats = 100000

        mock_tx = MagicMock()
        mock_tx.balance_after_sats = 99975

        with app.test_request_context("/test"):
            with patch("canary.services.goose.gas_metered.get_session", return_value=mock_session):
                with patch("canary.services.goose.gas_metered.GasMeter") as MockGM:
                    with patch("canary.services.goose.gas_metered.WalletService") as MockWS:
                        with patch("canary.services.goose.gas_metered.TreasuryService") as MockTS:
                            with patch("canary.services.goose.gas_metered.MacaroonService", side_effect=Exception("should not be called")) as MockMS:
                                MockGM.return_value.get_cost.return_value = 25
                                MockWS.return_value.get_wallet.side_effect = [None, new_wallet]
                                MockWS.return_value.debit.return_value = mock_tx

                                g.merchant_id = "merchant-new"

                                @gas_metered("owl.query.basic")
                                def dummy_route():
                                    return jsonify({"ok": True})

                                # Should not raise — MacaroonService should never be instantiated
                                response = dummy_route()
                                assert response.status_code == 200
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/unit/test_gas_metered.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'canary.services.goose.gas_metered'`

- [ ] **Step 3: Commit test file**

```bash
git add tests/unit/test_gas_metered.py
git commit -m "test: add unit tests for @gas_metered decorator (RED)"
```

---

### Task 2: Implement `@gas_metered` decorator

**Files:**
- Create: `canary/services/goose/gas_metered.py`

- [ ] **Step 4: Write the decorator implementation**

```python
"""@gas_metered — soft-gate decorator for Goose gas metering.

Charges the merchant's wallet per-operation using the gas schedule.
Never blocks — always passes through, even on insufficient balance or errors.
This is metering, not gating.

Uses GasMeter.get_cost() for price lookup, then WalletService.debit() directly
(bypassing GasMeter.charge() which blocks on insufficient balance).

Auto-provisions wallets for merchants who predate Goose.
"""

import logging
import os
import uuid
from functools import wraps

from flask import g

logger = logging.getLogger("canary.gas_metered")


def gas_metered(operation_key: str):
    """Decorator that meters a route's gas cost against the merchant's wallet.

    Usage:
        @jwt_required
        @gas_metered("owl.query.basic")
        def my_route():
            # g.gas_cost and g.gas_wallet_status available
            ...

    Args:
        operation_key: The gas_schedule operation_key for this endpoint.
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # 1. Get merchant_id from JWT context
            merchant_id = getattr(g, "merchant_id", None)
            if not merchant_id:
                return f(*args, **kwargs)

            try:
                from canary.db.session_factory import get_session
                from canary.services.goose.gas_meter import GasMeter
                from canary.services.goose.wallet_service import WalletService
                from canary.models.app.merchant_wallet import MerchantWallet

                session = get_session()

                # 2. Look up cost
                gas_meter = GasMeter(session)
                cost = gas_meter.get_cost(operation_key)

                if cost == 0:
                    g.gas_cost = 0
                    g.gas_wallet_status = None
                    return f(*args, **kwargs)

                # 3. Get wallet
                wallet_svc = WalletService(session)
                wallet = wallet_svc.get_wallet(merchant_id)

                # 4. Auto-provision if no wallet
                if wallet is None:
                    wallet = _provision_wallet(session, wallet_svc, merchant_id)

                if wallet is None:
                    # Provision failed — skip metering, pass through
                    logger.error("Failed to provision wallet for %s", merchant_id)
                    return f(*args, **kwargs)

                # 5. Debit directly (soft gate — allows negative)
                tx = wallet_svc.debit(
                    wallet_id=wallet.id,
                    merchant_id=merchant_id,
                    amount_sats=cost,
                    operation_type=operation_key,
                    reference_id=str(uuid.uuid4()),
                    reference_type="http_request",
                )

                # 6. Log
                logger.info(
                    "gas_metered: merchant=%s op=%s cost=%d balance_after=%d status=%s",
                    merchant_id, operation_key, cost,
                    tx.balance_after_sats, wallet.status,
                )
                if wallet.status in ("depleted", "warning"):
                    logger.warning(
                        "gas_metered: wallet %s for merchant %s is %s (balance: %d)",
                        wallet.id, merchant_id, wallet.status, wallet.balance_sats,
                    )

                # 7. Set request context
                g.gas_cost = cost
                g.gas_wallet_status = wallet.status

                # 8. Commit the charge
                session.commit()

            except Exception:
                logger.exception("gas_metered: error charging %s for %s — passing through", operation_key, merchant_id)

            return f(*args, **kwargs)

        return decorated
    return decorator


def _provision_wallet(session, wallet_svc, merchant_id: str):
    """Create a wallet and fund it from treasury. No macaroon minting."""
    from canary.models.app.merchant_wallet import MerchantWallet
    from canary.services.goose.treasury import TreasuryService

    initial_sats = int(os.getenv("GOOSE_INITIAL_FUNDING_SATS", "100000"))

    wallet = MerchantWallet(
        merchant_id=merchant_id,
        balance_sats=0,
        status="active",
    )
    session.add(wallet)
    session.flush()  # Flush so treasury can find it

    treasury = TreasuryService(session)
    treasury.fund_merchant(merchant_id, initial_sats, note="auto-provisioned by gas_metered")

    # Re-fetch to get updated balance
    return wallet_svc.get_wallet(merchant_id)
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/unit/test_gas_metered.py -v`
Expected: 8 passed

- [ ] **Step 6: Commit**

```bash
git add canary/services/goose/gas_metered.py
git commit -m "feat(goose): @gas_metered decorator — soft-gate gas metering"
```

---

## Chunk 2: Route Integration

### Task 3: Add `@gas_metered` to Owl routes

**Files:**
- Modify: `canary/blueprints/owl_api.py`

- [ ] **Step 7: Add import at top of owl_api.py**

After line 27 (`from canary.middleware.jwt_auth import jwt_required`), add:

```python
from canary.services.goose.gas_metered import gas_metered
```

- [ ] **Step 8: Decorate 5 Owl routes**

Add `@gas_metered(...)` below each `@jwt_required` on these routes. The decorator goes AFTER `@jwt_required` (which sets `g.merchant_id`):

1. Line 75 — `one_thing()`: add `@gas_metered("owl.query.basic")` between `@jwt_required` and `def one_thing():`
2. Line 133 — `chat()`: add `@gas_metered("owl.query.basic")` between `@jwt_required` and `def chat():`
3. Line 295 — `health_check_report()`: add `@gas_metered("owl.health_check")` between `@jwt_required` and `def health_check_report():`
4. Line 437 — `execute_action()`: add `@gas_metered("owl.query.deep")` between `@jwt_required` and `def execute_action():`
5. Line 1142 — `owl_drill()`: add `@gas_metered("owl.query.deep")` between `@jwt_required` and `def owl_drill():`

Note: `@jwt_required` is used WITHOUT parentheses in this file. Match that convention.

- [ ] **Step 9: Commit**

```bash
git add canary/blueprints/owl_api.py
git commit -m "feat(goose): add gas metering to 5 Owl intelligence routes"
```

---

### Task 4: Add `@gas_metered` to Fox routes

**Files:**
- Modify: `canary/blueprints/fox_wired.py`

- [ ] **Step 10: Add import at top of fox_wired.py**

After line 5 (`from canary.middleware.jwt_auth import jwt_required, roles_required`), add:

```python
from canary.services.goose.gas_metered import gas_metered
```

- [ ] **Step 11: Decorate 2 Fox routes**

Add `@gas_metered(...)` AFTER `@roles_required(...)` on these routes:

1. Lines 42-44 — `create_case()`: add `@gas_metered("fox.case.created")` after `@roles_required("owner", "operator", "admin")` and before `def create_case():`
2. Lines 120-122 — `add_evidence()`: add `@gas_metered("fox.evidence.attached")` after `@roles_required("owner", "operator", "admin")` and before `def add_evidence(case_id):`

Note: `@jwt_required()` is used WITH parentheses in this file. Match that convention.

- [ ] **Step 12: Commit**

```bash
git add canary/blueprints/fox_wired.py
git commit -m "feat(goose): add gas metering to Fox case creation and evidence routes"
```

---

### Task 5: Add JWT + gas metering + merchant scoping to receipt routes

**Files:**
- Modify: `canary/blueprints/receipt_tsp.py`

- [ ] **Step 13: Add imports at top of receipt_tsp.py**

After line 14 (`from flask import Blueprint, jsonify`), add:

```python
from flask import g
from canary.middleware.jwt_auth import jwt_required
from canary.services.goose.gas_metered import gas_metered
```

- [ ] **Step 14: Decorate receipt routes with JWT + gas metering**

1. Line 23 — `receipt_by_hash()`: add `@jwt_required` and `@gas_metered("receipt.proof")` between the `@route` and `def`:

```python
@receipt_tsp_bp.route("/by-hash/<event_hash_hex>", methods=["GET"])
@jwt_required
@gas_metered("receipt.proof")
def receipt_by_hash(event_hash_hex: str):
```

2. Line 47 — `receipt_by_event_id()`: same pattern:

```python
@receipt_tsp_bp.route("/by-event/<event_id>", methods=["GET"])
@jwt_required
@gas_metered("receipt.proof")
def receipt_by_event_id(event_id: str):
```

- [ ] **Step 15: Add merchant scoping to `_build_receipt()` queries**

Update `_build_receipt()` function signature to accept and use `merchant_id`:

1. Change the function signature at line 65:
```python
def _build_receipt(event_hash_hex: str = None, event_id: str = None):
```
to:
```python
def _build_receipt(event_hash_hex: str = None, event_id: str = None, merchant_id: str = None):
```

2. Add merchant_id filter to the event_hash query (line 82-91). Change the SQL WHERE clause from:
```sql
WHERE event_hash = :hash
```
to:
```sql
WHERE event_hash = :hash AND merchant_id = :mid
```
And add `"mid": merchant_id` to the params dict.

3. Same change for the event_id query (line 93-103). Change:
```sql
WHERE event_id = :eid
```
to:
```sql
WHERE event_id = :eid AND merchant_id = :mid
```
And add `"mid": merchant_id` to the params dict.

4. Update the callers to pass `merchant_id=g.merchant_id`:

Line 44: `return _build_receipt(event_hash_hex=event_hash_hex, merchant_id=g.merchant_id)`
Line 56: `return _build_receipt(event_id=event_id, merchant_id=g.merchant_id)`

5. Update the docstring at the top of the file — remove the "Sprint 6: No L402 payment gate" comment and update to reflect current state.

- [ ] **Step 16: Commit**

```bash
git add canary/blueprints/receipt_tsp.py
git commit -m "feat(goose): add JWT auth + gas metering + merchant scoping to receipt routes"
```

---

## Chunk 3: Integration Tests

### Task 6: Write integration tests

**Files:**
- Create: `tests/integration/test_gas_metered_routes.py`

- [ ] **Step 17: Write integration test file**

```python
"""Integration tests for gas-metered routes.

Verifies:
1. Owl endpoint creates wallet_transaction on metered request
2. Receipt endpoint rejects unauthenticated requests
3. Receipt endpoint scopes lookups to merchant's own data
"""

import pytest
from unittest.mock import patch, MagicMock

from canary.db.session_factory import get_session
from canary.models.app.wallet_transaction import WalletTransaction
from canary.models.app.merchant_wallet import MerchantWallet


@pytest.mark.postgres
class TestGasMeteredRoutes:
    """Integration tests for gas-metered route wiring."""

    def test_owl_endpoint_creates_wallet_transaction(self, client, merchant_jwt):
        """JWT auth -> hit Owl endpoint -> verify wallet_transaction created."""
        # This test requires a seeded merchant + gas_schedule in the test DB.
        # The @gas_metered decorator will auto-provision a wallet.
        response = client.post(
            "/owl/one-thing",
            headers={"Authorization": f"Bearer {merchant_jwt}"},
            json={},
        )
        # Route may return various status codes depending on Owl state,
        # but should NOT be 401 (auth passed) and should NOT be 402 (soft gate)
        assert response.status_code != 401
        assert response.status_code != 402

        # Verify a wallet_transaction was created
        session = get_session()
        txns = (
            session.query(WalletTransaction)
            .filter_by(operation_type="owl.query.basic")
            .all()
        )
        assert len(txns) >= 1
        assert txns[-1].source == "gas_fee"
        assert txns[-1].amount_sats == 25  # from gas_schedule seed

    def test_receipt_rejects_unauthenticated(self, client):
        """Receipt endpoint returns 401 without JWT (previously public)."""
        response = client.get("/receipt/by-hash/" + "a" * 64)
        assert response.status_code == 401

    def test_receipt_scopes_to_own_merchant(self, client, merchant_jwt, other_merchant_jwt):
        """Receipt endpoint only returns data for the authenticated merchant."""
        # Look up a receipt belonging to the first merchant using the second merchant's JWT
        # Should return 404 (not found for that merchant), not the actual data
        response = client.get(
            "/receipt/by-hash/" + "a" * 64,
            headers={"Authorization": f"Bearer {other_merchant_jwt}"},
        )
        # Should be 404 (scoped to other merchant, won't find first merchant's data)
        assert response.status_code == 404
```

Note: These tests depend on the test database having seeded gas_schedule entries and test merchants. The existing `conftest.py` may need fixtures for `merchant_jwt` and `other_merchant_jwt`. Adapt to whatever the existing test infrastructure provides — check `tests/integration/conftest.py` for available fixtures.

- [ ] **Step 18: Run integration tests**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/test_gas_metered_routes.py -v -m postgres`
Expected: 3 passed (may need fixture adjustments)

- [ ] **Step 19: Run full unit test suite to check for regressions**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/unit/ -v`
Expected: All existing tests still pass

- [ ] **Step 20: Run full integration test suite**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/integration/ -v -m postgres`
Expected: All existing tests still pass

- [ ] **Step 21: Commit integration tests**

```bash
git add tests/integration/test_gas_metered_routes.py
git commit -m "test: add integration tests for gas-metered route wiring"
```

---

## Chunk 4: Final Verification

### Task 7: Verify and commit

- [ ] **Step 22: Run all Goose-related tests together**

Run: `cd ~/GrowDirect/Canary && python3 -m pytest tests/unit/test_gas_metered.py tests/unit/test_goose_*.py tests/integration/test_goose_*.py tests/integration/test_gas_metered_routes.py -v`
Expected: All pass (existing Goose tests + new gas metering tests)

- [ ] **Step 23: Verify no import errors in modified blueprints**

Run: `cd ~/GrowDirect/Canary && python3 -c "from canary.blueprints.owl_api import owl_api_bp; from canary.blueprints.fox_wired import fox_bp; from canary.blueprints.receipt_tsp import receipt_tsp_bp; print('All blueprints import cleanly')"`
Expected: "All blueprints import cleanly"

- [ ] **Step 24: Update Goose SDD with gas metering status**

In `docs/sdds/canary/goose.md`, update the L402 gaps table:
- Change L402-1 ("No endpoint uses `@l402_required`") to note that 9 endpoints now use `@gas_metered` for soft-gate metering. L402 hard gating remains deferred.
- Update Phase Roadmap: Phase 0.5 → "Gas metering on 9 routes" status = **Complete**

- [ ] **Step 25: Final commit**

```bash
git add docs/sdds/canary/goose.md
git commit -m "docs: update Goose SDD — gas metering wired to 9 endpoints"
```
