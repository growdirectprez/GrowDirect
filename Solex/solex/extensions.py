import redis
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_session import Session
from flask_mail import Mail
from sqlalchemy.orm import DeclarativeBase, sessionmaker, scoped_session
from sqlalchemy import create_engine


class Base(DeclarativeBase):
    pass


class Database:
    def __init__(self):
        self.engine = None
        self.session = None

    def init_app(self, app):
        self.engine = create_engine(
            app.config["SQLALCHEMY_DATABASE_URI"],
            **app.config.get("SQLALCHEMY_ENGINE_OPTIONS", {}),
        )
        self.session = scoped_session(sessionmaker(bind=self.engine, future=True))

        @app.teardown_appcontext
        def remove_session(exc=None):
            self.session.remove()


db = Database()
admin_login = LoginManager()
admin_login.login_view = "admin_auth.login"
customer_login = LoginManager()
customer_login.login_view = "account_auth.login"
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address)
server_session = Session()
mail = Mail()


def init_extensions(app):
    db.init_app(app)
    admin_login.init_app(app)
    customer_login.init_app(app)
    csrf.init_app(app)

    app.config["SESSION_REDIS"] = redis.Redis.from_url(app.config["VALKEY_URL"])
    server_session.init_app(app)

    storage_uri = app.config["VALKEY_URL"]
    limiter.storage_uri = storage_uri
    limiter.init_app(app)

    app.config.setdefault("MAIL_SERVER", app.config["SMTP_HOST"])
    app.config.setdefault("MAIL_PORT", app.config["SMTP_PORT"])
    app.config.setdefault("MAIL_DEFAULT_SENDER", app.config["SMTP_FROM"])
    mail.init_app(app)
