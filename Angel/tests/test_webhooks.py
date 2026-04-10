"""Test suite for Angel webhook endpoints.

Tests webhook signature verification, payload normalization, and lead creation.

Note: Angel code actually lives in Cove (Angel is a Cove module).
Real webhook tests are in ~/GrowDirect/Cove/tests/.
This file provided for scaffolding reference.
"""

import json
import hmac
import hashlib
import pytest
from angel.models.lead import Lead


def sign_payload(payload_bytes, secret):
    """Sign payload using HMAC-SHA256."""
    digest = hmac.new(secret, payload_bytes, hashlib.sha256).hexdigest()
    return f"sha256={digest}"


class TestLPWebhook:
    """Test LP webhook endpoint."""

    def test_health_check(self, client):
        """Test webhook health endpoint."""
        response = client.get("/api/webhooks/health")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "ok"
        assert "timestamp" in data

    def test_valid_lead_submission(self, client, app):
        """Test valid LP lead submission with full contact info."""
        payload = {
            "first_name": "John",
            "last_name": "Smith",
            "email": "john@example.com",
            "phone": "555-0100",
            "interest_type": "buying",
            "message": "Looking for a home on the Hill",
            "page_url": "https://angeliquelyle.com/properties",
            "id": "lp-12345",
        }

        payload_bytes = json.dumps(payload).encode()
        secret = app.config.get("LP_WEBHOOK_SECRET", "test-secret").encode()
        signature = sign_payload(payload_bytes, secret)

        with app.app_context():
            app.config["LP_WEBHOOK_SECRET"] = "test-secret"

            response = client.post(
                "/api/webhooks/lp",
                data=payload_bytes,
                content_type="application/json",
                headers={"X-Webhook-Signature": signature},
            )

            assert response.status_code == 200
            data = response.get_json()
            assert data["status"] == "ok"
            assert "lead_id" in data

            # Verify lead was created
            lead = Lead.query.filter_by(email="john@example.com").first()
            assert lead is not None
            assert lead.first_name == "John"
            assert lead.last_name == "Smith"
            assert lead.status == "new"
            assert lead.lp_lead_id == "lp-12345"

    def test_missing_signature(self, client):
        """Test request without signature header."""
        payload = {"first_name": "Jane", "email": "jane@example.com"}
        payload_bytes = json.dumps(payload).encode()

        response = client.post(
            "/api/webhooks/lp",
            data=payload_bytes,
            content_type="application/json",
        )

        assert response.status_code == 401
        data = response.get_json()
        assert "Invalid signature" in data.get("error", "")

    def test_invalid_signature(self, client, app):
        """Test request with invalid signature."""
        payload = {"first_name": "Jane", "email": "jane@example.com"}
        payload_bytes = json.dumps(payload).encode()

        with app.app_context():
            app.config["LP_WEBHOOK_SECRET"] = "test-secret"

            response = client.post(
                "/api/webhooks/lp",
                data=payload_bytes,
                content_type="application/json",
                headers={"X-Webhook-Signature": "sha256=invalid_digest"},
            )

            assert response.status_code == 401

    def test_no_contact_info(self, client, app):
        """Test payload with no contact information."""
        payload = {"interest_type": "buying", "message": "No contact info"}

        payload_bytes = json.dumps(payload).encode()
        secret = app.config.get("LP_WEBHOOK_SECRET", "test-secret").encode()
        signature = sign_payload(payload_bytes, secret)

        with app.app_context():
            app.config["LP_WEBHOOK_SECRET"] = "test-secret"

            response = client.post(
                "/api/webhooks/lp",
                data=payload_bytes,
                content_type="application/json",
                headers={"X-Webhook-Signature": signature},
            )

            assert response.status_code == 422
            data = response.get_json()
            assert "No contact information" in data.get("error", "")

    def test_full_name_parsing(self, client, app):
        """Test parsing full name from 'name' field."""
        payload = {
            "name": "Alice Johnson",
            "email": "alice@example.com",
            "page_url": "https://angeliquelyle.com",
        }

        payload_bytes = json.dumps(payload).encode()
        secret = app.config.get("LP_WEBHOOK_SECRET", "test-secret").encode()
        signature = sign_payload(payload_bytes, secret)

        with app.app_context():
            app.config["LP_WEBHOOK_SECRET"] = "test-secret"

            response = client.post(
                "/api/webhooks/lp",
                data=payload_bytes,
                content_type="application/json",
                headers={"X-Webhook-Signature": signature},
            )

            assert response.status_code == 200

            lead = Lead.query.filter_by(email="alice@example.com").first()
            assert lead is not None
            assert lead.first_name == "Alice"
            assert lead.last_name == "Johnson"

    def test_optional_fields(self, client, app):
        """Test that optional fields are captured correctly."""
        payload = {
            "first_name": "Bob",
            "last_name": "Builder",
            "email": "bob@example.com",
            "interest_type": "selling",
            "message": "Ready to sell my Palos Verdes home",
            "page_url": "https://angeliquelyle.com/sellers",
            "referrer": "https://google.com",
        }

        payload_bytes = json.dumps(payload).encode()
        secret = app.config.get("LP_WEBHOOK_SECRET", "test-secret").encode()
        signature = sign_payload(payload_bytes, secret)

        with app.app_context():
            app.config["LP_WEBHOOK_SECRET"] = "test-secret"

            response = client.post(
                "/api/webhooks/lp",
                data=payload_bytes,
                content_type="application/json",
                headers={"X-Webhook-Signature": signature},
            )

            assert response.status_code == 200

            lead = Lead.query.filter_by(email="bob@example.com").first()
            assert lead is not None
            assert lead.interest_type == "selling"
            assert lead.message == "Ready to sell my Palos Verdes home"
            assert lead.page_url == "https://angeliquelyle.com/sellers"
