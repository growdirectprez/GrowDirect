"""VIVA configuration — env-based, four classes."""

import os


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/viva",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = "redis"
    WTF_CSRF_ENABLED = True

    # VIVA-specific
    VIVA_PHASE = os.getenv("VIVA_PHASE", "research")  # research | validation | production
    VIVA_PAPER_MODE = os.getenv("VIVA_PAPER_MODE", "true").lower() == "true"
    VIVA_MAX_POSITION_PCT = float(os.getenv("VIVA_MAX_POSITION_PCT", "0.30"))  # 30% per strategy
    VIVA_KILL_SWITCH_PCT = float(os.getenv("VIVA_KILL_SWITCH_PCT", "0.15"))  # -15% drawdown
    VIVA_CORRELATION_THRESHOLD = float(os.getenv("VIVA_CORRELATION_THRESHOLD", "0.70"))
    VIVA_DEPLOYED_CAPITAL_SATS = int(os.getenv("VIVA_DEPLOYED_CAPITAL_SATS", "0"))  # 0 = paper mode


class DevConfig(BaseConfig):
    DEBUG = True
    VIVA_PAPER_MODE = True  # Always paper in dev


class TestConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://growdirect:growdirect_dev@growdirect_postgres:5432/viva_test",
    )
    VIVA_PAPER_MODE = True  # Always paper in test


class ProdConfig(BaseConfig):
    DEBUG = False
    SECRET_KEY = os.environ["SECRET_KEY"]
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    # VIVA_PAPER_MODE controlled by env — must be explicitly set to false


config_by_name = {
    "dev": DevConfig,
    "development": DevConfig,
    "test": TestConfig,
    "testing": TestConfig,
    "prod": ProdConfig,
    "production": ProdConfig,
}
