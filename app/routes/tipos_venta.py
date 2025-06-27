from flask import Blueprint, jsonify, request
from app.db.conexion import get_db
import mysql.connector

bp_tipos_venta = Blueprint("tipos_venta", __name__)

def validar_tipo_venta(data):
    if not data or "nombre_tipo" not in data or not data["nombre_tipo"]:
        return False, "Falta el campo requerido: nombre_tipo"
    return True, None

@bp_tipos_venta.route("/", methods=["GET"])
def listar_tipos_venta():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tipo_venta")
        resultados = cursor.fetchall()
        cursor.close()
        return jsonify(resultados), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_tipos_venta.route("/<int:id>", methods=["GET"])
def listar_tipo_venta(id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tipo_venta WHERE id_tipo_venta = %s", (id,))
        resultado = cursor.fetchone()
        cursor.close()
        if resultado:
            return jsonify(resultado), 200
        return jsonify({"error": "Tipo de venta no encontrado"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_tipos_venta.route("/", methods=["POST"])
def guardar_tipo_venta():
    try:
        data = request.get_json(silent=True)
        valido, error = validar_tipo_venta(data)
        if not valido:
            return jsonify({"error": error}), 400

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO tipo_venta (nombre_tipo) VALUES (%s)",
            (data["nombre_tipo"],)
        )
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Tipo de venta creado correctamente"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_tipos_venta.route("/<int:id>", methods=["PUT"])
def actualizar_tipo_venta(id):
    try:
        data = request.get_json(silent=True)
        valido, error = validar_tipo_venta(data)
        if not valido:
            return jsonify({"error": error}), 400

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "UPDATE tipo_venta SET nombre_tipo = %s WHERE id_tipo_venta = %s",
            (data["nombre_tipo"], id)
        )
        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Tipo de venta no encontrado"}), 404
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Tipo de venta actualizado correctamente"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_tipos_venta.route("/<int:id>", methods=["DELETE"])
def eliminar_tipo_venta(id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("DELETE FROM tipo_venta WHERE id_tipo_venta = %s", (id,))
        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Tipo de venta no encontrado"}), 404
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Tipo de venta eliminado correctamente"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500