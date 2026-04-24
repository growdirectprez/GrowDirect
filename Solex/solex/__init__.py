from flask import Flask
from solex.config import resolve_config
from solex.extensions import init_extensions


def create_app(config_cls=None) -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config_cls or resolve_config())
    init_extensions(app)
    from solex.routes import api, storefront, cart as cart_routes, checkout as checkout_routes
    app.register_blueprint(api.bp)
    app.register_blueprint(storefront.bp)
    app.register_blueprint(cart_routes.bp)
    app.register_blueprint(checkout_routes.bp)
    from solex.extensions import csrf
    csrf.exempt(cart_routes.bp)
    csrf.exempt(checkout_routes.bp)
    return app
