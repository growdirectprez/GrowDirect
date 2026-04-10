"""Angel app configuration.

Note: Angel code actually lives in Cove (Angel is a Cove module).
Real config is in ~/GrowDirect/Cove/cove/config.py.
This file provided for scaffolding reference.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    """Base configuration — inherited by all environments."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-prod")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/angel",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True, "pool_recycle": 300}

    # Session backend — Valkey is Redis-compatible
    SESSION_TYPE = "redis"
    SESSION_REDIS = None  # Set from VALKEY_URL in create_app
    VALKEY_URL = os.environ.get(
        "VALKEY_URL", "redis://growdirect_valkey:6379/3"
    )  # Angel uses Valkey DB 3

    # Security
    WTF_CSRF_ENABLED = True
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB

    # Webhook secret for LP HMAC verification
    LP_WEBHOOK_SECRET = os.environ.get("LP_WEBHOOK_SECRET", "")


class DevConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True
    SESSION_COOKIE_SECURE = False


class TestConfig(BaseConfig):
    """Test configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL",
        "postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/angel_test",
    )
    WTF_CSRF_ENABLED = False
    SESSION_TYPE = "null"  # Use Flask default cookie session in tests
    SQLALCHEMY_ENGINE_OPTIONS = {}  # Disable pool options in tests


class ProdConfig(BaseConfig):
    """Production configuration."""

    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True


class StagingConfig(ProdConfig):
    """Staging inherits production security."""

    pass


config_by_name = {
    "dev": DevConfig,
    "development": DevConfig,
    "test": TestConfig,
    "testing": TestConfig,
    "staging": StagingConfig,
    "prod": ProdConfig,
    "production": ProdConfig,
}
