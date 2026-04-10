"""Angel webhook blueprint — receives lead events from Luxury Presence.

LP Custom Webhook sends POST requests when forms are submitted on
AngeliqueLyle.com. This endpoint:
  1. Validates HMAC signature (LP sends X-Webhook-Signature)
  2. Normalizes the payload
  3. Creates a Lead record in the database
  4. Returns 200 OK (LP retries on non-2xx)

Note: Angel code actually lives in Cove (Angel is a Cove module).
Real webhook implementation is in ~/GrowDirect/Cove/cove/angel/webhook_routes.py.
This file provided for scaffolding reference.
"""

import logging
import hmac
import hashlib
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from angel import db
from angel.models.lead import Lead

logger = logging.getLogger(__name__)

angel_webhook_bp = Blueprint("angel_webhook", __name__)


def verify_webhook_signature(payload_bytes, signature_header):
    """Verify HMAC-SHA256 signature from LP webhook.

    LP sends X-Webhook-Signature header with format:
      sha256=<hex_digest>

    We compute HMAC-SHA256(payload_bytes, secret_key) and compare.
    """
    if not signature_header:
        logger.warning("Webhook: missing X-Webhook-Signature header")
        return False

    # Extract algorithm and digest
    parts = signature_header.split("=", 1)
    if len(parts) != 2:
        logger.warning("Webhook: invalid signature format: %s", signature_header)
        return False

    algo, provided_digest = parts

    if algo != "sha256":
        logger.warning("Webhook: unsupported algorithm: %s", algo)
        return False

    secret = current_app.config.get("LP_WEBHOOK_SECRET", "").encode()
    if not secret:
        logger.error("Webhook: LP_WEBHOOK_SECRET not configured")
        return False

    # Compute expected digest
    expected_digest = hmac.new(secret, payload_bytes, hashlib.sha256).hexdigest()

    # Constant-time comparison
    return hmac.compare_digest(expected_digest, provided_digest)


@angel_webhook_bp.route("/lp", methods=["POST"])
def receive_lp_lead():
    """Receive a lead from Luxury Presence Custom Webhook.

    Expects JSON payload with fields:
      - name (or first_name/last_name)
      - email
      - phone
      - interest_type (optional: buying, selling, relocating, welcome_guide, exploring)
      - message (optional: inquiry message)
      - page_url (optional: which page the form was on)
      - source_url (alternative key for page_url)

    Returns:
      - 200 OK + {status, lead_id} on success
      - 401 Unauthorized if signature invalid
      - 400 Bad Request if malformed
      - 422 Unprocessable Entity if no contact info
    """
    # Get raw request body for signature verification
    raw_payload = request.get_data()

    # Verify signature
    signature = request.headers.get("X-Webhook-Signature")
    if not verify_webhook_signature(raw_payload, signature):
        logger.warning("Webhook: signature verification failed from %s", request.remote_addr)
        return jsonify({"error": "Invalid signature"}), 401

    # Parse JSON
    payload = request.get_json(silent=True)
    if not payload:
        logger.warning("Webhook: empty or malformed JSON")
        return jsonify({"error": "Empty payload"}), 400

    # Extract contact info (normalize field names)
    first_name = payload.get("first_name") or ""
    last_name = payload.get("last_name") or ""

    # If name field is provided instead, split it
    if not (first_name or last_name):
        full_name = payload.get("name") or payload.get("full_name") or ""
        if full_name:
            parts = full_name.strip().split(None, 1)  # Split on first whitespace
            first_name = parts[0]
            last_name = parts[1] if len(parts) > 1 else ""

    email = (payload.get("email") or "").strip()
    phone = (payload.get("phone") or payload.get("phone_number") or "").strip()

    # Require at least one contact field
    if not (first_name or last_name or email or phone):
        logger.warning("Webhook: no contact info in payload")
        return jsonify({"error": "No contact information provided"}), 422

    # Extract optional fields
    interest_type = (payload.get("interest_type") or "").strip()
    message = (payload.get("message") or "").strip()
    page_url = (payload.get("page_url") or payload.get("source_url") or "").strip()

    # Create lead record
    try:
        lead = Lead(
            apn="UNKNOWN",  # Will be enriched later via APN lookup
            first_name=first_name or None,
            last_name=last_name or None,
            email=email or None,
            phone=phone or None,
            interest_type=interest_type or None,
            message=message or None,
            page_url=page_url or None,
            status="new",
            lp_lead_id=payload.get("id") or payload.get("lead_id"),  # LP internal ID if provided
            raw_payload=payload,
        )

        db.session.add(lead)
        db.session.commit()

        logger.info(
            "Webhook: lead created %s (%s %s / %s)",
            lead.id[:8],
            first_name,
            last_name,
            email,
        )

        return jsonify({"status": "ok", "lead_id": lead.id}), 200

    except Exception as e:
        logger.exception("Webhook: database error creating lead: %s", e)
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500


@angel_webhook_bp.route("/health", methods=["GET"])
def webhook_health():
    """Health check for webhook endpoint."""
    return jsonify({"status": "ok", "timestamp": datetime.utcnow().isoformat()}), 200
