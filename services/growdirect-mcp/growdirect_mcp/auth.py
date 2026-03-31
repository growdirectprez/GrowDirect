"""Auth middleware — API key and JWT validation for MCP transports."""

import os
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)


class AuthError(Exception):
    """Raised when authentication fails."""
    pass


def validate_api_key(provided_key: Optional[str]) -> bool:
    if os.environ.get("MCP_AUTH_DISABLED", "").strip() == "1":
        return True

    expected_key = os.environ.get("MCP_API_KEY", "").strip()

    if not expected_key:
        raise AuthError("MCP_API_KEY not configured — set it or use MCP_AUTH_DISABLED=1 for trusted networks")

    if not provided_key:
        raise AuthError("API key required — set X-API-Key header or MCP_API_KEY param")

    if provided_key != expected_key:
        raise AuthError("Invalid API key")

    return True


def validate_jwt(token: str) -> dict[str, Any]:
    import jwt as pyjwt

    secret = os.environ.get("MCP_JWT_SECRET", "").strip()
    if not secret:
        raise AuthError("JWT validation not configured — set MCP_JWT_SECRET")

    try:
        claims = pyjwt.decode(token, secret, algorithms=["HS256"])
        return claims
    except pyjwt.InvalidTokenError as e:
        raise AuthError(f"Invalid JWT: {e}") from e
