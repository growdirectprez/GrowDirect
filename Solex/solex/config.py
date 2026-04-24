import os


def _psycopg3_url(raw: str) -> str:
    """Ensure the URL uses the psycopg3 driver scheme (postgresql+psycopg://)."""
    if raw.startswith("postgresql://") or raw.startswith("postgres://"):
        return raw.replace("postgresql://", "postgresql+psycopg://", 1).replace(
            "postgres://", "postgresql+psycopg://", 1
        )
    return raw


class BaseConfig:
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = _psycopg3_url(os.environ["DATABASE_URL"])
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    VALKEY_URL = os.environ["VALKEY_URL"]
    SESSION_TYPE = "redis"
    SESSION_KEY_PREFIX = "solex:session:"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = 7 * 24 * 3600
    WTF_CSRF_TIME_LIMIT = None
    SQUARE_ENVIRONMENT = os.environ.get("SQUARE_ENVIRONMENT", "sandbox")
    SQUARE_APPLICATION_ID = os.environ.get("SQUARE_SANDBOX_APPLICATION_ID", "")
    SQUARE_ACCESS_TOKEN = os.environ.get("SQUARE_SANDBOX_ACCESS_TOKEN", "")
    SQUARE_LOCATION_ID = os.environ.get("SQUARE_SANDBOX_LOCATION_ID", "")
    SQUARE_WEBHOOK_SIGNATURE_KEY = os.environ.get("SQUARE_SANDBOX_WEBHOOK_SIGNATURE_KEY", "")
    SMTP_HOST = os.environ.get("SMTP_HOST", "localhost")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", "1025"))
    SMTP_FROM = os.environ.get("SMTP_FROM", "orders@solex.local")
    TAX_RATE_PCT = float(os.environ.get("TAX_RATE_PCT", "0.0"))
    SHIPPING_FLAT_CENTS = int(os.environ.get("SHIPPING_FLAT_CENTS", "695"))
    SHIPPING_FREE_THRESHOLD_CENTS = int(os.environ.get("SHIPPING_FREE_THRESHOLD_CENTS", "9900"))


class DevConfig(BaseConfig):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True


class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = _psycopg3_url(os.environ.get(
        "TEST_DATABASE_URL",
        os.environ.get("DATABASE_URL", "") + "_test",
    ))
    WTF_CSRF_ENABLED = False


class ProdConfig(BaseConfig):
    DEBUG = False


def resolve_config():
    env = os.environ.get("SOLEX_ENV", "development").lower()
    match env:
        case "development": return DevConfig
        case "testing":     return TestConfig
        case "production":  return ProdConfig
        case _: raise ValueError(f"Invalid SOLEX_ENV: {env}")
