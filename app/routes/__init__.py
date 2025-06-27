from flask import Flask


def register_blueprints(app: Flask):
    from . import productos
    from . import categoria
    from . import inventario
    from . import usuario
    from . import venta
    from . import actividad
    from . import movimiento_almacen
    from . import herramienta
    from . import rol
    from . import tipos_venta
    from . import tipos_movimiento
    from . import estado
    from . import tipo_actividad

    app.register_blueprint(productos.bp_producto, url_prefix="/api/productos")
    app.register_blueprint(categoria.bp_categoria, url_prefix="/api/categorias")
    app.register_blueprint(inventario.bp_inventario, url_prefix="/api/inventarios")
    app.register_blueprint(usuario.bp_usuario, url_prefix="/api/usuarios")
    app.register_blueprint(venta.bp_venta, url_prefix="/api/ventas")
    app.register_blueprint(actividad.bp_actividad, url_prefix="/api/actividades")
    app.register_blueprint(movimiento_almacen.bp_movimiento, url_prefix="/api/movimientos_almacen")
    app.register_blueprint(herramienta.bp_herramienta, url_prefix="/api/herramientas")
    app.register_blueprint(rol.bp_roles, url_prefix="/api/roles")
    app.register_blueprint(tipos_venta.bp_tipos_venta, url_prefix="/api/tipos_venta")
    app.register_blueprint(tipos_movimiento.bp_tipos_movimiento, url_prefix="/api/tipos_movimiento")
    app.register_blueprint(estado.bp_estado, url_prefix="/api/estados")
    app.register_blueprint(tipo_actividad.bp_tipo_actividad, url_prefix="/api/tipo_actividad")
