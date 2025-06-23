from flask import Flask


def register_blueprints(app: Flask):
    from . import productos

    app.register_blueprint(productos.bp_producto, url_prefix="/api/productos")
