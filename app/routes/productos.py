from flask import Blueprint, jsonify, request
from app.db.conexion import get_db

bp_producto = Blueprint("productos", __name__)


@bp_producto.route("/", methods=["GET"])
def listar_productos():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM producto")
    resultados = cursor.fetchall()
    cursor.close()
    return jsonify(resultados), 200


@bp_producto.route("/<int:id>", methods=["GET"])
def listar_producto(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM producto WHERE id_producto = %s", (id,))
    resultado = cursor.fetchone()
    cursor.close()
    
    if resultado:
        return jsonify(resultado), 200
    else:
        return jsonify({"error": "Producto no encontrado"}), 404
    

@bp_producto.route("/", methods=["POST"])
def guardar_producto():
    if request.method == 'POST':
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        data =  request.get_json()
        id_categoria = data.get("id_categoria")
        nombre_producto = data.get('nombre_producto')
        precio_base = data.get("precio_base")
        
        cursor.execute(
            "INSERT INTO producto (id_categoria, nombre_producto, precio_base) VALUES (%s,%s,%s)",(id_categoria,nombre_producto,precio_base))
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Producto creado correctamente"}), 201
    
    return jsonify({"error": "Método no permitido"}), 405

@bp_producto.route("/<int:id>", methods=["PUT"])
def actualizar_producto(id):
    if request.method == 'PUT':
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        data = request.get_json()
        id_categoria = data.get("id_categoria")
        nombre_producto = data.get('nombre_producto')
        precio_base = data.get("precio_base")
        
        cursor.execute(
            "UPDATE producto SET id_categoria = %s, nombre_producto = %s, precio_base = %s WHERE id_producto = %s",
            (id_categoria, nombre_producto, precio_base, id))
        conn.commit()
        cursor.close()
        
        return jsonify({"mensaje": "Producto actualizado correctamente"}), 200
    
    return jsonify({"error": "Método no permitido"}), 405

@bp_producto.route("/<int:id>", methods=["DELETE"])
def eliminar_producto(id):
    if request.method == 'DELETE':
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("DELETE FROM producto WHERE id_producto = %s", (id,))
        conn.commit()
        cursor.close()
        
        return jsonify({"mensaje": "Producto eliminado correctamente"}), 200
    
    return jsonify({"error": "Método no permitido"}), 405