from flask import Blueprint, jsonify, request
from app.db.conexion import get_db
import mysql.connector

bp_categoria = Blueprint("categoria", __name__)

error_permiso = 'Método no permitido'


@bp_categoria.route("/", methods=["GET"])
def listar_categoria():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categoria")
        resultados = cursor.fetchall()
        cursor.close()
        return jsonify(resultados), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_categoria.route("/<int:id>", methods=["GET"])
def listar_categoria_id(id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categoria WHERE id_categoria = %s", (id,))
        resultado = cursor.fetchone()
        cursor.close()
        if resultado:
            return jsonify(resultado), 200
        else:
            return jsonify({"error": "Categoría no encontrada"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_categoria.route("/", methods=["POST"])
def guardar_categoria():
    try:
        data = request.get_json()
        if not data or "nombre_categoria" not in data:
            return jsonify({"error": "Falta el campo 'nombre_categoria'"}), 400

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO categoria (nombre_categoria) VALUES (%s)", (data["nombre_categoria"],)
        )
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Categoría creada correctamente"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_categoria.route("/<int:id>", methods=["PUT"])
def actualizar_categoria(id):
    try:
        data = request.get_json()
        if not data or "nombre_categoria" not in data:
            return jsonify({"error": "Falta el campo 'nombre_categoria'"}), 400

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "UPDATE categoria SET nombre_categoria = %s WHERE id_categoria = %s",
            (data["nombre_categoria"], id)
        )
        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Categoría no encontrada"}), 404
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Categoría actualizada correctamente"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_categoria.route("/<int:id>", methods=["DELETE"])
def eliminar_categoria(id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("DELETE FROM categoria WHERE id_categoria = %s", (id,))
        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Categoría no encontrada"}), 404
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Categoría eliminada correctamente"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500