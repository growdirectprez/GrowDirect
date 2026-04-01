"""VIVA — Agentic Treasury Operations Engine.

App factory for the Flask dashboard/API service.
Signal workers and execution workers run as separate processes.
"""

import os

from flask import Flask

from viva.config import config_by_name
from viva.extensions import db, login_manager, csrf


def create_app(config_name: str | None = None) -> Flask:
    config_name = config_name or os.getenv("FLASK_ENV", "prod")
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from viva.public.routes import public_bp
    from viva.auth.routes import auth_bp
    from viva.dashboard.routes import dashboard_bp

    app.register_blueprint(public_bp, url_prefix="/")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

    from viva.models.strategy import Strategy  # noqa: F401
    from viva.models.trade import Trade  # noqa: F401
    from viva.models.position import Position  # noqa: F401
    from viva.models.signal import Signal  # noqa: F401
    from viva.models.council_verdict import CouncilVerdict  # noqa: F401

    @login_manager.user_loader
    def load_user(user_id):
        # VIVA is internal-only — Jeffe is the only user
        # Defer to platform auth when ready
        return None

    return app
