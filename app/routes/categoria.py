from flask import Blueprint, jsonify, request
from app.db.conexion import get_db

bp_categoria = Blueprint("categoria", __name__)

error_permiso = 'Método no permitido'


@bp_categoria.route("/", methods=["GET"])
def listar_categoria():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categoria")
    resultados = cursor.fetchall()
    cursor.close()
    return jsonify(resultados), 200

@bp_categoria.route("/<int:id>", methods=["GET"])
def listar_categoria_id(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categoria WHERE id_categoria = %s", (id,))
    resultado = cursor.fetchone()
    cursor.close()
    if resultado:
        return jsonify(resultado), 200
    else:
        return jsonify({"error": "Categoria no encontrado"}), 404
    
@bp_categoria.route("/", methods=["POST"])
def guardar_categoria():
    if request.method == 'POST':
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        data =  request.get_json()
        nombre_categoria = data.get('nombre_categoria')
        cursor.execute(
            "INSERT INTO categoria (nombre_categoria) VALUES (%s)", (nombre_categoria,))
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Categoria creado correctamente"}), 201
    return jsonify({"error": {error_permiso}}), 405

@bp_categoria.route("/<int:id>", methods=["PUT"])
def actualizar_categoria(id):
    if request.method == 'PUT':
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        data = request.get_json()
        nombre_categoria = data.get('nombre_categoria')
        
        cursor.execute(
            "UPDATE categoria SET nombre_categoria = %s WHERE id_categoria = %s",
            (nombre_categoria, id,))
        conn.commit()
        cursor.close()
        
        return jsonify({"mensaje": "Categoria actualizado correctamente"}), 200
    
    return jsonify({"error": {error_permiso}}), 405

@bp_categoria.route("/<int:id>", methods=["DELETE"])
def eliminar_categoria(id):
    if request.method == 'DELETE':
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("DELETE FROM categoria WHERE id_categoria = %s", (id,))
        conn.commit()
        cursor.close()
        
        return jsonify({"mensaje": "Categoria eliminado correctamente"}), 200
    
    return jsonify({"error": "Método no permitido"}), 405