# Angel Webhook Scaffold

**Important:** Angel is a Cove module, not a standalone Flask app. This scaffold exists for reference and local development only.

## Architecture Note

Angel code lives in `~/GrowDirect/Cove/`, not in this directory:

| Component | Real Location |
|-----------|---------------|
| Flask app | `Cove/wsgi.py` and `Cove/cove/__init__.py` |
| Lead model | `Cove/cove/models/lead.py` |
| Webhook blueprint | `Cove/cove/angel/webhook_routes.py` |
| Database | `cove` (shared with Cove) |
| Port | 5002 (same as Cove) |

This scaffold in `Angel/` is provided for:
- Local development reference
- Understanding webhook structure
- Testing the integration pattern
- Documentation purposes

## Files in This Scaffold

```
Angel/
├── angel/
│   ├── __init__.py                 # Flask app factory
│   ├── config.py                   # Configuration classes (Dev, Test, Prod)
│   ├── models/
│   │   ├── __init__.py
│   │   └── lead.py                 # Lead model (schema reference)
│   └── routes/
│       ├── __init__.py
│       └── webhooks.py             # Webhook receiver with HMAC verification
├── wsgi.py                         # WSGI entry point
├── conftest.py                     # pytest fixtures
├── migrations/                     # Alembic migrations (reference)
├── tests/
│   ├── __init__.py
│   └── test_webhooks.py            # Webhook integration tests
└── WEBHOOK_SCAFFOLD.md             # This file
```

## Webhook Endpoint

The webhook receiver is at `POST /api/webhooks/lp`.

### Request Format

```json
{
  "first_name": "John",
  "last_name": "Smith",
  "email": "john@example.com",
  "phone": "555-0100",
  "interest_type": "buying",
  "message": "Looking for homes in Palos Verdes",
  "page_url": "https://angeliquelyle.com/properties",
  "id": "lp-internal-id"
}
```

### Security

The webhook requires HMAC-SHA256 signature verification:

```
POST /api/webhooks/lp HTTP/1.1
X-Webhook-Signature: sha256=<hex_digest>
Content-Type: application/json

{...}
```

The signature is computed as:
```
digest = HMAC-SHA256(request_body, LP_WEBHOOK_SECRET)
header = f"sha256={digest.hex()}"
```

Set `LP_WEBHOOK_SECRET` in your `.env`:
```
LP_WEBHOOK_SECRET=your-secret-from-luxury-presence
```

### Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success — lead created |
| 400 | Malformed request (empty or invalid JSON) |
| 401 | Invalid signature |
| 422 | Unprocessable — no contact information |
| 500 | Database error |

### Success Response

```json
{
  "status": "ok",
  "lead_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

## Lead Model

The `Lead` model captures form submissions with:

- **id**: UUID primary key
- **apn**: Assessor's Parcel Number (initially "UNKNOWN", enriched later)
- **first_name, last_name, email, phone**: Contact info
- **interest_type**: buying, selling, relocating, welcome_guide, exploring
- **message**: Free-form inquiry text
- **page_url**: Which Luxury Presence page the form was on
- **referrer**: HTTP referrer (if available)
- **raw_payload**: Full original JSON payload
- **lp_lead_id**: Luxury Presence internal lead ID
- **status**: Pipeline stage (new, contacted, qualified, converted, closed)
- **created_at, updated_at**: Timestamps

## Local Development

This scaffold can be run locally for testing:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install flask flask-sqlalchemy flask-session redis python-dotenv

# Create .env
cat > .env << EOF
SECRET_KEY=dev-secret-key
DATABASE_URL=postgresql://growdirect:growdirect_dev@localhost:5432/angel
VALKEY_URL=redis://localhost:6379/3
LP_WEBHOOK_SECRET=test-secret
FLASK_ENV=dev
EOF

# Run app
flask --app wsgi run --port 5000
```

Test the webhook:

```bash
curl -X POST http://localhost:5000/api/webhooks/lp \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Signature: sha256=<computed_signature>" \
  -d '{
    "first_name": "Test",
    "email": "test@example.com",
    "page_url": "https://angeliquelyle.com"
  }'
```

## Testing

Run tests with pytest:

```bash
pytest tests/test_webhooks.py -v
```

Tests cover:
- Health check endpoint
- Valid lead submission
- Signature verification (valid and invalid)
- Missing contact info
- Full name parsing
- Optional fields

## Integration with Real Cove App

To integrate this webhook into the real Cove app (where Angel actually lives):

1. Lead model is already in `Cove/cove/models/lead.py`
2. Webhook blueprint is already in `Cove/cove/angel/webhook_routes.py`
3. Both are registered in `Cove/cove/__init__.py`
4. Database: `cove` (Valkey DB 1)
5. Port: 5002

The real implementation is identical to this scaffold but integrated into the Cove Flask app lifecycle.

## Architecture Diagram

```
Luxury Presence Dashboard
  │
  ├─── Custom Webhook Script
  │    └─ POST /api/webhooks/lp
  │
Cove Flask (port 5002)
  │
  ├─── angel_webhook_bp
  │    │
  │    ├─ POST /api/webhooks/lp (signature verification)
  │    │  └─ Create Lead in cove DB
  │    │
  │    └─ GET /api/webhooks/health
  │
  ├─── angel_chat_bp (chat widget proxy)
  ├─── angel_web_bp (content engine)
  │
Cove Database (PostgreSQL)
  │
  └─── leads table
       └─ [lead records from LP forms]
```

## Key Differences: Scaffold vs Real

| Aspect | Scaffold | Real (Cove) |
|--------|----------|-----------|
| Location | Angel/ | Cove/cove/angel/ |
| Database | angel or angel_test | cove or cove_test |
| Port | 5000 (dev) or 5001 | 5002 (Cove) |
| Valkey DB | 3 | 1 (shared with Cove) |
| App context | Standalone Flask app | Blueprint in Cove app |
| Deployment | Not deployed | Deployed as part of Cove |

---

*Angel Webhook Scaffold | GrowDirect Inc. | Reference only — real code lives in Cove*
