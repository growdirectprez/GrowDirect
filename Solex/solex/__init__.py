from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    from solex.routes import api
    app.register_blueprint(api.bp)
    return app
