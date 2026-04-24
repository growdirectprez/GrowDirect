from flask import Flask
from solex.config import resolve_config


def create_app(config_cls=None) -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config_cls or resolve_config())
    from solex.routes import api
    app.register_blueprint(api.bp)
    return app
