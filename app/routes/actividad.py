from flask import Blueprint, jsonify, request
from app.db.conexion import get_db
import mysql.connector

bp_actividad = Blueprint("actividades", __name__)

def validar_actividad(data):
    campos_obligatorios = ["id_tipoactividad", "fecha"]
    if not data:
        return False, "No se recibió información"
    for campo in campos_obligatorios:
        if campo not in data or data[campo] in (None, ""):
            return False, f"Falta el campo requerido: {campo}"
    return True, None

@bp_actividad.route("/", methods=["GET"])
def listar_actividades():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM actividad")
        resultados = cursor.fetchall()
        cursor.close()
        return jsonify(resultados), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_actividad.route("/<int:id>", methods=["GET"])
def listar_actividad(id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM actividad WHERE id_actividad = %s", (id,))
        resultado = cursor.fetchone()
        cursor.close()
        if resultado:
            return jsonify(resultado), 200
        else:
            return jsonify({"error": "Actividad no encontrada"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_actividad.route("/", methods=["POST"])
def guardar_actividad():
    try:
        data = request.get_json()
        valido, error = validar_actividad(data)
        if not valido:
            return jsonify({"error": error}), 400

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "INSERT INTO actividad (id_tipoactividad, fecha, duracion, lote, personal, observaciones) VALUES (%s, %s, %s, %s, %s, %s)",
            (
                data["id_tipoactividad"],
                data["fecha"],
                data.get("duracion"),
                data.get("lote"),
                data.get("personal"),
                data.get("observaciones")
            )
        )
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Actividad creada correctamente"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_actividad.route("/<int:id>", methods=["PUT"])
def actualizar_actividad(id):
    try:
        data = request.get_json()
        valido, error = validar_actividad(data)
        if not valido:
            return jsonify({"error": error}), 400

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "UPDATE actividad SET id_tipoactividad = %s, fecha = %s, duracion = %s, lote = %s, personal = %s, observaciones = %s WHERE id_actividad = %s",
            (
                data["id_tipoactividad"],
                data["fecha"],
                data.get("duracion"),
                data.get("lote"),
                data.get("personal"),
                data.get("observaciones"),
                id
            )
        )
        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Actividad no encontrada"}), 404
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Actividad actualizada correctamente"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp_actividad.route("/<int:id>", methods=["DELETE"])
def eliminar_actividad(id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("DELETE FROM actividad WHERE id_actividad = %s", (id,))
        if cursor.rowcount == 0:
            cursor.close()
            return jsonify({"error": "Actividad no encontrada"}), 404
        conn.commit()
        cursor.close()
        return jsonify({"mensaje": "Actividad eliminada correctamente"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500