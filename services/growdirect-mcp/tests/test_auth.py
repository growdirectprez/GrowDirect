"""Tests for auth middleware — API key, JWT validation, and no-auth opt-in."""

import os
import pytest
from growdirect_mcp.auth import validate_api_key, validate_jwt, AuthError


def test_validate_api_key_passes_with_correct_key(monkeypatch):
    monkeypatch.setenv("MCP_API_KEY", "test-secret-key")
    assert validate_api_key("test-secret-key") is True


def test_validate_api_key_raises_on_wrong_key(monkeypatch):
    monkeypatch.setenv("MCP_API_KEY", "test-secret-key")
    with pytest.raises(AuthError, match="Invalid API key"):
        validate_api_key("wrong-key")


def test_validate_api_key_raises_on_missing_key(monkeypatch):
    monkeypatch.setenv("MCP_API_KEY", "test-secret-key")
    with pytest.raises(AuthError, match="API key required"):
        validate_api_key(None)


def test_validate_api_key_raises_on_empty_key(monkeypatch):
    monkeypatch.setenv("MCP_API_KEY", "test-secret-key")
    with pytest.raises(AuthError, match="API key required"):
        validate_api_key("")


def test_validate_api_key_rejects_when_no_env_key(monkeypatch):
    monkeypatch.delenv("MCP_API_KEY", raising=False)
    monkeypatch.delenv("MCP_AUTH_DISABLED", raising=False)
    with pytest.raises(AuthError, match="MCP_API_KEY not configured"):
        validate_api_key("any-key")


def test_validate_api_key_allows_when_auth_explicitly_disabled(monkeypatch):
    monkeypatch.delenv("MCP_API_KEY", raising=False)
    monkeypatch.setenv("MCP_AUTH_DISABLED", "1")
    assert validate_api_key(None) is True


def test_validate_jwt_passes_with_valid_token(monkeypatch):
    monkeypatch.setenv("MCP_JWT_SECRET", "test-jwt-secret")
    import jwt
    token = jwt.encode({"sub": "service-a", "iss": "growdirect"}, "test-jwt-secret", algorithm="HS256")
    claims = validate_jwt(token)
    assert claims["sub"] == "service-a"


def test_validate_jwt_raises_on_invalid_token(monkeypatch):
    monkeypatch.setenv("MCP_JWT_SECRET", "test-jwt-secret")
    with pytest.raises(AuthError, match="Invalid JWT"):
        validate_jwt("garbage-token")


def test_validate_jwt_raises_when_no_secret(monkeypatch):
    monkeypatch.delenv("MCP_JWT_SECRET", raising=False)
    with pytest.raises(AuthError, match="JWT validation not configured"):
        validate_jwt("any-token")
