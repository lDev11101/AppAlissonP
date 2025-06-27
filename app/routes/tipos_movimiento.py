from flask import Blueprint, jsonify, request
from app.db.conexion import get_db
import mysql.connector

bp_tipos_movimiento = Blueprint("tipos_movimiento", __name__)

def validar_tipo_movimiento(data):
    if not data or "nombre_tipo" not in data or not data["nombre_tipo"]:
        return False, "Falta el campo requerido: nombre_tipo"
    return True, None

@bp_tipos_movimiento.route("/", methods=["GET"])
def listar_tipos_movimiento():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tipo_movimiento")
        resultados = cursor.fetchall()
        cursor.close()
        return jsonify(resultados), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_tipos_movimiento.route("/<int:id>", methods=["GET"])
def listar_tipo_movimiento(id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tipo_movimiento WHERE id_tipo_movimiento = %s", (id,))
        resultado = cursor.fetchone()
        cursor.close()
        if resultado:
            return jsonify(resultado), 200
        return jsonify({"error": "Tipo de movimiento no encontrado"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_tipos_movimiento.route("/", methods=["POST"])
def guardar_tipo_movimiento():
    try:
        data = request.get_json(silent=True)
        valido, error = validar_tipo_movimiento(data)
        if not valido:
            return jsonify({"error": error}), 400

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO tipo_movimiento (nombre_tipo) VALUES (%s)",
            (data["nombre_tipo"],)
        )
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Tipo de movimiento creado correctamente"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_tipos_movimiento.route("/<int:id>", methods=["PUT"])
def actualizar_tipo_movimiento(id):
    try:
        data = request.get_json(silent=True)
        valido, error = validar_tipo_movimiento(data)
        if not valido:
            return jsonify({"error": error}), 400

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "UPDATE tipo_movimiento SET nombre_tipo = %s WHERE id_tipo_movimiento = %s",
            (data["nombre_tipo"], id)
        )
        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Tipo de movimiento no encontrado"}), 404
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Tipo de movimiento actualizado correctamente"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_tipos_movimiento.route("/<int:id>", methods=["DELETE"])
def eliminar_tipo_movimiento(id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("DELETE FROM tipo_movimiento WHERE id_tipo_movimiento = %s", (id,))
        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Tipo de movimiento no encontrado"}), 404
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Tipo de movimiento eliminado correctamente"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500