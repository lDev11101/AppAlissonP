from flask import Flask


def register_blueprints(app: Flask):
    from . import productos
    from . import categoria
    from . import inventario

    app.register_blueprint(productos.bp_producto, url_prefix="/api/productos")
    app.register_blueprint(categoria.bp_categoria, url_prefix="/api/categoria")
    app.register_blueprint(inventario.bp_inventario, url_prefix="/api/inventario")
