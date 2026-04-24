from flask import Flask
from solex.config import resolve_config
from solex.extensions import init_extensions


def create_app(config_cls=None) -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config_cls or resolve_config())
    init_extensions(app)
    from solex.routes import api, storefront, cart as cart_routes, checkout as checkout_routes
    from solex.routes import admin_auth, account_auth
    from solex.routes import admin, admin_catalog, admin_orders, admin_inventory
    from solex.routes import admin_customers, admin_subscriptions, admin_returns
    app.register_blueprint(api.bp)
    app.register_blueprint(storefront.bp)
    app.register_blueprint(cart_routes.bp)
    app.register_blueprint(checkout_routes.bp)
    app.register_blueprint(admin_auth.bp)
    app.register_blueprint(account_auth.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(admin_catalog.bp)
    app.register_blueprint(admin_orders.bp)
    app.register_blueprint(admin_inventory.bp)
    app.register_blueprint(admin_customers.bp)
    app.register_blueprint(admin_subscriptions.bp)
    app.register_blueprint(admin_returns.bp)
    from solex.extensions import csrf
    csrf.exempt(api.bp)
    csrf.exempt(cart_routes.bp)
    csrf.exempt(checkout_routes.bp)
    csrf.exempt(admin_auth.bp)
    csrf.exempt(account_auth.bp)
    return app
