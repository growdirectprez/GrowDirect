"""Angel Flask app factory.

Note: Angel code actually lives in Cove (Angel is a Cove module).
This skeleton exists for reference only. The real app is in:
  ~/GrowDirect/Cove/cove/angel/

This file provided for scaffolding and local development reference.
"""

import os
import logging
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
session = Session()


def create_app(config_name="dev"):
    """Flask application factory."""
    app = Flask(__name__)

    # Load config
    config_module = f"angel.config.{_get_config_class(config_name).__name__}"
    app.config.from_object(_get_config_class(config_name))

    # Initialize extensions
    db.init_app(app)
    session.init_app(app)

    # Register blueprints
    from angel.routes.webhooks import angel_webhook_bp

    app.register_blueprint(angel_webhook_bp, url_prefix="/api/webhooks")

    # Create tables
    with app.app_context():
        db.create_all()

    # Logging
    if not app.debug:
        logging.basicConfig(level=logging.INFO)

    return app


def _get_config_class(config_name):
    """Get config class by name."""
    from angel.config import DevConfig, TestConfig, ProdConfig

    config_map = {
        "dev": DevConfig,
        "development": DevConfig,
        "test": TestConfig,
        "testing": TestConfig,
        "prod": ProdConfig,
        "production": ProdConfig,
    }
    return config_map.get(config_name.lower(), DevConfig)
