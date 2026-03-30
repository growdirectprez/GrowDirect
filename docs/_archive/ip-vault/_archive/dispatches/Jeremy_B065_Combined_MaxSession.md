---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Jeremy Session Prompt — B-065 COMBINED MAX SESSION
**Work Orders:** B-065-A + B-065-B (collapsed)
**Date:** February 28, 2026
**Dispatched by:** ALX
**Priority:** 🔴 CRITICAL — Jeffe at keyboard, debug mode
**Session type:** Acquire + Build + Wire + Test

---

## Situation

Jeffe is at the keyboard. Debug live. Move fast.

Integration test passed 9/9 (Feb 27 s7). The only thing between us and the live heartbeat (B-064) is:
1. Square repos on disk so we know what we're working with
2. `canary-hooks` subscription pointed at a real URL (not webhook.site placeholder)
3. Signature key in `.env`
4. Merchant ID in `.env`
5. Flask confirmed receiving real Square test webhooks

Do all of it this session. Jeffe debugs whatever breaks.

---

## Context

- Sandbox credentials already in `.env`:
  - `SQUARE_APPLICATION_ID=sandbox-sq0idb-SduFLmiaE43X0BeFC37Taw`
  - `SQUARE_ACCESS_TOKEN=EAAAl3ns-vSWSvjgQL7KMKyTxoWP5PMPns6W2PP3pQ_43Fs8lf3_qHV_wyj693Rl`
  - `SQUARE_ENVIRONMENT=sandbox`
  - `SQUARE_WEBHOOK_SIGNATURE_KEY=` ← EMPTY, needs to be set
- `canary-hooks` subscription exists in Square Developer Dashboard (Sandbox)
- Current notification URL: webhook.site placeholder (Chrome is open to webhook.site — grab that URL)
- Integration test: 9/9 PASS using mock curl webhook (Feb 27 s7)
- Stack: Flask + PostgreSQL + Valkey via `docker-compose.alpha3x.yml`

---

## PHASE 1 — Clone Square Repos (do while stack starts)

```bash
mkdir -p /Users/geofflyle/GrowDirect/Canary/square
cd /Users/geofflyle/GrowDirect/Canary/square

# Priority 1 — these matter for today
git clone https://github.com/square/square-python-sdk.git
git clone https://github.com/square/connect-api-examples.git
git clone https://github.com/square/connect-api-specification.git

# Priority 2 — reference
git clone https://github.com/square/connect-python-sdk.git
```

Read immediately after clone:
```
connect-api-examples/connect-examples/oauth/python/oauth-flow.py
square-python-sdk/README.md  ← verify_signature section
```

---

## PHASE 2 — Start Stack + ngrok

```bash
cd /Users/geofflyle/GrowDirect/Canary

# Start stack
docker compose -f devops/docker-compose.alpha3x.yml up -d

# Confirm Flask port (check compose file if unsure)
docker compose -f devops/docker-compose.alpha3x.yml ps
```

In a **separate terminal**, start ngrok:
```bash
ngrok http <flask_port>
```

Copy the `https://` forwarding URL. This is `NGROK_URL` for the rest of the session.

---

## PHASE 3 — Verify OAuth Token + Get Merchant ID

```bash
curl https://connect.squareupsandbox.com/v2/merchants/me \
  -H "Authorization: Bearer EAAAl3ns-vSWSvjgQL7KMKyTxoWP5PMPns6W2PP3pQ_43Fs8lf3_qHV_wyj693Rl" \
  -H "Square-Version: 2026-01-22"
```

Copy the `id` field from the response. Write to `.env`:
```
SQUARE_MERCHANT_ID=<id_from_response>
```

---

## PHASE 4 — List Subscriptions + Get Subscription ID

```bash
curl https://connect.squareupsandbox.com/v2/webhooks/subscriptions \
  -H "Authorization: Bearer EAAAl3ns-vSWSvjgQL7KMKyTxoWP5PMPns6W2PP3pQ_43Fs8lf3_qHV_wyj693Rl" \
  -H "Square-Version: 2026-01-22"
```

Find `canary-hooks` in the response. Copy its `id`.

---

## PHASE 5 — Update Subscription URL via API

```bash
curl https://connect.squareupsandbox.com/v2/webhooks/subscriptions/<SUBSCRIPTION_ID> \
  -X PUT \
  -H "Authorization: Bearer EAAAl3ns-vSWSvjgQL7KMKyTxoWP5PMPns6W2PP3pQ_43Fs8lf3_qHV_wyj693Rl" \
  -H "Square-Version: 2026-01-22" \
  -H "Content-Type: application/json" \
  -d '{
    "subscription": {
      "notification_url": "https://<NGROK_URL>/webhooks/square",
      "name": "canary-hooks"
    }
  }'
```

Confirm response shows updated `notification_url`.

---

## PHASE 6 — Get Signature Key

**Two options — try API first:**

```bash
curl https://connect.squareupsandbox.com/v2/webhooks/subscriptions/<SUBSCRIPTION_ID> \
  -H "Authorization: Bearer EAAAl3ns-vSWSvjgQL7KMKyTxoWP5PMPns6W2PP3pQ_43Fs8lf3_qHV_wyj693Rl" \
  -H "Square-Version: 2026-01-22"
```

Look for `signature_key` in the response.

**If not in response:** Square Dashboard → Webhooks → canary-hooks → Endpoint Details → Show Signature Key. Copy it.

Write to `.env`:
```
SQUARE_WEBHOOK_SIGNATURE_KEY=<key>
SQUARE_NOTIFICATION_URL=https://<NGROK_URL>/webhooks/square
```

Restart Flask after `.env` update:
```bash
docker compose -f devops/docker-compose.alpha3x.yml restart canary
# or whatever the Flask service name is
```

---

## PHASE 7 — Build square_webhook_manager.py

Create `/Users/geofflyle/GrowDirect/Canary/canary/services/square_webhook_manager.py`

This replaces the dashboard for all future subscription management. Use the Square Python SDK — verify exact method names against the cloned `square-python-sdk` before writing. Pattern:

```python
"""
Square Webhook Subscription Manager
Manages webhook subscriptions programmatically via Square API.
Replaces manual dashboard interaction.

Usage:
  python -m canary.services.square_webhook_manager list
  python -m canary.services.square_webhook_manager update <subscription_id> <ngrok_url>
  python -m canary.services.square_webhook_manager create <ngrok_url>
  python -m canary.services.square_webhook_manager get <subscription_id>
"""
import os
import sys
import json
import uuid
from square import Square

client = Square(
    token=os.environ.get("SQUARE_ACCESS_TOKEN"),
    environment=os.environ.get("SQUARE_ENVIRONMENT", "sandbox"),
)

SUBSCRIPTION_NAME = "canary-hooks"
WEBHOOK_PATH = "/webhooks/square"
API_VERSION = "2026-01-22"

def list_subscriptions():
    # verify exact method name in square-python-sdk README
    pass

def get_subscription(subscription_id: str):
    pass

def update_subscription(subscription_id: str, ngrok_url: str):
    notification_url = ngrok_url.rstrip("/") + WEBHOOK_PATH
    # build update call from SDK
    pass

def create_subscription(ngrok_url: str):
    notification_url = ngrok_url.rstrip("/") + WEBHOOK_PATH
    # build create call with idempotency_key=str(uuid.uuid4())
    pass

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "list":
        list_subscriptions()
    elif cmd == "get" and len(sys.argv) == 3:
        get_subscription(sys.argv[2])
    elif cmd == "update" and len(sys.argv) == 4:
        update_subscription(sys.argv[2], sys.argv[3])
    elif cmd == "create" and len(sys.argv) == 3:
        create_subscription(sys.argv[2])
    else:
        print(__doc__)
```

Fill in the actual SDK calls from the cloned repo. Don't guess method names.

---

## PHASE 8 — Verify webhook.site vs TSP-01 verify_signature

Check how current Flask `/webhooks/square` does HMAC verification. Compare against:
- Square SDK `verify_signature` from `square-python-sdk`
- Square's own example at `connect-api-examples/connect-examples/oauth/python/oauth-flow.py`

If we're doing manual HMAC, consider switching to SDK helper. Flag for Jeffe if it requires changes to `blueprints/webhooks.py`.

---

## PHASE 9 — Send Test Webhook from Square Dashboard

In Square Developer Dashboard → Webhooks → canary-hooks → Send Test Event → `refund.created` → Send.

Watch Flask logs. Expected:
```
POST /webhooks/square  200
```

If 401: signature key mismatch — recheck `SQUARE_WEBHOOK_SIGNATURE_KEY` and `SQUARE_NOTIFICATION_URL` in `.env`. Jeffe is at keyboard — debug live.

If 200: B-064 next gate is now Jeffe's phone. The heartbeat is one real transaction away.

---

## PHASE 10 — Catalog (do last, non-blocking)

```bash
find /Users/geofflyle/GrowDirect/Canary/square -type f \
  \( -name "*.py" -o -name "*.md" -o -name "*.yaml" -o -name "*.json" \) \
  | sort > /Users/geofflyle/GrowDirect/Canary/square/SQUARE_ASSET_INDEX.txt
```

Write brief `SQUARE_SCAN_NOTES.md` — SDK version in cloned repo vs. `requirements.txt`, OAuth flow notes, anything worth flagging. Don't let this block Phases 1-9.

---

## Success Criteria

- [ ] Square repos cloned to `/Canary/square/`
- [ ] `SQUARE_MERCHANT_ID` in `.env`
- [ ] `canary-hooks` subscription updated with real ngrok URL via API
- [ ] `SQUARE_WEBHOOK_SIGNATURE_KEY` in `.env`
- [ ] `SQUARE_NOTIFICATION_URL` in `.env`
- [ ] Flask returns 200 on Square test webhook
- [ ] `square_webhook_manager.py` built and functional
- [ ] `SQUARE_ASSET_INDEX.txt` written

---

## Standing Directives

- B-063: SDK is `squareup` (no pin) — confirm version matches latest in cloned repo
- B-064: This session clears the path. Next gate is Jeffe's phone.
- Jeffe is at keyboard — debug live, move fast, don't stop to document mid-session

---

## Session Close

1. TRIAGE: update B-065-A, B-065-B, B-064 status
2. HANDOFF: what's in `.env`, subscription ID, what's ready for live transaction test
3. Timelog

---

*ALX | February 28, 2026 | B-065 COMBINED*
*Jeffe at keyboard. Go.*
