from flask import Blueprint, jsonify, request
from app.db.conexion import get_db
import mysql.connector

bp_herramienta = Blueprint("herramientas", __name__)

def validar_herramienta(data):
    campos = ["nombre"]
    if not data:
        return False, "No se recibió información"
    for campo in campos:
        if campo not in data or data[campo] in (None, ""):
            return False, f"Falta el campo requerido: {campo}"
    return True, None

@bp_herramienta.route("/", methods=["GET"])
def listar_herramientas():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM herramienta")
        resultados = cursor.fetchall()
        cursor.close()
        return jsonify(resultados), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_herramienta.route("/<int:id>", methods=["GET"])
def listar_herramienta(id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM herramienta WHERE id_herramienta = %s", (id,))
        resultado = cursor.fetchone()
        cursor.close()
        if resultado:
            return jsonify(resultado), 200
        return jsonify({"error": "Herramienta no encontrada"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_herramienta.route("/", methods=["POST"])
def guardar_herramienta():
    try:
        data = request.get_json(silent=True)
        valido, error = validar_herramienta(data)
        if not valido:
            return jsonify({"error": error}), 400

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO herramienta (nombre, id_estado, ubicacion, observaciones) VALUES (%s, %s, %s, %s)",
            (
                data["nombre"],
                data.get("id_estado"),
                data.get("ubicacion"),
                data.get("observaciones")
            )
        )
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Herramienta creada correctamente"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_herramienta.route("/<int:id>", methods=["PUT"])
def actualizar_herramienta(id):
    try:
        data = request.get_json(silent=True)
        valido, error = validar_herramienta(data)
        if not valido:
            return jsonify({"error": error}), 400

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "UPDATE herramienta SET nombre = %s, id_estado = %s, ubicacion = %s, observaciones = %s WHERE id_herramienta = %s",
            (
                data["nombre"],
                data.get("id_estado"),
                data.get("ubicacion"),
                data.get("observaciones"),
                id
            )
        )
        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Herramienta no encontrada"}), 404
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Herramienta actualizada correctamente"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_herramienta.route("/<int:id>", methods=["DELETE"])
def eliminar_herramienta(id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("DELETE FROM herramienta WHERE id_herramienta = %s", (id,))
        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Herramienta no encontrada"}), 404
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Herramienta eliminada correctamente"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return