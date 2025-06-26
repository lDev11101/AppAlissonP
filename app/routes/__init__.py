from flask import Flask


def register_blueprints(app: Flask):
    from . import productos
    from . import categoria

    app.register_blueprint(productos.bp_producto, url_prefix="/api/productos")
    app.register_blueprint(categoria.bp_categoria, url_prefix="/api/categoria")
