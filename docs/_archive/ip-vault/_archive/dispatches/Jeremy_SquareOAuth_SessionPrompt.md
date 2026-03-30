---
type: workorder
domain: canary
status: archived
created: 2026-03-18
updated: 2026-03-19
---
# Jeremy Session Prompt — Square OAuth Connection (Sandbox Merchant)
**Work Order:** B-065-B
**Date:** February 28, 2026
**Dispatched by:** ALX
**Priority:** HIGH — blocks live webhook test (B-064)
**Session type:** Integration build
**Depends on:** B-065-A (Square GitHub scan — read oauth-flow.py first)

---

## Context

We need a working OAuth connection from our Canary application to Jeffe's GrowDirect Lab sandbox merchant account. The sandbox subscription (`canary-hooks`) is already created in the Square Developer Dashboard. The webhook.site URL is a temporary placeholder — this session replaces it with our real ngrok endpoint and completes the OAuth handshake.

**What we have:**
- Sandbox app credentials in `.env`:
  - `SQUARE_APPLICATION_ID=sandbox-sq0idb-SduFLmiaE43X0BeFC37Taw`
  - `SQUARE_ACCESS_TOKEN=EAAAl3ns-vSWSvjgQL7KMKyTxoWP5PMPns6W2PP3pQ_43Fs8lf3_qHV_wyj693Rl`
  - `SQUARE_ENVIRONMENT=sandbox`
  - `SQUARE_WEBHOOK_SIGNATURE_KEY=` ← still needs to be set
- Webhook subscription `canary-hooks` created in Square Developer Dashboard (Sandbox)
- Notification URL: currently webhook.site placeholder — needs to be updated to ngrok URL
- Chrome is open to `https://webhook.site` on Jeffe's machine — the unique URL is visible there

**What we need after this session:**
- Flask endpoint at `/webhooks/square` confirmed reachable via ngrok
- Square subscription `canary-hooks` updated with real ngrok URL
- `SQUARE_WEBHOOK_SIGNATURE_KEY` captured from Square Dashboard and written to `.env`
- OAuth access token confirmed valid for sandbox merchant (GrowDirect Lab)
- Webhook subscription created/updated via Square API (not just dashboard)

---

## Step 1 — Read First

Before writing any code, read:
```
/Users/geofflyle/GrowDirect/Canary/square/connect-api-examples/connect-examples/oauth/python/oauth-flow.py
```

This is Square's reference OAuth implementation in Python. Understand the full flow before proceeding.

Also read:
```
/Users/geofflyle/GrowDirect/Canary/square/square-python-sdk/README.md
```
Specifically: OAuth section and `verify_signature` webhook helper.

---

## Step 2 — Start the Stack

```bash
cd /Users/geofflyle/GrowDirect/Canary
docker compose -f devops/docker-compose.alpha3x.yml up -d
```

Verify Flask is running:
```bash
curl http://localhost:5000/health
# or whichever port Flask is on — check docker-compose.alpha3x.yml if unsure
```

---

## Step 3 — Start ngrok

In a separate terminal:
```bash
ngrok http <flask_port>
```

Copy the `https://` forwarding URL. This is your `NGROK_URL` for the rest of this session.

---

## Step 4 — Update the Webhook Subscription URL

Use the Square API to update the `canary-hooks` subscription with the real ngrok URL. Do NOT do this manually in the dashboard.

First, list existing subscriptions to get the subscription ID:

```bash
curl https://connect.squareupsandbox.com/v2/webhooks/subscriptions \
  -H "Authorization: Bearer $SQUARE_ACCESS_TOKEN" \
  -H "Square-Version: 2026-01-22"
```

Note the `id` of the `canary-hooks` subscription.

Then update it:

```bash
curl https://connect.squareupsandbox.com/v2/webhooks/subscriptions/<SUBSCRIPTION_ID> \
  -X PUT \
  -H "Authorization: Bearer $SQUARE_ACCESS_TOKEN" \
  -H "Square-Version: 2026-01-22" \
  -H "Content-Type: application/json" \
  -d '{
    "subscription": {
      "notification_url": "https://<NGROK_URL>/webhooks/square",
      "name": "canary-hooks"
    }
  }'
```

---

## Step 5 — Get the Signature Key

In Square Developer Dashboard → Webhooks → canary-hooks → Endpoint Details → Show Signature Key.

Copy the key and write it to `.env`:
```
SQUARE_WEBHOOK_SIGNATURE_KEY=<key_from_dashboard>
```

Also set:
```
SQUARE_NOTIFICATION_URL=https://<NGROK_URL>/webhooks/square
```

Restart Flask after `.env` update.

---

## Step 6 — Automate Webhook Subscription Management

Create a new utility script at:
```
/Users/geofflyle/GrowDirect/Canary/canary/services/square_webhook_manager.py
```

This script handles webhook subscription lifecycle via the Square API:

```python
"""
Square Webhook Subscription Manager
Manages webhook subscriptions programmatically via Square API.
Use this instead of the dashboard for subscription create/update/list.

Usage:
  python -m canary.services.square_webhook_manager list
  python -m canary.services.square_webhook_manager update <subscription_id> <ngrok_url>
  python -m canary.services.square_webhook_manager create <ngrok_url>
  python -m canary.services.square_webhook_manager get_signature_key <subscription_id>
"""

import os
import sys
import json
from square import Square

# Build using existing .env credentials
client = Square(
    token=os.environ.get("SQUARE_ACCESS_TOKEN"),
    environment=os.environ.get("SQUARE_ENVIRONMENT", "sandbox"),
)

SUBSCRIPTION_NAME = "canary-hooks"
ALL_EVENTS = "*"  # Square supports wildcard — confirm in SDK docs

def list_subscriptions():
    """List all webhook subscriptions for this application."""
    result = client.webhook_subscriptions.list()
    print(json.dumps(result, indent=2, default=str))

def update_subscription(subscription_id: str, ngrok_url: str):
    """Update the notification URL for an existing subscription."""
    notification_url = f"{ngrok_url}/webhooks/square"
    result = client.webhook_subscriptions.update(
        subscription_id=subscription_id,
        body={
            "subscription": {
                "notification_url": notification_url,
                "name": SUBSCRIPTION_NAME,
            }
        }
    )
    print(f"Updated subscription URL to: {notification_url}")
    print(json.dumps(result, indent=2, default=str))

def create_subscription(ngrok_url: str):
    """Create a new canary-hooks webhook subscription."""
    import uuid
    notification_url = f"{ngrok_url}/webhooks/square"
    result = client.webhook_subscriptions.create(
        body={
            "idempotency_key": str(uuid.uuid4()),
            "subscription": {
                "name": SUBSCRIPTION_NAME,
                "notification_url": notification_url,
                "api_version": "2026-01-22",
                "enabled": True,
            }
        }
    )
    print(f"Created subscription at: {notification_url}")
    print(json.dumps(result, indent=2, default=str))

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "list":
        list_subscriptions()
    elif cmd == "update" and len(sys.argv) == 4:
        update_subscription(sys.argv[2], sys.argv[3])
    elif cmd == "create" and len(sys.argv) == 3:
        create_subscription(sys.argv[2])
    else:
        print(__doc__)
```

**Verify the Square Python SDK method names against the cloned repo** before finalizing — method names above are approximations based on SDK patterns. Correct them to match `square-python-sdk` actual API.

---

## Step 7 — Verify OAuth Token is Valid

Confirm the sandbox access token works for the GrowDirect Lab merchant:

```bash
curl https://connect.squareupsandbox.com/v2/merchants/me \
  -H "Authorization: Bearer $SQUARE_ACCESS_TOKEN" \
  -H "Square-Version: 2026-01-22"
```

Expected: returns merchant profile with `id` matching the `merchant_id` in webhook payloads.

Note the `merchant_id` value — write it to `.env` as:
```
SQUARE_MERCHANT_ID=<merchant_id_from_response>
```

This is the merchant_id the TSP pipeline expects to find in incoming webhook payloads (per TSP-01 §processing sequence step 8).

---

## Step 8 — Send Test Webhook

Once Stack + ngrok + signature key are all in place:

In Square Developer Dashboard → Webhooks → canary-hooks → Send Test Event → select `refund.created` → Send.

Watch Flask logs. You should see:
```
POST /webhooks/square  200
```

If you see 401: signature key mismatch. Double-check `SQUARE_WEBHOOK_SIGNATURE_KEY` and `SQUARE_NOTIFICATION_URL` in `.env`.

---

## OAuth Notes for Future Sessions

The current setup uses the **sandbox access token directly** — this is acceptable for sandbox testing (it acts as a pre-authorized merchant connection). Full OAuth flow (authorization code, redirect, token exchange, refresh) is needed for:

1. Production merchant onboarding (any merchant that isn't Jeffe)
2. Multi-merchant support (Sprint 7+)

The Square OAuth Python example at `connect-api-examples/connect-examples/oauth/python/oauth-flow.py` is the template for that future build. Flag in HANDOFF.md when ready to tackle it.

---

## Success Criteria

- [ ] Square API returns valid merchant profile for GrowDirect Lab sandbox account
- [ ] `canary-hooks` subscription updated with real ngrok URL via API (not dashboard)
- [ ] `SQUARE_WEBHOOK_SIGNATURE_KEY` written to `.env`
- [ ] `SQUARE_MERCHANT_ID` written to `.env`
- [ ] Flask returns 200 on test webhook from Square Dashboard
- [ ] `square_webhook_manager.py` created and functional
- [ ] SQUARE_SCAN_NOTES.md updated with OAuth findings

---

## Standing Directives

- B-064 is still the gate: live webhook test from real transaction (Jeffe's phone) comes after this session
- All external comms: Syd reviews, Jeffe approves — no scope additions without joint decision
- MVP scope is frozen — this session is infrastructure plumbing, not feature work
- Verify `squareup` SDK version per B-063 — flag any version gaps

---

## Session Close

1. Update TRIAGE.md: B-065-B status
2. Update HANDOFF.md: OAuth/webhook subscription status, what's in `.env`, what's pending
3. Note `SQUARE_MERCHANT_ID` value for B-064 (live transaction test)

---

*ALX | February 28, 2026 | B-065-B*
*Feeds: B-064 (live webhook test — this unblocks it)*
